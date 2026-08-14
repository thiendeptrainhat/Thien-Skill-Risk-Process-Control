#!/usr/bin/env python3
"""Run the deterministic acceptance checks for the 104-case test catalog.

`tests/cases.yaml` is deliberately JSON-compatible YAML so it can be validated
without third-party dependencies.  This runner never executes behavioral model
tests.  Selected behavioral cases remain explicitly `not_run` until a separate
forward-testing activity records real observations.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
        / "thien-skill-risk-process-control"
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
    skill_path = repo_root / "skills" / "thien-skill-risk-process-control"
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
        "suite": "Thien-Skill-Risk-Process-Control deterministic acceptance",
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
    tests_dir = repo_root / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / "deterministic-results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (tests_dir / "acceptance-report.md").write_text(
        render_acceptance_report(payload),
        encoding="utf-8",
    )


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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    report = TestReport()
    cases = load_cases(repo_root / "tests" / "cases.yaml", report)
    normalized = validate_catalog(cases, report)
    validate_coverage_matrix(repo_root, normalized, report)
    run_package_validator(repo_root, report)
    payload = result_payload(report, normalized)

    if args.write_results:
        try:
            write_results(repo_root, payload)
        except OSError as exc:
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
