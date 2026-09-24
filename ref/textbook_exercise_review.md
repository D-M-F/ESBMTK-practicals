# Textbook review of exercises 01–04

2026-09-23. **Core recommendations implemented in instructor/student 01–04.**
The sections below preserve the rationale and proposed workload tradeoffs.
The lower-priority alternative question and optional follow-ups remain proposals.
No model parameters, core integrations or prerequisites were added; 03's revised
55-minute allocation remains subject to a student pilot. Verification is recorded
in `../WORKPLAN.md`.

This review compares the current instructor sources, including the uncommitted
01–04 revisions, with the local textbooks. It also uses `TEACHING_GOALS.md`,
`ref/design.md`, the current `WORKPLAN.md`, the earlier exercise-revision proposal,
and the relevant 2026 lecture material. The recently implemented reconstruction,
matched-control and independent-model exercises are treated as existing work.
Notebook 00 and the dated archive are outside the proposed changes.

**Recommendation: retain the progression and make a few replacements, with the
largest benefit in 03/04.** The books support the current emphasis on hypotheses,
balances, model construction and interpretation. They suggest making students
explain more directly how a process changes DIC and TA, and how a maintained
background carbon distribution differs from a response to new forcing. They do
not justify adding another long set of calculations to this four-hour practical.

## Reading and exercise crosswalk

SG = Sarmiento and Gruber (2006), *Ocean Biogeochemical Dynamics*;
M = Middelburg (2019), *Marine Carbon Biogeochemistry*.
Page references below are **printed pages**; PDF positions are provided separately
where useful. Relevant sections and problem sets were read selectively, rather
than treating the entirety of these books as required course reading.

| Topic and notebook | Relevant textbook material | Exercise connection and assessment |
| --- | --- | --- |
| Hypothesis, conservation and two-box reasoning; 01/02 | SG §1.2, pp. 10–14; §2.1, especially the box-model discussion on p. 22 | Problems 1.5–1.7, 1.10–1.12 (pp. 16–18) connect balances, exchange, endpoints and response times. The current no-pump comparison and masked stationary derivation already teach these skills. |
| Gas exchange and carbonate chemistry; 01 | SG §§3.2–3.4; §8.2 and the physical-process discussion in §8.3, pp. 322–331. M §§5.1–5.4, pp. 77–88 | SG 3.3 distinguishes dry mole fraction from partial pressure; 3.7 concerns gas relaxation; 8.1–8.4 and 8.10–8.11 concern chemistry and CO2 equilibration. Current 01 already contains the key distinctions, with a different atmospheric boundary from 8.11. |
| Effective versus biological export; 02/03 | SG §1.2, pp. 10–14, §§8.4–8.5, pp. 342–354; M §§3.1–3.3, especially pp. 38–44, and §6.1, pp. 107–109 | SG 8.18–8.19 distinguish biological-pump efficiency, processes and observed gradients. M distinguishes production, export and remineralization depth. These support making the effective-arrow interpretation concrete, not reinstating a quantitative attribution exercise in 02. |
| Process effects on DIC/TA; 03/04 | SG §8.3, pp. 331–334, Fig. 8.3.5; M §§5.6–5.7, pp. 90–96, Figs. 5.5–5.6 and Table 5.3 | SG 8.4 and 8.7 (p. 355) are the best direct models for a short process-vector question; 8.14 (pp. 357–358) provides a longer optional sequential chemistry calculation. |
| Carbonate sediments and adjustment; 03/04 | SG §§9.4–9.5, especially pp. 374–375 and 384–388; M Box 5.2, pp. 101–103 | SG 9.1, 9.13 and 9.16–9.18 distinguish horizons, boundaries, adjustment and remineralization depth. Current notebooks already include dissolution, signed net burial and snowline memory. Refine interpretation rather than add sediment equations. |
| Carbon perturbations, capacity and rate; 04 | SG §10.2, especially pp. 400–405 and 414–415; M Box 5.1, pp. 97–101 | SG 8.13, 10.3, 10.5 and 10.9 distinguish inventory from incremental uptake, changing buffering, several adjustment processes and fixed versus changing biology. These motivate the proposed 04 questions and optional extensions. |

Middelburg's supplied primer has **no numbered end-of-chapter exercise sets**.
Its worked derivations, figures and explanatory boxes provide material for new
questions; these should not be cited as existing numbered exercises.

Useful local PDF positions:

- [SG problems 8.1–8.8](<Sarmiento and Gruber - 2006 - Ocean biogeochemical dynamics.pdf#page=378>): printed p. 355; problems 8.10–8.11 on PDF p. 379; 8.13–8.14 on PDF pp. 380–381.
- SG Fig. 8.3.5: printed p. 333 / PDF p. 356. Problems 9.16–9.18: printed p. 391 / PDF p. 414. Problems 10.3–10.5 and 10.9: printed pp. 454–455 / PDF pp. 477–478.
- [M process-vector figures](<Middelburg - 2019 - Marine Carbon Biogeochemistry A Primer for Earth System Scientists.pdf#page=101>): printed pp. 92–93 / PDF pp. 101–102. Table 5.3: printed p. 95 / PDF p. 104. Box 5.2: printed pp. 101–103 / PDF pp. 110–112.

PDF offsets are not constant throughout either file; use these verified positions.

## 01: retain the exercise, strengthen one chemical explanation

**Already strong:** the failed TA-free hypothesis, conserved finite carbon stock,
inverse TA calculation, forward pCO2–DIC curves, and separate initial-partition
and piston-velocity comparisons. This is more useful than replacing the notebook
with a carbonate-equilibrium worksheet. Its distinction between a fitted endpoint
and an independent prediction should remain.

**Small proposed replacement in the post-run diagnosis:** instead of only asking
whether a represented process can change TA, ask students to justify the answer:

> CO2 enters the water and its pH changes. Why does this not create or consume
> total alkalinity? Explain using the paired production of bicarbonate and H+.
> Which initial chemical assumption therefore persists during the run?

Supply the reaction `CO2* + H2O ⇌ H+ + HCO3−` beside the question, explaining
that CO2* denotes the dissolved CO2/carbonic-acid pool. The positive bicarbonate
and negative proton contributions cancel in TA; subsequent acid–base
repartitioning also conserves TA. This does not require students to derive the
full seawater alkalinity expression. It makes the chemical reason for the existing
TA audit explicit. Basis: SG §8.2 and problem 8.4(c); M §§5.3 and 5.7.

Keep the pCO2–DIC curves and the short Revelle connection. Do not add a mandatory
Revelle-factor derivation or transplant problem 8.11's exponential solution:
that problem fixes atmospheric pCO2 and the local buffer derivative, whereas 01
has a finite, evolving atmosphere and a very large initial disequilibrium.
The current 1% settling criterion is not that analytical e-folding time.

**Workload:** substitute within the existing diagnosis, targeting about two minutes
for the chemical explanation. Any extra explanation time must be checked in the
40-minute pilot; there is no additional calculation or run.

## 02: preserve both derivations and refine the effective-pump interpretation

**Already strong:** native reservoir/connection choices, source-concentration
transport laws, student-derived k with units, matched pump-on/off comparison,
and the separately derived external carbon addition. SG's two-box balance
explicitly distinguishes estimating a flux from explaining its biological
mechanism (pp. 11–12); the current calibration-first framing is appropriate.

**Proposed replacement for the broad second half of B4:**

> Sketch production → export → remineralization beside the effective DIC arrow.
> Which steps are collapsed into that arrow? Is the represented transfer primary
> production, export reaching the deep box, or permanent carbon burial? State one
> omitted control on the real process.

Define primary production as carbon fixation and export as organic carbon leaving
the surface layer if those terms need a local reminder. The intended answer is an
effective export-and-deep-remineralization transfer. Surface recycling is omitted,
the model has no separate particle inventory, and the carbon remains available
for return by mixing. Nutrients, light and the depth distribution of recycling
are examples of omitted controls. Keep the existing identification with the
soft-tissue pump and qualification that fitting the full gradient does not
isolate its measured contribution. Basis: SG §1.2 and §8.4; M §§3.1–3.3.

Add only a supplied clarification beside C1: **62.4 is a ratio of existing carbon
stocks at the specified reference state, not the fraction of a future carbon
addition absorbed by the ocean.** SG problem 8.3 calculates a stock partition;
8.13 and §10.2 address the different, incremental uptake problem. No additional
Revelle calculation is needed in core 02.

Retain `J_pump(t) = k DIC_s(t)`, the kg/yr units of k, ratio-derived geometry,
actual 01 initial inventory and masked analytical/code solutions. Do not restore
the removed export-flux comparison or parameter-identifiability question.

**Workload:** a two- to three-minute replacement for the existing B4 answer,
plus one supplied sentence in C1; retain the provisional 55-minute target and pilot it.

## 03: highest priority — make the carbonate counter-pump an explanation task

Students already reconstruct signed DIC/TA effects and link PIC rates in code.
The missing explicit learning check is whether they can use that stoichiometry
to explain **why removal of carbon need not lower seawater pCO2**. Merely
entering `pic_ta_rate = 2 * pic_dic_rate` does not demonstrate that understanding.

**Proposed adaptation of SG 8.4/8.7 and M Figs. 5.5–5.6:** supply a small
pCO2-contour diagram with DIC on the horizontal axis and TA on the vertical axis,
calculated using the benchmark low-latitude conditions and a representative
reference state. Students sketch two small local changes:

> Remove the same amount of DIC through the model's POC pathway and through
> CaCO3 formation. Draw the corresponding DIC–TA arrows and use the contours
> to predict the seawater pCO2 change. Why do the signs differ? Reverse the
> carbonate arrow to explain dissolution.

The instructor key, per unit of carbon removed from the same water mass, is:

| Local change | ΔDIC | ΔTA | Expected local seawater pCO2 response near the benchmark state |
| --- | ---: | ---: | --- |
| Model's DIC-only organic removal | −1 | 0 | Decrease |
| CaCO3 formation | −1 | −2 | Increase |
| CaCO3 dissolution | +1 | +2 | Decrease |

TA entries are equivalents per corresponding mole of carbon. These arrows
describe local chemical perturbations before gas exchange and transport; they
are not alternative full-model integrations or numerical attributions of the
global atmospheric response. Equal inventory transfers between unequal boxes
also produce unequal concentration changes: use each box's own water mass.

Real nitrate-based production has an additional TA effect; preserve the current
supplied nutrient caveat. Use a DIC-only arrow explicitly labelled as the model
closure, rather than silently copying a textbook Redfield arrow. The figure's
chemistry/plotting code should be supplied. Do not give students another plotting
or carbonate-solver implementation task.

**Placement and tradeoff:** use the arrows as the answer format for the existing
POC/PIC inventory-effects fields in 03.1; students then reuse those answers in
03.4. Avoid requiring the same signs in prose, table and diagram three times.
Preserve endpoints, laws, native construction and the boundary derivation.
Target four to six minutes within the reconstruction/export discussion. The
contour interpretation is additional reasoning even if presentation is
consolidated: if the revised opening cannot fit, plan 60 rather than 55 minutes
for 03, or make the contour interpretation optional. Do not silently take time
from 00 or the remaining buffer.

A useful lower-priority alternative is to replace the repeated
concentration-to-inventory explanation in 03.2 with: *Why distinguish the
high-latitude surface box from the low-latitude box, and which circulation arrow
carries its properties into the deep ocean?* SG pp. 13–14 motivate three-box
structure through a failed globally averaged surface model. Use the thermal and
circulation aspects here; do not add oxygen or nutrients to the benchmark.

## 04: sharpen two of the existing four interpretation answers

The revised notebook already does the hard work of specifying controls,
reporting forcing integrals, checking open-boundary budgets and plotting matched
anomalies. Retain those features and the three existing runs.

**Priority A — replace the generic fixed-assumption part of question 4:**

> Deep DIC increases in the carbon-forced run. Is this evidence that biological
> export became stronger? Identify the prescribed and responding fluxes. Propose
> one matched experiment and diagnostic that would test a biological response
> hypothesis, without running it here.

The expected reasoning is that POC and PIC export are prescribed identically
in control and forced cases. Their flux anomalies are therefore zero even while
deep DIC changes through transport, gas exchange and carbonate dissolution.
Their baseline role in setting the carbon distribution is distinct from an
increase in export caused by forcing. Fixed biology still affects the baseline
chemistry and hence the response; it is not scientifically irrelevant.
Keep the existing brief distinction between benchmark reproduction and
conditional prediction. Basis: SG §10.2, pp. 414–415, and problem 10.9.

**Priority B — structure question 3 around two buffering mechanisms:**

> Use the existing plots to distinguish rapid repartitioning among dissolved
> carbonate species from the later change in dissolution/net burial. Which
> conserves TA and which changes the active ocn TA inventory? Identify a
> surface-to-deep lag and explain why a chemical horizon can move before the
> snowline. Is chemical or biological carbonate compensation represented?

Supply the definitions: *chemical compensation* changes carbonate dissolution
and preservation with prescribed carbonate rain; *biological compensation*
also involves changes in calcification/export. The current fixed-export
experiments represent the former. Carbonate equilibrium is applied rapidly
locally, but air–sea exchange and transport take time; sediment response has
additional history. This does not imply a universally strict sequence or that
all adjustment finishes within the plotted interval. Require a stated interval
and small tendencies/balanced fluxes before claiming stationarity.
Basis: SG §§9.5 and 10.2, problems 9.16–9.17 and 10.5; M §5.4 and Box 5.2.
The 2026 ocean-carbon lecture already introduces chemical versus biological
compensation on slide 66.

Keep question 2's important distinction: idealized pure-TA OAE adds no carbon
directly, but the atm–ocn carbon anomaly need not be zero because net burial can
change. These unequal OA/OAE inputs do not measure relative intervention
efficiency. Applying the textbook process reasoning to this OAE experiment is
our adaptation, not an OAE exercise quoted from either book.

**Workload:** retain four short answers and no fourth integration. Replace the
current broad questions with these focused prompts, using a small response table
if needed to keep answers short. Do not append all subquestions to the existing
text. The 15-minute interpretation allocation and 40-minute total still need a pilot.

## Optional follow-ups, outside the core

1. **Stock versus incremental uptake.** Adapt SG 8.13/10.3 using supplied
   PyCO2SYS calls to compare a small and larger carbon addition. Hold TA,
   thermodynamic settings and the system boundary explicit. This extends 01's
   curve interpretation without turning 02 into an anthropogenic-uptake exercise.
2. **Same fitted gradient, different dynamics.** Adapt SG 1.5/1.10 by scaling
   k and Q by the same positive factor in 02. With density fixed, the stationary
   ratio `DIC_d^*/DIC_s^* = 1 + k/(Q rho)` is unchanged, while relaxation can
   change. Air–sea exchange stays another rate control, so do not promise a
   uniform rescaling of the whole trajectory. Use the optional independent-model
   starter; supply execution and plots.
3. **Remineralization depth.** M §3.3 and SG 9.18 motivate a surface/thermocline/deep
   extension that redistributes equal total export between depths. The current
   three-box benchmark has two surface boxes, not an intermediate-depth box.
   Adding this experiment needs a different model, new calibration/restarts and
   a separate session; it is not a small core edit.

## Source cautions and implementation acceptance

- **Alkalinity sign discrepancy:** M printed p. 85 / PDF p. 94 reverses the
  nitrate/ammonium uptake signs in one prose sentence. Printed p. 94, equations
  5.27–5.28, and Table 5.3 on p. 95 correctly give nitrate uptake increasing TA
  and ammonium uptake decreasing it for the stated nutrient bookkeeping.
  These pages were visually checked. Preserve the correct existing 03 wording.
- **Axes differ:** SG Fig. 8.3.5 puts TA on x and DIC on y; M Figs. 5.5–5.6
  put DIC on x and TA on y. Adopt one convention and label units; copying a
  slope without checking axes reverses the apparent stoichiometry.
- **State the boundary:** SG's closed/open distinctions refer to different
  boundaries in different discussions: a water parcel with/without gas exchange
  in §8.3, and inclusion of weathering/burial adjustment in §9.5. Neither label
  alone establishes whether the combined atm–ocn inventory is conserved.
- **Do not copy approximation limits or old numbers as model inputs:**
  carbonate-alkalinity approximations near normal seawater do not describe the
  TA-free extreme; local buffer factors are not constants over large pulses;
  historical textbook budgets/scenarios are not current observations. Use the
  repository's chemistry choices, densities and gas conventions for new figures.
- A separate presentation defect was found in instructor 03, the written answer
  after Exercise 03.2: the intended `m = \rho V` is split into `m=` and `ho V`,
  and multiplication is rendered as commas. This has been corrected in the
  implementation; it is unrelated to the textbook-driven scope proposal.

Implementation updated instructor sources, masked the new interpretations,
regenerated student 01–04 and aligned teaching goals/design/workplan with the
final scope and provisional timing. Local chemistry signs and units, rendered
equations/contours and student masking were checked; all four instructor
notebooks executed with their conservation checks. See `../WORKPLAN.md` for
verification evidence and the unrelated existing 00 generated-copy mismatch.
The core replacements require no numerical model changes or new prerequisites.
The optional follow-ups remain proposals, not implemented notebook behavior.
