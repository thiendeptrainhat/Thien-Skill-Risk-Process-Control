"""Focused unit tests for the read-only release inspector."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


INSPECTOR_PATH = Path(__file__).with_name("inspect_release.py")
SPEC = importlib.util.spec_from_file_location("release_inspector_under_test", INSPECTOR_PATH)
assert SPEC is not None and SPEC.loader is not None
inspector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspector)


class ReleaseInspectorTests(unittest.TestCase):
    def test_current_identity_and_preservation_baseline(self) -> None:
        self.assertEqual(inspector.SKILL_ID, "thien-skill-risk-control-process")
        self.assertEqual(inspector.SKILL, inspector.SKILL_ID)
        self.assertEqual(
            inspector.BASELINE,
            "38e30011371d1aafe1f4b715c65fdd74b76b6396",
        )
        release = {
            "skill_id": inspector.SKILL_ID,
            "skill_version": "1.2.0",
            "canonical_source": f"skills/{inspector.SKILL_ID}",
            "artifact_directory": "dist/1.2.0",
        }
        self.assertEqual(
            inspector.validate_release_identity(release),
            ("1.2.0", f"skills/{inspector.SKILL_ID}", "dist/1.2.0"),
        )
        release["skill_id"] = "thien-skill-risk-process-control"
        with self.assertRaisesRegex(ValueError, "skill_id"):
            inspector.validate_release_identity(release)

    def test_frozen_selection_uses_policy_and_baseline_intersection(self) -> None:
        baseline = {
            "dist/1.1.1/package.zip",
            "tests/phase-3/static/result.json",
            "tests/phase-3/tooling/inspect_release.py",
            "tests/acceptance-report.md",
        }
        selected = inspector.select_immutable_paths(
            baseline,
            ("dist/", "tests/phase-3/static/"),
            ("tests/acceptance-report.md", "tests/not-in-baseline.json"),
        )
        self.assertEqual(
            selected,
            [
                "dist/1.1.1/package.zip",
                "tests/acceptance-report.md",
                "tests/phase-3/static/result.json",
            ],
        )
        self.assertNotIn("tests/phase-3/tooling/inspect_release.py", selected)
        self.assertNotIn("tests/not-in-baseline.json", selected)

    def test_policy_is_strict_and_does_not_infer_all_tests_are_frozen(self) -> None:
        policy = {
            "schema_version": "1.0",
            "retention": {
                "immutable_historical_prefixes": ["tests/phase-3/static/", "dist/"],
                "immutable_historical_files": ["tests/acceptance-report.md"],
            },
        }
        parsed = inspector.parse_hygiene_policy(json.dumps(policy).encode())
        self.assertEqual(
            parsed["immutable_historical_prefixes"],
            ("tests/phase-3/static/", "dist/"),
        )
        malformed = b'{"schema_version":"1.0","retention":{"immutable_historical_prefixes":["tests/"],"immutable_historical_prefixes":[],"immutable_historical_files":[]}}'
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            inspector.parse_hygiene_policy(malformed)
        policy["retention"]["immutable_historical_prefixes"] = ["../tests/"]
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            inspector.parse_hygiene_policy(json.dumps(policy).encode())

    def test_release_addendum_covers_current_without_relabeling_history(self) -> None:
        historical = "- **Covered skill versions:** `1.1.1`.\n"
        addendum = "- **Current release covered version:** `1.2.0`.\n"
        self.assertTrue(inspector.license_application_covers(historical, "1.1.1"))
        self.assertFalse(inspector.license_application_covers(historical, "1.2.0"))
        self.assertTrue(
            inspector.license_application_covers(historical + addendum, "1.2.0")
        )
        self.assertTrue(inspector.historical_license_label_preserved(historical + addendum))
        relabeled = "- **Covered skill versions:** `1.2.0`.\n"
        self.assertFalse(inspector.historical_license_label_preserved(relabeled))
        appended_to_history = historical + relabeled + addendum
        self.assertFalse(inspector.historical_license_label_preserved(appended_to_history))

    def test_duplicate_checksum_entries_hard_fail(self) -> None:
        digest = "0" * 64
        duplicate = f"{digest}  package.zip\n{digest}  package.zip\n".encode()
        with self.assertRaisesRegex(ValueError, "Duplicate checksum"):
            inspector.parse_checksums(duplicate)


if __name__ == "__main__":
    unittest.main()
