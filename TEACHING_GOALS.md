# Teaching goals and workload: practicals 00–04

Last updated: 2026-09-22. This is the maintained summary of the **implemented**
student route, required learning outcomes and workload. Update it in the same
change whenever notebook tasks, scope, prerequisites or timing change. Record
pending ideas and verification evidence in `WORKPLAN.md`; scientific rationale
and boundaries remain in `ref/design.md`. Archive snapshots are historical.

## Scope and time budget

Notebook **00 now provides answer sheets for the supplied exercise 9 (a–h)**.
The student version has one unrelated PyCO2SYS example, documentation links and
blank calculation/answer cells; the instructor version has full numerical and
written answers. The eight parts include temperature/salinity comparisons,
historical CO2, mineral saturation, a high-CO2 endpoint and a saturation-target
alkalinity calculation. The existing 20-minute slot remains a provisional
reservation, not a verified estimate for this now-explicit workload. Pilot all
eight parts; if they take longer, extend the session or explicitly reallocate
time. No 01–04 work has been removed to make room. These are planning estimates,
not measured student completion times.

| Activity | Minutes | Required work |
| --- | ---: | --- |
| Introduction and environment check | 10 | Identify states, arrows and boundary |
| 00: exercise 9 answer sheet | 20 reserved | Eight chemistry parts (a–h); duration needs a pilot |
| 01: missing alkalinity | 40 | TA inference; pCO2–DIC curves; model interpretation |
| 02: layers and effective pump | 55 | Scaffolded connections; two derivations; budget interpretation |
| Break | 10 | |
| 03: complete-model mapping | 55 | Four mapping tasks; graph/stationarity verification |
| 04: carbon versus alkalinity forcing | 40 | Two short code tasks; matched-response interpretation |
| Synthesis and completion buffer | 10 | Trace a flux pathway and its budget |
| **Total** | **240** | Includes the provisional 00 allocation |

01–04 contain 190 minutes of notebook work; with introduction, break and synthesis
their allocation is 220 minutes. Installation is a course prerequisite: provide
a working course environment before class, using the supplied uv route or
Anaconda alternative; ESBMTK314 remains the instructor reference. Required reading and short answers
fit inside the notebook allocations; no extra report or extension is required.
Pilot with a student unfamiliar with the code before treating these timings as
established. Record measured times here after the pilot.

An optional Anaconda installation recipe and student guide now support a
separate `esbmtk-practicals` environment with the same Python line and pinned
ESBMTK/PyCO2SYS versions. This recipe still requires fresh-installation and
cross-platform pilots; ESBMTK314 remains the verified instructor reference.
Setup and instructor validation happen before class, with no new student
exercise or change to the practical's provisional timetable.
The three-page uv and Anaconda PDF handouts under `output/pdf/` support
that same pre-class setup. The uv route now supplies `pyproject.toml`, `uv.lock`,
`.python-version` and `scripts/check_environment.py`, and downloads Python itself.
Both guides explain terminals and folders, confirm successful installation,
and separate opening notebooks from stopping/restarting the JupyterLab server.
The Anaconda guide explains environment activation and uses the same supplied
environment checker; its Markdown owns the student PDF text.
A fresh Windows uv environment passes numerical/chemistry/workbook/plot checks,
all five core instructor notebooks and an actual JupyterLab kernel and
launch/shutdown/relaunch check. macOS/Linux and novice-student setup pilots remain
required. Setup time stays separate from the unchanged practical timetable.

## Common method and learning checks

Use **predict → map → run → check → explain**. Each notebook identifies required
work and a stopping point. Students choose scientific fields while supplied code
handles loops, parsing, units, plotting, restarts and numerical compatibility.
Native constructors remain visible wherever reservoir/flux mapping is taught.

Students should explain one whole-system conservation equation in 01, then read
supplied time-resolved audits in later notebooks. A successful run alone is not
evidence that its diagram, budget or scientific interpretation is correct.

Use inputs minus outputs consistently in the 01–03 conceptual budgets: separate
air–sea invasion/outgassing and downward/upward mixing terms, with each transfer
leaving one box and entering another. Introduce net fluxes afterward as differences
of those terms. The effective pump is one directed surface-to-deep transfer.
Explain that native gas exchange evaluates two directional terms in one connection;
the software-object count need not equal the conceptual-arrow count. This replaces
the previous net-first explanations within the existing activities, without new
exercises or prerequisites. Keep the provisional allocations and pilot the revised
reading load alongside the other supplied explanations.

These practicals are ungraded. Use completed mappings, the two 02 derivations
with units and concise interpretations as learning checks. Keep answers in the
notebooks; no separate submission or syntax memorisation is required. Plotting
and numerical internals are supplied. Instructor solutions are masked in the
generated student notebooks.

The shared [coding cheatsheet](ref/modelling_cheatsheet.md), also available as a
[two-page handout](output/pdf/modelling_cheatsheet.pdf), supports the transferable
skill of tracing a scientific assumption through a code object, balance and check.
It covers conceptual mapping, one unrelated passive-tracer example, basic Python
patterns, repository inputs/helpers, execution order and restarts. It supplies
syntax without exposing the 02 derivations or completing the core mapping tasks.
Code cells in 01–04 carry three labels: **Choose and explain** (student scientific
choices), **Understand and run** (supplied steps and their evidence), and
**Supplied implementation** (supporting machinery). Supplied code may still need
scientific explanation; focus on the mapping and evidence.

Offer the sheet as optional lookup support within 01's existing diagram/prediction
and worked-example activity. Introduce essential syntax locally in 01/02 so that
neither notebook requires switching documents. It remains available throughout 02–04. Reading or
executing the separate tracer example is optional, with no extra submission or
required run. This adds reference support within the planned allocation rather
than a new teaching task or prerequisite; the novice-student pilot must check
whether that orientation and the existing activities fit. Notebook 00 is unchanged.

The reference now visualizes box geometry, tracer states, initial concentrations,
conditions and connection arguments with short code labels. An attached process
legend distinguishes carbonate diagnostics, species coupling and external forcing;
solid arrows indicate material transfers and dashed arrows indicate information.
The supplied 01 construction uses the same visual conventions with its actual
object names. These diagrams replace the corresponding mapping tables within
the existing reference and diagram-check activity; no extra answer, run or
prerequisite is added. Keep the provisional allocation and pilot requirement.

## 00 — Exercise 9: atmospheric CO2 and ocean acidification (20 minutes reserved)

**Students should be able to:** select two carbonate-system inputs, use the
PyCO2SYS documentation, calculate seawater-scale pH/DIC/saturation, and interpret
comparisons under explicit equilibrium constraints. Distinguish a prescribed
saturation target and inferred TA from an independently predicted intervention.

**Do:** complete parts a–h using the exercise's TA = 2100 µmol/kg, 15 °C and
salinity 35 baseline; compare 5/25 °C and salinity 32/38, historical CO2 values,
and the 935 ppm endpoint with and without 3 °C warming. Infer TA to restore
present aragonite saturation at both 15 and 18 °C. Give short interpretations.

**Supplied:** environment imports, unchanged `config.chemistry`, one TA/DIC example
with different inputs, and links to parameter and result documentation. Preserve
the prior dry-air xCO2 convention (type 9); explain its difference from pCO2.
All answer calculations, numeric tables and interpretations are instructor-only.

**Evidence:** eight calculations/short answers with units and assumptions. These
are static equilibrium states with DIC allowed to adjust, not a closed carbon
budget, transient forcing or a reef feasibility assessment. Installation is a
prerequisite. The 20-minute reservation must be checked against the complete task.

## 01 — Diagnose missing alkalinity (40 minutes)

**Students should be able to:**

1. Identify atmosphere/ocean states, carbonate diagnostics and the gas connection.
2. Explain why CO2 invasion moves carbon but cannot generate TA.
3. Infer background TA, use pCO2–DIC curves to explain partitioning, and distinguish the fit from prediction.
4. Distinguish initial partition and exchange rate from equilibrium controls.

The opening casts students as new ESBMTK modellers testing a fictional
atmosphere–ocean experiment. A NaCl solution with a trace of dissolved CO2 gives
an intuitive picture of nonzero initial DIC with TA = 0; the calculation retains
its supplied seawater chemistry settings. This replaces the opening explanation
without adding a task or changing its provisional timing. They critique
the expectation that correct code plus the target-derived total carbon must
recover both reference values. The neutral title defers the diagnosis until
after prediction and the first run. Budget checks support implementation
verification; they do not establish physical adequacy or complete code correctness.

**Do:** annotate the supplied construction and explain cancellation of internal
carbon tendencies; predict and diagnose the TA-free run; write the complete
PyCO2SYS TA calculation from DIC/xCO2; complete a DIC/TA-to-pCO2 call
inside a supplied loop and explain the curve intersections; interpret supplied
partition and piston-velocity comparisons. Reuse 00's input-pair and result-extraction skills,
but use 01's shared 16 °C conditions rather than 00's 15 °C baseline.
Allocate 10 minutes to diagram/prediction, 20 to diagnosis/inference/curves,
and 10 to paths. The added five minutes come from the completion buffer;
the session remains four hours. Pilot this allocation with students after 00.

**Supplied:** model construction, target-derived inventory, thermodynamic settings,
comparison runs, DIC grid, repeated loop, conserved-carbon atmosphere line,
unit conversions, plots and carbon/TA audits.

In 00–02, the shared configuration is named `config` in code to distinguish it
from carbon inventories such as $C_0$ and $C_{atm}$. This is a naming clarification;
it changes no scientific inputs, tasks or timing.

Before construction, the worked example states the finite atmospheric size,
evolving dry-air CO2 fraction, inventory-based initial partition and exchange
settings explicitly. The directional gas law shows invasion as solubility times
atmospheric CO2 and outgassing as a function of ocean aqueous CO2, with a note
linking the atmospheric term to the code's dry-air mole fraction and conversions.
This elaborates the existing diagram/prediction reading;
it adds no exercise or prerequisite. Keep the provisional 40-minute allocation
and check this reading load in the novice-student pilot.

Introduce the individual `Species2Species` connection here, before calling
`connect_atmosphere`: a supplied Markdown excerpt shows the helper's actual
constructor and explains endpoints, `ctype`, exchanged species and diagnostic
reference. It is reading support for the existing mapping activity, not a new
coding task. Include this excerpt in the reading-load pilot.

Before its first use, explain that `single_box` packages the construction from
section 2 and returns a fresh, unrun model. Link its parameter changes to initial
TA, carbon partition and exchange rate, including the atmospheric adjustment
that preserves total carbon. This supports the existing rerun/comparison activity;
it adds no task or prerequisite and shares its provisional reading-time allocation.

**Evidence:** a complete TA calculation with the correct inputs, conditions and
units, a forward chemistry call, and explanations beside the diagnosis,
inference, curve interpretation and path-comparison activities. Mask the whole calculation, including input types, solver call and TA
extraction; supply the targets, shared settings, documentation and `inferred_ta`
output name. Also mask the forward chemistry call and pCO2 extraction,
with input/output hints supplied. Place the curve exercise after TA inference
and before the model rerun; mask the causal interpretation as a written answer.
Students infer uptake from the full curves and the common atmosphere line,
not a stated slope ordering or a single local sensitivity. Briefly connect
fractional Revelle sensitivity to lecture slide 46 without adding an R exercise.
Keep the model rerun in a separate supplied cell.

The construction now has short steps for atmospheric initialization, gas exchange,
object mapping and connection construction, with code beside the relevant text.
The diagnosis explicitly asks which chemical assumption causes the mismatch and
whether any represented process can change it. The final synthesis is consolidated
into those local questions; the ending is a stopping cue. Real-ocean TA sources
are supplied context, not an extra recall task. The connection-summary call is removed.

The full TA inference and forward curve calculation reuse skills from 00.
The provisional 10/20/10-minute allocation allows five more minutes for the
curve exercise; this is not a verified timing result. Pilot the revised
40-minute route with students who have completed 00. No pump attribution, OA/OAE time histories or sediment analysis here.

The opening explicitly names 280 ppm and 2040 µmol/kg as the reference values.
Use "small positive initial concentration" for the initial DIC, define gas
transfer velocity (piston velocity), and link the displayed connection excerpt
to `connect_atmosphere` in `simple_models.py`. A brief optional chemistry note
distinguishes registering species definitions from creating transported states;
boron and auxiliary H⁺/CO2 initialization remain supplied implementation.

Report "equilibration time (1% criterion)": the first saved time after which
atmospheric CO2 remains within 1% of its final simulated value. Distinguish it
from an exponential relaxation constant. Explain assertions once as supplied
verification. Keep construction, prescribed-carbon, conservation and calibrated
endpoint checks visible; remove duplicate TA checking and put expected-mismatch
and slower-response assertions in an instructor-only cell. These clarifications
add no exercise or prerequisite; include their reading load in the existing
provisional 40-minute pilot rather than claiming verified completion time.

## 02 — Conservative extension and effective pump (55 minutes)

**Students should be able to:**

1. Add the deep reservoir and two opposing water arrows carrying DIC and TA.
2. Explain why no-pump equilibrium agrees with 01 at the same total inventory.
3. Derive the stationary balance, expression, units and numerical value of k
   from the supplied first-order assumption; identify what was fitted.
4. Derive the finite carbon addition from 62.4 and the actual initial inventory,
   then interpret the supplied forcing and budget verification.

**Do:** A (20 minutes): select deep-box fields, arrow names, transported species
and one flux law for both mixing directions from explained choices.
B (20): derive k, choose the DIC-only pump endpoints/law/scale and interpret matched runs.
C (15): derive/evaluate the added carbon and insert it into supplied Signal code.
Explain the equivalent finite-deep-box inventory calculation on paper; its code
cross-check is instructor-only, not another coding exercise.

**Supplied:** ratio-derived teaching geometry; Q-to-mass conversion using ESBMTK
density; constructor templates; all chemistry, restart, signal-integration,
plotting and time-resolved carbon/TA checks.

Local reading support explains `config` attributes, case-sensitive dictionary
keys, concentration pairs/unpacking, and `Source_to_Sink@id`. The first bulk
example builds on 01's individual constructor: `ty` and `ctype` choose the
flux law, while `sp` selects species. Internal wrapper structure is omitted.
Students choose `mixing_type` and `pump_type` within the existing masked blocks;
there are no additional model runs or derivations.

**Evidence:** conservative connections, two derivations with units, and a sentence
separating a fitted DIC ratio from conditional atmospheric response. Mathematical
and code solutions for both derivations remain masked. Preserve the actual 01
initial inventory. Restoration of 280 ppm checks forcing/conservation, not
independent pump validity. B4 relates the transfer qualitatively to the lecture's
soft-tissue pump, explains omitted features and compares reference-state export
with simulated-equilibrium export. Quantitative pump attribution remains outside
02; a sourced export-comparison note is optional and requires no calculation.

The 02 reading route uses short A1–A4, B1–B4 and C1–C3 steps. Model definition
and supplied comparison runs are separate cells, so completing the pump mapping
only requires rerunning its definition and the pump comparison. Brief explanations
introduce first-order fluxes, stationary notation, output units and restart/control
runs. Define inventory ratio R separately from the lecture's capacity F; explain
that uniform TA gives zero net redistribution while preserving buffering, and
that pulse duration is a supplied choice. The optional duration experiment uses
a supplied helper to resolve and align positive whole-year pulses, with matching
control/forced clocks; students still interpret the mass and endpoint checks.
This numerical support adds no required task or timing allocation. A4 asks about endpoint
equivalence, supported by the existing checks, rather than an unplotted transient.
Consolidated interpretation questions and a simple stopping cue replace repeated
calibration/completion prompts. The two law choices and qualitative pump link
revise the work within the provisional 20/20/15-minute allocation; prerequisites,
derivations and runs stay the same. Pilot the revised reading and question load
rather than treating the 55-minute estimate as established.

## 03 — Scaffolded complete-model construction (55 minutes)

**Students should be able to:**

1. Trace every box and arrow from diagram to workbook record to ESBMTK object.
2. Map water transport using source concentration and both DIC and TA.
3. Distinguish DIC-only POC transfer from linked 1:2 DIC–TA PIC transfer.
4. Identify gas exchange, external weathering and net burial, and explain the
   difference between loading a state and constructing the correct flux graph.

**Do:** inspect diagram/workbook (10 minutes); complete four mapping tasks (30):
reservoir concentration/geometry fields, transport endpoints/species, POC/PIC
choices and linked rates, and gas-exchange endpoints/species. Then inspect the
graph and short stationary restart (10), and explain its meaning (5).

**Supplied:** Model clock, parsing and repeated loops; T/S/P fields; boundary-node
setup; chemistry and sediment-module wiring; flux-object lookup; restart and
verification code. Students still construct the graph through native calls.
The workbook owns numerical inputs and retains benchmark box-specific conditions.

**Evidence:** four mappings; water balance at each box; PIC 1:2 coupling; correct
interpretation of stationarity as implementation verification. Know qualitatively
how dissolution/burial affect carbon/TA and why sediment response can be slow.
Detailed horizon equations and lookup tables are optional reference material.

## 04 — Matched carbon and alkalinity experiments (40 minutes)

**Students should be able to:**

1. Map external carbon input to atmospheric CO2 and pure TA input to surface TA.
2. Verify the input inventories and distinguish prescribed forcing from responses.
3. Interpret forced-minus-matched-control atmospheric CO2, surface pH, deep DIC,
   and dissolution/net-burial responses.
4. Explain how carbonate chemistry, exchange, transport and sediments couple
   the response, including chemical-horizon versus snowline timing, and why OA
   and OAE are not opposite versions of one input.

**Do:** predict (5 minutes); convert two prescribed inventories and select forcing
endpoints/species (10); run supplied models and inspect budgets (10); read selected
panels and answer four short interpretation questions (15). The final allocation
now includes the full response figures: follow forcing to atmosphere/surface,
then deep water and sediments. Other panels provide supporting context, not extra
questions. The 40-minute estimate is retained by keeping two coding tasks, four
answers and the same three model runs; the reading workload still needs a pilot.

**Supplied:** the verified complete model, independent baseline copies, stationary
restart, archived forcing scaling, integration, time-resolved carbon/TA audits
including weathering/net burial, full eight-panel OA/OAE response figures (with
the OA benchmark overlay), and four diagnostic groups plotted as anomalies.
The aggregate response-chain explanation and figures formerly in extension Part II
belong to core 04. Plotting implementation stays in `teaching_plots.py`.
Distinguish the post-1800 benchmark inventory from the whole-run forcing integral.

**Evidence:** two forcing tasks, passing budget checks and four brief explanations.
The OA benchmark and 10 Pmol TA experiment retain their distinct amplitudes.
Distinguish absolute benchmark reproduction from matched forcing-response analysis.
No panel-by-panel report or additional figure-coding task is required.
Do not infer full equilibration from the end of the plotted transient.

## Optional material and maintenance

- `ref/sediment_reference.md`: detailed sediment equations from the earlier 03.
- `notebooks/instructor/extensions/04_attribution_and_feedbacks.ipynb` and its
  generated student copy: Part I's storage tagging and Part III's state-dependent
  feedback hypotheses. Supplied prerequisites rebuild fixed reference cases in a
  fresh kernel without repeating Part II's core questions or figures. These require
  a separate session; core 04 does not execute them.
- `archive/2026-09-16_before_guided_revision/`: frozen pre-change 01–04 notebooks,
  supporting model code/data, tests and documents with SHA-256 manifest. Do not
  edit it or use it as the current teaching source.

For subsequent teaching changes, update this file, relevant design/README text,
and the workplan together; edit instructor sources and regenerate student copies.
Check masking and scaffold visibility, execute changed notebooks, and run relevant
conservation/regression tests. Do not claim unchanged timings after adding tasks
without revisiting the workload allocation. Leave 00 unchanged unless explicitly
requested by the user responsible for its separate question set.
