"""Scientific checks for the supplied surface/contour/slice representation."""
import unittest

import numpy as np
import PyCO2SYS as pyco2

from teaching_carbonate import carbonate_explorer_data, carbonate_explorer_html, show_carbonate_explorer
from teaching_config import TEACHING as config


class CarbonateExplorerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ta = float(config.reference_state()['alkalinity'])
        cls.data = carbonate_explorer_data(config, cls.ta)

    def test_slices_and_reference_use_shared_chemistry(self):
        for name, sample in self.data['ranges'].items():
            with self.subTest(range=name):
                i, j = sample['dic_index'], sample['ta_index']
                self.assertEqual(sample['dic'][i], config.target_dic_umol_kg)
                self.assertEqual(sample['ta'][j], self.ta)
                direct = pyco2.sys(par1=sample['dic'], par1_type=2, par2=self.ta,
                                   par2_type=1, **config.pyco2)['pCO2']
                np.testing.assert_allclose(sample['pco2'][j], direct, rtol=1e-12)
                # The closed-inventory atm and inferred seawater intersect at
                # the fitted reference, in pCO2 rather than dry-air ppm.
                self.assertAlmostEqual(sample['atmosphere'][i], direct[i], places=7)
                self.assertLess(direct[i], config.target_xco2_ppm)

    def test_local_sensitivity_matches_an_independent_perturbation(self):
        sample = self.data['ranges']['local']
        i, j = sample['dic_index'], sample['ta_index']
        values = pyco2.sys(par1=np.array([2039.9, 2040.1]), par1_type=2,
                           par2=self.ta, par2_type=1, **config.pyco2)['pCO2']
        self.assertAlmostEqual(sample['slope'][j][i], (values[1]-values[0])/.2, places=5)

    def test_contour_vertices_represent_their_labelled_pco2(self):
        sample = self.data['ranges']['local']
        for line in sample['contours']:
            for points in line['paths']:
                xy = np.asarray(points)[::10]
                direct = pyco2.sys(par1=xy[:,0], par1_type=2, par2=xy[:,1],
                                   par2_type=1, **config.pyco2)['pCO2']
                # Isolines interpolate a 2.5 DIC by 5 TA mesh, not exact roots.
                np.testing.assert_allclose(direct, line['value'], rtol=.003)

    def test_ranges_separate_ta_free_states_and_omit_negative_atmosphere(self):
        local, full = (self.data['ranges'][name] for name in ('local','full'))
        self.assertGreater(min(local['ta']), 0)
        self.assertEqual(min(full['ta']), 0)
        self.assertTrue(any(v is None for v in local['atmosphere']))
        self.assertTrue(all(v is not None and v >= 0 for v in full['atmosphere']))
        for dic, value in zip(local['dic'], local['atmosphere']):
            self.assertEqual(value is None, dic > self.data['maximum_dic'])

    def test_html_runs_without_remote_assets_or_new_extensions(self):
        page = carbonate_explorer_html(config, self.ta)
        self.assertNotIn('__CARBONATE_DATA__', page)
        self.assertNotIn('<script src=', page)
        self.assertNotIn('https://', page)
        self.assertNotIn('NaN', page)
        self.assertIn('application/json', page)
        frame = show_carbonate_explorer(config, self.ta)._repr_html_()
        self.assertIn('sandbox="allow-scripts allow-downloads"', frame)
        self.assertIn('srcdoc=', frame)


if __name__ == '__main__':
    unittest.main()
