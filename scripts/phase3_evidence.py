#!/usr/bin/env python3
"""Read-only Phase 3 receipt validator; this module never runs a model.

Hashes bind retained artifacts and reviews to the approved matrix and a frozen
skill snapshot. They do not authenticate the claimed executor or establish the
semantic truth of a review. A complete receipt is deliberately distinct from a
successful model run, a current-release claim, and a platform-wide assertion.

Only the standard library is imported. The approved YAML is parsed with Ruby's
safe YAML loader when it is not JSON-compatible; no dependency is installed.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


MATRIX_SOURCE = "docs/phase-1/ACCEPTANCE-MATRIX.yaml"
DEFAULT_MATRIX = "tests/phase-3/acceptance-matrix.json"
DEFAULT_EVIDENCE = "tests/phase-3/evidence-index.json"
SNAPSHOT_PREFIX = "tests/phase-3/snapshots/"
EXCLUDED_NAMES = {".DS_Store", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
LINE_RE = re.compile(r"^L([1-9][0-9]*)(?:-L([1-9][0-9]*))?$")
REVIEW_RESULTS = {"pass", "fail", "inconclusive"}
ACTUAL_ARTIFACTS = {"raw_output", "tool_trace", "execution_record"}
RUN_ARTIFACT_FIELDS = ("raw_prompt", "raw_output", "tool_trace", "execution_record")
STATIC_KINDS = {"packaging", "release_evidence"}
CAPABILITY_CLAIMS = {
    "live_external_lookup", "file_input_parity", "live_document_evidence_handoff",
}
REQUIRED_RELEASE_CLAIMS = (
    "core_business_logic", "backward_compatibility", "distribution_integrity",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json(data: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def invalid(value: str) -> None:
        raise ValueError(f"Non-finite JSON value: {value}")

    return json.loads(data, object_pairs_hook=pairs, parse_constant=invalid)


def safe_yaml(text: str) -> Any:
    """Do not silently substitute a lossy ad-hoc parser for approved YAML."""
    try:
        return strict_json(text)
    except (ValueError, json.JSONDecodeError):
        pass
    ruby = """
require 'yaml'
require 'json'
text = STDIN.read
def unique_keys(node)
  return unless node.respond_to?(:children) && node.children
  if node.is_a?(Psych::Nodes::Mapping)
    keys = node.children.each_slice(2).map do |key, _|
      raise 'Non-scalar YAML key' unless key.is_a?(Psych::Nodes::Scalar)
      key.value
    end
    raise 'Duplicate YAML key' unless keys.uniq.length == keys.length
  end
  node.children.each { |child| unique_keys(child) }
end
unique_keys(YAML.parse(text))
STDOUT.write(JSON.generate(YAML.safe_load(text, aliases: false)))
"""
    completed = subprocess.run(
        ["ruby", "-e", ruby], input=text, text=True, capture_output=True,
        check=False, timeout=30,
    )
    if completed.returncode:
        raise ValueError("Safe YAML parser failed: " + completed.stderr.strip())
    return strict_json(completed.stdout)


def meaningful(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: Any, *, nonempty: bool = False) -> bool:
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(meaningful(item) for item in value))


def expected_checks(case: dict[str, Any], variant: dict[str, Any],
                    *, group: bool = False) -> dict[str, str]:
    result: dict[str, str] = {}
    scopes = [("case", case)] if group else [("case", case), ("variant", variant)]
    fields = ("group_must_observe", "group_must_not_observe") if group else (
        "must_observe", "must_not_observe",
    )
    for scope, source in scopes:
        for field in fields:
            for number, text in enumerate(source.get(field, []), 1):
                result[f"{scope}.{field}.{number}"] = text
    return result


def combined_status(states: list[str], *, claim: bool = False) -> str:
    if not states or all(state == "not_run" for state in states):
        return "not_run"
    if "fail" in states:
        return "fail"
    if "inconclusive" in states:
        return "inconclusive"
    if all(state == "pass" for state in states):
        return "verified" if claim else "pass"
    if "executed_unreviewed" in states:
        return "executed_unreviewed"
    if "pass" in states:
        return "partial"
    return "blocked" if "blocked" in states else "not_run"


class EvidenceValidator:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root.resolve()
        self.errors: list[dict[str, str]] = []
        self.warnings: list[dict[str, str]] = []
        self.matrix: dict[str, Any] = {}
        self.matrix_sha: str | None = None
        self.cases: dict[str, dict[str, Any]] = {}
        self.variants: dict[str, dict[str, dict[str, Any]]] = {}
        self.snapshots: dict[tuple[str, str], dict[str, Any]] = {}
        self.runs: dict[str, dict[str, Any]] = {}
        self.groups: list[dict[str, Any]] = []

    def error(self, code: str, message: str, where: str) -> None:
        self.errors.append({"code": code, "message": message, "where": where})

    def warning(self, code: str, message: str, where: str) -> None:
        self.warnings.append({"code": code, "message": message, "where": where})

    def path(self, raw: Any, where: str, *, directory: bool = False) -> Path | None:
        if not meaningful(raw) or "\\" in raw or "\x00" in raw:
            self.error("artifact-path", "Use a nonempty repository-relative POSIX path.", where)
            return None
        logical = PurePosixPath(raw)
        if logical.is_absolute() or ".." in logical.parts or str(logical) != raw or raw == ".":
            self.error("artifact-path", "Absolute, non-normalized or escaping paths are not allowed.", where)
            return None
        candidate = self.root.joinpath(*logical.parts)
        cursor = self.root
        for part in logical.parts:
            cursor /= part
            if cursor.is_symlink():
                self.error("artifact-symlink", "Evidence must not traverse a symlink.", where)
                return None
        if not candidate.resolve().is_relative_to(self.root):
            self.error("artifact-escape", "Evidence resolved outside the repository.", where)
            return None
        exists = candidate.is_dir() if directory else candidate.is_file()
        if not exists:
            self.error("artifact-missing", f"Retained {'directory' if directory else 'file'} is missing: {raw}", where)
            return None
        return candidate

    def json_file(self, raw: Any, where: str) -> dict[str, Any] | None:
        path = self.path(raw, where)
        if path is None:
            return None
        try:
            value = strict_json(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            self.error("json-read", str(exc), where)
            return None
        if not isinstance(value, dict):
            self.error("json-shape", "Expected a JSON object.", where)
            return None
        return value

    def artifact(self, pointer: Any, where: str, *, text: bool = False) -> bytes | None:
        if not isinstance(pointer, dict):
            self.error("artifact-pointer", "Expected an artifact object with path and sha256.", where)
            return None
        claimed_sha = pointer.get("sha256")
        if not isinstance(claimed_sha, str) or not SHA_RE.fullmatch(claimed_sha):
            self.error("artifact-hash", "sha256 must be 64 lowercase hexadecimal characters.", where)
            return None
        path = self.path(pointer.get("path"), where)
        if path is None:
            return None
        try:
            data = path.read_bytes()
        except OSError as exc:
            self.error("artifact-read", str(exc), where)
            return None
        if digest(data) != claimed_sha:
            self.error("artifact-hash-mismatch", "Retained bytes do not match the recorded SHA-256.", where)
            return None
        if text:
            try:
                if not data.decode("utf-8").strip():
                    raise ValueError("Text evidence is empty.")
            except (UnicodeError, ValueError) as exc:
                self.error("artifact-text", str(exc), where)
                return None
        return data

    def json_artifact(self, pointer: Any, where: str) -> dict[str, Any] | None:
        data = self.artifact(pointer, where, text=True)
        if data is None:
            return None
        try:
            value = strict_json(data.decode("utf-8"))
        except ValueError as exc:
            self.error("json-artifact", str(exc), where)
            return None
        if not isinstance(value, dict) or not value:
            self.error("json-artifact", "Expected a nonempty JSON object.", where)
            return None
        return value

    def timestamp(self, raw: Any, where: str) -> datetime | None:
        try:
            if not meaningful(raw) or "T" not in raw:
                raise ValueError("Expected an ISO-8601 timestamp with timezone.")
            value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError("Timestamp must include a timezone.")
            return value
        except (TypeError, ValueError) as exc:
            self.error("timestamp", str(exc), where)
            return None

    def read_matrix(self, matrix_path: str) -> None:
        where = "matrix"
        envelope = self.json_file(matrix_path, where)
        if envelope is None:
            return
        source = envelope.get("source")
        if not isinstance(source, dict) or source.get("path") != MATRIX_SOURCE:
            self.error("matrix-source", f"The matrix must be bound to {MATRIX_SOURCE}.", where)
            return
        raw = self.artifact(source, where + ".source", text=True)
        if raw is None:
            return
        try:
            approved = safe_yaml(raw.decode("utf-8"))
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            self.error("matrix-parse", str(exc), where)
            return
        matrix = envelope.get("matrix")
        if not isinstance(matrix, dict) or matrix != approved:
            self.error("matrix-content", "JSON matrix is not exactly the parsed approved YAML; do not weaken its rubric.", where)
            return
        self.matrix, self.matrix_sha = matrix, source["sha256"]
        baseline = matrix.get("baseline")
        if not isinstance(baseline, dict) or not meaningful(baseline.get("skill_id")):
            self.error("matrix-baseline", "baseline must identify the canonical skill.", where)
        requirements = matrix.get("requirements")
        cases = matrix.get("cases")
        claims = matrix.get("acceptance_claims")
        if not isinstance(requirements, dict) or not requirements:
            self.error("matrix-requirements", "requirements must be a nonempty mapping.", where)
            requirements = {}
        if not isinstance(cases, list) or not cases or not isinstance(claims, dict) or not claims:
            self.error("matrix-shape", "cases and acceptance_claims must be nonempty.", where)
            return
        coverage: set[str] = set()
        all_variant_ids: set[str] = set()
        for case in cases:
            if not isinstance(case, dict) or not meaningful(case.get("id")):
                self.error("matrix-case", "Each case needs an ID.", where)
                continue
            case_id = case["id"]
            if case_id in self.cases:
                self.error("matrix-case-duplicate", "Duplicate case ID.", case_id)
                continue
            self.cases[case_id] = case
            req = case.get("requirements")
            if not string_list(req, nonempty=True) or len(set(req)) != len(req) or set(req) - requirements.keys():
                self.error("matrix-case-requirements", "Case requirements must be unique known IDs.", case_id)
            else:
                coverage.update(req)
            kind = case.get("kind")
            if not meaningful(kind) or not (kind.startswith("behavioral") or kind in STATIC_KINDS or kind == "compatibility_fixture_and_static"):
                self.error("matrix-case-kind", "Unknown case verification kind.", case_id)
            for field in ("must_observe", "must_not_observe", "group_must_observe", "group_must_not_observe"):
                if field in case and not string_list(case[field], nonempty=True):
                    self.error("matrix-invariants", f"{field} must contain nonempty invariant strings.", case_id)
            if not case.get("must_observe"):
                self.error("matrix-invariants", "A case must have mandatory observable invariants.", case_id)
            variants = case.get("variants", [{"variant_id": case_id + "-V01"}])
            self.variants[case_id] = {}
            if not isinstance(variants, list) or not variants:
                self.error("matrix-variants", "variants must be a nonempty list.", case_id)
                continue
            for variant in variants:
                variant_id = variant.get("variant_id") if isinstance(variant, dict) else None
                if not meaningful(variant_id) or not variant_id.startswith(case_id + "-V") or variant_id in all_variant_ids:
                    self.error("matrix-variant-id", "Variants need unique IDs within their case namespace.", case_id)
                    continue
                all_variant_ids.add(variant_id)
                self.variants[case_id][variant_id] = variant
                for field in ("must_observe", "must_not_observe"):
                    if field in variant and not string_list(variant[field], nonempty=True):
                        self.error("matrix-invariants", f"{field} must contain nonempty invariant strings.", variant_id)
        if set(requirements) - coverage:
            self.error("matrix-coverage", "Requirements without cases: " + ", ".join(sorted(set(requirements) - coverage)), where)
        valid_claims: dict[str, dict[str, Any]] = {}
        for claim_id, claim in claims.items():
            required = claim.get("required_cases") if isinstance(claim, dict) else None
            if not string_list(required, nonempty=True) or len(set(required)) != len(required) or set(required) - self.cases.keys():
                self.error("matrix-claim", "Claims need unique, known required cases.", str(claim_id))
                continue
            selection = claim.get("variant_selection", {})
            if not isinstance(selection, dict) or set(selection) - set(required):
                self.error("matrix-claim-selection", "Variant selection must refer to required cases.", str(claim_id))
                continue
            for case_id, chosen in selection.items():
                if not string_list(chosen, nonempty=True) or len(set(chosen)) != len(chosen) or set(chosen) - self.variants[case_id].keys():
                    self.error("matrix-claim-selection", "Selected variants must be unique known IDs.", str(claim_id))
            if all(string_list(chosen, nonempty=True) for chosen in selection.values()):
                valid_claims[claim_id] = claim
        for case_id, variants in self.variants.items():
            for variant_id, variant in variants.items():
                declared = variant.get("required_for_claim")
                if declared is None:
                    continue
                actual = {claim_id for claim_id, claim in valid_claims.items()
                          if case_id in claim.get("required_cases", [])
                          and variant_id in claim.get("variant_selection", {}).get(case_id, variants)}
                if not string_list(declared) or set(declared) != actual:
                    self.error("matrix-variant-claims", "required_for_claim disagrees with acceptance_claims.", variant_id)

    def tree_hashes(self, root: Path, where: str) -> dict[str, str]:
        files: dict[str, str] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            if any(part in EXCLUDED_NAMES for part in relative.parts) or path.suffix in EXCLUDED_SUFFIXES:
                continue
            if path.is_symlink():
                self.error("snapshot-symlink", "Snapshots/canonical source must not contain symlinks.", where)
            elif path.is_file():
                try:
                    files[relative.as_posix()] = digest(path.read_bytes())
                except OSError as exc:
                    self.error("snapshot-read", str(exc), where)
        return files

    def snapshot(self, pointer: Any, where: str) -> dict[str, Any] | None:
        key = (pointer.get("path"), pointer.get("sha256")) if isinstance(pointer, dict) else None
        if key is not None and all(isinstance(part, str) for part in key) and key in self.snapshots:
            return self.snapshots[key]
        before = len(self.errors)
        manifest = self.json_artifact(pointer, where)
        if manifest is None:
            return None
        skill_id = self.matrix.get("baseline", {}).get("skill_id")
        expected_canonical = f"skills/{skill_id}"
        if manifest.get("skill_id") != skill_id or not meaningful(manifest.get("skill_version")):
            self.error("snapshot-identity", "Snapshot must name the approved skill and its tested version.", where)
        if manifest.get("canonical_source") != expected_canonical:
            self.error("snapshot-canonical", "canonical_source must name this skill's canonical source.", where)
        raw_root = manifest.get("source_root")
        if not meaningful(raw_root) or not raw_root.startswith(SNAPSHOT_PREFIX):
            self.error("snapshot-root", "Use a frozen round under tests/phase-3/snapshots/, not the mutable canonical directory.", where)
            return None
        root = self.path(raw_root, where + ".source_root", directory=True)
        if root is None:
            return None
        actual = self.tree_hashes(root, where)
        declared: dict[str, str] = {}
        pointers = manifest.get("files")
        if not isinstance(pointers, list) or not pointers:
            self.error("snapshot-files", "Snapshot must inventory every retained source file.", where)
            pointers = []
        for file_pointer in pointers:
            data = self.artifact(file_pointer, where + ".files")
            if data is None:
                continue
            raw_path = file_pointer["path"]
            if not raw_path.startswith(raw_root + "/"):
                self.error("snapshot-file-scope", "Inventory item is outside source_root.", where)
                continue
            relative = raw_path[len(raw_root) + 1:]
            if relative in declared:
                self.error("snapshot-file-duplicate", "Snapshot inventory repeats a file.", where)
            declared[relative] = file_pointer["sha256"]
        if declared != actual:
            self.error("snapshot-completeness", "Inventory and frozen source tree must have exactly the same files and hashes.", where)
        try:
            skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
            parts = skill_text.split("---", 2)
            frontmatter = safe_yaml(parts[1]) if skill_text.startswith("---\n") and len(parts) == 3 else None
            registry = safe_yaml((root / "integration/master-orchestrator-registry-entry.yaml").read_text(encoding="utf-8"))
            if not isinstance(frontmatter, dict) or frontmatter.get("name") != skill_id:
                self.error("snapshot-skill-name", "Frozen SKILL.md name does not match the manifest.", where)
            if not isinstance(registry, dict) or str(registry.get("version")) != manifest.get("skill_version"):
                self.error("snapshot-version", "Frozen integration registry version does not match the manifest.", where)
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            self.error("snapshot-metadata", str(exc), where)
        canonical = self.path(expected_canonical, where + ".canonical_source", directory=True)
        current = self.tree_hashes(canonical, where + ".canonical_source") if canonical else {}
        matches_current = bool(actual) and actual == current
        if not matches_current:
            self.warning("snapshot-not-current", "Historical snapshot is not identical to current canonical content; its runs cannot verify the current release.", where)
        result = {
            "manifest_path": pointer["path"], "manifest_sha256": pointer["sha256"],
            "skill_id": skill_id, "skill_version": manifest.get("skill_version"),
            "source_root": raw_root, "canonical_source": expected_canonical,
            "file_count": len(actual), "valid": len(self.errors) == before,
            "content_sha256": digest(json.dumps(actual, sort_keys=True, separators=(",", ":")).encode()),
            "matches_current_canonical": matches_current,
            "canonical_differences": sorted(name for name in set(actual) | set(current) if actual.get(name) != current.get(name)),
        }
        if key is not None:
            self.snapshots[key] = result
        return result

    def check_runtime(self, raw: Any, mode: str, limitations: Any, where: str) -> dict[str, Any]:
        runtime = raw if isinstance(raw, dict) else {}
        for key in ("platform", "surface", "runtime"):
            if not meaningful(runtime.get(key)):
                self.error("runtime-metadata", f"runtime.{key} must identify the actual execution context.", where)
        if not isinstance(runtime.get("capabilities"), dict) or not runtime["capabilities"]:
            self.error("runtime-capabilities", "Record actual capability/tool/permission availability, including explicit unavailability.", where)
        if not isinstance(runtime.get("capability_simulation"), bool):
            self.error("runtime-simulation", "capability_simulation must be an explicit boolean.", where)
        status = runtime.get("model_identifier_status")
        if mode == "static":
            if status != "not_applicable" or runtime.get("model") is not None:
                self.error("runtime-model", "Static receipts must use model=null and model_identifier_status=not_applicable.", where)
        else:
            if status == "provided":
                if not meaningful(runtime.get("model")):
                    self.error("runtime-model", "A host-provided model identifier is required when status=provided.", where)
            elif isinstance(status, str) and status in {"not_available", "not_provided"}:
                if runtime.get("model") is not None or not string_list(limitations, nonempty=True):
                    self.error("runtime-model", "Unknown model identifier must stay null with an explicit limitation.", where)
            else:
                self.error("runtime-model", "Record provided/not_available/not_provided, never invent an exact model.", where)
            if runtime.get("fresh_context") is not True:
                self.error("runtime-context", "Behavioral cases/variants require a recorded fresh context.", where)
        return runtime

    def review(self, value: dict[str, Any], expected: dict[str, str], where: str,
               evidence: dict[str, dict[str, bytes]], *, run_id: str | None = None,
               not_before: datetime | None = None) -> dict[str, Any]:
        before = len(self.errors)
        if run_id is not None and value.get("run_id") != run_id:
            self.error("review-run", "Review is for a different run.", where)
        reviewer = value.get("reviewer")
        if (not isinstance(reviewer, dict)
                or not all(meaningful(reviewer.get(key)) for key in ("name", "role", "relationship"))
                or reviewer["relationship"] not in {"independent", "self_check"}):
            self.error("reviewer", "Attribute the review to a named reviewer/role and independent or self_check relationship.", where)
        stamp = self.timestamp(value.get("timestamp"), where)
        if stamp is not None and not_before is not None and stamp < not_before:
            self.error("review-time", "Review predates the execution it reviews.", where)
        if value.get("rubric_source_sha256") != self.matrix_sha:
            self.error("review-rubric", "Review must use the exact approved rubric source hash.", where)
        if not string_list(value.get("limitations")):
            self.error("review-limitations", "limitations must be a list of nonempty strings (possibly empty).", where)
        checks = value.get("checks")
        if not isinstance(checks, dict):
            self.error("review-checks", "Review requires per-invariant checks.", where)
            checks = {}
        if set(checks) != set(expected):
            missing, extra = sorted(set(expected) - set(checks)), sorted(set(checks) - set(expected))
            self.error("review-coverage", f"Invariant IDs must match exactly; missing={missing}, extra={extra}.", where)
        states: list[str] = []
        referenced_outputs: set[str] = set()
        for check_id, check in checks.items():
            check_where = where + "." + str(check_id)
            if (not isinstance(check, dict) or not isinstance(check.get("result"), str)
                    or check["result"] not in REVIEW_RESULTS or not meaningful(check.get("rationale"))):
                self.error("review-check", "Each invariant needs pass/fail/inconclusive and a specific rationale.", check_where)
                continue
            states.append(check["result"])
            refs = check.get("evidence_refs")
            if not isinstance(refs, list) or not refs:
                self.error("review-evidence", "Every judgment needs retained actual-evidence locators.", check_where)
                continue
            for reference in refs:
                reference_run = reference.get("run_id", run_id) if isinstance(reference, dict) else None
                artifact_name = reference.get("artifact") if isinstance(reference, dict) else None
                if (not isinstance(reference_run, str) or reference_run not in evidence
                        or not isinstance(artifact_name, str) or artifact_name not in ACTUAL_ARTIFACTS):
                    self.error("review-evidence", "References must identify actual raw_output/tool_trace/execution_record for a reviewed run.", check_where)
                    continue
                raw = evidence[reference_run].get(artifact_name)
                if raw is None:
                    self.error("review-evidence", "Referenced evidence was not retained with a valid hash.", check_where)
                    continue
                locator = reference.get("locator")
                if locator != "entire_artifact":
                    match = LINE_RE.fullmatch(locator) if isinstance(locator, str) else None
                    if not match:
                        self.error("review-locator", "Use L<number>, L<start>-L<end>, or entire_artifact.", check_where)
                        continue
                    start, end = int(match[1]), int(match[2] or match[1])
                    if start > end or end > len(raw.decode("utf-8").splitlines()):
                        self.error("review-locator", "Line locator is outside the retained evidence.", check_where)
                        continue
                if artifact_name == "raw_output":
                    referenced_outputs.add(reference_run)
        aggregate = "fail" if "fail" in states else "inconclusive" if "inconclusive" in states or not states else "pass"
        if not isinstance(value.get("result"), str) or value["result"] not in REVIEW_RESULTS or value["result"] != aggregate:
            self.error("review-result", "Review result must agree with every mandatory invariant; no partial-pass arithmetic.", where)
        return {
            "status": aggregate if len(self.errors) == before else "inconclusive",
            "valid": len(self.errors) == before, "timestamp": stamp,
            "reviewer": reviewer, "mandatory_checks": len(expected),
            "reviewed_checks": len(checks), "referenced_outputs": referenced_outputs,
        }

    def read_run(self, raw: Any, number: int) -> None:
        where = f"runs[{number}]"
        if not isinstance(raw, dict) or not meaningful(raw.get("run_id")):
            self.error("run-shape", "Each run needs a unique run_id.", where)
            return
        run_id = raw["run_id"]
        where = "run:" + run_id
        if run_id in self.runs:
            self.error("run-duplicate", "Duplicate run_id.", where)
            return
        before = len(self.errors)
        case_id, variant_id = raw.get("case_id"), raw.get("variant_id")
        if not isinstance(case_id, str) or case_id not in self.cases or not isinstance(variant_id, str) or variant_id not in self.variants.get(case_id, {}):
            self.error("run-case-variant", "Run must use an approved case and variant.", where)
            return
        case, variant = self.cases[case_id], self.variants[case_id][variant_id]
        requirements = raw.get("requirement_ids")
        if not string_list(requirements, nonempty=True) or len(set(requirements)) != len(requirements) or set(requirements) != set(case["requirements"]):
            self.error("run-requirements", "requirement_ids must exactly match this case's coverage.", where)
        execution = raw.get("execution_status")
        if not isinstance(execution, str) or execution not in {"executed", "not_run", "blocked"}:
            self.error("run-execution-status", "Use executed/not_run/blocked; review result is a separate field.", where)
            execution = "invalid"
        limitations = raw.get("limitations")
        if not string_list(limitations, nonempty=execution == "blocked"):
            self.error("run-limitations", "Record limitations as a list; blocked records require a reason.", where)
        retest = raw.get("retest_of", [])
        if not string_list(retest) or len(set(retest)) != len(retest):
            self.error("run-retest", "retest_of must be a list of unique run IDs.", where)
            retest = []
        stamp = self.timestamp(raw.get("timestamp"), where) if execution == "executed" or "timestamp" in raw else None
        record: dict[str, Any] = {
            "raw": raw, "run_id": run_id, "case_id": case_id, "variant_id": variant_id,
            "execution_status": execution, "timestamp": stamp, "retest_of": retest,
            "status": execution if execution in {"not_run", "blocked"} else "inconclusive",
            "valid": False, "artifacts": {}, "snapshot": None, "context_id": None,
            "review": None, "runtime": raw.get("runtime", {}),
            "verification_mode": raw.get("verification_mode"),
        }
        self.runs[run_id] = record
        if execution != "executed":
            if raw.get("review") is not None:
                self.error("unexecuted-review", "An unexecuted record cannot carry an acceptance review.", where)
            record["valid"] = len(self.errors) == before
            return
        mode = raw.get("verification_mode")
        expected_mode = "static" if case["kind"] in STATIC_KINDS else "model"
        if mode != expected_mode:
            self.error("run-verification-mode", f"This case requires {expected_mode} evidence; static checks are not model execution.", where)
        runtime = self.check_runtime(raw.get("runtime"), mode, limitations, where)
        record["runtime"] = runtime
        if not meaningful(raw.get("authorized_source_scope")):
            self.error("run-source-scope", "Describe which synthetic or user-authorized sources were allowed for this run.", where)
        inputs = raw.get("inputs")
        if not isinstance(inputs, list) or not inputs:
            self.error("run-inputs", "Retain actual input artifacts with fixture IDs, versions and hashes.", where)
            inputs = []
        input_keys: set[tuple[str, str, str]] = set()
        for number, item in enumerate(inputs):
            if not isinstance(item, dict) or not meaningful(item.get("fixture_id")) or not meaningful(item.get("version")):
                self.error("run-input", "Each input requires fixture_id, version and artifact.", where)
                continue
            data = self.artifact(item.get("artifact"), where + f".inputs[{number}]")
            if data is not None:
                key = (item["fixture_id"], item["version"], item["artifact"]["path"])
                if key in input_keys:
                    self.error("run-input-duplicate", "Input artifact is duplicated.", where)
                input_keys.add(key)
        snapshot = self.snapshot(raw.get("skill_snapshot"), where + ".skill_snapshot")
        record["snapshot"] = snapshot
        artifact_paths: dict[str, str] = {}
        artifact_hashes: dict[str, str] = {}
        for field in RUN_ARTIFACT_FIELDS:
            data = self.artifact(raw.get(field), where + "." + field, text=True)
            if data is not None:
                record["artifacts"][field] = data
                pointer = raw[field]
                resolved = self.root.joinpath(*PurePosixPath(pointer["path"]).parts).resolve()
                artifact_paths[field] = resolved.relative_to(self.root).as_posix()
                artifact_hashes[field] = digest(data)
        for aliases, code, basis in (
            (artifact_paths, "run-artifact-path-alias", "resolved repository-relative path"),
            (artifact_hashes, "run-artifact-content-alias", "SHA-256 content hash"),
        ):
            grouped: dict[str, list[str]] = {}
            for field, identity in aliases.items():
                grouped.setdefault(identity, []).append(field)
            for identity, fields in grouped.items():
                if len(fields) > 1:
                    self.error(
                        code,
                        f"Execution artifacts must be pairwise distinct by {basis}; "
                        f"{', '.join(fields)} alias {identity}.",
                        where,
                    )
        # Structured data, extraction packets and supporting images are retained
        # evidence too. Their hashes must not silently escape validation merely
        # because review locators refer to the accompanying narrative/trace.
        supplemental = raw.get("additional_artifacts", [])
        if not isinstance(supplemental, list):
            self.error("run-additional-artifacts", "additional_artifacts must be a list of retained artifact pointers.", where)
            supplemental = []
        supplemental_paths: set[str] = set()
        for number, pointer in enumerate(supplemental):
            data = self.artifact(pointer, where + f".additional_artifacts[{number}]")
            if data is not None:
                path = pointer["path"]
                if path in supplemental_paths:
                    self.error("run-additional-duplicate", "Supplementary artifact is listed more than once.", where)
                supplemental_paths.add(path)
        if "execution_record" in record["artifacts"]:
            try:
                receipt = strict_json(record["artifacts"]["execution_record"].decode("utf-8"))
                if not isinstance(receipt, dict) or not receipt:
                    raise ValueError("Execution record must be a nonempty JSON object with retained execution metadata.")
                if "run_id" in receipt and receipt["run_id"] != run_id:
                    raise ValueError("Execution record belongs to a different run.")
            except ValueError as exc:
                self.error("run-execution-record", str(exc), where)
        if snapshot:
            context = {
                "verification_mode": mode,
                **{key: runtime.get(key) for key in ("platform", "surface", "runtime", "model", "model_identifier_status")},
                "snapshot_manifest_sha256": snapshot["manifest_sha256"],
            }
            record["context"] = context
            record["context_id"] = digest(json.dumps(context, sort_keys=True).encode())[:16]
        if raw.get("review") is None:
            record["status"] = "executed_unreviewed"
        else:
            review_json = self.json_artifact(raw["review"], where + ".review")
            if review_json is not None:
                reviewed = self.review(review_json, expected_checks(case, variant), where + ".review",
                                       {run_id: record["artifacts"]}, run_id=run_id, not_before=stamp)
                record["review"] = reviewed
                record["status"] = reviewed["status"]
                if run_id not in reviewed["referenced_outputs"]:
                    self.error("review-output-coverage", "A run review must cite its retained raw output, not just execution metadata.", where)
        record["valid"] = len(self.errors) == before and snapshot is not None and snapshot["valid"]
        if not record["valid"]:
            record["status"] = "inconclusive"

    def check_retests(self) -> None:
        structurally_valid: list[tuple[dict[str, Any], dict[str, Any], str]] = []

        def reject(run: dict[str, Any], code: str, message: str) -> None:
            self.error(code, message, "run:" + run["run_id"])
            run["valid"], run["status"] = False, "inconclusive"

        for run in self.runs.values():
            for prior_id in run["retest_of"]:
                prior = self.runs.get(prior_id)
                if prior is None:
                    reject(run, "run-retest-link", "Retest refers to a run_id that is not retained in this evidence index.")
                    continue
                if prior_id == run["run_id"]:
                    reject(run, "run-retest-self", "A run cannot be a retest of itself.")
                    continue
                if (prior["case_id"], prior["variant_id"]) != (run["case_id"], run["variant_id"]):
                    reject(run, "run-retest-scope", "Retest and prior run must use the same approved case and variant.")
                    continue
                if run["execution_status"] != "executed" or prior["execution_status"] != "executed":
                    reject(run, "run-retest-execution", "Retest and prior run must both have execution_status=executed.")
                    continue
                if run["timestamp"] is None or prior["timestamp"] is None:
                    reject(run, "run-retest-timestamp", "Retest and prior executed run must both have valid timestamps.")
                    continue
                if run["timestamp"] <= prior["timestamp"]:
                    reject(run, "run-retest-order", "Retest timestamp must be later than its prior executed run.")
                    continue
                structurally_valid.append((run, prior, prior_id))

        # A prior record can become invalid while validating its own retest link,
        # regardless of index order. Propagate that invalidity through the acyclic
        # (strictly time-ordered) retest graph instead of trusting list position.
        reported: set[tuple[str, str]] = set()
        changed = True
        while changed:
            changed = False
            for run, prior, prior_id in structurally_valid:
                link = (run["run_id"], prior_id)
                if not prior["valid"] and link not in reported:
                    was_valid = run["valid"]
                    reject(run, "run-retest-prior-invalid",
                           "Retest cannot rely on a prior record that failed evidence validation.")
                    reported.add(link)
                    changed = changed or was_valid

    def read_group(self, pointer: Any, number: int) -> None:
        where = f"group_reviews[{number}]"
        before = len(self.errors)
        value = self.json_artifact(pointer, where)
        if value is None:
            return
        group_id, case_id = value.get("group_review_id"), value.get("case_id")
        if not meaningful(group_id) or any(group["group_review_id"] == group_id for group in self.groups):
            self.error("group-id", "A group review needs a unique group_review_id.", where)
            return
        if not isinstance(case_id, str) or case_id not in self.cases:
            self.error("group-case", "Unknown group-review case.", where)
            return
        expected = expected_checks(self.cases[case_id], {}, group=True)
        if not expected:
            self.error("group-invariants", "Case has no group-level invariants to review.", where)
            return
        run_ids = value.get("run_ids")
        if not string_list(run_ids, nonempty=True) or len(set(run_ids)) != len(run_ids) or set(run_ids) - self.runs.keys():
            self.error("group-runs", "Group reviews need unique retained run IDs.", where)
            return
        runs = [self.runs[run_id] for run_id in run_ids]
        contexts = {run["context_id"] for run in runs}
        if (any(run["case_id"] != case_id for run in runs) or len(contexts) != 1 or None in contexts
                or len({run["variant_id"] for run in runs}) != len(runs)
                or {run["variant_id"] for run in runs} != set(self.variants[case_id])):
            self.error("group-scope", "Group must compare every case variant once, in one runtime/model/snapshot context.", where)
        times = [run["timestamp"] for run in runs if run["timestamp"] is not None]
        reviewed = self.review(value, expected, where, {run["run_id"]: run["artifacts"] for run in runs},
                               not_before=max(times) if times else None)
        if reviewed["referenced_outputs"] != set(run_ids):
            self.error("group-output-coverage", "Group comparison must cite the raw output of every compared run.", where)
        valid = len(self.errors) == before and all(run["valid"] for run in runs)
        self.groups.append({
            "group_review_id": group_id, "case_id": case_id, "run_ids": run_ids,
            "context_id": runs[0]["context_id"], "timestamp": reviewed["timestamp"],
            "valid": valid, "status": reviewed["status"] if valid else "inconclusive",
            "reviewer": reviewed["reviewer"], "artifact": pointer,
        })

    def read_index(self, evidence_path: str) -> None:
        value = self.json_file(evidence_path, "evidence-index")
        if value is None:
            return
        if value.get("schema_version") != "1":
            self.error("evidence-version", "Evidence index schema_version must be '1'.", "evidence-index")
        if value.get("matrix_source_sha256") != self.matrix_sha:
            self.error("evidence-matrix", "Index must bind the exact approved matrix source hash.", "evidence-index")
        for field in ("runs", "group_reviews"):
            if not isinstance(value.get(field), list):
                self.error("evidence-list", f"{field} must be a list (possibly empty).", "evidence-index")
        for number, raw in enumerate(value.get("runs", []) if isinstance(value.get("runs"), list) else []):
            self.read_run(raw, number)
        self.check_retests()
        for number, pointer in enumerate(value.get("group_reviews", []) if isinstance(value.get("group_reviews"), list) else []):
            self.read_group(pointer, number)

    def latest_runs(self, runs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        selected: dict[str, dict[str, Any]] = {}
        for run in runs:
            variant_id = run["variant_id"]
            prior = selected.get(variant_id)
            if prior is None:
                selected[variant_id] = run
            elif run["timestamp"] is None or prior["timestamp"] is None or run["timestamp"] == prior["timestamp"]:
                self.error("run-order", "Runs for one context/variant need distinct timestamps; cannot select a favorable result.", variant_id)
                selected[variant_id] = {**run, "status": "inconclusive", "valid": False}
            elif run["timestamp"] > prior["timestamp"]:
                selected[variant_id] = run
        return selected

    def claim(self, claim_id: str, claim: dict[str, Any], context_id: str,
              selected: dict[str, dict[str, Any]], mode: str, current: bool) -> dict[str, Any]:
        cases = claim["required_cases"]
        if all(("static" if self.cases[case_id]["kind"] in STATIC_KINDS else "model") != mode for case_id in cases):
            return {"status": "not_applicable", "eligible_for_current_release": False}
        states, required, chosen_ids, group_ids = [], [], [], []
        reasons: list[str] = []
        simulated = False
        for case_id in cases:
            variants = claim.get("variant_selection", {}).get(case_id, self.variants[case_id])
            case_run_ids: list[str] = []
            for variant_id in variants:
                required.append(variant_id)
                run = selected.get(variant_id)
                states.append(run["status"] if run else "not_run")
                if run:
                    chosen_ids.append(run["run_id"])
                    case_run_ids.append(run["run_id"])
                    simulated = simulated or run["runtime"].get("capability_simulation") is True
            if expected_checks(self.cases[case_id], {}, group=True):
                groups = [group for group in self.groups if group["context_id"] == context_id
                          and group["case_id"] == case_id and set(group["run_ids"]) == set(case_run_ids)]
                if groups:
                    dated = [group for group in groups if group["timestamp"] is not None]
                    latest = max(dated, key=lambda group: group["timestamp"]) if len(dated) == len(groups) else None
                    if latest is None or sum(group["timestamp"] == latest["timestamp"] for group in dated) != 1:
                        states.append("inconclusive")
                        reasons.append("Group review ordering is ambiguous.")
                    else:
                        states.append(latest["status"])
                        group_ids.append(latest["group_review_id"])
                else:
                    states.append("inconclusive" if case_run_ids else "not_run")
                    reasons.append(f"No group review for the selected {case_id} run set.")
        if claim_id in CAPABILITY_CLAIMS and simulated:
            states.append("inconclusive")
            reasons.append("Simulated capabilities do not verify live lookup, native-file parity or live handoff.")
        status = combined_status(states, claim=True)
        return {
            "status": status, "eligible_for_current_release": status == "verified" and current,
            "required_variant_ids": required, "selected_run_ids": chosen_ids,
            "group_review_ids": group_ids, "contains_simulated_capabilities": simulated,
            "platform_verification_eligible": status == "verified" and not simulated and mode == "model",
            "limitations": reasons,
        }

    def contexts(self) -> list[dict[str, Any]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for run in self.runs.values():
            if run["context_id"] is not None:
                grouped.setdefault(run["context_id"], []).append(run)
        result = []
        for context_id, runs in sorted(grouped.items()):
            selected = self.latest_runs(runs)
            snapshot = runs[0]["snapshot"]
            mode = runs[0]["verification_mode"]
            result.append({
                "context_id": context_id, **runs[0]["context"],
                "snapshot": snapshot,
                "claims": {claim_id: self.claim(claim_id, claim, context_id, selected, mode, snapshot["matches_current_canonical"])
                           for claim_id, claim in self.matrix.get("acceptance_claims", {}).items()},
            })
        return result

    def report(self, legacy_static_registry: dict[str, Any] | None = None) -> dict[str, Any]:
        contexts = self.contexts() if self.cases and not any(error["where"] == "matrix" or error["code"].startswith("matrix-") for error in self.errors) else []
        platform_spec = self.matrix.get("platform_status", [])
        platform_spec = platform_spec if isinstance(platform_spec, list) else []
        platforms: dict[str, dict[str, Any]] = {
            item["surface"]: {"surface": item["surface"], "status": "not_run", "actual_model_runs": 0,
                              "simulated_capability_runs": 0, "unverified_execution_records": 0, "context_ids": []}
            for item in platform_spec if isinstance(item, dict) and meaningful(item.get("surface"))
        }
        for run in self.runs.values():
            runtime = run["runtime"] if isinstance(run["runtime"], dict) else {}
            surface = runtime.get("surface")
            if not meaningful(surface) or run["verification_mode"] != "model":
                continue
            platform = platforms.setdefault(surface, {"surface": surface, "status": "not_run", "actual_model_runs": 0,
                                                       "simulated_capability_runs": 0, "unverified_execution_records": 0, "context_ids": []})
            if run["execution_status"] == "executed":
                if not run["valid"]:
                    platform["unverified_execution_records"] += 1
                elif runtime.get("capability_simulation") is True:
                    platform["simulated_capability_runs"] += 1
                else:
                    platform["actual_model_runs"] += 1
                platform["status"] = ("tested_partial" if platform["actual_model_runs"] else "simulation_only"
                                      if platform["simulated_capability_runs"] else "inconclusive")
            elif run["execution_status"] == "blocked" and platform["status"] == "not_run":
                platform["status"] = "blocked"
            if run["context_id"] and run["context_id"] not in platform["context_ids"]:
                platform["context_ids"].append(run["context_id"])
        qualified = []
        for context in contexts:
            claims = context["claims"]
            if context["verification_mode"] != "model" or not all(claims.get(name, {}).get("eligible_for_current_release") for name in REQUIRED_RELEASE_CLAIMS[:2]):
                continue
            if any(static["verification_mode"] == "static"
                   and static["snapshot"]["content_sha256"] == context["snapshot"]["content_sha256"]
                   and static["claims"].get("distribution_integrity", {}).get("eligible_for_current_release")
                   for static in contexts):
                qualified.append(context["context_id"])
        legacy_status = (legacy_static_registry or {}).get("status", "not_run")
        complete = bool(qualified) and not self.errors and legacy_status == "pass"
        counts = Counter(run["status"] for run in self.runs.values())
        coverage = []
        for case_id, variants in self.variants.items():
            for variant_id in variants:
                runs = [run for run in self.runs.values() if run["variant_id"] == variant_id]
                execution = ("executed" if any(run["execution_status"] == "executed" for run in runs)
                             else "blocked" if any(run["execution_status"] == "blocked" for run in runs) else "not_run")
                coverage.append({"case_id": case_id, "variant_id": variant_id, "execution_status": execution,
                                 "recorded_results": [{"run_id": run["run_id"], "context_id": run["context_id"], "status": run["status"]}
                                                      for run in runs]})
        requirements = self.matrix.get("requirements")
        return {
            "suite": "Thien-Skill-Risk-Process-Control Phase 3 retained evidence",
            "mode": "phase3_evidence_validation",
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "integrity_status": "fail" if self.errors else "pass",
            "acceptance_status": "evidence_complete" if complete else "incomplete",
            "legacy_static_registry": legacy_static_registry or {"status": "not_run"},
            "matrix": {"source_path": MATRIX_SOURCE, "source_sha256": self.matrix_sha,
                       "case_count": len(self.cases), "variant_count": sum(map(len, self.variants.values())),
                       "requirement_ids": sorted(requirements) if isinstance(requirements, dict) else []},
            "evidence_counts": {"retained_runs": len(self.runs), "run_statuses": dict(sorted(counts.items())),
                                "group_reviews": len(self.groups), "snapshots": len(self.snapshots)},
            "runs": [{
                **{key: run.get(key) for key in ("run_id", "case_id", "variant_id", "execution_status", "verification_mode", "status", "valid", "context_id", "retest_of")},
                "limitations": run["raw"].get("limitations"),
                "artifact_refs": {field: run["raw"].get(field) for field in ("raw_prompt", "raw_output", "tool_trace", "execution_record", "skill_snapshot", "review")},
                "review_metadata": {key: run["review"].get(key) for key in ("reviewer", "mandatory_checks", "reviewed_checks")} if run["review"] else None,
            } for run in self.runs.values()],
            "variant_coverage": coverage,
            "group_reviews": [{key: group[key] for key in ("group_review_id", "case_id", "run_ids", "context_id", "valid", "status", "reviewer")}
                              for group in self.groups],
            "claims_by_context": contexts,
            "per_platform": list(platforms.values()),
            "current_release_gate": {
                "status": "evidence_complete" if complete else "incomplete",
                "required_claims": list(REQUIRED_RELEASE_CLAIMS), "qualified_context_ids": qualified,
                "legacy_static_registry_status": legacy_status,
                "human_approval": "not_assessed", "installation": "not_run",
                "publication": "not_authorized_by_test_results",
            },
            "error_count": len(self.errors), "errors": self.errors, "warnings": self.warnings,
            "limitations": [
                "This validator does not execute models, authenticate executor identity, reconstruct hidden context, or independently establish review accuracy. It verifies retained bytes, metadata and attributed per-invariant reviews.",
                "A review pass for must_not_observe means the prohibited behavior was not observed. All mandatory checks are required; case counts, fixture existence and static passes are not behavioral acceptance.",
                "Claims apply only to the recorded runtime/model/capability conditions and exact skill snapshot. A simulated capability profile is not platform verification; historical snapshot results do not verify changed canonical content.",
                "Untested surfaces remain not_run. Valid ZIPs do not establish installation or cross-platform behavior, operating effectiveness, legal compliance, user approval or publication authority.",
                "A zero exit code indicates valid evidence structure, not complete acceptance. Check acceptance_status, individual claims, snapshot currency and current_release_gate separately.",
            ],
        }


def evaluate_phase3(repo_root: Path, matrix_path: str = DEFAULT_MATRIX,
                    evidence_path: str = DEFAULT_EVIDENCE,
                    legacy_static_registry: dict[str, Any] | None = None) -> dict[str, Any]:
    validator = EvidenceValidator(repo_root)
    validator.read_matrix(matrix_path)
    # Invalid/altered specifications cannot provide a trusted rubric for runs.
    if validator.matrix and not validator.errors:
        validator.read_index(evidence_path)
    return validator.report(legacy_static_registry)
