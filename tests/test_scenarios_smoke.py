"""Short end-to-end checks for the three tutorial forcing mechanisms."""

from __future__ import annotations

from pathlib import Path
from math import log10
import unittest

from model import initialize_model, run_model
from presets import BOUDREAU_2010
from scenarios import (
    add_alkalinity_signal,
    add_carbon_signal,
    add_flux_signal,
    connections_by_id,
)


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "Boudreau_2010" / "steady_state"


class ScenarioSmokeTest(unittest.TestCase):
    def model(self):
        model = initialize_model(BOUDREAU_2010, stop="100 yr", max_timestep="1 yr")
        model.read_state(directory=str(STATE))
        return model

    def test_carbon_signal_increases_atmospheric_carbon_and_lowers_ph(self):
        model = self.model()
        initial_pco2 = model.CO2_At.c[0]
        # pH is a derived post-run diagnostic; Hplus is part of the restart.
        initial_ph = -log10(model.L_b.Hplus.c[0])
        add_carbon_signal(
            model, duration="20 yr", mass="10 Pmol", shape="square"
        )
        run_model(model)
        self.assertGreater(model.CO2_At.c[-1], initial_pco2)
        self.assertLess(model.L_b.pH.c[-1], initial_ph)
        self.assertIs(model.carbon_signal_connection.sink, model.CO2_At)

    def test_alkalinity_signal_increases_target_ta_and_draws_down_co2(self):
        model = self.model()
        initial_ta = model.L_b.TA.c[0]
        initial_pco2 = model.CO2_At.c[0]
        add_alkalinity_signal(
            model,
            target=model.L_b.TA,
            duration="20 yr",
            mass="20 Pmol",
        )
        run_model(model)
        self.assertGreater(model.L_b.TA.c[-1], initial_ta)
        self.assertLess(model.CO2_At.c[-1], initial_pco2)
        self.assertIs(model.alkalinity_signal_connection.sink, model.L_b.TA)

    def test_flux_signal_modifies_only_requested_connections(self):
        model = self.model()
        pom_connections = connections_by_id(model, "POM")
        signals = add_flux_signal(
            model,
            pom_connections,
            factor=0.8,
            duration="100 yr",
            name="weaker_poc_export",
        )
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].stype, "multiplication")
        self.assertTrue(all(connection.signal in signals for connection in pom_connections))
        self.assertTrue(
            all(
                connection.signal == "None"
                for connection in model.loc
                if connection not in pom_connections
            )
        )
        run_model(model)
        self.assertNotEqual(model.D_b.DIC.c[-1], model.D_b.DIC.c[0])


if __name__ == "__main__":
    unittest.main()
