"""Checks for the one-trajectory process-tagged storage attribution."""

from __future__ import annotations

import unittest

import numpy as np

from model import initialize_model, run_model
from presets import make_process_variant
from storage_decomposition import decompose_dic_storage


class TaggedStorageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        params = make_process_variant(
            gas_exchange=True,
            soft_tissue=True,
            carbonate=True,
            weathering=False,
        )
        cls.model = initialize_model(params, stop="100 yr", max_timestep="1 yr")
        run_model(cls.model)
        cls.storage = decompose_dic_storage(cls.model)

    def test_atmosphere_is_prognostic(self):
        self.assertNotAlmostEqual(
            self.model.CO2_At.c[-1], self.model.CO2_At.c[0], places=9
        )

    def test_internal_tags_conserve_ocean_carbon(self):
        for name in ("soft_tissue", "carbonate"):
            with self.subTest(tag=name):
                self.assertLess(abs(self.storage.mass[name][-1].sum()), 1e5)

    def test_gas_tag_closes_with_atmosphere(self):
        residual = (
            self.storage.mass["gas_exchange"][-1].sum()
            + self.storage.atmospheric_gas_tag_mol[-1]
        )
        self.assertLess(abs(residual), 1e8)

    def test_tags_reconstruct_final_dic_and_expected_deep_storage(self):
        self.assertLess(np.max(np.abs(self.storage.closure_umol_kg[-1])), 0.2)
        for name in ("gas_exchange", "soft_tissue", "carbonate"):
            values = self.storage.concentration_umol_kg[name][-1]
            with self.subTest(tag=name):
                self.assertGreater(values[2] - values[0], 0)


if __name__ == "__main__":
    unittest.main()
