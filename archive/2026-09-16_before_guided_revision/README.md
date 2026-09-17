# ESBMTK carbon-cycle practicals 00–04

This repository contains a five-notebook learning sequence. It moves from
carbonate chemistry and a failed TA-free air–sea model to a student-built Boudreau-2010-like model,
then uses that verified model for carbon-storage, forcing, and biological-feedback
experiments.

| Notebook | Main task |
| --- | --- |
| [`00_PyCO2SYS.ipynb`](notebooks/00_PyCO2SYS.ipynb) | Calculate carbonate variables from two inputs and illustrate buffering |
| [`01_single_box_air_sea_CO2.ipynb`](notebooks/instructor/01_single_box_air_sea_CO2.ipynb) | Diagnose missing TA, infer it, and verify conservation and equilibrium controls |
| [`02_two_layer_ocean_carbon_pump.ipynb`](notebooks/instructor/02_two_layer_ocean_carbon_pump.ipynb) | Verify a conservative extension, calibrate an effective pump, and audit a finite carbon signal |
| [`03_boudreau_three_box_model.ipynb`](notebooks/instructor/03_boudreau_three_box_model.ipynb) | Reconstruct the complete Boudreau-like model from its flux diagram |
| [`04_pump_strength_OA_OAE.ipynb`](notebooks/instructor/04_pump_strength_OA_OAE.ipynb) | Attribute storage with process tags in one G+S+C model, reproduce the OA pulse, compare OAE, and test biological feedbacks |

## Teaching boundary

Notebooks 00–02 use [`teaching_config.py`](teaching_config.py) for shared carbonate
choices (constants 10, seawater pH scale 2, buffer mode 1). In 01/02, uniform
16 °C, salinity 35 and 0 bar isolate carbon redistribution. ESBMTK supplies the
density. For 02, the supplied layer split is derived from the prescribed pumped
ocean/atmosphere inventory ratio 62.4 and reference DIC values (about 298.75 m
surface depth with the defaults). It is labelled as ratio-derived teaching geometry.
[`simple_models.py`](simple_models.py) provides readable model and budget helpers.
The native ESBMTK objects remain visible in the construction exercises.

Notebook 01 begins with TA = 0. Its buffered rerun is a calibration and
cross-implementation check. Notebook 02 asks students to derive the effective
pump coefficient from a first-order export assumption, an observed stationary
DIC ratio and an independently chosen mixing rate.
Its atmospheric response is conditional; restoring 280 ppm with the calculated
carbon addition from 62.4 and the actual baseline inventory is a forcing/conservation check, not independent pump
validation. Distinct-pump attribution, OA/OAE science and sediments remain in 03/04.

Notebook 03 makes students construct the baseline themselves. Marked exercises
cover the `Model`, reservoirs, physical transports, POC/PIC connections,
carbonate systems, gas exchange, and weathering. Progressive assertions help
them check each diagram-to-code translation. The instructor-only final cell
compares the result with the reusable implementation.

Notebook 04 treats compatibility code as supplied infrastructure:

- [`model.py`](model.py) constructs and runs the reusable model;
- [`presets.py`](presets.py) defines the benchmark, the closed storage
  decomposition, and biological-pump variants;
- [`pump_functions.py`](pump_functions.py) supplies normalized pCO₂/CO₂(aq)
  soft-tissue feedback and TA–DIC carbonate feedback;
- [`storage_decomposition.py`](storage_decomposition.py) transports diagnostic
  gas-exchange, soft-tissue, and carbonate tags through the realized baseline;
- [`scenarios.py`](scenarios.py) adds idealized atmospheric-carbon or ocean-TA signals.

Notebook 04 labels $G$ as gas exchange, rather than conflating it with a
temperature/circulation sensitivity. It first solves one closed G+S+C model and
diagnoses additive bookkeeping tracers under the same realized gas exchange,
THC, and mixing. Low-latitude-referenced tag contrasts form the three-box
storage profile. It then restores weathering, dissolution, and burial for the
archived 4025 Gt-C OA pulse and a
same-shape 10 Pmol-equivalent OAE experiment. Only the biological pumps become
state dependent; temperature, THC, and high-latitude mixing stay fixed.

The PIC feedback returns DIC and TA fluxes together, preserving exact 1:2
stoichiometry, and its evaluated time series is passed to carbonate-compensation
post-processing. These compatibility details remain visible and testable but
are not student fill-in exercises. Notebook 04 masks only a tag-closure
calculation and the forcing-inventory calculation, plus explanatory responses.
Parts I and II are the core matched-control analysis; Part III's state-dependent
feedbacks are an optional extension. The 03/04 benchmark retains its distinct
box-specific thermodynamic conditions and carbonate settings.

## Shared Excel model definition for 03/04

Open [`model_definition.xlsx`](data/Boudreau_2010/model_definition.xlsx).
This workbook is the authoritative baseline model input, replacing the earlier
reservoir-only `reservoirs.xlsx` (retained as a superseded file and not loaded).

| Worksheet | Contents |
| --- | --- |
| Reservoirs | Three ocean boxes, atmosphere, weathering source and burial sink |
| Transport | Directed circulation/mixing arrows and references to their shared rate parameters |
| GasExchange | Atmosphere–surface connections and their gas-transfer parameter |
| Parameters | Transport, export, weathering, compensation, chemistry and optional feedback parameters |

[`reservoir_inputs.py`](reservoir_inputs.py) reads the reservoir records;
[`model_inputs.py`](model_inputs.py) validates and translates the complete
definition. [`presets.py`](presets.py) loads fresh inputs and creates independent
experiment variants, with no duplicate numerical baseline settings.

Save Excel edits, then rerun notebook setup and all dependent cells. Both
notebooks call `load_boudreau_parameters(WORKBOOK)` to read a fresh snapshot.
Keep named tables, column units and required box IDs intact. The `Order` column
preserves construction order after sorting. Transport parameters are entered
once on Parameters and referenced by name on each arrow. The loader rejects
unknown/duplicate connections, missing values, incorrect units and water
imbalance in any fixed-volume box. Both mixing directions are explicit.

Input cells require literal values. The derived PIC and weathering-TA readouts
use Excel formulas; Python derives these values from the same inputs, without
relying on cached Excel results. Baseline PIC = POC × PIC/POC ratio, and carbonate
weathering TA = 2 × weathering DIC. PIC's DIC–TA fluxes always remain linked 1:2,
including with state-dependent export.

Notebook 03 shows imported tables and one reservoir mapping before students
construct reservoirs, transport and gas-exchange connections using standard
ESBMTK functions. Specialized POC/PIC, chemistry and sediment equations remain
visible in the notebook. Notebook 04 reuses the verified definition for matched
cases; forcing amounts, pump strengths and feedback switches remain in its
experiment cells. Its diagnostic transport operator uses the same Excel arrows
and ESBMTK-derived water masses as the physical calculation.

**Geometry stays explicit.** The adapter passes the workbook's area and volume
directly to ESBMTK. Students do not need `area_percentage`, depth boundaries or a
hypsometry conversion. As in 01/02, geometry is supplied explicitly; 03/04 retain
their distinct benchmark sizes and box-specific thermodynamic settings.

For maintainers: the native depth-based Excel reader instead scales ESBMTK's
built-in global-ocean hypsometry. Its reference area depends on depth, unlike
the independently prescribed whole-ocean area in 01/02. That alternative is not
used here. The small adapter retains the named-table layout, explicit units,
validation, stable object IDs and benchmark construction order, then calls
`initialize_reservoirs`, `create_bulk_connections` and `Species2Species`.

Workbook concentrations are **initial inputs**. The archived restart replaces
them in 03 and in the complete-model runs of 04; 04 Part I starts from the
workbook concentrations. Retain the supplied values for benchmark reproduction.
Changed geometry, chemistry, transport or baseline process rates needs a new
stationary restart and matching control before interpreting perturbations.

## Instructor and student copies

The instructor notebooks for 01–04 are the source of truth. Generate distributable,
output-free student copies with:

```powershell
python scripts/build_student_notebooks.py
```

The builder replaces marked code and Markdown solutions with exercise
placeholders and removes cells tagged `solution-only`. Edit the instructor
notebooks, not the generated files under `notebooks/student/`.
The original top-level 01/02 paths are launchers linking to both copies.

## Environment and verification

From an Anaconda prompt:

```powershell
conda activate ESBMTK314
cd D:\ALK\TA\BGC\ESBMTK-practicals
python -m pip install -r requirements-excel.txt
jupyter lab
```

Use the `ESBMTK314` environment's Python 3.14 kernel. The verified model package is
ESBMTK 0.14.3.1.post0. `run_model()` includes the needed Windows equations-file
workaround without changing equations or solver settings.

Run the tests with:

```powershell
python -m unittest discover -s tests -v
python scripts/check_notebooks.py
```

The 1000 kyr baseline is the scientific regression. The archived restart under
[`data/Boudreau_2010/steady_state`](data/Boudreau_2010/steady_state) keeps the
classroom notebooks fast; it supplies initial state but never replaces the
model structure students build.

The notebook checker executes all 00–04 instructor code cells in fresh processes,
including optional feedbacks, and saves plots under `tmp/notebook_qa/` without
adding outputs to teaching sources. Tests cover 01/02 carbon and TA inventories,
implemented reservoir masses, no-pump equivalence, fitted-ratio labelling, signal
integration and the calibrated return. Run in the activated Conda environment:
its `Library/bin` must be on `PATH` on Windows for numerical-library DLLs.

## Scientific scope

The unit-strength, feedback-disabled configuration reproduces the ESBMTK
Boudreau benchmark. Modified configurations are described as *Boudreau-like
experiments*. OA is forced by adding atmospheric carbon, not by prescribing pH.
OAE is an idealized pure-TA addition and directly adds no DIC. State-dependent
laws are transparent mechanism hypotheses rather than calibrated ecosystem
models, and every forced result is compared with a matched unforced control.
