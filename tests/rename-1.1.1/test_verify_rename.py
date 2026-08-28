"""Small synthetic tooling fixtures, not skill behavioral executions."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "rename_verifier", Path(__file__).resolve().parents[2] / "scripts/verify_rename.py")
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class RenameVerifierTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="rename-check-unit-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        prefix = f"skills/{verifier.OLD_ID}/"
        self.baseline = {
            prefix + "SKILL.md": b"name: thien-skill-risk-process-control\nKeep evidence limitations.\n",
            prefix + "templates/example.yaml": b'schema_version: "1.1.0"\n',
            "LICENSE": b"Synthetic unchanged license terms.\n",
            "NOTICE": b"Thien-Skill-Risk-Process-Control - Synthetic notice\n",
            "LICENSE-APPLICATION.md": (
                f"Thien-Skill-Risk-Process-Control `1.1.0`\n{verifier.URL}\n").encode(),
            "tests/legacy.txt": b"Original historical evidence.\n",
            "dist/1.1.0/old.zip": b"Synthetic historical archive bytes, not a ZIP.\n",
        }
        for path, data in self.baseline.items():
            if path.startswith(prefix):
                name = path[len(prefix):]
                path = f"skills/{verifier.NEW_ID}/{name}"
                data = verifier.expected_bytes(name, data)
            elif path in ("NOTICE", "LICENSE-APPLICATION.md"):
                data = verifier.expected_bytes(path, data)
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (self.root / "docs").mkdir(exist_ok=True)
        for name in ("INSTALL.md", "docs/HANDOFF.md"):
            (self.root / name).write_text("Synthetic documentation.\n")
        (self.root / "README.md").write_text(
            "## Vai trò của skill\n## Lợi ích và tính năng khi kích hoạt\n"
            "## Cách sử dụng skill\n## Cài đặt\n")
        (self.root / "RELEASE-MANIFEST.yaml").write_text(
            f'url: "{verifier.CURRENT_URL}"\nvisibility: "public"\nskill_id: "{verifier.NEW_ID}"\nskill_version: "1.1.1"\n')

    def check(self):
        return verifier.verify(self.root, self.baseline)

    def test_identity_only_change_preserves_historical_url_and_schema(self):
        self.assertEqual(self.check()["status"], "pass")
        self.assertIn(verifier.URL, (self.root / "LICENSE-APPLICATION.md").read_text())
        self.assertEqual((self.root / f"skills/{verifier.NEW_ID}/templates/example.yaml").read_bytes(),
                         b'schema_version: "1.1.0"\n')

    def test_business_instruction_change_is_rejected(self):
        (self.root / f"skills/{verifier.NEW_ID}/SKILL.md").write_text("Do something else.\n")
        self.assertIn("Unexpected content change: SKILL.md", self.check()["errors"])

    def test_schema_change_is_rejected(self):
        (self.root / f"skills/{verifier.NEW_ID}/templates/example.yaml").write_text('schema_version: "1.1.1"\n')
        self.assertIn("Unexpected content change: templates/example.yaml", self.check()["errors"])

    def test_license_change_is_rejected(self):
        (self.root / "LICENSE").write_text("Different terms.\n")
        self.assertIn("Historical/license artifact changed: LICENSE", self.check()["errors"])

    def test_old_zip_change_is_rejected(self):
        (self.root / "dist/1.1.0/old.zip").write_bytes(b"Changed")
        self.assertIn("Historical/license artifact changed: dist/1.1.0/old.zip", self.check()["errors"])

    def test_unapproved_repository_metadata_change_is_rejected(self):
        manifest = self.root / "RELEASE-MANIFEST.yaml"
        original = manifest.read_text()
        for before, after, message in (
            (verifier.CURRENT_URL, verifier.CURRENT_URL + "-other",
             "Repository URL does not match the authorized current URL"),
            ('visibility: "public"', 'visibility: "private"',
             "Repository visibility does not match user-confirmed public status"),
        ):
            with self.subTest(field=before):
                manifest.write_text(original.replace(before, after))
                self.assertIn(message, self.check()["errors"])


if __name__ == "__main__":
    unittest.main()
