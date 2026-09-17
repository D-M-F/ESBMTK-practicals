"""Thin, native-ESBMTK forcing helpers shared by the tutorial notebooks."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


def add_carbon_signal(
    model,
    *,
    filename: str | Path | None = None,
    scale: float = 1.0,
    start: str = "0 yr",
    duration: str = "100 yr",
    mass: str = "83.26 Pmol",
    shape: str = "bell",
    name: str = "carbon_signal",
):
    """Add external carbon to the atmosphere; ocean uptake remains emergent.

    Supply ``filename`` for an ESBMTK CSV Signal, or omit it
    for an idealized mass-conserving pulse described by ``mass`` and ``shape``.
    The default 83.26 Pmol C is approximately 1000 Gt C; ESBMTK tracks carbon
    as moles rather than accepting a carbon-mass unit such as ``GtC``.
    """
    from esbmtk import Signal, Source, Species2Species

    signal_kwargs = {
        "name": name,
        "species": model.CO2,
        "scale": scale,
        "register": model,
    }
    if filename is not None:
        path = Path(filename).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Carbon forcing file not found: {path}")
        signal_kwargs["filename"] = str(path)
    else:
        signal_kwargs.update(
            start=start, duration=duration, mass=mass, shape=shape
        )

    signal = Signal(**signal_kwargs)
    source = Source(name=f"{name}_source", species=model.CO2)
    connection = Species2Species(
        source=source,
        sink=model.CO2_At,
        rate="0 mol/yr",
        signal=signal,
        id=name,
    )
    model.carbon_signal = signal
    model.carbon_signal_source = source
    model.carbon_signal_connection = connection
    return signal


def add_alkalinity_signal(
    model,
    *,
    target=None,
    filename: str | Path | None = None,
    scale: float = 1.0,
    start: str = "0 yr",
    duration: str = "20 yr",
    mass: str = "20 Pmol",
    shape: str = "square",
    name: str = "alkalinity_signal",
):
    """Add idealized pure TA to a surface box, without directly adding DIC."""
    from esbmtk import Signal, Source, Species2Species

    target_species = model.L_b.TA if target is None else target
    if getattr(target_species, "sp", None) is not model.TA:
        raise ValueError("target must be an ESBMTK TA reservoir species")

    signal_kwargs = {
        "name": name,
        "species": model.TA,
        "scale": scale,
        "register": model,
    }
    if filename is not None:
        path = Path(filename).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Alkalinity forcing file not found: {path}")
        signal_kwargs["filename"] = str(path)
    else:
        signal_kwargs.update(
            start=start, duration=duration, mass=mass, shape=shape
        )

    signal = Signal(**signal_kwargs)
    source = Source(name=f"{name}_source", species=model.TA)
    connection = Species2Species(
        source=source,
        sink=target_species,
        rate="0 mol/yr",
        signal=signal,
        id=name,
    )
    model.alkalinity_signal = signal
    model.alkalinity_signal_source = source
    model.alkalinity_signal_connection = connection
    return signal


def add_flux_signal(
    model,
    connections,
    *,
    factor: float,
    start: str = "0 yr",
    duration: str = "1000 yr",
    shape: str = "square",
    name: str = "process_signal",
):
    """Multiply one or more existing ESBMTK flux connections by a Signal.

    ``connections`` may contain connection objects or their ``M.<name>``
    attribute names.  Applying the same factor to all DIC/TA members of a
    transport process keeps its stoichiometry intact.

    ESBMTK 0.14.3 stores every Signal magnitude in model flux units even when
    ``stype='multiplication'``; the generated equation uses its numerical value
    as the dimensionless multiplier.  This helper contains that API detail.
    """
    from esbmtk import Signal

    if factor < 0:
        raise ValueError("factor must be non-negative")
    if isinstance(connections, (str, bytes)) or not isinstance(connections, Iterable):
        connections = [connections]

    signals = []
    for index, item in enumerate(connections):
        connection = getattr(model, item) if isinstance(item, str) else item
        if not hasattr(connection, "source") or not hasattr(connection, "sink"):
            raise TypeError("connections must be ESBMTK connection objects or names")
        if connection.signal != "None":
            raise ValueError(f"{connection.full_name} already has a Signal")

        signal = Signal(
            name=f"{name}_{index}",
            species=connection.source.sp,
            start=start,
            duration=duration,
            magnitude=f"{factor} {model.f_unit}",
            shape=shape,
            stype="multiplication",
            register=model,
        )
        connection.signal = signal
        connection.lop.append(signal)
        signal.__register_with_flux__(connection.lof[0])
        signals.append(signal)

    model.process_signals = getattr(model, "process_signals", []) + signals
    return signals


def connections_by_id(model, connection_id: str):
    """Return all native connection objects with a matching ESBMTK id."""
    matches = [connection for connection in model.loc if connection.id == connection_id]
    if not matches:
        raise KeyError(f"No connection with id={connection_id!r}")
    return matches


__all__ = [
    "add_alkalinity_signal",
    "add_carbon_signal",
    "add_flux_signal",
    "connections_by_id",
]
