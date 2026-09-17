"""Static checks for instructor and generated student notebooks."""

from __future__ import annotations

import json
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory

from scripts.build_student_notebooks import NOTEBOOKS, EXTENSION_NOTEBOOKS, build_student_notebook


ROOT = Path(__file__).resolve().parents[1]
EXERCISE_NOTEBOOKS = NOTEBOOKS


class StudentNotebookTest(unittest.TestCase):
    def test_00_provides_one_example_and_no_exercise_solutions(self):
        path = ROOT / "notebooks/student/00_PyCO2SYS.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        source = "\n".join("".join(c["source"]) for c in notebook["cells"])
        code = "\n".join("".join(c["source"]) for c in notebook["cells"]
                         if c["cell_type"] == "code")
        self.assertEqual(code.count("pyco2.sys("), 1)
        self.assertIn("par1=2300.0, par1_type=1", code)
        self.assertIn("par2=2000.0, par2_type=2", code)
        self.assertIn("**C.chemistry", code)
        self.assertEqual(source.count("Your explanation"), 8)
        self.assertEqual(code.count("# Your calculation"), 8)
        for letter in "abcdefgh":
            self.assertIn(f"## {letter})", source)
        self.assertIn("https://pyco2sys.readthedocs.io/en/latest/co2sys_nd/", source)
        self.assertNotIn("def equilibrium", code)
        self.assertNotIn("show_state", code)
        for answer in ("7.982", "1.975", "2922.4", "822.4", "637.2"):
            self.assertNotIn(answer, source)
        self.assertFalse(any("solution-only" in c.get("metadata", {}).get("tags", [])
                             for c in notebook["cells"]))

    def test_student_copies_are_masked_and_have_unique_cell_ids(self):
        for name in (*EXERCISE_NOTEBOOKS, *EXTENSION_NOTEBOOKS):
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
        self.assertEqual(code_source.count("NotImplementedError"), 4)
        self.assertNotIn("initialize_model", code_source)
        # The four semantic mappings are masked; native calls and repetition
        # remain readable, so students never need to rebuild API scaffolding.
        for constructor in ("Model(", "initialize_reservoirs(",
                            "create_bulk_connections(", "Species2Species("):
            self.assertIn(constructor, code_source)
        self.assertIn("for row in P['transport_connections']", code_source)
        self.assertIn("'sp': transported_species", code_source)
        self.assertIn("'ra': pic_ta_rate", code_source)
        self.assertIn("add_carbonate_system_2(", code_source)

    def test_04_keeps_compatibility_implementation_supplied(self):
        path = ROOT / "notebooks" / "student" / "04_pump_strength_OA_OAE.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        code_source = "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )
        # Two forcing tasks: inventory conversion, then one endpoint choice
        # in each supplied OA/OAE branch. No tagging or feedback runs in core.
        self.assertEqual(code_source.count("NotImplementedError"), 3)
        self.assertNotIn("make_process_variant", code_source)
        self.assertIn("make_pump_variant", code_source)
        self.assertNotIn("normalized_hill", code_source)
        self.assertNotIn("decompose_dic_storage", code_source)
        self.assertIn("build_complete_case", code_source)
        self.assertNotIn("feedback_switches", code_source)
        self.assertIn("signal = Signal(", code_source)
        self.assertIn("sink=forcing_target", code_source)
        self.assertIn("audit_complete_model(case, label)", code_source)
        self.assertIn("from teaching_plots import plot_figure4", code_source)
        self.assertIn("plot_figure4(fixed_cases['OA']", code_source)
        self.assertIn("plot_figure4(fixed_cases['OAE']", code_source)
        self.assertNotIn("def plot_figure4", code_source)

    def test_optional_04_remains_self_contained_and_masked(self):
        nb = json.loads((ROOT / 'notebooks/student' / EXTENSION_NOTEBOOKS[0]).read_text(encoding='utf-8'))
        source = '\n'.join(''.join(c['source']) for c in nb['cells'])
        self.assertIn('Outside the four-hour core', source)
        for token in ('decompose_dic_storage', 'build_complete_case',
                      'feedback_switches', 'normalized_hill', 'response_summary'):
            self.assertIn(token, source)
        self.assertNotIn('plot_figure4', source)
        self.assertNotIn('# Part II — Aggregate OA', source)
        self.assertIn('Supplied prerequisites for Part III', source)

    def test_03_04_share_excel_inputs_without_hiding_construction(self):
        for name in EXERCISE_NOTEBOOKS:
            if not name.startswith(("03_", "04_")):
                continue
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
                self.assertEqual(source.count('base=P,'), 1)

    def test_generated_copies_match_instructor_sources(self):
        with TemporaryDirectory() as tmp:
            for name in (*NOTEBOOKS, *EXTENSION_NOTEBOOKS):
                with self.subTest(notebook=name):
                    target = Path(tmp) / name
                    build_student_notebook(ROOT / "notebooks/instructor" / name, target)
                    self.assertEqual(target.read_bytes(),
                                     (ROOT / "notebooks/student" / name).read_bytes())

    def test_intro_exercises_and_scientific_labels(self):
        def read(name, directory="instructor"):
            nb = json.loads((ROOT / "notebooks" / directory / name).read_text(encoding="utf-8"))
            return "\n".join("".join(c["source"]) for c in nb["cells"])

        n1 = "01_single_box_air_sea_CO2.ipynb"
        n2 = "02_two_layer_ocean_carbon_pump.ipynb"
        one, two = read(n1), read(n2)
        self.assertLess(one.index("FIRST_TA = 0.0"), one.index("reference = pyco2.sys"))
        self.assertIn("not an independent prediction", one)
        self.assertIn("calibration-first", two)
        self.assertIn("not independent validation", " ".join(two.split()))
        self.assertIn("integrated_signal", two)
        self.assertEqual(read(n1, "student").count("NotImplementedError"), 1)
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
            *(ROOT / "notebooks" / "instructor" / name for name in EXTENSION_NOTEBOOKS),
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
