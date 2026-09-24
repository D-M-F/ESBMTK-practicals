# ESBMTK carbon-cycle practicals 00–04

This repository contains a five-notebook learning sequence. The guided 01–04
core moves from a failed TA-free air–sea model to scaffolded construction of a
Boudreau-like model, then matched carbon and alkalinity forcing experiments.
Notebook 00 provides student and instructor answer sheets for the supplied
exercise 9 (a–h), increasing atmospheric CO2 and ocean acidification.

See [TEACHING_GOALS.md](TEACHING_GOALS.md) for the maintained learning goals,
required/optional tasks and four-hour timetable. The timetable reserves 20 minutes
for 00's eight-part question set; that allocation needs confirmation through course
planning. 01–04 require an estimated 190 minutes of notebook work, plus introduction,
break and synthesis. Timings need a student pilot.

The [textbook review](ref/textbook_exercise_review.md) documents the implemented
01–04 refinements: chemical TA conservation, effective export versus production,
local DIC–TA process arrows, and fixed biology versus forcing responses.
In 01, a supplied offline explorer links a rotatable DIC–TA–pCO2 surface,
Deffeyes-style pCO2 contours and constant-TA slices before the existing curve
exercise. Run its cell in JupyterLab; no widget extension or extra package is
needed. Its **Save offline copy** button downloads a standalone browser version.
An [instructor preview](output/dic-ta-pco2-explorer.html) can be regenerated with
`python scripts/build_carbonate_explorer.py` in the activated course environment.
In 03, students reuse pCO2 contours for the existing flux-specification exercise;
the 55-minute target needs a pilot of this revised reasoning load.

The [pre-revision archive](archive/2026-09-16_before_guided_revision/ARCHIVE.md)
preserves the previous 01–04 notebooks, dependencies, data and teaching documents
with checksums. It is a frozen snapshot, separate from active teaching sources.

| Notebook | Main task |
| --- | --- |
| [`00_PyCO2SYS.ipynb`](notebooks/00_PyCO2SYS.ipynb) | Exercise 9: pH, saturation, CO2/temperature/salinity comparisons and inferred alkalinity |
| [`01_single_box_air_sea_CO2.ipynb`](notebooks/instructor/01_single_box_air_sea_CO2.ipynb) | Diagnose missing TA, infer it, and verify conservation and equilibrium controls |
| [`02_two_layer_ocean_carbon_pump.ipynb`](notebooks/instructor/02_two_layer_ocean_carbon_pump.ipynb) | Verify a conservative extension, calibrate an effective pump, and audit a finite carbon signal |
| [`03_boudreau_three_box_model.ipynb`](notebooks/instructor/03_boudreau_three_box_model.ipynb) | Reconstruct a schematic, reconcile Excel inputs, complete four mappings and audit the model |
| [`04_pump_strength_OA_OAE.ipynb`](notebooks/instructor/04_pump_strength_OA_OAE.ipynb) | Specify carbon/TA forcing, check budgets and interpret matched OA/OAE responses |

## Teaching boundary

### Shared coding reference for students

Keep [From conceptual model to code](ref/modelling_cheatsheet.md) or its
[two-page printable handout](output/pdf/modelling_cheatsheet.pdf) beside 01–04.
It maps scientific decisions to ESBMTK objects, traces a separate passive-tracer
example from diagram to balance to executable code, and explains Python patterns,
input files, execution order, restarts and budget checks. The worked example is
optional reference, not another exercise; run it from the repository root in
ESBMTK314 if useful. It does not contain the 02 derivations or exercise solutions.

The [box-to-code diagram](ref/figures/box_code_map.svg) labels geometry, tracer
states, initial values, conditions and connection arguments beside their visual
elements. Its attached legend distinguishes carbonate calculations, species
coupling and external forcing. Solid arrows carry material; dashed arrows carry
information. The [01 worked-example diagram](ref/figures/01_air_sea_code_map.svg)
uses the same conventions and the actual atmosphere/ocean object names. Both are
also supplied as PNGs for notebook display; 01 embeds its diagram alongside the
existing construction exercise. These replace textual mappings within the same
reference/orientation activity, with no extra student task.

Code cells distinguish **Choose and explain**, **Understand and run**, and
**Supplied implementation**. Labels identify how to use a cell; scientific
interpretation can still be required when its code is supplied. Students are
assessed on conceptual mapping and evidence, not memorised ESBMTK syntax.
Introduce the sheet during 01's existing diagram/worked-example activity;
the orientation shares its 10-minute allocation and needs a novice-student pilot.

The Markdown owns the handout prose; `scripts/build_coding_diagrams.py` owns the
diagram layouts and labels. Maintainers can regenerate both diagrams and the PDF with
`python scripts/build_modelling_cheatsheet.py` using an authoring environment
with `reportlab`, `pypdf` and Poppler's `pdftoppm` on PATH; these are not student
prerequisites. The same diagram source produces SVG/PNG assets and vector PDF
content. The builder requires exactly two pages. Render and visually inspect
both pages and the notebook diagram after edits.

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
unchanged `config.chemistry`; the instructor sheet includes the 18 °C warming case.
All states are static equilibrium comparisons, and saturation-target TA is an
inference, not a closed carbon budget or an assessment of reef intervention feasibility.

Notebook 01 begins with a fictional verification experiment by a new ESBMTK
modeller, using idealized saline water with TA = 0. Students critique whether
correct code and the target-derived total carbon guarantee the reference
partition, then use budget checks to distinguish implementation from physical
assumptions. Its buffered rerun is a calibration and cross-implementation check.
Notebook 02 asks students to derive the effective
pump coefficient from a first-order export assumption, an observed stationary
DIC ratio and an independently chosen mixing rate.
Its atmospheric response is conditional; restoring 280 ppm with the calculated
carbon addition from 62.4 and the actual baseline inventory is a forcing/conservation check, not independent pump
validation. Distinct-pump attribution, OA/OAE science and sediments remain in 03/04.

Notebooks 00–02 import the shared teaching configuration as `config`, keeping
its code name distinct from carbon-inventory notation such as $C_0$.

Notebook 01 supplies construction and comparison code; students reuse their 00
skills to write a fully masked TA calculation from the two reference targets,
then complete a forward DIC/TA-to-pCO2 call in a supplied loop. They use the
curves and a supplied atmospheric conservation line to explain carbon uptake
before testing the revised model. Construction, plotting and conversions are
supplied; scientific choices and interpretation remain student work. The
provisional 40-minute route takes five minutes from the completion buffer and
still needs a student pilot. Notebook 02
provides constructor templates while retaining student-derived pump strength and
carbon addition. Plotting and numerical audits are supplied throughout.

Notebook 03 starts with paired DIC/TA flux equations and a labelled schematic,
then reconciles that specification with named Excel records. The simplified
diagrams focus on boxes and process arrows, using Q for water volume transport;
the companion table contains the paired tracer equations. Corrected source
notes identify F5 organic export, PIC/POC and inorganic weathering carbon.
Dissolution has a supplied dependency function, with signed net burial
distinguished from an extra sink. A short J/m rule separates amount fluxes
from concentration tendencies; the contour exercise interprets those same laws.
Four native mapping exercises cover reservoirs, transport endpoints/species/law,
POC/PIC choices/law and linked rates, and gas exchange. Native calls stay visible;
Model setup, repeated loops, chemistry/sediment wiring and weathering construction
are supplied. Students complete one boundary budget and inspect graph, time-resolved
carbon/TA and short restart-drift checks. Conservation does not establish the
correctness of an internal law; short drift does not prove long-term stability.
The instructor-only final cell compares against the reusable implementation.

Notebook 04 treats compatibility code as supplied infrastructure:

- [`model.py`](model.py) constructs and runs the reusable model;
- [`presets.py`](presets.py) loads the benchmark and prepares independent cases;
- [`scenarios.py`](scenarios.py) adds idealized atmospheric-carbon or ocean-TA signals.
- [`teaching_plots.py`](teaching_plots.py) supplies the core figures;
- [`teaching_audits.py`](teaching_audits.py) checks complete-model carbon/TA budgets
  including forcing, weathering and net burial.

Core 04 has two short code exercises: convert prescribed inventories and choose
the forcing species/endpoints. Its fixed-pump control/OA/OAE cases retain the
archived 4025 Gt-C post-1800 pulse and same-shape 10 Pmol TA-equivalent input.
Students specify the experiment on their completed diagram and predict responses
before running. The actual forcing shapes appear in B1 before matched-control
anomalies in B2; full figures then support critical-depth, sediment-memory and
benchmark interpretation. Four short answers address timing, carbon uptake/TA,
critical depths and OA/OAE asymmetry, with the assumptions and limits of these runs.
Plotting is supplied; no fourth core run is required. The 03/04 allocations remain
provisional and need a student pilot after these task replacements.
The full forcing history, including the
small pre-1800 tail, enters the time-resolved inventory audit.

The [04 extension](notebooks/instructor/extensions/04_attribution_and_feedbacks.ipynb)
is retained but dormant. Its teaching goals are temporarily suspended until the
user explicitly asks to turn them on again. Current plans exclude its settings
and exercises; core 04's matched OA/OAE work remains active.
Detailed sediment equations are [optional reference](ref/sediment_reference.md).
The 03/04 benchmark retains its box-specific thermodynamic conditions.

The separate [independent-model starter](notebooks/student/extensions/05_independent_model.ipynb)
([instructor example](notebooks/instructor/extensions/05_independent_model.ipynb))
offers a provisional 60–90-minute optional activity: one question, one changed
assumption, native scientific choices, a matched comparison, budgets and one
interpreted figure. Its example compares fixed and first-order export in the
mass-consistent 02 model. It is outside the four-hour core and does not run from 04.

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

Notebook 03 first shows geometry and baseline parameters. Students reconstruct
their diagram, then reveal connection records for reconciliation. A partial
reservoir example supplies T/S/P syntax before students
construct reservoirs, transport and gas-exchange connections using standard
ESBMTK functions. Native POC/PIC and chemistry calls remain visible; sediment
equations are optional reference. Notebook 04 reuses the verified definition for matched
cases; forcing amounts and endpoints remain student choices, while baseline
pump strengths are fixed and feedback experiments stay in the optional extension.
The optional diagnostic transport operator uses the same Excel arrows
and ESBMTK-derived water masses as the physical calculation.

The [student flux worksheet](outputs/03_04_flux_specification/student.xlsx) and
[instructor reference](outputs/03_04_flux_specification/instructor.xlsx) connect
process IDs, scientific properties and workbook/code ownership. These are separate
teaching documents: editing them does not change model inputs. Students may use
the same table in notebook Markdown; Excel editing is optional. No numerical
baseline input is duplicated as an independent setting. See the
[schematic guide](ref/boudreau_diagrams.md) for sources and regeneration.

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

Core 00–04 use pale-gold key terms, blue question panels and purple written
instructor-answer panels. The [notebook reading-cue guide](ref/notebook_readability.md)
documents the markup and masking rules for lecturers and maintainers; `AGENTS.md`
requires future edits to preserve this convention.

## Environment and verification

The setup material is separated from the exercises. A temporary
[start-and-transition guide](ref/setup_only_start_here.md) explains how students
choose one installation route, verify JupyterLab and later move to the complete
GitHub repository. The setup-only ZIP is assembled from a fixed allow-list by
`python scripts/build_setup_package.py --rebuild-pdfs`; it contains no exercise
notebooks, model data or instructor material.

Printable student handouts: [uv setup (PDF)](output/pdf/student_setup_uv.pdf)
and [Anaconda setup (PDF)](output/pdf/student_setup_anaconda.pdf). Their Markdown
sources remain valid for either the setup-only folder or the eventual complete
repository. [`JUPYTER_BASICS.ipynb`](JUPYTER_BASICS.ipynb) introduces cell
execution and command-mode shortcuts, then checks the environment and the
labelled [`workbook_probe.xlsx`](setup_assets/workbook_probe.xlsx). Instructor
validation and dependency-maintenance notes are kept separately in
[`ref/setup_instructor_validation.md`](ref/setup_instructor_validation.md).

The locked uv environment was installed from scratch on Windows with managed
Python 3.14.7. Numerical/chemistry/workbook/plot checks, all five core instructor
notebooks and a JupyterLab launch/kernel/shutdown/relaunch cycle pass. The
Anaconda recipe was also created from scratch from the extracted setup-only ZIP
on Windows/Python 3.14; package checks, environment checks, kernel registration,
the Jupyter basics notebook and an HTTP JupyterLab launch pass. macOS and Linux
still need instructor pilots. ESBMTK314 remains the instructor reference environment.

Students who already use Anaconda/Miniconda can use the
[Anaconda setup guide](ref/anaconda_setup.md) and supplied
[`environment-anaconda.yml`](environment-anaconda.yml). The alternative recipe
creates a separate `esbmtk-practicals` environment and includes kernel-selection
instructions. uv users create a new project-local `.venv` after moving to the
complete repository; Conda users reuse the named environment unless dependency
changes require an explicit update. The instructions below describe the existing
verified instructor environment.

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

For scripts or a terminal where the environment is not already activated, use
Conda's environment launcher (with `conda` available on PATH):

```powershell
conda run -n ESBMTK314 --no-capture-output python -m jupyterlab
```

Calling the environment's `python.exe` by its full path does **not** activate
its DLL search paths. On this Windows installation, an unactivated NumPy linear
solve reproduces error `0xc06d007f` while resolving an OpenMP function through
`libiomp5md.dll` to `libomp.dll`; the same check and notebook 01's Jupyter
execution pass under `conda run`. Launch Jupyter from the intended environment
and select its ESBMTK314 kernel. See the
[environment diagnosis and setup status](ref/environment_setup_proposal.md)
for the evidence and the separately tested uv route without Anaconda.

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
integration and the calibrated return. Run in the activated Conda environment
(its `Library/bin` must be on `PATH` on Windows for numerical-library DLLs),
or prefix each command with `uv run --locked` for the supplied uv environment.
Use `python scripts/check_notebooks.py --include-extensions` to also verify the
optional attribution/feedback notebook. Active build/check defaults never traverse
the archive. Update `TEACHING_GOALS.md` whenever later teaching changes alter
learning outcomes, required work or timing.

## Scientific scope

For review without Jupyter, extract the [instructor PDF pack, 00–04](output/ESBMTK-instructor-review-00-04.zip)
and open `START_HERE.txt`. The five PDFs include freshly executed results,
instructor solutions and expanded optional notes. The pack also includes the
offline carbonate explorer and directly cited local references. It contains
answers and is intended for lecturers. See [export instructions](ref/instructor_review.md)
for rebuilding it from the current instructor sources.

The unit-strength, feedback-disabled configuration reproduces the ESBMTK
Boudreau benchmark. Modified configurations are described as *Boudreau-like
experiments*. OA is forced by adding atmospheric carbon, not by prescribing pH.
OAE is an idealized pure-TA addition and directly adds no DIC. State-dependent
laws are transparent mechanism hypotheses rather than calibrated ecosystem
models, and every forced result is compared with a matched unforced control.
