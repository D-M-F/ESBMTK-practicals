"""Check nonzero forcing tails and boundary-aware inventory diagnostics."""
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch

import numpy as np
from esbmtk import Q_

from teaching_audits import integrate_forcing_history, audit_complete_model


class ForcingHistoryTest(unittest.TestCase):
    def test_nonzero_tail_and_interior_times_use_piecewise_linear_integral(self):
        # F(t)=2+3t has a nonzero value at both endpoints. Its integral is
        # 2t + 1.5t^2, also between sampled points and on a nonuniform grid.
        time = np.array([0.0, 0.25, 2.0, 4.0])
        points = np.array([0.0, 0.1, 1.25, 4.0])
        actual = integrate_forcing_history(time, 2 + 3 * time, points)
        np.testing.assert_allclose(actual, 2 * points + 1.5 * points**2)

    def test_no_silent_extrapolation(self):
        for t in (-0.1, 2.1, np.nan):
            with self.subTest(time=t), self.assertRaises(ValueError):
                integrate_forcing_history([0, 2], [1, 1], t)

    def test_post_start_inventory_excludes_only_the_earlier_integral(self):
        whole = integrate_forcing_history([0, 1, 2], [2, 2, 2], 2)
        before = integrate_forcing_history([0, 1, 2], [2, 2, 2], 1)
        self.assertEqual(whole, 4)
        self.assertEqual(whole - before, 2)


class BoundaryAuditTest(unittest.TestCase):
    @staticmethod
    def model(forcing):
        # Manufactured three-box budget: 3 mol/yr weathering, 1 mol/yr
        # net burial, and 4 mol/yr external input of the chosen species.
        time = np.array([0.0, 1.0, 2.0])
        dic = np.full(3, 10.0)
        ta = np.full(3, 20.0)

        def box():
            return NS(DIC=NS(c=dic.copy(), volume=Q_('1 m**3')),
                      TA=NS(c=ta.copy()), swc=NS(density=1.0))

        model = NS(time=time, L_b=box(), H_b=box(), D_b=box(),
                   CO2_At=NS(c=np.ones(3), reservoir_mass=Q_('1 mol')),
                   tutorial_params={'weathering_dic': '3 mol/yr',
                                    'weathering_ta': '6 mol/yr'},
                   weathering_strength=1.0,
                   teaching_signal_time=time,
                   teaching_signal_flux=np.full(3, 4.0),
                   loc=[NS(id='PIC_DIC', rate=Q_('5 mol/yr')),
                        NS(id='PIC_TA', rate=Q_('10 mol/yr'))])
        model.L_b.DIC.c += 2 * time
        model.L_b.TA.c += 4 * time
        if forcing == 'OA':
            model.CO2_At.c += 4 * time
        elif forcing == 'OAE':
            model.L_b.TA.c += 4 * time
        model.D_b.Fburial = NS(c=np.ones(3))
        model.D_b.Fdiss = NS(c=np.full(3, 4.0))
        model.D_b.CaCO3_export = NS(c=np.full(3, 5.0))
        return model

    def test_weathering_burial_and_external_species_close(self):
        for forcing in ('control', 'OA', 'OAE'):
            with self.subTest(forcing=forcing):
                model = self.model(forcing)
                with patch('teaching_audits.solver_carbonate_fluxes',
                           return_value=(model.D_b.Fdiss.c, model.D_b.Fburial.c)):
                    result = audit_complete_model(model, forcing, atol_mol=0)
                self.assertEqual(result['max carbon error / initial stock'], 0)
                self.assertEqual(result['max TA error / initial stock'], 0)

    def test_rejects_wrong_external_species(self):
        model = self.model('OA')
        with patch('teaching_audits.solver_carbonate_fluxes',
                   return_value=(model.D_b.Fdiss.c, model.D_b.Fburial.c)), self.assertRaises(AssertionError):
            audit_complete_model(model, 'OAE', atol_mol=0)


if __name__ == '__main__':
    unittest.main()
