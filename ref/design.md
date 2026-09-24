# Learning design and scientific scope

**Current scope (2026-09-24):** 04 extension-related teaching goals are temporarily
suspended until the user explicitly asks to turn them on again. Retain its files
and implementation for later use; exclude its settings and tasks from current
planning and 03 explanations. Core 04's matched OA/OAE work remains active.

The maintained summary of the implemented core, workload, student tasks and
optional material is [`TEACHING_GOALS.md`](../TEACHING_GOALS.md). Update that file
alongside future teaching changes. The 2026-09-16 guided revision targets four
hours including a provisional 20-minute slot for 00. Exercise 9's full question
set was supplied on 2026-09-17; its eight-part workload still needs a pilot. The pre-revision
01–04 sources and their dependencies are frozen under
`archive/2026-09-16_before_guided_revision/`.

These practicals introduce first-year master's students from varied backgrounds to ocean-carbon chemistry and progressively more complex box models. The intended progression is **chemistry (00) -> missing buffering and model verification (01) -> conservative model extension and an effective pump (02) -> construction of the Boudreau-like model (03) -> experiments with the complete model (04)**.

The implemented [textbook refinements](textbook_exercise_review.md) retain that
progression. In 01, a supplied reaction supports the chemical explanation for
TA conservation during CO2 invasion. In 02, students distinguish production,
export and remineralization behind the effective DIC arrow; 62.4 is explicitly
a reference stock ratio rather than incremental carbon uptake. Both masked
derivations and the calibrated-state interpretation are retained.

In 01, introduce the DIC–TA–pCO2 surface after TA inference and before the
existing forward-chemistry exercise. Supply an offline rotatable surface,
labelled top-view contours and a linked constant-TA cutting plane/2D curve.
Use the shared configuration, preserve linear pCO2 scales and start near the
reference seawater state. A separate optional full-range view includes TA = 0;
it must not flatten the initial seawater view. Explain that the pCO2 contours
correspond to the pCO2 panel of lecture slide 16's Deffeyes diagram, whereas
pH contours require a different surface. The tangent gives local absolute
sensitivity, not the full uptake or response time. Introduce the optional atm
overlay only after the conservation equation; omit unphysical negative-atm
states from that line. Keep the existing masked inference and forward call.
The 3–5-minute guide replaces part of the sensitivity explanation and feeds
the existing interpretation answer, with no new code task or integration.
Pilot its fit within 01's provisional 40 minutes. Use no external assets or
new Jupyter dependencies; the supplied HTML can be saved for offline use.

In 03, reuse the representation with a supplied DIC-horizontal/TA-vertical
pCO2 contour plot that uses the workbook
L_b DIC/TA, temperature, salinity, pressure and benchmark chemistry options.
It describes a local input reference before exchange/transport, not the later
stationary restart or the whole-model atmospheric response. Students use arrows
to interpret their paired POC/PIC/dissolution flux equations and reuse them in
the native export mapping. The DIC-only POC closure and nutrient caveat remain
explicit. Equal inventory transfers must use each box's water mass when converted
to concentrations. The additional interpretation targets 4–6 minutes within
reconstruction/export discussion by consolidating repeated answers; pilot the
55-minute allocation, allowing 60 minutes or optional contour interpretation if
needed. There is no automatic transfer of time from 00 or the session buffer.

In 04, the four answers focus on interpreting forcing/response timing,
carbon uptake and TA, critical-depth motion and sediment memory, and OA/OAE
asymmetry and limits. Fixed biological export remains an interpretive boundary;
the former biological-response experiment proposal is suspended with the 04
extension. No extra core integrations, prerequisites or sediment equations are added.

The lecture slides, DeVries review, and ESBMTK paper are in `ref/`. The lectures already show algebraically that a larger deep-ocean DIC inventory raises the ocean/atmosphere carbon inventory ratio. Notebook 02 must therefore ask how a gradient is *maintained* and what follows from a specified mechanism, rather than present that inventory identity as a new discovery.

Across the sequence, translate each diagram's boxes, state variables, arrows, system boundary, and units into ESBMTK objects and conservation equations. Explain enough for students to understand the supplied code, while marking portions that can be hidden in student copies. Keep teaching hypotheses, calibrations, predictions, and software-consistency checks explicitly distinct.

Use the common inputs-minus-outputs formulation in 01–03 before combining terms
into a signed net flux. In 01, show separate invasion/outgassing arrows and their
equal-and-opposite contributions to atmosphere and ocean inventories. In 02,
retain both mixing arrows in the surface/deep budgets and introduce net upward
mixing only as their difference. The effective pump is a single directed transfer,
an output from the surface and the same input to the deep box, with upward return
provided separately by mixing. In 03, retain these directional gas terms when
mapping the general budget to gas exchange. Native gas exchange evaluates both
terms in one connection; explaining that mapping avoids treating constructor
choice as a scientific distinction. Keep native code unchanged and preserve the
masked stationary pump derivation. These explanations replace the net-first
presentation within the provisional activities; assess their reading load in the pilot.

Introduce `Species2Species` first in 01, before the helper invocation: show a
supplied reading excerpt of the constructor in `connect_atmosphere`, explain
the individual state endpoints and `ctype`, and map helper names to notebook
objects. Keep the excerpt in Markdown so it cannot create a duplicate connection
during normal execution. In 02, explain route strings and how `ty` selects the
same law as `ctype`. Supply explained choices for prescribed, concentration-dependent
and gas-exchange laws; students select mixing and pump laws within the existing
masked blocks. Explain the source/sink names and identifying role of `@id`;
omit the internal call chain. Focus on endpoints, species, flux laws and units.

The student-facing [coding cheatsheet](modelling_cheatsheet.md) and its
[two-page handout](../output/pdf/modelling_cheatsheet.pdf) make this translation
explicit across 01–04. The unrelated sealed-tank tracer example links a diagram,
equal-and-opposite inventory tendencies and native constructors, with a known
analytical endpoint. It uses mol/L and explicitly distinguishes the ocean's
mol/kg and ESBMTK-density inventory conversion. The example's fixed selective
transfer is an artificial assumption, not a water-transport or gas-exchange law.

The reference's box-to-code diagram places short constructor/attribute labels
beside geometry, evolving tracer states, initial values, environmental conditions
and connections. `M.DIC`, `M.A.DIC` and `M.A.DIC.c` distinguish a species definition,
its state in a box and its concentration series. The model container is explicitly
distinct from the physical system boundary. The main DIC arrow is one illustrative
internal transfer, not a complete water-flow graph. A minor attached legend covers
carbonate calculations, explicit species coupling and external forcing without
providing the core exercises' derivations or process mappings.

Solid arrows represent material transfer and dashed arrows represent information
used in calculations. In 01's corresponding worked-example diagram, carbonate
chemistry provides `M.Ocean.CO2aq` to the gas-exchange law; that diagnostic is not
an extra carbon inventory or transfer. The exchanged species `M.CO2` is distinct
from the updated ocean state `M.Ocean.DIC`. The diagram replaces the existing
mapping table in the same diagram-check activity, with no additional submission
or run; its reading time remains part of the provisional allocation to pilot.

The reference teaches only the Python patterns and architecture needed to read
the practicals. **Choose and explain**, **Understand and run**, and **Supplied
implementation** code labels direct attention while keeping scientific choices
visible. Offer it as optional lookup support in 01 and thereafter; introduce
essential syntax beside its first use in the notebooks. Its standalone example
is optional. The practicals are ungraded, with explanations retained in the
notebooks and no separate submission. The reading load still needs a pilot.
The sheet must not reveal the pump calibration/carbon-addition derivations, solve
the mapping exercises, or move 03/04 science into 01/02. Syntax is reference
material; explanation of assumptions, balances and evidence is the learning goal.

A shared configuration should align PyCO2SYS and ESBMTK choices where the exercises are meant to be comparable: for example `opt_k_carbonic=10`, `opt_pH_scale=2`, and `opt_buffers_mode=1`, with T = 16 degC, S = 35, and P = 0 bar for 01/02. Use the box-specific benchmark conditions needed in 03/04; do not silently force the simplified 01/02 conditions onto the Boudreau-like model. For teaching, use ESBMTK's documented objects and connections where feasible. Calculate seawater density from the same T, S, and P with ESBMTK's built-in method rather than separate hard-coded density estimates, and audit inventories in consistent units.

## 00 - PyCO2SYS foundations

**Learning goal:** Use two carbonate-system inputs and fixed thermodynamic choices to calculate and interpret the remaining seawater carbonate variables.

At the user's explicit request, notebook 00 now supplies student/instructor answer
sheets for exercise 9 (a–h), increasing atmospheric CO2 and ocean acidification.
The student sheet supplies only setup, one unrelated TA/DIC usage example and
documentation links alongside questions and blank answers. The instructor source
contains reproducible calculations and full interpretations; the shared builder
removes them from the student copy. The original path is a launcher.

Use the exercise's 15 °C, salinity 35, TA 2100 µmol/kg baseline and unchanged
`config.chemistry`. Preserve type 9 dry-air xCO2 in ppm, explicitly distinguishing it
from pCO2 in µatm. Temperature and salinity comparisons fix TA and xCO2 while DIC
adjusts; do not imply the same sensitivity for a closed sample. Historical CO2
and the RCP8.5-labelled 935 ppm endpoint are exercise inputs. Include both 15 °C
and 18 °C future states and alkalinity inversions. Restored aragonite saturation
is a prescribed target; inferred TA is not evidence for intervention feasibility,
and small pH sensitivity is not evidence that warming has little ecological effect.
These static chemistry exercises remain distinct from the coupled OA/OAE
histories, attribution and feedbacks of 04. Pilot the eight-part workload before
treating the provisional 20-minute timetable reservation as sufficient.

## 01 - Diagnose missing alkalinity in a one-ocean-box model

**Learning goals:**

1. Map an atmosphere-ocean diagram to ESBMTK boxes, states, gas exchange, and a conserved carbon inventory.
2. Explain why CO2 invasion can increase DIC but cannot create TA; infer the missing background TA with PyCO2SYS.
3. Distinguish equilibrium controls from rate controls.

Supply an example of the one-ocean-box ESBMTK implementation. Define its geometry, initial total carbon, chemistry choices, and fictional starting state explicitly: almost all carbon starts in the atmosphere and only a small positive ocean DIC is retained if needed for numerical stability. The comparison targets are atmospheric xCO2 = 280 ppm and ocean DIC = 2040 umol/kg. This is a thought experiment, not a history of how seawater acquired its alkalinity.

Before the atmosphere-connection step, state the physical configuration in the
notebook: fixed atmospheric size of 1.77e20 mol air, evolving dry-air CO2 mole
fraction, and initial atmospheric carbon equal to total carbon minus initial
ocean carbon. Explain the resulting roughly 16240 ppm initial state and distinguish
the 280 ppm inventory reference from a fixed atmospheric boundary condition.
Give the exchange area and piston velocity, and identify the shared T/S/P as
seawater settings. This is supplied explanation within the existing diagram
activity; retain the provisional workload and pilot requirement.

In 01's directional gas law, write invasion explicitly as solubility times
atmospheric CO2 rather than introducing an equilibrium aqueous-CO2 label.
Explain that, at fixed exchange and solubility settings, invasion is independent
of ocean DIC/TA; outgassing uses the aqueous CO2 calculated from them. Relate the
paper's atmospheric notation to the code's dry-air mole fraction through the
supplied gas-convention and unit conversions. Retain equal-and-opposite transfers
and nonzero balanced directional rates at equilibrium. This replaces the existing
explanation without adding an exercise or changing model code.

The **first run defaults to TA = 0**. Introduce the initialization through an idealized picture: start with water containing only dissolved NaCl (TA = 0), then dissolve a trace of CO2 to supply the small initial DIC without changing TA. Say CO2 rather than simply "adding DIC", since bicarbonate/carbonate salt additions can also change TA. Place the remaining carbon in the atmosphere within the same target-derived total inventory; this is initialization, not an extra forcing. In the system-specification section, distinguish that motivating picture from the supplied seawater chemistry used in the calculation. Frame the opening as a new ESBMTK modeller's fictional verification experiment: the modeller expects correct code and a target-derived total carbon inventory to reproduce both familiar reference values. Present that expectation as a hypothesis for students to critique, not a promised outcome. Use the neutral student-facing title "Can gas exchange explain ocean carbon storage?" and defer the diagnosis until after prediction and the first run.

Students distinguish a constraint on the combined carbon inventory from controls on its equilibrium partition. After running, they use the carbon and TA audits to explain why disagreement alone does not demonstrate a coding error: passing budgets supports implementation verification but establishes neither complete code correctness nor physical adequacy. Gas exchange moves carbon but does not generate TA; small initial DIC does not require small TA. They then use PyCO2SYS with the target DIC and atmospheric xCO2, under the shared conditions, to *infer* the required TA. A second ESBMTK run with that TA is a calibrated cross-implementation and conservation check, not an independent prediction of TA. Briefly distinguish the origin and maintenance of real-ocean TA from this closed-model inference; explicit weathering, carbonate dissolution, and burial are deferred to 03/04. The revised before/after prompts replace the existing prediction/diagnosis task within the provisional 40-minute allocation.

Compare at least two initial atmosphere-ocean carbon partitions at the same total carbon and TA. Their paths should differ, but their eventual equilibrium should agree. Change piston velocity to test whether it affects the relaxation time rather than the equilibrium state. Carbon and TA inventory audits, plus agreement between the specified and implemented chemistry/geometry, are the verification criteria. The approximation in section 2.4 of the ESBMTK paper can be noted as a numerical limitation, but it is not the principal learning question here.

Use the explicit diagnostic label "equilibration time (1% criterion)" for the
first saved time after which atmospheric CO2 remains within 1% of its final
simulated value. This depends on the starting state and threshold, and is not
an exponential relaxation constant or independent evidence of stationarity.
Keep the numerical criterion unchanged when renaming the helper and output.

Name the two reference values at the opening and call the initial DIC a small
positive initial concentration rather than a numerical seed. Define gas transfer
velocity (piston velocity) as an exchange coefficient, not a water-parcel speed;
retain the density factor with mol/kg concentrations. Point directly to the
source of `connect_atmosphere` when introducing the constructor excerpt.

Keep element/species registration in `new_model`, with brief optional explanation:
registration supplies definitions, while DIC/TA are the prescribed ocean states.
Seawater initialization supplies background boron through PyCO2SYS and carbonate
system 1 initializes/updates auxiliary Hplus and CO2aq. Miscellaneous sediment
definitions are unused in 01; registering them creates no sediment processes.
This does not turn the motivating NaCl picture into the implemented chemistry.

Explain `assert` and `assert_allclose` once as supplied checks that stop a cell
when a condition fails; they do not impose a result. Retain construction, carbon
inventory, conservation and calibrated-endpoint checks; consolidate duplicate
TA auditing. Move the assertions enforcing a large mismatch and longer response
under lower piston velocity into an instructor-only verification cell so the
student interprets those results. Keep their automated regression coverage.
These wording and verification changes add no student task; pilot their reading
load within the existing provisional allocation.

Introduce `single_box` before its first use as the supplied helper that repeats
the visible construction and returns a fresh, unrun model. Explain that changing
initial ocean DIC adjusts atmospheric carbon to preserve the total inventory,
and that `run_model` runs the newly created experiment. Keep this a brief reading
aid within the existing rerun/comparison activity, not another coding task.

For the provisional 40-minute guided core, students explain cancellation of
internal fluxes and write the complete PyCO2SYS TA calculation, transferring
input-pair and result-extraction skills from 00. Mask the input-type assignments,
solver call and TA extraction together. Supply the targets, `config.pyco2` settings,
documentation and required `inferred_ta` output name; explicitly distinguish
01's 16 °C from 00's 15 °C. Place the supplied buffered-model rerun in a separate
cell after the TA inference and curve exercise. This is a fresh initial condition, not
an alkalinity input during the original run.

Break the supplied construction into short atmospheric, gas-law, object-mapping
and connection steps, with native code beside its explanation. Keep the individual
constructor before the helper call; remove `M.connection_summary()`. Retain units
and directional conservation, using `atm` and `ocn` subscripts; put implementation
conversion details in reference notes. Ask explicitly which chemical assumption
prevents the target partition and whether any model process can change it.
Supply real-ocean TA sources as context and keep explanations beside diagnosis,
TA inference and the path comparison; end with a stopping cue rather than a
repeated synthesis question. Model construction, partition/rate comparisons, plotting
and numerical audits remain supplied. The fuller calculation increases independent
student work; streamlined reading and questions are intended to accommodate it
within 10/20/10 minutes, including five extra minutes for the curve exercise
from the completion buffer. The four-hour session is preserved, but this
revised allocation still requires a pilot after 00.

Position PyCO2SYS explicitly: infer TA from reference DIC/xCO2, then evaluate
seawater pCO2 from DIC/TA across a supplied grid before the revised ESBMTK
run. Students complete the forward chemistry call and output extraction;
supply the loop, grid, conserved-inventory atmosphere line, dry-xCO2/pCO2
conversion and plots. Ask them to interpret slopes and intersections,
placing the zero-TA uptake explanation in a masked instructor answer.
Distinguish carbonate-equilibrium states from air–sea equilibrium at
intersections, and uptake amount from equilibration time. Compare absolute
sensitivity at matched DIC under the shared settings; use the full curves
and carbon inventory to establish the endpoint rather than assuming one
local derivative describes the whole trajectory. Keep the Revelle factor
as a brief link to slide 46's fractional response to prescribed atmospheric
CO2 and fixed-R linear approximation, with no extra calculation.

## 02 - Verify a two-layer extension, then test an effective pump

**Learning goals:**

1. Add an ocean reservoir and conservative mixing, then verify that the no-pump model has the same equilibrium as 01.
2. Explain a maintained DIC gradient as a competition between downward export and mixing, without confusing calibration with prediction.
3. Implement and inventory-check a finite synthetic carbon forcing, then compare an analytical estimate with the model result.

### A. Structural and coding check

Prepare surface-layer depth **before** running the model in `teaching_config.py`, using the prescribed reference pumped ocean/atmosphere inventory ratio $r_{\mathrm{ocn/atm}}=62.4$, the reference atmospheric xCO2 and surface/deep DIC, ESBMTK density, and the independently specified whole-ocean area/depth and atmospheric size. This is **ratio-derived teaching geometry**, not an observed mixed-layer depth. Solve

$$\rho A[hDIC_s^*+(H-h)DIC_d^*]=r_{\mathrm{ocn/atm}} C_{atm,280}$$

for the surface depth $h$, giving

$$h=\frac{\rho AH DIC_d^*-r_{\mathrm{ocn/atm}} C_{atm,280}}{\rho A(DIC_d^*-DIC_s^*)}.$$

Use mol/kg for DIC and reject parameter choices that put $h$ outside $(0,H)$. With the default inputs the depth is about 298.75 m. The surface and deep volumes must sum to the 01 ocean volume. Do not use the rounded baseline ratio 57 to prepare geometry or tune the split against simulated output. Use the same total carbon, TA, T, S, P, chemistry settings, and atmospheric reservoir as the successful buffered 01 configuration. Surface and deep boxes can initially have the same TA, T, S, and P to isolate the new transport mechanism; explicitly say that the real ocean has TA and thermal gradients.

Students add the deep box and equal upward/downward water transports themselves. Mixing carries DIC and TA; only the surface box exchanges CO2 with the atmosphere. With no pump, symmetric mixing cannot maintain a DIC gradient. At equilibrium the two ocean DIC concentrations, atmospheric xCO2, and carbon inventory should match 01 within numerical tolerance. The transient may differ because the deep box is reached through mixing. Check water-volume consistency, total carbon conservation, and TA conservation before interpreting a pump run.

Use templates with native constructors visible: students select deep-box fields,
directed mixing names/species/law and pump endpoints/law/scale. Provide dictionary syntax,
unit conversion, restart handling, plotting and audits. Preserve 20/20/15 minutes
for structural extension, pump balance, and synthetic forcing respectively.
Explain `config` attributes, dictionary pairs/unpacking and route-string IDs
locally. Uniform initial TA and the absence of TA-changing processes make the
net TA redistribution zero while retaining carbonate buffering. Ask A4 about
equilibrium equivalence; the supplied checks do not plot the one-box/two-layer
transient. These revisions require a fresh reading-load pilot within the same
provisional allocation, not a claim of verified student completion time.

### B. Effective downward pump and an honest calibration

Add one aggregate, DIC-only downward export/remineralization closure. It is not yet a separate solubility, soft-tissue, or carbonate-pump decomposition. Let DIC be measured in mol/kg, Q in m3/time, and rho in kg/m3. Start with the two directed mixing fluxes

$$J_{mix,down}(t)=Q\rho DIC_s(t),\qquad J_{mix,up}(t)=Q\rho DIC_d(t).$$

Write deep accumulation as downward mixing plus pump input minus upward mixing
output. Only then introduce net upward mixing as their difference. At time t,

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
- **Calibration-first:** use observed stationary surface/deep DIC and an independently selected Q to *infer* k. The observed gradient is then an input used to fit the closure and must not be called a prediction or validation. The gradient constrains k/(Q rho), not k and Q separately; retain this as an instructor note rather than an additional student question. Quantitative comparison with observed export is outside the core route.

The calibration-first route is acceptable for this introductory exercise. At fixed total carbon and TA, compare pump-on with an otherwise identical pump-off control. The atmospheric xCO2, surface DIC, carbon transfer, and adjustment timescale are conditional model results; atmospheric xCO2 is not specified by the steady deep-box flux equation alone. Nonetheless, if 01 used observed xCO2 and surface DIC to infer TA and total carbon, do not advertise the resulting atmosphere as an independent observational validation. The closure `k DIC_s(t)` is deliberately effective: real biological export need not scale with the entire DIC pool.

Keep Part B centred on the deep-box balance, the derivation of k and the existing
atmospheric-CO2/pump–mixing figure. Put the full conservation equations in a
collapsible reference. Remove the reference-versus-simulated export comparison,
intermediate DIC/export printouts and deep-transfer diagnostic from the notebook;
retain all conservation, fitted-ratio and stationary-flux checks with a compact
success summary. B4 asks only which real-ocean pump the DIC-only transfer most
closely resembles and what is omitted. Its short masked answer relates it to the
soft-tissue pump without claiming to isolate a measured contribution.

Background for instructors, outside the core route: published global organic
carbon export estimates span roughly 5–12 Pg C/yr across different methods and
pathway definitions ([Nowicki et al., 2022](https://doi.org/10.1029/2021GB007083)).
Comparisons require matching export depth, pathways and reference period, as
well as acknowledging the prescribed transport and unresolved recycling. This
is not an additional task in 02.

### C. Synthetic carbon-addition and analytical check

Bridge from B by explaining that fitting the DIC ratio fixes relative concentrations,
while reaching the full reference state also requires the corresponding total
carbon inventory. The pump redistributes the original inventory; the external
input changes it. Students calculate that addition, insert it into the supplied
signal example, and read compact input/budget/endpoint checks alongside the
existing forcing figure. This introduces the forcing mechanics needed later in
04 without making 02 an OA/OAE or sediment-response exercise.

For the current exercise, give students the pumped ocean/atmosphere inventory ratio **62.4**, the reference atmospheric xCO2 and atmospheric mole inventory, and the existing mass-based combined carbon inventory $C_0$. Ask them to derive the carbon addition themselves, including its expression and numerical value, before inserting it into supplied forcing code. The instructor solution is

$$C_{atm,280}=N_{atm}(280\times10^{-6}),\qquad
\Delta C=(1+62.4)C_{atm,280}-C_0.$$

Equivalently, use the *calculated* baseline ocean/atmosphere inventory ratio

$$r_{\mathrm{ocn/atm},0}=\frac{C_0-C_{atm,280}}{C_{atm,280}},\qquad
\Delta C=(62.4-r_{\mathrm{ocn/atm},0})C_{atm,280}.$$

With the defaults, $r_{\mathrm{ocn/atm},0}\simeq56.9998256$ and the addition is about 267.6326 Pmol C. The rounded lecture value 57 may be mentioned as an approximation, but must not replace the actual inventory in the geometry or forcing calculation. These are ocean/atmosphere inventory ratios, not seawater equilibrium capacity F (about 7.3 near the preindustrial state).

Because the supplied geometry enforces the reference 62.4 ratio, the same addition must agree with the finite-box expression

$$\Delta C=m_d(DIC_d^*-DIC_s^*).$$

Mask both derivations and their calculation code in the student copy. Keep the native Signal/source/connection example and its inventory audits supplied; the student inserts `extra_carbon_mol` as the signal's mass. Check the sampled and piecewise-linear forcing integrals, the time-resolved combined carbon budget, TA conservation, and a matching unforced restart.

The student evaluates the ratio-based addition in code and explains the equivalent
finite-box inventory on paper. Its numerical cross-check is instructor-only, so
it does not add another required coding block.

The fitted DIC ratio, inferred TA and ratio-derived geometry intentionally make the reference state consistent. Injecting the calculated extra carbon and returning to 280 ppm verifies forcing implementation, conservation and analytical-versus-dynamic consistency. It is **not independent evidence for the pump hypothesis**. A mismatch should prompt a check of units, input inventory, chemistry and equilibration before changing any model inputs. Never overwrite the mass-consistent initial inventory to obtain agreement.

Use $r_{\mathrm{ocn/atm}}$ for the whole-reservoir ocean/atmosphere inventory ratio, separately from
the lecture's seawater equilibrium capacity F; reserve R for the Revelle factor and place the uniform-01 relation
in collapsible optional reference material before the carbon-addition exercise.
Pulse duration is
a supplied choice. Explain that changing duration at fixed mass changes the path,
while the eventual equilibrium is unchanged if sufficient relaxation time is
allowed. Numerical resolution and the forcing-integral check remain necessary.
For optional duration changes, supply a clock helper that resolves the pulse
and aligns its start/end with the native signal grid before constructing both
models. ESBMTK 0.14 requires whole-year start/duration values in these models;
reject unsupported fractional years and pulses touching the run boundaries.
Keep this numerical machinery outside the student derivations and retain the
user's selected 100-year example. It adds no required exercise.
Keep duration experimentation and interpolation details in a collapsible optional
note, with local clock syntax and the rerun instruction visible. Consolidate repeated
calibration explanations into B3/B4 and C3, and use an ungraded stopping cue.

## 03 - Construct and reproduce the Boudreau-like three-box model

**Learning goal:** Translate the benchmark diagram and parameters into a complete ESBMTK object graph and verify its preindustrial stationary behavior.

This is the model-construction exercise. Introduce its distinct low-/high-latitude surface boxes, circulation, explicitly represented POC and PIC fluxes, carbonate chemistry, weathering, dissolution, and burial. The benchmark's box-specific T, S, and P replace the simplifying uniform conditions of 01/02. The independent implementation and its conservation/stationarity checks matter more than forcing new scientific claims from the reproduced equilibrium.

The guided 55-minute core now begins with **Exercise 03.1: write paired DIC/TA
flux equations and label the diagram**, using box outlines, corrected ESBMTK
source material, selected reservoir/baseline Excel inputs and short row hints.
Use one amount-flux law for each process family, including zero TA effects;
students identify the changing inputs to each rate, prescribed constant rates,
and the two fluxes whose difference gives signed net burial.
Supply chemistry and dissolution dependency functions, then ask for the paired
stoichiometry and the export/dissolution relation. Q, physical rho Q and box mass
are distinct quantities. Use Q for water volume transport throughout, with
J_ij^X(t) = rho_i Q_ij X_i(t) for the physical tracer flux. Keep diagrams focused
on boxes and process arrows, with equations in the companion table.
A supplied J/m rule connects flux to concentration
tendency. Preserve the historical transport caveat. The contour question follows
the flux equations and interprets the same POC/PIC/dissolution stoichiometry.
Supply the F3/F5, inverted rain-ratio and inorganic-weathering corrections rather
than asking students to guess between inconsistent sources. Show dissolution
explicitly, separate material from information arrows, and identify the sediment
process module without inventing a sediment-carbon reservoir. Signed net burial
equals export minus dissolution and is not an additional implemented drain.
State the model assumptions beside the rows; expand biological TA effects in
reference notes and explain each native flux law directly at the B2 mapping. Keep the
weathering caveat concise: real riverine input need not have exactly the model's
1 DIC : 2 TA ratio. Detailed nutrient/sediment equations stay optional.

Present 03.1 in three steps: paired fluxes, diagram labelling, and one internal
inventory cancellation. Put notation and hints beside the relevant task and
define the physical snowline on first use. Consolidate gas-law explanation in
reconstruction; construction then explains the native mapping. Keep the full
transport-unit caveat at the code mapping, with a short advance notice in 03.1.
Make duplicate workbook cross-references and numerical audit details expandable,
while retaining visible input rows, physical drift limits and all core questions.
These are presentation changes within the existing provisional allocation;
pilot/fallback guidance stays in the teaching plan rather than student instructions.

Define a restart as a new run initialized from saved model values before first
using the term. Explain `scale_with_concentration` directly as coefficient times
current source concentration. Do not introduce or compare a broader
state-dependence category; the concrete flux laws are sufficient for this task.
For C2, define the atm plus dissolved-ocn inventory boundary and reuse W_0 and
the signed net burial already defined in A3. Ask for internal cancellation and
the two boundary balances; omit a repeated burial derivation and the hypothetical
additional-sink question. Budget closure does not
require constant inventories; constant inventories additionally require balanced
boundary inputs and outputs. Keep all these derivations inside solution markers.

After the attempt, students reconcile their diagram with the named connection
tables, then use that same specification in four mapping tasks: reservoir concentration/geometry
fields, transport endpoints/species, POC/PIC choices and linked rates, and gas
exchange endpoints/species. Supply the Model container, loops, chemistry/sediment
wiring, weathering construction, flux-object retrieval and restart checks.
Students choose the water and export laws as well as their endpoints/species.
Their paired diagrams/flux worksheets are generated from shared teaching metadata
and current input references, with selected student fields blank and no hidden
answer formulas. These teaching records are not an executable process-input
schema: specialized POC/PIC/weathering and sediment topology still resides in
Python. Numerical input ownership remains unchanged.
Students trace every diagram arrow even when its repeated code is supplied.
Qualitative sediment transfers and response times remain core; detailed horizon
equations and lookup-table mechanics move to `ref/sediment_reference.md`.

Use the shared Excel model-definition workbook (`data/Boudreau_2010/model_definition.xlsx`) to make geometry, box-specific water properties and initial DIC/TA comparable side by side. Keep atmospheric size and initial CO2 in a separate table with their own units. The workbook owns reservoir inputs, boundary nodes, directed transport and gas-exchange definitions, and baseline process/chemistry/feedback parameters. Python validates and translates them without duplicate baseline values. Parameter references keep shared rates in one place; PIC and weathering TA remain linked to their carbon inputs. Show one row-to-ESBMTK mapping, then let students generalize it and construct the connections. Display density and inventory quantities calculated with ESBMTK. Loading the spreadsheet must not replace the model-construction exercise. Preserve explicit benchmark area/volume through the adapter; do not expose area_percentage or replace geometry with global hypsometry. Show each transport row as an arrow and require water balance before constructing connections.

The partial reservoir example supplies T/S/P syntax rather than the complete
scientific answer. Explain the retained historical transport-unit convention
against 02's explicit Q rho rule. The revised allocation is 15 minutes for
reconstruction/reconciliation, 20 for four mappings, 15 for the consolidated
boundary budget and checks, and 5 for explanation. Remove duplicate boundary
prompts, graph summaries and closing synthesis. Pilot this target; a longer
reconstruction requires more time or an explicit further reduction.

Supply three complementary checks: exact connection graph, time-resolved
boundary-aware C/TA conservation, and absolute drift over a 20-year restart
for six ocean DIC/TA states, atm CO2 and snowline. Inspect all saved times, not
just endpoints. State tolerances in physical units; passing establishes local
restart consistency, not stability, uniqueness or scientific validation.

## 04 - Use the verified model for scientific experiments

**Core learning goal:** Use matched controls and clearly defined carbon/TA inputs
to explain the coupled carbon-cycle response. Extension teaching is suspended
under the current scope instruction above.

Reuse the same verified workbook configuration in 04 and pass independent copies to matched cases. Keep forcing choices visible in core experiment cells. Clearly distinguish workbook initial concentrations from the saved nearly stationary state used for complete-model runs. Changes to geometry, thermodynamics, transport or baseline process rates require new compatible saved starting values before interpreting perturbations.

Reserve the matched OA and OAE experiments for core 04. State which quantities are prescribed and which are outputs. Audit forcing inventories, matched forced-minus-control comparisons, carbon and TA budgets, and PIC's linked 1:2 DIC-TA stoichiometry. Avoid calling a fitted equilibrium an independent causal observation.

The 40-minute core starts with predictions and an experiment specification on
the completed 03 diagram. Students convert forcing inventories and select species
and endpoints; all three integrations, plotting and numerical audits are supplied.
Display the exact solver input rates in B1, before matched responses in B2:
separate carbon and TA units, with a normalized overlay for timing only. Retain
the small pre-1800 tail and both interval/whole-run inventory checks. Reuse 03's
active atm plus dissolved-ocn boundary and W_0 budget notation.

Use full eight-panel figures after the anomalies to interpret pathways, critical
depths and dissolution/burial, then the OA reproduction overlay. Define saturation
horizon, compensation depth and snowline separately using the original 2010 papers.
Explain the negative-elevation plotting convention and 200 m saturation bound.
Supply the snowline rules in B3 before asking for interpretation: CCD shoaling
leaves old sediment that must dissolve before the snowline retreats; CCD deepening
allows the preservation boundary to follow effectively instantly at the plotted
timescale, without resolving buildup of a thick sediment layer. Numerical tracking
may leave a small lag. No student lookup or derivation of the raw sediment code is
required. This response is relative to the changing CCD, not to the external input;
transport/chemistry delays remain, and later shoaling in OAE can leave a lag too.
The existing depth/memory answer asks students to apply these rules to plotted
depths and burial, not infer an unspecified closure. No task or time is added.
Read depth separation alongside dissolution/net burial rather than assuming
all three horizons move together or mirror one another in OA/OAE.

Retain two coding tasks and four short answers, now on forcing/response timing,
carbon uptake/TA, critical depths/memory and asymmetry/limits. Consolidate repeated
design prompts and remove the biological-response experiment proposal. Students
cite selected curves and approximate times within the existing provisional
15-minute interpretation allocation; no panel-by-panel report or new run is needed.
Unequal species, amounts and entry boxes must be distinguished from nonlinear
chemical and sediment mechanisms; these runs do not establish intervention
efficiency, cancellation, stronger biological export or final equilibrium.
Keep the 04 attribution/feedback extension and its implementation dormant until
explicitly re-enabled, with no settings or teaching tasks in the core route.
Pilot the revised reading and interpretation workload within the provisional 40 minutes.

The separate optional `extensions/05_independent_model.ipynb` gives a 60–90-minute
starter for independent modelling (pilot required). It supplies execution and
plotting around student-selected scientific choices. The instructor example
compares fixed and first-order export with equal initial fluxes in the 02 model;
same-state matched transients are explicitly distinguished from stationary
perturbation experiments. Keep it outside the four-hour core. It complements
the core sequence; it does not reactivate the dormant 04 extension.

## Overall evaluation and boundaries

The revised 01/02 sequence has a clear progression: **failed model prediction and missing-variable diagnosis (01) -> structural verification -> pump-versus-mixing mechanism -> synthetic forcing check (02)**. It adds dynamic conservation, flux balance, parameter identifiability, and time-to-equilibrium reasoning beyond the lecture's static inventory arithmetic. Its most important boundary is that a calibrated DIC gradient and a carbon addition calculated to restore 280 ppm cannot both be counted as independent validations.

The 00 chemistry answer sheets support the supplied exercise 9; keep their
static perturbations distinct from 04's coupled OA/OAE experiments. Notebook 03
repeats diagram-to-code mapping at greater complexity through scaffolded
construction and benchmark agreement. Notebook 04 requires matched OA/OAE
analysis; attribution/feedback extension teaching is currently suspended.

Implementation status is tracked in `WORKPLAN.md`. The revised instructor sources for 01/02 implement the TA-free diagnosis, matched conservative extension, student-derived first-order pump calibration, ratio-derived layer geometry, and finite forcing check. Their student copies are generated through the same masking workflow as 03/04; the original top-level paths link to both versions. Shared settings and ESBMTK-derived masses replace the earlier inconsistent chemistry, geometry and hard-coded inventory-ratio overwrite.

Keep stable repository conventions and scientific guardrails in `AGENTS.md`,
the current workload and learning-goal summary in `TEACHING_GOALS.md`, and one-off
edits, acceptance checks and implementation order in `WORKPLAN.md`. This file
records scientific teaching intent and the rationale behind those boundaries.
