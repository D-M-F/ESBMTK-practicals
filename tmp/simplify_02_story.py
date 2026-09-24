import json
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

OUT = ROOT / 'tmp/02_main_story'
OUT.mkdir(exist_ok=True)
name = '02_two_layer_ocean_carbon_pump.ipynb'
path = ROOT / 'notebooks/instructor' / name
(OUT / 'before.ipynb').write_bytes(path.read_bytes())
hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
          for folder in ('notebooks', 'archive') for p in (ROOT / folder).rglob('*.ipynb')}
(OUT / 'before_hashes.json').write_text(json.dumps(hashes, indent=2))
nb = json.loads(path.read_text(encoding='utf-8'))
cells = {c['id']: c for c in nb['cells']}

def source(id):
    return ''.join(cells[id]['source'])

def put(id, text):
    c = cells[id]
    c['source'] = text.splitlines(keepends=True)
    if c['cell_type'] == 'code':
        c['outputs'] = []
        c['execution_count'] = None

put('0a022ace', source('0a022ace').replace(
    'a downward carbon transfer to maintain a DIC difference between them.',
    'a downward carbon transfer to maintain a DIC difference between them.\n'
    'Follow three steps: **divide the ocean → maintain a gradient → supply the\n'
    'carbon needed for the full reference state**.'))

put('02-pump-budgets', r'''### B2. Focus on the deep-box balance

For the next derivation, use **deep-box inputs minus outputs**. Let $m_d$ be
the fixed deep-water mass in kg. Multiplying its DIC concentration tendency
by $m_d$ gives the inventory tendency in mol C/yr:

$$m_d\frac{dDIC_d(t)}{dt}=
J_{mix,down}(t)+J_{pump}(t)-J_{mix,up}(t).$$

The pump enters the deep box; mixing carries carbon both downwards and upwards.
The <mark style="background-color: #fff0b3; color: #513d00; padding: 0.05em 0.2em; border-radius: 3px;"><strong>net upward mixing</strong></mark>
shown in the plot is the difference of those two mixing arrows:

$$J_{mix}(t)=J_{mix,up}(t)-J_{mix,down}(t)
=Q\rho[DIC_d(t)-DIC_s(t)].$$

<details>
<summary>Reference — complete carbon and TA budgets</summary>

Let $m_s$ be surface-water mass and $C_{atm}$ atmospheric carbon in mol C.
The other two carbon budgets are

$$m_s\frac{dDIC_s(t)}{dt}=
J_{gas,in}(t)+J_{mix,up}(t)-J_{gas,out}(t)-J_{mix,down}(t)-J_{pump}(t),$$
$$\frac{dC_{atm}(t)}{dt}=J_{gas,out}(t)-J_{gas,in}(t).$$

Adding all three budgets cancels every internal carbon transfer. The pump
leaves the surface and enters the deep box at the same rate. For TA, the
surface budget is $J_{mix,up}^{(TA)}(t)-J_{mix,down}^{(TA)}(t)$ and the deep
budget is its opposite; gas exchange and this pump have no TA terms.

</details>
''')

t = source('02-pump-derivation')
t = t.replace('Determine the units of $k$; is it simply\n   an inverse-time rate constant when DIC is expressed in mol/kg?',
              'Determine the units of $k$ when DIC is expressed in mol/kg.')
t = t.replace('transport of 20 Sv. Which\n   combination of $k$, $Q$ and $\\rho$ does the DIC ratio constrain?',
              'transport of 20 Sv.')
t = t.replace('ratio. The output uses Tmol C/yr for export and Pmol C for inventories:\n1 Tmol = $10^{12}$ mol and 1 Pmol = $10^{15}$ mol.',
              'ratio. The flux plot uses Tmol C/yr, where 1 Tmol = $10^{12}$ mol.')
a = t.index('$k$ has units kg/yr')
b = t.index('\n</div>', a)
t = t[:a] + r'''$k$ has units kg/yr so that $kDIC_s(t)$ is mol/yr. Convert 20 Sv to m3/yr
before multiplying by ESBMTK density. With the defaults,
$k \simeq 6.6644\times10^{16}$ kg/yr. In 02.3, use the concentration-dependent
law with surface DIC as source, deep DIC as sink and $k$ as its scale.

**Instructor note.** The observed DIC ratio constrains $k/(Q\rho)$, rather
than $k$ and $Q$ individually. The inverse-time coefficient for the surface
concentration tendency would be $k/m_s$; neither point is a separate task.
''' + t[b:]
put('02-pump-derivation', t)
put('a76005d4', '\n'.join(line for line in source('a76005d4').splitlines()
                         if "print('Export at reference" not in line) + '\n')
put('02-run-pump', '''### Run the supplied pump comparison

After updating **02.3**, rerun the `build_layers` definition and the cell below.
Both runs have the same total carbon and TA; only the pump changes.
Use the figure to follow the atmospheric CO2 response and see downward pumping
balance net upward mixing. The supplied checks verify conservation, the fitted
DIC ratio and stationary flux balance.
''')
t = source('02-pump-comparison')
a = t.index('print(audit(pump_on))')
b = t.index('np.testing.assert_allclose', a)
t = t[:a] + 'audit(pump_on)\n' + t[b:]
t = t[:t.index('deep_transfer =')].rstrip() + '\n'
t += "print('Checks passed: carbon/TA conserved; fitted DIC ratio and pump–mixing balance recovered.')\n"
put('02-pump-comparison', t)

t = source('2957a52c')
qstart = t.index('<div ')
qend = t.index('</div>', qstart)
question = t[qstart:t.index('\n\n', qstart)] + '''

**Question — relate the model to the real ocean**

Which real-ocean pump does this DIC-only transfer most closely resemble?
What important features of the real process are omitted?

'''
astart = t.index('<div ', qend)
answer = t[astart:t.index('\n\n', astart)] + '''

**Instructor answer**

It most closely resembles the **soft-tissue biological pump**: carbon removed
near the surface returns to DIC at depth through remineralization (breakdown
of organic matter). One DIC arrow replaces production, sinking and recycling;
particles and nutrients are not represented. Uniform temperature omits the
thermal mechanism of the solubility pump, and this transfer has no TA change
associated with the carbonate pump. Fitting the full DIC ratio does not isolate
a measured soft-tissue contribution.

'''
put('2957a52c', '''### B4. Relate the effective pump to the real ocean

With the same total carbon, the pump transfers carbon towards the deep ocean
and lowers atmospheric CO2.

''' + question + '</div>\n\n<!-- BEGIN SOLUTION -->\n' + answer + '</div>\n<!-- END SOLUTION -->\n')

t = source('9aa6988c')
t = t.replace('Part B kept the original 01 carbon inventory. Now calculate the additional\ncarbon needed to reach the **full reference state**: 280 ppm in the atmosphere,\n2040 µmol/kg DIC at the surface and 2250 µmol/kg at depth.',
'''We chose $k$ to reproduce the reference DIC ratio. This determines the relative
concentrations, but the total carbon inventory also matters. Part B kept the
original 01 inventory. How much additional carbon is needed to reach the
**full reference state**: 280 ppm in the atmosphere, 2040 µmol/kg surface DIC
and 2250 µmol/kg deep DIC?''')
a = t.index('**Link to the lecture')
b = t.index('### C1.', a)
lecture = t[a:b].strip()
t = t[:a] + '''**Notation:** $R$ is the whole-ocean/atmosphere inventory ratio; it differs
from the lecture's seawater equilibrium capacity $F$.

<details>
<summary>Optional reference — connection to lecture slides 18–21</summary>

''' + lecture.replace('**Link to the lecture (slides 18–21).** ', '') + '\n\n</details>\n\n' + t[b:]
t = t.replace('Record your expected endpoint before running the model.',
              'Record your expected endpoint before running the model. Inventory output\nuses Pmol C, where 1 Pmol = $10^{15}$ mol.')
put('9aa6988c', t)

put('02-supplied-forcing', '''### C2. Run the supplied forcing and budget checks

A **restart** uses the Part B final concentrations as the initial state of a
new run. The **control** receives no input; the **forced run** receives your
extra carbon through the atmosphere.

`Signal` prescribes the flux over time; its `mass` is the total carbon addition.
`Source` represents carbon outside the system, connected to the atmospheric
reservoir by `Species2Species`.

The supplied clock helper resolves the pulse automatically. `clock` is a
dictionary of timing settings; `**clock` passes them to both model constructors.
If you change `pulse_duration`, use positive whole-year durations and rerun
this whole cell to build fresh models.

Read the final check summary: **input mass → carbon/TA budgets → reference
endpoint**. The figure shows the input and the atmospheric response.

<details>
<summary>Optional — changing pulse duration and numerical details</summary>

At fixed added mass, a longer square pulse has a smaller flux rate. Duration
changes the transient; after sufficient relaxation, the final equilibrium
depends on the total addition. Try, for example, `'100 yr'`, `'333 yr'` or
`'1 kyr'`. Keep the pulse inside the run and leave time after it to settle;
increase `run_stop` if the endpoint checks show that it has not settled yet.

`finite_pulse_clock` aligns the pulse with the model grid and refines the grid
for short pulses. The solver joins samples with straight lines, so the code
checks both the sampled sum and the interpolated integral against your addition.
The signal is zero at both simulation boundaries. The budget check compares
total carbon with the initial inventory plus cumulative input, while TA stays
constant. Endpoint checks compare atmospheric CO2 and both DIC concentrations
with the reference state.

</details>
''')
t = source('02-structural-check').replace('    print(audit(case))', '    audit(case)')
t += "print('Checks passed: carbon/TA conserved; no-pump equilibrium agrees with 01.')\n"
put('02-structural-check', t)
t = source('02-forcing-example').replace("print('Control budget:', audit(control))", 'audit(control)')
t = t.replace("print('Forced budget:', audit(forced, added))", 'audit(forced, added)')
t = t.replace("print('Final departure from 280 ppm:', forced.CO2_At.c[-1] * 1e6 - 280)",
              "print('Checks passed: input mass, carbon/TA budgets and full reference endpoint.')")
put('02-forcing-example', t)

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
build_student_notebook(path, ROOT / 'notebooks/student' / name)
print('Simplified 02 source and regenerated student copy.')
