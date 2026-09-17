"""Forcing-budget checks independent of the internal carbon-cycle response."""

from __future__ import annotations

import unittest

from model import initialize_model
from presets import BOUDREAU_2010
from scenarios import add_alkalinity_signal, add_carbon_signal


class ExternalSignalBudgetTest(unittest.TestCase):
    def test_square_carbon_signal_integrates_to_requested_mass(self):
        model = initialize_model(BOUDREAU_2010, stop="100 yr", max_timestep="1 yr")
        signal = add_carbon_signal(
            model, duration="20 yr", mass="10 Pmol", shape="square"
        )
        integrated_mass = signal.m.sum() * model.dt
        self.assertAlmostEqual(integrated_mass, signal.mass, delta=signal.mass * 1e-12)

    def test_pure_ta_signal_has_no_direct_dic_or_carbon_connection(self):
        model = initialize_model(BOUDREAU_2010, stop="100 yr", max_timestep="1 yr")
        signal = add_alkalinity_signal(
            model, duration="20 yr", mass="20 Pmol", shape="square"
        )
        integrated_mass = signal.m.sum() * model.dt
        self.assertAlmostEqual(integrated_mass, signal.mass, delta=signal.mass * 1e-12)
        connection = model.alkalinity_signal_connection
        self.assertIs(connection.source.sp, model.TA)
        self.assertIs(connection.sink, model.L_b.TA)
        self.assertIsNot(connection.sink, model.L_b.DIC)


if __name__ == "__main__":
    unittest.main()
