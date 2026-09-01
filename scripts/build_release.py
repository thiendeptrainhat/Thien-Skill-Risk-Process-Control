#!/usr/bin/env python3
"""Build three deterministic ZIP packages from one canonical skill source.

The command is intentionally mode-gated.  `--prepare` computes declarations in
temporary storage without repository writes; `--write` requires exact final
manifest hashes before immutable publication.  With neither mode it refuses to
run.  It uses only the Python standard library and does not access the network.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import unicodedata
import zipfile
import zlib
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
MANIFEST_TARGETS = {
    "claude": "claude",
    "chatgpt": "chatgpt",
    "universal-agents": "universal",
}
PACKAGE_FIELDS = {"target", "filename", "archive_root", "sha256"}
RELEASE_FIELDS = {
    "display_name", "skill_id", "skill_version", "application_date", "status",
    "artifact_directory", "source_repository", "license", "canonical_source",
    "packages", "verification", "publication",
}
RELEASE_FIELD_TYPES = {
    "display_name": str,
    "skill_id": str,
    "skill_version": str,
    "application_date": str,
    "status": str,
    "artifact_directory": str,
    "source_repository": dict,
    "license": dict,
    "canonical_source": str,
    "packages": list,
    "verification": dict,
    "publication": dict,
}
SOURCE_REPOSITORY_FIELDS = {
    "visibility": str,
    "url": str,
}
LICENSE_MANIFEST_FIELDS = {
    "id": str,
    "controlling_file": str,
    "application_file": str,
    "vietnamese_version_prevails": bool,
}
VERIFICATION_FIELDS = {
    "structural": str,
    "deterministic_case_registry": str,
    "behavioral_codex": str,
    "behavioral_claude": str,
    "behavioral_chatgpt": str,
    "archive_integrity": str,
    "native_installation_and_discovery": str,
    "fresh_context_behavioral_scenarios_reviewed_pass": int,
    "historical_model_variants_reviewed_pass_1_1_0": int,
    "tooling_tests_pass": int,
    "rename_regression_tests_pass": int,
    "qualification_report": str,
    "qualification_report_sha256": str,
    "evidence_report": str,
    "historical_report": str,
    "historical_release_gate_source": str,
    "scope": str,
}
PUBLICATION_FIELDS = {
    "local_artifacts": str,
    "github_commit_push": str,
    "git_tag": str,
    "github_release": str,
    "installed_skills": str,
}
QUALIFICATION_REPORT_FIELDS = {
    "schema_version", "release_version", "status", "source_bindings",
    "behavioral_evaluations", "deterministic_gates", "untested_surfaces",
    "limitations", "publication_authority",
}
SOURCE_BINDING_FIELDS = {"path", "sha256"}
BEHAVIORAL_EVALUATION_FIELDS = {
    "id", "output_path", "output_sha256", "status",
    "independent_executor", "independent_reviewer",
}
HYGIENE_LIMIT_FIELDS = {
    "max_file_bytes", "max_release_directory_bytes", "max_dist_bytes",
}
CANONICAL_REPOSITORY_URL = (
    "https://github.com/thiendeptrainhat/Thien-Skill-Risk-Control-Process"
)
CANONICAL_LICENSE = {
    "id": "LicenseRef-Tran-Ngoc-Thien-Skills-2.0",
    "controlling_file": "LICENSE",
    "application_file": "LICENSE-APPLICATION.md",
    "vietnamese_version_prevails": True,
}
HISTORICAL_LICENSE_COVERAGE_VERSION = "1.1.1"
WINDOWS_RESERVED_STEMS = {
    "con", "prn", "aux", "nul",
    *(f"com{digit}" for digit in "123456789"),
    *(f"lpt{digit}" for digit in "123456789"),
    *(f"com{digit}" for digit in "¹²³"),
    *(f"lpt{digit}" for digit in "¹²³"),
}
MAX_PACKAGE_PATH_BYTES = 240
MAX_PACKAGE_COMPONENT_BYTES = 255
EXCLUDED_NAMES = {".DS_Store", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
REQUIRED_FILES = {
    "SKILL.md", "LICENSE", "LICENSE-APPLICATION.md", "LICENSE-VERSION",
    "NOTICE", "THIRD-PARTY-NOTICES.md",
}


def validate_license_application_coverage(application_text: str, version: str) -> None:
    """Bind a release without rewriting the frozen 1.1.1 coverage declaration."""
    historical = re.findall(
        r"^- \*\*Covered skill versions:\*\*[^\r\n]*$",
        application_text,
        re.MULTILINE,
    )
    expected_historical = (
        "- **Covered skill versions:** "
        f"`{HISTORICAL_LICENSE_COVERAGE_VERSION}`."
    )
    if historical != [expected_historical]:
        raise RuntimeError(
            "LICENSE-APPLICATION.md must retain exactly one historical "
            f"Covered skill versions: {HISTORICAL_LICENSE_COVERAGE_VERSION} declaration."
        )

    current = re.findall(
        r"^- \*\*Current release covered version:\*\*[^\r\n]*$",
        application_text,
        re.MULTILINE,
    )
    expected_current = f"- **Current release covered version:** `{version}`."
    if version == HISTORICAL_LICENSE_COVERAGE_VERSION:
        if current not in ([], [expected_current]):
            raise RuntimeError(
                "LICENSE-APPLICATION.md current release coverage conflicts with "
                f"release version {version}."
            )
        return
    if current != [expected_current]:
        raise RuntimeError(
            "LICENSE-APPLICATION.md must contain exactly one Current release "
            f"covered version declaration for {version}."
        )


def _strip_yaml_comment(value: str) -> str:
    """Strip a YAML-subset comment without treating hashes in quotes as comments."""
    quote: str | None = None
    escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if quote == '"' and char == "\\":
            escaped = True
            continue
        if char in "\"'":
            if quote is None:
                quote = char
            elif quote == char:
                quote = None
            continue
        if char == "#" and quote is None and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
    if quote is not None:
        raise RuntimeError("Unterminated quoted scalar in RELEASE-MANIFEST.yaml.")
    return value.rstrip()


def _manifest_scalar(value: str, line_number: int) -> Any:
    """Parse the scalar subset used by RELEASE-MANIFEST.yaml with stdlib only."""
    value = _strip_yaml_comment(value).strip()
    if not value:
        raise RuntimeError(f"Empty manifest scalar at line {line_number}.")
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid quoted manifest scalar at line {line_number}.") from exc
        if not isinstance(parsed, str):
            raise RuntimeError(f"Manifest scalar at line {line_number} must be a string.")
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise RuntimeError(f"Invalid quoted manifest scalar at line {line_number}.")
        return value[1:-1].replace("''", "'")
    lowered = value.casefold()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "~"}:
        return None
    if re.fullmatch(r"-?(?:0|[1-9][0-9]*)", value):
        return int(value)
    if any(token in value for token in ("{", "}", "[", "]", "&", "*", "!", "|", ">")):
        raise RuntimeError(f"Unsupported manifest scalar syntax at line {line_number}.")
    return value


def _parse_manifest_block(lines: list[tuple[int, str, int]], start: int,
                          indent: int) -> tuple[Any, int]:
    """Parse mappings and lists from the deliberately small manifest YAML subset."""
    is_list = lines[start][1].startswith("- ")
    container: Any = [] if is_list else {}
    index = start
    while index < len(lines):
        current_indent, text, line_number = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise RuntimeError(
                f"Unexpected indentation in RELEASE-MANIFEST.yaml at line {line_number}."
            )
        if is_list:
            if not text.startswith("- "):
                break
            item_text = text[2:].strip()
            match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", item_text)
            if match is None or not match.group(2):
                raise RuntimeError(
                    f"Manifest list item at line {line_number} must start a mapping."
                )
            item = {match.group(1): _manifest_scalar(match.group(2), line_number)}
            index += 1
            if index < len(lines) and lines[index][0] > indent:
                child_indent = lines[index][0]
                continuation, index = _parse_manifest_block(lines, index, child_indent)
                if not isinstance(continuation, dict):
                    raise RuntimeError(
                        f"Manifest list continuation at line {line_number} must be a mapping."
                    )
                duplicate = item.keys() & continuation.keys()
                if duplicate:
                    raise RuntimeError(
                        f"Duplicate manifest field {sorted(duplicate)[0]!r} "
                        f"at line {line_number}."
                    )
                item.update(continuation)
            container.append(item)
            continue
        if text.startswith("- "):
            break
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", text)
        if match is None:
            raise RuntimeError(f"Invalid manifest mapping at line {line_number}.")
        key, raw_value = match.groups()
        if key in container:
            raise RuntimeError(f"Duplicate manifest field {key!r} at line {line_number}.")
        index += 1
        if raw_value:
            container[key] = _manifest_scalar(raw_value, line_number)
        else:
            if index >= len(lines) or lines[index][0] <= indent:
                raise RuntimeError(f"Manifest field {key!r} at line {line_number} has no value.")
            child_indent = lines[index][0]
            container[key], index = _parse_manifest_block(lines, index, child_indent)
    return container, index


def parse_release_manifest(path: Path, content: bytes | None = None) -> dict[str, Any]:
    """Parse RELEASE-MANIFEST.yaml without PyYAML or executable YAML features."""
    raw = path.read_bytes() if content is None else content
    try:
        manifest_text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("RELEASE-MANIFEST.yaml must be valid UTF-8.") from exc
    prepared: list[tuple[int, str, int]] = []
    for line_number, raw_line in enumerate(manifest_text.splitlines(), 1):
        if "\t" in raw_line:
            raise RuntimeError(
                f"Tabs are not allowed in RELEASE-MANIFEST.yaml at line {line_number}."
            )
        without_comment = _strip_yaml_comment(raw_line)
        if not without_comment.strip():
            continue
        indent = len(without_comment) - len(without_comment.lstrip(" "))
        if indent % 2:
            raise RuntimeError(
                f"Manifest indentation must use two-space levels at line {line_number}."
            )
        prepared.append((indent, without_comment.lstrip(" "), line_number))
    if not prepared or prepared[0][0] != 0:
        raise RuntimeError("RELEASE-MANIFEST.yaml must contain a root mapping.")
    parsed, index = _parse_manifest_block(prepared, 0, 0)
    if index != len(prepared) or not isinstance(parsed, dict):
        raise RuntimeError("RELEASE-MANIFEST.yaml must contain one root mapping.")
    unknown_root = set(parsed) - {"schema_version", "release"}
    if unknown_root:
        raise RuntimeError(f"Unknown root manifest field: {sorted(unknown_root)[0]!r}.")
    if set(parsed) != {"schema_version", "release"} or parsed["schema_version"] != "1.0":
        raise RuntimeError("RELEASE-MANIFEST.yaml must declare schema_version 1.0 and release.")
    if not isinstance(parsed["release"], dict):
        raise RuntimeError("Manifest release must be a mapping.")
    return parsed


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


def validate_exact_mapping(name: str, value: Any,
                           schema: dict[str, type]) -> dict[str, Any]:
    """Validate an exact manifest submapping, including bool/int separation."""
    if not isinstance(value, dict):
        raise RuntimeError(f"release.{name} must be a dict.")
    unknown = set(value) - set(schema)
    if unknown:
        raise RuntimeError(
            f"Unknown release.{name} field: {sorted(unknown)[0]!r}."
        )
    missing = set(schema) - set(value)
    if missing:
        raise RuntimeError(
            f"Missing release.{name} field: {sorted(missing)[0]!r}."
        )
    for field, expected_type in schema.items():
        item = value[field]
        if expected_type is int:
            valid_type = type(item) is int
        elif expected_type is bool:
            valid_type = type(item) is bool
        else:
            valid_type = isinstance(item, expected_type)
        if not valid_type:
            raise RuntimeError(
                f"release.{name}.{field} must be a {expected_type.__name__}."
            )
        if isinstance(item, str) and not item.strip():
            raise RuntimeError(f"release.{name}.{field} must not be empty.")
        if expected_type is int and item < 0:
            raise RuntimeError(f"release.{name}.{field} must not be negative.")
    return value


def release_declarations(repo_root: Path, canonical: Path, *,
                         allow_pending_hashes: bool = False) -> dict[str, Any]:
    """Load and bind publication-critical manifest declarations."""
    manifest = repo_root / "RELEASE-MANIFEST.yaml"
    manifest_bytes = manifest.read_bytes()
    parsed = parse_release_manifest(manifest, manifest_bytes)
    release = parsed["release"]
    unknown_release = set(release) - RELEASE_FIELDS
    if unknown_release:
        raise RuntimeError(f"Unknown release manifest field: {sorted(unknown_release)[0]!r}.")
    missing_release = RELEASE_FIELDS - set(release)
    if missing_release:
        raise RuntimeError(f"Missing release manifest field: {sorted(missing_release)[0]!r}.")
    for field, expected_type in RELEASE_FIELD_TYPES.items():
        value = release[field]
        if not isinstance(value, expected_type):
            raise RuntimeError(
                f"release.{field} must be a {expected_type.__name__}."
            )
        if ((isinstance(value, str) and not value.strip())
                or (isinstance(value, (dict, list)) and not value)):
            raise RuntimeError(f"release.{field} must not be empty.")
    version = release["skill_version"]
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", version):
        raise RuntimeError("release.skill_version must be a stable X.Y.Z version.")
    expected_release = {
        "display_name": DISPLAY_NAME,
        "skill_id": SKILL_ID,
        "canonical_source": f"skills/{SKILL_ID}",
        "artifact_directory": f"dist/{version}",
    }
    for key, expected in expected_release.items():
        if release[key] != expected:
            raise RuntimeError(f"release.{key} does not match the canonical package.")
    safe_relative_name(release["artifact_directory"])

    source_repository = validate_exact_mapping(
        "source_repository", release["source_repository"], SOURCE_REPOSITORY_FIELDS
    )
    if source_repository != {
        "visibility": "public", "url": CANONICAL_REPOSITORY_URL,
    }:
        raise RuntimeError("release.source_repository does not match the public canonical repository.")
    license_metadata = validate_exact_mapping(
        "license", release["license"], LICENSE_MANIFEST_FIELDS
    )
    if license_metadata != CANONICAL_LICENSE:
        raise RuntimeError("release.license does not match the canonical license declaration.")
    verification = validate_exact_mapping(
        "verification", release["verification"], VERIFICATION_FIELDS
    )
    publication = validate_exact_mapping(
        "publication", release["publication"], PUBLICATION_FIELDS
    )
    if not re.fullmatch(r"[0-9a-f]{64}", verification["qualification_report_sha256"]):
        raise RuntimeError("release.verification.qualification_report_sha256 is invalid.")
    safe_relative_name(verification["qualification_report"])

    packages = release["packages"]
    if not isinstance(packages, list):
        raise RuntimeError("release.packages must be a list.")
    declared_packages: dict[str, dict[str, str]] = {}
    for index, package in enumerate(packages):
        if not isinstance(package, dict):
            raise RuntimeError(f"release.packages[{index}] must be a mapping.")
        unknown_fields = set(package) - PACKAGE_FIELDS
        if unknown_fields:
            raise RuntimeError(
                f"Unknown package manifest field: {sorted(unknown_fields)[0]!r}."
            )
        missing_fields = PACKAGE_FIELDS - set(package)
        if missing_fields:
            raise RuntimeError(
                f"Missing package manifest field: {sorted(missing_fields)[0]!r}."
            )
        if any(not isinstance(package[field], str) for field in PACKAGE_FIELDS):
            raise RuntimeError(f"release.packages[{index}] fields must be strings.")
        manifest_target = package["target"]
        if manifest_target not in MANIFEST_TARGETS:
            raise RuntimeError(f"Unknown release package target: {manifest_target!r}.")
        target = MANIFEST_TARGETS[manifest_target]
        if target in declared_packages:
            raise RuntimeError(f"Duplicate release package target: {manifest_target!r}.")
        expected_filename = f"{DISPLAY_NAME}-v{version}-{PACKAGE_LABELS[target]}.zip"
        expected_root = (f".agents/skills/{SKILL_ID}/" if target == "universal"
                         else f"{SKILL_ID}/")
        if package["filename"] != expected_filename:
            raise RuntimeError(f"Package filename does not match target {manifest_target!r}.")
        if package["archive_root"] != expected_root:
            raise RuntimeError(f"Package archive_root does not match target {manifest_target!r}.")
        safe_relative_name(package["filename"])
        safe_relative_name(package["archive_root"].rstrip("/"))
        if package["sha256"] == "pending":
            if not allow_pending_hashes:
                raise RuntimeError(
                    f"Package sha256 is pending for target {manifest_target!r}; "
                    "pending is allowed only in --prepare mode."
                )
        elif not re.fullmatch(r"[0-9a-f]{64}", package["sha256"]):
            raise RuntimeError(f"Package sha256 is invalid for target {manifest_target!r}.")
        declared_packages[target] = {
            field: package[field] for field in sorted(PACKAGE_FIELDS)
        }
    expected_targets = set(PACKAGE_LABELS)
    if set(declared_packages) != expected_targets:
        missing_targets = sorted(expected_targets - set(declared_packages))
        raise RuntimeError(f"Missing release package targets: {missing_targets}.")

    registry = canonical / "integration" / "master-orchestrator-registry-entry.yaml"
    if scalar_field(registry, "version") != version:
        raise RuntimeError("Registry version does not match release.skill_version.")
    application = repo_root / "LICENSE-APPLICATION.md"
    if application.read_bytes() != (canonical / application.name).read_bytes():
        raise RuntimeError("Root and canonical LICENSE-APPLICATION.md differ.")
    validate_license_application_coverage(
        application.read_text(encoding="utf-8"),
        version,
    )
    qualification = validate_qualification_report(
        repo_root,
        version,
        verification,
    )
    return {
        "schema_version": parsed["schema_version"],
        "version": version,
        "display_name": release["display_name"],
        "artifact_directory": release["artifact_directory"],
        "packages": declared_packages,
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "manifest_structure": parsed,
        "qualification": qualification,
        "publication_metadata": publication,
    }


def release_version(repo_root: Path, canonical: Path) -> str:
    """Compatibility wrapper for callers that only need the bound version."""
    return release_declarations(repo_root, canonical)["version"]


def verify_package_declarations(declarations: dict[str, Any],
                                packages: dict[str, Any], *,
                                allow_pending_hashes: bool = False) -> None:
    """Require generated packages to match every predeclared publication identity/hash."""
    if set(packages) != set(declarations["packages"]):
        raise RuntimeError("Generated package target set differs from RELEASE-MANIFEST.yaml.")
    differences: list[str] = []
    for target, generated in packages.items():
        declared = declarations["packages"][target]
        for generated_key, declared_key in (
            ("file", "filename"), ("archive_root", "archive_root"), ("sha256", "sha256")
        ):
            if (generated_key == "sha256" and declared[declared_key] == "pending"
                    and allow_pending_hashes):
                continue
            if generated[generated_key] != declared[declared_key]:
                differences.append(
                    f"{target}.{generated_key} differs "
                    f"(declared={declared[declared_key]!r}, generated={generated[generated_key]!r})"
                )
    if differences:
        raise RuntimeError(
            "Generated packages differ from RELEASE-MANIFEST.yaml: " + "; ".join(differences)
        )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_check(command: list[str], label: str) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=180,
            env=environment,
        )
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
    normalized_name = unicodedata.normalize("NFC", name)
    components = normalized_name.split("/")
    if (not normalized_name or "\\" in normalized_name or ":" in normalized_name
            or any(ord(char) < 32 or ord(char) == 127 for char in normalized_name)
            or any(char in '<>"|?*' for char in normalized_name)
            or len(normalized_name.encode("utf-8")) > MAX_PACKAGE_PATH_BYTES
            or any(part in ("", ".", "..") or part != part.rstrip(" .")
                   or len(part.encode("utf-8")) > MAX_PACKAGE_COMPONENT_BYTES
                   or part.split(".", 1)[0].rstrip(" ").casefold() in WINDOWS_RESERVED_STEMS
                   for part in components)):
        raise RuntimeError(f"Unsafe or nonportable package path: {name!r}")
    return normalized_name.casefold()


def reject_symlink_chain(path: Path, boundary: Path) -> None:
    if path != boundary and boundary not in path.parents:
        raise RuntimeError(f"Path escapes repository boundary: {path}")
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise RuntimeError(f"Refusing symbolic link: {candidate}")
        if candidate == boundary:
            break


def read_regular_file_bytes(path: Path, boundary: Path, label: str) -> bytes:
    """Read a repository file without accepting path escape, links, or special files."""
    path = Path(os.path.abspath(os.fspath(path)))
    boundary = Path(os.path.abspath(os.fspath(boundary)))
    if path != boundary and boundary not in path.parents:
        raise RuntimeError(f"{label} escapes the repository: {path}")
    reject_symlink_chain(path, boundary)
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise RuntimeError(f"Cannot inspect {label}: {path}: {exc}") from exc
    if not stat.S_ISREG(metadata.st_mode):
        raise RuntimeError(f"{label} must be a regular file: {path}")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise RuntimeError(f"Cannot open {label}: {path}: {exc}") from exc
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise RuntimeError(f"{label} must be a regular file: {path}")
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            return handle.read()
    finally:
        os.close(descriptor)


def strict_json_bytes(data: bytes, label: str) -> Any:
    """Parse UTF-8 JSON while rejecting duplicate keys and non-finite values."""
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"Duplicate JSON key: {key}")
            value[key] = item
        return value

    def reject_constant(value: str) -> None:
        raise ValueError(f"Non-finite JSON value: {value}")

    try:
        text = data.decode("utf-8")
        return json.loads(
            text,
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError(f"Invalid strict JSON in {label}: {exc}") from exc


def _string_list(value: Any, field: str, *, nonempty: bool = True) -> list[str]:
    if (not isinstance(value, list)
            or (nonempty and not value)
            or not all(isinstance(item, str) and item.strip() for item in value)):
        qualifier = "a nonempty" if nonempty else "an"
        raise RuntimeError(f"{field} must be {qualifier} array of nonempty strings.")
    if len(set(value)) != len(value):
        raise RuntimeError(f"{field} must not contain duplicates.")
    return value


def load_hygiene_policy(repo_root: Path) -> dict[str, Any]:
    """Load the release-relevant hygiene policy with strict JSON semantics."""
    path = repo_root / "REPOSITORY-HYGIENE.json"
    raw = read_regular_file_bytes(path, repo_root, "repository hygiene policy")
    policy = strict_json_bytes(raw, "REPOSITORY-HYGIENE.json")
    if not isinstance(policy, dict) or policy.get("schema_version") != "1.0":
        raise RuntimeError("REPOSITORY-HYGIENE.json must be an object with schema_version 1.0.")
    junk_names = _string_list(policy.get("junk_names"), "junk_names", nonempty=False)
    junk_suffixes = _string_list(policy.get("junk_suffixes"), "junk_suffixes", nonempty=False)
    private_patterns = _string_list(
        policy.get("private_path_patterns"), "private_path_patterns", nonempty=True
    )
    _string_list(policy.get("excluded_roots"), "excluded_roots", nonempty=False)
    _string_list(
        policy.get("allowed_private_path_files"),
        "allowed_private_path_files",
        nonempty=False,
    )
    if any("/" in item or "\\" in item for item in [*junk_names, *junk_suffixes]):
        raise RuntimeError("Hygiene junk names and suffixes must not contain path separators.")
    limits = policy.get("limits")
    if not isinstance(limits, dict) or set(limits) != HYGIENE_LIMIT_FIELDS:
        raise RuntimeError(
            "REPOSITORY-HYGIENE.json limits must contain exactly "
            + ", ".join(sorted(HYGIENE_LIMIT_FIELDS))
            + "."
        )
    parsed_limits: dict[str, int] = {}
    for field in HYGIENE_LIMIT_FIELDS:
        value = limits[field]
        if type(value) is not int or value <= 0:
            raise RuntimeError(f"limits.{field} must be a positive integer.")
        parsed_limits[field] = value
    return {
        "junk_names": frozenset(junk_names),
        "junk_suffixes": tuple(junk_suffixes),
        "private_path_patterns": tuple(private_patterns),
        "limits": parsed_limits,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def repository_file(repo_root: Path, raw_path: Any, label: str) -> tuple[str, bytes]:
    if not isinstance(raw_path, str) or not raw_path:
        raise RuntimeError(f"{label} path must be a nonempty string.")
    normalized = safe_relative_name(raw_path)
    path = repo_root.joinpath(*PurePosixPath(raw_path).parts)
    return normalized, read_regular_file_bytes(path, repo_root, label)


def reject_private_path_bytes(data: bytes, patterns: tuple[str, ...], label: str) -> None:
    for pattern in patterns:
        encoded = pattern.encode("utf-8")
        if encoded in data:
            raise RuntimeError(f"Private-path pattern {pattern!r} is not permitted in {label}.")


def validate_qualification_report(repo_root: Path, version: str,
                                  verification: dict[str, Any]) -> dict[str, Any]:
    """Bind a passing, independently reviewed qualification report to this release."""
    policy = load_hygiene_policy(repo_root)
    report_path = verification["qualification_report"]
    _, raw = repository_file(repo_root, report_path, "qualification report")
    actual_hash = hashlib.sha256(raw).hexdigest()
    if actual_hash != verification["qualification_report_sha256"]:
        raise RuntimeError("Qualification report SHA-256 does not match the manifest.")
    reject_private_path_bytes(raw, policy["private_path_patterns"], "qualification report")
    report = strict_json_bytes(raw, "qualification report")
    if not isinstance(report, dict) or set(report) != QUALIFICATION_REPORT_FIELDS:
        raise RuntimeError(
            "Qualification report must contain exactly: "
            + ", ".join(sorted(QUALIFICATION_REPORT_FIELDS))
            + "."
        )
    if report["schema_version"] != "1.0":
        raise RuntimeError("Qualification report schema_version must be exactly '1.0'.")
    if report["release_version"] != version:
        raise RuntimeError("Qualification report release_version does not match the manifest.")
    if report["status"] != "pass":
        raise RuntimeError("Qualification report status must be 'pass'.")
    if report["publication_authority"] != "owner_authorized":
        raise RuntimeError("Qualification report publication_authority must be 'owner_authorized'.")

    bindings = report["source_bindings"]
    if not isinstance(bindings, list) or not bindings:
        raise RuntimeError("Qualification report source_bindings must be a nonempty list.")
    seen_bindings: set[str] = set()
    for index, binding in enumerate(bindings):
        if not isinstance(binding, dict) or set(binding) != SOURCE_BINDING_FIELDS:
            raise RuntimeError(
                f"source_bindings[{index}] must contain exactly path and sha256."
            )
        path_key, data = repository_file(
            repo_root, binding.get("path"), f"source_bindings[{index}]"
        )
        claimed = binding.get("sha256")
        if not isinstance(claimed, str) or not re.fullmatch(r"[0-9a-f]{64}", claimed):
            raise RuntimeError(f"source_bindings[{index}].sha256 is invalid.")
        if path_key in seen_bindings:
            raise RuntimeError("Qualification report source_bindings paths must be unique.")
        seen_bindings.add(path_key)
        if hashlib.sha256(data).hexdigest() != claimed:
            raise RuntimeError(f"source_bindings[{index}] bytes do not match the recorded SHA-256.")

    evaluations = report["behavioral_evaluations"]
    if not isinstance(evaluations, list) or not evaluations:
        raise RuntimeError("Qualification report behavioral_evaluations must be a nonempty list.")
    expected_count = verification["fresh_context_behavioral_scenarios_reviewed_pass"]
    if len(evaluations) != expected_count:
        raise RuntimeError(
            "Qualification behavioral evaluation count does not match the manifest."
        )
    seen_ids: set[str] = set()
    seen_outputs: set[str] = set()
    for index, evaluation in enumerate(evaluations):
        if not isinstance(evaluation, dict) or set(evaluation) != BEHAVIORAL_EVALUATION_FIELDS:
            raise RuntimeError(
                f"behavioral_evaluations[{index}] has an invalid field set."
            )
        evaluation_id = evaluation["id"]
        if not isinstance(evaluation_id, str) or not evaluation_id.strip():
            raise RuntimeError(f"behavioral_evaluations[{index}].id must be nonempty.")
        if evaluation_id in seen_ids:
            raise RuntimeError("Qualification behavioral evaluation IDs must be unique.")
        seen_ids.add(evaluation_id)
        output_key, output = repository_file(
            repo_root,
            evaluation["output_path"],
            f"behavioral_evaluations[{index}] output",
        )
        if output_key in seen_outputs:
            raise RuntimeError("Qualification behavioral output paths must be unique.")
        seen_outputs.add(output_key)
        output_hash = evaluation["output_sha256"]
        if not isinstance(output_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", output_hash):
            raise RuntimeError(f"behavioral_evaluations[{index}].output_sha256 is invalid.")
        if hashlib.sha256(output).hexdigest() != output_hash:
            raise RuntimeError(
                f"behavioral_evaluations[{index}] output bytes do not match the recorded SHA-256."
            )
        reject_private_path_bytes(
            output,
            policy["private_path_patterns"],
            f"behavioral_evaluations[{index}] output",
        )
        if evaluation["status"] != "pass":
            raise RuntimeError(f"behavioral_evaluations[{index}].status must be 'pass'.")
        if evaluation["independent_executor"] is not True:
            raise RuntimeError(
                f"behavioral_evaluations[{index}].independent_executor must be true."
            )
        if evaluation["independent_reviewer"] is not True:
            raise RuntimeError(
                f"behavioral_evaluations[{index}].independent_reviewer must be true."
            )

    gates = report["deterministic_gates"]
    if (not isinstance(gates, dict) or not gates
            or not all(isinstance(key, str) and key.strip() and value == "pass"
                       for key, value in gates.items())):
        raise RuntimeError(
            "Qualification report deterministic_gates must be a nonempty mapping of pass statuses."
        )
    untested = _string_list(report["untested_surfaces"], "untested_surfaces")
    limitations = _string_list(report["limitations"], "limitations")
    return {
        "status": "pass",
        "report": report_path,
        "sha256": actual_hash,
        "source_binding_count": len(bindings),
        "behavioral_evaluations_reviewed_pass": len(evaluations),
        "deterministic_gates": dict(sorted(gates.items())),
        "untested_surfaces": untested,
        "limitations": limitations,
        "publication_authority": report["publication_authority"],
        "hygiene_policy_sha256": policy["sha256"],
    }


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
    # TemporaryDirectory may be exposed through a platform alias such as macOS
    # /var -> /private/var.  Resolve only the trusted staging parent so that the
    # validator does not mistake that system alias for a package symlink.  Keep
    # the final skill-root component unresolved: its own preflight must still
    # reject a linked package root or any link inside the package.
    supplied_root = Path(os.path.abspath(os.fspath(skill_root)))
    try:
        trusted_parent = supplied_root.parent.resolve(strict=True)
    except OSError as exc:
        raise RuntimeError(
            f"Cannot canonicalize staged package parent: {supplied_root.parent}: {exc}"
        ) from exc
    validation_root = trusted_parent / supplied_root.name
    validator = validation_root / "scripts" / "validate_package.py"
    return run_check(
        [
            sys.executable,
            str(validator),
            str(validation_root),
            "--target",
            target,
            "--json",
        ],
        f"Staged {target} package validation",
    )


def runtime_provenance() -> dict[str, Any]:
    """Return host-neutral runtime facts needed to qualify reproducibility claims."""
    builder_path = Path(__file__).resolve()
    return {
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
        },
        "zlib": {
            "compile_version": zlib.ZLIB_VERSION,
            "runtime_version": getattr(zlib, "ZLIB_RUNTIME_VERSION", zlib.ZLIB_VERSION),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "architecture_bits": struct.calcsize("P") * 8,
        },
        "builder": {
            "file": "scripts/build_release.py",
            "sha256": sha256(builder_path),
        },
    }


def scan_hygiene_tree(root: Path, policy: dict[str, Any], label: str) -> int:
    """Return regular-file bytes while rejecting unsafe or disallowed entries."""
    root = Path(os.path.abspath(os.fspath(root)))
    reject_symlink_chain(root, root.parent)
    try:
        root_metadata = root.lstat()
    except OSError as exc:
        raise RuntimeError(f"Cannot inspect {label}: {root}: {exc}") from exc
    if not stat.S_ISDIR(root_metadata.st_mode):
        raise RuntimeError(f"{label} must be a directory: {root}")
    total = 0

    def walk(directory: Path, relative: PurePosixPath) -> None:
        nonlocal total
        try:
            with os.scandir(directory) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name)
        except OSError as exc:
            raise RuntimeError(f"Cannot inspect {label} {relative}: {exc}") from exc
        for entry in entries:
            name = entry.name
            child = directory / name
            child_relative = relative / name
            safe_relative_name(child_relative.as_posix())
            try:
                metadata = entry.stat(follow_symlinks=False)
            except OSError as exc:
                raise RuntimeError(f"Cannot inspect {label} entry {child_relative}: {exc}") from exc
            if stat.S_ISLNK(metadata.st_mode):
                raise RuntimeError(f"Symbolic link is not permitted in {label}: {child_relative}")
            if name in policy["junk_names"] or any(
                name.endswith(suffix) for suffix in policy["junk_suffixes"]
            ):
                raise RuntimeError(f"Repository junk is not permitted in {label}: {child_relative}")
            if stat.S_ISDIR(metadata.st_mode):
                walk(child, child_relative)
            elif stat.S_ISREG(metadata.st_mode):
                if metadata.st_size > policy["limits"]["max_file_bytes"]:
                    raise RuntimeError(
                        f"File exceeds limits.max_file_bytes in {label} "
                        f"({metadata.st_size} bytes): {child_relative}"
                    )
                total += metadata.st_size
            else:
                raise RuntimeError(f"Special file is not permitted in {label}: {child_relative}")

    walk(root, PurePosixPath())
    return total


def validate_staged_release_hygiene(repo_root: Path, version: str,
                                    artifacts: Path) -> dict[str, int | str]:
    """Gate staged artifacts and prospective dist size before any publication."""
    policy = load_hygiene_policy(repo_root)
    staged_size = scan_hygiene_tree(artifacts, policy, "staged release")
    if staged_size > policy["limits"]["max_release_directory_bytes"]:
        raise RuntimeError(
            "Staged release exceeds limits.max_release_directory_bytes "
            f"({staged_size} bytes)."
        )

    dist = repo_root / "dist"
    current_dist_size = 0
    replaced_release_size = 0
    if os.path.lexists(dist):
        current_dist_size = scan_hygiene_tree(dist, policy, "dist")
        existing = dist / version
        if os.path.lexists(existing):
            replaced_release_size = scan_hygiene_tree(
                existing, policy, f"existing dist/{version}"
            )
    prospective = current_dist_size - replaced_release_size + staged_size
    if prospective > policy["limits"]["max_dist_bytes"]:
        raise RuntimeError(
            "Prospective dist exceeds limits.max_dist_bytes "
            f"({prospective} bytes)."
        )
    return {
        "status": "pass",
        "staged_release_bytes": staged_size,
        "current_dist_bytes": current_dist_size,
        "replaced_same_version_bytes": replaced_release_size,
        "prospective_dist_bytes": prospective,
    }


def packaging_report(version: str, validation: dict[str, Any], packages: dict[str, Any],
                     canonical_hashes: dict[str, str],
                     qualification: dict[str, Any],
                     manifest_package_binding: str = "pass") -> dict[str, Any]:
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
            "release_manifest_package_binding": manifest_package_binding,
            "current_release_qualification": "pass",
            "staged_release_hygiene": "pass",
        },
        "runtime_provenance": runtime_provenance(),
        "reproducibility": {
            "status": "pass",
            "builds_compared": 2,
            "scope": "Same canonical snapshot and Python/zlib runtime; byte-identical ZIPs.",
        },
        "behavioral": {
            "status": "pass_via_retained_qualification_report",
            "evidence_verified": True,
            "qualification_report": qualification["report"],
            "qualification_report_sha256": qualification["sha256"],
            "fresh_context_scenarios_reviewed_pass": (
                qualification["behavioral_evaluations_reviewed_pass"]
            ),
            "registry_reported_status": behavioral.get("status", "not_provided"),
            "note": (
                "Builder verified retained report structure, hashes, independence flags and pass statuses; "
                "it does not authenticate executor identity or independently re-grade semantics."
            ),
        },
        "release_acceptance": "qualified_by_retained_report",
        "qualification": qualification,
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


def computed_release_declarations(declarations: dict[str, Any],
                                  packages: dict[str, Any]) -> dict[str, Any]:
    """Return copy-ready publication declarations using the generated ZIP hashes."""
    return {
        "display_name": declarations["display_name"],
        "skill_version": declarations["version"],
        "artifact_directory": declarations["artifact_directory"],
        "packages": [
            {
                "target": declarations["packages"][target]["target"],
                "filename": package["file"],
                "archive_root": package["archive_root"],
                "sha256": package["sha256"],
            }
            for target, package in packages.items()
        ],
    }


def _run_packaging(repo_root: Path, *, publish: bool,
                   allow_pending_hashes: bool) -> dict[str, Any]:
    canonical = repo_root / "skills" / SKILL_ID
    snapshot = snapshot_canonical(canonical)
    declarations = release_declarations(
        repo_root, canonical, allow_pending_hashes=allow_pending_hashes
    )
    version = declarations["version"]
    validation = validate_before_build(repo_root, canonical)
    filenames = {target: package["filename"]
                 for target, package in declarations["packages"].items()}
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
        verify_package_declarations(
            declarations, package_results, allow_pending_hashes=allow_pending_hashes
        )
        pending_hashes = any(
            package["sha256"] == "pending"
            for package in declarations["packages"].values()
        )
        manifest_binding = "pending_hashes_computed" if pending_hashes else "pass"
        report = packaging_report(
            version,
            validation,
            package_results,
            file_hashes(snapshot),
            declarations["qualification"],
            manifest_package_binding=manifest_binding,
        )
        checksum_lines = [
            f"{package_results[key]['sha256']}  {filenames[key]}" for key in filenames
        ]
        (artifacts / "SHA256SUMS").write_text(
            "\n".join(checksum_lines) + "\n", encoding="utf-8"
        )
        (artifacts / "packaging-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        validate_staged_release_hygiene(repo_root, version, artifacts)
        if (snapshot_canonical(canonical) != snapshot
                or release_declarations(
                    repo_root, canonical, allow_pending_hashes=allow_pending_hashes
                ) != declarations):
            raise RuntimeError("Canonical source or release metadata changed during the build.")
        publication = (publish_artifacts(repo_root, version, artifacts) if publish
                       else "not_performed_prepare_only")
    return {
        **report,
        "mode": "publish" if publish else "prepare",
        "publication": publication,
        "repository_writes": publish,
        "computed_release_declarations": computed_release_declarations(
            declarations, package_results
        ),
    }


def build_packages(repo_root: Path) -> dict[str, Any]:
    """Build and publish only when every manifest declaration is final and exact."""
    return _run_packaging(repo_root, publish=True, allow_pending_hashes=False)


def prepare_packages(repo_root: Path) -> dict[str, Any]:
    """Compute release declarations in temporary storage without repository writes."""
    return _run_packaging(repo_root, publish=False, allow_pending_hashes=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root (default: parent of scripts/).",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--write",
        action="store_true",
        help="Create dist/<manifest-version>/; existing artifacts must be byte-identical.",
    )
    mode.add_argument(
        "--prepare",
        action="store_true",
        help=("Build only in temporary storage and print computed package declarations; "
              "sha256: pending is accepted only in this mode."),
    )
    parser.add_argument("--json", action="store_true", help="Print the build result as JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.write and not args.prepare:
        print("ERROR: --write or --prepare is required; no files were changed.", file=sys.stderr)
        return 2
    try:
        result = (prepare_packages(args.repo_root.resolve()) if args.prepare
                  else build_packages(args.repo_root.resolve()))
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        print(f"ERROR: release build failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.prepare:
        print("Packaging preparation: PASS (temporary build only; repository not modified)")
        declarations = result["computed_release_declarations"]
        for package in declarations["packages"]:
            print(
                f"  {package['target']:16} {package['filename']} "
                f"sha256 {package['sha256']} root {package['archive_root']}"
            )
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
