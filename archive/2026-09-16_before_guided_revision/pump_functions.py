"""Optional state-dependent ocean-pump functions for the teaching model.

The small numerical functions in this module are imported by ESBMTK's
generated equation system.  The ``add_*`` wrappers connect their return values
to ordinary ESBMTK flux objects so budgets and diagnostics remain native.
"""

from __future__ import annotations

from math import sqrt


def _positive_smooth(value: float, epsilon: float = 1e-12) -> float:
    """Smooth approximation to max(value, 0), friendly to stiff solvers."""
    return 0.5 * (value + sqrt(value * value + epsilon * epsilon))


def normalized_hill(
    state: float,
    reference: float,
    half_saturation: float,
    exponent: float,
) -> float:
    """Bounded Hill response normalized to one at ``reference``."""
    if reference <= 0 or half_saturation <= 0 or exponent <= 0:
        raise ValueError("Hill parameters and reference state must be positive")
    state = _positive_smooth(state)
    state_power = state**exponent
    half_power = half_saturation**exponent
    reference_power = reference**exponent
    response = state_power / (half_power + state_power)
    reference_response = reference_power / (half_power + reference_power)
    return response / reference_response


def soft_tissue_export(pco2: float, p: tuple) -> float:
    """Return POC export as a bounded function of atmospheric pCO2.

    ``pco2`` is the atmospheric mole fraction used internally by ESBMTK
    (280 ppm is 280e-6).  Parameters are reference flux, strength, reference
    pCO2, half-saturation pCO2, and Hill exponent.
    """
    reference_flux, strength, reference, half_saturation, exponent = p
    return reference_flux * strength * normalized_hill(
        pco2, reference, half_saturation, exponent
    )


def soft_tissue_export_co2aq(co2aq: float, p: tuple) -> float:
    """Return POC export driven by surface dissolved CO2 concentration."""
    reference_flux, strength, reference, half_saturation, exponent = p
    return reference_flux * strength * normalized_hill(
        co2aq, reference, half_saturation, exponent
    )


def carbonate_export(dic: float, ta: float, p: tuple) -> tuple[float, float]:
    """Return coupled PIC DIC and TA export fluxes.

    The transparent teaching driver is carbonate excess ``TA - DIC``.  The
    single calculation returns ``(F_PIC, 2 F_PIC)`` so the carbonate-pump
    stoichiometry cannot drift between independently evaluated functions.
    """
    reference_flux, strength, reference, half_saturation, exponent = p
    excess = _positive_smooth(ta - dic)
    flux = reference_flux * strength * normalized_hill(
        excess, reference, half_saturation, exponent
    )
    return flux, 2.0 * flux


def add_soft_tissue_feedback(model, config: dict, strength: float = 1.0):
    """Create a live-state POC export connection and return its Flux."""
    from esbmtk import (
        ExternalCode,
        Q_,
        Species2Species,
        register_return_values,
    )
    from esbmtk.utility_functions import register_user_function

    connection = Species2Species(
        source=model.L_b.DIC,
        sink=model.D_b.DIC,
        species=model.DIC,
        ctype="ignore",
        id="POM",
    )
    connection.fh.ftype = "computed"

    driver = config.get("driver", "atmospheric_pco2")
    if driver == "atmospheric_pco2":
        function = soft_tissue_export
        function_name = "soft_tissue_export"
        state = model.CO2_At
        reference = Q_(config["reference"]).to("ppm").magnitude * 1e-6
        half_saturation = (
            Q_(config["half_saturation"]).to("ppm").magnitude * 1e-6
        )
    elif driver == "surface_co2aq":
        function = soft_tissue_export_co2aq
        function_name = "soft_tissue_export_co2aq"
        state = model.L_b.CO2aq
        reference = Q_(config["reference"]).to("mol/kg").magnitude
        half_saturation = Q_(config["half_saturation"]).to("mol/kg").magnitude
    else:
        raise ValueError(
            "soft-tissue driver must be 'atmospheric_pco2' or 'surface_co2aq'"
        )

    reference_flux = Q_(model.tutorial_params["poc_export"]).to(
        model.f_unit
    ).magnitude
    params = (
        reference_flux,
        float(strength),
        reference,
        half_saturation,
        float(config["exponent"]),
    )
    register_user_function(model, "pump_functions", function_name)
    external = ExternalCode(
        name="soft_tissue_feedback",
        species=model.DIC,
        function=function,
        fname=function_name,
        ftype="std",
        function_input_data=[state],
        function_params=params,
        return_values=[{f"F_{connection.fh.full_name}": "soft_tissue"}],
        register=model,
    )
    register_return_values(external, model.L_b.DIC)
    model.soft_tissue_connection = connection
    model.soft_tissue_feedback = external
    model.OM_export_flux = connection.fh
    return connection.fh


def add_carbonate_feedback(model, config: dict, strength: float = 1.0):
    """Create coupled live-state PIC DIC/TA connections.

    Both connections bypass their nominal deep-ocean sink because carbonate
    system 2 uses the DIC export flux to calculate dissolution and burial.
    """
    from esbmtk import (
        ExternalCode,
        Q_,
        Species2Species,
        register_return_values,
    )
    from esbmtk.utility_functions import register_user_function

    if config.get("driver", "ta_minus_dic") != "ta_minus_dic":
        raise ValueError("carbonate driver must be 'ta_minus_dic'")

    dic_connection = Species2Species(
        source=model.L_b.DIC,
        sink=model.D_b.DIC,
        species=model.DIC,
        ctype="ignore",
        bypass="sink",
        id="PIC_DIC",
    )
    ta_connection = Species2Species(
        source=model.L_b.TA,
        sink=model.D_b.TA,
        species=model.TA,
        ctype="ignore",
        bypass="sink",
        id="PIC_TA",
    )
    dic_connection.fh.ftype = "computed"
    ta_connection.fh.ftype = "computed"

    reference_flux = Q_(model.tutorial_params["pic_export"]).to(
        model.f_unit
    ).magnitude
    params = (
        reference_flux,
        float(strength),
        Q_(config["reference"]).to("mol/kg").magnitude,
        Q_(config["half_saturation"]).to("mol/kg").magnitude,
        float(config["exponent"]),
    )
    register_user_function(model, "pump_functions", "carbonate_export")
    external = ExternalCode(
        name="carbonate_feedback",
        species=model.DIC,
        function=carbonate_export,
        fname="carbonate_export",
        ftype="std",
        function_input_data=[model.L_b.DIC, model.L_b.TA],
        function_params=params,
        return_values=[
            {f"F_{dic_connection.fh.full_name}": "carbonate_dic"},
            {f"F_{ta_connection.fh.full_name}": "carbonate_ta"},
        ],
        register=model,
    )
    register_return_values(external, model.L_b)
    model.carbonate_dic_connection = dic_connection
    model.carbonate_ta_connection = ta_connection
    model.carbonate_feedback = external
    model.CaCO3_export_flux = dic_connection.fh
    return dic_connection.fh


def update_pump_flux_diagnostics(model):
    """Reconstruct live pump flux series on the solver's output time grid.

    ESBMTK 0.14.3 evaluates ExternalCode fluxes inside the ODE but does not
    populate their ``Flux.m`` arrays during result mapping.  Re-evaluating the
    same pure functions here makes plotting and carbonate post-processing use
    the actual state-dependent export rather than the zero initialization.
    """
    import numpy as np

    # Notebooks 05/06 use the same runner but intentionally have no Boudreau
    # pump configuration.  In that case there is nothing to reconstruct.
    tutorial_params = getattr(model, "tutorial_params", {})
    feedbacks = tutorial_params.get("pump_feedbacks", {})

    soft_config = feedbacks.get("soft_tissue", {})
    if soft_config.get("enabled", False):
        driver = soft_config.get("driver", "atmospheric_pco2")
        if driver == "atmospheric_pco2":
            values = model.CO2_At.c
            function = soft_tissue_export
        elif driver == "surface_co2aq":
            values = model.L_b.CO2aq.c
            function = soft_tissue_export_co2aq
        else:  # validated during construction; retained as a defensive check
            raise ValueError(f"unknown soft-tissue driver: {driver}")
        params = model.soft_tissue_feedback.function_params
        model.OM_export_flux.m = np.asarray(
            [function(float(value), params) for value in values]
        )

    carbonate_config = feedbacks.get("carbonate", {})
    if carbonate_config.get("enabled", False):
        params = model.carbonate_feedback.function_params
        paired = np.asarray(
            [
                carbonate_export(float(dic), float(ta), params)
                for dic, ta in zip(model.L_b.DIC.c, model.L_b.TA.c)
            ]
        )
        model.CaCO3_export_flux.m = paired[:, 0]
        model.carbonate_ta_connection.fh.m = paired[:, 1]

    return model


__all__ = [
    "add_carbonate_feedback",
    "add_soft_tissue_feedback",
    "carbonate_export",
    "normalized_hill",
    "soft_tissue_export",
    "soft_tissue_export_co2aq",
    "update_pump_flux_diagnostics",
]
