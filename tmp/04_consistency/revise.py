import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
p = ROOT / 'notebooks/instructor/04_pump_strength_OA_OAE.ipynb'
nb = json.loads(p.read_text(encoding='utf-8'))
c = nb['cells']
def put(i, text):
    c[i]['source'] = text.strip().splitlines(keepends=True)
def get(i):
    return ''.join(c[i]['source'])

put(0, get(0).replace('specify matched experiments; map external inputs; use budget-checked anomalies to explain mechanisms, timing and limits.', 'interpret how carbon and alkalinity inputs change atm CO2, ocean chemistry and carbonate preservation; explain critical-depth motion and OA/OAE asymmetry using matched controls.'))
put(1, get(1).replace('from reservoir_inputs import reservoir_inventory_rows\n', '').replace('OAE_TARGET_PMOL = 10.0\nOAE_SCALE = REFERENCE_SCALE * OAE_TARGET_PMOL / REFERENCE_CARBON_PMOL\n', ''))
put(2, '''## A1. Reuse the model specification from 03

Use your completed 03 schematic as the experiment map; add the external input arrow. Each case uses an independent copy of the same workbook geometry, box-specific T/S/P, transport and baseline rates, and the same saved nearly stationary state (the **restart**). These saved concentrations replace the workbook initial values.

POC/PIC export and weathering remain fixed; gas exchange and carbonate dissolution/burial respond to the evolving state. The atm reservoir is finite. **Ocean acidification (OA)** here is driven by carbon input; idealized **ocean alkalinity enhancement (OAE)** supplies TA with no direct carbon input.

OA uses the archived IS92a-shaped forcing (scale 0.877, no terrestrial uptake). OAE uses the same time profile, with its own prescribed amount. These are a historical benchmark scenario and a teaching intervention, not present-day forecasts. Runs cover model years 0–3800 with a one-month maximum step; year 1800 is the reporting reference, not a switch from exactly zero input.

After changing a forcing choice, rerun the case-building cell and all subsequent cells. Changing baseline geometry, chemistry or process rates requires a new compatible stationary restart.''')
put(3, get(3).replace('Revisit this prediction in your four final answers.', 'Revisit this prediction in C1.'))
put(6, '''## A2. Exercise 04.1: specify the two forcing inventories

Use the amounts in A1's table for the interval after model year 1800.

<div style="background-color: #edf5ff; color: #173b61; border-left: 4px solid #3977b8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">

**Question — specify forcing inventories**

Assign `oa_target_mol` and `oae_target_mol` in mol C and mol TA equivalents. One Gt is $10^{15}$ g, one Pmol is $10^{15}$ mol, and carbon has molar mass 12 g/mol. The supplied scaling preserves the archived shape and its small pre-1800 tail; B1 reports both the post-1800 and whole-run inputs.

</div>''')
put(9, get(9).replace('params = make_pump_variant(\n        base=P, solubility_strength=1.0, soft_tissue_strength=1.0,\n        carbonate_strength=1.0, soft_tissue_feedback=False, carbonate_feedback=False,\n    )', 'params = make_pump_variant(base=P)  # independent copy with fixed baseline export').replace("\ndisplay(pd.DataFrame(reservoir_inventory_rows(fixed_cases['control'])).set_index('Box'))", ''))
put(10, r'''## B1. Inspect the forcing, then check the runs

The first plot shows the **actual input rates supplied to the solver**, before any response. Separate axes retain mol C versus TA-equivalent units; the third panel divides each rate by its own peak to compare timing only. The vertical line marks year 1800. Follow the rise, peak and decline and inspect whether input has ended when interpreting a later response. Area under a rate curve is an inventory; peak height is not the total input.

The supplied inventory check then precedes the three model integrations. Reuse 03's active boundary (atm plus dissolved ocn; sediment outside) and its weathering carbon flux $W_0$:

$$\frac{dC_{atm+ocn}}{dt}=I_C(t)+W_0-B_{net}(t),\qquad
\frac{dA_{ocn}}{dt}=I_A(t)+2W_0-2B_{net}(t).$$

Here $I_C$ is experimental carbon input [mol C/yr] and $I_A$ is experimental TA input [equivalents/yr]. $B_{net}$ is the signed net burial already defined in 03; negative values return sediment material to the active inventories. OA has $I_A=0$; pure-TA OAE has $I_C=0$.

Inspect the supplied budget errors once before interpreting results. They compare inventory changes with integrated boundary fluxes, allowing for numerical quadrature; passing does not require constant inventories or establish scientific realism.''')
forcing_cell = {'cell_type': 'code', 'execution_count': None, 'id': 'forcing-before-responses', 'metadata': {}, 'outputs': [], 'source': [
    '# Understand and run: inspect prescribed causes before interpreting responses.\n',
    'from teaching_plots import plot_external_forcings\n',
    'plot_external_forcings(fixed_cases, pulse_start=PULSE_START)\n',
    'plt.show()']}
put(12, r'''## B2. Interpret matched responses

For each quantity use the <mark style="background-color: #fff0b3; color: #513d00; padding: 0.05em 0.2em; border-radius: 3px;"><strong>matched anomaly</strong></mark>

$$\Delta Y(t)=Y_{forced}(t)-Y_{control}(t).$$

Subtracting the control removes shared baseline drift. It isolates the response to the prescribed input within this model; it does not remove numerical error or validate omitted processes.

Read the atm CO2 and low-latitude surface pH anomalies first, then deep DIC and dissolution/net burial. Compare their signs and turning points with the forcing in B1: a response maximum need not coincide with the input-rate maximum. Surface chemistry, gas exchange, transport and sediment adjustment act together, with different response times.

**Compare mechanisms and timing, not raw amplitudes:** the two columns have different vertical scales, input species and total amounts. The overlaid normalized forcings establish common timing only; they do not make the interventions equally strong. Use B2 for C1–C2 and the depth/flux panels below for C3–C4.''')
put(14, r'''## B3. Read critical depths and carbonate preservation

These complete figures reuse the same runs. Solid lines are model results; OA's dotted lines are archived digitizations of the published benchmark. Use them to assess reproduction, while B2's matched anomalies identify the forcing response.

| Panels | Read for |
| --- | --- |
| a / b / c | DIC, TA and pH: surface-to-deep chemical change |
| d / f | Air–sea transfer and atm CO2 |
| e / h | Critical depths, dissolution and net burial: carbonate preservation |
| g | The forcing from B1, repeated here as a timing reference |

The three <mark style="background-color: #fff0b3; color: #513d00; padding: 0.05em 0.2em; border-radius: 3px;"><strong>critical depths</strong></mark> answer different questions. Calcite saturation $\Omega$ compares the calcium–carbonate ion product with its equilibrium solubility product; $\Omega<1$ means undersaturation.

| Depth | Physical meaning | What controls it here? |
| --- | --- | --- |
| $z_{sat}$: saturation horizon | Water has $\Omega_{calcite}=1$; deeper water is undersaturated | Current deep carbonate chemistry and pressure-dependent solubility |
| $z_{cc}$: compensation depth | Dissolution balances the arriving modern CaCO3 rain; none survives for burial | Current chemistry, dissolution kinetics and prescribed rain |
| $z_{snow}$: snowline | Deepest boundary of existing reactive carbonate sediment | Past deposition and dissolution; erosion takes time |

Thus undersaturated water does not imply immediate disappearance of all sediment carbonate. This distinction follows [Boudreau et al. (2010), *Carbonate compensation dynamics*](https://doi.org/10.1029/2009GL041847). Depth is positive downward in these definitions, but **panel e plots elevation $-z$**: upward means shallower. The lower limit of the implemented saturation horizon is 200 m; reaching that bound is not evidence that every surface water is undersaturated.

**Read e together with h.** When compensation depth and snowline separate, the sediment present need not be in equilibrium with current rain and chemistry. In this implementation, erosion depends on the finite existing reactive stock; during deepening the snowline is made to follow the compensation depth rapidly. It does not resolve gradual accumulation of a new sediment column. Treat that part of the OA/OAE contrast as a model assumption.

**Chemical carbonate compensation** means changing dissolution/preservation at fixed carbonate rain. It changes dissolved TA, unlike acid–base repartitioning among dissolved species. POC and PIC exports remain prescribed in all three cases: changing deep DIC alone cannot establish changing biological export.

The benchmark's transient depth separation and sediment response are discussed in [Boudreau et al. (2010), *Ongoing transients in carbonate compensation*, sections 3.1–3.2](https://doi.org/10.1029/2009GB003654). Read the selected panels for the four answers below; no sediment-equation derivation or panel-by-panel report is required.''')
put(17, r'''## C. Explain the scientific results in four short answers

Use two or three sentences per answer, referring to a curve and an approximate model year or interval. Read approximate values from the supplied plots; no extra calculations or runs are required.

<div style="background-color: #edf5ff; color: #173b61; border-left: 4px solid #3977b8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">

**Question — mechanisms, critical depths and OA/OAE asymmetry**

1. **Forcing and response:** revisit your sign prediction using B2. Compare the input-rate peak with the atm/surface response and one delayed deep response. Does declining input mean the perturbation is over?
2. **Carbon uptake and TA:** explain OAE's atm CO2 response without a direct carbon input. Contrast TA-conserving dissolved-species repartitioning with the changing ocn TA in OA; use the net-burial term in B1 and panel h as evidence.
3. **Critical depths and memory:** compare the directions and separation of $z_{sat}$, $z_{cc}$ and $z_{snow}$ in OA and OAE. What does the OA interval between compensation depth and snowline imply for old sediment, and why is OAE deepening not simply the reverse history? Relate the contrast to dissolution/net burial and the stated snowline assumption.
4. **Asymmetry and limits:** identify one difference beyond opposite response signs. Separate unequal forcing amounts/entry species from a chemical or sediment mechanism. Why can these runs establish neither an OAE amount that cancels OA nor stronger biological export from higher deep DIC? State what the late curves and benchmark overlay do (and do not) establish.

</div>

<!-- BEGIN SOLUTION -->
<div style="background-color: #f3eefb; color: #38224f; border-left: 4px solid #7952a8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">

**Instructor answer**

1. OA raises atm CO2 and lowers surface pH; OAE initially does the reverse. Locate the forcing peak in B1 and compare it with B2's extrema: the deep signal develops more slowly as transport carries the perturbation downward, while declining positive input still adds material and sediment adjustment continues. A peak or the final plotted value alone is not equilibrium.
2. Adding TA shifts dissolved carbonate speciation and lowers aqueous CO2, driving internal transfer from atm to ocn without external carbon addition. Dissolved acid–base repartitioning itself conserves TA; OA's enhanced dissolution/reduced net burial retains or returns TA to the active ocn at two equivalents per mole of carbonate carbon. Changed net burial also changes total active carbon, so atm loss need not equal ocn gain exactly.
3. OA shoals the chemical horizons while the snowline erodes more slowly: old carbonate remains below the new compensation depth and can dissolve although modern rain no longer survives there. OAE deepens the horizons and favors preservation; its snowline follows the compensation depth closely under the supplied rapid-deepening rule. This contrasts finite-stock erosion with an idealized deepening closure, rather than demonstrating symmetric sediment recovery.
4. OA's pronounced depth separation and dissolution response differ from OAE's smaller deepening and increased preservation. The amplitudes alone cannot establish intrinsic asymmetry because the inputs differ in amount, species and receiving box; nonlinear chemistry and sediment history give additional reasons not to expect mirror images. Fixed POC/PIC export excludes stronger biological export as the explanation of higher deep DIC. These separate perturbations do not test cancellation, late adjustment is not proven stationarity, and the OA overlay supports model reproduction rather than independent observational validation.

</div>
<!-- END SOLUTION -->

**You have completed 04.** Keep your forcing choices, checked budgets and four interpretations here.''')
# Remove the trailing empty cell; insert the forcing plot before audit/integration.
nb['cells'] = c[:11] + [forcing_cell] + c[11:18]
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None
p.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
build_student_notebook(p, ROOT / 'notebooks/student' / p.name)
print('Revised and regenerated 04')
