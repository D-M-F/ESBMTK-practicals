from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

protected = [p for folder in ('notebooks', 'archive', 'data', 'ref/figures', 'outputs/03_04_flux_specification')
             for p in (ROOT / folder).rglob('*') if p.is_file() and not p.name.startswith('~$')]
(OUT / 'protected.json').write_text(json.dumps({str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                               for p in protected}, indent=2))
path = ROOT / 'notebooks/instructor/03_boudreau_three_box_model.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
cells = {c['id']: c for c in nb['cells']}
def get(id):
    return ''.join(cells[id]['source'])
def put(id, text):
    cells[id]['source'] = text.splitlines(keepends=True)
def replace(id, old, new):
    text = get(id)
    assert old in text, (id, old)
    put(id, text.replace(old, new))

replace('e20cf049', ' Use 4–6 minutes of reconstruction/export discussion for interpreting the paired fluxes on the contour plot. This allocation needs a student pilot; if it does not fit, plan 60 minutes or make contour interpretation optional, without taking time from 00.', '')
replace('e20cf049', 'The construction below does not call the complete-model helper.\n[Teaching goals](../../TEACHING_GOALS.md).', '[Teaching goals and instructor timing notes](../../TEACHING_GOALS.md).')
replace('8df51381', 'Its snowline is a memory state; it has no explicit sediment-carbon inventory.', 'The **snowline** is the deepest boundary of existing reactive carbonate sediment. It records sediment history; the module has no explicit sediment-carbon inventory.')

old = get('03-carbonate-plane-reading')
notation = old[old.index('Use <mark'):old.index('Here $p_i$')]
table = old[old.index('| Process | Arrow |'):old.index('\n\nFor any internal dissolved transfer')]
notes = old[old.index('<details>'):].strip()
notes = notes.replace('The DIC-only POC closure omits nutrient/redox effects on TA.', 'The POC assumption omits nutrient/redox effects on TA.')
panel_open = '<div style="background-color: #edf5ff; color: #173b61; border-left: 4px solid #3977b8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">'
def question(label, text):
    return f'{panel_open}\n\n**Question — {label}**\n\n{text}\n\n</div>'

step1 = '''## A3. Exercise 03.1: write the paired fluxes and label the diagram

### Step 1 — Write the paired fluxes

'''+question('equations on arrows', 'Complete both flux columns, including zero effects. Use one family expression for repeated water/gas arrows. Keep only actual state dependencies; mark each row **fixed**, **state-dependent**, or **residual** beside its process ID.')+'''

Use the notation and supplied hints below. Fill the table here or in the [student Excel worksheet](../../outputs/03_04_flux_specification/student.xlsx), whose amber fields are answer spaces. Write symbolic equations, not Excel calculation formulas.
'''
symbols = '''#### Notation

'''+notation+'''Here $p_i$ is water pressure; $pCO_{2,atm}$ is atmospheric CO2 partial pressure.
**Transport convention:** use physical $\\rho Q$ for these equations; B2 explains the historical unit conversion retained in the benchmark code.
'''
hints = r'''#### Supplied hints and flux table

For gas exchange, chemistry supplies aqueous CO2:

$$c_i(t)=\mathcal C(DIC_i(t),TA_i(t);T_i,S_i,p_i).$$

Use area $A_i$ [m²] and velocity $v_i$ [m/yr]. Invasion uses $K_{0,i}pCO_{2,atm}(t)$; outgassing uses $c_i(t)$, both in mol/m³. Local solubility $K_{0,i}$ converts partial pressure to concentration. Form the two directional transfers before taking their difference. Supplied chemistry handles mol/kg and dry-air mole-fraction conversions.

For dissolution, **use this supplied dependency function**:

$$D(t)=\mathcal D\!\left(E(t),DIC_d(t),TA_d(t),z_{snow}(t);T_d,S_d,p_d,\alpha,z_0\right).$$

Here $d$ means D_b, $z_{snow}$ is the snowline, and $\alpha,z_0$ are workbook sediment parameters. This states the dependencies; the sediment equations and their code are supplied.

In this model, POC export changes DIC but leaves TA unchanged (the **DIC-only closure** in the table).

'''+table+'\n\n'+notes+'\n'
step2 = '''### Step 2 — Label the diagram

'''+question('label the diagram', 'Draw and label the arrows with these expressions. Add states and the active atm–ocn boundary; distinguish chemistry diagnostics and sediment memory. Check water balance at H_b.')+r'''

Label water arrows with $Q$: circulation $Q_{LH},Q_{HD},Q_{DL}$ and mixing $Q_{mix,down},Q_{mix,up}$. The paired $J$ equations describe the tracers they carry. F1–F8 remain paper aliases. Net burial is the signed amount left after dissolution, not an additional drain from deep water.

![Box outlines for reconstruction](../../ref/figures/03_04_boudreau_student.png)
'''
step3 = r'''### Step 3 — Check one internal transfer

For any internal dissolved transfer of $X=DIC$ or $TA$, **flux and concentration tendency differ**:

$$\left.\frac{dX_i}{dt}\right|_{i\to j}=-\frac{J^X_{ij}(t)}{m_i},\qquad
\left.\frac{dX_j}{dt}\right|_{i\to j}=+\frac{J^X_{ij}(t)}{m_j}.$$

'''+question('check inventory cancellation', 'For one internal arrow, use the supplied tendency rule above to show equal-and-opposite inventory changes. Do not rewrite the effects in prose.')+'\n'
put('03-carbonate-plane-reading', step1)
idx = nb['cells'].index(cells['03-carbonate-plane-reading']) + 1
for id, text in reversed(list(zip(('03-flux-notation', '03-flux-hints', '03-label-diagram', '03-internal-transfer'), (symbols, hints, step2, step3)))):
    nb['cells'].insert(idx, {'cell_type': 'markdown', 'id': id, 'metadata': {}, 'source': text.splitlines(keepends=True)})

a4 = get('120d2b39')
mapping = a4[a4.index('| Diagram content |'):a4.index('\n\nThe [flux worksheets]')]
put('120d2b39', '''### A4. Reconcile your drawing with Excel

Compare the water and gas connection rows below with your arrows. Identify water routes by **source + sink + flux_id**: all three circulation rows use `thc`, so that ID alone is not unique. Check boundary-node names and correct your diagram before construction. `Fb` declares a boundary node; it does not add a separate burial drain.

The loader validates names, units and water balance, then creates parameter records. You will create the reservoirs and connections in B1–B4.

<details>
<summary>Optional reference: workbook-to-code links</summary>

'''+mapping+'''

The [flux worksheets](../../ref/boudreau_diagrams.md) are teaching documentation, not live model inputs. POC/PIC/weathering topology and sediment coupling are supplied Python patterns. Changing baseline geometry, chemistry or rates requires a new compatible stationary state.

</details>
''')
for c in nb['cells']:
    s = ''.join(c['source'])
    if "display(pd.DataFrame(workbook_connections(WORKBOOK)).set_index('ID'))" in s:
        s = s.replace("display(pd.DataFrame(workbook_connections(WORKBOOK)).set_index('ID'))", '''# Optional lookup repeats these routes with their paper aliases.
from IPython.display import HTML
display(HTML(
    '<details><summary>Optional reference: connection cross-reference</summary>'
    + pd.DataFrame(workbook_connections(WORKBOOK)).set_index('ID').to_html()
    + '</details>'
))''')
        c['source'] = s.splitlines(keepends=True)
    elif s.startswith('from teaching_plots import plot_carbonate_process_plane'):
        c['source'] = ('# Understand and run: use the contours to interpret your paired fluxes.\n'+s).splitlines(keepends=True)

replace('b6d3e772', 'Use the POC and PIC arrows from your diagram. The native PIC connections have nominal deep endpoints but bypass those sinks; the supplied carbonate module adds the actual dissolution return later. A direct addition of all PIC to deep DIC/TA would represent a different model.', "Use the POC and PIC arrows from your diagram. The PIC connections remove material from L_b without directly adding it to D_b: `bp='sink'` bypasses the named destination. The supplied sediment module returns only the dissolved fraction to D_b.")
replace('b6d3e772', 'Compare this closure with 02:', 'Compare this export assumption with 02:')
replace('adc68f52', 'Your dissolution arrow returns material to deep dissolved inventories. `add_carbonate_system_2` supplies that coupling using the actual PIC flux object, deep chemistry and the snowline. Do not add another manual dissolution connection.', '`add_carbonate_system_2` implements your dissolution arrow using the actual PIC flux object, deep chemistry and the snowline. Run this supplied wiring; no manual dissolution connection is needed.')
replace('adc68f52', 'The saturation horizon marks calcite saturation = 1; the compensation depth concerns survival of modern rain. Both are chemistry-dependent diagnostics. The snowline retains sediment history and may lag. Dissolution can exceed current rain when old sediment dissolves, giving negative net burial. Net burial is a diagnostic boundary residual, not another deep-water drain.', 'The **saturation horizon** marks calcite saturation = 1; the **compensation depth** is where the arriving carbonate rain dissolves completely. These diagnostics respond to current chemistry. The snowline can lag because old sediment takes time to dissolve; this can make dissolution exceed current rain and net burial negative.')
b4 = get('c9101ca9')
put('c9101ca9', '''## B4. Exercise 03.5: connect the atmosphere

Map your A3 gas law to one connection per surface box. Each connection evaluates invasion minus outgassing, with equal-and-opposite atm and ocn transfers. Its endpoints define the positive direction; the net flux can reverse. Native code handles the conversions from dry-air mole fraction and mol/kg states.

Chemistry, gas exchange and circulation together produce solubility-related storage; no extra solubility-pump arrow is needed.

'''+b4[b4.index('<div'):])
c3 = get('d69c9b4d')
start = c3.index('The separate audit')
put('d69c9b4d', c3[:start]+'''The budget audit separately checks that carbon and TA inventory changes match the integrated weathering and net-burial fluxes from C2.

<details>
<summary>Technical note: numerical budget tolerance</summary>

The audit's relative tolerance (2 × 10⁻⁵ of the evolving stock, plus a small absolute allowance) includes numerical integration of diagnostic fluxes. It evaluates net burial with the solver's own law; plotting diagnostics use a slightly different carbonate evaluation.

</details>
''')
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False)+'\n', encoding='utf-8')
build_student_notebook(path, ROOT/'notebooks/student'/path.name)
print('Revised instructor 03 and regenerated student 03.')
