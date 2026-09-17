"""Regression safety for the shared Boudreau-like model."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import unittest

import numpy as np

from model import initialize_model, postprocess_carbonate_horizons, run_model
from presets import BOUDREAU_2010


ROOT = Path(__file__).resolve().parents[1]


class Boudreau2010RegressionTest(unittest.TestCase):
    """Compare the teaching implementation with the authoritative reference."""

    @classmethod
    def setUpClass(cls):
        cls.model = initialize_model(
            BOUDREAU_2010,
            stop="1000 kyr",
            max_timestep="100 yr",
        )
        run_model(cls.model, method="BDF")
        postprocess_carbonate_horizons(cls.model)

    def test_reference_state(self):
        M = self.model
        tolerance = 1e-3
        values = {
            "L_b DIC": (M.L_b.DIC.c[-1] * 1e6, 1940.91189),
            "H_b DIC": (M.H_b.DIC.c[-1] * 1e6, 2152.08134),
            "D_b DIC": (M.D_b.DIC.c[-1] * 1e6, 2294.96581),
            "L_b TA": (M.L_b.TA.c[-1] * 1e6, 2282.13700),
            "H_b TA": (M.H_b.TA.c[-1] * 1e6, 2348.50915),
            "D_b TA": (M.D_b.TA.c[-1] * 1e6, 2403.81926),
            "L_b pH": (M.L_b.pH.c[-1], 8.268),
            "H_b pH": (M.H_b.pH.c[-1], 8.231),
            "D_b pH": (M.D_b.pH.c[-1], 7.912),
            "L_b CO3": (M.L_b.CO3.c[-1] * 1e6, 236.98378),
            "H_b CO3": (M.H_b.CO3.c[-1] * 1e6, 140.47935),
            "D_b CO3": (M.D_b.CO3.c[-1] * 1e6, 87.39742),
            "zsat": (M.D_b.zsat.c[-1], 3755.0),
            "zcc": (M.D_b.zcc.c[-1], 4812.0),
            "zsnow": (M.D_b.zsnow.c[-1], 4812.9963),
        }
        for name, (observed, expected) in values.items():
            with self.subTest(name=name):
                relative_difference = abs(observed - expected) / abs(expected)
                self.assertLessEqual(relative_difference, tolerance)


class Boudreau2010ReferenceDataTest(unittest.TestCase):
    def test_archived_pulse_identity_and_integrated_mass(self):
        path = ROOT / "data" / "Boudreau_2010" / "IS92a-scenario.csv"
        self.assertEqual(
            sha256(path.read_bytes()).hexdigest(),
            "6024588cd37addcded8261f452defec49a7f0d284892780237d48fa8ab3bd6b6",
        )
        data = np.genfromtxt(path, delimiter=",", skip_header=1)
        years = data[:, 0]
        carbon_flux = data[:, 1]
        mask = years >= 1800.0
        moles = np.trapezoid(carbon_flux[mask] * 0.877, years[mask])
        self.assertAlmostEqual(moles / 1e15, 335.3560189847107, places=9)
        self.assertAlmostEqual(moles * 12.0 / 1e15, 4024.2722278165284, places=9)


if __name__ == "__main__":
    unittest.main()
