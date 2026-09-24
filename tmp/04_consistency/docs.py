from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
p = ROOT/'TEACHING_GOALS.md'
s = p.read_text(encoding='utf-8').replace('four evidence/design answers', 'four scientific interpretations')
start = s.index('## 04 — Matched carbon and alkalinity experiments')
end = s.index('## Optional material and maintenance',start)
s = s[:start] + '''## 04 — Matched carbon and alkalinity experiments (40 minutes)

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
rapid snowline-deepening assumption. Fixed POC/PIC export cannot establish a
biological response. Unequal OA/OAE amounts cannot establish relative efficiency
or cancellation; late values alone do not establish equilibrium; the benchmark
overlay supports reproduction, not independent observational validation.

The two original 2010 Boudreau papers support local definitions and scientific
interpretation. Detailed sediment equations and extension experiments remain
outside the required work. The 40-minute allocation is still provisional:
pilot the revised depth/asymmetry reading and four answers before relying on it.

''' + s[end:]
p.write_text(s,encoding='utf-8')
p = ROOT/'ref/design.md'
s = p.read_text(encoding='utf-8')
start = s.index('In 04, two of the existing four answers')
end = s.index('The lecture slides',start)
s = s[:start]+'''In 04, the four answers focus on interpreting forcing/response timing,
carbon uptake and TA, critical-depth motion and sediment memory, and OA/OAE
asymmetry and limits. Fixed biological export remains an interpretive boundary;
the former biological-response experiment proposal is suspended with the 04
extension. No extra core integrations, prerequisites or sediment equations are added.

'''+s[end:]
start=s.index('The 40-minute core starts')
end=s.index('The separate optional `extensions/05',start)
s=s[:start]+'''The 40-minute core starts with predictions and an experiment specification on
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
Distinguish erosion of pre-existing sediment from the supplied rapid-deepening
snowline closure; do not claim that the latter predicts realistic accumulation
times. Read depth separation alongside dissolution/net burial rather than assuming
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

'''+s[end:]
p.write_text(s,encoding='utf-8')
p=ROOT/'README.md'
s=p.read_text(encoding='utf-8')
s=s.replace('before running. Matched-control anomalies come first, followed by full eight-panel\nfigures for pathways, sediment memory and the benchmark overlay. Four short answers\naddress design/evidence, mechanism/budget, timing/processes and a proposed next test.', 'before running. The actual forcing shapes appear in B1 before matched-control\nanomalies in B2; full figures then support critical-depth, sediment-memory and\nbenchmark interpretation. Four short answers address timing, carbon uptake/TA,\ncritical depths and OA/OAE asymmetry, with the assumptions and limits of these runs.')
p.write_text(s,encoding='utf-8')
p=ROOT/'data/Boudreau_2010/README.md'
s=p.read_text(encoding='utf-8').replace('Part I of 04 starts from the workbook state. Altered baseline geometry,', 'The dormant attribution extension starts its separate tagged calculation from\nthe workbook state. Altered baseline geometry,')
p.write_text(s,encoding='utf-8')
print('Updated current teaching scope and corrected stale 04 data-guide pointer')
