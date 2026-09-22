import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

path = ROOT / 'notebooks/instructor/01_single_box_air_sea_CO2.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))

def source(index):
    return ''.join(nb['cells'][index]['source'])

def put(index, text):
    nb['cells'][index]['source'] = text.splitlines(keepends=True)

blue = '<div style="background-color: #edf5ff; color: #173b61; border-left: 4px solid #3977b8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">'
purple = '<div style="background-color: #f3eefb; color: #38224f; border-left: 4px solid #7952a8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">'

put(0, source(0).replace(
    '**Provisional time: 35 minutes.** Diagram and prediction (10); diagnosis and\nTA calculation (15); comparisons and explanation (10). Use the PyCO2SYS skills\nfrom 00 to write one complete TA calculation. Model construction, comparison\nruns, plotting and budget checks are supplied. Give short answers.',
    '**Provisional time: 40 minutes.** Diagram and prediction (10); diagnosis,\nTA inference and pCO2–DIC curves (20); model comparisons and explanation (10).\nReuse your PyCO2SYS skills from 00 to infer TA, then calculate seawater pCO2\nacross a supplied DIC range. Model construction, loops, conversions, plotting\nand budget checks are supplied. Give short answers.'))
put(1, source(1).replace('single_box, inventories, audit,',
                         'single_box, inventories, audit, atmospheric_pco2_curve,').replace(
    'from teaching_plots import plot_ta_free, plot_partition_comparison',
    'from teaching_plots import (\n    plot_ta_free, plot_partition_comparison, plot_equilibrium_curves,\n)'))
nb['cells'][1]['execution_count'] = None
nb['cells'][1]['outputs'] = []

diagnosis = source(12).split('\n**How TA affects carbon uptake.**')[0]
diagnosis = diagnosis.replace(
    'Gas exchange adds DIC but no TA, so the initial TA = 0 persists. At zero TA,\na much larger fraction of DIC is aqueous CO2 than in the buffered reference\nstate. The ocean therefore cannot retain the target DIC at 280 ppm. No process\nin this model can generate the missing alkalinity. A small initial DIC does\nnot require zero TA; these are separate initial assumptions.',
    'Gas exchange adds DIC but no TA, so the initial TA = 0 persists. No process\nin this model can generate the missing alkalinity. A small initial DIC does\nnot require zero TA; these are separate initial assumptions. Section 3 tests\nhow changing TA changes the relation between DIC and seawater pCO2.')
put(12, diagnosis.rstrip() + '\n')
put(13, source(13).replace('## 3. Infer TA, then test the revised model',
    '## 3. Infer TA, explain the partition, then test the revised model\n\n'
    'PyCO2SYS calculates carbonate-equilibrium states; ESBMTK follows carbon\n'
    'transfer through time. First use the reference DIC and atmospheric xCO2\n'
    'to infer TA. Then use DIC and TA to calculate seawater pCO2 and explain\n'
    'the contrasting carbon partitions.\n\n### 3.1 Infer TA from the reference state'))
put(15, source(15).replace('### Run a fresh model with the inferred TA',
    '### 3.3 Test the curve interpretation with a fresh model').replace(
    'Change only the initial TA. This is a',
    'Change only the initial TA. Compare the final DIC with the intersection\n'
    'you identified above. This is a'))

intro = r'''### 3.2 Use PyCO2SYS to explain the carbon partition

For each TA, calculate seawater pCO2 over the same range of DIC. Each point
is a carbonate-equilibrium state: its pCO2 is the atmospheric partial pressure
that would balance CO2 exchange with that water. It need not equal the
**actual** atmospheric pCO2 in our closed system. The plot is a set of possible
states, not a time series.

The slope of each seawater curve is its
<mark style="background-color: #fff0b3; color: #513d00; padding: 0.05em 0.2em; border-radius: 3px;"><strong>absolute sensitivity</strong></mark>,

$$\left(\frac{\partial pCO_{2,ocn}}{\partial DIC}\right)_{TA,T,S,P}.$$

It measures the pCO2 increase per small DIC increase at fixed TA and
thermodynamic conditions, here in µatm per (µmol/kg). It can vary along a
curve; use the calculated curves to compare the two TA cases.

**Supplied atmosphere line.** At each DIC, conservation requires

$$C_{atm}=C_0-m_{ocn}DIC,\qquad xCO_{2,atm}=\frac{C_{atm}}{N_{atm}}.$$

Here DIC is in mol/kg, $m_{ocn}$ is the ocean mass in kg and $N_{atm}$ is the
atmospheric amount in mol. The supplied
[`atmospheric_pco2_curve`](../../simple_models.py) applies these equations and
converts dry-air xCO2 to pCO2 using the shared gas settings. Both plot axes use
pCO2 in **µatm**; the reference **280 ppm is dry-air xCO2**, not 280 µatm.
The same line applies to both TA cases because their total carbon and reservoir
sizes are identical.

BLUE

**Question — calculate the seawater curves (Exercise 01.2)**

Complete the chemistry calculation inside the supplied loop. For the current
`ta_value`, pass `dic_grid` and TA to PyCO2SYS with the shared `**config.pyco2`
settings. Choose the input-type codes and save the output pCO2 array as
**`curve_pco2`, in µatm**.

**Hints:** use the DIC and TA entries in the
[input-type table](https://pyco2sys.readthedocs.io/en/latest/co2sys_nd/#carbonate-system-parameters)
and the `pCO2` output. An array can replace a single concentration in a
PyCO2SYS call; one TA value applies to every DIC in that array. The supplied
loop repeats your call for TA = 0 and `inferred_ta`, then saves both curves
in a dictionary. The grid ends just below the limit where all carbon would
be in the ocean, leaving no atmospheric carbon.

</div>
'''.replace('BLUE', blue)

code = '''# Supplied implementation: candidate DIC values and the conserved-carbon atmosphere.
max_dic = config.total_carbon_mol / box_mass_kg(M.Ocean) * 1e6
dic_grid = np.linspace(INITIAL_DIC, max_dic * (1 - 1e-6), 600)
atm_pco2 = atmospheric_pco2_curve(dic_grid, config)

# Choose and explain: calculate seawater pCO2 from DIC and TA.
ocean_pco2 = {}
for label, ta_value in [('TA = 0', FIRST_TA), ('inferred TA', inferred_ta)]:
    # BEGIN SOLUTION
    curve = pyco2.sys(par1=dic_grid, par1_type=2,
                     par2=ta_value, par2_type=1, **config.pyco2)
    curve_pco2 = curve['pCO2']
    # END SOLUTION
    ocean_pco2[label] = curve_pco2

# Supplied implementation: linear axes; the right panel enlarges the reference region.
plot_equilibrium_curves(dic_grid, ocean_pco2, atm_pco2, config);
'''

interpret = r'''BLUE

**Question — explain the contrasting carbon uptake**

1. Why does atmospheric pCO2 fall as DIC increases? Use conservation to relate
   a given DIC increase to the carbon lost by the atmosphere.
2. Locate each seawater curve's intersection with the atmosphere line and
   estimate its DIC. Why does each intersection represent zero **net** air–sea
   exchange? Use the zoom for the inferred-TA case.
3. Compare the seawater slopes at the same DIC on the left panel. Starting
   from the same initial DIC and total carbon, explain the difference in net
   ocean uptake. Do these curves alone tell you which model equilibrates sooner?

**Hint:** use the sign of $pCO_{2,atm}-pCO_{2,ocn}$ to identify the direction of
net transfer. For the same ocean mass and initial DIC, a larger final DIC
means more net carbon uptake. Compare slopes on the same panel: the zoom has
different axis scales. Curves outside a panel's vertical range are clipped.

</div>

<!-- BEGIN SOLUTION -->
PURPLE

**Instructor answer**

Each mole gained by the ocean is lost from the atmosphere. A DIC increase
$\Delta DIC$ therefore removes $m_{ocn}\Delta DIC$ mol from the atmosphere
(DIC in mol/kg), lowering atmospheric xCO2 and pCO2. This relation is the
same in both cases; TA changes the seawater chemistry curve.

The zero-TA intersection is near **470 µmol/kg**. The inferred-TA intersection
is at **2040 µmol/kg**, where pCO2 is about **275 µatm**, equivalent to the
reference dry-air xCO2 of **280 ppm**. At an intersection the two pCO2 values
are equal, so invasion and outgassing balance and net exchange is zero.
The second intersection recovers the state used to fit TA, not an independent
prediction of it.

For these settings and this DIC range, the zero-TA seawater curve rises more
steeply at a given DIC. Starting from the common small initial DIC, it meets
the falling atmosphere line at much lower DIC, after less net carbon transfer.
With inferred TA, seawater pCO2 stays lower over this range and more carbon
can accumulate before air–sea equilibrium is reached. The full curves and
the common inventory constraint establish this result; one local derivative
alone would not determine the endpoint. The initial DIC and atmospheric
carbon are identical, but the initial chemical speciation differs with TA.

This explains the **amount** absorbed. The curves have no time axis and do
not establish which case equilibrates sooner; section 4 examines exchange
rate and equilibration time.

</div>
<!-- END SOLUTION -->

> **Connection to the lecture.** The Revelle sensitivity factor $R$ expresses
> the local pCO2–DIC response in fractional terms. On
> [slide 46](../../ref/Ocean_C_cycle_2026.pdf#page=46), it estimates fractional
> DIC uptake for a prescribed atmospheric CO2 increase at fixed TA and
> thermodynamic conditions. The doubling example is a linear approximation
> using fixed $R$. Here we use the full curves and our closed carbon inventory.
'''.replace('BLUE', blue).replace('PURPLE', purple)

def cell(kind, ident, content):
    c = dict(cell_type=kind, id=ident, metadata={}, source=content.splitlines(keepends=True))
    if kind == 'code':
        c.update(execution_count=None, outputs=[])
    return c

nb['cells'][15:15] = [cell('markdown', '01-curve-purpose', intro),
                       cell('code', '01-curve-calculation', code),
                       cell('markdown', '01-curve-interpretation', interpret)]
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
build_student_notebook(path, ROOT / 'notebooks/student' / path.name)

def edit(name, replacements):
    p = ROOT / name
    text = p.read_text(encoding='utf-8')
    for old, new in replacements:
        assert old in text, (name, old)
        text = text.replace(old, new)
    p.write_text(text, encoding='utf-8')

edit('TEACHING_GOALS.md', [
    ('| 01: missing alkalinity | 35 | One complete TA calculation; predictions and explanation |',
     '| 01: missing alkalinity | 40 | TA inference; pCO2–DIC curves; model interpretation |'),
    ('| Synthesis and completion buffer | 15 |', '| Synthesis and completion buffer | 10 |'),
    ('01–04 contain 185 minutes', '01–04 contain 190 minutes'),
    ('01 — Diagnose missing alkalinity (35 minutes)', '01 — Diagnose missing alkalinity (40 minutes)'),
    ('3. Infer background TA from the two targets and distinguish that fit from prediction.',
     '3. Infer background TA, use pCO2–DIC curves to explain partitioning, and distinguish the fit from prediction.'),
    ('PyCO2SYS TA calculation from DIC/xCO2; interpret supplied partition and\npiston-velocity comparisons.',
     'PyCO2SYS TA calculation from DIC/xCO2; complete a DIC/TA-to-pCO2 call\ninside a supplied loop and explain the curve intersections; interpret supplied\npartition and piston-velocity comparisons.'),
    ('Allocate 10 minutes to diagram/prediction, 15 to diagnosis/inference, and 10 to paths.',
     'Allocate 10 minutes to diagram/prediction, 20 to diagnosis/inference/curves,\nand 10 to paths. The added five minutes come from the completion buffer;\nthe session remains four hours. Pilot this allocation with students after 00.'),
    ('comparison runs, unit conversions, plots and carbon/TA audits.',
     'comparison runs, DIC grid, repeated loop, conserved-carbon atmosphere line,\nunit conversions, plots and carbon/TA audits.'),
    ('provisional 35-minute', 'provisional 40-minute'),
    ('units, plus explanations beside the diagnosis, inference and path-comparison\nactivities.',
     'units, a forward chemistry call, and explanations beside the diagnosis,\ninference, curve interpretation and path-comparison activities.'),
    ('output name. Keep the model rerun in a separate supplied cell.',
     'output name. Also mask the forward chemistry call and pCO2 extraction,\nwith input/output hints supplied. Place the curve exercise after TA inference\nand before the model rerun; mask the causal interpretation as a written answer.\nStudents infer uptake from the full curves and the common atmosphere line,\nnot a stated slope ordering or a single local sensitivity. Briefly connect\nfractional Revelle sensitivity to lecture slide 46 without adding an R exercise.\nKeep the model rerun in a separate supplied cell.'),
    ('The full TA calculation replaces the two-number selection task and requires more\nindependent work. Shorter explanations and consolidated questions make room for\nit within the provisional 10/15/10-minute allocation; this is not a verified\ntiming result. Pilot the revised 35-minute route with students who have completed\n00.',
     'The full TA inference and forward curve calculation reuse skills from 00.\nThe provisional 10/20/10-minute allocation allows five more minutes for the\ncurve exercise; this is not a verified timing result. Pilot the revised\n40-minute route with students who have completed 00.'),
])
edit('ref/design.md', [
    ('provisional 35-minute', 'provisional 40-minute'),
    ('cell after the inferred TA is displayed.', 'cell after the TA inference and curve exercise.'),
    ('within 10/15/10 minutes, but this revised allocation still requires a pilot after 00.',
     'within 10/20/10 minutes, including five extra minutes for the curve exercise\nfrom the completion buffer. The four-hour session is preserved, but this\nrevised allocation still requires a pilot after 00.\n\n'
     'Position PyCO2SYS explicitly: infer TA from reference DIC/xCO2, then evaluate\n'
     'seawater pCO2 from DIC/TA across a supplied grid before the revised ESBMTK\n'
     'run. Students complete the forward chemistry call and output extraction;\n'
     'supply the loop, grid, conserved-inventory atmosphere line, dry-xCO2/pCO2\n'
     'conversion and plots. Ask them to interpret slopes and intersections,\n'
     'placing the zero-TA uptake explanation in a masked instructor answer.\n'
     'Distinguish carbonate-equilibrium states from air–sea equilibrium at\n'
     'intersections, and uptake amount from equilibration time. Compare absolute\n'
     'sensitivity at matched DIC under the shared settings; use the full curves\n'
     'and carbon inventory to establish the endpoint rather than assuming one\n'
     'local derivative describes the whole trajectory. Keep the Revelle factor\n'
     'as a brief link to slide 46\'s fractional response to prescribed atmospheric\n'
     'CO2 and fixed-R linear approximation, with no extra calculation.'),
])
edit('README.md', [
    ('estimated 185 minutes', 'estimated 190 minutes'),
    ('then explain the missing TA, calibration and rate/equilibrium distinction.\nThe supplied rerun follows in a separate cell. Shorter construction steps and\none final synthesis support the provisional 35-minute route, which still needs\na student pilot with the fuller calculation. Notebook 02',
     'then complete a forward DIC/TA-to-pCO2 call in a supplied loop. They use the\ncurves and a supplied atmospheric conservation line to explain carbon uptake\nbefore testing the revised model. Construction, plotting and conversions are\nsupplied; scientific choices and interpretation remain student work. The\nprovisional 40-minute route takes five minutes from the completion buffer and\nstill needs a student pilot. Notebook 02'),
])
print('Updated instructor/student 01 and teaching documentation.')
