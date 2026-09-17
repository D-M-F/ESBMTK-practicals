"""One readable ESBMTK model shared by all tutorial scenarios.

The model order and equations intentionally remain close to the official
``ESBMTK-Examples/Boudreau_2010`` implementation.  Scenario-specific changes
belong in :mod:`scenarios`, not here.
"""

from __future__ import annotations

import logging
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Mapping

from presets import BOUDREAU_2010
from model_inputs import transport_specification


def initialize_model(
    params: Mapping | None = None,
    stop: str = "3800 yr",
    max_timestep: str = "1 month",
):
    """Build the shared three-ocean-box plus atmosphere carbon-cycle model.

    Parameters are ordinary mappings so students can see and change them
    directly.  With :data:`presets.BOUDREAU_2010`, the equations and numerical
    options match the official example.
    """
    from esbmtk import (
        Q_,
        ConnectionProperties,
        GasReservoir,
        Model,
        Species2Species,
        add_carbonate_system_1,
        add_carbonate_system_2,
        create_bulk_connections,
        initialize_reservoirs,
    )

    p = BOUDREAU_2010 if params is None else params
    _validate_params(p)
    strengths = p.get(
        "pump_strengths",
        {"solubility": 1.0, "soft_tissue": 1.0, "carbonate": 1.0},
    )
    feedbacks = p.get(
        "pump_feedbacks",
        {
            "soft_tissue": {"enabled": False},
            "carbonate": {"enabled": False},
        },
    )
    carbonate_compensation_enabled = bool(
        p.get("carbonate_compensation_enabled", True)
    )

    # Model construction creates M.log.  Keep this generated file out of the
    # teaching repository without changing ESBMTK's own logging behavior.
    root_logger = logging.getLogger()
    previous_level = root_logger.level
    previous_handlers = set(root_logger.handlers)
    with TemporaryDirectory(prefix="esbmtk_initialization_") as tmp_dir:
        with _working_directory(tmp_dir):
            try:
                M = Model(
                    stop=stop,
                    max_timestep=max_timestep,
                    element=["Carbon", "Boron", "Hydrogen", "misc_variables"],
                    mass_unit="mol",
                    concentration_unit="mol/kg",
                    opt_k_carbonic=p["opt_k_carbonic"],
                    opt_pH_scale=p["opt_pH_scale"],
                )
            finally:
                for handler in set(root_logger.handlers) - previous_handlers:
                    filename = getattr(handler, "baseFilename", "")
                    if filename and Path(filename).name == "M.log":
                        handler.close()
                        root_logger.removeHandler(handler)
                root_logger.setLevel(previous_level)

    # 1. Reservoirs and initial concentrations.
    box_parameters = {}
    for box_name, box in p["boxes"].items():
        box_parameters[box_name] = {
            "c": {M.DIC: box["dic"], M.TA: box["ta"]},
            "g": {"area": box["area"], "volume": box["volume"]},
            "T": box["temperature"],
            "P": box["pressure"],
            "S": box["salinity"],
        }
    for node in p["boundary_nodes"]:
        box_parameters[node["name"]] = {
            "ty": node["type"],
            "sp": [getattr(M, species) for species in node["species"]],
        }
    species_list = initialize_reservoirs(M, box_parameters)

    # 2. Map the workbook arrows through the standard ESBMTK constructor.
    create_bulk_connections(transport_specification(p, species_list), M)

    # Retain the chosen dictionary for notebook introspection/provenance.  The
    # state-dependent pump wrappers also use it to obtain reference fluxes.
    M.tutorial_params = p

    # 3. Organic (POC) and carbonate (PIC) export.  Strength and feedback are
    # independent controls.  At unit strength with feedback disabled this is
    # exactly the official 200/60 Tmol/yr Boudreau configuration.
    soft_strength = float(strengths.get("soft_tissue", 1.0))
    carbonate_strength = float(strengths.get("carbonate", 1.0))
    M.OM_export_reference = Q_(p["poc_export"])
    M.CaCO3_export_reference = Q_(p["pic_export"])
    M.OM_export = M.OM_export_reference * soft_strength
    M.CaCO3_export = M.CaCO3_export_reference * carbonate_strength

    soft_config = feedbacks.get("soft_tissue", {"enabled": False})
    soft_feedback_enabled = soft_config.get("enabled", False)
    carbonate_config = feedbacks.get("carbonate", {"enabled": False})
    carbonate_feedback_enabled = carbonate_config.get("enabled", False)

    if not soft_feedback_enabled and not carbonate_feedback_enabled:
        # Preserve the upstream connection-construction grouping.  ESBMTK's
        # generated equation ordering is sensitive to this detail on the
        # currently supported Windows/Python combination.
        fixed_pumps = {
            "L_b_to_D_b@POM": {
                "sp": M.DIC,
                "ty": "Fixed",
                "ra": M.OM_export,
            },
            "L_b_to_D_b@PIC_DIC": {
                "sp": M.DIC,
                "ty": "Fixed",
                "ra": M.CaCO3_export,
            },
            "L_b_to_D_b@PIC_TA": {
                "sp": M.TA,
                "ty": "Fixed",
                "ra": M.CaCO3_export * 2,
            },
        }
        if carbonate_compensation_enabled:
            fixed_pumps["L_b_to_D_b@PIC_DIC"]["bp"] = "sink"
            fixed_pumps["L_b_to_D_b@PIC_TA"]["bp"] = "sink"
        create_bulk_connections(fixed_pumps, M)
        M.OM_export_flux = M.flux_summary(
            filter_by="POM", return_list=True
        )[0]
        M.CaCO3_export_flux = M.flux_summary(
            filter_by="PIC_DIC", return_list=True
        )[0]
    else:
        if not soft_feedback_enabled:
            create_bulk_connections(
                {
                    "L_b_to_D_b@POM": {
                        "sp": M.DIC,
                        "ty": "Fixed",
                        "ra": M.OM_export,
                    }
                },
                M,
            )
            M.OM_export_flux = M.flux_summary(
                filter_by="POM", return_list=True
            )[0]

        if carbonate_feedback_enabled:
            if not carbonate_compensation_enabled:
                raise ValueError(
                    "state-dependent carbonate export requires "
                    "carbonate_compensation_enabled=True"
                )
            from pump_functions import add_carbonate_feedback

            add_carbonate_feedback(M, carbonate_config, carbonate_strength)
        else:
            fixed_pic = {
                "L_b_to_D_b@PIC_DIC": {
                    "sp": M.DIC,
                    "ty": "Fixed",
                    "ra": M.CaCO3_export,
                },
                "L_b_to_D_b@PIC_TA": {
                    "sp": M.TA,
                    "ty": "Fixed",
                    "ra": M.CaCO3_export * 2,
                },
            }
            if carbonate_compensation_enabled:
                fixed_pic["L_b_to_D_b@PIC_DIC"]["bp"] = "sink"
                fixed_pic["L_b_to_D_b@PIC_TA"]["bp"] = "sink"
            create_bulk_connections(fixed_pic, M)
            M.CaCO3_export_flux = M.flux_summary(
                filter_by="PIC_DIC", return_list=True
            )[0]

    poc = M.OM_export.to("Tmol/yr").magnitude
    pic = M.CaCO3_export.to("Tmol/yr").magnitude
    M.rain_ratio = pic / poc if poc else float("nan")

    # 4. Carbonate chemistry and compensation.  Carbonate system 2 consumes
    # the actual PIC flux object, whether it is fixed or calculated from the
    # evolving TA-DIC state.  Keep this ahead of atmosphere construction: that
    # is the stable ordering used by the upstream Boudreau implementation.
    surface_boxes = [M.L_b, M.H_b]
    add_carbonate_system_1(surface_boxes)
    M.carbonate_compensation_enabled = carbonate_compensation_enabled
    if carbonate_compensation_enabled:
        export_fluxes = [M.CaCO3_export_flux]
        add_carbonate_system_2(
            r_sb=[M.L_b],
            r_db=[M.D_b],
            carbonate_export_fluxes=export_fluxes,
            z0=p["z0"],
            alpha=p["alpha"],
        )
    else:
        # Closed storage-decomposition mode: PIC is added directly to the
        # deep box, and ordinary carbonate chemistry supplies deep pH/CO3.
        add_carbonate_system_1([M.D_b])

    # 5. Atmosphere and gas exchange.  A live soft-tissue connection is
    # created here, after either atmospheric pCO2 or surface CO2aq exists.  Its
    # ExternalCode is still emitted in ESBMTK's pre-flux evaluation block.
    GasReservoir(
        name="CO2_At", species=M.CO2, species_ppm=p["pco2"],
        reservoir_mass=p["atmosphere_moles"],
    )
    if soft_feedback_enabled:
        from pump_functions import add_soft_tissue_feedback

        add_soft_tissue_feedback(M, soft_config, soft_strength)

    M.gas_exchange_enabled = bool(p.get("gas_exchange_enabled", True))
    if M.gas_exchange_enabled:
        for row in p["gas_exchange_connections"]:
            surface_box = getattr(M, row["surface"])
            Species2Species(
                source=getattr(M, row["atmosphere"]),
                sink=surface_box.DIC,
                species=getattr(M, row["species"]),
                piston_velocity=p[row["parameter"]],
                ctype="gasexchange",
                id=surface_box.name,
            )

    # 6. Weathering.
    M.weathering_strength = float(p.get("weathering_strength", 1.0))
    if M.weathering_strength < 0:
        raise ValueError("weathering_strength must be non-negative")
    if M.weathering_strength:
        ConnectionProperties(
            source=M.Fw,
            sink=M.L_b,
            rate={
                M.DIC: Q_(p["weathering_dic"]) * M.weathering_strength,
                M.TA: Q_(p["weathering_ta"]) * M.weathering_strength,
            },
            species=[M.DIC, M.TA],
            ctype="fixed",
            id="weathering",
        )

    return M


def run_model(model, method: str = "BDF"):
    """Run a model, including the ESBMTK Windows temporary-file workaround.

    ESBMTK 0.14.3.1.post0 may be unable to reopen its named temporary
    equations file on Windows under both Python 3.13 and 3.14.  Its persistent
    equations path is equivalent and does work; generated files are confined
    to a temporary directory.
    """
    needs_workaround = os.name == "nt"
    if not needs_workaround:
        model.run(method=method)
        from pump_functions import update_pump_flux_diagnostics

        update_pump_flux_diagnostics(model)
        return model

    old_setting = model.debug_equations_file
    with TemporaryDirectory(prefix="esbmtk_equations_") as tmp_dir:
        try:
            model.debug_equations_file = True
            sys.modules.pop("equations", None)
            with _working_directory(tmp_dir):
                model.run(method=method)
        finally:
            model.debug_equations_file = old_setting
            sys.modules.pop("equations", None)
    from pump_functions import update_pump_flux_diagnostics

    update_pump_flux_diagnostics(model)
    return model


def postprocess_carbonate_horizons(model):
    """Populate zsat, zcc, zsnow, dissolution, and burial diagnostics."""
    from esbmtk import carbonate_system_2_pp

    if not getattr(model, "carbonate_compensation_enabled", True):
        return model

    # Flux.m contains the evaluated time series after integration.  Passing it
    # through is essential for state-dependent PIC production; fall back to
    # the nominal scalar for older model objects.
    export_flux = getattr(model, "CaCO3_export_flux", None)
    export_data = getattr(export_flux, "m", None)
    if export_data is not None and len(export_data) == len(model.time):
        export = export_data
    else:
        export = model.CaCO3_export.to(f"{model.f_unit}").magnitude
    carbonate_system_2_pp(model.D_b, export, zsat_min=200, zmax=10999)
    return model


def standard_diagnostics(model):
    """Return native ESBMTK objects used by every tutorial plot."""
    from esbmtk import DataField, data_summaries

    species = [model.DIC, model.TA, model.pH, model.CO3]
    boxes = [model.L_b, model.H_b, model.D_b]
    diagnostics = data_summaries(model, species, boxes)

    # ESBMTK 0.14.3 post-processing represents several carbonate outputs as
    # VectorData, which intentionally has no direct __plot__ method. Group the
    # native arrays in DataFields so the common M.plot(...) path remains usable.
    DataField(
        name="carbonate_depths_df",
        register=model,
        x1_data=model.time,
        y1_data=[model.D_b.zsat.c, model.D_b.zcc.c, model.D_b.zsnow.c],
        y1_label=["zsat", "zcc", "zsnow"],
        y1_legend="Depth [m]",
        x1_as_time=True,
        title="Carbonate compensation depths",
    )
    DataField(
        name="carbonate_fluxes_df",
        register=model,
        x1_data=model.time,
        y1_data=[model.D_b.Fdiss.c, model.D_b.Fburial.c],
        y1_label=["Fdiss", "Fburial"],
        y1_legend=f"Carbonate flux [{model.f_unit:~P}]",
        x1_as_time=True,
        title="Carbonate dissolution and burial",
    )
    diagnostics += [
        model.CO2_At,
        model.carbonate_depths_df,
        model.carbonate_fluxes_df,
    ]
    return diagnostics


def _validate_params(params: Mapping) -> None:
    required = {
        "pco2",
        "atmosphere_moles",
        "thc",
        "mixing",
        "poc_export",
        "pic_export",
        "rain_ratio",
        "weathering_dic",
        "weathering_ta",
        "alpha",
        "z0",
        "piston_velocity",
        "opt_k_carbonic",
        "opt_pH_scale",
        "boxes",
        "boundary_nodes",
        "transport_connections",
        "gas_exchange_connections",
    }
    missing = required.difference(params)
    if missing:
        raise KeyError(f"Missing model parameters: {sorted(missing)}")

    # POC and PIC are deliberately independent experiment controls.  The
    # historical rain_ratio input is retained as provenance and as a
    # compatibility-wrapper convenience, but the effective ratio is derived
    # from the two explicit export fluxes.
    from esbmtk import Q_

    poc = Q_(params["poc_export"]).to("Tmol/yr").magnitude
    pic = Q_(params["pic_export"]).to("Tmol/yr").magnitude
    if poc < 0 or pic < 0:
        raise ValueError("poc_export and pic_export must be non-negative")
    strengths = params.get("pump_strengths", {})
    if any(float(value) < 0 for value in strengths.values()):
        raise ValueError("pump strengths must be non-negative")


@contextmanager
def _working_directory(path: str | Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


__all__ = [
    "initialize_model",
    "postprocess_carbonate_horizons",
    "run_model",
    "standard_diagnostics",
]
