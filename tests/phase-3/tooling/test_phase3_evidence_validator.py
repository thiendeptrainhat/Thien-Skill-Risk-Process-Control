#!/usr/bin/env python3
"""Verifier self-tests ONLY: all receipts are synthetic, isolated temp data.

No model is invoked and no result here is evidence for an acceptance-matrix
case, installed platform, skill capability or release. Never copy these dummy
receipts into tests/phase-3/runs or its real evidence index.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPOSITORY / "scripts"))
from phase3_evidence import (  # noqa: E402
    DEFAULT_EVIDENCE, DEFAULT_MATRIX, MATRIX_SOURCE, EvidenceValidator,
    evaluate_phase3, expected_checks, safe_yaml, strict_json,
)
import run_tests  # noqa: E402


class SyntheticReceiptFixture:
    """Only writes into a caller-owned TemporaryDirectory, not the repository."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.source_root = "tests/phase-3/snapshots/round-1/skill"
        self.canonical = "skills/thien-skill-risk-process-control"
        self.files = {
            "SKILL.md": '---\n{"name":"thien-skill-risk-process-control"}\n---\nSynthetic verifier fixture, not a skill.\n',
            "integration/master-orchestrator-registry-entry.yaml": '{"version":"1.1.0"}\n',
            "references/fixture.md": "Synthetic verifier source only.\n",
        }
        for relative, text in self.files.items():
            self.write(self.canonical + "/" + relative, text)
            self.write(self.source_root + "/" + relative, text)
        self.snapshot = self.write_json("tests/phase-3/snapshots/round-1/manifest.json", {
            "skill_id": "thien-skill-risk-process-control", "skill_version": "1.1.0",
            "source_root": self.source_root, "canonical_source": self.canonical,
            "files": [self.pointer(self.source_root + "/" + relative) for relative in self.files],
        })
        self.matrix = {
            "artifact_kind": "synthetic_verifier_self_test_only",
            "baseline": {"skill_id": "thien-skill-risk-process-control"},
            "requirements": {"R01": "Synthetic verifier requirement, not acceptance evidence."},
            "cases": [self.case("P1-U01")],
            "acceptance_claims": {"core_business_logic": {"required_cases": ["P1-U01"]}},
            "platform_status": [{"surface": name, "status": "not_run"}
                                for name in ("Synthetic Codex surface", "Claude Desktop", "Claude Web", "ChatGPT Desktop", "ChatGPT Web")],
        }
        self.index = {"schema_version": "1", "runs": [], "group_reviews": []}
        self.save_matrix()
        self.save_index()

    @staticmethod
    def case(case_id: str, kind: str = "behavioral") -> dict:
        return {
            "id": case_id, "kind": kind, "requirements": ["R01"],
            "must_observe": ["Synthetic mandatory invariant used to test the validator."],
            "must_not_observe": ["Synthetic forbidden behavior used to test the validator."],
        }

    def write(self, relative: str, text: str) -> dict:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return self.pointer(relative)

    def write_json(self, relative: str, value: dict) -> dict:
        return self.write(relative, json.dumps(value, ensure_ascii=False, indent=2) + "\n")

    def pointer(self, relative: str) -> dict:
        return {"path": relative, "sha256": hashlib.sha256((self.root / relative).read_bytes()).hexdigest()}

    def save_matrix(self) -> None:
        source = self.write_json(MATRIX_SOURCE, self.matrix)
        self.write_json(DEFAULT_MATRIX, {"source": source, "matrix": self.matrix})
        self.index["matrix_source_sha256"] = source["sha256"]

    def save_index(self) -> None:
        self.write_json(DEFAULT_EVIDENCE, self.index)

    def find_case(self, case_id: str) -> dict:
        return next(case for case in self.matrix["cases"] if case["id"] == case_id)

    def add_run(self, run_id: str = "synthetic-run-1", case_id: str = "P1-U01",
                variant_id: str | None = None, *, result: str | None = "pass",
                minute: int = 0, mode: str = "model") -> dict:
        case = self.find_case(case_id)
        variant_id = variant_id or case_id + "-V01"
        prefix = "tests/phase-3/runs/" + run_id
        runtime = {
            "platform": "SYNTHETIC_VERIFIER_ONLY", "surface": "Synthetic Codex surface",
            "runtime": "unittest temporary-data generator, NOT a model executor",
            "model": "SYNTHETIC-NOT-A-MODEL" if mode == "model" else None,
            "model_identifier_status": "provided" if mode == "model" else "not_applicable",
            "capabilities": {"source": "synthetic verifier metadata; no tool or model called"},
            "capability_simulation": False, "fresh_context": True,
        }
        run = {
            "run_id": run_id, "case_id": case_id, "variant_id": variant_id,
            "requirement_ids": case["requirements"], "execution_status": "executed",
            "verification_mode": mode, "timestamp": f"2026-08-28T10:{minute:02d}:00+07:00",
            "runtime": runtime, "authorized_source_scope": "Synthetic verifier unit-test data only.",
            "inputs": [{"fixture_id": "SYNTHETIC-VERIFIER-ONLY", "version": "1",
                        "artifact": self.write(prefix + "/input.txt", "Synthetic verifier input.\n")}],
            "skill_snapshot": self.snapshot,
            "raw_prompt": self.write(prefix + "/prompt.txt", "Synthetic verifier prompt, never sent to a model.\n"),
            "raw_output": self.write(prefix + "/output.txt", "Synthetic verifier observation.\nNo actual model was run.\n"),
            "tool_trace": self.write(prefix + "/trace.txt", "Synthetic verifier tool trace. No actual tool called.\n"),
            "execution_record": self.write_json(prefix + "/execution.json", {
                "run_id": run_id, "dispatch": {"kind": "synthetic verifier self-test"},
                "completion": {"kind": "synthetic verifier self-test"},
            }),
            "review": None, "limitations": ["SYNTHETIC verifier self-test; not a real model run."],
            "retest_of": [],
        }
        if result is not None:
            variant = next((variant for variant in case.get("variants", []) if variant["variant_id"] == variant_id), {})
            checks = {key: {"result": "pass", "rationale": "Synthetic verifier assertion, not a behavioral review.",
                            "evidence_refs": [{"artifact": "raw_output", "locator": "L1-L2"}]}
                      for key in expected_checks(case, variant)}
            if result != "pass":
                checks[next(iter(checks))]["result"] = result
            run["review"] = self.write_json(prefix + "/review.json", {
                "run_id": run_id, "reviewer": {"name": "Synthetic verifier", "role": "unittest", "relationship": "self_check"},
                "timestamp": "2026-08-28T12:00:00+07:00", "rubric_source_sha256": self.index["matrix_source_sha256"],
                "checks": checks, "result": result, "limitations": ["Synthetic verifier assertion only."],
            })
        self.index["runs"].append(run)
        self.save_index()
        return run

    def edit_review(self, run: dict, edit) -> None:
        path = run["review"]["path"]
        value = json.loads((self.root / path).read_text(encoding="utf-8"))
        edit(value)
        run["review"] = self.write_json(path, value)
        self.save_index()

    def add_group(self, run_ids: list[str], result: str = "pass", group_id: str = "synthetic-group-1") -> dict:
        case = self.find_case("P1-U15")
        value = {
            "group_review_id": group_id, "case_id": case["id"], "run_ids": run_ids,
            "reviewer": {"name": "Synthetic reviewer", "role": "unittest", "relationship": "self_check"},
            "timestamp": "2026-08-28T13:00:00+07:00", "rubric_source_sha256": self.index["matrix_source_sha256"],
            "checks": {key: {"result": result, "rationale": "Synthetic cross-output verifier check only.",
                            "evidence_refs": [{"run_id": run_id, "artifact": "raw_output", "locator": "entire_artifact"}
                                              for run_id in run_ids]}
                       for key in expected_checks(case, {}, group=True)},
            "result": result, "limitations": ["Synthetic verifier assertion only."],
        }
        pointer = self.write_json("tests/phase-3/runs/" + group_id + ".json", value)
        self.index["group_reviews"].append(pointer)
        self.save_index()
        return value

    def result(self, legacy: dict | None = None) -> dict:
        self.save_index()
        return evaluate_phase3(self.root, legacy_static_registry=legacy)


class Phase3EvidenceValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="rpc-evidence-verifier-only-")
        self.addCleanup(self.temporary.cleanup)
        self.fixture = SyntheticReceiptFixture(Path(self.temporary.name))

    def assertError(self, report: dict, code: str) -> None:
        self.assertEqual(report["integrity_status"], "fail", report["errors"])
        self.assertIn(code, [error["code"] for error in report["errors"]], report["errors"])
        self.assertEqual(report["acceptance_status"], "incomplete")

    def new_fixture(self) -> SyntheticReceiptFixture:
        temporary = tempfile.TemporaryDirectory(prefix="rpc-evidence-verifier-only-")
        self.addCleanup(temporary.cleanup)
        return SyntheticReceiptFixture(Path(temporary.name))

    def claim(self, report: dict, name: str = "core_business_logic", index: int = 0) -> dict:
        return report["claims_by_context"][index]["claims"][name]

    def test_empty_index_is_not_behavioral_acceptance(self) -> None:
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(report["acceptance_status"], "incomplete")
        self.assertEqual(report["claims_by_context"], [])
        self.assertTrue(all(surface["status"] == "not_run" for surface in report["per_platform"]))
        self.assertEqual(report["variant_coverage"][0]["execution_status"], "not_run")

    def test_complete_synthetic_receipt_checks_integrity_not_executor_authenticity(self) -> None:
        self.fixture.add_run()
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(self.claim(report)["status"], "verified")
        self.assertTrue(self.claim(report)["eligible_for_current_release"])
        self.assertEqual(report["acceptance_status"], "incomplete")
        self.assertIn("authenticate executor", " ".join(report["limitations"]))
        self.assertTrue(all(surface["status"] == "not_run" for surface in report["per_platform"] if surface["surface"] != "Synthetic Codex surface"))

    def test_unreviewed_is_not_pass(self) -> None:
        self.fixture.add_run(result=None)
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(report["runs"][0]["status"], "executed_unreviewed")
        self.assertEqual(self.claim(report)["status"], "executed_unreviewed")

    def test_missing_raw_output_is_inconclusive(self) -> None:
        run = self.fixture.add_run()
        run.pop("raw_output")
        report = self.fixture.result()
        self.assertError(report, "artifact-pointer")
        self.assertEqual(report["runs"][0]["status"], "inconclusive")
        self.assertEqual(report["per_platform"][0]["actual_model_runs"], 0)
        self.assertEqual(report["per_platform"][0]["status"], "inconclusive")

    def test_changed_raw_bytes_do_not_match_retained_hash(self) -> None:
        run = self.fixture.add_run()
        self.fixture.write(run["raw_output"]["path"], "Changed bytes.\n")
        self.assertError(self.fixture.result(), "artifact-hash-mismatch")

    def test_supplementary_structured_artifact_is_validated(self) -> None:
        run = self.fixture.add_run()
        run["additional_artifacts"] = [self.fixture.write_json(
            "tests/phase-3/runs/synthetic-run-1/data.json", {"synthetic": True})]
        self.assertEqual(self.fixture.result()["integrity_status"], "pass")

    def test_changed_supplementary_bytes_invalidate_evidence(self) -> None:
        run = self.fixture.add_run()
        pointer = self.fixture.write_json("tests/phase-3/runs/synthetic-run-1/data.json", {"synthetic": True})
        run["additional_artifacts"] = [pointer]
        self.fixture.write_json(pointer["path"], {"synthetic": "changed"})
        self.assertError(self.fixture.result(), "artifact-hash-mismatch")

    def test_duplicate_supplementary_artifact_rejected(self) -> None:
        run = self.fixture.add_run()
        pointer = self.fixture.write_json("tests/phase-3/runs/synthetic-run-1/data.json", {"synthetic": True})
        run["additional_artifacts"] = [pointer, copy.deepcopy(pointer)]
        self.assertError(self.fixture.result(), "run-additional-duplicate")

    def test_supplementary_artifacts_require_a_list(self) -> None:
        run = self.fixture.add_run()
        run["additional_artifacts"] = {"not": "a list"}
        self.assertError(self.fixture.result(), "run-additional-artifacts")

    def test_missing_forbidden_behavior_review_is_not_pass(self) -> None:
        run = self.fixture.add_run()
        self.fixture.edit_review(run, lambda review: review["checks"].pop("case.must_not_observe.1"))
        self.assertError(self.fixture.result(), "review-coverage")

    def test_summary_pass_cannot_override_failed_invariant(self) -> None:
        run = self.fixture.add_run(result="fail")
        self.fixture.edit_review(run, lambda review: review.update(result="pass"))
        self.assertError(self.fixture.result(), "review-result")

    def test_real_failed_review_has_valid_integrity_but_no_acceptance(self) -> None:
        self.fixture.add_run(result="fail")
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(self.claim(report)["status"], "fail")
        self.assertFalse(self.claim(report)["eligible_for_current_release"])

    def test_out_of_range_locator_rejected(self) -> None:
        run = self.fixture.add_run()
        self.fixture.edit_review(run, lambda review: review["checks"]["case.must_observe.1"]["evidence_refs"][0].update(locator="L100-L101"))
        self.assertError(self.fixture.result(), "review-locator")

    def test_review_cannot_use_expected_input_as_observed_output(self) -> None:
        run = self.fixture.add_run()
        self.fixture.edit_review(run, lambda review: review["checks"]["case.must_observe.1"]["evidence_refs"][0].update(artifact="inputs"))
        self.assertError(self.fixture.result(), "review-evidence")

    def test_review_cannot_rely_only_on_execution_metadata(self) -> None:
        run = self.fixture.add_run()
        def edit(review):
            for check in review["checks"].values():
                check["evidence_refs"] = [{"artifact": "execution_record", "locator": "entire_artifact"}]
        self.fixture.edit_review(run, edit)
        self.assertError(self.fixture.result(), "review-output-coverage")

    def test_old_snapshot_remains_valid_but_is_ineligible_for_changed_source(self) -> None:
        self.fixture.add_run()
        self.fixture.write(self.fixture.canonical + "/references/fixture.md", "New canonical source.\n")
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(self.claim(report)["status"], "verified")
        self.assertFalse(self.claim(report)["eligible_for_current_release"])
        self.assertFalse(report["claims_by_context"][0]["snapshot"]["matches_current_canonical"])

    def test_snapshot_inventory_must_be_complete(self) -> None:
        self.fixture.add_run()
        self.fixture.write(self.fixture.source_root + "/unlisted.txt", "Unlisted retained source.\n")
        self.assertError(self.fixture.result(), "snapshot-completeness")

    def test_unknown_case_or_variant_rejected(self) -> None:
        run = self.fixture.add_run()
        run["variant_id"] = "P1-U01-V99"
        self.assertError(self.fixture.result(), "run-case-variant")

    def test_duplicate_run_ids_rejected(self) -> None:
        run = self.fixture.add_run()
        self.fixture.index["runs"].append(copy.deepcopy(run))
        self.assertError(self.fixture.result(), "run-duplicate")

    def test_matrix_envelope_cannot_weaken_approved_invariants(self) -> None:
        path = self.fixture.root / DEFAULT_MATRIX
        envelope = json.loads(path.read_text())
        envelope["matrix"]["cases"][0]["must_not_observe"] = []
        self.fixture.write_json(DEFAULT_MATRIX, envelope)
        self.assertError(self.fixture.result(), "matrix-content")

    def test_repository_escape_rejected(self) -> None:
        run = self.fixture.add_run()
        run["raw_output"]["path"] = "../outside.txt"
        self.assertError(self.fixture.result(), "artifact-path")

    def test_symlink_evidence_rejected(self) -> None:
        run = self.fixture.add_run()
        link = self.fixture.root / "tests/phase-3/runs/output-link.txt"
        link.symlink_to(self.fixture.root / run["raw_output"]["path"])
        run["raw_output"]["path"] = link.relative_to(self.fixture.root).as_posix()
        self.assertError(self.fixture.result(), "artifact-symlink")

    def test_execution_artifacts_must_have_pairwise_distinct_resolved_paths(self) -> None:
        fields = ("raw_prompt", "raw_output", "tool_trace", "execution_record")
        for left_number, left in enumerate(fields):
            for right in fields[left_number + 1:]:
                with self.subTest(left=left, right=right):
                    fixture = self.new_fixture()
                    run = fixture.add_run()
                    run[right] = copy.deepcopy(run[left])
                    self.assertError(fixture.result(), "run-artifact-path-alias")

    def test_execution_artifacts_must_have_distinct_hashes_even_at_different_paths(self) -> None:
        run = self.fixture.add_run()
        output_bytes = (self.fixture.root / run["raw_output"]["path"]).read_text(encoding="utf-8")
        run["tool_trace"] = self.fixture.write(run["tool_trace"]["path"], output_bytes)
        report = self.fixture.result()
        self.assertError(report, "run-artifact-content-alias")
        self.assertNotIn("run-artifact-path-alias", [error["code"] for error in report["errors"]])

    def test_model_case_requires_recorded_fresh_context(self) -> None:
        run = self.fixture.add_run()
        run["runtime"]["fresh_context"] = False
        self.assertError(self.fixture.result(), "runtime-context")

    def test_unavailable_model_identifier_is_explicit_not_fabricated(self) -> None:
        run = self.fixture.add_run()
        run["runtime"].update(model=None, model_identifier_status="not_available")
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        run["runtime"]["model"] = "an invented exact model"
        self.assertError(self.fixture.result(), "runtime-model")

    def test_timezone_is_required(self) -> None:
        run = self.fixture.add_run()
        run["timestamp"] = "2026-08-28T10:00:00"
        self.assertError(self.fixture.result(), "timestamp")

    def test_latest_failed_retest_cannot_be_hidden_by_earlier_pass(self) -> None:
        self.fixture.add_run("synthetic-older-pass", minute=0)
        newer = self.fixture.add_run("synthetic-newer-fail", result="fail", minute=1)
        newer["retest_of"] = ["synthetic-older-pass"]
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(self.claim(report)["status"], "fail")
        self.assertEqual(self.claim(report)["selected_run_ids"], ["synthetic-newer-fail"])

    def test_retest_links_are_validated(self) -> None:
        run = self.fixture.add_run()
        run["retest_of"] = ["a-missing-run"]
        self.assertError(self.fixture.result(), "run-retest-link")

    def test_retest_cannot_self_reference(self) -> None:
        run = self.fixture.add_run()
        run["retest_of"] = [run["run_id"]]
        self.assertError(self.fixture.result(), "run-retest-self")

    def test_retest_must_use_same_case_and_variant(self) -> None:
        case = self.fixture.find_case("P1-U01")
        case["variants"] = [{"variant_id": "P1-U01-V01"}, {"variant_id": "P1-U01-V02"}]
        self.fixture.save_matrix()
        self.fixture.add_run("synthetic-prior", variant_id="P1-U01-V01", minute=0)
        current = self.fixture.add_run("synthetic-current", variant_id="P1-U01-V02", minute=1)
        current["retest_of"] = ["synthetic-prior"]
        self.assertError(self.fixture.result(), "run-retest-scope")

    def test_retest_rejects_blocked_prior(self) -> None:
        prior = self.fixture.add_run("synthetic-prior", minute=0)
        prior.update(execution_status="blocked", review=None)
        current = self.fixture.add_run("synthetic-current", minute=1)
        current["retest_of"] = ["synthetic-prior"]
        self.assertError(self.fixture.result(), "run-retest-execution")

    def test_retest_rejects_not_run_prior(self) -> None:
        prior = self.fixture.add_run("synthetic-prior", minute=0)
        prior.update(execution_status="not_run", review=None)
        current = self.fixture.add_run("synthetic-current", minute=1)
        current["retest_of"] = ["synthetic-prior"]
        self.assertError(self.fixture.result(), "run-retest-execution")

    def test_retest_rejects_invalid_prior_record(self) -> None:
        prior = self.fixture.add_run("synthetic-prior", minute=0)
        self.fixture.write(prior["raw_output"]["path"], "Changed prior bytes.\n")
        current = self.fixture.add_run("synthetic-current", minute=1)
        current["retest_of"] = ["synthetic-prior"]
        self.assertError(self.fixture.result(), "run-retest-prior-invalid")

    def test_retest_propagates_prior_link_invalidity_independent_of_index_order(self) -> None:
        current = self.fixture.add_run("synthetic-current", minute=2)
        current["retest_of"] = ["synthetic-prior"]
        prior = self.fixture.add_run("synthetic-prior", minute=1)
        prior["retest_of"] = ["a-missing-run"]
        self.assertError(self.fixture.result(), "run-retest-prior-invalid")

    def test_retest_rejects_prior_without_timestamp(self) -> None:
        prior = self.fixture.add_run("synthetic-prior", minute=0)
        prior.pop("timestamp")
        current = self.fixture.add_run("synthetic-current", minute=1)
        current["retest_of"] = ["synthetic-prior"]
        self.assertError(self.fixture.result(), "run-retest-timestamp")

    def test_retest_rejects_current_without_timestamp(self) -> None:
        self.fixture.add_run("synthetic-prior", minute=0)
        current = self.fixture.add_run("synthetic-current", minute=1)
        current.pop("timestamp")
        current["retest_of"] = ["synthetic-prior"]
        self.assertError(self.fixture.result(), "run-retest-timestamp")

    def test_retest_rejects_non_later_timestamp(self) -> None:
        self.fixture.add_run("synthetic-prior", minute=1)
        current = self.fixture.add_run("synthetic-current", minute=0)
        current["retest_of"] = ["synthetic-prior"]
        self.assertError(self.fixture.result(), "run-retest-order")

    def test_retest_allows_valid_executed_prior_with_failed_or_missing_review(self) -> None:
        for result in ("fail", None):
            with self.subTest(prior_review_result=result):
                fixture = self.new_fixture()
                fixture.add_run("synthetic-prior", result=result, minute=0)
                current = fixture.add_run("synthetic-current", minute=1)
                current["retest_of"] = ["synthetic-prior"]
                report = fixture.result()
                self.assertEqual(report["integrity_status"], "pass", report["errors"])
                self.assertEqual(self.claim(report)["status"], "verified")

    def test_same_time_retests_are_not_cherry_picked(self) -> None:
        self.fixture.add_run("synthetic-pass", result="pass")
        self.fixture.add_run("synthetic-fail", result="fail")
        self.assertError(self.fixture.result(), "run-order")

    def setup_group_case(self) -> None:
        case = self.fixture.case("P1-U15", "behavioral_document_variants")
        case["variants"] = [{"variant_id": f"P1-U15-V{number:02d}"} for number in range(1, 4)]
        case["group_must_observe"] = ["Synthetic invariant comparing all three outputs."]
        self.fixture.matrix["cases"] = [case]
        self.fixture.matrix["acceptance_claims"] = {"file_input_parity": {"required_cases": ["P1-U15"]}}
        self.fixture.save_matrix()
        for number in range(1, 4):
            self.fixture.add_run(f"synthetic-format-{number}", "P1-U15", f"P1-U15-V{number:02d}", minute=number)

    def test_group_parity_requires_cross_output_review(self) -> None:
        self.setup_group_case()
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(self.claim(report, "file_input_parity")["status"], "inconclusive")
        self.fixture.add_group([f"synthetic-format-{number}" for number in range(1, 4)])
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(self.claim(report, "file_input_parity")["status"], "verified")

    def test_group_review_for_old_run_does_not_cover_a_retest(self) -> None:
        self.setup_group_case()
        self.fixture.add_group([f"synthetic-format-{number}" for number in range(1, 4)])
        self.fixture.add_run("synthetic-format-1-retest", "P1-U15", "P1-U15-V01", minute=4)
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(self.claim(report, "file_input_parity")["status"], "inconclusive")

    def test_simulated_lookup_cannot_verify_live_capability(self) -> None:
        self.fixture.matrix["acceptance_claims"] = {"live_external_lookup": {"required_cases": ["P1-U01"]}}
        self.fixture.save_matrix()
        run = self.fixture.add_run()
        run["runtime"]["capability_simulation"] = True
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(self.claim(report, "live_external_lookup")["status"], "inconclusive")
        self.assertEqual(report["per_platform"][0]["status"], "simulation_only")

    def test_static_receipt_does_not_count_as_model_execution(self) -> None:
        self.fixture.matrix["cases"] = [self.fixture.case("P1-P01", "packaging")]
        self.fixture.matrix["acceptance_claims"] = {"distribution_integrity": {"required_cases": ["P1-P01"]}}
        self.fixture.save_matrix()
        self.fixture.add_run(case_id="P1-P01", mode="static")
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(self.claim(report, "distribution_integrity")["status"], "verified")
        self.assertTrue(all(surface["status"] == "not_run" for surface in report["per_platform"]))

    def test_cannot_substitute_static_validation_for_behavior(self) -> None:
        self.fixture.add_run(mode="static")
        self.assertError(self.fixture.result(), "run-verification-mode")

    def test_claims_cannot_combine_different_runtime_models(self) -> None:
        self.fixture.matrix["cases"].append(self.fixture.case("P1-U02"))
        self.fixture.matrix["acceptance_claims"]["core_business_logic"]["required_cases"].append("P1-U02")
        self.fixture.save_matrix()
        self.fixture.add_run("synthetic-one", case_id="P1-U01")
        second = self.fixture.add_run("synthetic-two", case_id="P1-U02")
        second["runtime"]["model"] = "SYNTHETIC-DIFFERENT-MODEL"
        report = self.fixture.result()
        self.assertEqual(len(report["claims_by_context"]), 2)
        self.assertTrue(all(context["claims"]["core_business_logic"]["status"] != "verified" for context in report["claims_by_context"]))

    def test_pending_and_blocked_records_do_not_need_fake_outputs(self) -> None:
        self.fixture.index["runs"] = [{
            "run_id": "synthetic-blocked", "case_id": "P1-U01", "variant_id": "P1-U01-V01",
            "requirement_ids": ["R01"], "execution_status": "blocked",
            "limitations": ["Synthetic unavailable capability condition."],
        }]
        report = self.fixture.result()
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(report["runs"][0]["status"], "blocked")
        self.assertEqual(report["acceptance_status"], "incomplete")

    def test_complete_gate_requires_static_plus_same_context_business_and_compatibility(self) -> None:
        self.fixture.matrix["cases"] += [self.fixture.case("P1-U22", "compatibility_fixture_and_static"), self.fixture.case("P1-P01", "packaging")]
        self.fixture.matrix["acceptance_claims"].update({
            "backward_compatibility": {"required_cases": ["P1-U22"]},
            "distribution_integrity": {"required_cases": ["P1-P01"]},
        })
        self.fixture.save_matrix()
        self.fixture.add_run("synthetic-core")
        self.fixture.add_run("synthetic-compatibility", case_id="P1-U22")
        self.fixture.add_run("synthetic-static", case_id="P1-P01", mode="static")
        incomplete = self.fixture.result()
        self.assertEqual(incomplete["acceptance_status"], "incomplete")
        report = self.fixture.result(legacy={"status": "pass", "note": "Synthetic static receipt only."})
        self.assertEqual(report["integrity_status"], "pass", report["errors"])
        self.assertEqual(report["acceptance_status"], "evidence_complete")
        self.assertEqual(report["current_release_gate"]["human_approval"], "not_assessed")
        self.assertEqual(report["current_release_gate"]["installation"], "not_run")

    def test_duplicate_json_keys_and_nonfinite_numbers_rejected(self) -> None:
        for text in ('{"key":1,"key":2}', '{"key":NaN}', '{"key":Infinity}'):
            with self.assertRaises(ValueError):
                strict_json(text)

    @unittest.skipUnless(shutil.which("ruby"), "Ruby safe YAML parser is unavailable; no installation attempted.")
    def test_safe_yaml_non_json_source_and_duplicate_keys(self) -> None:
        self.assertEqual(safe_yaml('name: synthetic-verifier\nversion: "1.1.0"\n'), {
            "name": "synthetic-verifier", "version": "1.1.0",
        })
        with self.assertRaises(ValueError):
            safe_yaml('name: synthetic-one\nname: synthetic-two\n')
        with self.assertRaises(ValueError):
            safe_yaml('payload: !ruby/object:Object {}\n')

    def test_malformed_run_metadata_fails_without_traceback(self) -> None:
        run = self.fixture.add_run()
        for field, value, code in (
            ("execution_status", [], "run-execution-status"),
            ("requirement_ids", {}, "run-requirements"),
            ("verification_mode", [], "run-verification-mode"),
            ("runtime", [], "runtime-metadata"),
            ("inputs", {}, "run-inputs"),
            ("retest_of", {}, "run-retest"),
        ):
            with self.subTest(field=field):
                original = run[field]
                run[field] = value
                self.assertError(self.fixture.result(), code)
                run[field] = original
        for field, value, code in (
            ("model_identifier_status", {}, "runtime-model"),
            ("capability_simulation", {}, "runtime-simulation"),
            ("capabilities", [], "runtime-capabilities"),
        ):
            with self.subTest(field=field):
                original = run["runtime"][field]
                run["runtime"][field] = value
                self.assertError(self.fixture.result(), code)
                run["runtime"][field] = original

    def test_malformed_review_metadata_fails_without_traceback(self) -> None:
        run = self.fixture.add_run()
        original = json.loads((self.fixture.root / run["review"]["path"]).read_text())
        edits = [
            (lambda review: review.update(result={}), "review-result"),
            (lambda review: review["reviewer"].update(relationship={}), "reviewer"),
            (lambda review: review["checks"]["case.must_observe.1"].update(result={}), "review-check"),
            (lambda review: review["checks"]["case.must_observe.1"]["evidence_refs"][0].update(run_id=[]), "review-evidence"),
            (lambda review: review["checks"]["case.must_observe.1"]["evidence_refs"][0].update(artifact=[]), "review-evidence"),
        ]
        for number, (edit, code) in enumerate(edits):
            with self.subTest(number=number):
                self.fixture.write_json(run["review"]["path"], original)
                self.fixture.edit_review(run, edit)
                self.assertError(self.fixture.result(), code)

    def test_malformed_approved_matrix_schema_fails_without_traceback(self) -> None:
        original = copy.deepcopy(self.fixture.matrix)
        edits = [
            (lambda matrix: matrix.update(requirements=None), "matrix-requirements"),
            (lambda matrix: matrix.update(baseline=[]), "matrix-baseline"),
            (lambda matrix: matrix["acceptance_claims"]["core_business_logic"].update(variant_selection=[]), "matrix-claim-selection"),
        ]
        for number, (edit, code) in enumerate(edits):
            with self.subTest(number=number):
                self.fixture.matrix = copy.deepcopy(original)
                edit(self.fixture.matrix)
                self.fixture.save_matrix()
                self.assertError(self.fixture.result(), code)

    def test_legacy_payload_keeps_static_status_and_zero_behavioral_execution(self) -> None:
        report = run_tests.TestReport()
        payload = run_tests.result_payload(report, [])
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["behavioral"]["executed"], 0)
        self.assertEqual(payload["behavioral"]["status"], "not_run")

    def test_phase3_write_results_flag_is_rejected_before_any_write(self) -> None:
        old = self.fixture.write("tests/acceptance-report.md", "Historical summary must remain unchanged.\n")
        completed = subprocess.run([
            sys.executable, str(REPOSITORY / "scripts/run_tests.py"), "--repo-root", str(self.fixture.root),
            "--phase3", "--write-results",
        ], capture_output=True, text=True, check=False, timeout=15)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("historical", completed.stderr)
        self.assertEqual(self.fixture.pointer(old["path"]), old)
        self.assertFalse((self.fixture.root / "tests/deterministic-results.json").exists())


if __name__ == "__main__":
    unittest.main()
