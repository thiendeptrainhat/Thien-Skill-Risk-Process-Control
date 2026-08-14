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
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


SKILL_ID = "thien-skill-risk-process-control"
DISPLAY_NAME = "Thien-Skill-Risk-Process-Control"
VERSION = "1.0.0"
FIXED_ZIP_TIME = (2026, 8, 13, 0, 0, 0)
PACKAGE_NAMES = {
    "claude": f"{DISPLAY_NAME}-v{VERSION}-Claude.zip",
    "chatgpt": f"{DISPLAY_NAME}-v{VERSION}-ChatGPT.zip",
    "universal": f"{DISPLAY_NAME}-v{VERSION}-Universal.zip",
}
EXCLUDED_NAMES = {".DS_Store", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


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
        "Deterministic acceptance",
    )
    return {"package_validation": package_result, "deterministic_acceptance": test_result}


def should_copy(relative: Path, include_agents: bool) -> bool:
    if any(part in EXCLUDED_NAMES for part in relative.parts):
        return False
    if relative.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    if not include_agents and relative.parts and relative.parts[0] == "agents":
        return False
    return True


def copy_canonical(canonical: Path, destination: Path, include_agents: bool) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for source in sorted(canonical.rglob("*")):
        relative = source.relative_to(canonical)
        if not should_copy(relative, include_agents):
            continue
        if source.is_symlink():
            raise RuntimeError(f"Refusing to package symbolic link: {source}")
        target = destination / relative
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif source.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def zip_tree(source_root: Path, destination_zip: Path) -> dict[str, Any]:
    file_count = 0
    with zipfile.ZipFile(
        destination_zip,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
            arcname = PurePosixPath(*source.relative_to(source_root).parts).as_posix()
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


def inspect_archive(path: Path, expected_prefix: str, agents_policy: str) -> None:
    with zipfile.ZipFile(path, "r") as archive:
        names = archive.namelist()
        if not names:
            raise RuntimeError(f"Archive is empty: {path.name}")
        if any(not name.startswith(expected_prefix) for name in names):
            raise RuntimeError(f"Archive contains an entry outside {expected_prefix!r}: {path.name}")
        skill_prefix = expected_prefix
        required = {
            skill_prefix + "SKILL.md",
            skill_prefix + "LICENSE",
            skill_prefix + "LICENSE-APPLICATION.md",
            skill_prefix + "LICENSE-VERSION",
            skill_prefix + "NOTICE",
            skill_prefix + "THIRD-PARTY-NOTICES.md",
        }
        missing = sorted(required - set(names))
        if missing:
            raise RuntimeError(f"Archive {path.name} is missing required entries: {missing}")
        has_agents = any(name.startswith(skill_prefix + "agents/") for name in names)
        if agents_policy == "required" and not has_agents:
            raise RuntimeError(f"Archive {path.name} must include agents/ metadata.")
        if agents_policy == "excluded" and has_agents:
            raise RuntimeError(f"Archive {path.name} must exclude agents/ metadata.")


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


def build_packages(repo_root: Path) -> dict[str, Any]:
    canonical = repo_root / "skills" / SKILL_ID
    dist = repo_root / "dist"
    if not canonical.is_dir():
        raise RuntimeError(f"Canonical skill directory is missing: {canonical}")

    validation = validate_before_build(repo_root, canonical)
    dist.mkdir(parents=True, exist_ok=True)
    outputs = {key: dist / filename for key, filename in PACKAGE_NAMES.items()}

    with tempfile.TemporaryDirectory(prefix="thien-risk-process-control-release-") as temporary:
        staging = Path(temporary)

        claude_root = staging / "claude" / SKILL_ID
        copy_canonical(canonical, claude_root, include_agents=False)
        claude_validation = validate_staged_package(claude_root, "claude")
        claude_result = zip_tree(staging / "claude", outputs["claude"])
        claude_result["validation"] = claude_validation["status"]
        inspect_archive(outputs["claude"], f"{SKILL_ID}/", "excluded")

        chatgpt_root = staging / "chatgpt" / SKILL_ID
        copy_canonical(canonical, chatgpt_root, include_agents=True)
        chatgpt_validation = validate_staged_package(chatgpt_root, "chatgpt")
        chatgpt_result = zip_tree(staging / "chatgpt", outputs["chatgpt"])
        chatgpt_result["validation"] = chatgpt_validation["status"]
        inspect_archive(outputs["chatgpt"], f"{SKILL_ID}/", "required")

        universal_root = staging / "universal" / ".agents" / "skills" / SKILL_ID
        copy_canonical(canonical, universal_root, include_agents=True)
        universal_validation = validate_staged_package(universal_root, "universal")
        universal_result = zip_tree(staging / "universal", outputs["universal"])
        universal_result["validation"] = universal_validation["status"]
        inspect_archive(
            outputs["universal"],
            f".agents/skills/{SKILL_ID}/",
            "required",
        )

    package_results = {
        "claude": claude_result,
        "chatgpt": chatgpt_result,
        "universal": universal_result,
    }
    checksum_path = dist / "SHA256SUMS"
    checksum_lines = [
        f"{package_results[key]['sha256']}  {PACKAGE_NAMES[key]}"
        for key in ("claude", "chatgpt", "universal")
    ]
    checksum_path.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    return {
        "builder": "build_release.py",
        "status": "pass",
        "skill_id": SKILL_ID,
        "version": VERSION,
        "canonical_source": f"skills/{SKILL_ID}",
        "validation": {
            "package": validation["package_validation"].get("status"),
            "deterministic": validation["deterministic_acceptance"].get("status"),
        },
        "packages": package_results,
        "checksums": checksum_path.name,
    }


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
        help="Required safety gate: create/overwrite only the three named ZIPs and dist/SHA256SUMS.",
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
        print("Release build: PASS")
        for platform, package in result["packages"].items():
            print(
                f"  {platform:9} {package['file']} "
                f"({package['file_count']} files, sha256 {package['sha256']})"
            )
        print(f"  checksums {result['checksums']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
