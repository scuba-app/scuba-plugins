import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent


class PackageScriptTests(unittest.TestCase):
    def test_package_builds_verified_posix_archives(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir)
            res = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "package.py"),
                    "--output",
                    str(out_dir),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(res.returncode, 0, msg=res.stderr or res.stdout)
            sums = (out_dir / "SHA256SUMS").read_text(encoding="utf-8")
            for platform in ("openai", "cursor", "claude"):
                archive = out_dir / f"scuba-{platform}.zip"
                self.assertTrue(archive.exists(), msg=f"Missing {archive}")
                self.assertIn(archive.name, sums)
                with ZipFile(archive) as zf:
                    names = zf.namelist()
                    self.assertTrue(any(n.startswith("skills/") for n in names))
                    for name in names:
                        self.assertNotIn("\\", name)
                    self.assertIsNone(zf.testzip())


if __name__ == "__main__":
    unittest.main()
