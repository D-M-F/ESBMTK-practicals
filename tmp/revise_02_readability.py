import ast
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

OUT = ROOT / 'tmp/02_readability'
OUT.mkdir(exist_ok=True)
NAME = '02_two_layer_ocean_carbon_pump.ipynb'
path = ROOT / 'notebooks/instructor' / NAME
before = path.read_bytes()
(OUT / 'instructor_before.ipynb').write_bytes(before)
(OUT / 'student_before.ipynb').write_bytes((ROOT / 'notebooks/student' / NAME).read_bytes())
paths = list((ROOT / 'notebooks').rglob('*.ipynb')) + list((ROOT / 'archive').rglob('*'))
(OUT / 'before_hashes.json').write_text(json.dumps({str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}))
nb = json.loads(before)
old = copy.deepcopy(nb)
cells = nb['cells']

def source(i):
    return ''.join(cells[i]['source'])

def put(i, text):
    cells[i]['source'] = text.splitlines(keepends=True)

def replace(i, a, b):
    assert a in source(i), (i, a)
    put(i, source(i).replace(a, b, 1))

def mark(text):
    return '<mark style="background-color: #fff0b3; color: #513d00; padding: 0.05em 0.2em; border-radius: 3px;"><strong>' + text + '</strong></mark>'

opening = source(0)
end = opening[opening.index('**Coding reference:**'):]
put(0, '''# 02 — Build a two-layer ocean and test an effective carbon pump

In 01, adding the inferred TA allowed a uniform ocean to recover the reference
state. Here you divide that ocean into surface and deep layers, then introduce
a downward carbon transfer to maintain a DIC difference between them.

**Learning goals:** check that adding a reservoir conserves carbon and TA;
explain a maintained DIC gradient as a balance between pump and mixing;
calculate a finite carbon input and verify its inventory.

**Core time: 55 minutes.** Follow the same predict → map → run → check → explain
sequence as in 01.

| Part | Main question | Time |
| --- | --- | --- |
| A. Add the deep box | Does the two-layer model recover the buffered 01 equilibrium without a pump? | 20 min |
| B. Add the effective pump | What pump coefficient maintains the reference DIC ratio? | 20 min |
| C. Add carbon | How much carbon allows the pumped model to reach the full reference state? | 15 min |

Part B follows a ''' + mark('calibration-first') + ''' approach: you fit the pump coefficient
to the reference DIC ratio, then examine the other model results. Part C checks
the prescribed input and carbon budget. Separate pump mechanisms, OA/OAE,
sediments and feedbacks come in 03/04.

Complete the marked scientific choices and the two derivations. Constructor
syntax, chemistry, plots, restarts and budget checks are supplied.
[Teaching goals](../../TEACHING_GOALS.md).

''' + end)

# Put setup, transport and coding guidance under descriptive steps.
a = source(2)
diagram = a[a.index('```text'):a.index('Only the surface')]
transport = a[a.index('As in 01'):a.index('**From one connection to many.**')]
transport = transport.replace('As in 01 and the larger model in 03, list', 'As in 01, write each budget as')
transport = transport.replace('**inputs minus outputs** for each\nbox.', '**inputs minus outputs**.')
transport = transport.replace('For $X=$ DIC or TA,', 'Subscripts $s$ and $d$ denote surface and deep water. For $X=$ DIC or TA,')
transport = transport.replace('Use $Q$ in m³/yr,', 'The prescribed transport is 20 Sv in each direction (1 Sv = $10^6$ m³/s).\nUse $Q$ in m³/yr,')
transport = transport.replace('Air–sea exchange retains the two conceptual terms from 01,\nevaluated together by one native gas connection.', 'Air–sea exchange retains invasion and outgassing from 01, evaluated together\nby one native gas connection.')
put(2, '''## A. Add a deep box and check the unpumped model

### A1. Keep the 01 inventory and chemistry

''' + diagram + '''Only the surface exchanges CO2 with the atmosphere. The surface and deep
volumes together equal the ocean volume in 01. Both layers use the inferred
01 TA, T = 16 °C, S = 35 and P = 0 bar, with the same carbonate settings.
The combined atmosphere-plus-ocean carbon inventory also stays the same.
Real thermal and TA gradients are omitted here; 03/04 use distinct box conditions.

**Supplied geometry.** The layer split in `teaching_config.py` is calculated
algebraically before any model run. It makes the reference DIC values
(surface 2040, deep 2250 µmol/kg) give an ocean/atmosphere carbon inventory ratio
of **62.4** at 280 ppm. Using the independent whole-ocean volume and atmospheric
size, with ESBMTK density, gives a surface depth of about **298.75 m**. This is
''' + mark('ratio-derived teaching geometry') + ''', rather than an observed mixed-layer depth.
You will use the ratio again in Part C; preparing this geometry does not add carbon.

### A2. Translate the mixing arrows into fluxes

''' + transport + '''### A3. Complete the reservoir and mixing choices

`build_layers` below constructs a fresh model and returns it without running it.
It reuses the inferred TA from 01. By default, both layers start at
1000 µmol/kg DIC, the alternative initial partition checked in 01; the supplied
atmosphere helper assigns the remaining carbon to the atmosphere.

**From one connection to many.** `create_bulk_connections` repeats the
`Species2Species` construction introduced in 01 for the routes and tracers in
a dictionary. It uses `ConnectionProperties` groups; `ty` selects the flux law
(the same choice as `ctype` in an individual connection). Here `sc` is the mass
transport scale and `sp` lists the transported species.

The bulk helper handles repeated DIC/TA routes. Gas exchange still uses the
supplied helper because the bulk helper does not forward its specialised
settings. Part B uses `Species2Species` directly for the single pump arrow.
Focus on endpoints, species and flux laws; the internal call chain is not assessed.

<div style="background-color: #edf5ff; color: #173b61; border-left: 4px solid #3977b8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">

**Question — map reservoirs and mixing**

Complete **02.1** (deep-box volume and initial concentrations) and **02.2**
(mixing arrow names and transported species) in `build_layers` below. The
surface-box construction is supplied as an example.

Leave **02.3** for Part B: the pump block is skipped while `k_kg_yr=0`.
Run the definition cell, then the separate supplied comparison.

</div>''')

replace(4, '### Explain the structural check', '### A4. Explain the structural check')
replace(4, 'Why can symmetric mixing change the transient but not maintain a stationary\nDIC gradient?', 'Why can equal upward/downward water transports change the approach to\nequilibrium but not maintain a stationary DIC gradient without a pump?')
replace(4, '## B. Derive the first-order pump coefficient', '## B. Derive and test the effective pump\n\n### B1. Read the supplied pump assumption')
replace(4, 'This is an aggregate export/remineralization closure. It carries DIC only,\nwithout water or TA. The coefficient $k$ is constant in this exercise; real\nbiological export need not scale with the entire DIC pool.', '''Here, **first order** means that the flux is proportional to the current
surface DIC: doubling that concentration doubles the flux at fixed $k$.
The single arrow represents organic carbon leaving the surface and returning
to DIC at depth through remineralization (the breakdown of organic matter).
This is an **effective pump**: the model transfers DIC directly, without an
explicit organic-carbon reservoir, water transport or TA transfer. The coefficient
$k$ stays constant here; real biological export need not scale with the entire DIC pool.

### B2. Read the budgets as inputs minus outputs

Let $m_s$ and $m_d$ be the fixed seawater masses in kg and $C_{atm}$ the
atmospheric carbon inventory in mol C. Multiplying a DIC concentration tendency
by box mass gives the carbon inventory tendency in mol C/yr.''')
replace(4, 'The pump is one directed transfer: an output from the surface and the same\ninput to the deep box. Export followed by remineralization is represented by\nthis single effective transfer; it is not a difference between opposing pump\nfluxes. Upward transport is already represented by the mixing arrow.', 'The pump leaves the surface and enters the deep box at the same rate.\nThe upward return is already represented by mixing.')
replace(4, 'Likewise $J_{gas}=J_{gas,in}-J_{gas,out}$ is', 'Likewise $J_{gas}(t)=J_{gas,in}(t)-J_{gas,out}(t)$ is')
replace(4, '### Exercise: derive the expression before coding', '### B3. Exercise: derive the expression before coding\n\nA **stationary state** has no further change in any reservoir inventory, even\nthough individual transfers continue. Stars denote stationary concentrations:\n$DIC_s^*$ and $DIC_d^*$.')
replace(4, '4. Complete Exercise 02.3 in `build_layers` and rerun its definition cell, then compare pump on\n   and pump off at the same initial total carbon and TA. Report the implied\n   reference export flux as well as the realized stationary export.', '''4. Complete **02.3** in `build_layers` (Part A) and rerun that definition cell.
   Enter your expression for $k$ in the calculation cell below, then run the
   supplied pump comparison at the same initial total carbon and TA. Report
   the implied reference export flux and the actual stationary export.

The supplied `mixing_mass_transport()` returns $Q\\rho$ in kg/yr using ESBMTK
density and the prescribed 20 Sv. Use the same DIC units in your concentration
ratio. Export is reported in Tmol C/yr, where 1 Tmol = $10^{12}$ mol.''')
replace(6, '### Interpret the matched experiment', '### B4. Interpret the pump-on/pump-off comparison\n\nThe two runs start with the same carbon and TA inventories; only the pump\nchanges. A **conditional model result** is an output that follows from these\nchosen inputs and assumptions.')
replace(6, 'Why need the final atmosphere not be 280 ppm?', 'Why does fitting the DIC ratio not require the final atmosphere to be 280 ppm?')

c = source(7)
start = c.index('### Exercise:')
put(7, '''## C. Calculate a carbon input and verify the forced run

Part B kept the original 01 carbon inventory. Now calculate the additional
carbon needed to reach the **full reference state**: 280 ppm in the atmosphere,
2040 µmol/kg DIC at the surface and 2250 µmol/kg at depth.

At that reference state, the prepared geometry gives an ocean/atmosphere
''' + mark('inventory ratio') + ''' of **62.4**, meaning 62.4 moles of ocean carbon per mole
of atmospheric carbon. This compares whole-reservoir inventories; it is not
the seawater equilibrium capacity $F$ discussed in the lecture.

''' + c[start:])
replace(7, '### Exercise: calculate the required addition', '### C1. Derive and calculate the required addition')
replace(7, 'Atmospheric mole inventory |', 'Total atmospheric gas inventory (mol) |')
replace(7, 'Existing atmosphere-plus-ocean carbon |', 'Existing atmosphere-plus-ocean carbon (mol C) |')
replace(7, '5. Assign your result in **mol C** to `extra_carbon_mol` in the calculation cell.\n   The supplied `Signal` example below will use this variable as its `mass`.', '''5. In **02.4**, assign the atmospheric reference inventory to `C_atm_280`, the
   combined target to `target_total_carbon`, and the addition in **mol C** to
   `extra_carbon_mol`. The supplied forcing uses the addition as its `mass`.
   The printed unit Pmol C means $10^{15}$ mol C.''')
replace(7, 'Predict the endpoint before integrating. The final return to the reference\nstate is a forcing-implementation and conservation check. The chosen geometry,\ninferred TA and fitted pump already make that reference state consistent; the\nrun is not independent evidence for the pump mechanism.', 'Predict the endpoint before running the model. The geometry, inferred TA and\nfitted pump already make the reference state consistent; recovering it tests\nthe forcing implementation and conservation.')
put(10, '''### C2. Run the supplied forcing and budget checks

A **restart** uses the final concentrations from a previous run as the initial
state of a new run. Here both new runs start from the Part B pump-on endpoint.
The **control** receives no input; the **forced run** receives your extra carbon
through the atmosphere. Their difference isolates the response to that input.

`Signal` prescribes the carbon flux over time. Its `mass` is the total addition,
not a flux rate. The square pulse starts at 1000 yr and lasts 1000 yr; `Source`
represents carbon outside the model, connected to the atmospheric reservoir by
`Species2Species`.

Read the supplied checks in this order:

1. **Input:** both the sum of sampled fluxes times the time step and the integral
   of the solver's interpolated flux equal your intended addition. The solver
   joins successive samples with straight lines. The pulse is zero at the start
   and end of the simulation.
2. **Budget:** total carbon increases by the cumulative input, while total TA
   stays constant. `audit(forced, added)` checks this throughout the run.
3. **Endpoint:** compare the final atmosphere and both DIC concentrations with
   the reference state. This is a consistency check of the constructed model.
''')
replace(12, '### What did the forcing experiment establish?', '### C3. Explain what the forcing experiment establishes')

# Split long reading blocks; keep solution panels and markers intact.
def md(text, identifier):
    return {'cell_type': 'markdown', 'id': identifier, 'metadata': {}, 'source': text.strip().splitlines(keepends=True)}

def code(text, identifier, metadata=None):
    return {'cell_type': 'code', 'id': identifier, 'metadata': metadata or {},
            'source': text.strip().splitlines(keepends=True), 'outputs': [], 'execution_count': None}

revised = []
for i, cell in enumerate(cells):
    if i in (2, 4):
        text = source(i)
        sections = ([('### A2.', '02-mixing-fluxes'), ('### A3.', '02-map-connections')] if i == 2 else
                    [('## B.', '02-pump-assumption'), ('### B2.', '02-pump-budgets'), ('### B3.', '02-pump-derivation')])
        for title, ident in sections:
            first, text = text.split(title, 1)
            revised.append(md(first, cell['id']))
            cell = md('', ident)
            text = title + text
        revised.append(md(text, cell['id']))
    elif i == 3:
        definition, run = source(i).split('# Supplied structural checks:', 1)
        revised.append(code(definition, cell['id'], cell['metadata']))
        revised.append(md('''### Run the supplied no-pump comparison

The next cell runs `build_layers()` with the pump off and the corresponding
buffered one-box model from 01. `audit` checks carbon and TA conservation;
`assert_allclose` checks that ocean masses and final concentrations agree within
numerical tolerances. A failed assertion stops the cell so you can inspect
the relevant choices before continuing.''', '02-run-structural-check'))
        revised.append(code('# Understand and run: trace this supplied step and interpret its evidence.\n# Supplied structural checks:' + run, '02-structural-check'))
    elif i == 5:
        calculation, run = source(i).split('pump_on = build_layers(k)', 1)
        revised.append(code(calculation, cell['id'], cell['metadata']))
        revised.append(md('''### Run the supplied pump comparison

After updating **02.3** and rerunning the `build_layers` definition, run the
cell below. It checks the fitted stationary DIC ratio and compares the net
upward mixing flux with the downward pump flux. Read the atmospheric and DIC
responses in the plots, then answer B4.''', '02-run-pump'))
        revised.append(code('# Understand and run: trace this supplied step and interpret its evidence.\npump_on = build_layers(k)' + run, '02-pump-comparison'))
    else:
        revised.append(cell)
nb['cells'] = revised

def executable(data):
    return ast.dump(ast.parse('\n'.join(''.join(c['source']) for c in data['cells'] if c['cell_type'] == 'code')))

assert executable(old) == executable(nb), 'Executable code changed'
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
build_student_notebook(path, ROOT / 'notebooks/student' / NAME)
print('Reorganized 02 and regenerated student copy; executable AST unchanged.')
