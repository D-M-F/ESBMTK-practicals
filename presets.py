"""Plain-dictionary parameters for the Boudreau-like teaching model."""

from __future__ import annotations

from copy import deepcopy

from reservoir_inputs import DEFAULT_RESERVOIR_WORKBOOK
from model_inputs import load_model_inputs


def load_boudreau_parameters(workbook=DEFAULT_RESERVOIR_WORKBOOK):
    """Read a fresh model definition from Excel, including linked fluxes.

    The workbook owns baseline geometry, connections and process parameters.
    Each call returns independent dictionaries. Experiments override these
    copies without changing the workbook or a matched control.
    """
    return load_model_inputs(workbook)


# Compatibility snapshot for scripts; notebooks explicitly reload on setup.
BOUDREAU_2010 = load_boudreau_parameters()


def make_pump_variant(
    base=None,
    *,
    solubility_strength: float = 1.0,
    soft_tissue_strength: float = 1.0,
    carbonate_strength: float = 1.0,
    soft_tissue_feedback: bool = False,
    carbonate_feedback: bool = False,
):
    """Return an independent Boudreau-like pump experiment dictionary.

    ``solubility_strength`` scales the reference low-to-high-latitude
    temperature contrast.  It is deliberately not mapped to piston velocity:
    piston velocity changes equilibration rate, not equilibrium solubility.

    The POC and PIC strengths are independent.  Consequently the resulting
    PIC/POC ratio is a diagnostic rather than an invariant input.
    """
    strengths = {
        "solubility": solubility_strength,
        "soft_tissue": soft_tissue_strength,
        "carbonate": carbonate_strength,
    }
    if any(value < 0 for value in strengths.values()):
        raise ValueError("pump strengths must be non-negative")

    params = deepcopy(BOUDREAU_2010 if base is None else base)
    params["pump_strengths"] = strengths
    params["pump_feedbacks"]["soft_tissue"]["enabled"] = soft_tissue_feedback
    params["pump_feedbacks"]["carbonate"]["enabled"] = carbonate_feedback

    low_temperature = float(params["boxes"]["L_b"]["temperature"])
    reference_high_temperature = float(params["boxes"]["H_b"]["temperature"])
    reference_contrast = low_temperature - reference_high_temperature
    params["boxes"]["H_b"]["temperature"] = (
        low_temperature - solubility_strength * reference_contrast
    )

    # Keep the reference fluxes visible in the preset.  The strength factors
    # are applied when connections are constructed, including feedback cases.
    params["name"] = (
        "Boudreau-like pump variant "
        f"(solubility={solubility_strength:g}, "
        f"soft={soft_tissue_strength:g}, carbonate={carbonate_strength:g})"
    )
    return params


def make_process_variant(
    base=None,
    *,
    gas_exchange: bool = True,
    soft_tissue: bool = True,
    carbonate: bool = True,
    weathering: bool = False,
):
    """Return a process-on/off configuration for storage decomposition.

    Thermohaline circulation and high-latitude mixing intentionally remain at
    their reference values. Weathering defaults to off because cases without
    carbonate export have no balancing long-term burial sink.
    """
    params = make_pump_variant(
        BOUDREAU_2010 if base is None else base,
        solubility_strength=1.0,
        soft_tissue_strength=float(soft_tissue),
        carbonate_strength=float(carbonate),
        soft_tissue_feedback=False,
        carbonate_feedback=False,
    )
    params["gas_exchange_enabled"] = bool(gas_exchange)
    params["weathering_strength"] = float(weathering)
    # Storage decomposition tracks redistribution within the active
    # atmosphere-ocean inventory. Exported PIC therefore redissolves fully in
    # the deep box instead of entering the implicit CS2 burial sink.
    params["carbonate_compensation_enabled"] = False
    params["name"] = (
        "Sequential storage configuration "
        f"(G={int(gas_exchange)}, S={int(soft_tissue)}, "
        f"C={int(carbonate)}, weathering={int(weathering)})"
    )
    return params


__all__ = ["BOUDREAU_2010", "load_boudreau_parameters", "make_process_variant", "make_pump_variant"]
