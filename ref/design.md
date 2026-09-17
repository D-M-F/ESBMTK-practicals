# Learning design and scientific scope

The maintained summary of the implemented core, workload, student tasks and
optional material is [`TEACHING_GOALS.md`](../TEACHING_GOALS.md). Update that file
alongside future teaching changes. The 2026-09-16 guided revision targets four
hours including a provisional 20-minute slot for 00; the unknown external 00
question set prevents verification of that part of the workload. The pre-revision
01–04 sources and their dependencies are frozen under
`archive/2026-09-16_before_guided_revision/`.

These practicals introduce first-year master's students from varied backgrounds to ocean-carbon chemistry and progressively more complex box models. The intended progression is **chemistry (00) -> missing buffering and model verification (01) -> conservative model extension and an effective pump (02) -> construction of the Boudreau-like model (03) -> experiments with the complete model (04)**.

The lecture slides, DeVries review, and ESBMTK paper are in `ref/`. The lectures already show algebraically that a larger deep-ocean DIC inventory raises the ocean/atmosphere carbon inventory ratio. Notebook 02 must therefore ask how a gradient is *maintained* and what follows from a specified mechanism, rather than present that inventory identity as a new discovery.

Across the sequence, translate each diagram's boxes, state variables, arrows, system boundary, and units into ESBMTK objects and conservation equations. Explain enough for students to understand the supplied code, while marking portions that can be hidden in student copies. Keep teaching hypotheses, calibrations, predictions, and software-consistency checks explicitly distinct.

A shared configuration should align PyCO2SYS and ESBMTK choices where the exercises are meant to be comparable: for example `opt_k_carbonic=10`, `opt_pH_scale=2`, and `opt_buffers_mode=1`, with T = 16 degC, S = 35, and P = 0 bar for 01/02. Use the box-specific benchmark conditions needed in 03/04; do not silently force the simplified 01/02 conditions onto the Boudreau-like model. For teaching, use ESBMTK's documented objects and connections where feasible. Calculate seawater density from the same T, S, and P with ESBMTK's built-in method rather than separate hard-coded density estimates, and audit inventories in consistent units.

## 00 - PyCO2SYS foundations

**Learning goal:** Use two carbonate-system inputs and fixed thermodynamic choices to calculate and interpret the remaining seawater carbonate variables.

Notebook 00 answers a separate question set outside this repository. It is unchanged
by the guided 01–04 revision and must not be shortened or reassessed without an
explicit request. Its static chemistry examples remain distinct from the coupled
OA/OAE histories, attribution and feedbacks of 04.

## 01 - Diagnose missing alkalinity in a one-ocean-box model

**Learning goals:**

1. Map an atmosphere-ocean diagram to ESBMTK boxes, states, gas exchange, and a conserved carbon inventory.
2. Explain why CO2 invasion can increase DIC but cannot create TA; infer the missing background TA with PyCO2SYS.
3. Distinguish equilibrium controls from rate controls.

Supply an example of the one-ocean-box ESBMTK implementation. Define its geometry, initial total carbon, chemistry choices, and fictional starting state explicitly: almost all carbon starts in the atmosphere and only a small positive ocean DIC is retained if needed for numerical stability. The comparison targets are atmospheric xCO2 = 280 ppm and ocean DIC = 2040 umol/kg. This is a thought experiment, not a history of how seawater acquired its alkalinity.

The **first run defaults to TA = 0**. It represents CO2 invading water containing NaCl but lacking the real ocean's background alkalinity. Students should predict, run, and diagnose why gas exchange cannot reproduce both target values: gas exchange moves carbon but does not generate TA. They then use PyCO2SYS with the target DIC and atmospheric xCO2, under the shared conditions, to *infer* the required TA. A second ESBMTK run with that TA is a calibrated cross-implementation and conservation check, not an independent prediction of TA. Briefly distinguish the origin and maintenance of real-ocean TA from this closed-model inference; explicit weathering, carbonate dissolution, and burial are deferred to 03/04.

Compare at least two initial atmosphere-ocean carbon partitions at the same total carbon and TA. Their paths should differ, but their eventual equilibrium should agree. Change piston velocity to test whether it affects the relaxation time rather than the equilibrium state. Carbon and TA inventory audits, plus agreement between the specified and implemented chemistry/geometry, are the verification criteria. The approximation in section 2.4 of the ESBMTK paper can be noted as a numerical limitation, but it is not the principal learning question here.

For the 35-minute guided core, students explain cancellation of internal fluxes
and select the PyCO2SYS input pair. Model construction is a worked example;
partition/rate comparisons, plotting and all numerical audits are supplied.

## 02 - Verify a two-layer extension, then test an effective pump

**Learning goals:**

1. Add an ocean reservoir and conservative mixing, then verify that the no-pump model has the same equilibrium as 01.
2. Explain a maintained DIC gradient as a competition between downward export and mixing, without confusing calibration with prediction.
3. Implement and inventory-check a finite synthetic carbon forcing, then compare an analytical estimate with the model result.

### A. Structural and coding check

Prepare surface-layer depth **before** running the model in `teaching_config.py`, using the prescribed reference pumped ocean/atmosphere inventory ratio $R=62.4$, the reference atmospheric xCO2 and surface/deep DIC, ESBMTK density, and the independently specified whole-ocean area/depth and atmospheric size. This is **ratio-derived teaching geometry**, not an observed mixed-layer depth. Solve

$$\rho A[hDIC_s^*+(H-h)DIC_d^*]=R C_{atm,280}$$

for the surface depth $h$, giving

$$h=\frac{\rho AH DIC_d^*-R C_{atm,280}}{\rho A(DIC_d^*-DIC_s^*)}.$$

Use mol/kg for DIC and reject parameter choices that put $h$ outside $(0,H)$. With the default inputs the depth is about 298.75 m. The surface and deep volumes must sum to the 01 ocean volume. Do not use the rounded baseline ratio 57 to prepare geometry or tune the split against simulated output. Use the same total carbon, TA, T, S, P, chemistry settings, and atmospheric reservoir as the successful buffered 01 configuration. Surface and deep boxes can initially have the same TA, T, S, and P to isolate the new transport mechanism; explicitly say that the real ocean has TA and thermal gradients.

Students add the deep box and equal upward/downward water transports themselves. Mixing carries DIC and TA; only the surface box exchanges CO2 with the atmosphere. With no pump, symmetric mixing cannot maintain a DIC gradient. At equilibrium the two ocean DIC concentrations, atmospheric xCO2, and carbon inventory should match 01 within numerical tolerance. The transient may differ because the deep box is reached through mixing. Check water-volume consistency, total carbon conservation, and TA conservation before interpreting a pump run.

Use templates with native constructors visible: students select deep-box fields,
directed mixing names/species and pump endpoints/scale. Provide dictionary syntax,
unit conversion, restart handling, plotting and audits. Preserve 20/20/15 minutes
for structural extension, pump balance, and synthetic forcing respectively.

### B. Effective downward pump and an honest calibration

Add one aggregate, DIC-only downward export/remineralization closure. It is not yet a separate solubility, soft-tissue, or carbonate-pump decomposition. Let DIC be measured in mol/kg, Q in m3/time, and rho in kg/m3. At time t,

\[
J_{\rm mix}(t)=Q\rho\,[DIC_d(t)-DIC_s(t)],\qquad
J_{\rm pump}(t)=kDIC_s(t),
\]

where k has units of kg/time. These are *time-dependent* fluxes. Only at a stationary state with zero net deep-box accumulation does

\[
Q\rho(DIC_d^*-DIC_s^*)=kDIC_s^*,\qquad
k=Q\rho\left(\frac{DIC_d^*}{DIC_s^*}-1\right).
\]

For the current 02 exercise, supply the first-order assumption and the time-dependent box equations, then ask students to derive the stationary balance, solve for the expression for k, identify its units, and evaluate it numerically. Keep the displayed stationary derivation and its code inside maskable solution blocks. The numerical k helper must not supply the answer in the student path.

There are two scientifically valid teaching routes; the current notebook uses **calibration-first**:

- **Prediction-first:** obtain a reference export flux independently of the deep-DIC target, set `k = P_ref / DIC_s,ref`, choose Q separately, and compare the *predicted* stationary gradient with the observed gradient.
- **Calibration-first:** use observed stationary surface/deep DIC and an independently selected Q to *infer* k. The observed gradient is then an input used to fit the closure and must not be called a prediction or validation. Report the implied pump flux and assess it against an independent export estimate if available. The gradient constrains k/(Q rho), not k and Q separately.

The calibration-first route is acceptable for this introductory exercise. At fixed total carbon and TA, compare pump-on with an otherwise identical pump-off control. The atmospheric xCO2, surface DIC, carbon transfer, and adjustment timescale are conditional model results; atmospheric xCO2 is not specified by the steady deep-box flux equation alone. Nonetheless, if 01 used observed xCO2 and surface DIC to infer TA and total carbon, do not advertise the resulting atmosphere as an independent observational validation. The closure `k DIC_s(t)` is deliberately effective: real biological export need not scale with the entire DIC pool.

### C. Synthetic carbon-addition and analytical check

After the matched pump-on/pump-off experiment, add a finite, known amount of carbon to the atmosphere of the pump-on model. Students complete the supplied signal example with their calculated carbon inventory, inspect its integrated flux, check the combined carbon budget, and follow the system to equilibrium. This introduces the forcing mechanics needed later in 04 without making 02 an OA/OAE or sediment-response exercise.

For the current exercise, give students the pumped ocean/atmosphere inventory ratio **62.4**, the reference atmospheric xCO2 and atmospheric mole inventory, and the existing mass-based combined carbon inventory $C_0$. Ask them to derive the carbon addition themselves, including its expression and numerical value, before inserting it into supplied forcing code. The instructor solution is

$$C_{atm,280}=N_{atm}(280\times10^{-6}),\qquad
\Delta C=(1+62.4)C_{atm,280}-C_0.$$

Equivalently, use the *calculated* baseline ocean/atmosphere inventory ratio

$$R_0=\frac{C_0-C_{atm,280}}{C_{atm,280}},\qquad
\Delta C=(62.4-R_0)C_{atm,280}.$$

With the defaults, $R_0\simeq56.9998256$ and the addition is about 267.6326 Pmol C. The rounded lecture value 57 may be mentioned as an approximation, but must not replace the actual inventory in the geometry or forcing calculation. These are ocean/atmosphere inventory ratios, not seawater equilibrium capacity F (about 7.3 near the preindustrial state).

Because the supplied geometry enforces the reference 62.4 ratio, the same addition must agree with the finite-box expression

$$\Delta C=m_d(DIC_d^*-DIC_s^*).$$

Mask both derivations and their calculation code in the student copy. Keep the native Signal/source/connection example and its inventory audits supplied; the student inserts `extra_carbon_mol` as the signal's mass. Check the sampled and piecewise-linear forcing integrals, the time-resolved combined carbon budget, TA conservation, and a matching unforced restart.

The student evaluates the ratio-based addition in code and explains the equivalent
finite-box inventory on paper. Its numerical cross-check is instructor-only, so
it does not add another required coding block.

The fitted DIC ratio, inferred TA and ratio-derived geometry intentionally make the reference state consistent. Injecting the calculated extra carbon and returning to 280 ppm verifies forcing implementation, conservation and analytical-versus-dynamic consistency. It is **not independent evidence for the pump hypothesis**. A mismatch should prompt a check of units, input inventory, chemistry and equilibration before changing any model inputs. Never overwrite the mass-consistent initial inventory to obtain agreement.

## 03 - Construct and reproduce the Boudreau-like three-box model

**Learning goal:** Translate the benchmark diagram and parameters into a complete ESBMTK object graph and verify its preindustrial stationary behavior.

This is the model-construction exercise. Introduce its distinct low-/high-latitude surface boxes, circulation, explicitly represented POC and PIC fluxes, carbonate chemistry, weathering, dissolution, and burial. The benchmark's box-specific T, S, and P replace the simplifying uniform conditions of 01/02. The independent implementation and its conservation/stationarity checks matter more than forcing new scientific claims from the reproduced equilibrium.

The guided 55-minute core has four mapping tasks: reservoir concentration/geometry
fields, transport endpoints/species, POC/PIC choices and linked rates, and gas
exchange endpoints/species. Supply the Model container, loops, chemistry/sediment
wiring, weathering construction, flux-object retrieval and restart checks.
Students trace every diagram arrow even when its repeated code is supplied.
Qualitative sediment transfers and response times remain core; detailed horizon
equations and lookup-table mechanics move to `ref/sediment_reference.md`.

Use the shared Excel model-definition workbook (`data/Boudreau_2010/model_definition.xlsx`) to make geometry, box-specific water properties and initial DIC/TA comparable side by side. Keep atmospheric size and initial CO2 in a separate table with their own units. The workbook owns reservoir inputs, boundary nodes, directed transport and gas-exchange definitions, and baseline process/chemistry/feedback parameters. Python validates and translates them without duplicate baseline values. Parameter references keep shared rates in one place; PIC and weathering TA remain linked to their carbon inputs. Show one row-to-ESBMTK mapping, then let students generalize it and construct the connections. Display density and inventory quantities calculated with ESBMTK. Loading the spreadsheet must not replace the model-construction exercise. Preserve explicit benchmark area/volume through the adapter; do not expose area_percentage or replace geometry with global hypsometry. Show each transport row as an arrow and require water balance before constructing connections.

## 04 - Use the verified model for scientific experiments

**Core learning goal:** Use matched controls and clearly defined carbon/TA inputs
to explain the coupled carbon-cycle response. Process attribution and feedback
hypotheses are optional extensions outside the four-hour core.

Reuse the same verified workbook configuration in 04 and pass independent copies to matched cases. Keep forcing choices visible in core experiment cells and feedback controls visible in the extension. Clearly distinguish workbook initial concentrations from the archived stationary restart: the extension's tagged-attribution experiment uses the workbook initial state, while complete-model runs load the restart. Changes to geometry, thermodynamics, transport or baseline process rates require a new stationary restart before interpreting perturbations.

Reserve for 04 the decomposition/attribution of equilibrium DIC or storage to distinct processes, OA and OAE experiments, and state-dependent POC/PIC hypotheses. State which quantities are prescribed and which are outputs. Audit forcing inventories, matched forced-minus-control comparisons, carbon and TA budgets, and PIC's linked 1:2 DIC-TA stoichiometry. Avoid calling a fitted equilibrium, a tagged attribution, or a feedback law an independent causal observation.

The 40-minute core asks students to convert prescribed forcing inventories,
select OA/OAE species and endpoints, inspect supplied boundary-aware carbon/TA
audits, and interpret atmospheric CO2, surface pH, deep DIC and dissolution/burial
anomalies. Core 04 also owns the former Part II response-chain explanations and
full eight-panel OA/OAE figures, including the OA benchmark overlay. Supply plot
implementation and a guided route through forcing, atmosphere/surface, deep ocean
and sediment panels. Distinguish chemical horizons from sediment snowline memory
and absolute benchmark reproduction from matched anomalies. Retain two coding
tasks, four short answers and the same three runs; selected-panel reading shares
the 15-minute interpretation allocation, with no extra panel-by-panel report.
The archived signal has a small pre-1800 tail: show both the post-1800
benchmark integral and the whole-run input used in conservation checks. Keep
only Part I's tagged storage and Part III's feedback teaching in the self-contained
`notebooks/instructor/extensions/04_attribution_and_feedbacks.ipynb` (and generated
student copy). Supplied fixed-case prerequisites let the feedback section run in
a fresh kernel, but do not duplicate the core response exercise or figures.
The core does not run that extension. Do not move its scientific
questions into 02 to save time.

## Overall evaluation and boundaries

The revised 01/02 sequence has a clear progression: **failed model prediction and missing-variable diagnosis (01) -> structural verification -> pump-versus-mixing mechanism -> synthetic forcing check (02)**. It adds dynamic conservation, flux balance, parameter identifiability, and time-to-equilibrium reasoning beyond the lecture's static inventory arithmetic. Its most important boundary is that a calibrated DIC gradient and a carbon addition calculated to restore 280 ppm cannot both be counted as independent validations.

The unchanged 00 chemistry notebook supports a separate question set; keep its
static perturbations distinct from 04's coupled OA/OAE experiments. Notebook 03
repeats diagram-to-code mapping at greater complexity through scaffolded
construction and benchmark agreement. Notebook 04 requires matched OA/OAE
analysis; tagged attribution and feedbacks require a separate optional session.

Implementation status is tracked in `WORKPLAN.md`. The revised instructor sources for 01/02 implement the TA-free diagnosis, matched conservative extension, student-derived first-order pump calibration, ratio-derived layer geometry, and finite forcing check. Their student copies are generated through the same masking workflow as 03/04; the original top-level paths link to both versions. Shared settings and ESBMTK-derived masses replace the earlier inconsistent chemistry, geometry and hard-coded inventory-ratio overwrite.

Keep stable repository conventions and scientific guardrails in `AGENTS.md`,
the current workload and learning-goal summary in `TEACHING_GOALS.md`, and one-off
edits, acceptance checks and implementation order in `WORKPLAN.md`. This file
records scientific teaching intent and the rationale behind those boundaries.
