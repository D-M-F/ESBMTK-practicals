import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from scripts.build_setup_package import ARCHIVE_ROOT, PACKAGE_FILES, build_package


ROOT = Path(__file__).resolve().parents[1]


class SetupPackageTests(unittest.TestCase):
    def test_package_allow_list_excludes_exercises_and_course_data(self):
        destinations = set(PACKAGE_FILES)
        self.assertFalse(any(name.startswith("notebooks/") for name in destinations))
        self.assertFalse(any(name.startswith("data/") for name in destinations))
        self.assertIn("JUPYTER_BASICS.ipynb", destinations)
        self.assertIn("setup_assets/workbook_probe.xlsx", destinations)

    def test_zip_contains_exact_allow_list(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "setup.zip"
            build_package(output)
            with ZipFile(output) as archive:
                names = set(archive.namelist())
        expected = {f"{ARCHIVE_ROOT}/{name}" for name in PACKAGE_FILES}
        self.assertEqual(names, expected)

    def test_repeated_builds_are_identical(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.zip"
            second = Path(directory) / "second.zip"
            build_package(first)
            build_package(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_transition_guide_has_both_routes(self):
        guide = PACKAGE_FILES["START_HERE.md"].read_text(encoding="utf-8")
        self.assertIn("uv sync --locked", guide)
        self.assertIn("conda activate esbmtk-practicals", guide)
        self.assertIn("do not copy `.venv`", guide)

    def test_jupyter_basics_is_an_unexecuted_valid_notebook(self):
        notebook = json.loads((ROOT / "JUPYTER_BASICS.ipynb").read_text(encoding="utf-8"))
        self.assertEqual(notebook["nbformat"], 4)
        code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        self.assertTrue(code_cells)
        self.assertTrue(all(cell["execution_count"] is None for cell in code_cells))
        self.assertTrue(all(cell["outputs"] == [] for cell in code_cells))


if __name__ == "__main__":
    unittest.main()
