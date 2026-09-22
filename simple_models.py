"""Supplied construction and inventory helpers for practicals 01/02.

Student notebooks expose reservoir, mixing, pump and signal construction.
These helpers also provide independently executable model regression cases.
"""

import numpy as np

from teaching_config import TEACHING


def new_model(*, stop="30 kyr", max_timestep="20 yr", config=TEACHING):
    """Register species definitions and supply the model clock and units.

    Registering Carbon/Boron/Hydrogen/misc_variables does not create transported
    reservoirs. box_parameters supplies initial DIC/TA; seawater initialization
    obtains background boron and equilibrium constants through PyCO2SYS.
    add_carbonate_system_1 initializes and updates auxiliary Hplus and CO2aq.
    The miscellaneous sediment-variable definitions are unused in 01/02 and
    do not activate sediment processes.
    """
    from esbmtk import Model

    return Model(stop=stop, max_timestep=max_timestep,
                 element=["Carbon", "Boron", "Hydrogen", "misc_variables"],
                 mass_unit="mol", concentration_unit="mol/kg", rtol=1e-8,
                 **config.chemistry)


def box_parameters(model, volume_m3, dic_umol_kg, ta_umol_kg, config=TEACHING):
    return {"c": {model.DIC: f"{dic_umol_kg} umol/kg",
                  model.TA: f"{ta_umol_kg} umol/kg"},
            "g": {"area": f"{config.ocean_area_m2} m**2",
                  "volume": f"{volume_m3} m**3"},
            "T": config.temperature, "S": config.salinity,
            "P": config.pressure_bar}


def box_mass_kg(box):
    """Mass used by ESBMTK's ODE coefficient matrix (volume times density)."""
    return box.DIC.volume.to("m**3").magnitude * box.swc.density


def atmospheric_pco2_curve(dic_umol_kg, config=TEACHING):
    """Conserved-inventory atmosphere line for 01, in microatmospheres.

    DIC is in umol/kg. Use the same ocean mass and dry atmospheric inventory
    as the time-dependent model. PyCO2SYS converts dry xCO2 (ppm) to pCO2
    (uatm); this gas conversion neither requires nor infers ocean TA.
    """
    import PyCO2SYS as pyco2

    dic = np.asarray(dic_umol_kg, dtype=float)
    ocean_mass = config.ocean_volume_m3 * config.density_kg_m3
    carbon_atm = config.total_carbon_mol - ocean_mass * dic * 1e-6
    if np.any(~np.isfinite(dic)) or np.any(dic < 0) or np.any(carbon_atm < 0):
        raise ValueError("DIC must be finite and within the closed carbon inventory")
    xco2_ppm = carbon_atm / config.atmosphere_mol * 1e6
    return pyco2.sys(par1=xco2_ppm, par1_type=9, **config.pyco2)["pCO2"]


def connect_atmosphere(model, boxes, *, total_carbon_mol=None,
                       piston_velocity="4 m/d", config=TEACHING):
    from esbmtk import GasReservoir, Species2Species
    import PyCO2SYS as pyco2

    total = config.total_carbon_mol if total_carbon_mol is None else total_carbon_mol
    ocean_carbon = sum(box_mass_kg(b) * b.DIC.c[0] for b in boxes)
    xco2 = (total - ocean_carbon) / config.atmosphere_mol
    if xco2 <= 0:
        raise ValueError("initial ocean carbon must be less than total carbon")
    GasReservoir(name="CO2_At", species=model.CO2,
                 species_ppm=f"{xco2 * 1e6} ppm",
                 reservoir_mass=f"{config.atmosphere_mol} mol")
    # A single gas input gives the xCO2 -> aqueous CO2 conversion without
    # inferring TA. Native gas_exchange uses 1000 * CO2aq (mol/kg).
    # Scale both sides by rho/1000 to recover A*v*rho*(CO2eq-CO2aq).
    gas = pyco2.sys(par1=1.0, par1_type=9, **config.pyco2)
    beta_native = float(gas["aqueous_CO2"]) * 1000.0
    surface = boxes[0]
    model.air_sea_exchange = Species2Species(
        source=model.CO2_At, sink=surface.DIC, species=model.CO2,
        piston_velocity=piston_velocity, ctype="gasexchange",
        solubility=f"{beta_native} mol/(m**3 * atm)",
        scale=surface.swc.density / 1000.0,
        ref_species=surface.CO2aq, id="air_sea")
    model.ocean_boxes = tuple(boxes)
    model.initial_carbon_mol = total
    model.teaching_config = config
    return model.air_sea_exchange


def mixing_mass_transport(config=TEACHING):
    from esbmtk import Q_

    return (Q_(f"{config.mixing_sv} Sverdrup").to("m**3/yr").magnitude
            * config.density_kg_m3)


def add_mixing(model, config=TEACHING):
    from esbmtk import create_bulk_connections

    # Native scale accepts a numeric coefficient; with mol/kg states its
    # numerical unit is kg/yr. ESBMTK 0.14's unit mapper rejects kg/yr strings.
    transport = mixing_mass_transport(config)
    create_bulk_connections({
        "Surface_to_Deep@mix_down": {
            "ty": "scale_with_concentration", "sc": transport,
            "sp": [model.DIC, model.TA]},
        "Deep_to_Surface@mix_up": {
            "ty": "scale_with_concentration", "sc": transport,
            "sp": [model.DIC, model.TA]},
    }, model)


def calibrated_pump_coefficient(config=TEACHING):
    """Fitted k (kg/yr); the DIC gradient constrains k/(Q rho)."""
    return mixing_mass_transport(config) * (
        config.target_deep_dic_umol_kg / config.target_dic_umol_kg - 1)


def add_effective_pump(model, k_kg_yr):
    from esbmtk import Species2Species

    if k_kg_yr < 0:
        raise ValueError("pump coefficient must be non-negative")
    model.pump_k_kg_yr = k_kg_yr
    model.effective_pump = Species2Species(
        source=model.Surface.DIC, sink=model.Deep.DIC,
        ctype="scale_with_concentration", scale=float(k_kg_yr),
        id="effective_pump")
    return model.effective_pump


def single_box(*, ta_umol_kg=0.0, initial_dic_umol_kg=0.01,
               piston_velocity="4 m/d", config=TEACHING, **clock):
    from esbmtk import initialize_reservoirs, add_carbonate_system_1

    clock.setdefault("stop", "2 kyr")
    clock.setdefault("max_timestep", "1 yr")
    model = new_model(config=config, **clock)
    initialize_reservoirs(model, {"Ocean": box_parameters(
        model, config.ocean_volume_m3, initial_dic_umol_kg, ta_umol_kg, config)})
    add_carbonate_system_1([model.Ocean])
    connect_atmosphere(model, [model.Ocean], piston_velocity=piston_velocity,
                       config=config)
    return model


def two_layer(*, ta_umol_kg=None, initial_dic_umol_kg=1000.0,
              k_kg_yr=0.0, state=None, config=TEACHING, **clock):
    from esbmtk import initialize_reservoirs, add_carbonate_system_1

    if ta_umol_kg is None:
        ta_umol_kg = float(config.reference_state()["alkalinity"])
    if state is None:
        state = {"Surface": (initial_dic_umol_kg, ta_umol_kg),
                 "Deep": (initial_dic_umol_kg, ta_umol_kg)}
    model = new_model(config=config, **clock)
    initialize_reservoirs(model, {
        name: box_parameters(model, volume, *state[name], config)
        for name, volume in (("Surface", config.surface_volume_m3),
                             ("Deep", config.deep_volume_m3))})
    add_carbonate_system_1([model.Surface, model.Deep])
    add_mixing(model, config)
    if k_kg_yr:
        add_effective_pump(model, k_kg_yr)
    connect_atmosphere(model, [model.Surface, model.Deep], config=config)
    return model


def inventories(model):
    carbon = model.CO2_At.c * model.CO2_At.v[0]
    ta = np.zeros_like(carbon)
    for box in model.ocean_boxes:
        carbon = carbon + box_mass_kg(box) * box.DIC.c
        ta = ta + box_mass_kg(box) * box.TA.c
    return carbon, ta


def audit(model, added_carbon=None, *, rtol=2e-6):
    carbon, ta = inventories(model)
    expected = carbon[0] if added_carbon is None else carbon[0] + added_carbon
    np.testing.assert_allclose(carbon, expected, rtol=rtol, atol=1e5)
    np.testing.assert_allclose(ta, ta[0], rtol=rtol, atol=1e5)
    for box in model.ocean_boxes:
        assert np.all(np.isfinite(box.DIC.c)) and np.all(box.DIC.c > 0)
    return {"carbon_relative_error": float(np.max(np.abs(carbon - expected)) / carbon[0]),
            "ta_change_mol": float(np.max(np.abs(ta - ta[0])))}


def finite_box_addition(config=TEACHING):
    return (config.deep_volume_m3 * config.density_kg_m3
            * (config.target_deep_dic_umol_kg - config.target_dic_umol_kg) * 1e-6)


def finite_pulse_clock(*, start, duration, stop="30 kyr"):
    """Supply a resolved, aligned clock for the finite square pulse in 02.

    Native ESBMTK 0.14 truncates start/duration to whole model years and maps
    signals by exact time matches. Use a common integer-year divisor, halved
    if necessary, so pulse boundaries and the model grid align exactly. Keep
    the usual 20-year limit and at least 20 intervals across the pulse. This
    also avoids its broken warning path for fewer than 10 intervals.
    """
    from math import gcd
    from esbmtk import Q_

    years = {}
    for name, value in (("start", start), ("duration", duration), ("stop", stop)):
        number = float(Q_(value).to("yr").magnitude)
        rounded = round(number) if np.isfinite(number) else 0
        if not np.isfinite(number) or not np.isclose(number, rounded, rtol=0, atol=1e-9):
            raise ValueError(f"pulse {name} must be a whole number of years for ESBMTK")
        years[name] = rounded
    if years["start"] <= 0 or years["duration"] <= 0:
        raise ValueError("pulse start and duration must be positive")
    if years["start"] + years["duration"] >= years["stop"]:
        raise ValueError("pulse must end before stop; leave time for equilibration")
    step = float(gcd(20, years["start"], years["duration"], years["stop"]))
    while years["duration"] / step < 20:
        step /= 2
    return {"stop": f'{years["stop"]} yr', "max_timestep": f"{step:g} yr"}


def integrated_signal(time, flux, evaluation_time):
    """Exact integral of the piecewise-linear Signal used by ESBMTK.

    Save the native time and flux arrays before running: model post-processing
    can change the display grid. The finite pulse must be zero at both ends.
    """
    from scipy.integrate import cumulative_trapezoid

    time, flux, t = map(np.asarray, (time, flux, evaluation_time))
    if time.ndim != 1 or flux.shape != time.shape or np.any(np.diff(time) <= 0):
        raise ValueError("signal needs matching arrays on an increasing time grid")
    if flux[0] != 0 or flux[-1] != 0:
        raise ValueError("finite signal must be zero at both model boundaries")
    cumulative = cumulative_trapezoid(flux, time, initial=0)
    clipped = np.clip(t, time[0], time[-1])
    i = np.clip(np.searchsorted(time, clipped, side="right") - 1, 0, len(time) - 2)
    dt = clipped - time[i]
    slope = (flux[i + 1] - flux[i]) / (time[i + 1] - time[i])
    return cumulative[i] + flux[i] * dt + 0.5 * slope * dt**2
