#!/usr/bin/env python3
"""Build three deterministic ZIP packages from one canonical skill source.

The command is intentionally write-gated.  Without `--write` it exits without
creating or changing artifacts.  It uses only the Python standard library and
does not access the network.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


SKILL_ID = "thien-skill-risk-control-process"
DISPLAY_NAME = "Thien-Skill-Risk-Control-Process"
FIXED_ZIP_TIME = (2026, 8, 13, 0, 0, 0)
PACKAGE_LABELS = {
    "claude": "Claude",
    "chatgpt": "ChatGPT",
    "universal": "Universal",
}
EXCLUDED_NAMES = {".DS_Store", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
REQUIRED_FILES = {
    "SKILL.md", "LICENSE", "LICENSE-APPLICATION.md", "LICENSE-VERSION",
    "NOTICE", "THIRD-PARTY-NOTICES.md",
}


def scalar_field(path: Path, key: str, parent: str | None = None) -> str:
    """Read one simple metadata scalar, not arbitrary YAML or executable tags."""
    lines = path.read_text(encoding="utf-8").splitlines()
    indent = ""
    if parent is not None:
        matches = [i for i, line in enumerate(lines)
                   if re.fullmatch(re.escape(parent) + r":\s*(?:#.*)?", line)]
        if len(matches) != 1:
            raise RuntimeError(f"Expected one {parent!r} mapping in {path.name}.")
        start = matches[0] + 1
        end = next((i for i in range(start, len(lines))
                    if lines[i].strip() and not lines[i].startswith((" ", "#"))), len(lines))
        lines = lines[start:end]
        indent = "  "
    pattern = re.compile(re.escape(indent + key) + r":\s*(.*?)\s*$")
    values = [match.group(1) for line in lines if (match := pattern.fullmatch(line))]
    if len(values) != 1:
        raise RuntimeError(f"Expected one {parent + '.' if parent else ''}{key} in {path.name}.")
    value = values[0].split(" #", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def release_version(repo_root: Path, canonical: Path) -> str:
    manifest = repo_root / "RELEASE-MANIFEST.yaml"
    version = scalar_field(manifest, "skill_version", "release")
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", version):
        raise RuntimeError("release.skill_version must be a stable X.Y.Z version.")
    for key, expected in (("skill_id", SKILL_ID), ("canonical_source", f"skills/{SKILL_ID}")):
        if scalar_field(manifest, key, "release") != expected:
            raise RuntimeError(f"release.{key} does not match the canonical package.")
    registry = canonical / "integration" / "master-orchestrator-registry-entry.yaml"
    if scalar_field(registry, "version") != version:
        raise RuntimeError("Registry version does not match release.skill_version.")
    application = repo_root / "LICENSE-APPLICATION.md"
    if application.read_bytes() != (canonical / application.name).read_bytes():
        raise RuntimeError("Root and canonical LICENSE-APPLICATION.md differ.")
    covered = re.findall(r"^\- \*\*Covered skill versions:\*\* (.+)$",
                         application.read_text(encoding="utf-8"), re.MULTILINE)
    if len(covered) != 1 or version not in re.findall(r"`([^`]+)`", covered[0]):
        raise RuntimeError("LICENSE-APPLICATION.md does not cover the release version.")
    return version


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_check(command: list[str], label: str) -> dict[str, Any]:
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"{label} could not run: {exc}") from exc
    if completed.returncode != 0:
        detail = completed.stdout.strip() or completed.stderr.strip() or "no diagnostic output"
        raise RuntimeError(f"{label} failed (exit {completed.returncode}):\n{detail}")
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{label} did not return valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label} did not return a JSON object.")
    if payload.get("status") != "pass":
        raise RuntimeError(f"{label} returned status {payload.get('status')!r}.")
    return payload


def validate_before_build(repo_root: Path, canonical: Path) -> dict[str, Any]:
    validator = canonical / "scripts" / "validate_package.py"
    test_runner = repo_root / "scripts" / "run_tests.py"
    if not validator.is_file():
        raise RuntimeError(f"Package validator is missing: {validator}")
    if not test_runner.is_file():
        raise RuntimeError(f"Test runner is missing: {test_runner}")
    package_result = run_check(
        [
            sys.executable,
            str(validator),
            str(canonical),
            "--repo-root",
            str(repo_root),
            "--json",
        ],
        "Package validation",
    )
    test_result = run_check(
        [sys.executable, str(test_runner), "--repo-root", str(repo_root), "--json"],
        "Static checks and deterministic case registry (not behavioral execution)",
    )
    return {"package_validation": package_result, "case_registry": test_result}


def should_copy(relative: Path, include_agents: bool) -> bool:
    if any(part in EXCLUDED_NAMES for part in relative.parts):
        return False
    if relative.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    if not include_agents and relative.parts and relative.parts[0] == "agents":
        return False
    return True


def safe_relative_name(name: str) -> str:
    if (not name or "\\" in name or ":" in name
            or any(ord(char) < 32 or ord(char) == 127 for char in name)
            or any(part in ("", ".", "..") or part != part.rstrip(" .")
                   for part in name.split("/"))):
        raise RuntimeError(f"Unsafe or nonportable package path: {name!r}")
    return unicodedata.normalize("NFC", name).casefold()


def reject_symlink_chain(path: Path, boundary: Path) -> None:
    if path != boundary and boundary not in path.parents:
        raise RuntimeError(f"Path escapes repository boundary: {path}")
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise RuntimeError(f"Refusing symbolic link: {candidate}")
        if candidate == boundary:
            break


def snapshot_canonical(canonical: Path) -> dict[str, bytes]:
    reject_symlink_chain(canonical, canonical.parent.parent)
    if not canonical.is_dir():
        raise RuntimeError(f"Canonical skill directory is missing: {canonical}")
    snapshot: dict[str, bytes] = {}
    seen: set[str] = set()
    for source in sorted(canonical.rglob("*")):
        mode = source.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise RuntimeError(f"Refusing to package symbolic link: {source}")
        relative = source.relative_to(canonical)
        if not should_copy(relative, include_agents=True):
            continue
        name = relative.as_posix()
        normalized = safe_relative_name(name)
        if normalized in seen:
            raise RuntimeError(f"Case or Unicode path collision: {name!r}")
        seen.add(normalized)
        if stat.S_ISREG(mode):
            snapshot[name] = source.read_bytes()
        elif not stat.S_ISDIR(mode):
            raise RuntimeError(f"Refusing nonregular source entry: {source}")
    if not snapshot:
        raise RuntimeError("Canonical package contains no files.")
    return snapshot


def stage_snapshot(snapshot: dict[str, bytes], destination: Path, include_agents: bool) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for name, content in sorted(snapshot.items()):
        if should_copy(Path(name), include_agents):
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)


def file_hashes(snapshot: dict[str, bytes], include_agents: bool = True) -> dict[str, str]:
    return {name: hashlib.sha256(content).hexdigest() for name, content in sorted(snapshot.items())
            if should_copy(Path(name), include_agents)}


def zip_tree(source_root: Path, destination_zip: Path) -> dict[str, Any]:
    file_count = 0
    with zipfile.ZipFile(
        destination_zip,
        mode="x",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
            arcname = PurePosixPath(*source.relative_to(source_root).parts).as_posix()
            safe_relative_name(arcname)
            reject_symlink_chain(source, source_root)
            info = zipfile.ZipInfo(arcname, date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.create_system = 3
            archive.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            file_count += 1
    return {
        "file": destination_zip.name,
        "file_count": file_count,
        "size_bytes": destination_zip.stat().st_size,
        "sha256": sha256(destination_zip),
    }


def inspect_archive(path: Path, expected_prefix: str, agents_policy: str,
                    expected_hashes: dict[str, str]) -> dict[str, str]:
    with zipfile.ZipFile(path, "r") as archive:
        names = archive.namelist()
        if not names:
            raise RuntimeError(f"Archive is empty: {path.name}")
        if names != sorted(names) or len(names) != len(set(names)):
            raise RuntimeError(f"Archive entries must be sorted and unique: {path.name}")
        seen: set[str] = set()
        actual: dict[str, str] = {}
        for info in archive.infolist():
            normalized = safe_relative_name(info.filename)
            if normalized in seen:
                raise RuntimeError(f"Case or Unicode collision in archive: {info.filename}")
            seen.add(normalized)
            if not info.filename.startswith(expected_prefix):
                raise RuntimeError(f"Archive entry is outside {expected_prefix!r}: {info.filename}")
            if (info.create_system != 3 or info.external_attr >> 16 != 0o100644
                    or info.date_time != FIXED_ZIP_TIME or info.compress_type != zipfile.ZIP_DEFLATED
                    or info.extra or info.comment or info.flag_bits & 1):
                raise RuntimeError(f"Unsafe or nondeterministic ZIP metadata: {info.filename}")
            relative = info.filename[len(expected_prefix):]
            safe_relative_name(relative)
            actual[relative] = hashlib.sha256(archive.read(info)).hexdigest()
        if archive.comment or archive.testzip() is not None:
            raise RuntimeError(f"Archive comment or CRC integrity failure: {path.name}")
        missing = sorted(REQUIRED_FILES - actual.keys())
        if missing:
            raise RuntimeError(f"Archive {path.name} is missing required entries: {missing}")
        has_agents = any(name.startswith("agents/") for name in actual)
        if agents_policy == "required" and "agents/openai.yaml" not in actual:
            raise RuntimeError(f"Archive {path.name} must include agents/openai.yaml.")
        if agents_policy == "excluded" and has_agents:
            raise RuntimeError(f"Archive {path.name} must exclude agents/ metadata.")
        if agents_policy not in {"required", "excluded"}:
            raise RuntimeError(f"Unknown agents policy: {agents_policy}")
        if actual != expected_hashes:
            missing = sorted(expected_hashes.keys() - actual.keys())
            extra = sorted(actual.keys() - expected_hashes.keys())
            changed = sorted(name for name in actual.keys() & expected_hashes.keys()
                             if actual[name] != expected_hashes[name])
            raise RuntimeError(f"Normalized file parity failed for {path.name}: "
                               f"missing={missing}, extra={extra}, changed={changed}")
        return actual


def validate_staged_package(skill_root: Path, target: str) -> dict[str, Any]:
    validator = skill_root / "scripts" / "validate_package.py"
    return run_check(
        [
            sys.executable,
            str(validator),
            str(skill_root),
            "--target",
            target,
            "--json",
        ],
        f"Staged {target} package validation",
    )


def packaging_report(version: str, validation: dict[str, Any], packages: dict[str, Any],
                     canonical_hashes: dict[str, str]) -> dict[str, Any]:
    registry = validation["case_registry"]
    behavioral = registry.get("behavioral", {})
    if not isinstance(behavioral, dict):
        behavioral = {}
    return {
        "builder": "build_release.py",
        "report_kind": "packaging_verification",
        "status": "pass",
        "status_scope": "structural_registry_and_packaging_only",
        "skill_id": SKILL_ID,
        "version": version,
        "version_source": "RELEASE-MANIFEST.yaml:release.skill_version",
        "canonical_source": f"skills/{SKILL_ID}",
        "artifact_directory": f"dist/{version}",
        "validation": {
            "package": validation["package_validation"]["status"],
            "deterministic_case_registry": registry["status"],
            "registry_case_count": registry.get("case_count"),
            "version_and_license_application_parity": "pass",
            "normalized_file_parity": "pass",
            "archive_integrity": "pass",
            "safe_paths_and_no_symlinks": "pass",
        },
        "reproducibility": {
            "status": "pass",
            "builds_compared": 2,
            "scope": "Same canonical snapshot and Python/zlib runtime; byte-identical ZIPs.",
        },
        "behavioral": {
            "status": "not_evaluated_by_builder",
            "evidence_verified": False,
            "registry_reported_status": behavioral.get("status", "not_provided"),
            "note": "No model execution or behavioral/platform acceptance is inferred from packaging.",
        },
        "release_acceptance": "not_determined_by_builder",
        "canonical_file_sha256": canonical_hashes,
        "packages": packages,
        "checksums": "SHA256SUMS",
        "report_file": "packaging-report.json",
    }


def publish_artifacts(repo_root: Path, version: str, artifacts: Path) -> str:
    """Publish only a new version directory; an existing release is immutable."""
    dist = repo_root / "dist"
    destination = dist / version
    reject_symlink_chain(destination, repo_root)
    expected = {path.name: path.read_bytes() for path in artifacts.iterdir()}
    if destination.exists():
        if not destination.is_dir() or {path.name for path in destination.iterdir()} != expected.keys():
            raise RuntimeError(f"Existing release directory has different artifacts: {destination}")
        for name, content in expected.items():
            target = destination / name
            if target.is_symlink() or not target.is_file() or target.read_bytes() != content:
                raise RuntimeError(f"Refusing to overwrite different release artifact: {target}")
        return "unchanged"
    dist.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".release-{version}-", dir=dist) as temporary:
        staged = Path(temporary) / "artifacts"
        shutil.copytree(artifacts, staged)
        # Never merge into or replace an existing release, including partial output.
        if destination.exists() or destination.is_symlink():
            raise RuntimeError(f"Release destination appeared during build: {destination}")
        staged.rename(destination)
    return "created"


def build_packages(repo_root: Path) -> dict[str, Any]:
    canonical = repo_root / "skills" / SKILL_ID
    snapshot = snapshot_canonical(canonical)
    version = release_version(repo_root, canonical)
    validation = validate_before_build(repo_root, canonical)
    filenames = {key: f"{DISPLAY_NAME}-v{version}-{label}.zip"
                 for key, label in PACKAGE_LABELS.items()}
    package_results: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="thien-risk-process-control-release-") as temporary:
        staging = Path(temporary)
        artifacts = staging / "artifacts"
        artifacts.mkdir()
        repeated = staging / "repeated"
        repeated.mkdir()
        for target, filename in filenames.items():
            include_agents = target != "claude"
            prefix = f"{SKILL_ID}/" if target != "universal" else f".agents/skills/{SKILL_ID}/"
            expected = file_hashes(snapshot, include_agents)
            first_result: dict[str, Any] = {}
            for attempt in range(2):
                package_root = staging / f"build-{attempt}" / target
                skill_root = package_root / prefix.rstrip("/")
                stage_snapshot(snapshot, skill_root, include_agents)
                if attempt == 0:
                    validate_staged_package(skill_root, target)
                output = (artifacts if attempt == 0 else repeated) / filename
                result = zip_tree(package_root, output)
                inspect_archive(output, prefix, "required" if include_agents else "excluded", expected)
                if attempt == 0:
                    first_result = result
                elif result["sha256"] != first_result["sha256"]:
                    raise RuntimeError(f"Reproducibility check failed for {target}.")
            first_result.update({
                "archive_root": prefix,
                "validation": "pass",
                "normalized_file_sha256": expected,
                "canonical_exclusions": sorted(set(snapshot) - set(expected)),
            })
            package_results[target] = first_result
        report = packaging_report(version, validation, package_results, file_hashes(snapshot))
        checksum_lines = [f"{package_results[key]['sha256']}  {filenames[key]}" for key in filenames]
        (artifacts / "SHA256SUMS").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
        (artifacts / "packaging-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if snapshot_canonical(canonical) != snapshot or release_version(repo_root, canonical) != version:
            raise RuntimeError("Canonical source or release metadata changed during the build.")
        publication = publish_artifacts(repo_root, version, artifacts)
    return {**report, "publication": publication}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root (default: parent of scripts/).",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Create dist/<manifest-version>/; existing artifacts must be byte-identical.",
    )
    parser.add_argument("--json", action="store_true", help="Print the build result as JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.write:
        print("ERROR: --write is required; no files were changed.", file=sys.stderr)
        return 2
    try:
        result = build_packages(args.repo_root.resolve())
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        print(f"ERROR: release build failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Packaging checks: PASS (behavioral acceptance not evaluated)")
        for platform, package in result["packages"].items():
            print(
                f"  {platform:9} {package['file']} "
                f"({package['file_count']} files, sha256 {package['sha256']})"
            )
        print(f"  output {result['artifact_directory']} ({result['publication']})")
        print(f"  checksums {result['checksums']}; report {result['report_file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
