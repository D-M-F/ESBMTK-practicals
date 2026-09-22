"""Conservation, structural equivalence and conditional forcing checks for 01/02."""

from dataclasses import replace
import unittest

import numpy as np

from model import run_model
from scenarios import add_carbon_signal
from simple_models import (
    audit, box_mass_kg, calibrated_pump_coefficient, finite_box_addition,
    finite_pulse_clock, integrated_signal, inventories, mixing_mass_transport,
    new_model, single_box, two_layer,
)
from teaching_config import TEACHING as C
from teaching_plots import equilibration_time


class IntroductoryModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ta = float(C.reference_state()["alkalinity"])
        cls.zero = run_model(single_box())
        cls.buffered = run_model(single_box(ta_umol_kg=cls.ta))
        cls.partition = run_model(single_box(ta_umol_kg=cls.ta, initial_dic_umol_kg=1000))
        cls.slow = run_model(single_box(ta_umol_kg=cls.ta, piston_velocity="2 m/d"))
        cls.layers = run_model(two_layer())
        cls.k = calibrated_pump_coefficient()
        cls.pump = run_model(two_layer(k_kg_yr=cls.k))

    def test_ta_free_failure_is_chemical_not_loss_of_carbon(self):
        audit(self.zero)
        self.assertGreater(self.zero.CO2_At.c[-1] * 1e6, 10000)
        self.assertLess(self.zero.Ocean.DIC.c[-1] * 1e6, 1000)
        np.testing.assert_allclose(self.zero.Ocean.TA.c, 0, atol=1e-20)
        fraction = box_mass_kg(self.zero.Ocean) * self.zero.Ocean.DIC.c[0] / C.total_carbon_mol
        self.assertLess(fraction, 1e-5)

    def test_geometry_chemistry_and_implemented_ode_mass(self):
        self.assertAlmostEqual(C.surface_volume_m3 / C.ocean_area_m2, C.surface_depth_m)
        self.assertGreater(C.surface_depth_m, 0)
        self.assertLess(C.surface_depth_m, C.ocean_depth_m)
        self.assertEqual(C.surface_volume_m3 + C.deep_volume_m3, C.ocean_volume_m3)
        for model in (self.zero, self.buffered, self.layers):
            for name, value in C.chemistry.items():
                self.assertEqual(getattr(model, name), value)
            for box in model.ocean_boxes:
                self.assertEqual(box.swc.temperature, C.temperature)
                self.assertEqual(box.swc.salinity, C.salinity)
                self.assertEqual(box.swc.pressure, C.pressure_bar)
                self.assertAlmostEqual(box.swc.density, C.density_kg_m3)
                # Inspect an actual flux coefficient, independently of the
                # inventory helper, to catch volume/mass conversion mistakes.
                nonzero = model.CM[box.DIC.idx]
                nonzero = nonzero[nonzero != 0]
                np.testing.assert_allclose(abs(nonzero), 1 / box_mass_kg(box), rtol=1e-12)
        self.assertEqual(replace(C, pressure_bar=10).pyco2["pressure"], 100)

    def test_equilibrium_is_independent_of_partition_and_piston_velocity(self):
        for model in (self.buffered, self.partition, self.slow):
            audit(model)
            np.testing.assert_allclose(model.CO2_At.c[-1] * 1e6, 280, atol=0.5)
            np.testing.assert_allclose(model.Ocean.DIC.c[-1] * 1e6, 2040, atol=0.2)
        self.assertGreater(equilibration_time(self.slow), equilibration_time(self.buffered))
        self.assertNotEqual(self.partition.CO2_At.c[0], self.buffered.CO2_At.c[0])

    def test_no_pump_extension_preserves_equilibrium_and_both_inventories(self):
        audit(self.layers)
        for box in self.layers.ocean_boxes:
            np.testing.assert_allclose(box.DIC.c[-1], self.buffered.Ocean.DIC.c[-1], atol=0.2e-6)
        np.testing.assert_allclose(self.layers.CO2_At.c[-1], self.buffered.CO2_At.c[-1], atol=0.5e-6)
        np.testing.assert_allclose(inventories(self.layers)[0][0], C.total_carbon_mol, rtol=1e-12)

    def test_internal_mixing_and_pump_have_equal_opposite_inventory_tendencies(self):
        m = self.pump
        # Every transport column sums to zero after restoring reservoir mass.
        rows = [(b.DIC.idx, box_mass_kg(b)) for b in m.ocean_boxes]
        rows += [(b.TA.idx, box_mass_kg(b)) for b in m.ocean_boxes]
        for connection in m.loc:
            if connection.ctype != "scale_with_concentration":
                continue
            column = m.CM[:, connection.fh.idx]
            tendency = sum(column[i] * mass for i, mass in rows)
            self.assertAlmostEqual(tendency, 0, places=12)
        self.assertIs(m.effective_pump.source, m.Surface.DIC)
        self.assertIs(m.effective_pump.sink, m.Deep.DIC)

    def test_calibrated_ratio_and_conditional_atmosphere(self):
        audit(self.pump)
        s, d = self.pump.Surface.DIC.c[-1], self.pump.Deep.DIC.c[-1]
        self.assertAlmostEqual(d / s, C.target_deep_dic_umol_kg / C.target_dic_umol_kg, places=5)
        np.testing.assert_allclose(mixing_mass_transport() * (d - s), self.k * s, rtol=1e-5)
        self.assertLess(self.pump.CO2_At.c[-1], self.layers.CO2_At.c[-1])
        # Absolute fitted DIC values do not hold at the original total carbon.
        self.assertLess(s * 1e6, C.target_dic_umol_kg)

    def test_finite_signal_inventory_and_calibrated_return(self):
        state = {b.name: (b.DIC.c[-1] * 1e6, b.TA.c[-1] * 1e6)
                 for b in self.pump.ocean_boxes}
        forced = two_layer(k_kg_yr=self.k, state=state)
        control = two_layer(k_kg_yr=self.k, state=state)
        # Students derive the input from 62.4 and the actual 01 inventory;
        # compare with the independent finite-box expression before forcing.
        atmosphere_reference = C.atmosphere_mol * C.target_xco2_ppm * 1e-6
        amount = (1 + C.pumped_ocean_atmosphere_ratio) * atmosphere_reference - C.total_carbon_mol
        np.testing.assert_allclose(amount, finite_box_addition(), rtol=1e-12)
        signal = add_carbon_signal(forced, start="1000 yr", duration="1000 yr",
                                   mass=f"{amount} mol", shape="square")
        time, flux = forced.time.copy(), signal.m.copy()
        self.assertAlmostEqual(flux.sum() * forced.dt / amount, 1, places=12)
        self.assertAlmostEqual(float(integrated_signal(time, flux, time[-1])) / amount, 1, places=12)
        run_model(control)
        run_model(forced)
        added = integrated_signal(time, flux, forced.time)
        audit(control)
        audit(forced, added)
        np.testing.assert_allclose(forced.CO2_At.c[-1] * 1e6, 280, atol=0.5)
        np.testing.assert_allclose(forced.Surface.DIC.c[-1] * 1e6, 2040, atol=0.2)
        np.testing.assert_allclose(forced.Deep.DIC.c[-1] * 1e6, 2250, atol=0.2)
        np.testing.assert_allclose(control.CO2_At.c[-1], self.pump.CO2_At.c[-1], atol=0.5e-6)
        carbon, _ = inventories(forced)
        control_carbon, _ = inventories(control)
        np.testing.assert_allclose(carbon - control_carbon, added, rtol=2e-5,
                                   atol=C.total_carbon_mol * 2e-6)

    def test_transport_identifiability_and_ratio_derived_geometry(self):
        stronger_mixing = replace(C, mixing_sv=40)
        self.assertAlmostEqual(calibrated_pump_coefficient(stronger_mixing) / self.k, 2)
        self.assertEqual(stronger_mixing.total_carbon_mol, C.total_carbon_mol)
        for config in (C, replace(C, pumped_ocean_atmosphere_ratio=62.0),
                       replace(C, atmosphere_mol=C.atmosphere_mol * 1.005)):
            reference_ocean = config.density_kg_m3 * (
                config.surface_volume_m3 * config.target_dic_umol_kg
                + config.deep_volume_m3 * config.target_deep_dic_umol_kg) * 1e-6
            reference_air = config.atmosphere_mol * config.target_xco2_ppm * 1e-6
            self.assertAlmostEqual(reference_ocean / reference_air,
                                   config.pumped_ocean_atmosphere_ratio, places=12)
            original_ocean = config.ocean_volume_m3 * config.density_kg_m3 * config.target_dic_umol_kg * 1e-6
            np.testing.assert_allclose(config.total_carbon_mol,
                                       reference_air + original_ocean, rtol=1e-12)
        lower_ratio = replace(C, pumped_ocean_atmosphere_ratio=62.0)
        self.assertEqual(lower_ratio.total_carbon_mol, C.total_carbon_mol)
        self.assertGreater(lower_ratio.surface_depth_m, C.surface_depth_m)
        self.assertLess(finite_box_addition(lower_ratio), finite_box_addition())

    def test_changed_pulse_durations_preserve_mass_and_equilibrium(self):
        state = {b.name: (b.DIC.c[-1] * 1e6, b.TA.c[-1] * 1e6)
                 for b in self.pump.ocean_boxes}
        amount = finite_box_addition()
        for duration in ("100 yr", "333 yr", "5000 yr"):
            with self.subTest(duration=duration):
                clock = finite_pulse_clock(start="1000 yr", duration=duration)
                forced = two_layer(k_kg_yr=self.k, state=state, **clock)
                signal = add_carbon_signal(forced, start="1000 yr", duration=duration,
                                           mass=f"{amount} mol", shape="square")
                time, flux = forced.time.copy(), signal.m.copy()
                np.testing.assert_allclose(integrated_signal(time, flux, time[-1]),
                                           amount, rtol=1e-12)
                run_model(forced)
                audit(forced, integrated_signal(time, flux, forced.time))
                np.testing.assert_allclose(forced.CO2_At.c[-1] * 1e6, 280, atol=0.5)
                np.testing.assert_allclose(forced.Surface.DIC.c[-1] * 1e6, 2040, atol=0.2)
                np.testing.assert_allclose(forced.Deep.DIC.c[-1] * 1e6, 2250, atol=0.2)

    def test_impossible_inventory_ratios_reject_unphysical_geometry(self):
        for ratio in (1.0, 100.0):
            with self.assertRaises(ValueError):
                _ = replace(C, pumped_ocean_atmosphere_ratio=ratio).surface_depth_m


class SignalIntegralTest(unittest.TestCase):
    def test_resolved_clock_maps_native_square_pulses_without_losing_mass(self):
        from esbmtk import Q_, Signal

        for duration in ("100 yr", "333 yr", "1 kyr", "5000 yr"):
            with self.subTest(duration=duration):
                m = new_model(**finite_pulse_clock(start="1000 yr", duration=duration))
                signal = Signal(name="test_pulse", species=m.CO2, register=m,
                                start="1000 yr", duration=duration, mass="1 Pmol",
                                shape="square")
                self.assertGreaterEqual(Q_(duration).to("yr").magnitude / m.dt, 20)
                self.assertAlmostEqual(signal.m.sum() * m.dt / 1e15, 1, places=12)
                self.assertAlmostEqual(float(integrated_signal(m.time, signal.m,
                                                              m.time[-1])) / 1e15,
                                       1, places=12)

    def test_invalid_pulse_clock_has_actionable_errors(self):
        for start, duration in (("0 yr", "100 yr"), ("1000 yr", "0 yr"),
                                ("1000 yr", "-1 yr"), ("1000 yr", "0.5 yr"),
                                ("1000 yr", "29000 yr"), ("1000 yr", "40000 yr")):
            with self.subTest(start=start, duration=duration), self.assertRaises(ValueError):
                finite_pulse_clock(start=start, duration=duration)

    def test_integrates_within_sloping_segments_not_just_at_knots(self):
        # A triangular pulse has exact antiderivative t^2/2 on its first side.
        result = integrated_signal([0, 1, 2], [0, 1, 0], [-1, 0.5, 1, 1.5, 3])
        np.testing.assert_allclose(result, [0, 0.125, 0.5, 0.875, 1])


if __name__ == "__main__":
    unittest.main()
