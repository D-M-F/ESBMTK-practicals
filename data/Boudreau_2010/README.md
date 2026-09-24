# Boudreau-like reference data

The forcing, restart and digitized curves are copied without numerical modification from the official
`ESBMTK-Examples/Boudreau_2010` archive cited by Wortmann et al. (2025):

- Zenodo record: <https://doi.org/10.5281/zenodo.14528185>
- archive version: `v0.0.0.3`, compatible with ESBMTK `0.14.0.11`
- archive MD5: `9452e86807b1c224e1b1ec71ef8b7a01`

The restart avoids repeating a one-million-year spin-up during class. It only
sets reservoir state; the notebook must still construct all boxes, connections,
chemistry, and boundary fluxes correctly. The archived example is licensed
LGPL-3.0.

`IS92a-scenario.csv` is the exact forcing file used by notebook 04. With the
archived scale factor 0.877, integration from model year 1800 gives
4024.27 Gt C (335.356 Pmol C, using 12 g mol$^{-1}$). Its SHA-256 is
`6024588cd37addcded8261f452defec49a7f0d284892780237d48fa8ab3bd6b6`.

`digitized/` contains only the archived comparison curves required to overlay
the eight diagnostics represented in Figure 4: DIC, TA, hydrogen ion, gas
exchange, carbonate horizons, atmospheric pCO₂, forcing, dissolution, and
burial. These curves are visual checks, not restart data or extra model state.

## Model-definition workbook

`model_definition.xlsx` is the authoritative teaching input for 03/04. It was
created from the preserved Boudreau reservoir/process settings and teaching
feedback parameters; it is not an unchanged file from the archive. The older
reservoir-only `reservoirs.xlsx` is superseded and is not read by the models.

The workbook has six named tables on four sheets:

- `Reservoirs`: `OceanReservoirs`, `Atmosphere`, `BoundaryNodes`.
- `Transport`: `TransportConnections`, one row per directed water transport.
- `GasExchange`: `GasExchangeConnections`, linking the atmosphere to both surface boxes.
- `Parameters`: `ProcessParameters`, typed values with units, roles and descriptions.

Geometry remains explicit in m2 and m3, temperature in degC, pressure in bar,
and initial DIC/TA in umol/kg. Atmospheric size preserves the previous
ESBMTK default of 1.7786e20 mol. Density and water mass come from ESBMTK in the
notebooks. No area-fraction or depth-based geometry input is exposed.

Process rates occur once in Parameters; connection rows refer to their names.
The adapter validates units, IDs, ordering and per-box water balance before
constructing any model. The supported network retains the three benchmark box
IDs and the specialized biological/weathering/compensation equations. Additional
balanced physical transports among those boxes are supported and also used by
the diagnostic storage calculation. This is a teaching-model specification,
not a general replacement for ESBMTK's complete Python interface.

Baseline PIC export is derived from POC export and the PIC/POC ratio. Weathering
TA is twice weathering DIC. Excel shows the two derived fluxes as formulas;
Python recomputes them from the literal inputs rather than reading cached
formula results. PIC export and dissolution always link DIC and TA 1:2.

Save edits and rerun notebook setup and dependent cells. The archived restart
supersedes workbook initial concentrations in 03 and complete-model runs of 04.
The dormant attribution extension starts its separate tagged calculation from
the workbook state. Altered baseline geometry,
thermodynamics, transport or process rates requires a new stationary restart
and matched control. Forcing controls and feedback switches remain in 04.
