import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'codex-global-skills'
sys.path.insert(0, str(ROOT / 'scripts'))
from package_skills import build
from validate_bundle import validate


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # macOS /var is a symlink: use the resolved temporary destination.
        self.root = Path(self.temp.name).resolve()
        self.dest = self.root / 'skills'
        self.names = {e['name'] for e in json.loads((BUNDLE / 'manifest.json').read_text())['skills']}

    def run_install(self, *extra, bundle=BUNDLE):
        return subprocess.run([sys.executable, str(bundle / 'install.py'), '--destination', str(self.dest), *extra], capture_output=True, text=True)

    def test_fresh_install_and_idempotent_reinstall(self):
        first = self.run_install()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual({p.name for p in self.dest.iterdir()}, self.names)
        second = self.run_install()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(second.stdout.count('Already installed:'), len(self.names))

    def test_check_does_not_write(self):
        result = self.run_install('--check')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.dest.exists())

    def test_conflict_detected_before_any_installation(self):
        conflict = self.dest / 'data-review'
        conflict.mkdir(parents=True)
        sentinel = conflict / 'SKILL.md'
        sentinel.write_text('User customization')
        result = self.run_install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sentinel.read_text(), 'User customization')
        self.assertEqual(list(self.dest.iterdir()), [conflict])

    def test_tampering_detected_before_install(self):
        bundle = self.root / 'bundle'
        shutil.copytree(BUNDLE, bundle)
        (bundle / 'skills' / 'socratic-tutor' / 'SKILL.md').write_text('Tampered')
        result = self.run_install(bundle=bundle)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('checksum mismatch', result.stderr)
        self.assertFalse(self.dest.exists())

    def test_existing_symlink_not_followed(self):
        outside = self.root / 'outside'
        outside.mkdir()
        self.dest.mkdir()
        (self.dest / 'socratic-tutor').symlink_to(outside, target_is_directory=True)
        result = self.run_install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_failed_copy_rolls_back_new_directories(self):
        spec = importlib.util.spec_from_file_location('bundle_installer', BUNDLE / 'install.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with patch.object(sys, 'argv', ['install.py', '--destination', str(self.dest)]):
            with patch.object(module.shutil, 'copytree', side_effect=OSError('simulated disk failure')):
                with self.assertRaises(OSError):
                    module.main()
        self.assertEqual(list(self.dest.iterdir()), [])

    def test_manifest_and_skill_metadata(self):
        manifest, count = validate(BUNDLE)
        self.assertEqual({e['name'] for e in manifest['skills']}, self.names)
        self.assertGreater(count, len(self.names))

    def test_packaging_is_repeatable_and_archive_installs(self):
        first = self.root / 'a.zip'
        second = self.root / 'b.zip'
        self.assertEqual(build(BUNDLE, first), build(BUNDLE, second))
        extracted = self.root / 'extracted'
        with zipfile.ZipFile(first) as archive:
            self.assertIsNone(archive.testzip())
            self.assertNotIn('codex-global-skills/verification.json', archive.namelist())
            archive.extractall(extracted)
        result = self.run_install(bundle=extracted / 'codex-global-skills')
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
