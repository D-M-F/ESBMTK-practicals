# ESBMTK carbon-cycle practicals 00–04

This repository contains a five-notebook learning sequence. The guided 01–04
core moves from a failed TA-free air–sea model to scaffolded construction of a
Boudreau-like model, then matched carbon and alkalinity forcing experiments.
Notebook 00 provides student and instructor answer sheets for the supplied
exercise 9 (a–h), increasing atmospheric CO2 and ocean acidification.

See [TEACHING_GOALS.md](TEACHING_GOALS.md) for the maintained learning goals,
required/optional tasks and four-hour timetable. The timetable reserves 20 minutes
for 00's eight-part question set; that allocation needs confirmation through course
planning. 01–04 require an estimated 185 minutes of notebook work, plus introduction,
break and synthesis. Timings need a student pilot.

The [pre-revision archive](archive/2026-09-16_before_guided_revision/ARCHIVE.md)
preserves the previous 01–04 notebooks, dependencies, data and teaching documents
with checksums. It is a frozen snapshot, separate from active teaching sources.

| Notebook | Main task |
| --- | --- |
| [`00_PyCO2SYS.ipynb`](notebooks/00_PyCO2SYS.ipynb) | Exercise 9: pH, saturation, CO2/temperature/salinity comparisons and inferred alkalinity |
| [`01_single_box_air_sea_CO2.ipynb`](notebooks/instructor/01_single_box_air_sea_CO2.ipynb) | Diagnose missing TA, infer it, and verify conservation and equilibrium controls |
| [`02_two_layer_ocean_carbon_pump.ipynb`](notebooks/instructor/02_two_layer_ocean_carbon_pump.ipynb) | Verify a conservative extension, calibrate an effective pump, and audit a finite carbon signal |
| [`03_boudreau_three_box_model.ipynb`](notebooks/instructor/03_boudreau_three_box_model.ipynb) | Complete four reservoir/flux mappings and verify the constructed model |
| [`04_pump_strength_OA_OAE.ipynb`](notebooks/instructor/04_pump_strength_OA_OAE.ipynb) | Specify carbon/TA forcing, check budgets and interpret matched OA/OAE responses |

## Teaching boundary

Notebooks 00–02 use [`teaching_config.py`](teaching_config.py) for shared carbonate
choices (constants 10, seawater pH scale 2, buffer mode 1). In 01/02, uniform
16 °C, salinity 35 and 0 bar isolate carbon redistribution. ESBMTK supplies the
density. For 02, the supplied layer split is derived from the prescribed pumped
ocean/atmosphere inventory ratio 62.4 and reference DIC values (about 298.75 m
surface depth with the defaults). It is labelled as ratio-derived teaching geometry.
[`simple_models.py`](simple_models.py) provides readable model and budget helpers.
The native ESBMTK objects remain visible in the construction exercises.

For 00, open the [student answer sheet](notebooks/student/00_PyCO2SYS.ipynb) or
the [instructor answers](notebooks/instructor/00_PyCO2SYS.ipynb). Students receive
one unrelated PyCO2SYS usage example, documentation links and blank answers for
a–h. The exercise uses a 15 °C baseline and dry-air xCO2 in ppm (type 9), with
unchanged `C.chemistry`; the instructor sheet includes the 18 °C warming case.
All states are static equilibrium comparisons, and saturation-target TA is an
inference, not a closed carbon budget or an assessment of reef intervention feasibility.

Notebook 01 begins with TA = 0. Its buffered rerun is a calibration and
cross-implementation check. Notebook 02 asks students to derive the effective
pump coefficient from a first-order export assumption, an observed stationary
DIC ratio and an independently chosen mixing rate.
Its atmospheric response is conditional; restoring 280 ppm with the calculated
carbon addition from 62.4 and the actual baseline inventory is a forcing/conservation check, not independent pump
validation. Distinct-pump attribution, OA/OAE science and sediments remain in 03/04.

Notebook 01 supplies construction and comparison code; students select the chemistry
input pair and explain the missing TA and rate/equilibrium distinction. Notebook 02
provides constructor templates while retaining student-derived pump strength and
carbon addition. Plotting and numerical audits are supplied throughout.

Notebook 03 has four mapping exercises: reservoirs, physical transports, POC/PIC
choices and linked rates, and gas exchange. Native ESBMTK calls stay visible;
Model setup, repeated loops, chemistry/sediment wiring and weathering construction
are supplied. Students trace all arrows and inspect graph/stationarity checks.
The instructor-only final cell compares against the reusable implementation.

Notebook 04 treats compatibility code as supplied infrastructure:

- [`model.py`](model.py) constructs and runs the reusable model;
- [`presets.py`](presets.py) defines the benchmark, the closed storage
  decomposition, and biological-pump variants;
- [`pump_functions.py`](pump_functions.py) supplies normalized pCO₂/CO₂(aq)
  soft-tissue feedback and TA–DIC carbonate feedback;
- [`storage_decomposition.py`](storage_decomposition.py) transports diagnostic
  gas-exchange, soft-tissue, and carbonate tags through the realized baseline;
- [`scenarios.py`](scenarios.py) adds idealized atmospheric-carbon or ocean-TA signals.
- [`teaching_plots.py`](teaching_plots.py) supplies the core figures;
- [`teaching_audits.py`](teaching_audits.py) checks complete-model carbon/TA budgets
  including forcing, weathering and net burial.

Core 04 has two short code exercises: convert prescribed inventories and choose
the forcing species/endpoints. Its fixed-pump control/OA/OAE cases retain the
archived 4025 Gt-C post-1800 pulse and same-shape 10 Pmol TA-equivalent input.
Students inspect budgets, follow the full eight-panel OA/OAE response figures
through a guided reading route, and interpret atmospheric CO2, surface pH, deep DIC
and dissolution/net-burial anomalies. Chemical horizons and the sediment snowline
connect the deep response to sediment memory. The former extension Part II is now
in core 04; plotting is supplied and the same four short answers cover interpretation.
The full forcing history, including the
small pre-1800 tail, enters the time-resolved inventory audit.

The self-contained [optional extension](notebooks/instructor/extensions/04_attribution_and_feedbacks.ipynb)
retains Part I's process-tagged storage and Part III's biological feedback
experiments. Only supplied prerequisite runs of the fixed reference cases remain
there; Part II's response explanations and full figures are in core 04.
The extension is outside the four-hour core and is not executed by core 04.
Tags are bookkeeping attribution of one trajectory; $G$ means gas
exchange. Feedback laws remain hypotheses and preserve PIC's 1:2 DIC–TA coupling.
Detailed sediment equations are [optional reference](ref/sediment_reference.md).
The 03/04 benchmark retains its box-specific thermodynamic conditions.

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
ESBMTK functions. Native POC/PIC and chemistry calls remain visible; sediment
equations are optional reference. Notebook 04 reuses the verified definition for matched
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
them in 03 and in the complete-model runs of 04; the optional tagged experiment starts from the
workbook concentrations. Retain the supplied values for benchmark reproduction.
Changed geometry, chemistry, transport or baseline process rates needs a new
stationary restart and matching control before interpreting perturbations.

## Instructor and student copies

The instructor notebooks for 00–04 and the optional extension are the source of truth. Generate distributable,
output-free student copies with:

```powershell
python scripts/build_student_notebooks.py
```

The builder replaces marked code and Markdown solutions with exercise
placeholders and removes cells tagged `solution-only`. Edit the instructor
notebooks, not the generated files under `notebooks/student/`.
The original top-level 00/01/02 paths are launchers linking to both copies.

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

The notebook checker executes core 00–04 instructor code cells in fresh processes
and saves plots under `tmp/notebook_qa/` without
adding outputs to teaching sources. Tests cover 01/02 carbon and TA inventories,
implemented reservoir masses, no-pump equivalence, fitted-ratio labelling, signal
integration and the calibrated return. Run in the activated Conda environment:
its `Library/bin` must be on `PATH` on Windows for numerical-library DLLs.
Use `python scripts/check_notebooks.py --include-extensions` to also verify the
optional attribution/feedback notebook. Active build/check defaults never traverse
the archive. Update `TEACHING_GOALS.md` whenever later teaching changes alter
learning outcomes, required work or timing.

## Scientific scope

The unit-strength, feedback-disabled configuration reproduces the ESBMTK
Boudreau benchmark. Modified configurations are described as *Boudreau-like
experiments*. OA is forced by adding atmospheric carbon, not by prescribing pH.
OAE is an idealized pure-TA addition and directly adds no DIC. State-dependent
laws are transparent mechanism hypotheses rather than calibrated ecosystem
models, and every forced result is compared with a matched unforced control.
