from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

protected = [p for folder in ('notebooks', 'archive', 'data', 'ref/figures', 'outputs/03_04_flux_specification')
             for p in (ROOT/folder).rglob('*')
             if p.is_file() and not p.name.startswith('~$') and p.suffix != '.log']
(OUT/'protected.json').write_text(json.dumps({str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}, indent=2))
p = ROOT/'notebooks/instructor/03_boudreau_three_box_model.ipynb'
nb = json.loads(p.read_text(encoding='utf-8'))
cells = {c['id']: c for c in nb['cells']}
def get(id): return ''.join(cells[id]['source'])
def put(id, value): cells[id]['source'] = value.splitlines(keepends=True)
def replace(id, old, new):
    s = get(id)
    assert old in s, (id, old)
    put(id, s.replace(old, new))

replace('e20cf049', 'distinguish graph, budget and restart checks.', 'check the connections, whole-system budgets and a saved starting state.')
replace('5998b397', '| Reference state | Calibrated constraints | Archived benchmark restart |', '| Reference state | Calibrated constraints | Saved values from a long benchmark run |')
replace('5998b397', 'POC and PIC mean', '''A **model state** is the set of current values that the model evolves: here, ocn DIC/TA, atm CO2 and sediment snowline, along with auxiliary chemistry values. A **restart** uses saved values from an earlier run as the starting state of a new run. In C3 we will load a supplied state from a long benchmark run, then check that your reconstructed model changes little over 20 years. This avoids repeating the long calculation in class.

POC and PIC mean''')
replace('e1e283a3', '**Initial concentrations are replaced by the archived restart later.** Geometry and rates are retained.', '**The workbook concentrations initialize construction; C3 replaces them with the saved starting values.** Geometry, thermodynamic settings and process parameters stay the same.')
replace('e1e283a3', ' Optional feedback settings are omitted from this view.', '')
replace('03-carbonate-plane-reading', 'Keep only actual state dependencies; mark each row **fixed**, **state-dependent**, or **residual** beside its process ID.', "Beside each row, note which changing model values affect its rate; write **fixed** for a prescribed constant rate. For net burial, identify the two fluxes being compared.")
replace('03-flux-hints', 'Here $d$ means D_b, $z_{snow}$ is the snowline, and $\\alpha,z_0$ are workbook sediment parameters. This states the dependencies; the sediment equations and their code are supplied.', 'Here $d$ means D_b, $z_{snow}$ is the snowline, and $\\alpha,z_0$ are workbook sediment parameters. The function lists the inputs used to calculate dissolution; its equations and code are supplied.')
replace('03-flux-hints', 'Constant parameters do not imply constant fluxes: 02\'s export depended on $DIC_s(t)$ even with fixed $k$. Here both exports are fixed, but gas exchange and dissolution still respond to state. Additional pump feedbacks remain optional.', 'A constant coefficient does not imply a constant flux: in 02, $kDIC_s(t)$ scales with surface DIC even when $k$ stays fixed. Gas exchange and dissolution also respond to changing model values, but use their own calculations rather than simple scaling with source concentration.')
replace('03-flux-hints', 'Assumption notes: biology, weathering and fixed rates', 'Reference: biological TA effects, weathering and flux laws')
replace('0b59718c', 'The completed equations are tabulated below. POC, PIC and weathering are fixed; water-tracer transport, gas exchange and dissolution depend on state; net burial is a signed residual.', 'The completed equations are tabulated below. POC, PIC and weathering rates are fixed. Water-tracer fluxes scale with source concentration. Gas exchange uses atm CO2 and aqueous CO2; dissolution uses export, deep chemistry and snowline. Net burial is the difference between carbonate export and dissolution.')
replace('0b59718c', '\nThe paired carbonate fluxes give an aggregate active-system loss of $B_{net}$ carbon and $2B_{net}$ TA. Negative net burial returns old sediment. Do not apply a separate burial sink after PIC export and dissolution.\n', '')
replace('9f31685f', '**not the later stationary restart**', '**not the saved starting state loaded in C3**')
replace('120d2b39', 'requires a new compatible stationary state.', 'requires another long equilibration run to prepare compatible starting values.')
replace('72dd4cbb', 'A physical correction requires a separately tested baseline and fresh restart.', 'Changing that conversion requires retesting the baseline and preparing compatible saved starting values.')
replace('72dd4cbb', '| `scale_with_concentration` | coefficient × source concentration | `sc` |', '| `scale_with_concentration` | coefficient × current source concentration | `sc` |')
replace('72dd4cbb', '\n<div style=', '''
`scale_with_concentration` names a specific proportional law. Saying a flux depends on changing model values is broader: `gasexchange` uses both atm and ocn CO2, and the supplied dissolution calculation also uses sediment history. These are different calculations, even though their fluxes can all change during a run.

<div style=''',)
replace('e49abe16', '## C1. Check the graph before integrating', '## C1. Check the connections before running the model')
replace('e49abe16', 'The supplied structural check', 'The **connection graph** is the collection of boxes and connections you built. The supplied graph check')

blue = '<div style="background-color: #edf5ff; color: #173b61; border-left: 4px solid #3977b8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">'
purple = '<div style="background-color: #f3eefb; color: #38224f; border-left: 4px solid #7952a8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">'
put('9d724902', r'''## C2. Account for carbon and TA crossing the boundary

Use the **active atm–ocn boundary** drawn in A3: it encloses the atm and the three dissolved ocn inventories. The carbonate/sediment module is outside this inventory sum. For fixed box water masses $m_i$ and atmospheric air amount $N_{atm}$,

$$C_{atm+ocn}(t)=N_{atm}x_{CO2}(t)+\sum_i m_iDIC_i(t),\qquad
A_{ocn}(t)=\sum_i m_iTA_i(t).$$

$C_{atm+ocn}$ is carbon in mol C; $A_{ocn}$ is the TA inventory in equivalents. Here $x_{CO2}$ is the dry-air mole fraction, not ppm. TA has no atmospheric inventory.

Reuse A3's symbols: weathering supplies $W_0$ mol C/yr and $2W_0$ equivalents/yr; $E(t)$ is carbonate export and $D(t)$ is dissolution, both in mol C/yr. Follow their arrows across the boundary. There is **no experimental CO2 or TA addition** in this run, but weathering continues.

'''+blue+r'''

**Question — build the whole-system budget**

1. When you add the box inventories, why do water transport, gas exchange and POC export/remineralization make no net contribution?
2. Write $dC_{atm+ocn}/dt$ and $dA_{ocn}/dt$ as **inputs minus outputs**, using $W_0$, $E(t)$ and $D(t)$. Use the paired DIC/TA effects from your flux table.
3. Define $B_{net}(t)$ as carbonate export minus dissolution and rewrite both balances using it. Why would subtracting a further burial flux count the same loss twice?

</div>

<!-- BEGIN SOLUTION -->
'''+purple+r'''

**Instructor answer**

**1. Internal transfers cancel.** Each water or gas transfer removes carbon from one included box and adds the same amount to another. Water also transfers TA internally; gas exchange carries no TA. The model's POC transfer removes surface DIC and returns all of it as deep DIC through remineralization, with no TA effect.

**2. Add boundary inputs and subtract boundary outputs.** Weathering and dissolution enter the dissolved inventories; carbonate export leaves them:

$$\frac{dC_{atm+ocn}}{dt}=W_0+D(t)-E(t),$$
$$\frac{dA_{ocn}}{dt}=2W_0+2D(t)-2E(t).$$

The factor two follows the model's weathering and carbonate stoichiometry: two TA equivalents per mole C. The two balance equations therefore have different units, mol C/yr and equivalents/yr.

**3. Combine the carbonate terms once.** With $B_{net}(t)=E(t)-D(t)$,

$$\frac{dC_{atm+ocn}}{dt}=W_0-B_{net}(t),\qquad
\frac{dA_{ocn}}{dt}=2W_0-2B_{net}(t).$$

These are the same balances with the carbonate terms grouped. A further burial sink would repeat the loss already included through export minus dissolution. If dissolution exceeds export, $B_{net}<0$: old sediment supplies a net return to the dissolved inventories.

The inventories are constant only when weathering and net burial balance. A passing budget check means that inventory changes match the boundary fluxes; it does not require those changes to be zero.

</div>
<!-- END SOLUTION -->
''')
replace('d69c9b4d', '## C3. Load the reference state and check the short restart\n\nThe archived state avoids the million-year spin-up in class. It supplies state, not connections: your graph determines subsequent tendencies.', '''## C3. Load the saved state and check the next 20 years

`M.read_state(...)` loads the supplied saved values as this run's initial values: this is the **restart** introduced in A1. They come from a long benchmark run continued until changes were small (a nearly stationary state). Loading them does not create or repair connections; the equations you built determine what happens next.''')
replace('d69c9b4d', 'Run 20 unforced years.', 'Run 20 years with the existing weathering and export rates and no experimental addition.')
replace('e5ef09ef', 'distinguish the short restart check from independent scientific validation.', 'explain what little change over these 20 years establishes and what it cannot establish about the real ocean.')
replace('e5ef09ef', 'Small restart drift supports local consistency between the reconstructed equations and archived state.', 'Little change over 20 years supports consistency between the reconstructed equations and the saved starting values over that interval.')
replace('baa7b2df', ' Detailed sediments and process attribution remain optional.', '')

p.write_text(json.dumps(nb, indent=1, ensure_ascii=False)+'\n', encoding='utf-8')
build_student_notebook(p, ROOT/'notebooks/student'/p.name)
print('Revised 03 explanations, flux terminology and C2; regenerated student copy.')
