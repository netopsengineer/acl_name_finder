"""Offline syntax and security-regression checks. Never contact managed hosts."""
import ast
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class OfflineSafety(unittest.TestCase):
    def test_python_sources_parse_without_execution(self):
        paths = [p for p in ROOT.rglob("*.py") if not any(x.startswith(".") for x in p.relative_to(ROOT).parts)]
        for path in paths:
            with self.subTest(path=str(path.relative_to(ROOT))):
                ast.parse(path.read_text(), filename=str(path))

    def test_supported_controller_python(self):
        self.assertEqual((ROOT / ".python-version").read_text().strip(), "3.12.15")

    def test_ci_has_no_inventory_or_dependency_export(self):
        text = (ROOT / ".github/workflows/offline-security.yml").read_text()
        self.assertIn("persist-credentials: false", text)
        self.assertIn("contents: read", text)
        self.assertNotIn("pip install", text)
        self.assertNotIn("ansible-playbook", text)

    def test_install_instructions_verify_tls(self):
        self.assertNotIn("--ignore-certs", (ROOT / "requirements.yml").read_text())
