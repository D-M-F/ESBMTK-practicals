"""Full workbook wiring, linked fluxes and conservative transport checks."""

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import unittest

import numpy as np
from esbmtk import Q_

from model import initialize_model, run_model
from model_inputs import load_model_inputs, read_model_tables, transport_specification
from presets import load_boudreau_parameters, make_process_variant
from reservoir_inputs import DEFAULT_RESERVOIR_WORKBOOK, reservoir_inventory_rows


class FullModelWorkbookTest(unittest.TestCase):
    def test_named_tables_and_baseline_process_values(self):
        tables = read_model_tables()
        self.assertEqual(set(tables), {'OceanReservoirs', 'Atmosphere', 'BoundaryNodes',
                                     'TransportConnections', 'GasExchangeConnections', 'ProcessParameters'})
        p = load_model_inputs()
        for name, unit, expected in (
            ('thc', 'Sverdrup', 25), ('mixing', 'Sverdrup', 30),
            ('poc_export', 'Tmol/yr', 200), ('pic_export', 'Tmol/yr', 60),
            ('weathering_dic', 'Tmol/yr', 12), ('weathering_ta', 'Tmol/yr', 24),
            ('piston_velocity', 'm/d', 4.8),
        ):
            self.assertAlmostEqual(Q_(p[name]).to(unit).magnitude, expected)
        self.assertEqual(p['opt_k_carbonic'], 13)
        self.assertEqual(p['opt_pH_scale'], 3)
        self.assertEqual(p['z0'], -200)
        self.assertEqual(p['alpha'], 0.6)
        self.assertEqual(len(p['transport_connections']), 5)
        self.assertEqual(len(p['gas_exchange_connections']), 2)

    def test_excel_parameter_edits_reach_fluxes_and_chemistry(self):
        # Modify real numeric XML cells in a disposable workbook. Do not rely
        # on cached formula outputs: the loader derives PIC and weathering TA.
        values = {'C7': 20, 'C9': 150, 'C10': 0.4, 'C11': 10,
                  'C14': 3.5, 'C15': 10, 'C17': 275}
        ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        with TemporaryDirectory() as directory:
            file = Path(directory) / 'edited.xlsx'
            with ZipFile(DEFAULT_RESERVOIR_WORKBOOK) as src, ZipFile(file, 'w') as dst:
                for item in src.infolist():
                    data = src.read(item.filename)
                    if item.filename == 'xl/worksheets/sheet4.xml':
                        sheet = ET.fromstring(data)
                        for address, value in values.items():
                            cell = sheet.find(f".//s:c[@r='{address}']/s:v", ns)
                            self.assertIsNotNone(cell)
                            cell.text = str(value)
                        data = ET.tostring(sheet, encoding='utf-8')
                    dst.writestr(item, data)
            p = load_boudreau_parameters(file)
            self.assertAlmostEqual(Q_(p['weathering_ta']).magnitude, 20)
            self.assertAlmostEqual(Q_(p['pump_feedbacks']['soft_tissue']['reference']).magnitude, 275)
            m = initialize_model(p, stop='1 yr', max_timestep='1 yr')
            self.assertAlmostEqual(m.OM_export.to('Tmol/yr').magnitude, 150)
            self.assertAlmostEqual(m.CaCO3_export.to('Tmol/yr').magnitude, 60)
            self.assertEqual(m.opt_k_carbonic, 10)
            for conn in m.loc:
                if conn.ctype == 'gasexchange':
                    self.assertAlmostEqual(Q_(conn.piston_velocity).to('m/d').magnitude, 3.5)
            specs = transport_specification(p, [m.DIC, m.TA])
            self.assertAlmostEqual(Q_(specs['L_b_to_H_b@thc']['sc']).to('Sverdrup').magnitude, 20)

    def test_invalid_topology_units_and_incomplete_definitions_fail(self):
        cases = [
            ('TransportConnections', 0, 'sink', 'missing', 'distinct ocean'),
            ('TransportConnections', 0, 'sink', 'L_b', 'conserve water'),
            ('TransportConnections', 0, 'Species', 'DIC', 'both DIC'),
            ('TransportConnections', 1, 'Order', 1, 'duplicate Order'),
            ('TransportConnections', 0, 'Parameter', 'bogus', 'thc/mixing'),
            ('GasExchangeConnections', 0, 'Surface', 'D_b', 'both surface'),
            ('BoundaryNodes', 0, 'Type', 'Sink', 'expected Source'),
            ('ProcessParameters', 0, 'Unit', 'm3/s', 'expected unit'),
            ('ProcessParameters', 0, 'Value', None, 'finite number'),
            ('ProcessParameters', 9, 'Value', 2.5, 'integer option'),
        ]
        for name, index, key, value, message in cases:
            with self.subTest(table=name, field=key, value=value):
                tables = read_model_tables()
                tables[name][index][key] = value
                with patch('model_inputs._read_tables', return_value=tables):
                    with self.assertRaisesRegex(ValueError, message):
                        load_model_inputs()

    def test_sorting_preserves_equation_order_and_connections_are_not_duplicated(self):
        original = load_model_inputs()
        tables = read_model_tables()
        for rows in tables.values():
            rows.reverse()
        with patch('model_inputs._read_tables', return_value=tables):
            actual = load_model_inputs()
        self.assertEqual(actual, original)
        tables = read_model_tables()
        extra = deepcopy(tables['TransportConnections'][0])
        extra['Order'] = 6
        tables['TransportConnections'].append(extra)
        with patch('model_inputs._read_tables', return_value=tables):
            with self.assertRaisesRegex(ValueError, 'Duplicate transport'):
                load_model_inputs()

    def test_changed_transport_table_drives_conservative_model_and_tags(self):
        # Add a paired low-latitude/deep exchange: exercises editable topology,
        # actual ODE conservation and the diagnostic transport mapping together.
        tables = read_model_tables()
        tables['TransportConnections'].extend([
            {'Order': 6, 'source': 'L_b', 'sink': 'D_b', 'flux_id': 'extra_down',
             'Parameter': 'mixing', 'Species': 'DIC, TA'},
            {'Order': 7, 'source': 'D_b', 'sink': 'L_b', 'flux_id': 'extra_up',
             'Parameter': 'mixing', 'Species': 'DIC, TA'},
        ])
        with patch('model_inputs._read_tables', return_value=tables):
            p = make_process_variant(base=load_model_inputs())
        m = initialize_model(p, stop='100 yr', max_timestep='1 yr')
        run_model(m)
        self.assertEqual(sum(c.ctype == 'scale_with_concentration' for c in m.loc), 14)
        inventory = reservoir_inventory_rows(m)
        masses = {row['Box']: row['Water mass (kg)'] for row in inventory}
        carbon = m.CO2_At.c * m.CO2_At.v[0]
        ta = np.zeros_like(carbon)
        for name, mass in masses.items():
            carbon = carbon + mass * getattr(m, name).DIC.c
            ta += mass * getattr(m, name).TA.c
        np.testing.assert_allclose(carbon, carbon[0], rtol=2e-8)
        np.testing.assert_allclose(ta, ta[0], rtol=2e-8)
        for conn in m.loc:
            if conn.ctype != 'scale_with_concentration':
                continue
            a, b = conn.source, conn.sink
            self.assertAlmostEqual(m.CM[a.idx, conn.fh.idx] * masses[a.parent.name]
                                   + m.CM[b.idx, conn.fh.idx] * masses[b.parent.name], 0, places=12)
        from storage_decomposition import decompose_dic_storage
        tags = decompose_dic_storage(m)
        np.testing.assert_allclose(tags.reconstructed_dic_umol_kg, tags.model_dic_umol_kg,
                                   rtol=0, atol=0.2)


if __name__ == '__main__':
    unittest.main()
