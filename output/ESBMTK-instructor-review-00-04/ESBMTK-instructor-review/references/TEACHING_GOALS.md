# Teaching goals and workload: practicals 00–04

Last updated: 2026-09-24. This is the maintained summary of the **implemented**
student route, required learning outcomes and workload. Update it in the same
change whenever notebook tasks, scope, prerequisites or timing change. Record
pending ideas and verification evidence in `WORKPLAN.md`; scientific rationale
and boundaries remain in `ref/design.md`. Archive snapshots are historical.

## Scope and time budget

**Current scope:** teaching goals for the 04 attribution/feedback extension are
temporarily suspended until the user explicitly asks to turn them on again.
Keep its files and implementation dormant; do not include its goals, settings
or exercises in current teaching plans. Core 04's matched OA/OAE work remains active.

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
| 03: reconstruct and build the model | 55 | Diagram/flux specification; four mappings; boundary and restart checks |
| 04: carbon versus alkalinity forcing | 40 | Experiment specification; two code tasks; four scientific interpretations |
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
ESBMTK/PyCO2SYS versions. A fresh Windows installation from the setup-only ZIP
passes; macOS/Linux and novice-student pilots remain. ESBMTK314 remains the
verified instructor reference.
Setup and instructor validation happen before class, with no new student
exercise or change to the practical's provisional timetable.
The three-page uv and Anaconda PDF handouts under `output/pdf/` support
that same pre-class setup. A setup-only ZIP may be distributed before the
exercise notebooks are released. It contains the environment recipes, a shared
environment checker, a labelled workbook probe and a non-exercise JupyterLab
orientation notebook. A temporary start guide owns the later transition to the
complete GitHub repository: uv creates a repository-local `.venv`, while Conda
normally reuses the named environment. Both route guides explain terminals and
folders, confirm successful installation, and separate opening notebooks from
stopping/restarting the JupyterLab server. Instructor maintenance notes remain
outside the student guides.
Fresh Windows uv and Anaconda environments pass their documented setup checks
and actual JupyterLab kernel/launch checks. The uv environment also passes all
five core instructor notebooks. macOS/Linux and novice-student setup pilots
remain required. Setup time stays separate from the unchanged practical timetable.

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
2. Explain why CO2 invasion moves carbon but cannot generate TA, using the
   cancelling bicarbonate/proton contributions even as pH changes.
3. Infer background TA, use pCO2–DIC curves to explain partitioning, and distinguish the fit from prediction.
4. Distinguish initial partition and exchange rate from equilibrium controls.

After TA inference, use the supplied offline rotatable DIC–TA–pCO2 explorer
to connect a chemistry surface, its top-view pCO2 contours (the Deffeyes
representation), and constant-TA pCO2–DIC slices. Move the cutting plane and
inspect a local tangent, then add the conserved-carbon atmosphere line after
its explanation. The guide targets 3–5 minutes replacing part of the existing
sensitivity explanation within the 20-minute diagnosis/inference/curves block.
The existing curve-interpretation answer now includes this connection; no extra
coding exercise, model integration, submission or package prerequisite is added.
The 40-minute total remains provisional: pilot the revised activity and adjust
the allocation explicitly if it does not fit. The broad TA = 0 view is optional;
the existing two-curve exercise remains required. Do not shift time from 00.

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
The chemical explanation replaces the broad TA-persistence question within
diagnosis (about two minutes); its reaction is supplied, with no new calculation.

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
B4 replaces the broad omissions question with a production → export →
remineralization sketch (2–3 minutes within B). Students distinguish effective
deep export/remineralization from primary production and permanent burial and
name one omitted control. C1 supplies the distinction between the 62.4 stock
ratio and uptake of a future addition; it adds no derivation or run.

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
soft-tissue pump and explains omitted features. The reference-versus-simulated
export comparison, numerical intermediate DIC/export discussion and published
export estimates are outside the core notebook. Its existing figure still shows
the atmospheric response and pump–mixing balance; fitted-ratio and conservation
checks remain supplied. Quantitative pump attribution remains outside 02.

The 02 reading route uses short A1–A4, B1–B4 and C1–C3 steps. Model definition
and supplied comparison runs are separate cells, so completing the pump mapping
only requires rerunning its definition and the pump comparison. Brief explanations
introduce first-order fluxes, stationary notation, output units and restart/control
runs. Focus B2 on the deep-box balance; keep the full budgets in a collapsible
reference. The parameter-identifiability discussion is an instructor note, not
a separate question. Bridge B to C through the difference between a fitted ratio
and the total inventory needed for the full reference state.
Use $r_{\mathrm{ocn/atm}}$ for the inventory ratio, reserving R for the Revelle
factor and F for the lecture's capacity, with the
longer lecture connection in optional reference material; explain
that uniform TA gives zero net redistribution while preserving buffering, and
that pulse duration is a supplied choice. The optional duration experiment uses
a supplied helper to resolve and align positive whole-year pulses, with matching
control/forced clocks. Duration experiments and interpolation details are in an
optional note; students interpret compact input/budget/endpoint check summaries.
This numerical support adds no required task or timing allocation. A4 asks about endpoint
equivalence, supported by the existing checks, rather than an unplotted transient.
Consolidated interpretation questions and a simple stopping cue replace repeated
calibration/completion prompts. The two law choices and qualitative pump link
revise the work within the provisional 20/20/15-minute allocation; prerequisites,
derivations and runs stay the same. The 2026-09-23 simplification removes two B4
questions and the B3 identifiability question without adding required work.
Pilot the revised reading and question load
rather than treating the 55-minute estimate as established.

## 03 — Scaffolded complete-model construction (55 minutes)

**Students should be able to:**

1. Write paired DIC/TA amount-flux equations and reconstruct states/boundaries from corrected source
   material, then reconcile the diagram with named Excel records.
2. Translate that specification into native reservoirs and connections, including
   source-concentration transport, fixed POC/PIC export and gas exchange.
3. Explain linked carbonate export/dissolution, signed net burial and the
   assumptions about biological TA effects, weathering and pump dependence;
   use local DIC–TA vectors to explain contrasting POC/PIC pCO2 effects.
4. Complete the boundary carbon/TA budget and distinguish graph checks,
   conservation, short restart drift and independent scientific validation.

**Do:** write paired DIC/TA fluxes and label the reconstructed diagram, then reconcile
with Excel (15 minutes); translate those same choices through four native
mapping tasks (20): reservoirs, water endpoints/species/law, POC/PIC choices/law
and linked rates, and gas exchange. Complete one boundary budget and inspect
supplied graph/carbon/TA/restart checks (15); explain their evidence (5).
Reconstruction replaces passive diagram inspection; repeated boundary questions,
the duplicate graph dump and closing summary are removed. Thirteen flux expressions
and the POC arrow remain blank; the dissolution dependency function is supplied.
Students identify which changing model values affect each flux, which rates are
fixed, and which two fluxes determine net burial, then use
one supplied J/m tendency rule to show inventory cancellation. Distinguish Q,
rho Q and box mass, and water pressure from atmospheric CO2 partial pressure.
Use Q for water volume transport throughout. Keep diagrams focused on boxes
and process arrows, with paired tracer equations in the companion table.
Reuse the contour representation introduced in 01 to interpret the completed POC/PIC/D equations:
draw local arrows and reuse them in 03.4 without repeating effects in prose.
Allow 4–6 minutes
within reconstruction/export discussion for this added reasoning. The plot uses
the workbook L_b input state and benchmark chemistry; plotting is supplied.
Students now apply the familiar representation to process arrows; the benchmark
surface is recalculated under its own conditions, not inherited from 01.
The 55-minute allocation is a pilot target, not a demonstrated workload. If the
opening takes 20 minutes, allow 60 minutes for 03 or make contour interpretation
optional before class; do not silently retain the same timing with additional
required work or borrow from 00's unverified reservation.

The readability pass separates 03.1 into paired fluxes, diagram labelling and
one internal-transfer check, preserving the same questions and answer fields.
Workbook-to-code cross-references and numerical budget details are expandable
reference material; actual workbook rows and physical restart tolerances remain
visible. Gas-law hints stay with reconstruction, followed by a short mapping
reminder in construction. Pilot guidance and the fallback above remain instructor
planning notes. These presentation changes add no task, prerequisite or change
to the provisional time allocation.

Define restart on first use as starting a new run from saved model values, then
explain the workbook-to-saved-state replacement beside loading. Use
`scale_with_concentration` directly as coefficient times current source
concentration; omit comparisons with a broader state-dependence category.
C2 identifies the atm plus dissolved-ocn boundary, then asks two questions:
explain cancellation of internal transfers and write the carbon/TA balances
using W_0 and the net burial already defined in A3. Omit re-deriving net burial
and the hypothetical additional burial sink. No experimental addition does not remove
weathering. Distinguish accounting for boundary fluxes from constant inventories.
Remove feedback/attribution extension pointers from 03 while that teaching is
suspended. Keep the same provisional 55 minutes and pilot requirement.

**Supplied:** Model clock, parsing and repeated loops; T/S/P fields; boundary-node
setup; chemistry and sediment-module wiring; flux-object lookup; restart and
verification code. Students still construct the graph through native calls.
The workbook owns numerical inputs and retains benchmark box-specific conditions.
The opening contrasts these assumptions with 02, including fixed export and the
historical nominal litres/yr transport convention. Inventories continue to use
ESBMTK density; a physical transport correction is not part of this revision.
Short row hints state the required benchmark assumptions. Expandable reference
notes explain biological TA effects and weathering; B2 explains the available
native flux laws directly beside their code names.
The weathering caveat simply notes that real riverine input need not have the
model's exact 1 DIC : 2 TA ratio.

**Evidence:** reconstructed diagram/flux table, four mappings, water balance,
the boundary derivation and explanation. Dissolution is explicitly drawn but
implemented by supplied `add_carbonate_system_2`; net burial is a signed residual,
not an extra sink. The 20-year restart checks every saved value of all six ocean
DIC/TA states, atm CO2 and sediment snowline against explicit absolute tolerances.
It supports local consistency, not long-term stability. The instructor also
compares with the reusable implementation. Detailed sediment equations remain
optional. The companion student/instructor Excel flux worksheets are generated
teaching records, not live model inputs; Excel editing is optional and the same
exercise is visible in notebook Markdown. Student worksheets contain no hidden
answer tab or answer formulas.

## 04 — Matched carbon and alkalinity experiments (40 minutes)

**Students should be able to:**

1. Map carbon and pure-TA inputs to the appropriate states and verify their inventories.
2. Relate supplied forcing shapes to matched-control atm CO2, surface pH,
   deep DIC and dissolution/net-burial responses, including delayed adjustment.
3. Explain saturation horizon, compensation depth and snowline as distinct
   chemical, rain-balance and sediment-history diagnostics.
4. Interpret OA/OAE differences through carbon redistribution, TA-changing
   chemical compensation and sediment memory; distinguish these mechanisms
   from unequal forcing amplitudes and from prescribed biological export.

**Do:** predict/specify on the completed 03 diagram (5 minutes); convert two
inventories and select forcing species/endpoints (10); inspect the supplied
forcing plot, run three cases and check budgets (10); interpret selected panels
in four short answers (15). The answers cover forcing/response timing,
carbon uptake/TA, critical depths/memory and asymmetry/limits, citing curves
and approximate intervals. They replace repeated design questions and the
biological-response experiment proposal; that proposal is suspended with the
04 extension. No additional exercise, integration or prerequisite is introduced.

**Supplied:** independent fixed-export model copies and a common nearly
stationary restart; exact solver-input plots before B2, with separate physical
units and a normalized shape comparison; forcing integrals and time-resolved
boundary C/TA audits; four matched-anomaly diagnostic groups and full eight-panel
figures with the OA reproduction overlay. Repeated workbook tables remain optional
lookup support. Plotting stays in `teaching_plots.py`; no figure code is required.

**Evidence and limits:** keep two forcing tasks, checked budgets and four concise
interpretations. Separate post-1800 from whole-run inputs and input-rate peaks
from response peaks. Match 03's active boundary and W_0 notation. Explain pure-TA
OAE through internal uptake and a responding net-burial boundary; dissolved
repartitioning conserves TA but sediment dissolution does not conserve dissolved TA.
Read depth together with dissolution/burial. Explain positive depth versus plotted
negative elevation, the 200 m saturation-horizon bound and the implementation's
effectively instantaneous snowline-deepening assumption on the plotted timescale.
B3 supplies both rules explicitly: during CCD shoaling, old carbonate takes time
to dissolve and the snowline lags; during deepening it follows the new preservation
boundary without resolving the buildup of a thick sediment layer. Students apply
these rules to e/h, with no raw-code lookup or derivation. Distinguish snowline
tracking of the CCD from transport/chemistry delays after the external input;
the rule follows depth-change direction, including later shoaling in OAE.
This clarifies the existing depth/memory answer within the same provisional timing.
Fixed POC/PIC export cannot establish a
biological response. Unequal OA/OAE amounts cannot establish relative efficiency
or cancellation; late values alone do not establish equilibrium; the benchmark
overlay supports reproduction, not independent observational validation.

The two original 2010 Boudreau papers support local definitions and scientific
interpretation. Detailed sediment equations and extension experiments remain
outside the required work. The 40-minute allocation is still provisional:
pilot the revised depth/asymmetry reading and four answers before relying on it.

## Optional material and maintenance

- `notebooks/instructor/extensions/05_independent_model.ipynb` and its generated
  student copy: a separate 60–90-minute starter, also unverified by a pilot.
  Students choose a question, specify one change and its units, define a matched
  comparison, complete native scientific choices and interpret one supplied
  figure with budgets. The instructor example compares fixed and first-order
  export at a common initial/reference flux in 02's mass-consistent model.
  Cases share an initial state rather than claiming a stationary restart.
  A pulse-timing alternative points to 02's supplied forcing machinery.
  This is optional, not homework added to the four-hour core; uncertainty,
  independent constraints and ESM ensembles remain further research training.
- `ref/sediment_reference.md`: detailed sediment equations from the earlier 03.
- `notebooks/instructor/extensions/04_attribution_and_feedbacks.ipynb` and its
  generated student copy are retained but dormant. Their teaching goals are
  suspended until explicitly re-enabled by the user; no session is currently planned.
- `archive/2026-09-16_before_guided_revision/`: frozen pre-change 01–04 notebooks,
  supporting model code/data, tests and documents with SHA-256 manifest. Do not
  edit it or use it as the current teaching source.

For subsequent teaching changes, update this file, relevant design/README text,
and the workplan together; edit instructor sources and regenerate student copies.
Check masking and scaffold visibility, execute changed notebooks, and run relevant
conservation/regression tests. Do not claim unchanged timings after adding tasks
without revisiting the workload allocation. Leave 00 unchanged unless explicitly
requested by the user responsible for its separate question set.
