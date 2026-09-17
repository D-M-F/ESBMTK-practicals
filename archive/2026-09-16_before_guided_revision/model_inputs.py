"""Translate the 03/04 workbook into a validated model definition.

Named tables retain explicit benchmark area/volume. There is no area_percentage
input or hypsometry conversion. Object creation uses the standard ESBMTK
initialize_reservoirs/create_bulk_connections/Species2Species interfaces.
"""

from __future__ import annotations

import math
import re

from reservoir_inputs import (
    DEFAULT_RESERVOIR_WORKBOOK, BOX_ORDER, _read_tables, _number,
    read_reservoir_tables, load_reservoir_inputs,
)


TABLES = {
    'BoundaryNodes': ('Reservoirs', ('Box ID', 'Type', 'Species', 'Role')),
    'TransportConnections': ('Transport', ('Order', 'source', 'sink', 'flux_id', 'Parameter', 'Species')),
    'GasExchangeConnections': ('GasExchange', ('Order', 'Atmosphere', 'Surface', 'Species', 'Parameter')),
    'ProcessParameters': ('Parameters', ('Parameter', 'Value', 'Unit', 'Role', 'Description')),
}
# Schema and physical bounds only: numerical defaults live in Excel.
PARAMETERS = {
    'thc': ('Sverdrup', 0, None),
    'mixing': ('Sverdrup', 0, None),
    'poc_export': ('Tmol/yr', 0, None),
    'rain_ratio': ('1', 0, None),
    'weathering_dic': ('Tmol/yr', 0, None),
    'alpha': ('1', 0, 1),
    'z0': ('m', -11000, 0),
    'piston_velocity': ('m/d', 0, None),
    'opt_k_carbonic': ('1', 1, 18),
    'opt_pH_scale': ('1', 1, 4),
    'soft_reference': ('ppm', 0, None),
    'soft_half_saturation': ('ppm', 0, None),
    'soft_exponent': ('1', 0, None),
    'carbonate_reference': ('umol/kg', 0, None),
    'carbonate_half_saturation': ('umol/kg', 0, None),
    'carbonate_exponent': ('1', 0, None),
}


def read_model_tables(path=DEFAULT_RESERVOIR_WORKBOOK):
    """Return all user-facing input tables for notebook display."""
    return {**read_reservoir_tables(path), **_read_tables(path, TABLES)}


def _ordered(rows, name):
    orders = []
    for row in rows:
        value = _number({'Box ID': name, 'Order': row['Order']}, 'Order', positive=True)
        if value != int(value):
            raise ValueError(f'{name}: Order must be a positive integer')
        orders.append(value)
    if len(orders) != len(set(orders)):
        raise ValueError(f'{name}: duplicate Order values')
    return sorted(rows, key=lambda row: row['Order'])


def load_model_inputs(path=DEFAULT_RESERVOIR_WORKBOOK):
    """Read independent settings and derive linked PIC and weathering TA rates."""
    p = load_reservoir_inputs(path)
    tables = _read_tables(path, TABLES)
    rows = tables['ProcessParameters']
    names = [row['Parameter'] for row in rows]
    if len(names) != len(PARAMETERS) or set(names) != set(PARAMETERS):
        raise ValueError('ProcessParameters must contain each documented parameter exactly once')
    for row in rows:
        key = row['Parameter']
        unit, minimum, maximum = PARAMETERS[key]
        if row['Unit'] != unit:
            raise ValueError(f'{key}: expected unit {unit!r}')
        value = _number({'Box ID': key, 'Value': row['Value']}, 'Value',
                        minimum=minimum, maximum=maximum)
        if key.startswith(('soft_', 'carbonate_')) and value == 0:
            raise ValueError(f'{key}: feedback normalization values must be positive')
        if key in ('opt_k_carbonic', 'opt_pH_scale'):
            if value != int(value):
                raise ValueError(f'{key}: use an integer option')
            p[key] = int(value)
        elif unit == '1' or key == 'z0':
            p[key] = value
        else:
            p[key] = f'{value:.17g} {unit}'
    from esbmtk import Q_
    p['pic_export'] = f"{Q_(p['poc_export']).magnitude * p['rain_ratio']:.17g} Tmol/yr"
    # Carbonate weathering contributes 1 DIC : 2 TA. These are linked amounts.
    p['weathering_ta'] = f"{2 * Q_(p['weathering_dic']).magnitude:.17g} Tmol/yr"
    p['pump_feedbacks'] = {}
    for name, prefix, driver in (
        ('soft_tissue', 'soft', 'atmospheric_pco2'),
        ('carbonate', 'carbonate', 'ta_minus_dic'),
    ):
        p['pump_feedbacks'][name] = {
            'enabled': False, 'driver': driver,
            'reference': p.pop(f'{prefix}_reference'),
            'half_saturation': p.pop(f'{prefix}_half_saturation'),
            'exponent': p.pop(f'{prefix}_exponent'),
        }
    p['pump_strengths'] = {'solubility': 1.0, 'soft_tissue': 1.0, 'carbonate': 1.0}
    p['name'] = 'Boudreau et al. (2010) preindustrial reference'

    nodes = tables['BoundaryNodes']
    if len(nodes) != 2 or {row['Box ID'] for row in nodes} != {'Fw', 'Fb'}:
        raise ValueError('BoundaryNodes requires Fw and Fb exactly once')
    by_id = {row['Box ID']: row for row in nodes}
    p['boundary_nodes'] = []
    for name, kind in (('Fw', 'Source'), ('Fb', 'Sink')):
        row = by_id[name]
        if row['Type'] != kind or row['Species'] != 'DIC, TA':
            raise ValueError(f'{name}: expected {kind} with DIC, TA')
        p['boundary_nodes'].append({'name': name, 'type': kind, 'species': ('DIC', 'TA')})

    p['transport_connections'] = []
    seen = set()
    for row in _ordered(tables['TransportConnections'], 'TransportConnections'):
        source, sink, flux_id, key = (row[k] for k in ('source', 'sink', 'flux_id', 'Parameter'))
        if source not in BOX_ORDER or sink not in BOX_ORDER or source == sink:
            raise ValueError('Transport: source and sink must be distinct ocean box IDs')
        if not isinstance(flux_id, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', flux_id):
            raise ValueError('Transport: flux_id must be a simple identifier')
        if key not in ('thc', 'mixing') or row['Species'] != 'DIC, TA':
            raise ValueError('Transport: use thc/mixing and carry both DIC, TA')
        identity = (source, sink, flux_id)
        if identity in seen:
            raise ValueError(f'Duplicate transport connection: {identity}')
        seen.add(identity)
        p['transport_connections'].append({
            'source': source, 'sink': sink, 'id': flux_id, 'parameter': key,
        })
    validate_transport_balance(p)

    p['gas_exchange_connections'] = []
    rows = _ordered(tables['GasExchangeConnections'], 'GasExchangeConnections')
    if len(rows) != 2 or {row['Surface'] for row in rows} != {'H_b', 'L_b'}:
        raise ValueError('GasExchange requires both surface boxes exactly once')
    for row in rows:
        if (row['Atmosphere'], row['Species'], row['Parameter']) != ('CO2_At', 'CO2', 'piston_velocity'):
            raise ValueError('GasExchange: use CO2_At, CO2 and piston_velocity')
        p['gas_exchange_connections'].append({
            'atmosphere': row['Atmosphere'], 'surface': row['Surface'],
            'species': row['Species'], 'parameter': row['Parameter'],
        })
    return p


def validate_transport_balance(params):
    """Check that each fixed-volume ocean box gains and loses equal water."""
    from esbmtk import Q_
    balance = dict.fromkeys(BOX_ORDER, 0.0)
    total = 0.0
    if not params['transport_connections']:
        raise ValueError('TransportConnections cannot be empty')
    for row in params['transport_connections']:
        rate = Q_(params[row['parameter']]).to('Sverdrup').magnitude
        if not math.isfinite(rate) or rate < 0:
            raise ValueError('Transport rates must be finite and non-negative')
        balance[row['source']] -= rate
        balance[row['sink']] += rate
        total += rate
    if any(abs(value) > max(total, 1.0) * 1e-12 for value in balance.values()):
        raise ValueError(f'Transport does not conserve water in each box (Sv): {balance}')


def transport_specification(params, species_list):
    """Map each directed workbook row to the documented ESBMTK dictionary."""
    validate_transport_balance(params)
    return {
        f"{row['source']}_to_{row['sink']}@{row['id']}": {
            'ty': 'scale_with_concentration',
            'sc': params[row['parameter']], 'sp': species_list,
        }
        for row in params['transport_connections']
    }
