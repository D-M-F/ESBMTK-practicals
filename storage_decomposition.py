"""Process-tagged DIC storage diagnostics for the three-box teaching model.

The tags are diagnostic bookkeeping tracers.  They do not feed back on the
carbonate system: the coupled DIC/TA/atmosphere model is solved once, and its
realized gas-exchange flux is then propagated through the same linear THC and
mixing operator as DIC.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


BOX_ORDER = ("L_b", "H_b", "D_b")
TAG_ORDER = ("background", "gas_exchange", "soft_tissue", "carbonate")


@dataclass(frozen=True)
class StorageDecomposition:
    """Time-dependent process tags and their numerical closure diagnostics."""

    time: np.ndarray
    box_order: tuple[str, ...]
    tag_order: tuple[str, ...]
    mass: dict[str, np.ndarray]
    concentration_umol_kg: dict[str, np.ndarray]
    reconstructed_dic_umol_kg: np.ndarray
    model_dic_umol_kg: np.ndarray
    closure_umol_kg: np.ndarray
    atmospheric_gas_tag_mol: np.ndarray


def _water_transport_matrix(model) -> tuple[np.ndarray, np.ndarray]:
    """Return the DIC amount-space transport matrix and box water masses."""
    from esbmtk import Q_

    boxes = tuple(getattr(model, name) for name in BOX_ORDER)
    water_mass = np.array(
        [box.DIC.volume.to('m**3').magnitude * box.swc.density for box in boxes],
        dtype=float,
    )
    # Use the same workbook arrows as the physical model. Preserve the
    # benchmark's nominal litre/yr transport convention (03 explains it).
    index = {name: i for i, name in enumerate(BOX_ORDER)}
    matrix = np.zeros((3, 3), dtype=float)
    for connection in model.tutorial_params["transport_connections"]:
        source = index[connection["source"]]
        sink = index[connection["sink"]]
        water_flux = Q_(model.tutorial_params[connection["parameter"]]).to("liter/yr").magnitude
        rate = water_flux / water_mass[source]
        matrix[source, source] -= rate
        matrix[sink, source] += rate
    return matrix, water_mass


def decompose_dic_storage(model) -> StorageDecomposition:
    """Tag DIC storage in one executed, closed G+S+C model.

    ``model`` must have gas exchange, POC export, and PIC export enabled, while
    weathering and carbonate compensation are disabled.  The four diagnostic
    fields obey

    ``DIC = background + gas_exchange + soft_tissue + carbonate``.

    ``background`` carries the initial DIC field through THC and mixing.  The
    three zero-initialized process tags receive the realized gas-exchange flux,
    the POC transfer, or the fully redissolved PIC transfer, respectively.
    """
    from esbmtk import gas_exchange_fluxes
    from scipy.integrate import cumulative_trapezoid, solve_ivp

    if getattr(model, "executionstate", 0) != 1:
        raise ValueError("model must be executed before storage decomposition")
    if not getattr(model, "gas_exchange_enabled", False):
        raise ValueError("storage decomposition requires gas exchange")
    if getattr(model, "weathering_strength", 1.0) != 0:
        raise ValueError("storage decomposition requires weathering_strength=0")
    if getattr(model, "carbonate_compensation_enabled", True):
        raise ValueError(
            "storage decomposition requires carbonate_compensation_enabled=False"
        )

    time = np.asarray(model.time, dtype=float)
    matrix, water_mass = _water_transport_matrix(model)
    boxes = tuple(getattr(model, name) for name in BOX_ORDER)
    model_dic = np.vstack([box.DIC.c for box in boxes]).T * 1e6

    gas_low = np.asarray(
        gas_exchange_fluxes(
            model.L_b.DIC,
            model.CO2_At,
            model.tutorial_params["piston_velocity"],
        ),
        dtype=float,
    )
    gas_high = np.asarray(
        gas_exchange_fluxes(
            model.H_b.DIC,
            model.CO2_At,
            model.tutorial_params["piston_velocity"],
        ),
        dtype=float,
    )
    poc = model.OM_export.to("mol/year").magnitude
    pic = model.CaCO3_export.to("mol/year").magnitude

    initial = np.zeros((len(TAG_ORDER), len(BOX_ORDER)), dtype=float)
    initial[0] = water_mass * np.array([box.DIC.c[0] for box in boxes], dtype=float)

    def tendency(t, flattened):
        tags = flattened.reshape(len(TAG_ORDER), len(BOX_ORDER))
        source = np.zeros_like(tags)
        source[1, 0] = np.interp(t, time, gas_low)
        source[1, 1] = np.interp(t, time, gas_high)
        source[2] = (-poc, 0.0, poc)
        source[3] = (-pic, 0.0, pic)
        return (tags @ matrix.T + source).ravel()

    result = solve_ivp(
        tendency,
        (time[0], time[-1]),
        initial.ravel(),
        t_eval=time,
        method="BDF",
        rtol=1e-10,
        atol=1e3,
    )
    if not result.success:
        raise RuntimeError(result.message)

    tag_mass = result.y.T.reshape(len(time), len(TAG_ORDER), len(BOX_ORDER))
    mass = {name: tag_mass[:, index, :] for index, name in enumerate(TAG_ORDER)}
    concentration = {
        name: values / water_mass[np.newaxis, :] * 1e6
        for name, values in mass.items()
    }
    reconstructed = sum(concentration.values())
    closure = reconstructed - model_dic
    atmosphere = -cumulative_trapezoid(
        gas_low + gas_high,
        time,
        initial=0.0,
    )
    return StorageDecomposition(
        time=time,
        box_order=BOX_ORDER,
        tag_order=TAG_ORDER,
        mass=mass,
        concentration_umol_kg=concentration,
        reconstructed_dic_umol_kg=reconstructed,
        model_dic_umol_kg=model_dic,
        closure_umol_kg=closure,
        atmospheric_gas_tag_mol=atmosphere,
    )


__all__ = ["BOX_ORDER", "TAG_ORDER", "StorageDecomposition", "decompose_dic_storage"]
