"""Focused temp-directory tests for Stage 2 path and publication safety."""
from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import assemble_phase3_evidence as assemble  # noqa: E402
import capture_phase3_run as capture  # noqa: E402
import run_tests  # noqa: E402
import safe_filesystem  # noqa: E402

VALIDATOR_PATH = (
    REPO
    / "skills"
    / "thien-skill-risk-control-process"
    / "scripts"
    / "validate_package.py"
)
SPEC = importlib.util.spec_from_file_location("stage2_canonical_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class Stage2PathSafetyTests(unittest.TestCase):
    def temporary(self):
        return tempfile.TemporaryDirectory(dir="/private/tmp")

    def capture_fixture(self, base: Path, trace: bytes = b'{"started_at":"2026-01-01T00:00:00Z"}'):
        repo, output = base / "repo", base / "output"
        run_id, variant = "P1-U01-V01-R99", "P1-U01-V01"
        run = repo / "tests" / "phase-3" / "runs" / run_id
        run.mkdir(parents=True)
        (run / "prompt.txt").write_text("actual prompt\n")
        output.mkdir()
        (output / "output.md").write_text("actual output\n")
        (output / "tool-trace.json").write_bytes(trace)
        phase3 = repo / "tests" / "phase-3"
        (phase3 / "acceptance-matrix.json").write_text(
            json.dumps({"matrix": {"cases": [{"id": "P1-U01", "requirements": ["IV"]}]}})
        )
        fixture = phase3 / "fixtures" / variant
        fixture.mkdir(parents=True)
        (fixture / "input.md").write_text("fixture\n")
        (phase3 / "harness.md").write_text("harness\n")
        snapshot = phase3 / "snapshots" / "round-1"
        snapshot.mkdir(parents=True)
        (snapshot / "manifest.json").write_text("{}\n")
        return repo, output, run, run_id

    @staticmethod
    def capture_args(repo: Path, output: Path, run_id: str) -> list[str]:
        return [
            "--repo-root", str(repo), "--run-id", run_id,
            "--output-dir", str(output), "--agent-task", "/root/temp-test",
        ]

    def assemble_fixture(self, base: Path):
        repo = base / "repo"
        phase3 = repo / "tests" / "phase-3"
        run = phase3 / "runs" / "P1-U01-V01-R99"
        run.mkdir(parents=True)
        (run / "run.json").write_text(json.dumps({"run_id": run.name, "review": None}))
        (phase3 / "reviews").mkdir()
        (phase3 / "acceptance-matrix.json").write_text(
            json.dumps({"source": {"sha256": "a" * 64}})
        )
        index = phase3 / "evidence-index.json"
        index.write_text("original index\n")
        return repo, index

    @staticmethod
    def policy(**overrides):
        value = {
            "schema_version": "1.0",
            "junk_names": [".DS_Store"],
            "junk_suffixes": [".pyc"],
            "excluded_roots": [".git"],
            "private_path_patterns": ["/Users/", "C:\\Users\\"],
            "allowed_private_path_files": ["tests/frozen-receipt.txt"],
            "limits": {
                "max_file_bytes": 1000,
                "max_release_directory_bytes": 10,
                "max_dist_bytes": 15,
            },
        }
        value.update(overrides)
        return value

    def test_capture_rejects_symlink_and_dangling_destination_parent(self):
        for dangling in (False, True):
            with self.subTest(dangling=dangling), self.temporary() as name:
                repo, output, run, run_id = self.capture_fixture(Path(name))
                runs = run.parent
                for path in sorted(runs.rglob("*"), reverse=True):
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        path.rmdir()
                runs.rmdir()
                target = Path(name) / ("missing" if dangling else "outside")
                if not dangling:
                    target.mkdir()
                runs.symlink_to(target, target_is_directory=True)
                with self.assertRaisesRegex(ValueError, "Symlink not permitted"):
                    capture.main(self.capture_args(repo, output, run_id))

        with self.temporary() as name:
            repo, _, _, run_id = self.capture_fixture(Path(name))
            with self.assertRaisesRegex(ValueError, "isolated child directory"):
                capture.main(self.capture_args(repo, Path("/private/tmp"), run_id))

    def test_capture_validates_before_write_and_rolls_back_publish_failure(self):
        with self.temporary() as name:
            repo, output, run, run_id = self.capture_fixture(Path(name), trace=b"not json")
            with self.assertRaisesRegex(ValueError, "Invalid executor tool trace"):
                capture.main(self.capture_args(repo, output, run_id))
            self.assertEqual(["prompt.txt"], [path.name for path in run.iterdir()])

        with self.temporary() as name:
            repo, output, run, run_id = self.capture_fixture(Path(name))
            real_rename, calls = os.rename, 0

            def fail_second(source, destination):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected publication failure")
                return real_rename(source, destination)

            with mock.patch.object(capture.os, "rename", side_effect=fail_second):
                with self.assertRaisesRegex(OSError, "injected publication failure"):
                    capture.main(self.capture_args(repo, output, run_id))
            self.assertEqual(b"actual prompt\n", (run / "prompt.txt").read_bytes())
            self.assertEqual(["prompt.txt"], [path.name for path in run.iterdir()])
            self.assertFalse(list(run.parent.glob(".capture-*")))

        with self.temporary() as name:
            repo, output, run, run_id = self.capture_fixture(Path(name))
            with redirect_stdout(io.StringIO()):
                self.assertEqual(0, capture.main(self.capture_args(repo, output, run_id)))
            self.assertEqual("actual prompt\n", (run / "prompt.txt").read_text())
            self.assertEqual("actual output\n", (run / "artifacts" / "output.md").read_text())
            self.assertEqual(run_id, json.loads((run / "run.json").read_text())["run_id"])

    def test_assemble_atomic_failure_and_symlink_target_preserve_original(self):
        with self.temporary() as name:
            repo, index = self.assemble_fixture(Path(name))
            with mock.patch.object(safe_filesystem.os, "replace", side_effect=OSError("injected")):
                with self.assertRaisesRegex(OSError, "injected"):
                    assemble.main(["--repo-root", str(repo), "--write"])
            self.assertEqual("original index\n", index.read_text())
            self.assertFalse(list(index.parent.glob(".*.tmp")))

        with self.temporary() as name:
            repo, index = self.assemble_fixture(Path(name))
            outside = Path(name) / "outside-index"
            outside.write_text("outside\n")
            index.unlink()
            index.symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "Symlink not permitted"):
                assemble.main(["--repo-root", str(repo), "--write"])
            self.assertEqual("outside\n", outside.read_text())

        with self.temporary() as name:
            repo, index = self.assemble_fixture(Path(name))
            (index.parent / "runs" / "P1-U01-V01-R99" / "run.json").write_text("not json")
            with self.assertRaisesRegex(ValueError, "Invalid JSON"):
                assemble.main(["--repo-root", str(repo), "--write"])
            self.assertEqual("original index\n", index.read_text())

    def test_run_results_group_rollback_and_dangling_parent(self):
        payload = {
            "status": "fail", "case_count": 0, "expected_case_count": 104,
            "behavioral": {"selected": 0}, "checks": {}, "errors": [],
            "package_validator": None,
        }
        with self.temporary() as name:
            repo, tests = Path(name) / "repo", Path(name) / "repo" / "tests"
            tests.mkdir(parents=True)
            first, second = tests / "deterministic-results.json", tests / "acceptance-report.md"
            first.write_text("old json\n")
            second.write_text("old report\n")
            real_replace, calls = os.replace, 0

            def fail_second(source, destination):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected second replace failure")
                return real_replace(source, destination)

            with mock.patch.object(safe_filesystem.os, "replace", side_effect=fail_second):
                with self.assertRaisesRegex(OSError, "second replace"):
                    run_tests.write_results(repo, payload)
            self.assertEqual("old json\n", first.read_text())
            self.assertEqual("old report\n", second.read_text())
            self.assertFalse(list(tests.glob(".*.tmp")))

        with self.temporary() as name:
            repo = Path(name) / "repo"
            repo.mkdir()
            (repo / "tests").symlink_to(Path(name) / "missing", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "Symlink not permitted"):
                run_tests.write_results(repo, payload)

            outside = Path(name) / "outside"
            with self.assertRaisesRegex(ValueError, "escapes"):
                safe_filesystem.atomic_write(outside, b"unsafe", repo, "test destination")
            self.assertFalse(outside.exists())

    def test_hygiene_policy_and_findings_are_fail_closed_without_private_text_scan(self):
        with self.temporary() as name:
            repo = Path(name) / "repo"
            (repo / "docs").mkdir(parents=True)
            (repo / "docs" / "current.md").write_text("Frozen example /Users/alice/work\n")
            (repo / "REPOSITORY-HYGIENE.json").write_text(json.dumps(self.policy()))
            report = run_tests.TestReport()
            self.assertTrue(run_tests.validate_repository_hygiene(repo, report), report.errors)

            (repo / ".DS_Store").write_text("")
            (repo / "large.bin").write_bytes(b"x" * 1001)
            release = repo / "dist" / "1.0.0"
            release.mkdir(parents=True)
            (release / "a.bin").write_bytes(b"a" * 8)
            (release / "b.bin").write_bytes(b"b" * 8)
            (repo / "dangling").symlink_to(repo / "missing")
            report = run_tests.TestReport()
            self.assertFalse(run_tests.validate_repository_hygiene(repo, report))
            codes = {item["code"] for item in report.errors}
            self.assertTrue(
                {"hygiene-junk", "hygiene-file-size", "hygiene-symlink",
                 "hygiene-release-size", "hygiene-dist-size"}.issubset(codes),
                report.errors,
            )

        with self.temporary() as name:
            repo = Path(name) / "repo"
            release = repo / "dist" / "1.0.0"
            release.mkdir(parents=True)
            (release / "a.bin").write_bytes(b"a" * 8)
            policy = self.policy()
            policy["limits"]["max_dist_bytes"] = None
            (repo / "REPOSITORY-HYGIENE.json").write_text(json.dumps(policy))
            report = run_tests.TestReport()
            self.assertTrue(run_tests.validate_repository_hygiene(repo, report), report.errors)

        for policy_text in (
            None, "{", '{"junk_names": [], "junk_names": []}',
            json.dumps({key: value for key, value in self.policy().items() if key != "schema_version"}),
            json.dumps(self.policy(schema_version="2.0")),
            json.dumps(self.policy(allowed_private_path_files=["../escape"])),
        ):
            with self.subTest(policy_text=policy_text), self.temporary() as name:
                repo = Path(name) / "repo"
                repo.mkdir()
                if policy_text is not None:
                    (repo / "REPOSITORY-HYGIENE.json").write_text(policy_text)
                report = run_tests.TestReport()
                self.assertFalse(run_tests.validate_repository_hygiene(repo, report))
                self.assertEqual("hygiene-policy", report.errors[0]["code"])

    def test_validator_preflight_never_reads_symlink_targets(self):
        with self.temporary() as name:
            root = Path(name)
            skill, outside = root / "skill", root / "outside"
            skill.mkdir()
            outside.write_text("secret target content\n")
            (skill / "SKILL.md").symlink_to(outside)
            (skill / "nested").symlink_to(root / "missing", target_is_directory=True)
            stream = io.StringIO()
            with mock.patch.object(validator, "read_binary", side_effect=AssertionError("content read")):
                with redirect_stdout(stream):
                    result = validator.main([str(skill), "--json"])
            payload = json.loads(stream.getvalue())
            self.assertEqual(1, result)
            self.assertEqual("fail", payload["status"])
            self.assertEqual("fail", payload["checks"]["no_symlinks"])
            self.assertEqual(["symlink", "symlink"], [item["code"] for item in payload["errors"]])

        with self.temporary() as name:
            regular_file = Path(name) / "not-a-skill"
            regular_file.write_text("not a package\n")
            stream = io.StringIO()
            with redirect_stdout(stream):
                result = validator.main([str(regular_file), "--json"])
            self.assertEqual(1, result)
            self.assertEqual("skill-path", json.loads(stream.getvalue())["errors"][0]["code"])

        with self.temporary() as name:
            root = Path(name)
            real_parent = root / "real"
            skill = real_parent / "skill"
            skill.mkdir(parents=True)
            alias = root / "alias"
            alias.symlink_to(real_parent, target_is_directory=True)
            stream = io.StringIO()
            with mock.patch.object(validator, "read_binary", side_effect=AssertionError("content read")):
                with redirect_stdout(stream):
                    result = validator.main([str(alias / "skill"), "--json"])
            self.assertEqual(1, result)
            self.assertEqual("symlink", json.loads(stream.getvalue())["errors"][0]["code"])


if __name__ == "__main__":
    unittest.main()
