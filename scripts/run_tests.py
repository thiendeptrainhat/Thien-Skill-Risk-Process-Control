#!/usr/bin/env python3
"""Run legacy static checks, or validate separately retained Phase 3 evidence.

`tests/cases.yaml` is deliberately JSON-compatible YAML so it can be validated
without third-party dependencies.  This runner never executes behavioral model
tests.  Selected behavioral cases remain explicitly `not_run` until a separate
forward-testing activity records real observations. --phase3 validates receipts
against the approved upgrade matrix; it does not execute models or replace the
104-case registry, 28 historical summaries, or old result files.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safe_filesystem import (
    absolute_no_resolve, atomic_write_many, read_regular_bytes, reject_symlink_chain,
)


EXPECTED_COUNTS = {
    "A": 10,
    "B": 8,
    "C": 8,
    "D": 10,
    "E": 6,
    "F": 6,
    "G": 8,
    "H": 8,
    "I": 8,
    "J": 8,
    "K": 10,
    "L": 5,
    "M": 9,
}
REQUIRED_FIELDS = {
    "id",
    "family",
    "input",
    "mode",
    "expected_classification",
    "expected_workflow",
    "expected_risks",
    "expected_controls",
    "expected_handoff",
    "expected_approval_gate",
    "expected_non_action",
    "expected_output",
    "risk_level",
    "behavioral_selected",
}
ALLOWED_MODES = {
    "document-analysis",
    "current-state-discovery",
    "risk-control-analysis",
    "target-state-design",
    "rcm",
    "sod",
    "spof-dependency",
    "audit-support",
    "advisory",
    "assessment",
    "training",
}
ALLOWED_RISK_LEVELS = {"low", "medium", "high", "critical"}
CASE_ID_RE = re.compile(r"^(?:RPC-|TC-)?([A-M])[-_]?(\d{2,3})$")
COVERAGE_ROW_RE = re.compile(r"^\|\s*`([A-M]\d{2})`\s*\|", re.MULTILINE)
HYGIENE_POLICY_NAME = "REPOSITORY-HYGIENE.json"


class TestReport:
    def __init__(self) -> None:
        self.errors: list[dict[str, Any]] = []
        self.checks: dict[str, str] = {}
        self.case_results: list[dict[str, Any]] = []
        self.validator: dict[str, Any] | None = None

    def error(self, code: str, message: str, case_id: str | None = None) -> None:
        item: dict[str, Any] = {"code": code, "message": message}
        if case_id:
            item["case_id"] = case_id
        self.errors.append(item)

    def mark(self, check: str, before: int) -> None:
        self.checks[check] = "pass" if len(self.errors) == before else "fail"


def normalized_policy_path(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError(f"{field} entries must be non-empty repository-relative POSIX paths")
    path = Path(value)
    if path.is_absolute() or value.startswith("/") or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"{field} contains an unsafe path: {value!r}")
    normalized = path.as_posix()
    if normalized != value:
        raise ValueError(f"{field} path is not normalized: {value!r}")
    return normalized


def unique_string_list(value: Any, field: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{field} must be an array of strings")
    if (not allow_empty and not value) or any(not item or "\x00" in item for item in value):
        raise ValueError(f"{field} entries must be non-empty strings")
    if len(set(value)) != len(value):
        raise ValueError(f"{field} must not contain duplicates")
    return value


def load_hygiene_policy(repo_root: Path) -> dict[str, Any]:
    path = repo_root / HYGIENE_POLICY_NAME
    data = read_regular_bytes(path, repo_root, "repository hygiene policy")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"Duplicate policy key: {key}")
            value[key] = item
        return value

    def reject_constant(value: str) -> None:
        raise ValueError(f"Non-finite policy value: {value}")

    try:
        policy = json.loads(
            data,
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Malformed {HYGIENE_POLICY_NAME}: {exc}") from exc
    if not isinstance(policy, dict):
        raise ValueError(f"{HYGIENE_POLICY_NAME} root must be an object")
    if policy.get("schema_version") != "1.0":
        raise ValueError("schema_version must be exactly '1.0'")

    junk_names = unique_string_list(policy.get("junk_names"), "junk_names", allow_empty=True)
    junk_suffixes = unique_string_list(policy.get("junk_suffixes"), "junk_suffixes", allow_empty=True)
    if any("/" in item or "\\" in item for item in [*junk_names, *junk_suffixes]):
        raise ValueError("junk_names and junk_suffixes must contain basenames/suffixes, not paths")

    excluded_raw = unique_string_list(policy.get("excluded_roots"), "excluded_roots", allow_empty=True)
    excluded_roots = [normalized_policy_path(item, "excluded_roots") for item in excluded_raw]
    private_patterns = unique_string_list(
        policy.get("private_path_patterns", []),
        "private_path_patterns",
        allow_empty=True,
    )
    allowed_private_raw = unique_string_list(
        policy.get("allowed_private_path_files", []),
        "allowed_private_path_files",
        allow_empty=True,
    )
    allowed_private = [
        normalized_policy_path(item, "allowed_private_path_files") for item in allowed_private_raw
    ]

    limits = policy.get("limits")
    if not isinstance(limits, dict):
        raise ValueError("limits must be an object")
    parsed_limits: dict[str, int] = {}
    for name in ("max_file_bytes", "max_release_directory_bytes", "max_dist_bytes"):
        value = limits.get(name)
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"limits.{name} must be a positive integer")
        parsed_limits[name] = value

    return {
        "junk_names": frozenset(junk_names),
        "junk_suffixes": tuple(junk_suffixes),
        "excluded_roots": frozenset(excluded_roots),
        # These fields are validated for a future immutable-occurrence manifest.
        # They are deliberately not used for a blanket content scan: the current
        # repository contains frozen historical receipts that cannot be rewritten,
        # while a broad Phase-3 exclusion would silently exempt future evidence.
        "private_path_patterns": tuple(private_patterns),
        "allowed_private_path_files": frozenset(allowed_private),
        "limits": parsed_limits,
    }


def validate_repository_hygiene(repo_root: Path, report: TestReport) -> bool:
    """Apply the root hygiene policy without following any symbolic link."""
    before = len(report.errors)
    repo_root = absolute_no_resolve(repo_root)
    try:
        reject_symlink_chain(repo_root, "repository root")
        metadata = repo_root.lstat()
        if not stat.S_ISDIR(metadata.st_mode):
            raise ValueError(f"Repository root is not a directory: {repo_root}")
        policy = load_hygiene_policy(repo_root)
    except (OSError, ValueError) as exc:
        report.error("hygiene-policy", str(exc))
        report.mark("repository_hygiene", before)
        return False

    release_sizes: dict[str, int] = {}
    dist_size = 0

    def walk(directory: Path, relative: Path) -> None:
        nonlocal dist_size
        try:
            with os.scandir(directory) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name)
        except OSError as exc:
            report.error("hygiene-scan", f"Cannot inspect {relative.as_posix() or '.'}: {exc}")
            return
        for entry in entries:
            child = directory / entry.name
            child_relative = relative / entry.name
            child_name = entry.name
            child_key = child_relative.as_posix()
            try:
                child_metadata = entry.stat(follow_symlinks=False)
            except OSError as exc:
                report.error("hygiene-scan", f"Cannot inspect {child_key}: {exc}")
                continue

            if stat.S_ISLNK(child_metadata.st_mode):
                report.error("hygiene-symlink", f"Symbolic link is not permitted: {child_key}")
                continue
            if child_name in policy["junk_names"] or any(
                child_name.endswith(suffix) for suffix in policy["junk_suffixes"]
            ):
                report.error("hygiene-junk", f"Repository junk is not permitted: {child_key}")

            if child_key in policy["excluded_roots"]:
                continue
            if stat.S_ISDIR(child_metadata.st_mode):
                walk(child, child_relative)
                continue
            if not stat.S_ISREG(child_metadata.st_mode):
                report.error("hygiene-special", f"Special file is not permitted: {child_key}")
                continue

            size = child_metadata.st_size
            if size > policy["limits"]["max_file_bytes"]:
                report.error(
                    "hygiene-file-size",
                    f"File exceeds limits.max_file_bytes ({size} bytes): {child_key}",
                )
            if child_relative.parts[:1] == ("dist",):
                dist_size += size
                if len(child_relative.parts) >= 3:
                    release = child_relative.parts[1]
                    release_sizes[release] = release_sizes.get(release, 0) + size

    walk(repo_root, Path())
    for release, size in sorted(release_sizes.items()):
        if size > policy["limits"]["max_release_directory_bytes"]:
            report.error(
                "hygiene-release-size",
                f"dist/{release} exceeds limits.max_release_directory_bytes ({size} bytes)",
            )
    if dist_size > policy["limits"]["max_dist_bytes"]:
        report.error(
            "hygiene-dist-size",
            f"dist exceeds limits.max_dist_bytes ({dist_size} bytes)",
        )
    report.mark("repository_hygiene", before)
    return len(report.errors) == before


def expected_ids() -> set[str]:
    return {
        f"{family}{number:02d}"
        for family, count in EXPECTED_COUNTS.items()
        for number in range(1, count + 1)
    }


def normalize_case_id(raw: Any) -> str | None:
    if not isinstance(raw, str):
        return None
    match = CASE_ID_RE.fullmatch(raw.strip().upper())
    if not match:
        return None
    family, number = match.groups()
    return f"{family}{int(number):02d}"


def load_cases(path: Path, report: TestReport) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error("missing-catalog", f"Test catalog does not exist: {path}")
        return []
    except (OSError, UnicodeError) as exc:
        report.error("catalog-read", f"Cannot read test catalog: {exc}")
        return []
    except json.JSONDecodeError as exc:
        report.error(
            "catalog-syntax",
            "tests/cases.yaml must be JSON-compatible YAML: " + str(exc),
        )
        return []

    if isinstance(data, dict):
        cases = data.get("cases")
    else:
        cases = data
    if not isinstance(cases, list):
        report.error("catalog-shape", "Catalog root must be a list or an object with a 'cases' list.")
        return []
    if not all(isinstance(case, dict) for case in cases):
        report.error("case-shape", "Every catalog entry must be an object.")
        return [case for case in cases if isinstance(case, dict)]
    return cases


def has_meaningful_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def validate_catalog(cases: list[dict[str, Any]], report: TestReport) -> list[tuple[str, dict[str, Any]]]:
    normalized: list[tuple[str, dict[str, Any]]] = []

    before = len(report.errors)
    if len(cases) != 104:
        report.error("case-count", f"Expected exactly 104 cases, found {len(cases)}.")
    report.mark("exact_case_count", before)

    before = len(report.errors)
    seen: set[str] = set()
    for index, case in enumerate(cases, start=1):
        raw_id = case.get("id")
        case_id = normalize_case_id(raw_id)
        label = str(raw_id) if raw_id is not None else f"catalog-index-{index}"
        if case_id is None:
            report.error("case-id", f"Invalid case ID at catalog index {index}: {raw_id!r}", label)
            continue
        if case_id in seen:
            report.error("duplicate-case-id", "Case ID is duplicated.", case_id)
        seen.add(case_id)
        normalized.append((case_id, case))

        missing = sorted(REQUIRED_FIELDS - set(case))
        if missing:
            report.error("missing-fields", "Missing required fields: " + ", ".join(missing), case_id)
            continue
        empty = sorted(field for field in REQUIRED_FIELDS - {"behavioral_selected"} if not has_meaningful_value(case[field]))
        if empty:
            report.error("empty-fields", "Required fields have empty values: " + ", ".join(empty), case_id)

        family = case.get("family")
        if not isinstance(family, str) or family.upper() != case_id[0]:
            report.error("family-mismatch", f"Family must match ID family {case_id[0]!r}.", case_id)
        if case.get("mode") not in ALLOWED_MODES:
            report.error(
                "mode-value",
                "Mode must be one of: " + ", ".join(sorted(ALLOWED_MODES)),
                case_id,
            )
        if case.get("risk_level") not in ALLOWED_RISK_LEVELS:
            report.error(
                "risk-level-value",
                "risk_level must be low, medium, high, or critical.",
                case_id,
            )
        if not isinstance(case.get("behavioral_selected"), bool):
            report.error("behavioral-selection-type", "behavioral_selected must be boolean.", case_id)

    missing_ids = sorted(expected_ids() - seen)
    unexpected_ids = sorted(seen - expected_ids())
    if missing_ids:
        report.error("missing-case-ids", "Missing IDs: " + ", ".join(missing_ids))
    if unexpected_ids:
        report.error("unexpected-case-ids", "Unexpected IDs: " + ", ".join(unexpected_ids))
    report.mark("ids_fields_and_values", before)

    before = len(report.errors)
    counts = Counter(case_id[0] for case_id, _ in normalized)
    if dict(sorted(counts.items())) != EXPECTED_COUNTS:
        report.error(
            "family-counts",
            f"Expected family counts {EXPECTED_COUNTS}; found {dict(sorted(counts.items()))}.",
        )
    report.mark("family_counts", before)

    before = len(report.errors)
    selected = [(case_id, case) for case_id, case in normalized if case.get("behavioral_selected") is True]
    if len(selected) != 28:
        report.error("behavioral-count", f"Expected exactly 28 behavioral selections, found {len(selected)}.")
    selected_families = {case_id[0] for case_id, _ in selected}
    missing_families = sorted(set(EXPECTED_COUNTS) - selected_families)
    if missing_families:
        report.error(
            "behavioral-family-coverage",
            "Behavioral selections must cover every family; missing: " + ", ".join(missing_families),
        )
    if selected and not any(case.get("risk_level") in {"high", "critical"} for _, case in selected):
        report.error("behavioral-risk-coverage", "Behavioral selections must include a high/critical-risk case.")
    report.mark("behavioral_selection", before)

    return normalized


def validate_coverage_matrix(repo_root: Path, normalized: list[tuple[str, dict[str, Any]]], report: TestReport) -> None:
    before = len(report.errors)
    path = (
        repo_root
        / "skills"
        / "thien-skill-risk-control-process"
        / "references"
        / "requirement-coverage-matrix.md"
    )
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        report.error("coverage-read", f"Cannot read requirement coverage matrix: {exc}")
        report.mark("requirement_coverage", before)
        return
    test_section = text[text.find("## Test coverage") :] if "## Test coverage" in text else ""
    covered = set(COVERAGE_ROW_RE.findall(test_section))
    catalog_ids = {case_id for case_id, _ in normalized}
    missing = sorted(catalog_ids - covered)
    extra = sorted(covered - catalog_ids)
    if missing:
        report.error("coverage-missing", "Cases absent from coverage matrix: " + ", ".join(missing))
    if extra:
        report.error("coverage-extra", "Coverage matrix has unknown test IDs: " + ", ".join(extra))
    if "| `IV`" not in text or "| `XLII`" not in text:
        report.error("requirement-range", "Coverage matrix must trace the supplied IV–XLII requirements.")
    report.mark("requirement_coverage", before)


def run_package_validator(repo_root: Path, report: TestReport) -> None:
    before = len(report.errors)
    skill_path = repo_root / "skills" / "thien-skill-risk-control-process"
    validator = skill_path / "scripts" / "validate_package.py"
    command = [
        sys.executable,
        str(validator),
        str(skill_path),
        "--repo-root",
        str(repo_root),
        "--json",
    ]
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        report.error("validator-execution", f"Cannot execute package validator: {exc}")
        report.mark("package_validator", before)
        return
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        report.error(
            "validator-output",
            "Package validator did not emit valid JSON. stderr: " + completed.stderr.strip(),
        )
        report.mark("package_validator", before)
        return
    # Persist logical package identity only; never copy a machine-local path
    # from validator output into release acceptance artifacts.
    payload.pop("skill_path", None)
    report.validator = payload
    if completed.returncode != 0 or payload.get("status") != "pass":
        report.error(
            "package-validation",
            f"Package validator failed with {payload.get('error_count', 'unknown')} error(s).",
        )
    report.mark("package_validator", before)


def result_payload(
    report: TestReport,
    normalized: list[tuple[str, dict[str, Any]]],
) -> dict[str, Any]:
    selected_count = sum(case.get("behavioral_selected") is True for _, case in normalized)
    deterministic_status = "pass" if not report.errors else "fail"
    case_results = []
    for case_id, case in normalized:
        case_results.append(
            {
                "id": case_id,
                "deterministic_status": deterministic_status,
                "behavioral_status": "not_run" if case.get("behavioral_selected") is True else "not_selected",
            }
        )
    report.case_results = case_results
    return {
        "suite": "Thien-Skill-Risk-Control-Process deterministic acceptance",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": deterministic_status,
        "case_count": len(normalized),
        "expected_case_count": 104,
        "family_counts": dict(sorted(Counter(case_id[0] for case_id, _ in normalized).items())),
        "behavioral": {
            "selected": selected_count,
            "executed": 0,
            "status": "not_run",
            "note": "Behavioral selection is defined but this deterministic runner does not execute model tests.",
        },
        "checks": report.checks,
        "error_count": len(report.errors),
        "errors": report.errors,
        "package_validator": report.validator,
        "case_results": case_results,
    }


def render_acceptance_report(payload: dict[str, Any]) -> str:
    status = str(payload["status"]).upper()
    behavioral = payload["behavioral"]
    lines = [
        "# Acceptance report",
        "",
        f"- Deterministic status: `{status}`",
        f"- Deterministic catalog: `{payload['case_count']}` / `{payload['expected_case_count']}` cases",
        f"- Behavioral selection: `{behavioral['selected']}` cases",
        "- Behavioral execution: `NOT RUN` by this deterministic runner",
        "- Package validator: `"
        + str((payload.get("package_validator") or {}).get("status", "not available")).upper()
        + "`",
        "",
        "## Deterministic checks",
        "",
        "| Check | Result |",
        "|---|---|",
    ]
    for check, result in payload["checks"].items():
        lines.append(f"| `{check}` | `{str(result).upper()}` |")
    lines.extend(
        [
            "",
            "## Behavioral status",
            "",
            "The 28 selected cases are a stratified forward-test plan, not evidence that a model run occurred. "
            "Each selected case remains `not_run` in this deterministic result; unselected cases remain "
            "`not_selected`. `forward-test-results.json` separately records 28 execution summaries, but the "
            "raw outputs and required run metadata were not retained, so those summaries are provisional and "
            "are not accepted as verified behavioral passes. A future accepted run must retain model/platform, "
            "date, skill hash, input hash, raw output, reviewer, result rationale, and remediation status.",
            "",
            "## Errors",
            "",
        ]
    )
    if payload["errors"]:
        for item in payload["errors"]:
            case = f" ({item['case_id']})" if "case_id" in item else ""
            lines.append(f"- `{item['code']}`{case}: {item['message']}")
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Acceptance boundary",
            "",
            "A deterministic pass establishes package structure, catalog integrity, traceability, and static "
            "safety checks only. It does not establish operating effectiveness, legal compliance, audit "
            "assurance, or cross-platform behavioral equivalence.",
            "",
        ]
    )
    return "\n".join(lines)


def write_results(repo_root: Path, payload: dict[str, Any]) -> None:
    """Publish both result files atomically per file, rolling back group failure."""
    repo_root = absolute_no_resolve(repo_root)
    tests_dir = repo_root / "tests"
    outputs = {
        tests_dir / "deterministic-results.json": (
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8"),
        tests_dir / "acceptance-report.md": render_acceptance_report(payload).encode("utf-8"),
    }
    atomic_write_many(outputs, repo_root, "result destination")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root (default: parent of scripts/).",
    )
    parser.add_argument(
        "--write-results",
        action="store_true",
        help="Write tests/deterministic-results.json and tests/acceptance-report.md.",
    )
    parser.add_argument("--json", action="store_true", help="Print the complete JSON result.")
    parser.add_argument(
        "--phase3", action="store_true",
        help="Validate retained Phase 3 evidence separately; never execute a model or overwrite historical results.",
    )
    parser.add_argument(
        "--phase3-matrix", default="tests/phase-3/acceptance-matrix.json",
        help="Repository-relative JSON envelope of the approved Phase 1 matrix (requires --phase3).",
    )
    parser.add_argument(
        "--phase3-evidence", default="tests/phase-3/evidence-index.json",
        help="Repository-relative retained evidence index (requires --phase3).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.phase3 and args.write_results:
        parser.error("--phase3 cannot use --write-results: historical acceptance/results must remain unchanged.")
    if not args.phase3 and (
        args.phase3_matrix != "tests/phase-3/acceptance-matrix.json"
        or args.phase3_evidence != "tests/phase-3/evidence-index.json"
    ):
        parser.error("--phase3-matrix and --phase3-evidence require --phase3.")
    repo_root = absolute_no_resolve(args.repo_root)
    report = TestReport()
    hygiene_ok = validate_repository_hygiene(repo_root, report)
    if not hygiene_ok:
        payload = result_payload(report, [])
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        else:
            print("Deterministic acceptance: FAIL")
            print("Cases: 0 / 104 (payload checks blocked by repository hygiene)")
            for item in report.errors:
                print(f"ERROR {item['code']}: {item['message']}")
        return 1
    if (args.phase3
            and args.phase3_matrix == "tests/phase-3/acceptance-matrix.json"
            and (repo_root / "skills/thien-skill-risk-control-process").is_dir()
            and not (repo_root / "skills/thien-skill-risk-process-control").exists()):
        parser.error(
            "Default Phase 3 records belong to the pre-rename 1.1.0 tree. "
            "Use python3 -B scripts/verify_rename.py --historical to validate "
            "that frozen baseline; do not re-label historical runs as 1.1.1 evidence."
        )
    cases = load_cases(repo_root / "tests" / "cases.yaml", report)
    normalized = validate_catalog(cases, report)
    validate_coverage_matrix(repo_root, normalized, report)
    run_package_validator(repo_root, report)
    payload = result_payload(report, normalized)

    if args.phase3:
        # The default branch and its status=pass contract remain unchanged for
        # the builder. Receipt integrity and model acceptance are separate here.
        from phase3_evidence import evaluate_phase3

        evidence = evaluate_phase3(
            repo_root, args.phase3_matrix, args.phase3_evidence,
            legacy_static_registry=payload,
        )
        if args.json:
            print(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True))
        else:
            print(f"Phase 3 evidence integrity: {evidence['integrity_status'].upper()}")
            print(f"Phase 3 acceptance: {evidence['acceptance_status'].upper()}")
            print(f"Legacy static/registry: {payload['status'].upper()}")
            for context in evidence["claims_by_context"]:
                print(f"Context {context['context_id']}: {context['surface']} / {context['verification_mode']}")
                for claim_id, claim in context["claims"].items():
                    if claim["status"] != "not_applicable":
                        print(f"  {claim_id}: {claim['status']}")
            for item in evidence["errors"]:
                print(f"ERROR {item['code']} [{item['where']}]: {item['message']}")
            print("A zero exit code means valid structure, not complete behavioral acceptance.")
        return 0 if not report.errors and evidence["integrity_status"] == "pass" else 1

    if args.write_results:
        try:
            write_results(repo_root, payload)
        except (OSError, ValueError) as exc:
            print(f"ERROR result-write: {exc}", file=sys.stderr)
            return 2

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"Deterministic acceptance: {payload['status'].upper()}")
        print(f"Cases: {payload['case_count']} / 104")
        print(
            f"Behavioral: {payload['behavioral']['selected']} selected; "
            "0 executed; status NOT RUN"
        )
        for check, result in payload["checks"].items():
            print(f"  {str(result).upper():5} {check}")
        for item in payload["errors"]:
            case = f" [{item['case_id']}]" if "case_id" in item else ""
            print(f"ERROR {item['code']}{case}: {item['message']}")
    return 0 if not report.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
