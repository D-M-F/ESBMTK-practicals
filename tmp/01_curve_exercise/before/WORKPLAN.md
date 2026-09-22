# Implementation workplan

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
