"""Isolated builder unit tests; not skill behavioral or platform acceptance.

All archives and synthetic metadata live in TemporaryDirectory fixtures. Static
validator calls are mocked here; the real builder still requires them to pass.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest import mock


BUILDER_PATH = Path(__file__).resolve().parents[3] / "scripts" / "build_release.py"
SPEC = importlib.util.spec_from_file_location("release_builder_under_test", BUILDER_PATH)
assert SPEC is not None and SPEC.loader is not None
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class ReleaseBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="release-builder-unit-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve() / "repo"
        self.skill = self.root / "skills" / builder.SKILL_ID
        self.skill.mkdir(parents=True)
        self.manifest = self.root / "RELEASE-MANIFEST.yaml"
        self.manifest.write_text(
            'schema_version: "1.0"\nrelease:\n'
            '  skill_version: "1.1.0"\n'
            f'  skill_id: "{builder.SKILL_ID}"\n'
            f'  canonical_source: "skills/{builder.SKILL_ID}"\n', encoding="utf-8")
        files = {name: f"Synthetic {name}\n" for name in builder.REQUIRED_FILES}
        files.update({
            "LICENSE-APPLICATION.md": '- **Covered skill versions:** `1.1.0`.\n',
            "agents/openai.yaml": 'interface:\n  display_name: "Synthetic"\n',
            "references/example.md": "Synthetic process reference.\n",
            "templates/example.yaml": 'schema_version: "1.0.0"\n',
            "integration/master-orchestrator-registry-entry.yaml": 'version: "1.1.0"\n',
            "scripts/validate_package.py": "# Never executed by these unit tests.\n",
            ".DS_Store": "Excluded fixture\n",
            "__pycache__/module.pyc": "Excluded fixture\n",
        })
        for name, content in files.items():
            target = self.skill / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        (self.root / "LICENSE-APPLICATION.md").write_bytes(
            (self.skill / "LICENSE-APPLICATION.md").read_bytes())
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "run_tests.py").write_text("# Synthetic\n", encoding="utf-8")
        patcher = mock.patch.object(builder, "validate_before_build", return_value={
            "package_validation": {"status": "pass"},
            "case_registry": {"status": "pass", "case_count": 104,
                              "behavioral": {"status": "not_run"}},
        })
        self.static = patcher.start()
        self.addCleanup(patcher.stop)
        self.static_patcher = patcher
        staged = mock.patch.object(builder, "validate_staged_package", return_value={"status": "pass"})
        self.staged = staged.start()
        self.addCleanup(staged.stop)

    def artifact_bytes(self) -> dict[str, bytes]:
        return {path.name: path.read_bytes() for path in (self.root / "dist" / "1.1.0").iterdir()}

    def test_version_source_and_metadata_gates(self) -> None:
        self.assertEqual(builder.release_version(self.root, self.skill), "1.1.0")
        original = self.manifest.read_text(encoding="utf-8")
        for invalid in ("../1.1.0", "01.1.0", "1.1", "1.1.0-rc1", "1.1.0/extra"):
            with self.subTest(version=invalid):
                self.manifest.write_text(original.replace("1.1.0", invalid), encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "X.Y.Z"):
                    builder.release_version(self.root, self.skill)
        self.manifest.write_text(original + '  skill_version: "1.1.0"\n', encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Expected one"):
            builder.release_version(self.root, self.skill)
        self.manifest.write_text(original, encoding="utf-8")
        registry = self.skill / "integration" / "master-orchestrator-registry-entry.yaml"
        registry.write_text('version: "1.0.0"\n', encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Registry version"):
            builder.release_version(self.root, self.skill)

    def test_license_application_parity_and_coverage(self) -> None:
        application = self.root / "LICENSE-APPLICATION.md"
        application.write_text("different\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "differ"):
            builder.release_version(self.root, self.skill)
        application.write_text('- **Covered skill versions:** `1.0.0`.\n', encoding="utf-8")
        (self.skill / application.name).write_bytes(application.read_bytes())
        with self.assertRaisesRegex(RuntimeError, "does not cover"):
            builder.release_version(self.root, self.skill)

    def test_three_wrappers_and_per_file_parity(self) -> None:
        report = builder.build_packages(self.root)
        self.assertEqual(report["publication"], "created")
        self.assertEqual(len(self.artifact_bytes()), 5)
        self.assertEqual(self.staged.call_count, 3)
        canonical = report["canonical_file_sha256"]
        self.assertNotIn(".DS_Store", canonical)
        self.assertNotIn("__pycache__/module.pyc", canonical)
        for target, package in report["packages"].items():
            prefix = f"{builder.SKILL_ID}/"
            if target == "universal":
                prefix = ".agents/skills/" + prefix
            self.assertEqual(package["archive_root"], prefix)
            with zipfile.ZipFile(self.root / report["artifact_directory"] / package["file"]) as archive:
                actual = {name[len(prefix):]: hashlib.sha256(archive.read(name)).hexdigest()
                          for name in archive.namelist()}
                self.assertTrue(all(name.startswith(prefix) for name in archive.namelist()))
                self.assertEqual(actual, package["normalized_file_sha256"])
            expected = {name: digest for name, digest in canonical.items()
                        if target != "claude" or not name.startswith("agents/")}
            self.assertEqual(actual, expected)
        self.assertEqual(report["reproducibility"]["builds_compared"], 2)
        checksum_lines = self.artifact_bytes()["SHA256SUMS"].decode().splitlines()
        self.assertEqual(len(checksum_lines), 3)
        for line in checksum_lines:
            digest, filename = line.split("  ")
            self.assertEqual(digest, hashlib.sha256(self.artifact_bytes()[filename]).hexdigest())

    def test_idempotent_and_historical_artifacts_untouched(self) -> None:
        dist = self.root / "dist"
        dist.mkdir()
        historical = {dist / "old-v1.0.0.zip": b"old ZIP", dist / "SHA256SUMS": b"old checksums"}
        (self.root / "tests").mkdir()
        historical[self.root / "tests" / "deterministic-results.json"] = b"old registry result"
        historical[self.root / "tests" / "acceptance-report.md"] = b"old test summary"
        for path, content in historical.items():
            path.write_bytes(content)
        builder.build_packages(self.root)
        first = self.artifact_bytes()
        for path in self.skill.rglob("*"):
            if path.is_file():
                os.utime(path, (946684800, 946684800))
        self.static.return_value["case_registry"]["generated_at"] = "different unpersisted timestamp"
        report = builder.build_packages(self.root)
        self.assertEqual(report["publication"], "unchanged")
        self.assertEqual(first, self.artifact_bytes())
        self.assertEqual(historical, {path: path.read_bytes() for path in historical})

    def test_existing_release_mismatch_never_overwritten(self) -> None:
        builder.build_packages(self.root)
        before = self.artifact_bytes()
        (self.skill / "references" / "example.md").write_text("Changed content\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Refusing to overwrite"):
            builder.build_packages(self.root)
        self.assertEqual(before, self.artifact_bytes())

    def test_partial_version_directory_is_not_completed_or_replaced(self) -> None:
        destination = self.root / "dist" / "1.1.0"
        destination.mkdir(parents=True)
        (destination / "SHA256SUMS").write_bytes(b"partial release")
        with self.assertRaisesRegex(RuntimeError, "different artifacts"):
            builder.build_packages(self.root)
        self.assertEqual(self.artifact_bytes(), {"SHA256SUMS": b"partial release"})

    def test_symbolic_links_rejected_at_source_and_destination(self) -> None:
        link = self.skill / "reference-link.md"
        link.symlink_to(self.skill / "references" / "example.md")
        with self.assertRaisesRegex(RuntimeError, "symbolic link"):
            builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())
        link.unlink()
        external = self.root.parent / "external"
        external.mkdir()
        (self.root / "dist").symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, "symbolic link"):
            builder.build_packages(self.root)
        self.assertEqual(list(external.iterdir()), [])

    def test_existing_artifact_symlink_is_rejected(self) -> None:
        builder.build_packages(self.root)
        destination = self.root / "dist" / "1.1.0" / "SHA256SUMS"
        outside = self.root.parent / "outside-checksums"
        outside.write_bytes(destination.read_bytes())
        destination.unlink()
        destination.symlink_to(outside)
        before = outside.read_bytes()
        with self.assertRaisesRegex(RuntimeError, "Refusing to overwrite"):
            builder.build_packages(self.root)
        self.assertEqual(outside.read_bytes(), before)
        self.assertTrue(destination.is_symlink())

    def test_path_safety_and_case_collision(self) -> None:
        for name in ("../escape", "/absolute", "a//b", "a/./b", "a/../b", "a\\b",
                     "C:/escape", "a\x00b", "a\nb", "a./b", "a/ "):
            with self.subTest(name=name), self.assertRaisesRegex(RuntimeError, "Unsafe"):
                builder.safe_relative_name(name)
        self.assertEqual(builder.safe_relative_name("references/example.md"), "references/example.md")
        bad = self.skill / "unsafe\\name.md"
        bad.write_bytes(b"unsafe fixture")
        with self.assertRaisesRegex(RuntimeError, "Unsafe"):
            builder.snapshot_canonical(self.skill)
        bad.unlink()
        # Case-insensitive filesystems may not allow both paths to exist; test the
        # collision key without depending on the host filesystem's case policy.
        self.assertEqual(builder.safe_relative_name("A/e\u0301.md"),
                         builder.safe_relative_name("a/\u00e9.md"))

    def test_archive_metadata_and_duplicate_names_are_rejected(self) -> None:
        path = self.root / "bad.zip"
        prefix = f"{builder.SKILL_ID}/"
        info = zipfile.ZipInfo(prefix + "SKILL.md", builder.FIXED_ZIP_TIME)
        info.create_system = 3
        info.external_attr = 0o120777 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(info, "linked-file")
        with self.assertRaisesRegex(RuntimeError, "ZIP metadata"):
            builder.inspect_archive(path, prefix, "excluded", {})
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(info, "first")
                archive.writestr(info, "second")
        with self.assertRaisesRegex(RuntimeError, "sorted and unique"):
            builder.inspect_archive(path, prefix, "excluded", {})
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(prefix + "../escape", "outside")
        with self.assertRaisesRegex(RuntimeError, "Unsafe"):
            builder.inspect_archive(path, prefix, "excluded", {})

    def test_archive_parity_and_agents_rules_are_enforced(self) -> None:
        report = builder.build_packages(self.root)
        package = report["packages"]["chatgpt"]
        path = self.root / report["artifact_directory"] / package["file"]
        expected = dict(package["normalized_file_sha256"])
        expected["SKILL.md"] = "0" * 64
        with self.assertRaisesRegex(RuntimeError, "Normalized file parity"):
            builder.inspect_archive(path, package["archive_root"], "required", expected)
        with self.assertRaisesRegex(RuntimeError, "must exclude agents"):
            builder.inspect_archive(path, package["archive_root"], "excluded", expected)
        package = report["packages"]["claude"]
        path = self.root / report["artifact_directory"] / package["file"]
        with self.assertRaisesRegex(RuntimeError, "must include agents/openai.yaml"):
            builder.inspect_archive(path, package["archive_root"], "required", {})

    def test_reproducibility_failure_prevents_publication(self) -> None:
        original = builder.zip_tree
        calls = []

        def changed_digest(*args):
            result = original(*args)
            calls.append(result)
            if len(calls) == 2:
                result["sha256"] = "0" * 64
            return result

        with mock.patch.object(builder, "zip_tree", side_effect=changed_digest):
            with self.assertRaisesRegex(RuntimeError, "Reproducibility check failed"):
                builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_source_drift_prevents_publication(self) -> None:
        def mutate_source(*args):
            (self.skill / "references" / "example.md").write_bytes(b"Changed during validation")
            return {"status": "pass"}

        self.staged.side_effect = mutate_source
        with self.assertRaisesRegex(RuntimeError, "changed during the build"):
            builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_structural_failure_prevents_publication(self) -> None:
        self.static.side_effect = RuntimeError("synthetic static failure")
        with self.assertRaisesRegex(RuntimeError, "static failure"):
            builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_report_does_not_promote_behavioral_status(self) -> None:
        self.static.return_value["case_registry"]["behavioral"]["status"] = "pass"
        report = builder.build_packages(self.root)
        persisted = json.loads(self.artifact_bytes()["packaging-report.json"])
        self.assertEqual(report["behavioral"]["status"], "not_evaluated_by_builder")
        self.assertFalse(report["behavioral"]["evidence_verified"])
        self.assertEqual(report["release_acceptance"], "not_determined_by_builder")
        self.assertEqual(persisted["behavioral"], report["behavioral"])
        self.assertNotIn("publication", persisted)

    def test_static_runner_is_never_given_write_results(self) -> None:
        self.static_patcher.stop()
        with mock.patch.object(builder, "run_check", return_value={"status": "pass"}) as checks:
            builder.validate_before_build(self.root, self.skill)
        self.assertEqual(checks.call_count, 2)
        commands = [call.args[0] for call in checks.call_args_list]
        self.assertTrue(any(str(self.root / "scripts" / "run_tests.py") in command
                            for command in commands))
        self.assertTrue(all("--write-results" not in command for command in commands))

    def test_run_check_requires_passing_json_object(self) -> None:
        for stdout in ("[]", "not json", '{"status":"fail"}'):
            completed = subprocess.CompletedProcess(["synthetic"], 0, stdout, "")
            with self.subTest(stdout=stdout):
                with mock.patch.object(builder.subprocess, "run", return_value=completed):
                    with self.assertRaises(RuntimeError):
                        builder.run_check(["synthetic"], "synthetic gate")

    def test_cli_without_write_does_not_build(self) -> None:
        with mock.patch.object(builder, "build_packages") as build:
            with contextlib.redirect_stderr(io.StringIO()):
                result = builder.main(["--repo-root", str(self.root), "--json"])
        self.assertEqual(result, 2)
        build.assert_not_called()
        self.assertFalse((self.root / "dist").exists())


if __name__ == "__main__":
    unittest.main()
