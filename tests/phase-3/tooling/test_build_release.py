"""Isolated builder unit tests; not skill behavioral or platform acceptance.

All archives and synthetic metadata live in TemporaryDirectory fixtures. Static
validator calls are mocked here; the real builder still requires them to pass.
"""

from __future__ import annotations

import contextlib
import copy
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
REAL_VALIDATE_STAGED_PACKAGE = builder.validate_staged_package


class ReleaseBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="release-builder-unit-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve() / "repo"
        self.skill = self.root / "skills" / builder.SKILL_ID
        self.skill.mkdir(parents=True)
        self.manifest = self.root / "RELEASE-MANIFEST.yaml"
        files = {name: f"Synthetic {name}\n" for name in builder.REQUIRED_FILES}
        files.update({
            "LICENSE-APPLICATION.md": (
                '- **Covered skill versions:** `1.1.1`.\n'
                '- **Current release covered version:** `1.2.0`.\n'
            ),
            "agents/openai.yaml": 'interface:\n  display_name: "Synthetic"\n',
            "references/example.md": "Synthetic process reference.\n",
            "templates/example.yaml": 'schema_version: "1.0.0"\n',
            "integration/master-orchestrator-registry-entry.yaml": 'version: "1.2.0"\n',
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
        self.write_hygiene_policy()
        self.qualification_path = self.root / "tests" / "release-1.2.0" / "qualification-report.json"
        self.behavior_output = self.qualification_path.parent / "behavior-output.md"
        self.behavior_output.parent.mkdir(parents=True)
        self.behavior_output.write_text("Independent synthetic behavioral output.\n", encoding="utf-8")
        qualification_hash = self.write_qualification_report()
        self.qualification_hash = qualification_hash
        self.package_hashes = self.synthetic_package_hashes()
        self.manifest_text = self.synthetic_manifest(self.package_hashes, qualification_hash)
        self.manifest.write_text(self.manifest_text, encoding="utf-8")
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

    def write_hygiene_policy(self, **limit_overrides: int | None) -> None:
        limits = {
            "max_file_bytes": 4 * 1024 * 1024,
            "max_release_directory_bytes": 10 * 1024 * 1024,
            "max_dist_bytes": 40 * 1024 * 1024,
        }
        limits.update(limit_overrides)
        policy = {
            "schema_version": "1.0",
            "junk_names": [".DS_Store", "__pycache__"],
            "junk_suffixes": [".pyc", ".pyo"],
            "excluded_roots": [".git"],
            "private_path_patterns": ["/Users/", "C:\\Users\\"],
            "allowed_private_path_files": [],
            "limits": limits,
        }
        (self.root / "REPOSITORY-HYGIENE.json").write_text(
            json.dumps(policy, sort_keys=True) + "\n", encoding="utf-8"
        )

    def qualification_payload(self) -> dict[str, object]:
        source = self.skill / "SKILL.md"
        return {
            "schema_version": "1.0",
            "release_version": "1.2.0",
            "status": "pass",
            "source_bindings": [{
                "path": source.relative_to(self.root).as_posix(),
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            }],
            "behavioral_evaluations": [{
                "id": "QA-1.2.0-01",
                "output_path": self.behavior_output.relative_to(self.root).as_posix(),
                "output_sha256": hashlib.sha256(self.behavior_output.read_bytes()).hexdigest(),
                "status": "pass",
                "independent_executor": True,
                "independent_reviewer": True,
            }],
            "deterministic_gates": {
                "canonical_validator": "pass",
                "tooling_unit_tests": "pass",
            },
            "untested_surfaces": ["Claude and ChatGPT native installation"],
            "limitations": ["Synthetic fixture; the builder does not re-grade semantics."],
            "publication_authority": "owner_authorized",
        }

    def write_qualification_report(self, payload: dict[str, object] | None = None) -> str:
        payload = self.qualification_payload() if payload is None else payload
        self.qualification_path.parent.mkdir(parents=True, exist_ok=True)
        self.qualification_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return hashlib.sha256(self.qualification_path.read_bytes()).hexdigest()

    def bind_qualification_payload(self, payload: dict[str, object]) -> None:
        digest = self.write_qualification_report(payload)
        self.manifest.write_text(
            self.manifest_text.replace(self.qualification_hash, digest, 1),
            encoding="utf-8",
        )

    def bind_qualification_bytes(self, data: bytes) -> None:
        self.qualification_path.write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        self.manifest.write_text(
            self.manifest_text.replace(self.qualification_hash, digest, 1),
            encoding="utf-8",
        )

    def synthetic_package_hashes(self) -> dict[str, str]:
        snapshot = builder.snapshot_canonical(self.skill)
        hashes: dict[str, str] = {}
        with tempfile.TemporaryDirectory(prefix="release-builder-hash-fixture-") as temporary:
            staging = Path(temporary)
            for target in builder.PACKAGE_LABELS:
                include_agents = target != "claude"
                prefix = (f".agents/skills/{builder.SKILL_ID}/" if target == "universal"
                          else f"{builder.SKILL_ID}/")
                package_root = staging / f"root-{target}"
                builder.stage_snapshot(snapshot, package_root / prefix.rstrip("/"), include_agents)
                result = builder.zip_tree(package_root, staging / f"{target}.zip")
                hashes[target] = result["sha256"]
        return hashes

    @staticmethod
    def synthetic_manifest(hashes: dict[str, str], qualification_hash: str) -> str:
        targets = (("claude", "claude"), ("chatgpt", "chatgpt"),
                   ("universal-agents", "universal"))
        lines = [
            'schema_version: "1.0"',
            "release:",
            f'  display_name: "{builder.DISPLAY_NAME}"',
            f'  skill_id: "{builder.SKILL_ID}"',
            '  skill_version: "1.2.0"',
            '  application_date: "2026-09-01"',
            '  status: "release_candidate"',
            '  artifact_directory: "dist/1.2.0"',
            "  source_repository:",
            '    visibility: "public"',
            f'    url: "{builder.CANONICAL_REPOSITORY_URL}"',
            "  license:",
            f'    id: "{builder.CANONICAL_LICENSE["id"]}"',
            '    controlling_file: "LICENSE"',
            '    application_file: "LICENSE-APPLICATION.md"',
            "    vietnamese_version_prevails: true",
            f'  canonical_source: "skills/{builder.SKILL_ID}"',
            "  packages:",
        ]
        for manifest_target, target in targets:
            root = (f".agents/skills/{builder.SKILL_ID}/" if target == "universal"
                    else f"{builder.SKILL_ID}/")
            lines.extend([
                f'    - target: "{manifest_target}"',
                f'      filename: "{builder.PACKAGE_BASENAME}-v1.2.0-'
                f'{builder.PACKAGE_LABELS[target]}.zip"',
                f'      archive_root: "{root}"',
                f'      sha256: "{hashes[target]}"',
            ])
        lines.extend([
            "  verification:",
            '    structural: "pass"',
            '    deterministic_case_registry: "pass"',
            '    behavioral_codex: "pass"',
            '    behavioral_claude: "not_run"',
            '    behavioral_chatgpt: "not_run"',
            '    archive_integrity: "pass"',
            '    native_installation_and_discovery: "not_run"',
            "    fresh_context_behavioral_scenarios_reviewed_pass: 1",
            "    historical_model_variants_reviewed_pass_1_1_0: 29",
            "    tooling_tests_pass: 91",
            "    rename_regression_tests_pass: 6",
            '    qualification_report: "tests/release-1.2.0/qualification-report.json"',
            f'    qualification_report_sha256: "{qualification_hash}"',
            '    evidence_report: "docs/HANDOFF.md"',
            '    historical_report: "docs/phase-3/REPORT.md"',
            '    historical_release_gate_source: "tests/phase-3/acceptance-results.json#current_release_gate"',
            '    scope: "Current 1.2.0 qualification with historical evidence kept separate"',
            "  publication:",
            '    local_artifacts: "not_created"',
            '    github_commit_push: "not_performed"',
            '    git_tag: "not_performed"',
            '    github_release: "not_performed"',
            '    installed_skills: "not_modified"',
        ])
        return "\n".join(lines) + "\n"

    def artifact_bytes(self) -> dict[str, bytes]:
        return {path.name: path.read_bytes() for path in (self.root / "dist" / "1.2.0").iterdir()}

    def test_version_source_and_metadata_gates(self) -> None:
        self.assertEqual(builder.release_version(self.root, self.skill), "1.2.0")
        original = self.manifest.read_text(encoding="utf-8")
        for invalid in ("../1.2.0", "01.2.0", "1.2", "1.2.0-rc1", "1.2.0/extra"):
            with self.subTest(version=invalid):
                self.manifest.write_text(original.replace("1.2.0", invalid), encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "X.Y.Z"):
                    builder.release_version(self.root, self.skill)
        self.manifest.write_text(original + '  skill_version: "1.2.0"\n', encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Duplicate manifest field"):
            builder.release_version(self.root, self.skill)
        self.manifest.write_text(original, encoding="utf-8")
        registry = self.skill / "integration" / "master-orchestrator-registry-entry.yaml"
        registry.write_text('version: "1.0.0"\n', encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Registry version"):
            builder.release_version(self.root, self.skill)

    def test_current_repository_manifest_is_compatible(self) -> None:
        repository = BUILDER_PATH.parent.parent
        declarations = builder.release_declarations(
            repository,
            repository / "skills" / builder.SKILL_ID,
            allow_pending_hashes=True,
        )
        self.assertEqual(declarations["version"], "1.2.1")
        self.assertEqual(declarations["display_name"], builder.DISPLAY_NAME)
        self.assertEqual(set(declarations["packages"]), set(builder.PACKAGE_LABELS))

    def test_manifest_package_declarations_are_strict(self) -> None:
        original = self.manifest_text
        claude_root = f'      archive_root: "{builder.SKILL_ID}/"\n'
        claude_filename = (
            f'      filename: "{builder.PACKAGE_BASENAME}-v1.2.0-Claude.zip"\n'
        )
        claude_hash = f'      sha256: "{self.package_hashes["claude"]}"\n'
        universal_block = (
            '    - target: "universal-agents"\n'
            f'      filename: "{builder.PACKAGE_BASENAME}-v1.2.0-Universal.zip"\n'
            f'      archive_root: ".agents/skills/{builder.SKILL_ID}/"\n'
            f'      sha256: "{self.package_hashes["universal"]}"\n'
        )
        mutations = {
            "missing field": (
                original.replace(claude_root, "", 1), "Missing package manifest field"
            ),
            "duplicate field": (
                original.replace(claude_filename, claude_filename + claude_filename, 1),
                "Duplicate manifest field",
            ),
            "unknown package field": (
                original.replace(claude_hash, claude_hash + '      digest: "unsupported"\n', 1),
                "Unknown package manifest field",
            ),
            "unknown release field": (
                original.replace("  packages:\n", '  undeclared: "value"\n  packages:\n', 1),
                "Unknown release manifest field",
            ),
            "missing known release field": (
                original.replace('  status: "release_candidate"\n', "", 1),
                "Missing release manifest field",
            ),
            "empty known release field": (
                original.replace('  status: "release_candidate"', '  status: ""', 1),
                "release.status must not be empty",
            ),
            "wrong known release field shape": (
                original.replace(
                    '  source_repository:\n'
                    '    visibility: "public"\n'
                    f'    url: "{builder.CANONICAL_REPOSITORY_URL}"\n',
                    '  source_repository: "private"\n',
                    1,
                ),
                "release.source_repository must be a dict",
            ),
            "missing nested source field": (
                original.replace(
                    f'    url: "{builder.CANONICAL_REPOSITORY_URL}"\n', "", 1
                ),
                "Missing release.source_repository field",
            ),
            "unknown nested license field": (
                original.replace(
                    '    application_file: "LICENSE-APPLICATION.md"\n',
                    '    application_file: "LICENSE-APPLICATION.md"\n'
                    '    unsupported: "value"\n',
                    1,
                ),
                "Unknown release.license field",
            ),
            "wrong nested license type": (
                original.replace(
                    "    vietnamese_version_prevails: true",
                    '    vietnamese_version_prevails: "true"',
                    1,
                ),
                "release.license.vietnamese_version_prevails must be a bool",
            ),
            "missing nested verification field": (
                original.replace('    behavioral_chatgpt: "not_run"\n', "", 1),
                "Missing release.verification field",
            ),
            "unknown nested publication field": (
                original.replace(
                    '    installed_skills: "not_modified"\n',
                    '    installed_skills: "not_modified"\n'
                    '    unsupported: "value"\n',
                    1,
                ),
                "Unknown release.publication field",
            ),
            "wrong qualification count type": (
                original.replace(
                    "    fresh_context_behavioral_scenarios_reviewed_pass: 1",
                    "    fresh_context_behavioral_scenarios_reviewed_pass: true",
                    1,
                ),
                "fresh_context_behavioral_scenarios_reviewed_pass must be a int",
            ),
            "unknown target": (
                original.replace('    - target: "claude"', '    - target: "desktop"', 1),
                "Unknown release package target",
            ),
            "duplicate target": (
                original.replace('    - target: "universal-agents"',
                                 '    - target: "chatgpt"', 1),
                "Duplicate release package target",
            ),
            "missing target": (
                original.replace(universal_block, "", 1),
                "Missing release package targets",
            ),
            "invalid hash": (
                original.replace(self.package_hashes["claude"], "not-a-sha256", 1),
                "Package sha256 is invalid",
            ),
            "wrong root": (
                original.replace(claude_root, '      archive_root: "wrong-root/"\n', 1),
                "Package archive_root does not match",
            ),
            "wrong filename": (
                original.replace(claude_filename, '      filename: "stale.zip"\n', 1),
                "Package filename does not match",
            ),
            "wrong display name": (
                original.replace(builder.DISPLAY_NAME, "Stale-Display-Name", 1),
                "release.display_name does not match",
            ),
            "wrong artifact directory": (
                original.replace('  artifact_directory: "dist/1.2.0"',
                                 '  artifact_directory: "dist/old"', 1),
                "release.artifact_directory does not match",
            ),
        }
        for label, (content, error) in mutations.items():
            with self.subTest(label=label):
                self.manifest.write_text(content, encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, error):
                    builder.release_declarations(self.root, self.skill)
        self.manifest.write_text(original, encoding="utf-8")

    def test_stale_manifest_hash_prevents_publication(self) -> None:
        self.manifest.write_text(
            self.manifest_text.replace(self.package_hashes["claude"], "0" * 64, 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "sha256 differs"):
            builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_prepare_with_pending_hashes_is_temporary_and_copy_ready(self) -> None:
        pending = self.manifest_text
        for digest in self.package_hashes.values():
            pending = pending.replace(digest, "pending", 1)
        self.manifest.write_text(pending, encoding="utf-8")
        before_files = {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for path in self.root.rglob("*") if path.is_file()
        }
        before_dirs = {
            path.relative_to(self.root).as_posix()
            for path in self.root.rglob("*") if path.is_dir()
        }

        with mock.patch.object(builder, "publish_artifacts") as publish:
            result = builder.prepare_packages(self.root)
        publish.assert_not_called()

        after_files = {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for path in self.root.rglob("*") if path.is_file()
        }
        after_dirs = {
            path.relative_to(self.root).as_posix()
            for path in self.root.rglob("*") if path.is_dir()
        }
        self.assertEqual(after_files, before_files)
        self.assertEqual(after_dirs, before_dirs)
        self.assertFalse((self.root / "dist").exists())
        self.assertEqual(result["mode"], "prepare")
        self.assertEqual(result["publication"], "not_performed_prepare_only")
        self.assertFalse(result["repository_writes"])
        self.assertEqual(
            result["validation"]["release_manifest_package_binding"],
            "pending_hashes_computed",
        )
        generated = {
            builder.MANIFEST_TARGETS[item["target"]]: item["sha256"]
            for item in result["computed_release_declarations"]["packages"]
        }
        self.assertEqual(generated, self.package_hashes)

    def test_pending_hashes_are_refused_in_publish_mode(self) -> None:
        self.manifest.write_text(
            self.manifest_text.replace(self.package_hashes["claude"], "pending", 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "allowed only in --prepare mode"):
            builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_prepare_does_not_bypass_stale_final_hash(self) -> None:
        self.manifest.write_text(
            self.manifest_text.replace(self.package_hashes["claude"], "0" * 64, 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "sha256 differs"):
            builder.prepare_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_license_application_parity_and_coverage(self) -> None:
        application = self.root / "LICENSE-APPLICATION.md"
        application.write_text("different\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "differ"):
            builder.release_version(self.root, self.skill)
        application.write_text(
            '- **Covered skill versions:** `1.1.1`.\n'
            '- **Current release covered version:** `1.1.1`.\n',
            encoding="utf-8",
        )
        (self.skill / application.name).write_bytes(application.read_bytes())
        with self.assertRaisesRegex(RuntimeError, "Current release covered version"):
            builder.release_version(self.root, self.skill)

    def test_license_application_coverage_preserves_history_and_binds_current(self) -> None:
        historical = '- **Covered skill versions:** `1.1.1`.\n'
        current = '- **Current release covered version:** `1.2.0`.\n'
        builder.validate_license_application_coverage(historical + current, "1.2.0")
        builder.validate_license_application_coverage(
            historical + current + '- **Current release covered version:** `1.2.1`.\n',
            "1.2.1",
        )
        builder.validate_license_application_coverage(historical, "1.1.1")
        builder.validate_license_application_coverage(
            historical + '- **Current release covered version:** `1.1.1`.\n',
            "1.1.1",
        )

        invalid_cases = (
            (current, "1.2.0", "historical"),
            ('- **Covered skill versions:** `1.2.0`.\n' + current,
             "1.2.0", "historical"),
            (historical + historical + current, "1.2.0", "historical"),
            (historical, "1.2.0", "Current release covered version"),
            (historical + '- **Current release covered version:** `1.1.1`.\n',
             "1.2.0", "Current release covered version"),
            (historical + current + current,
             "1.2.0", "Current release covered version"),
            (historical + current + '- **Current release covered version:** 1.2.0\n',
             "1.2.0", "Current release covered version"),
            (historical + current, "1.1.1", "conflicts"),
        )
        for text, version, error in invalid_cases:
            with self.subTest(version=version, error=error):
                with self.assertRaisesRegex(RuntimeError, error):
                    builder.validate_license_application_coverage(text, version)

    def test_qualification_report_binds_current_sources_and_behavior(self) -> None:
        declarations = builder.release_declarations(self.root, self.skill)
        qualification = declarations["qualification"]
        self.assertEqual(qualification["status"], "pass")
        self.assertEqual(qualification["qualification_kind"], "full_behavioral")
        self.assertEqual(qualification["behavioral_evaluations_reviewed_pass"], 1)
        self.assertEqual(qualification["source_binding_count"], 1)
        self.assertEqual(qualification["publication_authority"], "owner_authorized")

    def test_metadata_only_patch_preserves_prior_behavioral_attribution(self) -> None:
        inherited_path = self.qualification_path
        inherited_hash = hashlib.sha256(inherited_path.read_bytes()).hexdigest()
        self.qualification_path = (
            self.root / "tests" / "release-1.2.1" / "qualification-report.json"
        )
        source = self.skill / "SKILL.md"
        payload: dict[str, object] = {
            "schema_version": "1.1",
            "release_version": "1.2.1",
            "status": "pass",
            "qualification_kind": "metadata_only_patch",
            "source_bindings": [{
                "path": source.relative_to(self.root).as_posix(),
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            }],
            "behavioral_evaluations": [],
            "inherited_behavioral_evidence": {
                "source_release": "1.2.0",
                "qualification_report": inherited_path.relative_to(self.root).as_posix(),
                "qualification_report_sha256": inherited_hash,
                "relationship": "inherited_not_reexecuted_or_relabelled",
            },
            "deterministic_gates": {"metadata_parity": "pass"},
            "untested_surfaces": ["No new behavioral model run for 1.2.1"],
            "limitations": ["Prior evidence remains attributed to release 1.2.0."],
            "publication_authority": "owner_authorized",
        }
        digest = self.write_qualification_report(payload)
        manifest_121 = self.manifest_text.replace("1.2.0", "1.2.1")
        manifest_121 = manifest_121.replace(self.qualification_hash, digest, 1)
        manifest_121 = manifest_121.replace(
            "fresh_context_behavioral_scenarios_reviewed_pass: 1",
            "fresh_context_behavioral_scenarios_reviewed_pass: 0",
            1,
        )
        self.manifest.write_text(manifest_121, encoding="utf-8")
        registry = self.skill / "integration" / "master-orchestrator-registry-entry.yaml"
        registry.write_text('version: "1.2.1"\n', encoding="utf-8")
        application = self.root / "LICENSE-APPLICATION.md"
        application.write_text(
            '- **Covered skill versions:** `1.1.1`.\n'
            '- **Current release covered version:** `1.2.0`.\n'
            '- **Current release covered version:** `1.2.1`.\n',
            encoding="utf-8",
        )
        (self.skill / application.name).write_bytes(application.read_bytes())

        declarations = builder.release_declarations(self.root, self.skill)
        qualification = declarations["qualification"]
        self.assertEqual(qualification["qualification_kind"], "metadata_only_patch")
        self.assertEqual(qualification["behavioral_evaluations_reviewed_pass"], 0)
        self.assertEqual(
            qualification["inherited_behavioral_evidence"]["source_release"], "1.2.0"
        )
        self.assertEqual(
            qualification["inherited_behavioral_evidence"][
                "behavioral_evaluations_in_source_report"
            ],
            1,
        )

        payload["inherited_behavioral_evidence"]["relationship"] = "relabelled"  # type: ignore[index]
        digest = self.write_qualification_report(payload)
        self.manifest.write_text(
            manifest_121.replace(
                declarations["qualification"]["sha256"], digest, 1
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "inherited_not_reexecuted_or_relabelled"):
            builder.release_declarations(self.root, self.skill)

    def test_qualification_report_contract_rejections(self) -> None:
        mutations: list[tuple[str, dict[str, object], str]] = []
        for label, mutate, error in (
            ("version", lambda item: item.update(release_version="1.1.1"), "release_version"),
            ("status", lambda item: item.update(status="fail"), "status must be 'pass'"),
            ("authority", lambda item: item.update(publication_authority="not_authorized"),
             "publication_authority"),
            ("source empty", lambda item: item.update(source_bindings=[]), "source_bindings"),
            ("behavior empty", lambda item: item.update(behavioral_evaluations=[]),
             "behavioral_evaluations"),
            ("gate fail", lambda item: item.update(deterministic_gates={"tooling": "fail"}),
             "deterministic_gates"),
            ("untested empty", lambda item: item.update(untested_surfaces=[]), "untested_surfaces"),
            ("limitations empty", lambda item: item.update(limitations=[]), "limitations"),
            ("unknown root", lambda item: item.update(unsupported="value"), "contain exactly"),
        ):
            payload = copy.deepcopy(self.qualification_payload())
            mutate(payload)
            mutations.append((label, payload, error))

        payload = copy.deepcopy(self.qualification_payload())
        payload["source_bindings"][0]["sha256"] = "0" * 64  # type: ignore[index]
        mutations.append(("source hash", payload, r"source_bindings\[0\].*SHA-256"))
        payload = copy.deepcopy(self.qualification_payload())
        payload["behavioral_evaluations"][0]["output_sha256"] = "0" * 64  # type: ignore[index]
        mutations.append(("output hash", payload, "output bytes.*SHA-256"))
        payload = copy.deepcopy(self.qualification_payload())
        payload["behavioral_evaluations"][0]["independent_executor"] = False  # type: ignore[index]
        mutations.append(("executor independence", payload, "independent_executor must be true"))
        payload = copy.deepcopy(self.qualification_payload())
        payload["behavioral_evaluations"][0]["independent_reviewer"] = False  # type: ignore[index]
        mutations.append(("reviewer independence", payload, "independent_reviewer must be true"))
        payload = copy.deepcopy(self.qualification_payload())
        payload["behavioral_evaluations"].append(  # type: ignore[union-attr]
            {**payload["behavioral_evaluations"][0], "id": "QA-1.2.0-02",  # type: ignore[index]
             "output_path": "tests/release-1.2.0/second-output.md"}
        )
        second = self.qualification_path.parent / "second-output.md"
        second.write_bytes(self.behavior_output.read_bytes() + b"Second.\n")
        payload["behavioral_evaluations"][1]["output_sha256"] = hashlib.sha256(  # type: ignore[index]
            second.read_bytes()
        ).hexdigest()
        mutations.append(("count", payload, "count does not match"))

        for label, payload, error in mutations:
            with self.subTest(label=label):
                self.bind_qualification_payload(payload)
                with self.assertRaisesRegex(RuntimeError, error):
                    builder.release_declarations(self.root, self.skill)

    def test_qualification_json_symlink_and_private_paths_are_rejected(self) -> None:
        for raw in (
            b'{"schema_version":"1.0","schema_version":"1.0"}\n',
            b'{"schema_version":"1.0","value":NaN}\n',
        ):
            with self.subTest(raw=raw):
                self.bind_qualification_bytes(raw)
                with self.assertRaisesRegex(RuntimeError, "Invalid strict JSON"):
                    builder.release_declarations(self.root, self.skill)

        payload = self.qualification_payload()
        payload["limitations"] = ["Leaked /Users/alice/project path"]
        self.bind_qualification_payload(payload)
        with self.assertRaisesRegex(RuntimeError, "Private-path pattern"):
            builder.release_declarations(self.root, self.skill)

        self.behavior_output.write_text("Leaked C:\\Users\\alice\\project\n", encoding="utf-8")
        payload = self.qualification_payload()
        self.bind_qualification_payload(payload)
        with self.assertRaisesRegex(RuntimeError, "Private-path pattern"):
            builder.release_declarations(self.root, self.skill)

        self.behavior_output.write_text("Independent synthetic behavioral output.\n", encoding="utf-8")
        outside = self.root.parent / "outside-source.md"
        outside.write_text("outside\n", encoding="utf-8")
        link = self.root / "linked-source.md"
        link.symlink_to(outside)
        payload = self.qualification_payload()
        payload["source_bindings"] = [{
            "path": "linked-source.md",
            "sha256": hashlib.sha256(outside.read_bytes()).hexdigest(),
        }]
        self.bind_qualification_payload(payload)
        with self.assertRaisesRegex(RuntimeError, "symbolic link"):
            builder.release_declarations(self.root, self.skill)

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
        (self.root / "tests").mkdir(exist_ok=True)
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

    def test_staged_hygiene_applies_to_prepare_and_write_before_publication(self) -> None:
        pending = self.manifest_text
        for digest in self.package_hashes.values():
            pending = pending.replace(digest, "pending", 1)
        self.manifest.write_text(pending, encoding="utf-8")
        self.write_hygiene_policy(max_file_bytes=1)
        with self.assertRaisesRegex(RuntimeError, "max_file_bytes"):
            builder.prepare_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

        self.manifest.write_text(self.manifest_text, encoding="utf-8")
        self.write_hygiene_policy(max_release_directory_bytes=1)
        with self.assertRaisesRegex(RuntimeError, "max_release_directory_bytes"):
            builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

        self.write_hygiene_policy(max_dist_bytes=1)
        with self.assertRaisesRegex(RuntimeError, "max_dist_bytes"):
            builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

        self.write_hygiene_policy(max_dist_bytes=None)
        report = builder.build_packages(self.root)
        self.assertEqual(report["validation"]["staged_release_hygiene"], "pass")

    def test_hygiene_rejects_junk_symlink_special_and_strict_policy(self) -> None:
        artifacts = self.root / "staged"
        artifacts.mkdir()
        clean = artifacts / "artifact.zip"
        clean.write_bytes(b"clean")
        policy = builder.load_hygiene_policy(self.root)
        self.assertEqual(builder.scan_hygiene_tree(artifacts, policy, "test"), 5)

        junk = artifacts / ".DS_Store"
        junk.write_bytes(b"junk")
        with self.assertRaisesRegex(RuntimeError, "junk"):
            builder.scan_hygiene_tree(artifacts, policy, "test")
        junk.unlink()

        outside = self.root / "outside"
        outside.write_bytes(b"outside")
        link = artifacts / "linked.zip"
        link.symlink_to(outside)
        with self.assertRaisesRegex(RuntimeError, "Symbolic link"):
            builder.scan_hygiene_tree(artifacts, policy, "test")
        link.unlink()

        if hasattr(os, "mkfifo"):
            fifo = artifacts / "stream"
            os.mkfifo(fifo)
            with self.assertRaisesRegex(RuntimeError, "Special file"):
                builder.scan_hygiene_tree(artifacts, policy, "test")
            fifo.unlink()

        policy_path = self.root / "REPOSITORY-HYGIENE.json"
        policy_path.write_text('{"schema_version":"1.0","schema_version":"1.0"}\n')
        with self.assertRaisesRegex(RuntimeError, "Duplicate JSON key"):
            builder.load_hygiene_policy(self.root)
        policy_path.write_text('{"schema_version":"1.0","limits":{"max_file_bytes":NaN}}\n')
        with self.assertRaisesRegex(RuntimeError, "Non-finite JSON value"):
            builder.load_hygiene_policy(self.root)

    def test_prospective_dist_replaces_same_version_for_idempotent_size_math(self) -> None:
        builder.build_packages(self.root)
        release = self.root / "dist" / "1.2.0"
        release_size = sum(path.stat().st_size for path in release.iterdir())
        self.write_hygiene_policy(max_dist_bytes=release_size)
        result = builder.validate_staged_release_hygiene(self.root, "1.2.0", release)
        self.assertEqual(result["replaced_same_version_bytes"], release_size)
        self.assertEqual(result["prospective_dist_bytes"], release_size)

    def test_existing_release_mismatch_never_overwritten(self) -> None:
        report = builder.build_packages(self.root)
        target = self.root / report["artifact_directory"] / report["packages"]["claude"]["file"]
        target.write_bytes(target.read_bytes() + b"externally changed")
        before = self.artifact_bytes()
        with self.assertRaisesRegex(RuntimeError, "Refusing to overwrite"):
            builder.build_packages(self.root)
        self.assertEqual(before, self.artifact_bytes())

    def test_partial_version_directory_is_not_completed_or_replaced(self) -> None:
        destination = self.root / "dist" / "1.2.0"
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

    def test_staged_validator_canonicalizes_only_trusted_parent_ancestors(self) -> None:
        real_parent = self.root / "real-staging"
        skill_root = real_parent / "staged-skill"
        (skill_root / "scripts").mkdir(parents=True)
        (skill_root / "scripts" / "validate_package.py").write_text(
            "# command-path fixture\n", encoding="utf-8"
        )
        alias_parent = self.root / "system-style-alias"
        alias_parent.symlink_to(real_parent, target_is_directory=True)

        with mock.patch.object(
            builder, "run_check", return_value={"status": "pass"}
        ) as run:
            REAL_VALIDATE_STAGED_PACKAGE(alias_parent / skill_root.name, "chatgpt")

        command = run.call_args.args[0]
        command_validator = Path(command[1])
        command_root = Path(command[2])
        expected_root = real_parent.resolve(strict=True) / skill_root.name
        self.assertEqual(command_root, expected_root)
        self.assertEqual(
            command_validator,
            expected_root / "scripts" / "validate_package.py",
        )
        self.assertNotIn(alias_parent, command_root.parents)
        for component in (*reversed(command_root.parents), command_root):
            self.assertFalse(component.is_symlink(), component)

    def test_staged_validator_still_rejects_final_and_internal_symlinks(self) -> None:
        repository = BUILDER_PATH.parent.parent
        actual_validator = (
            repository / "skills" / builder.SKILL_ID / "scripts" / "validate_package.py"
        )
        (self.skill / "scripts" / "validate_package.py").write_bytes(
            actual_validator.read_bytes()
        )

        linked_root = self.root / "linked-staged-skill"
        linked_root.symlink_to(self.skill, target_is_directory=True)
        with self.assertRaises(RuntimeError) as final_error:
            REAL_VALIDATE_STAGED_PACKAGE(linked_root, "chatgpt")
        self.assertIn('"code": "symlink"', str(final_error.exception))

        outside = self.root / "outside-staged-content"
        outside.write_text("outside\n", encoding="utf-8")
        (self.skill / "internal-link").symlink_to(outside)
        with self.assertRaises(RuntimeError) as internal_error:
            REAL_VALIDATE_STAGED_PACKAGE(self.skill, "chatgpt")
        self.assertIn('"code": "symlink"', str(internal_error.exception))

    def test_existing_artifact_symlink_is_rejected(self) -> None:
        builder.build_packages(self.root)
        destination = self.root / "dist" / "1.2.0" / "SHA256SUMS"
        outside = self.root.parent / "outside-checksums"
        outside.write_bytes(destination.read_bytes())
        destination.unlink()
        destination.symlink_to(outside)
        before = outside.read_bytes()
        with self.assertRaisesRegex(RuntimeError, "Symbolic link|Refusing to overwrite"):
            builder.build_packages(self.root)
        self.assertEqual(outside.read_bytes(), before)
        self.assertTrue(destination.is_symlink())

    def test_path_safety_and_case_collision(self) -> None:
        for name in ("../escape", "/absolute", "a//b", "a/./b", "a/../b", "a\\b",
                     "C:/escape", "a\x00b", "a\nb", "a./b", "a/ ", "a?b", "a|b"):
            with self.subTest(name=name), self.assertRaisesRegex(RuntimeError, "Unsafe"):
                builder.safe_relative_name(name)
        self.assertEqual(builder.safe_relative_name("references/example.md"), "references/example.md")
        for name in ("CON", "con.txt", "CON .txt", "references/AUX.md", "COM1.log",
                     "nested/lpt9"):
            with self.subTest(reserved=name), self.assertRaisesRegex(RuntimeError, "Unsafe"):
                builder.safe_relative_name(name)
        with self.assertRaisesRegex(RuntimeError, "Unsafe"):
            builder.safe_relative_name("a" * (builder.MAX_PACKAGE_COMPONENT_BYTES + 1))
        long_path = "/".join(("a" * 80, "b" * 80, "c" * 80))
        self.assertGreater(len(long_path.encode("utf-8")), builder.MAX_PACKAGE_PATH_BYTES)
        with self.assertRaisesRegex(RuntimeError, "Unsafe"):
            builder.safe_relative_name(long_path)
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

    def test_nonprojected_manifest_drift_prevents_publication(self) -> None:
        def mutate_manifest(*args):
            content = self.manifest.read_text(encoding="utf-8")
            self.manifest.write_text(
                content.replace('status: "release_candidate"', 'status: "draft"', 1),
                encoding="utf-8",
            )
            return {"status": "pass"}

        self.staged.side_effect = mutate_manifest
        with self.assertRaisesRegex(RuntimeError, "release metadata changed during the build"):
            builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_manifest_byte_only_drift_prevents_publication(self) -> None:
        def mutate_manifest_bytes(*args):
            content = self.manifest.read_text(encoding="utf-8")
            if "# concurrent byte-only drift" not in content:
                self.manifest.write_text(
                    content + "# concurrent byte-only drift\n", encoding="utf-8"
                )
            return {"status": "pass"}

        self.staged.side_effect = mutate_manifest_bytes
        with self.assertRaisesRegex(RuntimeError, "release metadata changed during the build"):
            builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_structural_failure_prevents_publication(self) -> None:
        self.static.side_effect = RuntimeError("synthetic static failure")
        with self.assertRaisesRegex(RuntimeError, "static failure"):
            builder.build_packages(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_report_uses_retained_qualification_not_static_runner_behavior(self) -> None:
        self.static.return_value["case_registry"]["behavioral"]["status"] = "pass"
        report = builder.build_packages(self.root)
        persisted = json.loads(self.artifact_bytes()["packaging-report.json"])
        self.assertEqual(report["behavioral"]["status"], "pass_via_retained_qualification_report")
        self.assertTrue(report["behavioral"]["evidence_verified"])
        self.assertEqual(report["behavioral"]["fresh_context_scenarios_reviewed_pass"], 1)
        self.assertEqual(report["release_acceptance"], "qualified_by_retained_report")
        self.assertEqual(report["behavioral"]["registry_reported_status"], "pass")
        self.assertEqual(persisted["behavioral"], report["behavioral"])
        self.assertEqual(persisted["qualification"], report["qualification"])
        self.assertNotIn("publication", persisted)

    def test_report_records_runtime_and_builder_provenance(self) -> None:
        report = builder.build_packages(self.root)
        provenance = report["runtime_provenance"]
        persisted = json.loads(self.artifact_bytes()["packaging-report.json"])
        self.assertEqual(set(provenance), {"python", "zlib", "platform", "builder"})
        self.assertTrue(provenance["python"]["implementation"])
        self.assertRegex(provenance["python"]["version"], r"^\d+\.\d+\.\d+")
        self.assertTrue(provenance["zlib"]["compile_version"])
        self.assertTrue(provenance["zlib"]["runtime_version"])
        self.assertIn(provenance["platform"]["architecture_bits"], {32, 64})
        self.assertTrue(provenance["platform"]["system"])
        self.assertEqual(provenance["builder"]["file"], "scripts/build_release.py")
        self.assertRegex(provenance["builder"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(persisted["runtime_provenance"], provenance)
        self.assertNotIn(str(BUILDER_PATH.parent), json.dumps(provenance))
        self.assertEqual(
            report["validation"]["release_manifest_package_binding"], "pass"
        )

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

    def test_run_check_disables_repository_bytecode_writes(self) -> None:
        completed = subprocess.CompletedProcess(
            ["synthetic"], 0, '{"status":"pass"}', ""
        )
        with mock.patch.object(builder.subprocess, "run", return_value=completed) as run:
            builder.run_check(["synthetic"], "synthetic gate")
        self.assertEqual(run.call_args.kwargs["env"]["PYTHONDONTWRITEBYTECODE"], "1")

    def test_cli_without_write_does_not_build(self) -> None:
        with (mock.patch.object(builder, "build_packages") as build,
              mock.patch.object(builder, "prepare_packages") as prepare):
            with contextlib.redirect_stderr(io.StringIO()):
                result = builder.main(["--repo-root", str(self.root), "--json"])
        self.assertEqual(result, 2)
        build.assert_not_called()
        prepare.assert_not_called()
        self.assertFalse((self.root / "dist").exists())

    def test_cli_prepare_dispatches_without_publish(self) -> None:
        prepared = {
            "mode": "prepare",
            "publication": "not_performed_prepare_only",
            "repository_writes": False,
            "computed_release_declarations": {"packages": []},
        }
        with (mock.patch.object(builder, "prepare_packages", return_value=prepared) as prepare,
              mock.patch.object(builder, "build_packages") as publish,
              contextlib.redirect_stdout(io.StringIO()) as output):
            result = builder.main([
                "--repo-root", str(self.root), "--prepare", "--json",
            ])
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(output.getvalue()), prepared)
        prepare.assert_called_once_with(self.root)
        publish.assert_not_called()

    def test_cli_modes_are_mutually_exclusive(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            builder.main(["--repo-root", str(self.root), "--prepare", "--write"])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
