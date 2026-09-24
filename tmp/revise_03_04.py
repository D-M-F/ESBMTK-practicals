"""One-time editing script. Instructor notebooks remain the teaching sources."""
import json
import sys
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from teaching_specification import flux_specification, implementation_references
from scripts.build_student_notebooks import build_student_notebook

BEFORE = ROOT / 'tmp/03_04_revision'
old3 = nbf.read(BEFORE / '03_boudreau_three_box_model.ipynb', 4)
old4 = nbf.read(BEFORE / '04_pump_strength_OA_OAE.ipynb', 4)
BLUE = 'background-color: #edf5ff; color: #173b61; border-left: 4px solid #3977b8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;'
PURPLE = BLUE.replace('#edf5ff', '#f3eefb').replace('#173b61', '#38224f').replace('#3977b8', '#7952a8')

def md(text, **kwargs):
    return nbf.v4.new_markdown_cell(text.strip(), **kwargs)

def code(text, **kwargs):
    return nbf.v4.new_code_cell(text.strip(), **kwargs)

def q(title, body):
    return f'<div style="{BLUE}">\n\n**Question — {title}**\n\n{body.strip()}\n\n</div>'

def answer(text):
    return f'<!-- BEGIN SOLUTION -->\n<div style="{PURPLE}">\n\n**Instructor answer**\n\n{text.strip()}\n\n</div>\n<!-- END SOLUTION -->'

def gold(text):
    return f'<mark style="background-color: #fff0b3; color: #513d00; padding: 0.05em 0.2em; border-radius: 3px;"><strong>{text}</strong></mark>'

def table(rows, columns):
    return '\n'.join(['| '+' | '.join(columns)+' |', '| '+' | '.join(['---']*len(columns))+' |']+
                     ['| '+' | '.join(str(r[c]).replace('|','/') for c in columns)+' |' for r in rows])

KEY = f'''**Reading key:** {gold('Key term')} = concept to notice. Blue **Question** panels identify student work; purple **Instructor answer** panels appear only in the instructor sheet.
Code labels distinguish **Choose and explain**, **Understand and run**, and **Supplied implementation**.
This practical is ungraded. Keep your explanations here; no separate submission is required.
The [coding cheatsheet](../../ref/modelling_cheatsheet.md) is optional lookup support; essential syntax is explained locally.'''

c=[]
c.append(md('''# 03 — Reconstruct, build and audit a three-box model

**Learning goals:** reconstruct a scientific flux diagram; translate it through Excel records into native ESBMTK objects; distinguish graph, budget and restart checks.

**Provisional time: 55 minutes.** Diagram and Excel reconciliation (15), four native mappings (20), boundary budget and checks (15), explanation (5). This allocation needs a student pilot.

Follow **reconstruct → reconcile → map → run → check → explain**. Your diagram and flux table are the specification for your code and for 04. Repeated loops, chemistry/sediment wiring, integration and plotting are supplied.
The construction below does not call the complete-model helper.
[Teaching goals](../../TEACHING_GOALS.md).

'''+KEY))
c.append(md(r'''## A1. What changes from 02?

This is a Boudreau-like benchmark with a different specification. Do not carry over 02's fitted k, ratio-derived geometry or total carbon inventory.

| Feature | 02 | 03/04 |
| --- | --- | --- |
| Geometry and conditions | Two layers, uniform T/S/P | Low-/high-latitude surface and deep boxes; box-specific conditions |
| Organic export | $kDIC_s(t)$ | Fixed POC export |
| Carbonate processes | Absent | PIC export, dissolution and net burial |
| Active atm–ocn boundary | Closed except the pulse | Weathering and net burial; forcing added in 04 |
| Reference state | Calibrated constraints | Archived benchmark restart |

POC and PIC mean **particulate organic and inorganic carbon**. Here POC export includes full deep remineralization: conversion back to dissolved carbon. There is no explicit particle or nutrient inventory. The **rain ratio** is PIC/POC carbon export; the workbook prescribes this ratio and POC, then the loader derives PIC.

Read [ESBMTK section 3 and Figure 3](../../ref/ESBMTK.pdf#page=8) (printed p. 1162; [online version](https://gmd.copernicus.org/articles/18/1155/2025/#section3)). Use these corrections:

- The organic-export label in the prose should be **F5**, not F3; F3 denotes circulation.
- The benchmark uses **F6/F5 = PIC/POC = 0.3**, not the inverted ratio in the prose.
- Weathering supplies **dissolved inorganic carbon** here, not organic carbon.

Figure 3 is an incomplete specification: its arrows omit equations, stoichiometry and an explicit dissolution return. Reconstruct those properties using the following assumptions and workbook inputs.'''))
c.append(md(r'''### Supplied process assumptions

Use these to specify the model; they are not universal descriptions of the ocean.

- Water transport carries DIC and TA at its source concentration. The circulation is a closed loop through both surface boxes and the deep box; mixing exchanges water between high latitudes and depth. Each fixed-volume box gains and loses equal water.
- Each surface exchanges CO2 with the same finite atmosphere. As in 01/02, invasion and outgassing are two conceptual transfers evaluated by one native connection. Chemistry calculates aqueous CO2 and pH from DIC/TA and local conditions; these diagnostics are not extra carbon inventories.
- Only low latitudes export POC/PIC in this benchmark. POC is fully remineralized at depth, with no TA effect in this closure. Real nutrient uptake and recycling can affect TA: nitrate uptake increases it, whereas ammonium uptake decreases it. A richer model needs the associated nutrient/redox bookkeeping rather than an arbitrary TA coefficient on POC.
- CaCO3 formation removes one dissolved carbon and two TA equivalents per mole; dissolution reverses that reaction. Carbonate rain enters a sediment-process module, which calculates dissolution using deep chemistry and sediment history. The **snowline** is the depth boundary of reactive sediment and carries memory; there is no explicit conserved sediment-carbon stock. Detailed equations remain [optional](../../ref/sediment_reference.md).
- The prescribed weathering input is a lumped **1 DIC : 2 TA** boundary closure. This is not a universal river composition. Carbonic-acid weathering of CaCO3 delivers two bicarbonates while consuming one CO2: river-only and combined atm–ocn accounting differ. This model applies its lumped source to the low-latitude box, with no explicit atmospheric weathering sink.

Biological TA effects and weathering accounting are discussed in [Middelburg et al. (2020), sections 4–6](https://doi.org/10.1029/2019RG000681). These notes explain the chosen simplifications; they add no nutrient or weathering-reaction derivation.

**Rate choices.** Both exports are fixed in 03/04. In 02, constant k still gave state-dependent export through $kDIC_s(t)$. Fixed exports do not freeze the rest of the model: gas exchange and dissolution respond to evolving conditions. Additional biological response laws are hypotheses explored in the optional extension.'''))
setup=old3.cells[4].source.replace('import pandas as pd','import pandas as pd\nimport numpy as np')
setup=setup.replace('ROOT = Path.cwd().resolve()\nif ROOT.name in {\'instructor\', \'student\'}:\n    ROOT = ROOT.parents[1]\nelif ROOT.name == \'notebooks\':\n    ROOT = ROOT.parent', "ROOT = next(p for p in (Path.cwd().resolve(), *Path.cwd().resolve().parents)\n            if (p / 'teaching_config.py').is_file())")
setup += '\nfrom teaching_specification import BASELINE_PARAMETERS, workbook_connections\nfrom teaching_audits import audit_benchmark_graph, audit_complete_model, audit_restart_drift'
c.append(code(setup))
c.append(md('''### A2. Inspect the numerical inputs

The workbook owns areas, volumes, box-specific T/S/P and initial states. The atmosphere has its own mole-fraction and total-air units. **Initial concentrations are replaced by the archived restart later.** Geometry and rates are retained.

For now inspect only reservoir and baseline parameter tables. Connection rows come after your reconstruction. Optional feedback settings are omitted from this view. Excel editing is not required.'''))
c.append(code('''# Understand and run: read these supplied inputs before drawing.
display(pd.DataFrame(input_tables['OceanReservoirs']).set_index('Box ID'))
display(pd.DataFrame(input_tables['Atmosphere']).set_index('Box ID'))
baseline_parameters = pd.DataFrame(input_tables['ProcessParameters']).set_index('Parameter')
display(baseline_parameters.loc[list(BASELINE_PARAMETERS)])'''))
student_rows=flux_specification(student=True)
student_table=table(student_rows, ('Process ID','Process','Endpoints','Inventory effects','Flux rule','Status'))
c.append(md('''## A3. Exercise 03.1: reconstruct the diagram and flux properties

![Box outlines for reconstruction](../../ref/figures/03_04_boudreau_student.png)

'''+q('reconstruct a scientific specification',r'''Sketch or annotate the outlines; drawing quality is irrelevant. Use descriptive IDs (T, M, G, POC, PIC, W, D, B_net), keeping F1–F8 only as paper aliases.

1. Label the states and active atm–ocn boundary. Distinguish chemistry diagnostics and the sediment-memory state.
2. Draw the three circulation legs, both mixing directions, and invasion/outgassing at each surface. Check water balance at H_b and cancellation of one internal transfer.
3. Draw POC/PIC export, weathering, the **explicit dissolution return**, and signed net burial. A dashed information arrow may connect deep chemistry to the module.
4. Complete the process-family table below. Write source/destination effects with signs. State units: carbon in mol C/yr, TA in equivalents/yr, concentrations in mol/kg or equivalents/kg. One family law covers repeated water arrows.

For dissolution use the supplied functional form; detailed sediment equations are not an exercise. For burial, relate export and dissolution, allowing loss of old sediment. Do not create an extra sediment-carbon box.''')+'''

An unrelated format example: **dye input → tank; +J to dye inventory; J = prescribed rate; mol dye/yr; external prescribed input**.

'''+student_table+'''

Edit this Markdown table or use the [student Excel worksheet](../../outputs/03_04_flux_specification/student.xlsx). Its amber cells are answer spaces; it does not alter model inputs. Numerical values remain in the production workbook.

'''+answer(r'''![Completed instructor specification](../../ref/figures/03_04_boudreau_instructor.png)

H_b gains 25 Sv through circulation plus 30 Sv through mixing and loses the same amounts. Each internal transfer has equal source loss and destination gain. pH/CO2aq are diagnostics; DIC/TA and atm CO2 are evolving reservoir states. Snowline is a sediment-memory state, not an additional carbon inventory.

The completed flux table follows. Net burial is E - D: the overall dissolved-system loss is B_net in carbon and 2 B_net in TA. A negative B_net returns old sediment material.''')))
c.append(code('''# Instructor reference: the student file omits this completed table.
from teaching_specification import flux_specification, implementation_references
display(pd.DataFrame(flux_specification()).set_index('Process ID'))
display(pd.DataFrame(implementation_references()).set_index('Process ID'))''',metadata={'tags':['solution-only']}))
c.append(md('''### A4. Reconcile your drawing with Excel

After your attempt, compare each connection row with your arrows. Identify it by **source + sink + flux_id**: all three circulation rows use `thc`, so that ID alone is not unique. Correct your diagram before using it for construction.

| Diagram content | Input owner / stable key | Code role |
| --- | --- | --- |
| Geometry and states | OceanReservoirs / Box ID; Atmosphere | Reservoir specification |
| Water arrows | TransportConnections / source, sink, flux_id | Native bulk connections |
| Gas exchange | GasExchangeConnections / Atmosphere, Surface | Individual gas connections |
| POC and PIC | ProcessParameters / poc_export, rain_ratio | PIC derived from POC × ratio |
| Weathering | ProcessParameters / weathering_dic; BoundaryNodes / Fw | TA derived as twice weathering DIC |
| Dissolution / burial | Calculated responses, no prescribed flux row | Supplied carbonate module |

The [flux worksheets](../../ref/boudreau_diagrams.md) document these links. Their process table is **teaching documentation**, not an executable input schema. POC/PIC/weathering topology and sediment coupling are supplied Python patterns. `Fb` declares a boundary node; it does not require an additional active drain.

The loader validates names, units and water balance. It creates parameter records, not reservoirs. Changing the baseline geometry, chemistry or rates later requires a new compatible stationary state.'''))
c.append(code('''# Understand and run: compare these rows with the diagram you reconstructed.
display(pd.DataFrame(input_tables['TransportConnections']).sort_values('Order'))
display(pd.DataFrame(input_tables['GasExchangeConnections']).sort_values('Order'))
display(pd.DataFrame(input_tables['BoundaryNodes']).set_index('Box ID'))
display(pd.DataFrame(workbook_connections(WORKBOOK)).set_index('ID'))'''))
c.append(md('''## B1. Exercise 03.2: map reservoirs

`Model` defines the clock, units and chemistry options; it is not a physical box or the system boundary. Run its supplied construction, then map the ocean records. Geometry remains explicit and ESBMTK calculates density from each box's T/S/P.

'''+q('map reservoir fields', '''Complete `concentrations` and `geometry` using the `box` record. Use species keys `M.DIC`, `M.TA` and geometry keys `area`, `volume`. The loop and T/S/P mapping are supplied.
Trace one initial concentration from Excel to its state. Explain how volume and density convert ocn concentration to inventory, and why atm mole fraction needs a different conversion.''')+'''

**Local syntax:** `box['dic']` retrieves a record field; `M.DIC` is the registered species, while `M.H_b.DIC` is its state in a particular reservoir. Dictionary keys are case-sensitive. The partial example below supplies the unchanged environmental fields.'''))
c.append(code(old3.cells[10].source))
c.append(code("# Understand and run: partial record-to-constructor example.\nhigh = P['boxes']['H_b']\nhigh_specification = {'T': high['temperature'], 'P': high['pressure'], 'S': high['salinity']}\nhigh_specification"))
c.append(code(old3.cells[13].source.replace('03.1','03.2').replace('following high_specification','using your diagram and the field hints')))
c.append(code(old3.cells[15].source))
c.append(md(answer(r'''For a water mass $m=ho V$, carbon inventory is $m,DIC$ and TA inventory is $m,TA$. Convert µmol/kg to mol/kg first. Atmospheric carbon is $N_{atm}x_{CO2}$ with dry-air mole fraction x; ppm must be multiplied by $10^{-6}$. `box['dic']` supplies an initial concentration, not a fixed target imposed during integration.''')))
c.append(md(r'''## B2. Exercise 03.3: map water arrows and their law

For a directed physical water transport, $q_{i\to j}=\rho Q_{i\to j}$ in kg/yr and
$$J_{i\to j}^{(X)}(t)=q_{i\to j}X_i(t),\qquad X=\mathrm{DIC\ or\ TA}.$$
The flux removes material at the source and adds the same amount at the destination.

**Benchmark unit convention:** 02 explicitly uses $Q\rho$. The historical benchmark instead passes volume scales through a native conversion to litres/yr while the states use mol/kg. We retain that nominal numerical conversion for reproduction; it is not a general dimensional recipe for new models. Inventories still use ESBMTK densities. A physical correction requires a separately tested baseline and fresh restart.

As in 02, `Source_to_Sink@id` names a route. `ty` (or individual `ctype`) chooses the law; `sp` chooses species.

| Law choice | Meaning | Supplied coefficient |
| --- | --- | --- |
| `scale_with_concentration` | coefficient × source concentration | `sc` |
| `Fixed` | prescribed amount/time; alias of `regular` | `ra` |
| `gasexchange` | invasion minus outgassing | gas-transfer settings |

'''+q('implement your water arrows', '''Complete endpoints, transported species and `transport_type` from your reconciled specification. For the H_b-to-D_b mixing arrow, identify which concentration appears in its law. Would substituting destination concentration necessarily fail a whole-system inventory test?''')))
trans=old3.cells[17].source.replace("display(pd.DataFrame(input_tables['TransportConnections']).sort_values('Order'))\n",'')
trans=trans.replace('03.2','03.3').replace('transported_species = [M.DIC, M.TA]',"transported_species = [M.DIC, M.TA]\n    transport_type = 'scale_with_concentration'")
trans=trans.replace("'ty': 'scale_with_concentration'", "'ty': transport_type")
c.append(code(trans))
c.append(md(answer('''The H_b-to-D_b flux uses H_b's current concentration. Using D_b's concentration would implement a different process, but equal source loss and destination gain could still conserve total inventory. Graph and equation checks therefore complement conservation.''')))
c.append(md('''## B3. Exercise 03.4: map biological export

Use the POC and PIC arrows from your diagram. The native PIC connections have nominal deep endpoints but bypass those sinks; the supplied carbonate module adds the actual dissolution return later. A direct addition of all PIC to deep DIC/TA would represent a different model.

'''+q('choose pump species, laws and linked rates',r'''Assign POC source/sink/species, select `export_type` from the law choices above, and link the PIC DIC and TA rates. Compare this closure with 02: if $DIC_s(t)$ changes while parameters stay fixed, what happens to export in each model?''')))
pump=old3.cells[19].source.replace('03.3','03.4').replace("poc_species = M.DIC", "poc_species = M.DIC\nexport_type = 'Fixed'")
pump=pump.replace("'ty': 'Fixed'", "'ty': export_type")
c.append(code(pump))
c.append(md(answer(r'''Here POC and PIC export remain constant. In 02, $J_{pump}(t)=kDIC_s(t)$ changes proportionally with surface DIC despite constant k. The benchmark's fixed rain ratio links baseline PIC to POC; the computed ratio afterward is a consistency check, not an independent prediction.''')))
c.append(md('''### Supplied dissolution and chemistry wiring

Your dissolution arrow returns material to deep dissolved inventories. `add_carbonate_system_2` supplies that coupling using the actual PIC flux object, deep chemistry and the snowline. Do not add another manual dissolution connection.

The saturation horizon marks calcite saturation = 1; the compensation depth concerns survival of modern rain. Both are chemistry-dependent diagnostics. The snowline retains sediment history and may lag. Dissolution can exceed current rain when old sediment dissolves, giving negative net burial. Net burial is a diagnostic boundary residual, not another deep-water drain.

The benchmark coefficient `alpha` was tuned in the ESBMTK reproduction; agreement with its reference is not independent evidence for that coefficient.'''))
c.append(code(old3.cells[21].source))
c.append(md(r'''## B4. Exercise 03.5: connect the atmosphere

As in 01, use solubility and the current atmosphere for invasion. For surface i, schematically,
$$J_{gas,in,i}(t)=v_iA_iK_{0,i}pCO_{2,atm}(t),\qquad
J_{gas,out,i}(t)=v_iA_i[CO_2]_{aq,i}(t).$$
Here solubility $K_0$ converts partial pressure to mol/m³; aqueous CO2 also uses mol/m³. With area in m² and velocity in m/yr, flux is mol C/yr. Native code handles these conversions from dry-air mole fraction and mol/kg states. Local conditions affect solubility. The ocean and atmosphere receive equal-and-opposite tendencies.

One gas connection evaluates invasion minus outgassing. Its named endpoints set the positive direction, not a permanently one-way flux. Chemistry, gas exchange and circulation together produce solubility-related storage; there is no extra solubility-pump arrow to add.

'''+q('map gas exchange', '''Assign `gas_source`, `gas_sink` and `gas_species` inside the supplied loop. `getattr(M, row['atmosphere'])` retrieves the named atmospheric object; `surface_box.DIC` selects a state within a surface box. Why does gas exchange update DIC although its law uses aqueous CO2?''')))
gas=old3.cells[23].source.replace("display(pd.DataFrame(input_tables['GasExchangeConnections']).sort_values('Order'))\n",'').replace('03.4','03.5')
c.append(code(gas))
c.append(md(answer('''Aqueous CO2 is a diagnostic fraction of DIC. Transfer of CO2 therefore changes DIC, after which carbonate chemistry repartitions the dissolved carbon. Treating CO2aq as an additional carbon stock would count carbon twice.''')))
c.append(md('''### Supplied weathering connection

The workbook prescribes `weathering_dic`; the loader derives the paired TA rate for this benchmark closure. Changing the ratio would require revisiting the joint carbon/TA budget and stationary state, not just substituting a new value. Run the native boundary connection unchanged.'''))
c.append(code(old3.cells[25].source+'\n# Supplied metadata for the same boundary audit used in 04.\nM.weathering_strength = 1.0'))
c.append(md('''## C1. Check the graph before integrating

The supplied structural check matches endpoints, species, laws and process rates with the specification. Inspect this single summary and trace a water arrow, POC, linked PIC pair and gas connection to your diagram. A passing inventory check alone cannot establish that these are the intended equations.'''))
c.append(code('''# Understand and run: inspect one complete native graph summary.
connection_table = pd.DataFrame(audit_benchmark_graph(M))
display(connection_table)'''))
c.append(md(r'''## C2. Complete the boundary budget

Continue **inputs minus outputs** from 01/02. Define
$$C_{atm+ocn}=N_{atm}x_{CO2}+\sum_i m_iDIC_i,\qquad
A_{ocn}=\sum_i m_iTA_i.$$
Let $W_C$ and $W_A$ denote weathering carbon and TA input, E carbonate export, D dissolution and $B_{net}$ signed net burial. Carbon fluxes use mol C/yr and TA fluxes equivalents/yr. Positive net burial removes material from active atm–ocn inventories.

'''+q('sum the inventories',r'''Which water, gas and organic transfers cancel? Complete $B_{net}=$ …, $dC_{atm+ocn}/dt=$ … and $dA_{ocn}/dt=$ … for this unforced model. Use your linked carbonate effects and $W_A=2W_C$. Explain why adding a separate burial sink after accounting for PIC export and dissolution would be wrong.''')+'\n\n'+answer(r'''Internal water, gas and POC transfers cancel. Carbonate export removes E and dissolution returns D, so
$$B_{net}(t)=E(t)-D(t),\qquad
\frac{dC_{atm+ocn}}{dt}=W_C-B_{net}(t),\qquad
\frac{dA_{ocn}}{dt}=W_A-2B_{net}(t).$$
Counting both export-minus-dissolution and another burial sink counts the same loss twice. If D > E, negative net burial returns old sediment material. Speciation itself creates neither carbon nor TA.''')))
c.append(md('''## C3. Load the reference state and check the short restart

The archived state avoids the million-year spin-up in class. It supplies state, not connections: your graph determines subsequent tendencies.

Run 20 unforced years. The supplied check allows at most **0.01 µmol/kg DIC, 0.01 µeq/kg TA, 0.01 ppm atm CO2 and 0.01 m snowline movement**, measured at every saved time relative to the first. These are absolute teaching tolerances over this short run, not a relaxation timescale or proof of long-term stability.

The separate audit integrates weathering and solver-consistent net burial and checks carbon/TA inventories. Its relative tolerance (2 × 10⁻⁵ of the evolving stock, plus a small absolute allowance) includes numerical integration of diagnostic fluxes. Plotting diagnostics use a slightly different carbonate evaluation; the audit uses the solver's own law.'''))
c.append(code('''# Understand and run: state loading, integration and all audits are supplied.
M.read_state(directory=str(STATE))
run_model(M)
postprocess_carbonate_horizons(M)
budget_report = audit_complete_model(M)
drift_report = pd.DataFrame(audit_restart_drift(M)).set_index('State')
assert (M.D_b.zsat.c <= M.D_b.zcc.c).all()
display(drift_report)
print('Graph and PIC coupling checked; carbon/TA budgets close; short restart drift is within the stated limits.')
print({key: value for key, value in budget_report.items() if 'error' in key})'''))
c.append(md(q('explain the evidence', '''Name one error that the graph check could detect despite passing conservation, and distinguish the short restart check from independent scientific validation. In your results, identify one state, one chemistry diagnostic and one flux. Use this explanation rather than another final report.''')+'\n\n'+answer('''A conservative but misdirected internal arrow may pass a global budget; the graph comparison can detect it. Small restart drift supports local consistency between the reconstructed equations and archived state. It does not prove long-term stability or observational validity. DIC is a state, pH a chemistry diagnostic, and dissolution a calculated flux. The sediment snowline is another evolving state, not a carbonate-ion diagnostic.''')))
c.append(code(old3.cells[36].source,metadata={'tags':['solution-only']}))
c.append(md('''**You have completed 03.** Keep the reconstructed diagram, flux table, four mappings and budget explanation. Reuse the diagram in 04. Detailed sediments and process attribution remain optional.'''))
nb3=nbf.v4.new_notebook(cells=c,metadata=old3.metadata)

# 04 retains the exact case construction, amplitudes and integration.
c=[]
c.append(md('''# 04 — Design and interpret carbon and alkalinity experiments

**Learning goals:** specify matched experiments; map external inputs; use budget-checked anomalies to explain mechanisms, timing and limits.

**Provisional time: 40 minutes.** Prediction/specification (5), two forcing tasks (10), supplied runs/checks (10), four short answers (15). Three cases are run: control, OA and OAE. All plotting and numerical machinery are supplied.
[Teaching goals](../../TEACHING_GOALS.md).

'''+KEY))
c.append(code(old4.cells[1].source))
c.append(md('''## A1. Reuse the model specification from 03

Your completed schematic is the experiment map. Add only the external carbon or TA arrow; identify the outputs you will examine. The workbook owns the same geometry, box-specific T/S/P, transport and baseline rates. Each case gets an independent parameter copy and the same archived stationary state. Workbook initial concentrations are replaced by that restart.

The supplied `build_complete_case` below returns a fresh, unrun model. After changing a forcing choice, rerun its definition and all subsequent case/run cells. Changes to baseline geometry, chemistry or process rates require a fresh compatible stationary control.

POC/PIC export remains fixed. Weathering, gas exchange and state-dependent dissolution/burial remain active. The atmospheric reservoir is finite. Ocean acidification (OA) here is driven by atmospheric carbon input; idealized ocean alkalinity enhancement (OAE) adds surface TA with no direct carbon input.

Keep these prescribed inputs: OA uses the archived IS92a-shaped forcing (scale 0.877, no terrestrial uptake), while OAE uses the same shape/timing at a different amplitude. Runs last 3800 model years with a one-month maximum step. These choices reproduce a benchmark and test a specified intervention; they are not present-day forecasts.'''))
c.append(md(q('specify and predict before running',r'''Complete the entry-species/receiving-state fields through Exercise 04.2 below and your diagram. State what must match the control. Predict the sign of atm CO2 and surface pH anomalies in OA and OAE; identify a diagnostic whose opposite sign would challenge your prediction. Revisit this prediction in your four final answers.

| Case | External input after year 1800 | Entry species / receiving state | Initial state and baseline |
| --- | --- | --- | --- |
| Control | None | No forcing connection | Archived restart; fixed benchmark parameters |
| OA | About 4025 Gt C | Your diagram and code choice | Same as control |
| OAE | 10 Pmol TA equivalents | Your diagram and code choice | Same as control |

The whole-run forcing includes a small pre-1800 tail. The supplied audit reports both intervals. The amounts and units differ, so raw OA/OAE curves do not compare equal-strength interventions.''')+'\n\n'+answer('''OA adds carbon to atmospheric CO2; OAE adds TA to low-latitude surface TA. Match geometry, chemistry, baseline rates, clock and restart with the control. Expected early OA anomalies are positive atm CO2 and negative surface pH; OAE is expected to give negative atm CO2 and positive surface pH. Opposite sustained anomalies in those diagnostics would require checking the choices and revisiting the explanation.''')))
c.append(md('''<details>
<summary>Optional reference — inspect the shared workbook again</summary>

The following function displays input records only if you call it. The core uses the specification you already inspected in 03. Numerical baseline inputs stay in `model_definition.xlsx`.

</details>'''))
c.append(code('''# Supplied implementation: optional lookup, not another required table-reading task.
def show_input_reference():
    display(pd.DataFrame(input_tables['OceanReservoirs']).set_index('Box ID'))
    display(pd.DataFrame(input_tables['Atmosphere']).set_index('Box ID'))
    display(pd.DataFrame(input_tables['TransportConnections']).sort_values('Order'))
    display(pd.DataFrame(input_tables['GasExchangeConnections']).sort_values('Order'))
    display(pd.DataFrame(input_tables['ProcessParameters']).set_index('Parameter'))
# To inspect the tables again, run show_input_reference().'''))
c.append(md(old4.cells[5].source.replace('## 3.', '## A2.')))
c.append(code(old4.cells[6].source))
c.append(md('''## A3. Exercise 04.2: map the external arrows

'''+q('implement the experiment specification', '''Inside each branch, assign `forcing_species` and `forcing_target` from your diagram. Choose from the model's CO2 and TA species and its atmospheric CO2 or low-latitude surface TA state. No pH is imposed; it is calculated from the evolving state.

`Source` represents material outside the boundary. `Signal` supplies a time-dependent flux; the native connection attaches it to the chosen state. The control has no such connection. Constructor syntax, waveform scaling and the numerical audit are supplied.''')))
c.append(code(old4.cells[8].source))
c.append(md(r'''## B1. Verify inputs and the boundary budget

In 03, internal water, gas and POC transfers cancel when summing inventories. Including external carbon $I_C(t)$ and TA $I_A(t)$ gives
$$\frac{dC_{atm+ocn}}{dt}=I_C(t)+W_C-B_{net}(t),\qquad
\frac{dA_{ocn}}{dt}=I_A(t)+W_A-2B_{net}(t).$$
These are boundary-aware budgets, not constant-inventory tests. Net burial may change in response to forcing. Pure-TA OAE sets $I_C=0$; distinguish direct external carbon input from internal air–sea redistribution.

The supplied code checks forcing units and integrated amounts before integration, then evaluates the same carbonate flux law used by the solver to audit all saved times. Small tolerance also covers numerical quadrature of the diagnostic flux history. Inspect budget errors before interpreting responses.'''))
c.append(code(old4.cells[10].source))
c.append(md(r'''## B2. Start with matched responses

For each quantity use
$$\Delta Y(t)=Y_{forced}(t)-Y_{control}(t).$$
This compares the imposed forcing against the same baseline evolution, including control drift. It isolates the response within this deterministic model; subtraction does not eliminate numerical errors or validate omitted processes.

Read four diagnostic groups: atm CO2, surface pH, deep DIC and dissolution/net burial. Compare signs and timing against your initial prediction. Read units and scales: these unequal forcing amounts do not establish relative intervention efficiency.'''))
c.append(code(old4.cells[15].source+'\nplt.show()'))
c.append(md('''## B3. Use the complete figures for pathways and sediment memory

The supplied plots below use the same integrated cases. Solid curves are the model; OA's dotted curves reproduce the archived published comparison. That overlay checks reproduction, while matched anomalies address the forcing response.

| Panel | Diagnostic | Use |
| --- | --- | --- |
| g | External carbon or TA input | Prescribed cause, with distinct units |
| f / c | atm CO2 / pH | Check your predicted atmosphere/surface response |
| a / b / d | DIC / TA / gas exchange | Trace transfer and redistribution |
| e / h | Horizons / dissolution and burial | Examine deep chemistry and sediment history |

The **saturation horizon** has calcite saturation = 1; the **compensation depth** concerns complete dissolution of modern rain; the **snowline** is the boundary of existing reactive sediment. The first two respond to current chemistry/rain, while snowline motion retains history. Plot e uses negative depth (elevation), so upward means shallower.

Consult e/h for the sediment answer and the OA overlay for reproduction. There is no extra panel-by-panel report. The final plotted time need not be a new equilibrium.'''))
c.append(code(old4.cells[12].source))
c.append(code(old4.cells[13].source))
c.append(md('''## C. Explain the experiment in four short answers

'''+q('evidence, mechanisms and next test', '''1. **Design and evidence:** identify the entry species/state in each case and what matches the control. Use the atm/surface anomalies to assess your prediction. Why can comparison with the initial state alone be misleading if the control drifts?
2. **Mechanism and budget:** explain how TA input changes atmospheric CO2 without directly supplying carbon. Trace the internal transfer and use the boundary budget. Why are these experiments neither opposite nor equal-strength inputs?
3. **Time and process:** identify a surface/deep response lag and use e/h to explain the linked 1 DIC : 2 TA transfers and sediment memory. What evidence would you need before claiming equilibration?
4. **Claims and next test:** distinguish benchmark reproduction from a conditional prediction. Choose one fixed assumption and propose one changed input, matched control and diagnostic for a follow-up test. One or two sentences are enough; do not run a fourth case in the core.''')+'\n\n'+answer(r'''1. OA enters `CO2_At` as CO2 and OAE enters `L_b.TA` as TA. Geometry, chemistry, rates, clock and restart match the control. The anomalies show positive atm CO2/negative surface pH for OA and the opposite initial tendency for OAE. Forced-minus-initial includes baseline evolution; forced-minus-control removes that shared drift.
2. TA changes carbonate partitioning and aqueous CO2, inducing internal atmospheric-to-ocean transfer. No carbon enters directly through the TA connection. The total active carbon can still differ from control because net burial responds. The cases differ in species, amount and nonlinear chemical/sediment response; opposite signs do not imply cancellation or comparable efficiency.
3. Surface chemistry responds before the transported deep signal. Carbonate dissolution returns 1 DIC and 2 TA, while net burial removes them. OA tends to increase dissolution/reduce burial; OAE tends to oppose this, modifying the forcing response. Chemical horizons respond to current conditions while the snowline can lag. Small sustained tendencies and balanced fluxes over a sufficiently long interval would support stationarity; the last plotted point alone does not.
4. The OA overlay checks reproduction of a published model, not independent observational validation. The forcing response is conditional on assumptions. For example, compare two temporal shapes with equal integrated TA using the same unforced control and measure the atm CO2 anomaly at a stated time. Or test a state-dependent export hypothesis against a fixed-export control, first preparing compatible stationary baselines and retaining PIC stoichiometry.''')+'''

**You have completed 04.** Keep the forcing choices, checked budgets and four explanations in this notebook. The [independent-model starter](extensions/05_independent_model.ipynb) and [attribution/feedback extension](extensions/04_attribution_and_feedbacks.ipynb) are optional work outside the core.'''))
nb4=nbf.v4.new_notebook(cells=c,metadata=old4.metadata)

for name, nb in [('03_boudreau_three_box_model.ipynb',nb3),('04_pump_strength_OA_OAE.ipynb',nb4)]:
    # Correct raw-string authoring escapes once, keeping dollar math delimiters.
    for cell in nb.cells:
        if cell.cell_type=='markdown':
            cell.source=cell.source.replace('\\\\','\\')
    nbf.validate(nb)
    source=ROOT/'notebooks/instructor'/name
    nbf.write(nb,source)
    build_student_notebook(source,ROOT/'notebooks/student'/name)
    print(name,len(nb.cells),'cells')

# A separate optional starter: the instructor example is one valid design,
# not a unique scientific answer or a required core experiment.
c=[]
c.append(md('''# Optional — Build and test one model change

**Outside the four-hour core. Provisional time: 60–90 minutes, to be piloted.**
Use this starter after 02–04 to practise specifying your own small experiment.
Choose one question, draw its boxes/arrows, write the changed equation with units,
run a matched comparison and interpret one figure with conservation evidence.

The supplied starting model is 02's transparent two-layer construction, including
its ratio-derived teaching geometry and explicit mass-based transport. It has
no sediment or weathering boundary. This is a teaching model, not a calibrated
research configuration. Copy the notebook to develop your own design; keep the
course inputs intact.

Code labelled **Choose and explain** contains your decisions; repeated model
construction, integration, plotting and audit code are supplied. Blue questions
mark student work, purple instructor panels give one possible design.
Keep explanations in this ungraded notebook. No separate report is needed.'''))
c.append(md(q('specify one testable change',r'''Choose a bounded question, for example:

- Does fixed versus first-order carbon export produce a different transient when
  both exports agree at a stated reference concentration?
- Does changing the duration of the same finite carbon input change peak CO2
  and its timing? For this option reuse 02's supplied pulse/clock machinery.

State your hypothesis and a result that would challenge it. Draw the modified
arrow, write its equation and units, identify the control, and choose one response
metric and comparison time. Separate prescribed inputs from outputs and explain
which carbon/TA terms cancel. Change one scientific assumption at a time.

The code below supports the export-law option. You may adapt it for your chosen
question. Its matched cases start from the same initial state, not a stationary
restart; do not interpret their early adjustment as a perturbation of equilibrium.''')+'\n\n'+answer(r'''Example: compare fixed export P0 with first-order export k DIC_s(t), choosing
k = P0 / DIC_ref so their initial fluxes agree when DIC_s(0) = DIC_ref.
Both conserve the same carbon and TA because export is an internal DIC transfer.
Hypothesis: as surface DIC falls, the first-order flux weakens relative to fixed
export, producing a less pronounced atmospheric drawdown. Compare atmospheric
CO2 at 1000 years and inspect the difference over the full trajectory.
Use identical initial DIC/TA, geometry, chemistry, circulation and clocks.
This tests the chosen closure inside the model, not whether biology follows it.''')))
c.append(code('''# Supplied implementation: environment and reusable two-layer construction.
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ROOT = next(p for p in (Path.cwd().resolve(), *Path.cwd().resolve().parents)
            if (p / 'teaching_config.py').is_file())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from esbmtk import Species2Species
from teaching_config import TEACHING as config
from simple_models import two_layer, audit, box_mass_kg
from model import run_model'''))
c.append(md(q('choose inputs and implement your changed arrow',r'''Choose a positive hypothetical reference export and reference concentration,
giving their units and provenance. These are experiment choices, not observations.
Set `reference_export_mol_yr`, `reference_dic_umol_kg`, `comparison_year`,
`run_stop` and `max_timestep`. The reference and changed case use the same values.

Complete the two native connections inside `build_case`. For the export-law option,
both transfer DIC from Surface to Deep; use a fixed amount/time for the reference
and derive the concentration coefficient for the changed case. Concentrations in
the native law are mol/kg, not µmol/kg. Keep the kernel's class signature/documentation
available; syntax memorisation is not the objective.''')))
c.append(code('''# Choose and explain: one possible instructor design is masked for students.
# BEGIN SOLUTION
reference_export_mol_yr = 120e12  # Hypothetical experiment input, mol C/yr.
reference_dic_umol_kg = 2000.0   # Hypothetical common starting concentration.
comparison_year = 1000.0
run_stop, max_timestep = '30 kyr', '20 yr'
# END SOLUTION

def build_case(kind):
    model = two_layer(initial_dic_umol_kg=reference_dic_umol_kg, k_kg_yr=0.0,
                      stop=run_stop, max_timestep=max_timestep, config=config)
    # The helper supplies water/gas arrows and inferred TA; add your one change.
    # BEGIN SOLUTION
    if kind == 'reference':
        model.export_connection = Species2Species(
            source=model.Surface.DIC, sink=model.Deep.DIC,
            ctype='regular', rate=f'{reference_export_mol_yr} mol/yr', id='export')
    elif kind == 'changed':
        k_kg_yr = reference_export_mol_yr / (reference_dic_umol_kg * 1e-6)
        model.export_connection = Species2Species(
            source=model.Surface.DIC, sink=model.Deep.DIC,
            ctype='scale_with_concentration', scale=k_kg_yr, id='export')
    else:
        raise ValueError(kind)
    # END SOLUTION
    return model

cases = {kind: build_case(kind) for kind in ('reference', 'changed')}'''))
c.append(md('''The supplied checks require matching initial carbon/TA and clocks. They audit
each run, not just the difference between runs. If you choose a boundary forcing,
adapt the expected inventory using the integrated input as in 02; do not disable
the conservation test. These checks cannot decide whether the chosen closure is
scientifically adequate.'''))
c.append(code('''# Understand and run: supplied execution, budgets, metric and figure.
np.testing.assert_allclose(cases['reference'].time, cases['changed'].time)
def initial_inventory(case):
    # Before integration, native array lengths need not yet match; use scalars.
    carbon = case.CO2_At.c[0] * case.CO2_At.reservoir_mass.to('mol').magnitude
    ta = 0.0
    for box in case.ocean_boxes:
        carbon += box_mass_kg(box) * box.DIC.c[0]
        ta += box_mass_kg(box) * box.TA.c[0]
    return carbon, ta
np.testing.assert_allclose(initial_inventory(cases['reference']),
                           initial_inventory(cases['changed']), rtol=1e-12)
reports = {}
for name, case in cases.items():
    run_model(case)
    reports[name] = audit(case)
display(pd.DataFrame(reports).T)
ref, changed = cases['reference'], cases['changed']
if not ref.time[0] <= comparison_year <= ref.time[-1]:
    raise ValueError('Comparison time must lie inside the run')
delta = (changed.CO2_At.c - ref.CO2_At.c) * 1e6
print('Changed minus reference at', comparison_year, 'yr:',
      float(np.interp(comparison_year, ref.time, delta)), 'ppm')
fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
for name, case in cases.items():
    axes[0].plot(case.time, case.CO2_At.c * 1e6, label=name)
axes[0].set_ylabel('atm CO2 (ppm)')
axes[0].legend()
axes[1].plot(ref.time, delta)
axes[1].axhline(0, color='gray', ls='--')
axes[1].set(xlabel='Time (yr)', ylabel='Changed - reference (ppm)')
fig.tight_layout()
plt.show()'''))
c.append(md(q('interpret and identify the next evidence needed', '''Use your chosen metric and one feature of the figure to assess the hypothesis.
Explain the controlling flux balance and one limitation. Distinguish transient
adjustment from an established stationary response. Name an independent observation
or constraint that would help evaluate the closure, and one sensitivity or numerical
resolution check needed before a research claim. You need not run a large parameter
sweep in this starter.''')+'\n\n'+answer('''For the supplied example the changed case has a higher atmospheric CO2 after
the initial adjustment because its export weakens as surface DIC decreases.
Both conserve total carbon/TA, so the atmospheric difference is redistribution.
The fixed export is not limited by nutrients and can become unrealistic outside
this tested range. Compare export observations with compatible depths and units
independently of any fitted concentration target. Test numerical resolution and
the reference flux/concentration choice before interpreting a general biological
effect. A plot ending at 30 kyr alone is not proof of stationarity.''')+'''

**Keep the experiment specification with the code and figure.** ESM research will
also require spatial diagnostics, uncertainty and internal-variability/ensemble
analysis; this deterministic comparison is a starting exercise.'''))
ext=nbf.v4.new_notebook(cells=c,metadata=old3.metadata)
extname='extensions/05_independent_model.ipynb'
nbf.write(ext,ROOT/'notebooks/instructor'/extname)
build_student_notebook(ROOT/'notebooks/instructor'/extname,ROOT/'notebooks/student'/extname)
