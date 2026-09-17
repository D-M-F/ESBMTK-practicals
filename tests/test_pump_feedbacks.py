"""Unit and end-to-end checks for Boudreau-like pump experiments."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

import numpy as np

from model import initialize_model, postprocess_carbonate_horizons, run_model
from presets import BOUDREAU_2010, make_process_variant, make_pump_variant
from pump_functions import carbonate_export, normalized_hill, soft_tissue_export
from scenarios import add_alkalinity_signal, add_carbon_signal


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "Boudreau_2010" / "steady_state"


class PumpFunctionTest(unittest.TestCase):
    def test_hill_response_is_one_at_reference(self):
        self.assertAlmostEqual(normalized_hill(2.0, 2.0, 1.5, 2.0), 1.0)

    def test_carbonate_function_returns_exact_one_to_two_fluxes(self):
        dic_flux, ta_flux = carbonate_export(
            2.0e-3,
            2.3e-3,
            (60e12, 1.0, 0.3e-3, 0.25e-3, 2.0),
        )
        self.assertGreater(dic_flux, 0)
        self.assertEqual(ta_flux, 2.0 * dic_flux)

    def test_soft_tissue_function_is_bounded_and_monotonic(self):
        params = (200e12, 1.0, 280e-6, 280e-6, 1.0)
        low = soft_tissue_export(140e-6, params)
        reference = soft_tissue_export(280e-6, params)
        high = soft_tissue_export(1120e-6, params)
        self.assertLess(low, reference)
        self.assertLess(reference, high)
        self.assertLess(high, 400e12)


class PumpPresetTest(unittest.TestCase):
    def test_variant_is_independent_and_scales_temperature_contrast(self):
        original = deepcopy(BOUDREAU_2010)
        variant = make_pump_variant(
            solubility_strength=0.5,
            soft_tissue_strength=1.2,
            carbonate_strength=0.8,
            soft_tissue_feedback=True,
            carbonate_feedback=True,
        )
        self.assertEqual(BOUDREAU_2010, original)
        self.assertAlmostEqual(variant["boxes"]["H_b"]["temperature"], 11.75)
        self.assertEqual(variant["pump_strengths"]["soft_tissue"], 1.2)
        self.assertEqual(variant["pump_strengths"]["carbonate"], 0.8)
        self.assertTrue(variant["pump_feedbacks"]["soft_tissue"]["enabled"])
        self.assertTrue(variant["pump_feedbacks"]["carbonate"]["enabled"])

    def test_poc_and_pic_strengths_are_independent(self):
        variant = make_pump_variant(
            soft_tissue_strength=0.5, carbonate_strength=1.5
        )
        model = initialize_model(variant, stop="10 yr", max_timestep="1 yr")
        self.assertAlmostEqual(model.OM_export.to("Tmol/yr").magnitude, 100.0)
        self.assertAlmostEqual(model.CaCO3_export.to("Tmol/yr").magnitude, 90.0)
        self.assertAlmostEqual(model.rain_ratio, 0.9)

    def test_process_variant_keeps_physics_and_disables_weathering(self):
        variant = make_process_variant(
            gas_exchange=False,
            soft_tissue=True,
            carbonate=False,
        )
        self.assertFalse(variant["gas_exchange_enabled"])
        self.assertEqual(variant["pump_strengths"]["soft_tissue"], 1.0)
        self.assertEqual(variant["pump_strengths"]["carbonate"], 0.0)
        self.assertEqual(variant["weathering_strength"], 0.0)
        self.assertFalse(variant["carbonate_compensation_enabled"])
        self.assertEqual(variant["thc"], BOUDREAU_2010["thc"])
        self.assertEqual(variant["mixing"], BOUDREAU_2010["mixing"])


class PumpFeedbackIntegrationTest(unittest.TestCase):
    def model(self):
        params = make_pump_variant(
            soft_tissue_feedback=True,
            carbonate_feedback=True,
        )
        model = initialize_model(params, stop="50 yr", max_timestep="1 yr")
        model.read_state(directory=str(STATE))
        return model

    def test_oa_changes_pco2_dependent_soft_tissue_export(self):
        model = self.model()
        add_carbon_signal(
            model, duration="20 yr", mass="10 Pmol", shape="square"
        )
        run_model(model)
        self.assertEqual(len(model.OM_export_flux.m), len(model.time))
        self.assertTrue(np.all(model.OM_export_flux.m > 0))
        self.assertGreater(model.OM_export_flux.m.max(), model.OM_export_flux.m[0])

    def test_oae_changes_ta_dic_dependent_pic_and_preserves_stoichiometry(self):
        model = self.model()
        add_alkalinity_signal(
            model, duration="20 yr", mass="5 Pmol", shape="square"
        )
        run_model(model)
        postprocess_carbonate_horizons(model)
        pic = model.CaCO3_export_flux.m
        ta = model.carbonate_ta_connection.fh.m
        self.assertEqual(len(pic), len(model.time))
        np.testing.assert_allclose(ta, 2.0 * pic, rtol=0, atol=0)
        self.assertGreater(pic.max(), pic[0])
        self.assertEqual(len(model.D_b.zcc.c), len(model.time))


if __name__ == "__main__":
    unittest.main()
