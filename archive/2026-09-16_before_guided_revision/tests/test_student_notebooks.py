"""Static checks for instructor and generated student notebooks."""

from __future__ import annotations

import json
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory

from scripts.build_student_notebooks import NOTEBOOKS, build_student_notebook


ROOT = Path(__file__).resolve().parents[1]
EXERCISE_NOTEBOOKS = NOTEBOOKS


class StudentNotebookTest(unittest.TestCase):
    def test_student_copies_are_masked_and_have_unique_cell_ids(self):
        for name in EXERCISE_NOTEBOOKS:
            with self.subTest(notebook=name):
                path = ROOT / "notebooks" / "student" / name
                notebook = json.loads(path.read_text(encoding="utf-8"))
                rendered = json.dumps(notebook)
                self.assertNotIn("BEGIN SOLUTION", rendered)
                self.assertNotIn("END SOLUTION", rendered)
                self.assertTrue(
                    "Your explanation" in rendered
                    or "Exercise: replace this line" in rendered
                )
                ids = [cell["id"] for cell in notebook["cells"]]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(
                    all(
                        not cell.get("outputs")
                        for cell in notebook["cells"]
                        if cell["cell_type"] == "code"
                    )
                )

    def test_03_requires_students_to_construct_the_baseline(self):
        path = ROOT / "notebooks" / "student" / "03_boudreau_three_box_model.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        code_source = "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )
        self.assertGreaterEqual(code_source.count("NotImplementedError"), 7)
        self.assertNotIn("initialize_model", code_source)

    def test_04_keeps_compatibility_implementation_supplied(self):
        path = ROOT / "notebooks" / "student" / "04_pump_strength_OA_OAE.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        code_source = "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )
        self.assertEqual(code_source.count("NotImplementedError"), 2)
        self.assertIn("make_process_variant", code_source)
        self.assertIn("make_pump_variant", code_source)
        self.assertIn("normalized_hill", code_source)
        self.assertIn("decompose_dic_storage", code_source)
        self.assertIn("build_complete_case", code_source)
        self.assertIn("feedback_switches", code_source)

    def test_03_04_share_excel_inputs_without_hiding_construction(self):
        for name in EXERCISE_NOTEBOOKS[2:]:
            nb = json.loads((ROOT / 'notebooks/student' / name).read_text(encoding='utf-8'))
            source = '\n'.join(''.join(c['source']) for c in nb['cells'])
            self.assertIn('load_boudreau_parameters(WORKBOOK)', source)
            self.assertIn("input_tables['OceanReservoirs']", source)
            self.assertIn("input_tables['Atmosphere']", source)
            self.assertIn('reservoir_inventory_rows', source)
            self.assertIn('model_definition.xlsx', source)
            self.assertIn('read_model_tables(WORKBOOK)', source)
            self.assertIn("input_tables['TransportConnections']", source)
            self.assertIn("input_tables['GasExchangeConnections']", source)
            self.assertIn("input_tables['ProcessParameters']", source)
            self.assertNotIn("area_percentage", source)
            if name.startswith('03'):
                self.assertIn('high_specification', source)
                self.assertIn('Exercise 03.2', source)
            else:
                self.assertEqual(source.count('base=P,'), 2)

    def test_generated_copies_match_instructor_sources(self):
        with TemporaryDirectory() as tmp:
            for name in NOTEBOOKS:
                with self.subTest(notebook=name):
                    target = Path(tmp) / name
                    build_student_notebook(ROOT / "notebooks/instructor" / name, target)
                    self.assertEqual(target.read_bytes(),
                                     (ROOT / "notebooks/student" / name).read_bytes())

    def test_intro_exercises_and_scientific_labels(self):
        def read(name, directory="instructor"):
            nb = json.loads((ROOT / "notebooks" / directory / name).read_text(encoding="utf-8"))
            return "\n".join("".join(c["source"]) for c in nb["cells"])

        n1, n2 = NOTEBOOKS[:2]
        one, two = read(n1), read(n2)
        self.assertLess(one.index("FIRST_TA = 0.0"), one.index("reference = pyco2.sys"))
        self.assertIn("not an independent prediction", one)
        self.assertIn("calibration-first", two)
        self.assertIn("not independent validation", " ".join(two.split()))
        self.assertIn("integrated_signal", two)
        self.assertGreaterEqual(read(n1, "student").count("NotImplementedError"), 2)
        self.assertGreaterEqual(read(n2, "student").count("NotImplementedError"), 5)

    def test_02_masks_derivations_and_keeps_the_forcing_example_supplied(self):
        name = "02_two_layer_ocean_carbon_pump.ipynb"
        nb = json.loads((ROOT / "notebooks/student" / name).read_text(encoding="utf-8"))
        source = "\n".join("".join(c["source"]) for c in nb["cells"])
        self.assertIn("derive the expression before coding", source)
        self.assertIn("J_{pump}(t)=kDIC_s(t)", source)
        self.assertNotIn(r"k=Q\rho", source)
        self.assertNotIn("calibrated_pump_coefficient", source)
        self.assertNotIn("extra_carbon_mol =", source)
        self.assertNotIn("finite_box_addition", source)
        self.assertIn("signal = Signal(", source)
        self.assertIn("mass=f'{extra_carbon_mol} mol'", source)
        self.assertIn("pumped_ocean_atmosphere_ratio", source)
        self.assertIn("integrated_signal", source)

    def test_all_teaching_markdown_uses_dollar_math_delimiters(self):
        paths = [
            ROOT / "notebooks" / "01_single_box_air_sea_CO2.ipynb",
            ROOT / "notebooks" / "02_two_layer_ocean_carbon_pump.ipynb",
            *(ROOT / "notebooks" / "instructor" / name for name in EXERCISE_NOTEBOOKS),
        ]
        forbidden = (r"\(", r"\)", r"\[", r"\]")
        for path in paths:
            with self.subTest(notebook=path.name):
                notebook = json.loads(path.read_text(encoding="utf-8"))
                markdown_source = "\n".join(
                    "".join(cell.get("source", []))
                    for cell in notebook["cells"]
                    if cell["cell_type"] == "markdown"
                )
                for delimiter in forbidden:
                    self.assertNotIn(delimiter, markdown_source)


if __name__ == "__main__":
    unittest.main()
