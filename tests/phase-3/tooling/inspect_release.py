#!/usr/bin/env python3
"""Read-only release content cross-check, separate from the ZIP builder."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import unicodedata
import zipfile


SKILL_ID = "thien-skill-risk-control-process"
# Retain the old public name for callers that imported the original inspector.
SKILL = SKILL_ID
BASELINE = "38e30011371d1aafe1f4b715c65fdd74b76b6396"
HISTORICAL_COVERED_VERSION = "1.1.1"
POLICY_FILE = "REPOSITORY-HYGIENE.json"
REGULAR_GIT_MODES = {"100644", "100755"}
PACKAGE_TARGETS = {"claude", "chatgpt", "universal-agents"}
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
VERSION_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")
APPROVED_HISTORICAL_RELOCATIONS = {
    "dist/SHA256SUMS": "dist/1.0.0/SHA256SUMS",
    "dist/Thien-Skill-Risk-Process-Control-v1.0.0-ChatGPT.zip": (
        "dist/1.0.0/Thien-Skill-Risk-Process-Control-v1.0.0-ChatGPT.zip"
    ),
    "dist/Thien-Skill-Risk-Process-Control-v1.0.0-Claude.zip": (
        "dist/1.0.0/Thien-Skill-Risk-Process-Control-v1.0.0-Claude.zip"
    ),
    "dist/Thien-Skill-Risk-Process-Control-v1.0.0-Universal.zip": (
        "dist/1.0.0/Thien-Skill-Risk-Process-Control-v1.0.0-Universal.zip"
    ),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _reject_duplicate_json_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Malformed policy: duplicate JSON key {key!r}")
        result[key] = value
    return result


def safe_relative_name(value: str, *, prefix: bool = False) -> str:
    """Return a repository-relative POSIX name or fail closed."""
    if type(value) is not str or not value:
        raise ValueError("Unsafe empty or non-string path")
    if unicodedata.normalize("NFC", value) != value:
        raise ValueError(f"Unsafe non-NFC path: {value!r}")
    if value.startswith("/") or "\\" in value or re.match(r"^[A-Za-z]:", value):
        raise ValueError(f"Unsafe path: {value!r}")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"Unsafe control character in path: {value!r}")
    if prefix:
        if not value.endswith("/"):
            raise ValueError(f"Malformed immutable prefix (missing trailing slash): {value!r}")
        check = value[:-1]
    else:
        if value.endswith("/"):
            raise ValueError(f"Unsafe file/directory path with trailing slash: {value!r}")
        check = value
    parts = check.split("/")
    if not check or any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"Unsafe path components: {value!r}")
    return value


def _normalized_alias(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def parse_hygiene_policy(data: bytes) -> dict[str, object]:
    """Parse the preservation policy strictly and return its immutable selectors."""
    try:
        raw = json.loads(data.decode("utf-8"), object_pairs_hook=_reject_duplicate_json_keys)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Malformed policy: {exc}") from exc
    if type(raw) is not dict or raw.get("schema_version") != "1.0":
        raise ValueError("Malformed policy: unsupported or missing schema_version")
    retention = raw.get("retention")
    if type(retention) is not dict:
        raise ValueError("Malformed policy: retention must be an object")
    prefixes = retention.get("immutable_historical_prefixes")
    files = retention.get("immutable_historical_files")
    relocations = raw.get("approved_historical_relocations", {})
    if type(prefixes) is not list or type(files) is not list:
        raise ValueError("Malformed policy: immutable prefixes/files must be arrays")
    if type(relocations) is not dict:
        raise ValueError("Malformed policy: approved_historical_relocations must be an object")

    validated_prefixes = tuple(safe_relative_name(item, prefix=True) for item in prefixes)
    validated_files = tuple(safe_relative_name(item) for item in files)
    for label, values in (("prefix", validated_prefixes), ("file", validated_files)):
        aliases = [_normalized_alias(value) for value in values]
        if len(aliases) != len(set(aliases)):
            raise ValueError(f"Malformed policy: duplicate immutable {label} selector")
    validated_relocations = {
        safe_relative_name(source): safe_relative_name(destination)
        for source, destination in relocations.items()
    }
    destination_aliases = [
        _normalized_alias(destination) for destination in validated_relocations.values()
    ]
    if len(destination_aliases) != len(set(destination_aliases)):
        raise ValueError("Malformed policy: duplicate historical relocation destination")
    return {
        "immutable_historical_prefixes": validated_prefixes,
        "immutable_historical_files": validated_files,
        "approved_historical_relocations": validated_relocations,
    }


def select_immutable_paths(
    baseline_paths,
    immutable_prefixes,
    immutable_files,
) -> list[str]:
    """Select only immutable paths that actually existed at the baseline."""
    exact = set(immutable_files)
    return sorted({
        path for path in baseline_paths
        if path in exact or any(path.startswith(prefix) for prefix in immutable_prefixes)
    })


def _repo_artifact(repo: Path, relative: str, expected: str) -> Path:
    """Resolve a required artifact without following symlinks at any component."""
    safe_relative_name(relative)
    current = repo
    parts = relative.split("/")
    for index, part in enumerate(parts):
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError as exc:
            raise ValueError(f"Missing artifact: {relative}") from exc
        if stat.S_ISLNK(mode):
            raise ValueError(f"Unsafe symbolic-link artifact: {relative}")
        final = index == len(parts) - 1
        if not final and not stat.S_ISDIR(mode):
            raise ValueError(f"Unsafe non-directory path component: {relative}")
        if final:
            if expected == "file" and not stat.S_ISREG(mode):
                raise ValueError(f"Unsafe special artifact (regular file required): {relative}")
            if expected == "directory" and not stat.S_ISDIR(mode):
                raise ValueError(f"Unsafe special artifact (directory required): {relative}")
    return current


def repo_file_bytes(repo: Path, relative: str) -> bytes:
    return _repo_artifact(repo, relative, "file").read_bytes()


def repo_directory(repo: Path, relative: str) -> Path:
    return _repo_artifact(repo, relative, "directory")


def yaml_file(path: Path):
    cmd = [
        "ruby", "-ryaml", "-rjson", "-rdate", "-e",
        "puts JSON.generate(YAML.safe_load(File.read(ARGV[0]), "
        "permitted_classes: [Date, Time], aliases: false))",
        str(path),
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def repo_yaml(repo: Path, relative: str):
    return yaml_file(_repo_artifact(repo, relative, "file"))


def git_bytes(repo: Path, path: str) -> bytes:
    safe_relative_name(path)
    return subprocess.run(
        ["git", "show", BASELINE + ":" + path],
        cwd=repo,
        capture_output=True,
        check=True,
    ).stdout


def baseline_tree(repo: Path) -> dict[str, tuple[str, str]]:
    result = subprocess.run(
        ["git", "ls-tree", "-r", "-z", "--full-tree", BASELINE],
        cwd=repo,
        capture_output=True,
        check=True,
    )
    entries: dict[str, tuple[str, str]] = {}
    aliases: set[str] = set()
    for raw_entry in result.stdout.split(b"\0"):
        if not raw_entry:
            continue
        try:
            metadata, raw_name = raw_entry.split(b"\t", 1)
            mode, object_type, _object_id = metadata.decode("ascii").split(" ", 2)
            name = raw_name.decode("utf-8")
        except (UnicodeError, ValueError) as exc:
            raise ValueError("Unsafe or malformed path in preservation baseline") from exc
        safe_relative_name(name)
        alias = _normalized_alias(name)
        if alias in aliases:
            raise ValueError(f"Unsafe duplicate/colliding baseline path: {name}")
        aliases.add(alias)
        entries[name] = (mode, object_type)
    if not entries:
        raise ValueError(f"Missing or empty preservation baseline: {BASELINE}")
    return entries


def snapshot_canonical(repo: Path, canonical_relative: str) -> dict[str, str]:
    root = repo_directory(repo, canonical_relative)
    result: dict[str, str] = {}
    aliases: set[str] = set()
    stack = [root]
    while stack:
        directory = stack.pop()
        with os.scandir(directory) as entries:
            for entry in sorted(entries, key=lambda item: item.name):
                path = Path(entry.path)
                relative = path.relative_to(root).as_posix()
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISLNK(mode):
                    raise ValueError(f"Unsafe symbolic-link artifact: {canonical_relative}/{relative}")
                if stat.S_ISDIR(mode):
                    if entry.name != "__pycache__":
                        stack.append(path)
                    continue
                if not stat.S_ISREG(mode):
                    raise ValueError(f"Unsafe special artifact: {canonical_relative}/{relative}")
                if entry.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
                    continue
                safe_relative_name(relative)
                alias = _normalized_alias(relative)
                if alias in aliases:
                    raise ValueError(f"Unsafe duplicate/colliding canonical path: {relative}")
                aliases.add(alias)
                result[relative] = sha(path.read_bytes())
    if not result:
        raise ValueError(f"Missing canonical release content: {canonical_relative}")
    return result


def validate_release_identity(release: dict) -> tuple[str, str, str]:
    if type(release) is not dict:
        raise ValueError("Malformed release manifest: release must be an object")
    if release.get("skill_id") != SKILL_ID:
        raise ValueError(f"Release skill_id must be {SKILL_ID}")
    version = release.get("skill_version")
    if type(version) is not str or VERSION_RE.fullmatch(version) is None:
        raise ValueError("Malformed release skill_version; expected X.Y.Z")
    canonical = release.get("canonical_source")
    expected_canonical = f"skills/{SKILL_ID}"
    if canonical != expected_canonical:
        raise ValueError(f"Release canonical_source must be {expected_canonical}")
    artifact_directory = release.get("artifact_directory")
    safe_relative_name(artifact_directory)
    return version, canonical, artifact_directory


def _license_label_versions(text: str, label: str) -> list[str]:
    pattern = re.compile(
        rf"(?m)^\s*-\s+\*\*{re.escape(label)}:\*\*\s*`([^`]+)`\.?\s*$"
    )
    return pattern.findall(text)


def license_application_covers(text: str, version: str) -> bool:
    historical = _license_label_versions(text, "Covered skill versions")
    current = _license_label_versions(text, "Current release covered version")
    return version in historical or version in current


def historical_license_label_preserved(text: str) -> bool:
    return _license_label_versions(text, "Covered skill versions") == [
        HISTORICAL_COVERED_VERSION
    ]


def parse_checksums(data: bytes) -> dict[str, str]:
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeError as exc:
        raise ValueError("Malformed SHA256SUMS encoding") from exc
    if not lines:
        raise ValueError("Missing checksum entries")
    checksums: dict[str, str] = {}
    aliases: set[str] = set()
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            raise ValueError(f"Malformed checksum entry: {line!r}")
        digest, name = match.groups()
        safe_relative_name(name)
        if "/" in name:
            raise ValueError(f"Unsafe checksum filename: {name!r}")
        alias = _normalized_alias(name)
        if name in checksums or alias in aliases:
            raise ValueError(f"Duplicate checksum entry: {name}")
        aliases.add(alias)
        checksums[name] = digest
    return checksums


def inspect_archive(data: bytes, prefix: str) -> tuple[dict[str, str], str | None]:
    safe_relative_name(prefix, prefix=True)
    actual: dict[str, str] = {}
    aliases: set[str] = set()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for entry in archive.infolist():
            name = entry.filename
            mode = entry.external_attr >> 16
            file_type = stat.S_IFMT(mode)
            unsafe = (
                not name.startswith(prefix)
                or bool(entry.flag_bits & 0x1)
                or stat.S_ISLNK(mode)
                or file_type not in {0, stat.S_IFREG}
            )
            relative = name[len(prefix):] if name.startswith(prefix) else name
            try:
                safe_relative_name(name)
                safe_relative_name(relative)
            except ValueError:
                unsafe = True
            alias = _normalized_alias(name)
            if alias in aliases:
                unsafe = True
            if unsafe:
                raise ValueError(f"Unsafe ZIP entry: {name!r}")
            aliases.add(alias)
            actual[relative] = sha(archive.read(entry))
        crc_error = archive.testzip()
    if crc_error is not None:
        raise ValueError(f"Corrupt ZIP entry: {crc_error}")
    return actual, crc_error


def check_links(repo: Path, relative: str) -> dict:
    path = _repo_artifact(repo, relative, "file")
    text = path.read_text(encoding="utf-8")
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
    return {
        "path": relative,
        "links_seen": len(links),
        "broken_local_targets": errors,
    }


def _preservation_map(
    repo: Path,
    paths: list[str],
    relocations: dict[str, str] | None = None,
) -> dict[str, bool]:
    relocations = {} if relocations is None else relocations
    result: dict[str, bool] = {}
    for baseline_path in paths:
        current_path = relocations.get(baseline_path, baseline_path)
        if current_path in result:
            raise ValueError(f"Duplicate preservation destination: {current_path}")
        result[current_path] = (
            sha(repo_file_bytes(repo, current_path)) == sha(git_bytes(repo, baseline_path))
        )
    return result


def inspect(repo: Path) -> dict:
    policy = parse_hygiene_policy(repo_file_bytes(repo, POLICY_FILE))
    tree = baseline_tree(repo)
    release_document = repo_yaml(repo, "RELEASE-MANIFEST.yaml")
    if type(release_document) is not dict or "release" not in release_document:
        raise ValueError("Malformed release manifest: missing release object")
    release = release_document["release"]
    version, canonical_relative, artifact_directory = validate_release_identity(release)
    expected = snapshot_canonical(repo, canonical_relative)
    registry = repo_yaml(
        repo,
        canonical_relative + "/integration/master-orchestrator-registry-entry.yaml",
    )

    repo_directory(repo, artifact_directory)
    sums = parse_checksums(repo_file_bytes(repo, artifact_directory + "/SHA256SUMS"))
    package_declarations = release.get("packages")
    if type(package_declarations) is not list:
        raise ValueError("Malformed release manifest: packages must be an array")
    targets, filenames = set(), set()
    packages = []
    for item in package_declarations:
        if type(item) is not dict:
            raise ValueError("Malformed release manifest: package must be an object")
        target = item.get("target")
        filename = item.get("filename")
        prefix = item.get("archive_root")
        declared_sha = item.get("sha256")
        if target not in PACKAGE_TARGETS or target in targets:
            raise ValueError(f"Malformed release package target: {target!r}")
        targets.add(target)
        expected_prefix = (
            f".agents/skills/{SKILL_ID}/"
            if target == "universal-agents"
            else f"{SKILL_ID}/"
        )
        if prefix != expected_prefix:
            raise ValueError(f"Malformed archive_root for package target {target}")
        safe_relative_name(filename)
        if "/" in filename or filename in filenames:
            raise ValueError(f"Unsafe or duplicate package filename: {filename!r}")
        filenames.add(filename)
        if type(declared_sha) is not str or SHA256_RE.fullmatch(declared_sha) is None:
            raise ValueError(f"Malformed package sha256: {filename}")
        data = repo_file_bytes(repo, artifact_directory + "/" + filename)
        actual, crc_error = inspect_archive(data, prefix)
        allow = {"agents/openai.yaml"} if target == "claude" else set()
        wanted = {key: value for key, value in expected.items() if key not in allow}
        packages.append({
            "target": target,
            "file": filename,
            "sha256": sha(data),
            "archive_root": prefix,
            "file_count": len(actual),
            "normalized_parity": actual == wanted,
            "metadata_checksum_match": (
                sha(data) == declared_sha == sums.get(filename)
            ),
            "unsafe_entries": [],
            "crc_error": crc_error,
            "canonical_exclusions": sorted(allow),
        })
    if targets != PACKAGE_TARGETS:
        raise ValueError("Missing release package target")
    if set(sums) != filenames:
        raise ValueError("Missing or unexpected checksum artifact")

    checks = {}
    checks["package_parity_roots_paths_crc"] = all(
        package["normalized_parity"] and package["crc_error"] is None
        for package in packages
    )
    checks["manifest_and_checksum"] = all(
        package["metadata_checksum_match"] for package in packages
    )
    checks["manifest_skill_id"] = release["skill_id"] == SKILL_ID
    checks["registry_version"] = registry["version"] == version
    checks["no_hard_specialist_dependency"] = registry.get("dependencies") == []
    checks["registry_not_installation_claim"] = (
        registry.get("runtime_verification", {}).get("verified") is False
    )

    root_application = repo_file_bytes(repo, "LICENSE-APPLICATION.md")
    canonical_application = repo_file_bytes(
        repo, canonical_relative + "/LICENSE-APPLICATION.md"
    )
    checks["license_application_parity"] = root_application == canonical_application
    application_text = root_application.decode("utf-8")
    checks["license_application_version"] = license_application_covers(
        application_text, version
    )
    checks["historical_license_coverage_label_preserved"] = (
        historical_license_label_preserved(application_text)
    )

    license_names = ["LICENSE", "LICENSE-VERSION", "NOTICE", "THIRD-PARTY-NOTICES.md"]
    preserved_paths = license_names + [
        f"{canonical_relative}/{name}" for name in license_names
    ]
    asset_prefix = canonical_relative + "/assets/"
    preserved_paths += sorted(path for path in tree if path.startswith(asset_prefix))
    missing_baseline_license_paths = [path for path in preserved_paths if path not in tree]
    if missing_baseline_license_paths:
        raise ValueError(
            "Missing license/NOTICE/assets artifact in baseline: "
            + ", ".join(missing_baseline_license_paths)
        )
    for path in preserved_paths:
        mode, object_type = tree[path]
        if mode not in REGULAR_GIT_MODES or object_type != "blob":
            raise ValueError(f"Unsafe special baseline preservation artifact: {path}")
    preserved = _preservation_map(repo, sorted(set(preserved_paths)))
    checks["license_terms_notice_logo_unchanged"] = all(preserved.values())

    immutable_paths = select_immutable_paths(
        tree,
        policy["immutable_historical_prefixes"],
        policy["immutable_historical_files"],
    )
    relocations = dict(APPROVED_HISTORICAL_RELOCATIONS)
    policy_relocations = policy["approved_historical_relocations"]
    conflicts = {
        source for source in relocations.keys() & policy_relocations.keys()
        if relocations[source] != policy_relocations[source]
    }
    if conflicts:
        raise ValueError(
            "Policy conflicts with an approved historical relocation: "
            + ", ".join(sorted(conflicts))
        )
    relocations.update(policy_relocations)
    unexpected_relocations = sorted(set(relocations) - set(immutable_paths))
    if unexpected_relocations:
        raise ValueError(
            "Historical relocation source is not an immutable baseline file: "
            + ", ".join(unexpected_relocations)
        )
    for path in immutable_paths:
        mode, object_type = tree[path]
        if mode not in REGULAR_GIT_MODES or object_type != "blob":
            raise ValueError(f"Unsafe special immutable baseline artifact: {path}")
    preserved_history = _preservation_map(repo, immutable_paths, relocations)
    checks["baseline_archives_and_tests_unchanged"] = all(preserved_history.values())

    links = [
        check_links(repo, path)
        for path in ["README.md", "INSTALL.md", "docs/phase-3/PLATFORM-GUIDANCE.md"]
    ]
    checks["release_docs_local_links"] = all(
        not item["broken_local_targets"] for item in links
    )
    checks["versioned_distribution_directory"] = (
        artifact_directory == "dist/" + version
    )
    required_new = [
        "references/external-process-control-libraries.md",
        "templates/control-baseline-comparison.yaml",
    ]
    checks["new_runtime_resources_present"] = all(path in expected for path in required_new)
    checks["no_phase_docs_or_test_payload_in_runtime"] = not any(
        name.startswith(("docs/", "tests/"))
        or "phase-1" in name
        or "phase-3" in name
        for name in expected
    )

    report = {
        "report_kind": "independent_read_only_release_content_check",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": version,
        "skill_id": SKILL_ID,
        "preservation_baseline": BASELINE,
        "preservation_policy": POLICY_FILE,
        "status": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "packages": packages,
        "preserved_license_asset_files": preserved,
        "preserved_historical_files": preserved_history,
        "immutable_historical_prefixes": list(policy["immutable_historical_prefixes"]),
        "immutable_historical_files": list(policy["immutable_historical_files"]),
        "approved_historical_relocations": relocations,
        "local_link_checks": links,
        "canonical_file_sha256": expected,
        "limitations": [
            "Not a model run, platform installation or behavioral acceptance.",
            "Hash and content checks do not establish legal enforceability or malware absence.",
            "External URLs are not fetched by this offline checker.",
            "Third-party provenance/content rights require separate human/analyst review.",
        ],
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    try:
        report = inspect(args.repo_root.resolve())
    except (
        OSError,
        ValueError,
        KeyError,
        subprocess.CalledProcessError,
        zipfile.BadZipFile,
    ) as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
