"""Supplied atmosphere-ocean inventory audit for the complete classroom model.

The active boundary excludes sediment carbon: weathering enters and net burial
leaves. Negative net burial represents return from pre-existing sediment.
All inventories use the water masses in ESBMTK's concentration equations.
"""

import numpy as np
from scipy.integrate import cumulative_trapezoid
from esbmtk import Q_, carbonate_system_2

from simple_models import box_mass_kg


def integrate_forcing_history(time, flux, evaluation_time):
    """Integrate a piecewise-linear history within its sampled time interval.

    Unlike 02's finite-pulse helper, this allows a nonzero boundary flux. It
    never assumes a zero tail or extrapolates outside the supplied history.
    """
    time, flux, t = map(lambda x: np.asarray(x, dtype=float),
                        (time, flux, evaluation_time))
    if (time.ndim != 1 or len(time) < 2 or flux.shape != time.shape
            or not np.all(np.isfinite(time)) or not np.all(np.isfinite(flux))
            or np.any(np.diff(time) <= 0)):
        raise ValueError("forcing requires finite matching arrays on an increasing grid")
    if not np.all(np.isfinite(t)) or np.any(t < time[0]) or np.any(t > time[-1]):
        raise ValueError("evaluation time must lie within the forcing history")
    cumulative = cumulative_trapezoid(flux, time, initial=0)
    i = np.clip(np.searchsorted(time, t, side="right") - 1, 0, len(time) - 2)
    dt = t - time[i]
    slope = (flux[i + 1] - flux[i]) / (time[i + 1] - time[i])
    return cumulative[i] + flux[i] * dt + 0.5 * slope * dt**2


def solver_carbonate_fluxes(model):
    """Re-evaluate the benchmark's actual dissolution law at saved states.

    Native plotting post-processing uses the stored H+ directly, whereas the
    ODE first updates H+ through get_hplus and applies its carbonate floor.
    Reusing the ODE function avoids treating that display approximation as a
    mass-balance defect. This helper is for the non-isotopic teaching model.
    """
    deep = model.D_b
    if deep.cs2.function_params[0][-1]:
        raise ValueError("classroom inventory audit expects a non-isotopic model")
    returned = np.array([
        carbonate_system_2(export, dic, ta, surface_dic, hplus, snow,
                           deep.cs2.function_params)
        for export, dic, ta, surface_dic, hplus, snow in zip(
            deep.CaCO3_export.c, deep.DIC.c, deep.TA.c,
            model.L_b.DIC.c, deep.Hplus.c, deep.zsnow.c,
        )
    ])
    np.testing.assert_allclose(returned[:, 1], 2 * returned[:, 0], rtol=0, atol=0)
    dissolution = returned[:, 0]
    return dissolution, deep.CaCO3_export.c - dissolution


def audit_complete_model(model, forcing="control", *, rtol=2e-5, atol_mol=1e6):
    """Check time-resolved C/TA budgets, with error normalized to initial stock.

    Call after integration and carbonate post-processing. The saved native signal
    grid is integrated exactly as a piecewise-linear forcing. Net burial is
    evaluated with the solver's own law on the output grid and integrated with
    the trapezoidal rule. The tolerance includes that diagnostic quadrature,
    not only solver error.
    """
    if forcing not in {"control", "OA", "OAE"}:
        raise ValueError(forcing)
    time = np.asarray(model.time)
    carbon = model.CO2_At.c * model.CO2_At.reservoir_mass.to("mol").magnitude
    ta = np.zeros_like(carbon)
    for box in (model.L_b, model.H_b, model.D_b):
        mass = box_mass_kg(box)
        carbon = carbon + mass * box.DIC.c
        ta = ta + mass * box.TA.c

    p = model.tutorial_params
    weathering_c = Q_(p["weathering_dic"]).to("mol/yr").magnitude * model.weathering_strength
    weathering_ta = Q_(p["weathering_ta"]).to("mol/yr").magnitude * model.weathering_strength
    elapsed = time - time[0]
    _, net_burial_flux = solver_carbonate_fluxes(model)
    burial = cumulative_trapezoid(net_burial_flux, time, initial=0)
    added = np.zeros_like(time)
    if forcing != "control":
        added = integrate_forcing_history(model.teaching_signal_time,
                                          model.teaching_signal_flux, time)
        added -= added[0]
    expected_carbon = carbon[0] + weathering_c * elapsed - burial
    expected_ta = ta[0] + weathering_ta * elapsed - 2 * burial
    if forcing == "OA":
        expected_carbon += added
    elif forcing == "OAE":
        expected_ta += added

    carbon_error = np.max(np.abs(carbon - expected_carbon)) / abs(carbon[0])
    ta_error = np.max(np.abs(ta - expected_ta)) / abs(ta[0])
    np.testing.assert_allclose(carbon, expected_carbon, rtol=rtol, atol=atol_mol)
    np.testing.assert_allclose(ta, expected_ta, rtol=rtol, atol=atol_mol)
    np.testing.assert_allclose(model.D_b.CaCO3_export.c,
                               model.D_b.Fdiss.c + model.D_b.Fburial.c,
                               rtol=0, atol=1e-6)
    pic_dic = next(c for c in model.loc if c.id == "PIC_DIC")
    pic_ta = next(c for c in model.loc if c.id == "PIC_TA")
    assert pic_ta.rate == 2 * pic_dic.rate
    return {"max carbon error / initial stock": float(carbon_error),
            "max TA error / initial stock": float(ta_error),
            "external input (Pmol C or TA eq)": float(added[-1] / 1e15)}


def audit_restart_drift(model, *, concentration_tolerance=0.01,
                        atmosphere_tolerance=0.01, snowline_tolerance=0.01):
    """Check all saved states of the short (<=20 yr) teaching restart.

    Absolute limits are in umol/kg (TA: ueq/kg), ppm, and metres. They are
    teaching acceptance tolerances, not evidence of asymptotic stability.
    Checking the full trace detects excursions hidden by an endpoint-only test.
    """
    if len(model.time) < 2 or not 0 < model.time[-1] - model.time[0] <= 20.000001:
        raise ValueError('restart drift check requires a positive run of at most 20 model years')
    series = [('atm CO2', model.CO2_At.c, 1e6, 'ppm', atmosphere_tolerance)]
    for box in (model.L_b, model.H_b, model.D_b):
        for species, unit in (('DIC', 'umol/kg'), ('TA', 'ueq/kg')):
            series.append((f'{box.name} {species}', getattr(box, species).c,
                           1e6, unit, concentration_tolerance))
    series.append(('sediment snowline', model.D_b.zsnow.c, 1., 'm', snowline_tolerance))
    rows = []
    for name, values, scale, unit, tolerance in series:
        values = np.asarray(values, dtype=float)
        if not np.isfinite(tolerance) or tolerance <= 0:
            raise ValueError('restart tolerances must be finite and positive')
        if values.shape != np.asarray(model.time).shape or not np.isfinite(values).all():
            raise AssertionError(f'{name}: invalid restart trace')
        drift = float(np.max(np.abs(values - values[0])) * scale)
        if drift > tolerance:
            raise AssertionError(f'{name}: restart drift {drift:g} {unit} exceeds {tolerance:g}')
        rows.append({'State': name, 'Maximum drift': drift, 'Tolerance': tolerance, 'Unit': unit})
    return rows


def audit_benchmark_graph(model):
    """Match every native connection to workbook topology and process metadata.

    This verifies structure separately from inventory conservation; a reversed
    conservative transfer would fail here. Carbonate sink bypass and module
    coupling are checked by the notebook and reference-trajectory comparison.
    """
    p = model.tutorial_params
    expected = []
    for r in p['transport_connections']:
        for sp in ('DIC', 'TA'):
            expected.append((r['id'], f"{r['source']}.{sp}",
                             f"{r['sink']}.{sp}", 'scale_with_concentration'))
    expected += [
        ('POM', 'L_b.DIC', 'D_b.DIC', 'regular'),
        ('PIC_DIC', 'L_b.DIC', 'D_b.DIC', 'regular'),
        ('PIC_TA', 'L_b.TA', 'D_b.TA', 'regular'),
        ('weathering', 'Fw.DIC', 'L_b.DIC', 'regular'),
        ('weathering', 'Fw.TA', 'L_b.TA', 'regular'),
    ]
    expected += [(r['surface'], r['atmosphere'], f"{r['surface']}.DIC", 'gasexchange')
                 for r in p['gas_exchange_connections']]
    # Only strip the shared model prefix; retain the species part of each name.
    prefix = model.name + '.'
    actual = [(c.id, c.source.full_name.removeprefix(prefix),
               c.sink.full_name.removeprefix(prefix), c.ctype) for c in model.loc]
    if sorted(actual) != sorted(expected):
        raise AssertionError('constructed connections differ from the workbook/process specification')
    for ident, parameter, factor in (('POM', 'poc_export', 1),
                                      ('PIC_DIC', 'pic_export', 1),
                                      ('PIC_TA', 'pic_export', 2)):
        connection = next(c for c in model.loc if c.id == ident)
        # Native connections store numeric rates in the model's mol/yr units.
        np.testing.assert_allclose(connection.rate,
                                   factor * Q_(p[parameter]).to('mol/yr').magnitude,
                                   rtol=1e-12, atol=0)
    return [dict(zip(('ID', 'Source', 'Sink', 'Law'), row)) for row in sorted(actual)]
