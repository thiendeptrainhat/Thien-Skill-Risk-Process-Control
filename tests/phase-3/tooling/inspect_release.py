#!/usr/bin/env python3
"""Read-only release content cross-check, separate from the ZIP builder."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import unicodedata
import zipfile

SKILL = "thien-skill-risk-process-control"
BASELINE = "d65fad595e0265dbe665477b6a5747faa5811139"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def yaml_file(path):
    cmd = ["ruby", "-ryaml", "-rjson", "-rdate", "-e",
           "puts JSON.generate(YAML.safe_load(File.read(ARGV[0]), permitted_classes: [Date, Time], aliases: false))",
           str(path)]
    result = subprocess.run(cmd, text=True, capture_output=True, check=True)
    return json.loads(result.stdout)

def git_bytes(repo, path):
    return subprocess.run(["git", "show", BASELINE + ":" + path], cwd=repo,
                          capture_output=True, check=True).stdout

def check_links(repo, path):
    text = path.read_text()
    errors = []
    links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
    # URL strings are checked as links only; this script does not access network.
    for raw in links:
        target = raw.strip().strip("<>")
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        candidate = (path.parent / target).resolve()
        if not candidate.is_relative_to(repo) or not candidate.exists():
            errors.append(raw)
    return {"path": path.relative_to(repo).as_posix(), "links_seen": len(links),
            "broken_local_targets": errors}

def inspect(repo):
    release = yaml_file(repo / "RELEASE-MANIFEST.yaml")["release"]
    version = release["skill_version"]
    canonical = repo / release["canonical_source"]
    registry = yaml_file(canonical / "integration/master-orchestrator-registry-entry.yaml")
    expected = {p.relative_to(canonical).as_posix(): sha(p.read_bytes())
                for p in canonical.rglob("*") if p.is_file()
                and p.name not in {".DS_Store"} and "__pycache__" not in p.parts
                and p.suffix not in {".pyc", ".pyo"}}
    dist = repo / release["artifact_directory"]
    sums = {}
    for line in (dist / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        if name in sums:
            raise ValueError("Duplicate checksum entry")
        sums[name] = digest
    checks, packages = {}, []
    for item in release["packages"]:
        path = dist / item["filename"]
        data = path.read_bytes()
        prefix = item["archive_root"]
        actual, unsafe, aliases = {}, [], set()
        with zipfile.ZipFile(path) as archive:
            for entry in archive.infolist():
                name = entry.filename
                parts = PurePosixPath(name).parts
                alias = unicodedata.normalize("NFC", name).casefold()
                mode = entry.external_attr >> 16
                if (name.startswith("/") or ".." in parts or "\\" in name
                    or not name.startswith(prefix) or alias in aliases
                    or stat.S_ISLNK(mode) or not stat.S_ISREG(mode)):
                    unsafe.append(name)
                aliases.add(alias)
                actual[name[len(prefix):]] = sha(archive.read(entry))
            crc_error = archive.testzip()
        allow = {"agents/openai.yaml"} if item["target"] == "claude" else set()
        wanted = {k: v for k, v in expected.items() if k not in allow}
        parity = actual == wanted
        metadata_ok = sha(data) == item["sha256"] == sums.get(path.name)
        packages.append({"target": item["target"], "file": path.name, "sha256": sha(data),
                         "archive_root": prefix, "file_count": len(actual),
                         "normalized_parity": parity, "metadata_checksum_match": metadata_ok,
                         "unsafe_entries": unsafe, "crc_error": crc_error,
                         "canonical_exclusions": sorted(allow)})
    checks["package_parity_roots_paths_crc"] = all(p["normalized_parity"] and not p["unsafe_entries"]
                                                   and p["crc_error"] is None for p in packages)
    checks["manifest_and_checksum"] = len(sums) == 3 and len(packages) == 3 and all(
        p["metadata_checksum_match"] for p in packages)
    checks["registry_version"] = registry["version"] == version
    checks["no_hard_specialist_dependency"] = registry.get("dependencies") == []
    checks["registry_not_installation_claim"] = registry.get("runtime_verification", {}).get("verified") is False
    app = (repo / "LICENSE-APPLICATION.md").read_bytes()
    checks["license_application_parity"] = app == (canonical / "LICENSE-APPLICATION.md").read_bytes()
    checks["license_application_version"] = ("Covered skill versions:** `" + version + "`") in app.decode()
    preserved_paths = ["LICENSE", "LICENSE-VERSION", "NOTICE", "THIRD-PARTY-NOTICES.md"]
    preserved_paths += [f"skills/{SKILL}/" + x for x in preserved_paths]
    preserved_paths += [p.relative_to(repo).as_posix() for p in (canonical / "assets").iterdir() if p.is_file()]
    preserved = {p: sha((repo / p).read_bytes()) == sha(git_bytes(repo, p)) for p in preserved_paths}
    checks["license_terms_notice_logo_unchanged"] = all(preserved.values())
    history = subprocess.run(["git", "ls-tree", "-r", "--name-only", BASELINE, "dist", "tests"],
                             cwd=repo, text=True, capture_output=True, check=True).stdout.splitlines()
    preserved_history = {p: sha((repo / p).read_bytes()) == sha(git_bytes(repo, p)) for p in history}
    checks["baseline_archives_and_tests_unchanged"] = all(preserved_history.values())
    links = [check_links(repo, repo / p) for p in ["README.md", "INSTALL.md", "docs/phase-3/PLATFORM-GUIDANCE.md"]]
    checks["release_docs_local_links"] = all(not item["broken_local_targets"] for item in links)
    checks["versioned_distribution_directory"] = release["artifact_directory"] == "dist/" + version
    required_new = ["references/external-process-control-libraries.md", "templates/control-baseline-comparison.yaml"]
    checks["new_runtime_resources_present"] = all(p in expected for p in required_new)
    checks["no_phase_docs_or_test_payload_in_runtime"] = not any(
        n.startswith(("docs/", "tests/")) or "phase-1" in n or "phase-3" in n for n in expected)
    report = {"report_kind": "independent_read_only_release_content_check",
              "timestamp": datetime.now(timezone.utc).isoformat(), "version": version,
              "status": "pass" if all(checks.values()) else "fail", "checks": checks,
              "packages": packages, "preserved_license_asset_files": preserved,
              "preserved_historical_files": preserved_history, "local_link_checks": links,
              "canonical_file_sha256": expected,
              "limitations": ["Not a model run, platform installation or behavioral acceptance.",
                              "Hash and content checks do not establish legal enforceability or malware absence.",
                              "External URLs are not fetched by this offline checker.",
                              "Third-party provenance/content rights require separate human/analyst review."]}
    return report

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = ap.parse_args()
    try:
        report = inspect(args.repo_root.resolve())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1

if __name__ == "__main__":
    raise SystemExit(main())
