# Implementation workplan

## Lecturer review PDF pack (2026-09-24)

- Execute isolated copies of all five current instructor notebooks in activated
  ESBMTK314, retaining full cell outputs, plots, tables and instructor answers.
- Export all eight disclosures expanded, execute 04's optional workbook lookup,
  and append 03's linked optional sediment reference. Supply three static
  explorer views plus its browser-only offline HTML companion.
- Package the five PDFs with their directly linked local references, existing
  coding cheatsheet, start guide and execution/hash manifest. Rewrite local
  PDF links for the extracted pack. Retain source notebooks and student copies.

Verification: all five notebooks completed without cell errors and passed their
embedded scientific/software audits. Printed stream-output completeness and
unchanged source SHA-256 checks pass. MathJax reports no formula errors; all
images load, all disclosures are open, and browser layout checks find no
horizontal overflow. All 75 final pages were rendered with Poppler and visually
inspected; page-coordinate checks find no text outside the page margins. The
five PDFs have 8/17/14/23/13 pages, and all 84 stream outputs pass completeness
checks. The ZIP integrity check passes (15.9 MiB). No teaching tasks,
prerequisites or workload change; the
dormant extension remains excluded. Builders and rebuild instructions are in
`scripts/*instructor_review*` and `ref/instructor_review.md`.

## Clarification: 04 critical depths and snowline memory (2026-09-24)

B3 now supplies the two snowline rules before the question: CCD shoaling leaves
old carbonate that must dissolve before the snowline retreats; CCD deepening lets
the preservation boundary follow effectively instantly at the century timescale,
without resolving accumulation of a thick sediment layer. Explain the possible
small numerical lag, distinguish tracking the CCD from response to external TA,
and note that later shoaling can produce a lag even in OAE. Students need no
raw-code lookup or sediment-equation derivation. C3 asks them to apply these
supplied rules to the depths and burial plot; the masked instructor answer explains
the OA lag, old-stock dissolution and the assumed OAE response explicitly.

Teaching goals/design are aligned. This clarifies one existing answer; the four
answers, runs and provisional timing remain unchanged. Only two instructor
Markdown cells changed; executable cells, saved outputs and execution counts were
verified unchanged. Prior conservation results remain applicable. Regenerated
student 04 exactly; both notebooks validate, masking/HTML structure checks and
three applicable notebook tests pass. Saved output tables were excluded from the
Markdown-only table count. Full browser visual QA remains blocked as recorded below.
Evidence: `tmp/04_consistency/check_memory.py` and the two `*_memory.html` previews.

## Follow-up: 04 consistency and scientific interpretation (2026-09-24)

- [x] Put the exact solver-input forcing shapes in B1, before B2 responses,
  with carbon/TA units and a normalized timing overlay. Keep interval and
  whole-run integrals, three matched cases and two coding exercises unchanged.
- [x] Replace repeated design questions and the dormant biological-response
  experiment proposal with four scientific interpretations: timing, uptake/TA,
  critical depths/memory and OA/OAE asymmetry. Remove the extension pointer and
  explicit extension switches from core 04; the helper's defaults are identical.
- [x] Define saturation, compensation and snowline separately with links to
  both original 2010 papers. Explain elevation sign, saturation-depth clipping,
  finite-stock erosion and the implementation's rapid snowline-deepening closure.
  Connect late OAE deep-DIC decline and increased burial with retention of TA/carbon,
  and OA negative net burial with dissolution of previously deposited sediment.
- [x] Reuse 03's W_0 boundary notation, remove the repeated inventory display
  and unused forcing constants, correct TA units/atm CO2 plot labels, and fix
  the stale core-04 'Part I' reference in the data guide. Align goals/design/README.
- [x] Regenerate only student 04 and update its existing structural tests.

Verification: all core 04 cells execute in activated ESBMTK314, including all
three integrations and continuous carbon/TA budget audits. Maximum carbon
residual/initial stock is 8.34e-6 (OA), below the audit tolerance. The plotted
solver-input peak is near year 2169; post-1800 integrals are 335.358 Pmol C and
10.00005 Pmol TA equivalents. Numerical evidence confirms OA's separated depths
and negative net burial, and OAE's smaller deepening and increased preservation.
All four figures were visually inspected. Notebook validation, compilation,
local links, HTML table/panel structure, answer masking and exact student
regeneration pass. The 23-test targeted suite has only the existing generated-copy
mismatch in untouched 00 (extra empty source cells); 04 and conservation checks pass.
Browser security policy blocks opening the local HTML preview, so a full visual
inspection of rendered notebook Markdown/math remains unverified; no alternate
browser route was attempted. Evidence and previews: `tmp/04_consistency/`.

Workload: replacement/consolidation of existing interpretation tasks, with no
new model run or code exercise. The 40-minute allocation remains provisional;
pilot the revised critical-depth/asymmetry reading and four short answers.

## Correction: use defined net burial directly in C2 (2026-09-24)

Removed the question about a hypothetical additional burial sink and the repeated
derivation of net burial. C2 now asks only why internal transfers cancel and how
weathering and the already-defined net burial enter carbon/TA balances. The
instructor answer uses those two balances directly. This reduces the existing
budget exercise; the provisional 55-minute allocation remains unchanged.
Regenerated student 03, checked both rendered C2 fragments and solution masking,
and verified that code and outputs are unchanged. The previous numerical audits
remain applicable to the identical executable code. Updated teaching goals/design
to keep this reduction in the maintained task scope.

## Correction: omit the state-dependence comparison in 03 (2026-09-24)

Removed B2's newly added comparison between `scale_with_concentration` and a
broader dependence on changing model values. That taxonomy is unnecessary for
the active teaching route. Retain the direct law-table definition, coefficient
times current source concentration, and explain other processes locally.
Updated current teaching guidance to prevent reintroducing the comparison.
Only this Markdown paragraph and guidance changed; code, outputs, exercises
and scope are unchanged. Student 03 was regenerated and checked against its
source; existing model execution evidence remains applicable to identical code.

## Follow-up: 03 terminology, budgets and temporary extension scope (2026-09-24)

- [x] Define model state, snowline and restart in A1. Explain that a restart
  starts from saved values, identify the workbook-to-saved-state replacement,
  and describe C3 as a 20-year continuation with no experimental addition.
- [x] Replace the fixed/state-dependent/residual classification wording with
  identifying the changing inputs to each flux. Explain `scale_with_concentration`
  as a specific proportional law; distinguish gas and sediment calculations.
- [x] Rework C2 around the explicit atm plus dissolved-ocn boundary and reuse
  W_0 rather than introducing W_C/W_A. Scaffold internal cancellation, inputs
  minus outputs, then regrouping into net burial. Explain why budget closure
  does not mean constant inventories, and why weathering persists without forcing.
- [x] Remove feedback/attribution extension pointers from 03 and redundant flux
  and burial explanations. Keep all four mappings and 13 flux-expression blanks.
- [x] Record the user's temporary suspension of 04 extension-related teaching
  goals in AGENTS.md, teaching goals, design and README. Its files and code remain
  dormant until explicitly re-enabled; core 04 OA/OAE and the separate 05 starter
  retain their existing scope. No teaching time or new exercise is added to 03.

Verification: all executable 03 code, stored instructor outputs and execution
counts match the starting worktree. Execution in ESBMTK314 passes graph, carbon/TA
budgets, 20-year saved-state drift and reusable-model agreement. Both notebooks
validate and student 03 regenerates exactly, with four masked code tasks, 13
expression blanks and no instructor answers, feedback or attribution pointers.
All three specification tests pass. The 12-test notebook suite has only the
existing generated-copy failures in untouched 00/04; 01 now passes with the user's
intervening title/generation change preserved. Browser inspection confirms the
restart explanation, flux-law explanation and C2 question/answer math layout.
Protected notebooks, archives, benchmark data, diagrams and worksheets match
their starting hashes. Evidence: `tmp/03_consistency/`. The 55-minute allocation
remains provisional and still needs the planned novice-student pilot.

## Follow-up: carbonate explorer title (2026-09-24)

Renamed 01 section 3.2 and the interactive figure to "DIC and TA constrain
carbonate chemistry", including the browser title and cached instructor display.
Regenerated student 01 and the offline preview. Verified that only title text
changed, with executable code, numerical data and other outputs preserved;
both notebooks validate and the student copy matches generation. Checked the
heading in the browser at narrow width. Teaching scope and timing are unchanged.

## Follow-up: overall readability of 03 (2026-09-24)

- [x] Split 03.1 into three visible steps: paired fluxes, diagram labelling and
  one internal-transfer check. Keep the same 13 flux blanks, POC arrow, scientific
  choices and four code mappings; put notation and supplied hints beside the work.
- [x] Consolidate gas-law explanation in A3 and the full historical transport-unit
  caveat in B2. Clarify snowline, DIC-only POC behaviour and bypassed PIC sinks.
- [x] Keep the three workbook input tables visible in A4; make the duplicate
  connection summary and workbook-to-code mapping expandable references.
- [x] Keep physical restart limits visible and move numerical budget details to
  a technical disclosure. Retain provisional timing in the opening; keep pilot
  and fallback planning in TEACHING_GOALS.md. Scope and allocation are unchanged.
- [x] Regenerate student 03 and inspect both HTML renderings. Fix notation-table
  widths after MathJax squeezed definitions into a narrow column.

Verification: 03 executes in ESBMTK314 with graph, carbon/TA budget, short-restart
and reusable-model agreement checks passing. Model code is unchanged; only the
optional cross-reference display and code-role/comment labels changed. Existing
instructor outputs and marked written answers are preserved. Student 03 validates,
regenerates exactly, keeps four masked coding blocks and all 13 flux blanks, and
contains no instructor panels or outputs. All three specification tests pass.
The 12-test notebook suite passes except its generated-copy subtests for untouched
00, 01 and 04 (00/04 extra empty cells; 01 serialization key order). Protected
notebook, archive, workbook, diagram and worksheet hashes remain unchanged;
execution-generated logs are excluded. Rendered equations, tables, diagram steps,
answer panels and disclosures were checked in the browser. The Jupyter kernel
reported a non-fatal read-only IPython history warning; all model audits completed.
Evidence: `tmp/03_readability/`. The novice-student timing pilot remains outstanding.

## Equation-first specification in 03.1 (2026-09-24)

- [x] Replace the prose-based effects/law/status table with paired amount-flux
  expressions J_DIC and J_TA for each process family. Keep 13 expression blanks
  and the POC arrow; ask students to mark fixed/state-dependent laws and residuals.
- [x] Supply notation, gas-chemistry and dissolution dependency hints, and the
  J/m concentration-tendency rule. Keep the historical transport-unit caveat;
  distinguish water pressure from atmospheric CO2 partial pressure and retain
  signed net burial without an extra drain.
- [x] Use short assumptions beside rows and expandable scientific reference
  notes. Put the existing contour interpretation after the flux equations,
  reusing the paired stoichiometry and preserving the four native mappings.
- [x] Generate the notebook table and paired Excel worksheets from shared
  equation records; regenerate student 03 only and update teaching documentation.
- [x] Verify execution/conservation, student masking, generated-copy equality,
  rendered equations/tables and worksheet previews.

Scope: a replacement of 03.1's presentation and scientific specification task.
No new integration, coding exercise or prerequisite. The provisional 55-minute
allocation and existing 60-minute/optional-contour fallback still need a novice
pilot; clarity improvements do not establish completion time.

Verification: instructor 03 executes in an activated ESBMTK314 Jupyter kernel
with graph, boundary C/TA, restart-drift and reusable-model agreement checks
passing. All model and plotting code cells match their starting sources; only
the instructor table-display code changed. Both notebook copies validate and
student 03 regenerates exactly, with four coding blocks, completed equations,
diagram and contour answers correctly masked. The full suite ran 79 tests:
only the previously documented generated-copy differences in untouched 00/04
fail. Student table content is checked against shared records, and saved XLSX
files retain the intended blank fields with no hidden answer sheets/formulas.
Browser inspection verified chemistry/dissolution/tendency equations, compact
tables, expandable notes and instructor math layout. Worksheet previews are
readable. Protected unrelated notebook, benchmark and archive hashes match.
Evidence: `tmp/03_equation_first/`.

## Linked carbonate views in 01 (2026-09-23)

- [x] Introduce a supplied rotatable DIC–TA–pCO2 surface after TA inference;
  connect its labelled top-view contours with the lecture's Deffeyes diagram
  and its constant-TA cutting plane with a linked pCO2–DIC curve.
- [x] Supply a movable DIC point/tangent, a separate optional TA = 0 range,
  and an optional conserved-carbon atm overlay introduced after the budget.
  Use shared 01 chemistry, exact PyCO2SYS grid evaluations and an offline HTML
  display with no additional student package or widget-extension requirement.
- [x] Preserve the two masked 01 chemistry tasks and existing integrations;
  incorporate the view connection into the existing interpretation answer.
  Reuse the representation in 03 with its own benchmark conditions and arrows.
  Regenerate only student 01/03. Leave 00, 02, 04 and dated archives unchanged.
- [x] Update teaching goals/design/readme: target 3–5 minutes replacing part
  of sensitivity explanation, within the provisional 40-minute 01 allocation.
  No extra written answer, integration or coding task; student pilot required.
- [x] Complete numerical, browser, rendered-notebook and conservation checks.

Verification: five new scientific/display checks pass, covering direct slice
chemistry, the fitted-reference intersection, finite-difference sensitivity,
contour labels, valid atmosphere inventory and offline embedding. Both instructor
01 and 03 execute through their ESBMTK314 Jupyter kernels with existing audits;
their original executable cells are unchanged. Student 01/03 regenerate exactly,
validate and retain masking. Browser checks cover rotation, view presets, both
sliders, tangent/atm overlays, TA = 0, reset, standalone download and narrow
layout. Actual JupyterLab execution confirms the embedded explorer's scripts
and controls work. Inspected rendered Markdown/math/question/answer panels and
the final plots. The offline instructor preview is generated by
`scripts/build_carbonate_explorer.py` at `output/dic-ta-pco2-explorer.html`.

The full suite ran 79 tests, with only two subtest failures in generated-copy
equality: untouched 00 has two extra blank instructor cells and untouched 04
has one. Their nonempty generated/stored cells agree. All 135 protected
unrelated notebook/archive/data hashes are unchanged (the open Excel lock file
was excluded from hashing). No environment dependency or student setup change.
Evidence: `tmp/carbonate_explorer/` (test and execution logs, browser screenshots,
rendered reading sections, initial hashes). Student workload remains unpiloted.


## Textbook exercise refinements (2026-09-23)

- [x] Implement the core recommendations in `ref/textbook_exercise_review.md`:
  01 bicarbonate/proton TA explanation; 02 production/export/remineralization
  interpretation and reference-stock clarification; 03 supplied local DIC–TA
  contours integrated with existing flux fields; 04 buffering/compensation and
  fixed-export versus biological-response questions.
- [x] Mask instructor arrows/answers and regenerate student 01–04 only. Repair
  the 03 water-mass LaTeX expression. Retain all original integration/mapping
  code, numerical inputs, four 03 mappings and three 04 cases.
- [x] Update teaching goals, design and README. Retain provisional timings with
  explicit consolidation and a 4–6-minute target for 03's process interpretation;
  allow 60 minutes or optional contours if the opening cannot fit in the pilot.
- [x] Complete numerical, conservation, generated-copy and visual checks.
- [ ] Pilot the revised reading and reasoning load with students. The optional
  textbook follow-ups and alternative high-latitude question remain proposals.

Verification: all four instructor notebooks execute in activated ESBMTK314,
including their conservation, calibrated-state and restart checks. 03 also
executes through its actual Jupyter kernel. Original code-cell sources are
unchanged; only the two supplied contour-plot calls are added to 03. At the
workbook L_b state (21.5 °C, salinity 35, 5 bar = 50 dbar, constants option 13,
pH scale 3), PyCO2SYS gives reference pCO2 286.985 µatm. Local POC removal,
CaCO3 formation and dissolution yield 261.812, 303.731 and 271.957 µatm for
the stated 20 µmol C/kg changes, confirming the expected signs.

All eight notebooks validate and compile; student copies regenerate exactly,
with no saved outputs, purple solution panels or instructor process arrows.
Rendered reaction, mass equation, process prompt, contours, tables and question/
answer panels were visually inspected in HTML and figure previews. The full
suite runs 69 tests: 68 pass; the sole failure is the pre-existing generated-copy
mismatch in 00 (two extra blank instructor cells). 00 remains unchanged, along
with all protected benchmark/archive files (112 hashes checked). The Jupyter
kernel reported an unwritable IPython history database in the sandbox; execution
and numerical checks passed. Evidence: `tmp/textbook_implementation/` and
`tmp/notebook_qa/`.


## Implemented: exercises for independent modelling and revised 03/04 (2026-09-23)

- [x] Review current notebooks and the latest 01/02 revisions against future
  box-model and Earth system model research needs. Record the proposed student
  responsibilities, concrete replacement tasks, workload tradeoffs and optional
  independent project in `ref/exercise_revision_proposal.md`.
- [x] Refine the proposal so 03 starts with student reconstruction of the
  schematic and flux properties, then reconciliation with actual Excel tables.
  Check ESBMTK Figure 3/prose against the workbook and code: clarify F5 organic
  export, PIC/POC ratio and inorganic weathering carbon. Specify dissolution
  explicitly, signed net burial without double-counting, and brief assumptions
  about biological TA effects, pump state dependence and weathering accounting.
- [x] Implement the reconstruction and staged workbook views, plus a teaching
  flux-specification table with generated instructor/student versions. Preserve
  numerical input ownership and distinguish this documentation from executable
  process inputs. Reuse the completed diagram for 04's forcing choices.
- [x] Revise 03 around four native mappings, the changed model assumptions,
  one boundary-budget exercise and compact supplied verification. Preserve the
  benchmark and explicitly explain its historical transport-unit convention.
- [x] Revise 04 around experiment specification, matched anomalies and four
  focused interpretation/design answers, using its existing three runs.
- [x] Add optional extension 05: one student-defined question, model change,
  matched comparison, conservation evidence and interpreted figure. Supply
  numerical/plotting plumbing; mask the illustrative scientific choices.
- [x] Align teaching goals/design/README and diagram notes; regenerate only
  affected student notebooks and verify numerics, masking and rendering.
- [ ] Pilot the revised reading/reconstruction/coding workload with a novice.
  The 03/04 allocations (55/40 minutes) and optional starter (60–90 minutes)
  remain planning estimates, not measured completion times.

Status: the repository implementation is complete. 03 now starts with a blank
schematic and 14 selected flux-property fields, then reconciles actual workbook
records before four native mappings. Dissolution, signed net burial and the
source corrections are explicit; students derive one joint boundary budget.
04 specifies the existing control/OA/OAE experiment and shows matched anomalies
first, followed by four evidence/design questions. Separate Excel worksheets
are teaching documentation; production inputs remain owned by the original
workbook. Scientific references include local ESBMTK PDF page 8, the published
ESBMTK article and Middelburg et al. (2020).

Verification: instructor 03, 04 and optional 05 execute successfully both with
the notebook checker and actual Jupyter kernels in activated ESBMTK314.
03's native graph and reference-model agreement pass; maximum short-restart
drift is 0.000126 µmol/kg DIC, 0.000251 µeq/kg TA, 0.000006 ppm atm CO2 and
0.000171 m snowline. Carbon/TA audits pass in all three 04 cases. The optional
starter's matched runs conserve inventories to relative errors below 3e-15.
Its initial adjustment triggers ESBMTK's pH-change warnings between saved
samples; successful budgets do not substitute for the resolution checks
requested before using that illustrative design for research.
All six affected notebooks validate and their student copies regenerate
exactly, without instructor panels, completed diagrams or saved outputs.
The full suite runs 69 tests with two existing generated-copy failures in
unrelated 00/01; all other tests pass. Those sources/copies were not regenerated
to conceal the differences. Benchmark data and dated archives retain their
starting hashes; concurrent user edits to instructor 01 were preserved.
Rendered notebook equations, tables, panels, diagrams and figure order, and
all four worksheet-sheet previews, were inspected. Evidence:
`tmp/03_04_revision/` and `tmp/notebook_qa/`.

## Notation: distinguish inventory ratio from Revelle factor (2026-09-23)

- [x] Rename the 02 carbon inventory ratio to `r_{ocn/atm}` and its uniform-ocean
  baseline to `r_{ocn/atm,0}` in the geometry explanation, C1 inputs/derivation,
  optional lecture reference and teaching documentation. Reserve R for the
  Revelle factor and retain F for seawater equilibrium capacity.
- [x] Regenerate student 02. Preserve all code, outputs, scientific inputs,
  exercise masking and teaching scope; this supersedes the earlier R notation.

## Follow-up: simplify 02 around its main story (2026-09-23)

- [x] Centre the reading route on dividing the ocean, maintaining a gradient,
  and supplying the carbon needed for the full reference state. Keep B2's
  deep-box equation prominent and the full budgets in a collapsible reference.
- [x] Remove the reference/simulated export comparison, intermediate DIC/export
  and deep-transfer printouts, and the published-export discussion from the
  core notebook. Retain the atmospheric and pump–mixing figure and all checks.
- [x] Keep only the real-ocean analogy question in B4, with its masked answer.
  Move parameter identifiability to an instructor note and bridge B to C through
  the distinction between relative concentrations and total carbon inventory.
- [x] Keep local Python guidance, both student derivations and native model
  mapping. Put lecture notation details and pulse-duration experimentation in
  optional collapsible notes. Replace verbose audit output with short success
  summaries. Preserve the selected 100-year pulse and its automatic clock.
- [x] Regenerate student 02 and update teaching goals/design; retain the
  provisional 55-minute allocation pending a reading/workload pilot.

Verification: full 02 execution passes with two figures and every original
numerical assertion and audit retained. Both copies validate; student generation
matches exactly, five coding blocks and written solutions remain masked, and
browser inspection confirms the panels and expanded/collapsed reference math.
All 14 model tests and nine of 10 student tests pass. The generated-copy test
still reports existing mismatches in untouched 00 and 01. Hash comparisons
preserve every other notebook and archive; unchanged 02 code cells retain their
outputs. Evidence: `tmp/02_main_story/`.

## Follow-up: students derive the TA/uptake interpretation in 01 (2026-09-22)

- [x] Place a guided PyCO2SYS curve exercise in section 3.2, after the fully
  masked TA inference and before the revised ESBMTK run. Explain inverse
  reference-DIC/xCO2-to-TA inference versus forward DIC/TA-to-pCO2 calculation,
  and distinguish static chemistry states from time-dependent carbon transfer.
- [x] Supply the DIC grid, loop, closed-inventory atmosphere line, dry-xCO2/pCO2
  conversion and two-panel plot. Mask the forward chemistry call and output
  extraction; provide input-type, array and output hints.
- [x] Ask students to explain the falling atmosphere line, locate intersections
  and relate slopes and endpoints to net uptake. Move the zero-TA causal
  explanation into a masked instructor answer instead of stating it after
  the original diagnosis question. This supersedes the reminder placement
  recorded below. Keep the Revelle-factor connection to lecture slide 46 brief.
- [x] Regenerate student 01 and update teaching goals, design and README.
  Allow a provisional 40 minutes (10/20/10), taking five minutes from the
  completion buffer. Total remains 240 minutes; student timing needs a pilot.

Verification: complete instructor 01 execution passes, including carbon/TA
audits and calibrated endpoints. The new curve cell produces a finite plot
without warnings. A numerical regression test checks the atmosphere-line
inventory and gas conversion, slope ordering over the exercise's DIC range,
and agreement of both chemistry intersections with ESBMTK endpoints within
0.2 µmol/kg. All 14 model tests and nine of 10 notebook tests pass (23/24 total);
the only failure is the pre-existing 00 generated-copy mismatch. Both 01
notebooks validate; generation matches exactly, two code answers are masked,
and browser checks confirm equations, hints, plots and answer-panel layout.
Previous model cells and outputs, all other notebooks and archives retain
their starting content. Evidence: `tmp/01_curve_exercise/`.

## Follow-up: TA and CO2 sensitivity reminder in 01 (2026-09-22)

- [x] Explain absolute pCO2-DIC sensitivity after the post-run diagnosis
  question. Connect the steeper zero-TA response to less net carbon transfer
  before air-sea equilibrium; distinguish amount absorbed from elapsed time.
- [x] Keep Revelle sensitivity as a brief connection to ocean-carbon lecture
  slide 46: fractional DIC uptake under prescribed atmospheric CO2, fixed TA
  and thermodynamic conditions. Label its doubling estimate a linear
  approximation using fixed R; add no new calculation or experiment.
- [x] Move the reminder from section 2.2 to the post-run discussion before
  section 3, so students connect the explanation to the result just observed.
  Preserve the brief DIC/TA-to-aqueous-CO2 explanation beside the gas law.
- [x] Regenerate student 01, retaining the fully masked TA calculation.

Verification: both 01 notebooks validate and generation matches exactly;
student masking and browser-rendered math pass. Only one instructor Markdown
cell changed; all code cells and existing outputs are unchanged. All 13 model
tests and nine of 10 notebook tests pass; the existing 00 generated-copy mismatch
remains. No tasks, prerequisites or provisional timing change. Evidence:
`tmp/01_ta_sensitivity/`.

Placement and absolute-sensitivity follow-ups: exact student generation, masking, notebook validation and
rendered equation layout pass. Four focused notebook/conservation/equilibrium
tests pass; the move changes no code or existing outputs.

## Fix: optional pulse durations in 02 (2026-09-22)

- [x] Reproduce the 100-year pulse failure: ESBMTK 0.14.3.1.post0's
  under-resolved-signal warning accesses `self.model` before initialization.
- [x] Supply `finite_pulse_clock` before constructing fresh matched models.
  Resolve each pulse with at least 20 intervals and align native time samples
  to preserve the specified mass, including non-round durations. Validate
  whole-year times and a pulse strictly inside the simulation boundaries.
- [x] Expose one `pulse_duration` setting in C2, retain the user's 100-year
  choice, explain rerunning the whole cell and regenerate student 02.
  Native Signal/Source/connection construction and all student tasks remain.

Verification: 100, 333, 1000 and 5000-year native signals retain their mass;
new 100/333/5000-year integrations pass carbon/TA audits and reference endpoint
checks. The complete 02 notebook executes with its 100-year setting and two
figures: maximum relative carbon error 6.34e-10, TA change zero, final departure
from 280 ppm -1.90e-7 ppm. All 13 introductory-model tests and nine of 10 student
tests pass. The only failure remains the unrelated 00 generated-copy mismatch.
No installed ESBMTK files or notebook 01 were changed. Evidence:
`tmp/pulse_duration_fix/`. Scope and provisional teaching time are unchanged.

## Follow-up: self-contained, ungraded 01/02 route (2026-09-22)

- [x] State that the practicals are ungraded and syntax memorisation is not
  required. Introduce Python notation locally and keep the two-page coding
  reference as optional lookup; update its PDF and teaching documentation.
- [x] In 02, explain connection route names and offer a flux-law choice table.
  Mask the mixing and pump choices inside the existing exercise blocks, while
  retaining the masked analytical and numerical derivations.
- [x] Distinguish lecture equilibrium capacity F from inventory ratio R; explain
  uniform-TA mixing, replace the unplotted transient question with an endpoint
  question, and clarify the chosen pulse duration and conservation purpose.
- [x] Distinguish reference export from simulated equilibrium export in the
  labels and written answer. Ask which real pump the transfer resembles; retain
  the qualified comparison with published export estimates as optional context.
- [x] Consolidate repeated interpretation and completion prompts in both
  notebooks. Regenerate only student 01/02 and preserve their existing empty
  source cells. Keep the timing estimates provisional pending a reading pilot.

Verification in ESBMTK314: both notebooks execute successfully with their
conservation and endpoint checks passing. All 10 introductory-model tests and
nine of 10 student-notebook tests pass. The remaining generated-copy failure is
the existing pair of empty instructor cells in 00 missing from its student copy;
neither 00 file was changed. Both 01/02 student copies match generation exactly,
validate and mask solutions correctly. Code comparison confirms unchanged 01
code and equivalent 02 calculations after resolving the two new law-choice
variables and output labels. Rendered math, tables, reading panels and the
two-page reference PDF were inspected. Other notebooks and archives retain
their starting hashes. Evidence: `tmp/01_02_coherence/`.

## Draft: paired Boudreau teaching diagrams (2026-09-22)

- [x] Generate standalone instructor/student SVG and PNG schematics under
  `ref/figures/03_04_boudreau_*`, with two views of the same boxes: circulation
  and gas exchange; biological export, explicit dissolution and signed net burial.
- [x] Read numerical labels from the existing workbook and show actual table,
  parameter and native-object references. Guard the expected transport/gas
  topology. Explain the historical benchmark transport conversion and implicit
  burial boundary in `ref/boudreau_diagrams.md`.
- [x] Generate the student worksheet from the same source with three missing
  arrowheads, two process-name blanks and six transfer-property blanks. Preserve
  supplied weathering and process-module structure. No hidden solution strings
  remain in the student SVG.
- [ ] Integrate an agreed diagram exercise into 03/04 and update teaching goals
  and notebook generation together. These standalone drafts do not yet change
  active notebooks, the workbook, required tasks or provisional time allocation.

Verification: inspected both rendered PNGs after adjusting label placement;
both SVGs parse and the student masking check passes. Numerical labels and the
transport/gas topology are read from workbook named tables. No model code,
notebook sources, workbook data or archives were changed for this draft.


## Follow-up: overall readability review of 02 (2026-09-22)

- [x] Retain the A/B/C progression and add a short roadmap, numbered reading
  steps and clearer links from the buffered 01 model to the two-layer model.
  Separate supplied geometry, transport laws and the reservoir/connection task.
- [x] Separate `build_layers` from its supplied no-pump run, and the student's
  coefficient calculation from the supplied pump comparison. Explain which
  definition to rerun after completing 02.3. Preserve executable statements,
  their order, all scientific inputs and the five masked coding blocks.
- [x] Define first-order export, stationary notation, box masses, Sv/Tmol/Pmol,
  conditional results and restart/control runs at their first relevant use.
  Clarify that B fits a ratio while C supplies the inventory for the full
  reference state. Explain the forcing checks as input, budget and endpoint.
- [x] Preserve all seven question groups and five masked written answers with
  the existing reading cues. Regenerate only student 02. Clear outputs of the
  two split source cells; preserve outputs of untouched code cells.

Verification in ESBMTK314: 02 executes successfully with both figures and all
conservation, flux-balance, forcing-integral and endpoint checks passing. The
forced carbon error is 1.68e-9 of initial carbon, TA change is zero, and the final
departure from 280 ppm is 0.00000368 ppm. All 10 introductory-model tests pass;
nine of 10 student tests pass. The generated-copy test reports existing extra
empty instructor cells in 00 (two) and 01 (one), absent from their student copies.
Those files are unchanged. Both 02 copies validate, its generation matches
byte-for-byte, and both derivations/code solutions remain masked. Browser
inspection confirms readable tables, math, question/answer panels and the
student route. AST comparison confirms identical executable code and order;
hash checks preserve every other notebook and the archive. Scope and the
provisional 55-minute allocation are unchanged; the reading-load pilot remains
required. Evidence: `tmp/02_readability/` (snapshots, HTML and validation logs).

## Follow-up: clarify 01 terminology and supplied checks (2026-09-22)

- [x] Name 280 ppm dry-air xCO2 and 2040 µmol/kg DIC as the reference values at
  first introduction. Replace "numerical seed" with "small positive initial
  concentration" in prose and comments, preserving the prescribed 0.01 µmol/kg.
- [x] Define gas transfer velocity (piston velocity), retaining density in the
  flux explanation for mol/kg concentrations. Link `connect_atmosphere` directly
  to its source and explain the excerpt's local names.
- [x] Add a brief optional chemistry note and `new_model` docstring distinguishing
  species registration, prescribed DIC/TA, background boron, auxiliary Hplus/CO2aq
  and unused sediment-variable definitions. Keep all initialization supplied.
- [x] Rename the timing helper/output to `equilibration_time` / "equilibration
  time (1% criterion)" without changing its calculation. Distinguish the measured
  threshold time from an exponential relaxation constant. Use the real helper
  in the existing slower-response regression instead of duplicating its formula.
- [x] Explain assertions once and label construction, conservation and calibrated
  agreement checks. Remove duplicate TA auditing while retaining the explicit
  prescribed-carbon check. Move the expected-mismatch and slower-response
  assertions to a `solution-only` instructor verification cell.
- [x] Regenerate student 01 and align teaching goals/design. Preserve the reading
  cues and masked TA exercise. No new student task or scientific input; the extra
  clarification remains within the provisional reading-load pilot.

Verification in ESBMTK314: instructor 01 executes with both figures and all
carbon/TA, endpoint and instructor-outcome checks passing. The unchanged timing
criterion gives 72, 64 and 142 years for the baseline, alternative partition and
half-velocity cases. All 10 introductory-model tests pass. Nine of 10 student
tests pass; the sole failure is an unrelated 00 generation mismatch already in
the starting worktree: instructor 00 has two extra empty, untagged code cells
that its student copy lacks. Neither 00 file was changed in this revision.

Both 01 copies validate and generation matches byte-for-byte. Rendered HTML and
browser inspection confirm readable terms, equations, helper links, assertion
guidance and coloured panels; all seven question groups remain, and no instructor
answers or outcome assertions leak into student 01. Model construction, chemistry,
run and audit calls are unchanged. Edited code-cell outputs were cleared to avoid
stale labels. Hashes confirm every other notebook and archive is unchanged.
`git diff --check` passes. Logs: `tmp/01_terms_execution.log`,
`tmp/01_terms_tests.log`, `tmp/01_terms_verification.log`; HTML previews and
starting snapshots: `tmp/notebook_qa/01_terms/`.

## Follow-up: permanent configuration naming and notebook 00 (2026-09-22)

- [x] Add the lasting naming rule to `AGENTS.md`: use `config` for the shared
  teaching configuration in active notebooks and student-facing examples;
  preserve carbon notation and inventory names and leave dated archives unchanged.
- [x] Apply the alias rename to instructor 00's setup, worked example, solution
  calculations and explanations; regenerate only its student copy. Preserve the
  eight exercises, chemistry choices, values, answer masking and reading cues.
- [x] Align README, teaching goals, design guidance and the existing 00 masking
  test with `config.chemistry`. This changes no tasks, prerequisites or timing.

Verification in ESBMTK314: instructor 00 executes successfully and all 10 student
notebook tests pass, including exact generation for every core copy. Both 00
copies validate. Source/AST comparison confirms only the alias changed;
rendered Markdown is identical after normalizing that name, including styled
panels and answer tables. Existing instructor outputs and metadata are preserved.
Hashes confirm all other notebooks and archives retain their starting contents.
`git diff --check` passes. Logs: `tmp/00_config_rename.log`,
`tmp/00_config_execution.log`, `tmp/00_config_student_tests.log`.

## Follow-up: permanent reading convention across 00–04 (2026-09-22)

- [x] Put the lasting rule in `AGENTS.md` and the palette, authoring examples,
  accessibility cues and solution-masking instructions in
  `ref/notebook_readability.md`; link the guide from README. Keep WORKPLAN as
  implementation history rather than the only source of the convention.
- [x] Extend 01's gold key terms, blue question panels and purple written
  answers to instructor 00/02/03/04. Label existing instructor-only reference
  and verification notes accurately. Keep supplied explanations/run instructions
  distinct from student scientific prompts and retain existing code-role labels.
- [x] Regenerate the four student copies through the shared builder. In 00,
  replace the redundant inline answer prefix with the panel label, allowing
  all four written result tables to render correctly. Preserve its eight-part
  scope, unrelated usage example, calculation cells, values and interpretations.

Verification in ESBMTK314: all 30 student-generation, introductory-model,
boundary-audit, forcing-budget and scenario-smoke tests pass. Regenerating 00
also resolves the previously documented JSON field-order mismatch; all five
core student copies now match generation byte-for-byte. All ten core notebooks
validate. Render checks confirm the panel labels, four 00 answer tables and
02 derivation markup; student copies contain no purple answer panels or outputs.
Browser inspection covers 00 tables, 02 maths, 03 mapping/sediment prompts and
04 interpretation panels. Comparisons against the starting worktree confirm
unchanged executable cells, instructor outputs, scientific text and question
wording, excluding new presentation labels and the redundant 00 answer prefix.
Notebook 01, launchers, extensions and dated archives retain their starting
hashes. No teaching task, prerequisite or timing changed. Evidence is under
`tmp/notebook_qa/core_readability/` (`verification.log`, `tests.log`, HTML previews).

## Follow-up: visual reading cues in 01 (2026-09-22)

- [x] Highlight selected key concepts in pale gold; put the seven existing
  question groups in blue panels and four written instructor solutions in
  purple panels. Add a short reading key alongside the existing code labels.
  Keep explicit question/answer labels and bold key terms so colour is not
  the only distinction. Use self-contained HTML styles in Markdown cells;
  no setup cell, extension or stylesheet installation is needed.
- [x] Keep answer panels entirely inside the existing solution markers and
  regenerate student 01 through `build_student_notebook`. Preserve executable
  cells, outputs, scientific wording, exercises, workload and all other notebooks.

Verification: inspected the rendered question/answer layout in the browser.
Both 01 notebooks validate, Markdown inside panels renders, and the student
copy matches generation exactly with all four written solutions and the code
solution masked. All 10 introductory-model tests pass, including carbon/TA
conservation. Nine of 10 student tests pass; the only failure is the previously
documented untouched-00 JSON field-order mismatch, with equal parsed content.
Code cells and outputs match the starting worktree; all other notebooks and
archive files retain their starting hashes. Evidence: `tmp/01_highlights/`.
This is presentation only; learning outcomes, tasks and timing are unchanged.

## Follow-up: distinguish configuration from carbon (2026-09-21)

- [x] Rename the shared teaching-configuration alias from `C` to `config` in
  instructor 01/02, including code, comments and exercise explanations.
  Check core 03/04: neither uses this alias, so no edits are needed there.
- [x] Regenerate student 01/02 through the shared builder and align the README,
  teaching goals and design note. Preserve carbon symbols/units, notebook 00,
  all other notebooks and dated archives. Tasks and timing are unchanged.

Verification in ESBMTK314: instructor 01 and 02 execute successfully, producing
two figures each and passing their carbon/TA, equilibrium and forcing checks.
All 10 introductory-model tests pass. Nine of 10 student tests pass; the only
failure remains the documented untouched-00 JSON field-order mismatch.
Both edited notebook pairs validate and match generation byte-for-byte.
AST comparison confirms unchanged executable code apart from the alias rename;
cell metadata and existing outputs are preserved. Hashes confirm all other
notebooks and archive files are unchanged. `git diff --check` passes.
Logs: `tmp/config_alias_notebooks.log`, `tmp/config_alias_model_tests.log`,
`tmp/config_alias_student_tests.log`.

## Follow-up: readable 01 and complete TA inference (2026-09-21)

- [x] Replace the two-input-type selection with a complete PyCO2SYS TA
  calculation, reusing 00's skills. Mask the input types, solver call and TA
  extraction; retain reference targets, shared settings, documentation and the
  required output variable. Explicitly distinguish 01's 16 °C from 00's 15 °C.
- [x] Separate the chemistry exercise and displayed TA from the supplied buffered
  rerun. Explain that the rerun has a revised initial TA inventory, not an
  alkalinity addition during the original experiment.
- [x] Break construction into short atmospheric, exchange-law, object-mapping
  and connection steps. Interleave the native construction code; retain the
  individual connection excerpt before the helper call. Keep directional budgets,
  flux units and explicit physical inputs, and use `atm`/`ocn` notation.
- [x] Ask explicitly which chemical assumption prevents the reference partition
  and whether any represented process can change it. Consolidate the ending into
  three synthesis sentences; supply real-ocean TA sources as context. Clarify
  that settling times are printed and define their 1% criterion.
- [x] Remove `M.connection_summary()` from both versions, retaining its removal
  from the user's starting instructor source. Regenerate only student 01 through
  the shared builder. Preserve all other notebooks, archives and user changes.
- [x] Align README, teaching goals and design. Retain 35 minutes provisionally:
  the fuller calculation increases independent work, while shorter reading and
  consolidated questions aim to accommodate it. A pilot after 00 remains needed.

Verification in ESBMTK314: instructor 01 executes successfully with both figures
and all carbon/TA and endpoint checks. All 10 introductory-model tests pass.
Nine of 10 student tests pass, including strengthened TA-masking checks; the only
failure is the previously documented untouched-00 JSON field-order mismatch.
Its parsed generated/current contents are identical. Student 01 matches generation
byte-for-byte; both edited notebooks validate, local links resolve and no student
outputs or connection-summary calls remain. AST statement comparison against the
starting source confirms preserved executable statements, with only cell grouping
and diagnostic ordering changed. Hashes confirm other notebooks and archives are
unchanged. Student-facing Markdown is reduced from 1946 to 1793 whitespace-separated
words (including code/math, excluding masked answers); this is not a timing measure.

Logs: `tmp/01_readability_notebook.log`, `tmp/01_readability_model_tests.log`,
`tmp/01_readability_student_tests.log`.
The initial simultaneous Conda launches collided on a temporary activation file;
the isolated notebook rerun passed. Temporary editing/verification scripts and
snapshots were removed after checks. No environment or numerical-model
implementation was changed.

## Follow-up: explain the single-box construction helper (2026-09-21)

- [x] Introduce `single_box` immediately before its first use in 01, linking
  it to the visible section 2 construction and `simple_models.py`. Explain fresh
  model creation, the separate run step, changed parameters and fixed total
  carbon when the initial ocean/atmosphere partition changes.
- [x] Keep this within the existing rerun/comparison reading, with no new task,
  prerequisite or timing allocation; align teaching/design guidance.
- [x] Regenerate student 01 and verify notebook validity, unchanged student
  executable cells, masking/generation and introductory-model conservation.
  Preserve the existing student-only `M.connection_summary()` cell by copying
  it into the instructor source at the same point, so regeneration retains it.

Verification: both 01 notebooks validate; the student copy matches generation
exactly and differs from its starting contents in one Markdown cell only.
Existing instructor code cells and outputs are preserved, with the student's
connection-summary cell added to the source. All 10 introductory-model tests
pass in ESBMTK314; nine of 10 student tests pass, with only the previously
recorded untouched-00 JSON field-order mismatch. `git diff --check` passes.
Logs and before-edit snapshots: `tmp/single_box_note/`.

## Follow-up: introduce individual connections before wrappers (2026-09-21)

- [x] Introduce `Species2Species` explicitly in 01 before `connect_atmosphere`.
  Show the actual constructor as a supplied Markdown reading excerpt and map
  its helper-local names to notebook objects. Explain endpoints, `ctype`, the
  exchanged species and aqueous diagnostic before discussing the signed gas law.
- [x] Reframe 02's bulk-wrapper note as a progression from that individual
  connection, with a link back to 01. Keep direct pump construction distinct
  from the gas-specific case. Preserve all executable code and user additions.
- [x] Align teaching/design guidance and regenerate student 01/02. This is
  support for the existing mapping task, with no new coding exercise; include
  the supplied excerpt in the provisional reading-load pilot.

Verification: both instructor/student pairs validate and match generation.
AST comparison confirms every displayed constructor argument matches the actual
helper. Code cells and outputs are unchanged, as are all other notebooks and
archive files. All 10 introductory-model tests pass; nine of 10 student tests
pass, with only the previously recorded untouched-00 serialization mismatch.
`git diff --check` passes. Logs: `tmp/flux_budgets/connection_order_model_tests.log`
and `tmp/flux_budgets/connection_order_student_tests.log`.

## Follow-up: brief connection-wrapper reference in 02 (2026-09-21)

- [x] Add one short reference note before the first bulk-connection exercise:
  bulk dictionaries create `ConnectionProperties` groups, which create individual
  `Species2Species` connections; `ty` selects the same law as `ctype`. Explain
  the direct gas-specific configuration and the direct single pump connection.
  Do not imply that `Species2Species` is exclusive to gas exchange.
- [x] Keep internal call-chain knowledge unassessed, with no new exercise or
  prerequisite. Align teaching/design guidance and retain provisional timing.
  Regenerate student 02; preserve all code cells, outputs and user additions.

Verification: both 02 notebooks validate and the student copy matches generation
exactly. All other notebooks/archive files retain their starting hashes. All
10 introductory-model tests pass; nine of 10 student tests pass, with only the
previously recorded untouched-00 serialization mismatch. `git diff --check`
passes. Logs: `tmp/flux_budgets/wrapper_model_tests.log` and
`tmp/flux_budgets/wrapper_student_tests.log`.

## Follow-up: consistent directional budgets in 01–03 (2026-09-21)

- [x] Use inputs minus outputs as the common conceptual formulation. In 01,
  show separate atmospheric invasion and ocean outgassing terms, their units,
  and opposite signs in the two reservoir budgets. Draw two labelled arrows
  in the coding diagram and explain how one native gas connection evaluates
  their difference.
- [x] In 02, retain separate upward/downward mixing terms in the carbon budgets
  and describe the corresponding TA terms. Show the pump as one directed
  surface output/deep input; introduce net upward mixing only afterward as
  shorthand. Keep the stationary k derivation inside the solution block.
- [x] Align 03's gas-exchange explanation with its general inputs-minus-outputs
  budget and the notation introduced in 01/02. Preserve all executable cells,
  outputs and the user's added connection-summary cells. Regenerate student
  01–03 through the existing builder.
- [x] Update teaching goals and scientific design guidance. This replaces the
  net-first explanations without adding exercises or prerequisites; retain
  provisional timings and pilot the revised reading load.

Verification in ESBMTK314: all 10 introductory-model tests pass, including
carbon/TA conservation, equal-and-opposite internal tendencies and forcing.
Nine of 10 student tests pass; the sole failure remains the untouched-00 JSON
field-order mismatch, whose parsed contents still agree. All edited notebooks
validate, and generated student 01–03 match their instructor sources exactly.
Full code-cell/output comparison against the starting worktree confirms no
executable changes or loss of user additions. All other notebooks and archive
files retain their starting hashes. Rendered and visually checked the updated
two-arrow SVG/PNG diagram. Test logs: `tmp/flux_budgets/`; temporary snapshots
and rendering intermediates were removed after verification.

`TEACHING_GOALS.md` records the maintained learning goals, workload and required/optional tasks; `ref/design.md` records scientific intent. This file tracks implementation and acceptance checks. The initial items below were implemented and verified on 2026-09-15. Subsequent dated sections record the guided revision and follow-up changes.

## 1. Shared configuration and geometry

- [x] Introduce a shared configuration for comparable 00/01/02 PyCO2SYS and ESBMTK settings, including carbonate constants, pH scale, buffer mode where applicable, and 01/02 T, S, P. Keep the 03/04 benchmark's distinct box conditions.
- [x] Replace independent hard-coded seawater densities in 01/02 with a consistent ESBMTK-derived density and test inventory calculations against implemented reservoir mass.
- [x] Prepare and document the 02 surface-layer depth from the reference pumped inventory ratio 62.4 and the other default reservoir settings; preserve the whole-ocean volume and initial carbon inventory.

## 2. Notebook 01: TA-free diagnosis

- [x] Make the first default run TA = 0 while preserving the fictional almost-all-atmosphere initial carbon setup and a clear target comparison.
- [x] Check numerical feasibility of the low-positive-DIC, TA = 0 starting state; adjust only numerical initialization if needed, without silently adding buffering.
- [x] Let students diagnose failure to match 280 ppm and 2040 umol/kg; only afterward infer TA with PyCO2SYS and rerun as a calibration/software-consistency check.
- [x] Add matched-total-carbon initial-partition and piston-velocity comparisons, with carbon and TA inventory checks.
- [x] Label the real-ocean origin of TA as contextual explanation, not a process generated by the closed 01 model.

## 3. Notebook 02: extend, calibrate or predict, then force

- [x] Make reservoir creation and conservative DIC/TA mixing student coding exercises. With no pump, assert stationary agreement with 01 and check water volume, carbon, and TA conservation.
- [x] Add the effective closure `J_pump(t) = k DIC_s(t)` and diagnose `J_mix(t) = Q rho [DIC_d(t)-DIC_s(t)]`. Use observed-gradient calibration: have students derive the expression and units of k as well as its numerical value, and label its non-independent output honestly.
- [x] Compare matched pump-on and pump-off cases at the same total carbon and TA. Report the inferred or prescribed export flux and explain the gradient's dependence on k/(Q rho).
- [x] Have students derive the extra carbon from 62.4 and the actual initial total inventory, then insert it into supplied atmospheric Signal code. Compare with the finite-box `m_d(DIC_d^*-DIC_s^*)` expression, verify integrated forcing and combined budgets, and treat the return to 280 ppm as implementation verification.
- [x] Remove the current overwrite of the mass-consistent initial xCO2 and avoid a zero-strength, separately named TA-only carbonate pump in this simplified model.

## 4. Check the 00-04 boundary and student workflow

- [x] Keep 00 focused on PyCO2SYS fundamentals; if its current present/RCP/OAE examples are retained, distinguish static chemistry demonstrations from 04's full OA/OAE experiments.
- [x] Check 03's construction/benchmark scope and 04's attribution/forcing/feedback scope against the revised 01/02 goals; avoid duplicating scientific claims or forcing interpretation.
- [x] Pace 04's three strands as core matched-control analysis plus a clearly marked state-dependent-feedback extension for mixed-background students.
- [x] Resolve inconsistent displayed notebook numbers (00-04 versus 05-08/07-08) in the notebooks and README, without changing the scientific sequence.
- [x] Add a maskable instructor/student workflow for 01/02 coding and reasoning exercises without disturbing the existing 03/04 builder. Edit instructor sources before regenerating any student copies.
- [x] Run notebook and model tests after implementation. Add checks for 01/02 conservation, no-pump equivalence, calibrated-versus-predicted labels, and finite forcing mass.

## Initial acceptance evidence (2026-09-15; geometry superseded below)

- Shared inputs live in `teaching_config.py`; `simple_models.py` supplies native ESBMTK construction and inventory helpers. Ocean density is 1025.748495 kg/m3 at 16 °C, S = 35, P = 0 bar. The ocean volume is 1.35e18 m3; the prescribed 100 m surface occupies 3.6e16 m3 and the deep box 1.314e18 m3. Tests inspect the actual ODE coefficients to verify implemented reservoir masses and equal-and-opposite transport tendencies.
- Notebook 01 successfully starts at DIC = 0.01 umol/kg with TA exactly zero. Its endpoint is approximately 12561.78 ppm and 470.14 umol/kg DIC. PyCO2SYS then infers TA = 2348.236212 umol/kg under the shared settings; the buffered runs agree with 280 ppm and 2040 umol/kg across initial partitions and piston velocities. No alkalinity is added during any run.
- Notebook 02 uses the calibration-first route. With the same initial carbon and TA inventory, no-pump equilibrium agrees with 01; the fitted pump gives approximately 133.32 ppm, 1871.26 umol/kg surface DIC and 2063.89 umol/kg deep DIC. The fitted ratio is explicitly distinguished from these conditional outputs.
- The lecture carbon-addition estimate is 267.624 Pmol C; the independently prescribed finite-box geometry gives 283.045040 Pmol C. The square signal's sampled and piecewise-linear integrals agree with the requested inventory. The maximum time-resolved carbon-budget error is about 1.4e-9 of initial carbon; the final departure from 280 ppm is about 3e-6 ppm. Both are software/conservation checks, not independent pump validation.
- The 34-test suite passes, including the unchanged 1000 kyr Boudreau regression. All five 00–04 notebooks execute successfully through `scripts/check_notebooks.py`, including 04's optional feedback section. The updated 01/02 were re-executed after improving transient resolution. Generated 01–04 student copies match their instructor sources and contain no solutions or saved outputs.
- The original top-level 01/02 paths now link to instructor and student versions. Notebook 00 is a short chemistry prerequisite; 04 marks feedbacks as an optional extension. Displayed numbering is consistently 00–04.

### Numerical and benchmark boundaries

- Activate the Conda ESBMTK environment when running on Windows; its `Library/bin` must be on PATH for numerical DLLs. No environment packages or benchmark equations were modified.
- Native carbonate-system-1 can flag changes in pH between stored points during large transients. These warnings are documented; budget and stationary-state checks pass. Transient pH is not a scientific outcome of 01/02.
- The 03/04 benchmark retains its historical native transport-scale conversion and box-specific chemistry. Notebook 03 explains that convention explicitly. The simplified 01/02 models use explicit density-based mass transport. Changing the benchmark convention would require a separately labelled sensitivity experiment.

## Follow-up: restore 00 examples (2026-09-15)

- Restored the Present (TA 2100 umol/kg, xCO2 430 ppm), RCP8.5-labelled endpoint (935 ppm), and aragonite-saturation-target OAE examples using the current notebook structure and shared carbonate choices.
- Temperature, salinity and pressure are visible in the setup and passed explicitly in every PyCO2SYS call. Defaults remain the shared 16 °C, S = 35 and 0 dbar; the notebook explains how to revisit the original 15 °C example.
- Each example is labelled as a static equilibrium calculation. The OAE TA is inferred from a prescribed saturation target, with no claim of an independently predicted outcome or a closed carbon budget.
- Executed all 00 cells successfully in ESBMTK314 with `python scripts/check_notebooks.py notebooks/00_PyCO2SYS.ipynb`; the saturation-target assertion passes. At the shared conditions, the required TA enhancement is approximately 816.73 umol/kg. The existing Python 3.14 kernel metadata is preserved.

## Follow-up: student derivations and 62.4 geometry (2026-09-15)

This revision supersedes the original 100 m geometry and the lecture-versus-box mismatch exercise above.

- The instructor supplies the first-order pump assumption. Students derive the stationary balance, k expression, units and value; both mathematical and code solutions are masked.
- `teaching_config.py` derives surface depth from the pumped ratio 62.4, reference DIC/xCO2, atmospheric size, ocean geometry and ESBMTK density. Defaults give about 298.75 m; no rounded 57 is used. The baseline carbon inventory remains the mass-consistent 01 value.
- Students derive the target total carbon and subtract the existing inventory, then insert `extra_carbon_mol` into the supplied forcing code. The exact baseline ratio is about 56.9998256 and the extra carbon about 267.6326 Pmol C. The finite-box expression is an analytical cross-check.
- Geometry is labelled as ratio-derived, k as fitted, and the final return as forcing/conservation verification. No independent pump validation is claimed.
- Verification in ESBMTK314: the full 36-test suite passes, including the Boudreau regression, ratio-derived geometry and unchanged initial-inventory checks, carbon/TA conservation, and student solution masking. Notebook 02 executes successfully; its no-pump endpoint matches 01, its forced budget error is approximately 1.7e-9 of initial carbon, and its final xCO2 is within 0.000004 ppm of 280 ppm. Student copies were regenerated from the instructor sources.

## Follow-up: shared Excel reservoir inputs for 03/04 (2026-09-15)

- Added `data/Boudreau_2010/reservoirs.xlsx` with named ocean and atmosphere tables, explicit units, initial-state labels, provenance, and editing/restart instructions. All benchmark reservoir inputs were migrated without numerical changes; atmospheric size explicitly preserves the previous ESBMTK default of 1.7786e20 mol.
- `reservoir_inputs.py` validates literal numeric cells, table schemas, box IDs and physical ranges. It returns readable parameter dictionaries and preserves benchmark construction order after Excel sorting. Reservoir defaults were removed from `presets.py`; `load_boudreau_parameters` reads a fresh workbook snapshot and adds process settings.
- Notebook 03 displays the imported tables, supplies a one-row ESBMTK mapping, and retains the marked reservoir/connection construction exercises. Notebook 04 passes the same workbook configuration to independent matched cases. Both display density-based inventory information and distinguish workbook initial values from archived restart state.
- Added and installed `openpyxl` 3.1.5 in ESBMTK314 for reading; `requirements-excel.txt` documents the dependency. Workbook authoring and visual verification used the bundled spreadsheet runtime. README and design guidance describe the workflow.
- Verification: all 45 tests pass in ESBMTK314, including the 1000 kyr Boudreau regression, existing carbon/TA and forcing checks, eight workbook input/mapping tests, and generated-student checks. The edited-workbook test verifies changes reach actual reservoir geometry, DIC and atmospheric inventory. Inventory checks inspect density-based ODE coefficients rather than nominal pre-run `.m` arrays.
- Both 03 and 04 execute successfully through `scripts/check_notebooks.py`, including 04's optional feedback section. Student copies were regenerated from instructor sources. The workbook was exported, read back through the model loader, and visually checked for legibility.

## Follow-up: full Excel model definition for 03/04 (2026-09-15)

- Expanded the baseline into `data/Boudreau_2010/model_definition.xlsx`: Reservoirs (ocean, atmosphere and boundary nodes), Transport, GasExchange and Parameters. The old reservoir-only workbook was locked by an open application, so it was preserved as a superseded file; all current model/notebook paths load the new workbook.
- Chose the simple geometry route requested by the user: retain explicit benchmark area and volume through the adapter, with no exposed `area_percentage` or depth-based geometry conversion. Notebook geometry notes distinguish the benchmark sizes and box-specific conditions from 01/02. README explains the unused native hypsometry alternative for maintainers.
- `model_inputs.py` reads named tables, validates units/IDs/order, checks per-box water balance, and produces dictionaries for the documented ESBMTK constructors. Directed mixing arrows are explicit; shared rates are referenced by parameter name. `presets.py` no longer contains baseline numerical process/chemistry/feedback parameters.
- PIC export is derived from POC and PIC/POC ratio; carbonate-weathering TA is derived as twice weathering DIC. Excel displays the linked formulas; Python derives values from the literal inputs and does not depend on formula caches. PIC DIC/TA fluxes remain linked 1:2 in fixed and feedback cases.
- Updated 03's reservoir, transport and gas-exchange construction solutions to consume workbook rows, retaining masking and the supplied one-row example. 04 displays and reuses the full definition, while forcing amounts, strengths, feedback switches and equations remain in Python. Its gas-exchange plots use the loaded piston velocity.
- The storage diagnostic now reads the actual workbook transport graph and uses ESBMTK density-based water masses and initial inventories. An added-transport conservation test exposed the old nominal `.m`-based diagnostic masses; correcting them improved tag closure without changing the physical model equations.
- Verification in ESBMTK314: all 50 tests pass, including the 1000 kyr benchmark regression, workbook parameter edits, changed conservative transport topology, actual carbon/TA inventories, tag reconstruction, PIC coupling and generated-student checks. Both 03 and 04 execute successfully, including optional feedback experiments. Student copies were regenerated from instructor sources.
- Visually checked all four worksheets. Tested the live PIC formula against an edited/restored POC input before export, and checked the saved workbook through the model loader. README and data provenance now identify the new authoritative workbook and its supported scope.

## Guided four-hour revision (2026-09-16)

User scope: leave 00 unchanged because it supports a separate external question
set; archive the current 01–04 versions; implement guided simplification of 01–04
while retaining ocean-carbon concepts and diagram-to-code mapping; maintain a
Markdown summary of teaching goals with future work.

- [x] Freeze the earlier 01–04 instructor/student sources and 01/02 launchers in
  `archive/2026-09-16_before_guided_revision/`. Include their supporting model code,
  data, tests, generation/check scripts and design documents; preserve all 70
  payload files byte-for-byte with a SHA-256 manifest. Exclude 00, application lock
  files and generated caches. Document explicit archived notebook execution.
- [x] Leave `notebooks/00_PyCO2SYS.ipynb` unchanged. Before/after SHA-256:
  `b18d1da7936e8335e0c06d426dcd1e6d74eaa6cd31220ffb3bb3572540266c4e`.
- [x] Add `TEACHING_GOALS.md` with per-notebook learning outcomes, time allocations,
  required student work, supplied infrastructure, evidence and optional scope.
  Require maintenance alongside future teaching edits in `AGENTS.md`; align
  README and design guidance. The four-hour plan includes a provisional 20-minute
  slot for the unknown external 00 question set; timings await a student pilot.
- [x] 01 (35 minutes): retain the supplied native construction, TA-free diagnosis
  and buffered calibration. Limit code work to selecting the DIC/xCO2 input types;
  supply partition/rate comparisons and audits. Add an explicit diagram and
  cancellation-of-internal-fluxes explanation.
- [x] 02 (55 minutes): scaffold reservoir fields, mixing endpoints/species and
  DIC-only pump choices. Retain both masked analytical/numerical derivations for k
  and the carbon addition, unchanged prepared geometry and initial inventory, and
  supplied native Signal code. Make the finite-box numerical cross-check
  instructor-only; students still explain its algebraic equivalence.
- [x] 03 (55 minutes): retain native construction with four focused mapping tasks.
  Supply Model setup, repetitive loops, chemistry/sediment wiring and weathering
  construction. Keep all directed arrows, graph and stationarity checks, explicit
  workbook geometry and benchmark conditions. Move detailed sediment equations to
  `ref/sediment_reference.md`; keep qualitative DIC/TA transfers and sediment memory.
- [x] 04 (40 minutes): require forcing-inventory conversions and OA/OAE endpoint/
  species choices. Supply matched complete-model runs, forcing and boundary-aware
  C/TA checks, and four diagnostic groups plotted as forced-minus-control responses.
  Move the longer tagging, full benchmark plots and feedback analyses into the
  self-contained `extensions/04_attribution_and_feedbacks.ipynb` instructor/student
  pair, outside the required route.
- [x] Move repetitive core plotting to `teaching_plots.py`; add supplied complete-
  model checks in `teaching_audits.py`. Regenerate all student copies. Generation
  includes the extension; normal notebook execution excludes it unless an explicit
  path or `--include-extensions` is supplied. Neither default traverses the archive.

### Verification and numerical boundaries

- ESBMTK314: all 56 tests passed, including the unchanged 1000 kyr Boudreau
  regression and 01/02 geometry, mass and forcing tests. After final audit and
  scaffold refinements, all 14 student-generation and audit tests passed again.
- All four revised instructor notebooks execute successfully in fresh processes;
  the independent optional extension also executes successfully, including feedback
  cases. Student copies match instructor sources, contain no saved outputs or
  solution markers, and preserve the supplied native constructor scaffolds.
- 01/02 preserve the original numerical results. The no-pump extension matches 01;
  02's maximum forced carbon error is about 1.68e-9 of initial carbon and the final
  departure from 280 ppm is about 3.68e-6 ppm. 03 agrees with the independent
  reusable-model oracle. No baseline model equations or input data were altered.
- The 04 archived signal is not a zero-ended finite pulse. A separate supplied
  piecewise-linear integral handles nonzero tails without extrapolating. The
  post-1800 OA/OAE inputs are about 335.357579 Pmol C / 10.000047 Pmol TA eq;
  whole-run inputs used in the budget are 340.172309 / 10.143617 Pmol respectively.
  Tests check nonzero tails, interior integration times and rejection of incorrect
  forcing-species budgets.
- The native plotting postprocessor uses stored H+; the solver's carbonate function
  first updates it and applies its carbonate floor. For a valid conservation check,
  the audit re-evaluates the existing solver function at saved states rather than
  treating display-approximation differences as missing carbon. It changes no
  model equations. The largest 04 C/TA errors normalized to initial stock are about
  8.34e-6 / 1.11e-6 (OA); the specified 2e-5 relative check includes output-grid
  quadrature as well as solver error. PIC/dissolution TA coupling remains exact 1:2.
- Visually checked the new core OA/OAE comparison plot. Verified all 70 archive
  payload hashes and the unchanged 00 hash. Execution logs are under `tmp/` and
  rendered plots under `tmp/notebook_qa/` (generated, not teaching sources).

Remaining course-planning work: pilot the timed route, including the external 00
question set, then update `TEACHING_GOALS.md` with measured completion times.

## Follow-up: put aggregate OA/OAE analysis in core 04 (2026-09-16)

The user requested that extension Part II belong to core 04 to make the complete
response easier to understand. This supersedes the earlier placement of full
benchmark figures in the optional extension.

- [x] Move the aggregate response-chain explanations and supplied eight-panel
  OA/OAE figures (including the OA reference overlay) into core 04. Keep absolute
  benchmark reproduction distinct from matched forcing-response anomalies.
- [x] Explain the saturation horizon, compensation depth and sediment snowline
  qualitatively, including depth/elevation sign conventions and sediment memory.
  Supply a guided reading route from input to atmosphere/surface to deep ocean
  and sediments, followed by four focused answers.
- [x] Keep the same two coding tasks, prescribed inventories, three fixed cases,
  forcing/conservation checks and 40-minute planning allocation. The 15-minute
  interpretation slot now includes selected-panel reading; no panel-by-panel
  report, extra model runs or plotting task is required. Timing still needs a pilot.
- [x] Leave only Part I's attribution and Part III's feedback teaching in the
  extension. Retain supplied fixed-case prerequisites and forcing checks so the
  feedback section remains executable in a fresh kernel. Remove the duplicate
  aggregate-response questions/figures and fix roadmap/section numbering.
- [x] Move plotting and response-summary implementation into `teaching_plots.py`;
  update `TEACHING_GOALS.md`, README, design guidance and 03's figure cross-reference.
  Regenerate student copies without changing 00 or the frozen archive.

Verification in ESBMTK314: all 14 student-generation and teaching-audit tests
passed. Both revised notebooks execute successfully in fresh processes: core 04
produces three figures and the reduced extension produces four, including all
feedback runs. Core forcing inventories and carbon/TA budget checks retain their
previous results. Visually inspected both restored eight-panel figures, including
the OA overlay, OAE forcing units and horizon sign conventions. Generated copies
were rechecked after the 03 cross-reference edit. Verified that 00 and all 70
frozen archive payloads are unchanged. Logs: `tmp/part_ii_tests.log` and
`tmp/part_ii_notebooks.log`; plots: `tmp/notebook_qa/`.

## Follow-up: exercise 9 answer sheets for 00 (2026-09-17)

The user supplied exercise 9 (a–h) and explicitly requested revision of 00.
This supersedes earlier instructions to leave 00 unchanged for an unknown
external question set; the frozen archive remains untouched.

- [x] Add `notebooks/instructor/00_PyCO2SYS.ipynb` as the source for full
  calculations and written answers. Generate `notebooks/student/00_PyCO2SYS.ipynb`
  with only setup, one unrelated TA/DIC usage example, documentation links and
  blank calculation/answer cells for a–h. Make the original 00 path a launcher.
- [x] Preserve unmodified `C.chemistry` (10/2/1), the existing 15 °C exercise
  baseline, and dry-air xCO2 input type 9. Explain the ppm/µatm distinction.
  Include temperature and salinity sensitivities, historical CO2 comparisons,
  calcite/aragonite saturation, 935 ppm at 15/18 °C and both TA inversions.
- [x] Distinguish prescribed inputs, conditional equilibrium outputs and inferred
  TA. Avoid interpreting small pH sensitivity as small ecological or saturation
  sensitivity. Explain why the saturation target is not independent validation
  of reef protection, a closed carbon budget or a total alkalinity dose.
- [x] Include 00 in student generation and default instructor execution. Remove
  positional 01–04 assumptions from notebook tests and check that 00 retains
  exactly one worked example while all eight answers remain hidden.
- [x] Update learning goals, README, scientific design and maintenance guidance.
  Revisit the now-explicit eight-part workload: the 20-minute slot remains a
  reservation requiring a pilot, with no claim that all eight parts fit and no
  reduction of the 01–04 tasks.

Verification in ESBMTK314 / PyCO2SYS 1.8.3.4: instructor 00, generated student 00
and the launcher execute successfully and validate as notebooks. Present pH is
7.982009 and aragonite saturation is 1.974696. The inferred TA additions are
822.350367 µmol/kg at 15 °C and 637.244185 µmol/kg at 18 °C; re-solving with
TA/xCO2 reproduces the target saturation and inferred-state pH within 1e-8.
All 20 student-generation and introductory-model tests passed, including carbon/TA
conservation, geometry and finite forcing checks. After replacing Unicode console
labels with portable ASCII, all 10 student checks passed again. Logs:
`tmp/00_notebooks.log`, `tmp/00_tests.log`, `tmp/00_student_tests.log`.
The user's existing instructor-04 changes were preserved; generation only
synchronized its student copy's empty cell and JSON field order with that source.

## Follow-up: novice-modeller experiment in 01 (2026-09-17)

- [x] Replace the opening with a fictional atmosphere–ocean verification
  experiment. Present recovery of the two familiar reference values from their
  combined carbon inventory as the modeller's hypothesis, not a guaranteed result.
- [x] Use a neutral title and idealized saline-water wording consistent with the
  supplied seawater chemistry. Keep TA = 0 distinct from the low-DIC numerical seed.
- [x] Replace the prediction/diagnosis prompt with before/after reflection on
  inventory versus partition and implementation versus physical adequacy. Place
  the masked explanation and numerical mismatch assertion after the first run.
- [x] Retain the existing model, calibrated rerun, comparisons and one coding
  exercise. Update teaching goals, design and README; retain the provisional
  35-minute allocation with the revised prompts replacing the existing task.

Verification in ESBMTK314: instructor 01 executes successfully and produces two
figures; all 10 introductory-model tests pass, including carbon/TA conservation.
The generated 01 copy matches its source exactly, and student masking, exercise
counts and scientific-label checks pass. All executable statements are preserved;
only the mismatch assertion moves to after the diagnosis. The full 10-test
student suite has one failure: the pre-existing byte-for-byte generation mismatch
in 00 caused solely by JSON field order. Reproducing generation from HEAD confirms
that it predates this edit; parsed notebook contents agree. Restored the builder's
incidental 00 reordering so 00, 02–04 and the frozen archive remain unchanged.
Logs: `tmp/01_framing_notebook.log`, `tmp/01_framing_model_tests.log` and
`tmp/01_framing_student_tests.log`.

## Follow-up: shared conceptual-model-to-code reference (2026-09-17)

- [x] Add `ref/modelling_cheatsheet.md` and a two-page printable companion at
  `output/pdf/modelling_cheatsheet.pdf`. The Markdown is the single source;
  `scripts/build_modelling_cheatsheet.py` renders it with optional authoring-only
  ReportLab/pypdf dependencies and checks the page count.
- [x] Map boxes, states, arrows, boundaries, inputs and diagnostics to code.
  Include one unrelated, artificial passive-O2 tank transfer with an explicit
  balance, native ESBMTK constructors and analytical endpoint. Explain mol/L
  inventory conversion separately from ocean mol/kg and ESBMTK-density conversion.
  Keep pump/carbon-addition derivations and exercise solutions out of the guide.
- [x] Explain the recurring Python patterns, input/helper locations, execution
  order, rebuilding after edits, restart state versus model graph, and checks.
  Label nonempty student-facing code cells in 01–04 **Choose and explain**,
  **Understand and run**, or **Supplied implementation**. Supply the common legend
  and both guide links in each opening. Labels add comments only; executable
  statements and all exercise/solution markers are preserved.
- [x] Introduce the reference within 01's existing diagram/worked-example activity.
  The standalone tracer is optional reference, with no additional assignment,
  submission or student dependency. Update README, teaching goals and design;
  explicitly retain the need to pilot this orientation within the planned time.
- [x] Regenerate only the edited 01–04 student copies using
  `scripts.build_student_notebooks.py`'s `build_student_notebook` function.
  Preserve existing worktree changes, notebook 00 and the dated archive.

Verification in ESBMTK314: all four instructor notebooks execute in fresh
processes with their existing graph, stationarity and conservation checks.
The standalone tracer conserves its 3 mol inventory at all saved times and
matches both analytical 1.5 mol endpoints (relative tolerances 1e-9 and 1e-8).
Of 25 student-generation, introductory-model and teaching-audit tests, 24 pass;
the sole failure is the previously documented untouched-00 JSON field-order
mismatch. Confirmed that its parsed generated/current contents agree exactly.
The 01–04 copies match generation byte-for-byte; links and code labels resolve,
and AST comparison against the pre-edit worktree confirms unchanged executable
statements. All protected 00 and archive file hashes match the pre-edit snapshot.
Rendered and visually inspected both final PDF pages, including code, tables,
workflow arrows and footers. Logs: `tmp/cheatsheet_tests.log` and
`tmp/cheatsheet_notebooks.log`. Temporary layout previews were removed after QA.

## Follow-up: visual box-to-code architecture (2026-09-21)

- [x] Replace the cheatsheet's mapping table with a standalone diagram showing
  reservoir geometry, evolving tracers, initial concentrations and environmental
  conditions, plus a connection with short native constructor/attribute labels.
  Distinguish species definitions, box-specific states and concentration series.
- [x] Attach a smaller legend for carbonate calculations, explicit species
  coupling and external forcing. Use solid material arrows and dashed information
  arrows; distinguish the code container from the physical system boundary.
  Label the generic connection as one internal transfer, not a complete water graph.
- [x] Replace 01's worked-example mapping table with a matching atmosphere/ocean
  diagram using actual helper/object names. Identify atmospheric CO2, ocean DIC,
  and calculated CO2aq separately, with the chemistry-to-gas-law information link.
  Keep the existing diagram-check questions and marked solutions. Add no new task.
- [x] Add reproducible diagram source in `scripts/build_coding_diagrams.py` and
  SVG/PNG assets under `ref/figures/`. The PDF builder regenerates those assets
  and embeds the same vector drawing in the two-page handout. ReportLab, pypdf
  and Poppler remain optional authoring dependencies, not student prerequisites.
- [x] Update README, learning goals and design; regenerate student 01 through
  the existing student builder. Preserve the other notebooks, archive and existing
  worktree changes. Orientation remains within the provisional time allocation
  and still requires a novice-student pilot.

Verification: instructor 01 executes successfully in ESBMTK314 with its existing
carbon/TA audits and two figures. Of 20 student-generation and introductory-model
tests, 19 pass; the sole failure remains the untouched-00 JSON field-order
mismatch, whose parsed contents still agree. Student 01 matches its generated
source byte-for-byte, image links resolve, and AST comparison confirms unchanged
executable code. Hashes confirm that every other notebook and all archive files
are unchanged from this turn's starting worktree. Visually inspected both diagram
PNGs and both final PDF pages: labels, arrowheads, information links and legends
are readable without clipping or overlaps. The handout still has exactly two
pages. Logs: `tmp/diagram_tests.log` and `tmp/diagram_notebook.log`. Temporary
layout previews were removed after QA.

## Follow-up: physical atmospheric configuration in 01 (2026-09-21)

- [x] Explain the finite, well-mixed atmosphere before `connect_atmosphere`:
  fixed mole inventory, evolving dry-air CO2 fraction, and carbon inventory.
  State the initial-partition equation and approximately 16239.87 ppm starting
  value, distinguishing the 280 ppm reference from an imposed boundary value.
- [x] State exchange area, piston velocity, seawater thermodynamic settings and
  the closed carbon budget. Keep executable code and the prediction/diagnosis
  sequence unchanged. Regenerate student 01 from its instructor source.
- [x] Align teaching goals and design guidance. This elaborates the existing
  supplied reading with no additional exercise or prerequisite; the 35-minute
  allocation remains provisional and its reading load requires a student pilot.

Verification in ESBMTK314: all 10 introductory-model tests pass, including
carbon/TA conservation and initial-partition comparisons. Nine of 10 student
tests pass; the sole failure is the previously recorded untouched-00 JSON
field-order mismatch, with parsed contents confirmed identical. Both edited
01 notebooks validate and student 01 matches generation byte-for-byte. AST
comparison confirms unchanged executable code; all other notebooks and archive
files match their starting hashes. Logs: `tmp/atmosphere_note/model_tests.log`
and `tmp/atmosphere_note/student_tests.log`.

## Follow-up: explicit atmospheric invasion term in 01 (2026-09-21)

- [x] Replace the equilibrium aqueous-CO2 label in the invasion term with
  solubility times atmospheric CO2, following equation 6 of the ESBMTK paper.
  Explain the distinct atmospheric and ocean dependencies, concentration/flux
  units, equal-and-opposite transfers and balanced nonzero rates at equilibrium.
- [x] Map the displayed atmospheric term to the code's dry-air mole fraction
  through the helper's supplied solubility, scaling and gas-convention corrections.
  Regenerate student 01 and align teaching goals/design. This replaces supplied
  reading within the existing provisional allocation, with no new exercise.

Verification in ESBMTK314: all 10 introductory-model tests pass. Nine of 10
student tests pass; the sole failure remains the untouched-00 JSON field-order
mismatch, whose parsed contents agree. Both 01 notebooks validate and student 01
matches generation byte-for-byte. Exactly one instructor Markdown cell changed;
all executable code, outputs and other cells are unchanged. Other notebooks and
archive files retain their starting hashes. Jupyter execution encountered a
DeadKernelError; as a fallback, all seven instructor code cells execute in order
in a fresh ESBMTK314 process with a noninteractive plotting backend, passing all
existing assertions and carbon/TA audits. Logs are in `tmp/gas_explanation/`
(`model_tests.log`, `student_tests.log`, `notebook.log`, `code_execution.log`).

## Follow-up: clarify the initial DIC seed in 01 (2026-09-21)

- [x] Replace the abstract saline-water paragraph with the requested NaCl-solution
  picture: dissolve a trace of CO2 to supply initial DIC while TA remains zero,
  place almost all remaining carbon in the atmosphere, then allow gas exchange.
- [x] Move the distinction between this initialization picture and the supplied
  seawater chemistry settings to the system-specification section. Preserve the
  closed boundary and target-derived inventory; add no forcing or code changes.
- [x] Regenerate student 01 through the existing builder; align teaching goals
  and design. This replaces wording within the existing task and time allocation.

Verification in ESBMTK314: instructor 01 executes successfully with its carbon/TA
audits and two figures; all 10 introductory-model tests pass. Both 01 notebooks
validate and the student copy matches generation byte-for-byte. Executable cells
are unchanged from this turn's starting worktree. Nine of 10 student tests pass;
the sole failure remains the previously recorded, untouched-00 JSON field-order
mismatch. Logs: `tmp/01_nacl_execution.log`, `tmp/01_nacl_model_tests.log` and
`tmp/01_nacl_student_tests.log`.

## Investigation: Windows native crash and student setup (2026-09-21)

- [x] Reproduce `0xc06d007f` without visible crash dialogs using a small NumPy
  linear solve. Capture the delay-loaded DLL and missing symbol: `libiomp5md.dll`,
  `__kmpc_global_thread_num`, Windows error 127. Confirm the DLL export forwards
  to `libomp.dll`; the latter is absent from the captured failing process.
- [x] Verify that environment PATH setup and standard `conda run -n ESBMTK314`
  both resolve the failure. NumPy/SciPy linear solves and GSW/ESBMTK density
  calculations pass. All seven current instructor 01 cells also execute through
  the registered ESBMTK314 Jupyter kernel under `conda run`, including audits.
- [x] Record stale overlapping NumPy metadata (pip 2.5.2, Conda/imported 2.5.3)
  as a separate reproducibility concern. Do not infer a package reinstall is
  needed to resolve the demonstrated activation failure.
- [x] Add the verified environment-aware launcher to README and write
  `ref/environment_setup_proposal.md`: propose uv, a TOML manifest, pinned Python
  and a tested lockfile for students without Python, with Pixi and hosted
  JupyterHub alternatives. This is a proposal; active course prerequisites and
  notebook code remain unchanged. No global environment or package changes.

Evidence: `tmp/environment_diagnosis/dll_failure.log`,
`numerical_activated.log`, `conda_run.log` and `conda_jupyter.log`. Temporary
diagnostic scripts suppress crash dialogs in their own processes and log native
failures. The README launch clarification and proposal do not alter teaching
tasks or timing; a clean cross-platform installation pilot is required before
adopting a new student environment.

## Follow-up: Anaconda alternative for students (2026-09-21)

- [x] Supply `environment-anaconda.yml` and `ref/anaconda_setup.md` for students
  already using Anaconda/Miniconda. Use a separate `esbmtk-practicals` environment,
  Python 3.14 and the reference ESBMTK/PyCO2SYS pins. Conda owns Python/pip;
  pip owns the complete scientific/Jupyter stack to avoid overlapping installs.
- [x] Document creation, activation, environment-local kernel registration,
  explicit kernel selection, repeat launches and a small numerical check.
  Link the alternative from README and the environment proposal; record its
  pilot status in teaching goals without adding class work or changing timing.

Verification: YAML and all dependency strings validate; pip's dry run with
`--ignore-installed --only-binary=:all:` resolves the entire package stack for
Windows/Python 3.14. No packages were installed or existing environments changed.
The documented linear-solve check passes under activated ESBMTK314. Full fresh
installation/model verification and macOS pilots remain required; the YAML is
not a resolved lockfile. Evidence: `tmp/anaconda_setup/pip-resolution.log` and
`pip-resolution.json`. No notebooks or model code were edited in this change.

## Follow-up: printable student setup handouts (2026-09-21)

- [x] Generate two-page uv and Anaconda student PDFs under `output/pdf/`,
  with readable terminal commands, OS-specific setup steps, kernel selection,
  a notebook numerical check, repeat launches and brief troubleshooting.
- [x] Keep pilot status explicit. The uv handout requires instructor-supplied
  project files and lockfile; it does not claim those files are already present.
  Preserve the separate Anaconda recipe and current instructor environment.
- [x] Add reproducible ReportLab builder `scripts/build_setup_pdfs.py`; link
  both PDFs from README and describe them as existing pre-class setup support
  in teaching goals. No new class exercise or timetable change.

Verification: both PDFs have exactly two A4 pages, embedded fonts and clickable
references. All four Poppler-rendered pages were visually checked for readable
commands, spacing, margins and unclipped text. The numerical-check code passes
under `conda run -n ESBMTK314`. PDF text checks and `git diff --check` pass.
No notebook sources, model code, installed packages or running kernels changed.

Follow-up: revised both setup PDFs to say "Restart JupyterLab after shutting
it down" and distinguish that operation from opening/creating notebooks inside
an already-running JupyterLab. Matched the Anaconda Markdown guide. Both PDFs
remain two pages; all four rendered pages were visually checked after rebuilding.

## Follow-up: setup-only student package and repository transition (2026-09-23)

- [x] Separate the temporary distribution message from the durable uv and
  Anaconda setup guides. Add a start document that says the package contains no
  exercises and gives route-specific commands for moving to the later GitHub
  repository.
- [x] Add a non-exercise JupyterLab orientation notebook covering cell execution,
  command/edit modes, A/B/DD/M/Y, saving, imports, numerical calculations,
  plotting and workbook access.
- [x] Replace the setup check's dependency on the Boudreau workbook with a
  labelled workbook probe containing no course inputs or answers. Move Anaconda
  instructor maintenance notes out of the student guide.
- [x] Add a fixed-allow-list ZIP builder and package tests. The setup archive may
  contain only the start guide, two setup PDFs, environment recipes, checker,
  Jupyter basics notebook and workbook probe.

This changes pre-class distribution mechanics only. It adds no exercise or
class-time requirement; setup remains a prerequisite outside the four-hour
practical timetable.

Verification: the allow-list archive contains exactly 10 files and excludes
all exercise notebooks, model data and archives. Five package tests pass,
including identical repeated ZIP builds and both transition routes. The shared
checker passes in activated ESBMTK314 from an extracted package, and the Jupyter
basics notebook executes completely there. Both three-page A4 setup PDFs were
rendered and visually inspected. Final package:
`output/ESBMTK-practicals-setup-only.zip` (SHA-256
`ED780AD8046E63F1AA16663C67A163F3F3F01EAA4382D1418822D9B4250480D9`).

## Follow-up: fresh Anaconda setup-only pilot (2026-09-23)

- [x] Extract the distributed setup-only ZIP and create the exact named
  `esbmtk-practicals` environment from its `environment-anaconda.yml` on Windows.
- [x] Verify literal activation selects the new Python 3.14.7 interpreter; run
  `pip check` and the packaged numerical/chemistry/workbook/plot checker.
- [x] Register the environment-local `esbmtk-practicals` kernel and execute the
  complete Jupyter basics notebook through that named kernel.
- [x] Launch JupyterLab from the fresh environment and extracted folder, verify
  an HTTP 200 JupyterLab response, then shut it down and confirm the port closes.
- [x] Remove only the fresh pilot environment and retain all pre-existing Conda
  environments unchanged. Update the student/instructor status text; keep
  macOS/Linux and novice-student pilots outstanding.

Verification: Conda created Python 3.14.7 and pip installed the complete recipe,
including ESBMTK 0.14.3.1.post0, PyCO2SYS 1.8.3.4, NumPy 2.5.3, SciPy 1.18.1,
JupyterLab 4.6.4 and ipykernel 7.3.0. `pip check` reported no broken
requirements. The environment checker passed, all setup-notebook success
messages appeared, and `http://127.0.0.1:8898/lab` returned HTML identifying
JupyterLab. The temporary environment and server were removed after the test.

## Follow-up: working uv setup and novice instructions (2026-09-22)

- [x] Supply root `pyproject.toml`, `.python-version` (3.14.7), a generated
  `uv.lock`, and `scripts/check_environment.py`. Keep the verified ESBMTK and
  PyCO2SYS pins and use uv-managed Python independently of existing Conda.
  Ignore local `.venv` and temporary validation files.
- [x] Add canonical `ref/uv_setup.md` and regenerate the UV PDF as three readable
  pages. Explain ZIP extraction, opening PowerShell/Terminal, concrete paths,
  `cd`/`pwd`/`ls`, commands versus notebook code, supplied manifest/lock files,
  explicit setup success, notebook creation, saving, server shutdown and later
  launches. Students need no prior Python installation or TOML editing.
- [x] Make the PDF builder read this Markdown and accept `--only uv`, preserving
  the separate Anaconda PDF. Update README, setup status and prerequisites;
  preserve teaching scope, timetable and existing notebook edits.

Verification: uv 0.12.17 downloaded managed CPython 3.14.7 into an isolated test
location and created a fresh project `.venv` with `uv sync --locked`. Lock
consistency and installed dependency compatibility checks pass. The documented
checker verifies NumPy/SciPy solves, carbonate chemistry, GSW density, the actual
model workbook and PNG plotting. All five instructor notebooks 00-04 execute
successfully with their audits. A real JupyterLab server returns HTTP 200, starts
the environment-local course kernel, executes imports and a numerical solve,
shuts down cleanly and restarts successfully. Existing Conda environments and
running user sessions were not altered.

The full suite reports 56 passing tests and one failing generated-copy equality
test. Subsequent reference-Conda verification finds two extra empty instructor
code cells in 00 and one in 01 relative to student copies; other parsed content
matches exactly. This is unrelated to uv installation, and no teaching notebooks
were regenerated. Reconcile source/copy equality before notebook distribution.

The UV PDF has three A4 pages; every latest rendered page was visually checked,
and text checks confirm commands, success and shutdown instructions. `git diff
--check` passes. Evidence: `tmp/uv_validation/{lock,sync,check,tests,notebooks,
lifecycle,reference_copy_test}.log`. macOS/Linux pilots and testing the initial
uv installer with a novice on a clean laptop remain outstanding; this machine's
validation used an isolated uv install and did not test the Windows winget UI.

## Follow-up: shared beginner explanations in Anaconda setup (2026-09-22)

- [x] Expand `ref/anaconda_setup.md` and its PDF to explain environments,
  kernels, terminals, ZIP extraction, opening Anaconda Prompt, concrete course
  paths, checking the current directory, activation and expected success output.
- [x] Use `scripts/check_environment.py` for the terminal numerical/chemistry/
  workbook/plot check. Explain notebook creation, saving, Ctrl+C shutdown, why
  closing a browser tab leaves the server running, and subsequent launches.
- [x] Render the three-page student PDF from the Markdown source using the same
  parser as uv. Keep instructor maintenance notes outside the student PDF and
  retain the Anaconda route's fresh-installation/cross-platform pilot status.
  Update current page counts in README/teaching goals; no teaching tasks change.

Verification: the shared checker passes through `conda run -n ESBMTK314
--no-capture-output`; this is a reference-environment check, not a fresh Anaconda
recipe validation. All three rendered PDF pages were visually inspected; text
checks confirm commands, success, shutdown and restart instructions. No package
installation, notebook regeneration or changes to running user sessions.

## Follow-up: simplify 03 transport notation and schematics (2026-09-24)

- [x] Use Q for water volume transport throughout 03, its paired-flux metadata,
  worksheets and schematic labels. Write physical tracer fluxes as
  J_ij^X(t) = rho_i Q_ij X_i(t), retaining the benchmark implementation caveat.
- [x] Shorten the weathering explanation to the model's 1 mole DIC : 2 TA
  equivalents and the caveat that real riverine input need not have this ratio.
- [x] Simplify both shared 03/04 diagrams to boxes, arrows and short legends;
  keep equations and Excel links in the companion table. Preserve explicit
  dissolution, sediment memory and signed net burial. Regenerate student 03
  and both Excel worksheets; retain the same exercises and provisional timing.

Verification: instructor 03 executes in ESBMTK314 with graph, carbon/TA budget,
restart and reusable-model agreement checks passing. Executable model cells
are unchanged, student 03 regenerates exactly, and unrelated notebook/archive/
data hashes are preserved. All three specification/worksheet tests pass. The
12-test notebook suite has only its existing generated-copy mismatches in 00
and 04 (extra empty instructor cells); 03 checks pass. Both diagrams, both sheets
in each Excel file, and rendered notebook math/table/caveat layouts were visually
checked. Spreadsheet error scans and `git diff --check` pass. Evidence:
`tmp/03_schematic_simplification/`.
