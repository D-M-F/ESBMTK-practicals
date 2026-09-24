# Exercise revision proposal: preparation for independent modelling

Date: 2026-09-23. **Implemented; student timing pilot remains outstanding.**
The proposal below records the agreed rationale and scope. Implementation and
verification are recorded in `WORKPLAN.md`; the current student route is in
`TEACHING_GOALS.md`. Based on the current
instructor/student notebooks, including the uncommitted 02 simplification,
`TEACHING_GOALS.md`, `ref/design.md`, and the 2026 lecture material. ESM here
means Earth system model. Notebook 00 is outside this revision.

Follow-up: the proposed opening of 03 now makes schematic reconstruction and
its connection to the Excel inputs a required exercise. This supersedes the
earlier recommendation to use selected annotations from the existing draft.
The revised 03/04 notebooks, diagrams and separate student/instructor flux
worksheets now implement this opening. The production numerical workbook is
unchanged. The optional independent-model starter is available as extension 05.

## Recommendation

Retain the guided core, but give students more ownership of the model's
scientific specification and the evidence used to interpret it. Preparation
for future research does not require making them implement a carbonate solver
or repeat connection boilerplate. It does require that they can decide what
is a state, what crosses a boundary, which equation an arrow implements, what
is held fixed, and which result could contradict their expectation.

The desired progression is:

**00: calculate chemistry → 01: diagnose an inadequate model → 02: extend and
calibrate a model → 03: construct and audit a more complete model → 04: specify
and interpret a controlled experiment.**

Keep native reservoir and connection mapping as student work. Reduce exercises
whose answer is simply copying the identical dictionary from the preceding
cell. Fade scaffolding in the scientific decisions, while retaining local
syntax examples, explained choices and reliable supplied execution.

## What belongs in exercises

| Student responsibility                                            | Supplied support                                                 | Evidence of learning                                            |
| ----------------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------- |
| Select states, geometry fields and system boundary                | Diagram, input data, units and constructor signatures            | Distinguish an inventory from a concentration or diagnostic     |
| Map endpoints, species and a flux law                             | Syntax, repeated loops and special coupling machinery            | Explain the corresponding tendency and its units                |
| Derive one representative balance and interpret aggregate budgets | Numerical integration and full audits                            | Explain cancellation and identify external terms                |
| Identify assumptions, fitted quantities and conditional results   | Provenance of inputs and benchmark settings                      | State what agreement does and does not establish                |
| Specify forcing and matched comparison                            | Case copying, restart loading, Signal interpolation and plotting | Identify what changes, what stays fixed and the diagnostic used |
| Interpret results against a prediction                            | Compact figures, units and tolerances                            | Explain a mechanism using an observed feature of the run        |

Do not require plotting code, workbook parsing, solver settings, lookup tables,
flux-object retrieval, sediment equations or repeated chemistry wiring in the
core. Keep these readable and available for later study. Conversely, supplied
code should not mean supplied scientific interpretation: students should explain
why a check is relevant before treating its success as evidence.

For ESM preparation, the transferable objectives are experiment specification,
boundary-aware budgets, control drift, units, parameterization assumptions,
and restraint in interpreting fitted results. This practical cannot by itself
teach ESM configuration, spatial diagnostics, internal variability or ensemble
design. The deterministic box-model comparison provides a starting point;
research training must extend it.

## Preserve the revised 01/02 core

- **01:** retain the prediction/diagnosis, complete inverse TA calculation,
  forward chemistry call, curve interpretation and inventory reasoning.
  These now require students to use chemistry rather than just read its output.
  Keep the initial-partition and gas-transfer comparisons supplied.
- **02:** retain deep-box and connection choices, flux-law selection, the
  stationary derivation and numerical value of k, and the carbon-addition
  derivation using the actual initial inventory. Retain both code and written
  masking. These are strong preparation for constructing their own models.
- Keep the shorter 02 story. Do not restore its removed export comparison,
  identifiability question or intermediate diagnostic discussion to the core.
  Independent calibration/validation and alternative closures belong in a
  later project. Preserve the distinction between the fitted ratio and the
  inventory needed to recover the full reference state.
- Continue the inputs-minus-outputs convention, source concentrations,
  `DIC_s(t)`/`DIC_d(t)` for evolving states and stars for stationary states.
  Use `config` for shared teaching configuration, atm/ocn abbreviations, and
  reserve R for Revelle sensitivity.

## Proposed 03: construct a model you can audit

### A. Make the transition from 02 explicit

Open with a short comparison, replacing some existing introductory prose:

| Feature                 | 02                                         | 03/04 benchmark                                      |
| ----------------------- | ------------------------------------------ | ---------------------------------------------------- |
| Geometry                | Ratio-derived surface/deep split           | Prescribed low-/high-latitude surface and deep boxes |
| Water properties        | Uniform T/S/P and initially uniform TA     | Benchmark box-specific conditions                    |
| Organic export closure  | Effective first-order flux, k DIC_s(t)     | Prescribed fixed POC export                          |
| Carbonate transfer      | Absent                                     | Linked PIC removal, dissolution and net burial       |
| Active atm–ocn boundary | Closed except the finite carbon input      | Weathering and signed net burial, plus forcing in 04 |
| Reference state         | Constructed through calibrated constraints | Archived benchmark restart                           |

Explicitly say that 03 is a different model specification, not a refinement
that inherits 02's fitted k, geometry or carbon inventory. Retain the benchmark
conditions; do not homogenize them to match 01/02.

Introduce POC/PIC and the rain ratio briefly at first use. The current baseline
loader prescribes POC and rain ratio and derives PIC; the notebook subsequently
computes the resulting ratio. Describe that provenance rather than calling the
ratio only a diagnostic. Distinguish a flux representing organic export from
an explicitly simulated particle or nutrient reservoir.

### A1. Exercise 03.1: reconstruct the scientific specification before coding

**Yes: make reconstruction the first substantive student exercise.** The
learning product is a labelled schematic plus a compact flux-specification
table that students subsequently use to construct 03 and design experiments
in 04. Drawing quality is irrelevant: students may sketch or annotate supplied
box outlines. Reconstruct the repository's Boudreau-like ESBMTK benchmark,
clearly distinguished from an exact independent reconstruction of every detail
of the original Boudreau publications.

Supply the four box outlines/names, a process-module symbol distinct from a
reservoir, the relevant paper excerpt/figure, a short correction note, geometry
and parameter values from Excel, and the required scientific assumptions.
Do not show the completed teaching schematic or complete topology table before
the reconstruction attempt. The original figure can remain visible: the task
is to turn its incomplete specification into an unambiguous model, not to
recall its arrows from memory.

Students reconstruct these elements:

1. Mark atmosphere and ocean state variables and the active atm–ocn boundary.
   Identify pH/aqueous CO2 as calculated quantities, and snowline position as
   a module state rather than an additional conserved carbon inventory.
2. Draw each circulation leg and both mixing directions separately; annotate
   their transported species and source-concentration dependence. Show the
   two conceptual gas directions at each surface, implemented by one net
   connection per surface. Check water balance at one box and cancellation
   of one internal tracer transfer.
3. Add low-latitude POC and PIC export, explicit carbonate dissolution returning
   to deep water, signed net burial, and external weathering. Apply the supplied
   benchmark assumption of no high-latitude POC/PIC export. Mark changes to
   dissolved DIC and TA rather than suggesting particulate material is itself
   transported alkalinity.
4. Complete the missing properties in one row per process family: endpoints,
   affected state(s), flux expression, units, stoichiometry and prescribed versus
   calculated status. Attach the same descriptive arrow IDs to the diagram
   and workbook references. Repeated water/gas arrows share their family law.

Retain a short worked example for the flux-table format, using an unrelated
transfer. Supply sediment-law details and unfamiliar syntax. Ask students to
infer directions, signs and linked inventory effects from explained processes;
do not ask them to invent unpublished chemistry or reverse-engineer the module.

**Correct the reading, then ask for reasoning.** The provided note should state:

- The organic-export reference in section 3 of the ESBMTK paper should be F5;
  F3 denotes circulation. Use descriptive process IDs as the main labels.
- The course benchmark uses PIC/POC = F6/F5 = 60/200 = 0.3. The prose's reversed
  ratio is inconsistent with that specification. Weathering here supplies DIC,
  not dissolved organic carbon.
- Figure 3 does not label the complete equations/stoichiometry or explicitly
  draw the dissolution return. Students must supply those properties from the
  corrected specification rather than interpreting every downward arrow as
  direct addition to deep dissolved carbon.

These points are checked against [Wortmann et al. (2025), section 3 and
Figure 3](https://gmd.copernicus.org/articles/18/1155/2025/#section3), local
`ref/ESBMTK.pdf` page 8 (printed p. 1162), and this repository's workbook/loader.
They are teaching clarifications, not claims that upstream files were corrected.

### A2. Make dissolution explicit without creating a second implementation

Use two aligned diagram panels: water/gas exchange, and biological/carbonate
processes. Repeated boxes denote the same reservoirs. Solid arrows show material
transfers; dashed arrows show information, such as deep chemistry informing
dissolution. Draw a carbonate/sediment **process module**, not a new box implying
a prognostic sediment-carbon stock.

The following is the **instructor specification** for the carbonate panel;
mask the corresponding student answers in the exercise version. Let E(t) be
PIC export and D(t) be carbonate dissolution in mol C/yr:

| Conceptual process                | Effect on dissolved inventories                        | Implementation                                           |
| --------------------------------- | ------------------------------------------------------ | -------------------------------------------------------- |
| Low-latitude PIC export to module | Low-latitude DIC loses E; TA loses 2E                  | `PIC_DIC`/`PIC_TA`, nominal deep sinks bypassed          |
| Module dissolution to deep water  | Deep DIC gains D; TA gains 2D                          | Supplied `add_carbonate_system_2(...)` coupling          |
| Signed net burial B_net = E - D   | Aggregate atm–ocn change -B_net in C and -2B_net in TA | Calculated boundary diagnostic; no extra sink connection |

The 1:2 factors relate mol C to TA equivalents. E is fixed in the baseline,
whereas D depends on chemistry and sediment memory. A supplied functional label
`D(t) = sediment_response(PIC rain, deep chemistry, snowline; parameters)` is
sufficient; the detailed sediment equation is optional. D can exceed current
rain when existing sediment dissolves, giving negative net burial. Do not draw
a partition that silently requires 0 <= D <= E throughout a transient.

Tell students explicitly that the helper supplies the dissolution terms after
they identify the physical pathway. Adding a second manual dissolution return,
or a separate burial drain after export and dissolution, would double-count.
`M.D_b.Fdiss` and `Fburial` are postprocessed diagnostics; precise inventory
audits use the solver-consistent dissolution law as in `teaching_audits.py`.
The workbook's `Fb` node does not mean an extra active connection is required.

### A3. Connect the schematic to the Excel inputs in two stages

**First reconstruct; then reconcile.** Display the required reservoir and
baseline parameter rows for the first attempt. Afterward, display the relevant
connection rows and let students reconcile them with their diagram before
coding. The final diagram/table is their working specification, so the later
code exercise translates their earlier decisions instead of asking them twice.

Use actual named tables and stable keys, not worksheet row numbers:

| Diagram content                              | Current workbook owner                               | Student action                                                                                     |
| -------------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Box area, volume, T/S/P, initial DIC/TA      | `OceanReservoirs` in `Reservoirs`, keyed by `Box ID` | Match each state/geometry to its box; distinguish initial from restart values                      |
| Atmospheric size and initial CO2             | `Atmosphere` in `Reservoirs`                         | Identify mole-fraction and inventory units                                                         |
| Three circulation legs and two mixing arrows | `TransportConnections` in `Transport`                | Reconcile `(source, sink, flux_id)` and parameter reference with each arrow                        |
| Two atmosphere–surface connections           | `GasExchangeConnections` in `GasExchange`            | Match atmosphere/surface IDs and shared `piston_velocity`                                          |
| POC, PIC and weathering amounts              | `ProcessParameters` in `Parameters`                  | Trace `poc_export`, `rain_ratio`, `weathering_dic`; distinguish independent and derived quantities |
| Boundary-node names                          | `BoundaryNodes` in `Reservoirs`                      | Distinguish declared nodes from active connections                                                 |
| Dissolution and burial                       | No prescribed flux row: calculated by module         | Mark as calculated responses, not missing input values                                             |

Keep numerical values in their current owner tables. In particular, the loader
derives `pic_export = poc_export * rain_ratio` and
`weathering_ta = 2 * weathering_dic`; do not introduce independent duplicate
inputs for those values. Show only baseline parameters initially; optional
feedback parameters need not occupy the core input view.

**Proposed teaching addition:** a `FluxSpecification` worksheet/table, also
displayed in the notebook, with columns for descriptive process ID, source,
destination, affected inventory/stoichiometry, law, units, parameter/table key,
input/derived/response status, and code implementation. Group these columns
into a readable scientific view and a workbook/code view rather than squeezing
everything onto arrow labels. Keep F1–F8 as secondary source aliases;
G_L corresponds to F7 and G_H to F8. Use endpoint-qualified IDs for the three
`thc` rows, since `flux_id` alone is not unique.

Initially this is a **teaching specification**, not a new model-input parser.
The existing schema does not contain generic POC/PIC/weathering/dissolution
process rows; their topology still lives in Python. Generate the instructor
reference from current tables plus explicitly maintained process metadata and
check it against constructed objects. Generate a separate student worksheet
with selected properties blank, avoiding hidden answer formulas or a full
answer tab in the student file. Display it in the notebook so Excel editing is
optional. Student answers must not overwrite the production workbook.

No numerical formulas need to be stored in the current literal-input tables.
If a future change makes the process table executable input, update the schema,
validation, constructor and regression tests explicitly; do not imply that
editing documentation currently changes the simulation.

### A4. Supply brief assumption notes beside the relevant process

Use two or three sentences per process, not extra derivations or a long
limitations section. Students classify the specified closure and later select
one assumption for their 04 follow-up question.

- **Soft-tissue pump:** DIC-only export with zero TA effect is this benchmark's
  closure. Nutrient assimilation/remineralization can change TA; nitrate uptake
  raises it, whereas ammonium uptake lowers it, with the full balance depending
  on nutrient and redox transformations. A more complete model needs those
  linked processes, not an arbitrary universal TA coefficient on POC export.
  See [Middelburg et al. (2020), section 4/Table 2](https://doi.org/10.1029/2019RG000681).
- **Fixed export and feedback:** 02's k DIC_s(t) already has state dependence
  despite constant k. Core 03/04 instead prescribe POC and PIC export; this
  isolates the response under that closure. Biological export can respond to
  environmental/nutrient conditions; a chosen response law remains a hypothesis.
  Fixed export does not mean all feedbacks are absent: gas exchange, carbonate
  chemistry and dissolution still respond to the evolving state. Existing
  optional pump-feedback laws are illustrative hypotheses, not calibrated
  representations of all biological controls.
- **Weathering:** the implemented +1 DIC, +2 TA input is a lumped benchmark
  boundary closure, not universal river chemistry. For example, carbonic-acid
  dissolution of CaCO3 produces two bicarbonates (2 DIC and 2 TA) while consuming
  one CO2. If that CO2 comes from the represented atmosphere, including its
  loss gives net +1 C and +2 TA to atm–ocn; a river-only input has different
  accounting. The current code applies its lumped source at the low-latitude
  box, without an explicit coupled atmospheric weathering sink. Do not claim
  that this reproduces the spatial/transient pathway. State carbon provenance
  and boundary before selecting another ratio. See [Middelburg et al. (2020),
  sections 5–6](https://doi.org/10.1029/2019RG000681).
- **Carbonate stoichiometry:** pure CaCO3 precipitation/dissolution gives the
  1 DIC : 2 TA relation. Distinguish that reaction constraint from assuming a
  fixed export rate or rain ratio. No high-latitude export, complete deep POC
  remineralization and omission of explicit nutrient cycling are additional
  benchmark choices, not statements that those real-ocean processes vanish.

Changing weathering stoichiometry also changes the conditions for a joint C/TA
steady state with carbonate burial. It requires reconsidering the full boundary
budget and a fresh compatible reference state, not just editing one number.

### B. Retain four native mapping tasks, with stronger scientific choices

1. **Reservoirs and inventories.** Retain mapping of DIC/TA and area/volume.
   Use a partial syntax example rather than the identical completed mapping.
   Ask students to trace one workbook value into its state and explain the
   inventory conversion for that box versus the atmosphere. Supply densities,
   conversions and the remaining repeated rows; no new numerical derivation.
2. **Water arrows and law.** Retain source/sink and species choices, and expose
   the transport-law choice as in 02. For one named arrow, ask which box's
   concentration sets its flux; retain the H_b water-balance check. Keep the
   full graph visible, with repetition supplied. A student should be able to
   predict the effect of using the destination concentration even if a total
   inventory audit would still pass.
3. **POC/PIC and closure.** Retain POC endpoints/species and the linked PIC
   DIC/TA rates. Let students choose the fixed law from an explained list.
   Replace repeated pump definitions with: “If surface DIC changes while
   parameters remain fixed, how does export respond in 02 and in this model?”
   This establishes the changed assumption without adding a feedback run.
   Supply sink bypasses and sediment coupling; these are not discoverable
   scientific choices for a novice.
4. **Gas exchange.** Retain atmosphere/surface endpoints and exchanged species;
   retain the explanation of why the receiving state is DIC while the law
   uses aqueous CO2. Link directly to 01's individual constructor and 02's
   bulk syntax rather than teaching both afresh. Show the atmospheric
   invasion term explicitly using solubility and atmospheric CO2, with local
   conditions and conversions supplied.

Use the reconstructed diagram and flux specification as the planning step for
these same four mappings, renumbered after Exercise 03.1. Keep the existing
diagram drafts as instructor starting material; their eleven selected blanks
do not yet implement the proposed reconstruction. Remove duplicate questions
and repeated lookup work. Reveal the corrected reference only after the
attempt, then reuse it in 04.

### C. Replace repeated boundary questions with one substantive budget task

The current 03 asks about the boundary near the beginning, weathering later,
and construction again in its final synthesis. Consolidate these into one
short task after the graph is assembled:

> Sum the atmosphere and ocean budgets. Which transfers cancel? Complete the
> remaining carbon and TA tendencies using weathering and net burial, then
> explain what a successful inventory check would establish.

Supply the inventory definitions and sign convention; mask the boundary terms
and explanation. The instructor solution for the unforced benchmark is

\[
\frac{dC_{atm+ocn}}{dt}=W_C-B_{net},\qquad
\frac{dA_{ocn}}{dt}=W_A-2B_{net},\qquad W_A=2W_C.
\]

Here A is TA inventory in equivalents, W_C and B_net are mol C/yr, and W_A
is equivalents/yr. Positive net burial removes material from the active
boundary; negative net burial returns material from existing sediment. The
carbonate module carries sediment memory but is not an explicit conserved
sediment-carbon reservoir. Do not count dissolution again after using net burial.

Supply the numerical audit. Check graph structure and stoichiometry as well:
conservation alone can pass for a scientifically wrong internal transfer.
The present 03 shows restart changes, sediment partition checks and comparison
with the reusable implementation; these should not be described as an already
implemented full atm–ocn boundary audit or quantitative all-state stationarity test.

### D. Keep verification compact and precise

Show one graph summary and one compact verification report: construction,
carbon/TA residuals, PIC coupling and restart drift. Retain detailed diagnostics
in a supplied reference. Remove the duplicate `M.connection_summary()` output.
Provide quantitative drift tolerances for relevant states, including sediment
memory, if claiming a stationary restart check; a short run supports local
consistency and does not establish long-term stability or uniqueness.

Correct the mapping table's atmospheric “pCO2” label to dry-air CO2 mole fraction
where that is the stored quantity. Keep `Model` described as the software
container/clock, with the physical boundary chosen separately. Move statements
answering the consolidated budget question into marked instructor solutions.
End with a stopping cue instead of another six-point summary and synthesis task.

**Unit convention needs prominent treatment.** Current 03 retains the historical
benchmark volume-to-litres numerical transport scale multiplying mol/kg states;
02 explicitly uses Q rho in kg/yr. Label the former as a benchmark convention,
not a general dimensional recipe. Give students the physically consistent rule
for new models and explain why this reproduction retains the old convention.
Do not silently change it: a correction requires a separately versioned model,
fresh stationary state, regression checks and reevaluated benchmark comparison.

## Proposed 04: specify the experiment before interpreting it

Keep the three runs (control, OA, OAE), the two short coding tasks and four
written answers. Increase ownership by replacing repeated explanation and
table reading, not by adding more model runs.

### A. Replace the repeated workbook tour with an experiment specification

Provide a compact table with rows for control/OA/OAE and columns for input
species, receiving reservoir, amount and units, time history, initial state,
and fixed parameters. Supply the benchmark amounts/history and restart; students
complete species/endpoints through the existing code task and identify what
must match the control. Briefly explain what the case-building helper returns
and what to rerun after an edit, as in 01/02. Put the full workbook tables in
optional reference, since students inspected them in 03.

Reuse the completed 03 schematic: students add only atmospheric carbon input
I_C(t) for OA or low-latitude TA input I_A(t) for idealized OAE, marking the
unchanged internal processes and the measured outputs. This is the planning
part of the existing forcing-endpoint exercise, not a second reconstruction.

Retain the inventory conversions, but treat them as a quick unit check within
experiment specification. The scientific decision is what is added and where,
not just evaluating 10 × 10^15. Preserve the exact OA normalization and both
post-1800 and whole-run integrals; do not make the rounded 4025 Gt C number the
new forcing normalization. Numerical signal scaling and integration stay supplied.

Before running, ask students to choose the signs of atmospheric CO2 and surface
pH responses and identify a diagnostic that could contradict the prediction.
Reuse that prediction in the four answers; no additional submission.

### B. Put matched responses first

Lead with the existing matched-anomaly figure: atmospheric CO2, surface pH,
deep DIC and dissolution/net burial. Keep the complete eight-panel plots
available afterward, using the horizon panel for the sediment answer and the
OA overlay for reproduction. Do not require two complete figure tours before
students reach the comparison of interest.

Explain subtraction of the matched control, including any baseline drift.
It isolates the response to the changed forcing within this deterministic
model; it does not eliminate numerical errors or validate missing processes.
Distinguish forcings in mol C and TA equivalents, with different amplitudes.
Do not infer relative intervention efficiency from these raw trajectories.

Reuse the 03 budget with external input terms, supplied here:

\[
\frac{dC_{atm+ocn}}{dt}=I_C(t)+W_C-B_{net}(t),\qquad
\frac{dA_{ocn}}{dt}=I_A(t)+W_A-2B_{net}(t).
\]

Pure-TA OAE has I_C = 0; atmospheric-to-ocean uptake redistributes carbon
inside this boundary. Changes in net burial can nevertheless change the total
active carbon relative to control. This is a useful interpretation of the
budget, not another derivation or an assumption of constant total carbon in 04.

### C. Replace the four final prompts with four focused research habits

1. **Design and evidence:** identify what differs from control and use the
   atmosphere/surface anomalies to assess the initial OA/OAE prediction.
   Explain why comparison with the initial state alone is less informative
   if the control drifts, and name the relevant forcing species/endpoints.
2. **Mechanism and budget:** explain how pure TA input changes atmospheric
   CO2 without directly supplying carbon. Trace the internal gas transfer,
   use the boundary budget, and explain why these unequal inputs are not
   opposite or equal-strength interventions.
3. **Time and process:** use a surface/deep lag and the sediment panels to
   explain the response chain and linked 1:2 transfers. Distinguish chemical
   horizons from snowline memory. State whether the displayed evidence supports
   equilibration; do not infer it merely from reaching the final time.
4. **Claims and next test:** distinguish benchmark reproduction from a
   conditional prediction. Identify one fixed assumption limiting the
   interpretation and specify one changed input, matched control and diagnostic
   for a follow-up test. Propose it in one or two sentences; do not run it in
   the core. Changes to baseline physics or rates require a compatible new
   stationary state.

Move causal answers to marked solutions rather than revealing them before
these questions. Retain definitions students need to reason. Remove “Submit”
and historical “formerly Part II” explanations from the student route; keep
answers in the ungraded notebook and finish with one stopping cue.

## Workload and a route beyond the core

The proposed allocations remain **targets to pilot**, not verified unchanged
workloads. Retain 03/04's combined 95-minute envelope through replacement:

| Notebook   | Proposed allocation                                                                                                   | Space recovered                                                                                                                                                             |
| ---------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 03, 55 min | Transition/reconstruction/Excel reconciliation 15; four mappings 20; consolidated budget and checks 15; explanation 5 | Reconstruction replaces passive diagram inspection; code translates those same choices; remove duplicate copied example, boundary prompts, graph output and closing summary |
| 04, 40 min | Prediction/specification 5; forcing tasks 10; runs/checks 10; four answers 15                                         | Repeated workbook display and full-figure reading before anomalies                                                                                                          |

Keep 00's eight parts and provisional reserved slot unchanged. The overall
four-hour schedule is still unverified. Pilot elapsed reading, coding, model
runtime and discussion separately; if the replacement tasks do not fit,
provide more time or explicitly reduce required work. Do not quietly assign
the extra material as compulsory homework.

The revised 15-minute reconstruction allocation is especially tentative.
If building and explaining the diagram plus lookup table requires 20 minutes,
03 becomes a 60-minute activity unless another required task is explicitly
removed. Do not assume five minutes can be taken from 00's provisional slot
or silently compress native construction beyond what novices can complete.

For students pursuing their own models, propose a **separate optional 60–90
minute starter project**, with duration also to be piloted. Start from 02's
transparent, mass-consistent model or an explained minimal template; use 03's
benchmark adapter only with its unit caveat understood. Ask for one question,
a labelled diagram, one modified assumption/connection/forcing, its equation
and units, a matched experiment, conservation evidence and one interpreted
figure. Supply run/plot utilities, but omit the completed scientific mapping.

Offer bounded choices such as comparing fixed versus first-order export at a
common reference flux, or comparing two timings of the same integrated input.
Require appropriate controls and distinguish transient from stationary claims.
Keep the existing detailed sediment, tagged-attribution and feedback notebooks
optional; they are useful process extensions, but do not replace the practice
of specifying one's own small experiment. A credible research follow-up would
also need independent evidence and uncertainty analysis beyond this starter.

## Implementation and acceptance criteria

1. Revise 03 first, preserving numerical workbook inputs, benchmark dynamics
   and native construction. Implement the reconstruction, source-correction
   note and staged Excel reconciliation; generate student/instructor teaching
   specifications without overwriting live inputs or leaking completed answers.
   Add/adapt supplied boundary and drift checks before claiming them as learning
   evidence. Review the explicit dissolution diagram and historical unit warning.
2. Revise 04's specification, figure order and four prompts using the existing
   cases. Preserve forcing normalization, matched initial conditions and audits.
3. Update implemented learning outcomes, workload, design and README together
   only when those notebook revisions are made. Preserve current user edits
   and immutable archives. Do not regenerate unrelated 00/01 sources merely
   to reconcile their previously reported generated-copy differences.
4. Regenerate edited student copies from instructor sources. Check that
   scientific choices and written conclusions are masked, syntax support
   survives, and no diagram/table gives away the same exercise elsewhere.
   Retain the gold terms, blue questions, purple instructor panels and code roles.
5. Execute revised notebooks in activated ESBMTK314; run the applicable
   model-input, reservoir, mass-balance, teaching-audit, benchmark and generation
   checks. Inspect rendered equations, tables, diagrams and figure order in
   both versions. Separate pre-existing failures from new regressions.
6. Pilot with a novice after the current 00–02 sequence. Assess whether they
   can explain an unseen arrow or propose a controlled change, not merely
   whether they fill every blank successfully.

The implementation preserves benchmark numerical inputs and dynamics. Numerical,
generation and rendering evidence is recorded in `WORKPLAN.md`. Student workload
and transfer to independent modelling still require a novice pilot; execution
time and automated checks are not evidence of student completion time.
