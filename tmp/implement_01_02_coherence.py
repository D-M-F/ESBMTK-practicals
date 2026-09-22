import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

OUT = ROOT / 'tmp/01_02_coherence'
OUT.mkdir(exist_ok=True)
names = ['01_single_box_air_sea_CO2.ipynb', '02_two_layer_ocean_carbon_pump.ipynb']
paths = list((ROOT / 'notebooks').rglob('*.ipynb')) + list((ROOT / 'archive').rglob('*'))
paths += [ROOT / p for p in ['TEACHING_GOALS.md', 'ref/design.md', 'WORKPLAN.md',
                            'ref/modelling_cheatsheet.md', 'output/pdf/modelling_cheatsheet.pdf']]
(OUT / 'before_hashes.json').write_text(json.dumps({str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}))
for name in names:
    for version in ['instructor', 'student']:
        (OUT / f'{version}_{name}').write_bytes((ROOT / 'notebooks' / version / name).read_bytes())
for name in ['TEACHING_GOALS.md', 'ref/design.md', 'WORKPLAN.md', 'ref/modelling_cheatsheet.md']:
    (OUT / Path(name).name).write_bytes((ROOT / name).read_bytes())

def panel(body, label='Instructor answer', answer=True):
    bg, ink, border = ('#f3eefb', '#38224f', '#7952a8') if answer else ('#edf5ff', '#173b61', '#3977b8')
    p = (f'<div style="background-color: {bg}; color: {ink}; border-left: 4px solid {border}; '
         'padding: 12px 16px; margin: 16px 0; border-radius: 4px;">\n\n'
         f'**{label}**\n\n{body.strip()}\n\n</div>')
    return '<!-- BEGIN SOLUTION -->\n' + p + '\n<!-- END SOLUTION -->' if answer else p

def mark(text):
    return '<mark style="background-color: #fff0b3; color: #513d00; padding: 0.05em 0.2em; border-radius: 3px;"><strong>' + text + '</strong></mark>'

def edit_notebook(name, edit):
    path = ROOT / 'notebooks/instructor' / name
    nb = json.loads(path.read_text(encoding='utf-8'))
    original = copy.deepcopy(nb)
    cells = {c['id']: c for c in nb['cells']}
    def get(key): return ''.join(cells[key]['source'])
    def put(key, text): cells[key]['source'] = text.splitlines(keepends=True)
    def rep(key, old, new):
        assert old in get(key), (key, old)
        put(key, get(key).replace(old, new, 1))
    edit(get, put, rep)
    for c, before in zip(nb['cells'], original['cells']):
        if c['cell_type'] == 'code' and c['source'] != before['source']:
            c['outputs'] = []
            c['execution_count'] = None
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    build_student_notebook(path, ROOT / 'notebooks/student' / name)

def one(get, put, rep):
    rep('805ec91a', '''Keep the [coding reference](../../ref/modelling_cheatsheet.md)
([two-page handout](../../output/pdf/modelling_cheatsheet.pdf)) beside the notebook.
Use it during the diagram activity; its separate tracer example is optional.''', '''**Optional coding reference:** [From conceptual model to code](../../ref/modelling_cheatsheet.md)
([two-page handout](../../output/pdf/modelling_cheatsheet.pdf)). Use it for a reminder;
the syntax needed here is introduced below.''')
    rep('805ec91a', '''(support code). Supplied steps still need interpretation; syntax memorisation
is not assessed. See [teaching goals and timing](../../TEACHING_GOALS.md).''', '''(support code). This practical is ungraded. Syntax memorisation is not required:
refer to the examples and focus on connecting the scientific assumptions to the code.
See [teaching goals and timing](../../TEACHING_GOALS.md).''')
    put('e50c7e7e', get('e50c7e7e') + '''

**Reading the settings.** `config` is the shared configuration imported above.
The dot retrieves a named setting: `config.ocean_volume_m3` is the ocean volume
in m³. Names ending in `_umol_kg` or `_ppm` indicate the units. Some settings,
such as `config.pyco2`, collect several named values in a Python **dictionary**.
The next cell displays these settings; you do not need to edit the configuration file.''')
    rep('01-object-map', 'First create the ocean and its carbonate chemistry:', '''In `{'Ocean': box_parameters(...)}`, the quoted name is a dictionary **key**;
the function result after the colon is its **value**. `initialize_reservoirs`
uses that pair to create the named box from its supplied properties.

First create the ocean and its carbonate chemistry:''')
    rep('01-connection', '`source` and `sink` set the positive direction; `ctype` selects the flux law.', '''`source` and `sink` set the positive direction; `ctype` selects the flux law.
The `id` is a label used to identify a connection in summaries or later lookups;
here `air_sea` labels this one gas connection.''')
    rep('e74ed3f6', '''`**config.pyco2`. These settings include **16 °C**, salinity 35, pressure 0 dbar and
the shared carbonate choices.''', '''`**config.pyco2`. The double star passes the dictionary's entries as named
arguments to the function. These settings include **16 °C**, salinity 35,
pressure 0 dbar and the shared carbonate choices.''')
    rep('e74ed3f6', '''as needed. Dry-air xCO2 in ppm differs from pCO2 in µatm.''', '''as needed. Retrieve a result using `result['key']`, where `key` is its exact
name in the documentation. Dry-air xCO2 in ppm differs from pCO2 in µatm.''')
    rep('41a5ffe0', 'Does either change the eventual equilibrium?',
        'Does either change the eventual equilibrium? Explain why the two changes\n+can alter the path while preserving the endpoint.'.replace('\n+', '\n'))
    put('41a5ffe0', get('41a5ffe0').rstrip() + '\n\n' + panel('''Changing initial DIC redistributes the same carbon between atmosphere and ocean.
Changing piston velocity alters the exchange rate. At fixed total carbon, TA,
geometry and chemistry, neither change alters the gas-exchange equilibrium;
both runs recover the buffered reference state. A smaller positive piston
velocity lengthens the adjustment.'''))
    numerical = get('f73310db').split('> **Numerical reference.**', 1)[1]
    put('f73310db', '''## 5. Continue to the two-layer model

Real-ocean TA reflects weathering, mineral dissolution and carbonate burial.
This closed model includes none of those sources or sinks; prescribing background
TA does not simulate its origin. Those processes enter explicitly in 03/04.

**You have completed 01.** Keep your TA calculation and explanations in this
notebook; no separate submission is required. Continue to 02, which retains the
same total carbon inventory and adds a deep-ocean reservoir.

> **Numerical reference.**''' + numerical)

def two(get, put, rep):
    s = get('0a022ace')
    a, b = s.index('Part B follows'), s.index('Complete the marked')
    put('0a022ace', s[:a] + s[b:])
    rep('0a022ace', '**Core time: 55 minutes.**', '**Provisional time: 55 minutes.**')
    rep('0a022ace', '**Coding reference:**', '**Optional coding reference:**')
    rep('0a022ace', '([two-page handout](../../output/pdf/modelling_cheatsheet.pdf)). Keep it beside this notebook.',
        '([two-page handout](../../output/pdf/modelling_cheatsheet.pdf)). Essential syntax is explained below.')
    rep('0a022ace', '''The labels also apply to surrounding predictions and explanations: supplied code
can still require scientific interpretation. Syntax memorisation is not assessed.''', '''This practical is ungraded. Syntax memorisation is not required: refer to the
examples and focus on connecting scientific assumptions to the code.''')
    rep('2acb80bd', '''of **62.4** at 280 ppm.''', '''$R=C_{ocn}/C_{atm}=62.4$ at 280 ppm, where `ocn` and `atm` denote ocean and atmosphere.''')
    put('02-mixing-fluxes', get('02-mixing-fluxes') + '''

**Why keep TA transport?** Both layers start with the same TA, and none of the
processes represented here creates a TA difference. The opposing TA fluxes
therefore cancel: mixing causes no net TA redistribution. We retain its transport
for a consistent water-transfer model while isolating the DIC pump. TA still
controls carbonate chemistry; it is the spatial TA gradient that we omit.''')
    put('02-map-connections', '''### A3. Complete the reservoir and mixing choices

`build_layers` constructs a fresh model and returns it without running it.
Both layers initially have 1000 µmol/kg DIC, the alternative partition in 01,
and the inferred 01 TA. The atmosphere helper assigns the remaining carbon
to the atmosphere to preserve the total inventory.

**Reading this code.**

| Pattern | Meaning |
| --- | --- |
| `config.surface_volume_m3` | Retrieve a named setting from the shared configuration; here, surface volume in m³. |
| `state['Surface']` | Retrieve the surface entry from the `state` dictionary. Keys are case-sensitive: `'Surface'` and `'Deep'`. |
| `(1000.0, inferred_ta)` | A pair of concentrations in the order **DIC, TA**, both in µmol/kg. |
| `surface_dic, surface_ta = state['Surface']` | Unpack the pair into two variables. |
| `*state['Surface']` | Pass the two values as separate arguments to `box_parameters`. |
| `state=None` | Use the default initial values when no restart state is provided. |

`create_bulk_connections` builds repeated routes for the species listed in `sp`.
Each route key has the format **`Source_to_Sink@id`**: ESBMTK uses the two box
names to find its endpoints, and `id` to identify the connection. The names must
match the created reservoirs. The `@` belongs to ESBMTK's string format; it is
not a separate Python operation. These IDs can distinguish connections in
summaries or later lookups; 02 does not look them up directly.

**Choose a flux law.** The bulk dictionary's `ty` and an individual connection's
`ctype` select the same kind of law. Choose from these options by matching the
equation; the remaining constructor arguments are supplied for this exercise.

| Choice | Flux law | Relevant arguments |
| --- | --- | --- |
| `regular` | A prescribed flux independent of source concentration. | `rate` (bulk key `ra`), in amount/time. |
| `scale_with_concentration` | A coefficient multiplied by source concentration. | `scale` (bulk key `sc`); units must convert concentration to amount/time. |
| `gasexchange` | Net invasion minus outgassing, as in 01. | Gas-transfer and solubility settings, supplied by the atmosphere helper. |

''' + panel('''Complete **02.1** (deep-box volume and initial concentrations) and **02.2**
(the two directed arrow names, transported species and `mixing_type`). Use IDs
`mix_down` and `mix_up`. Choose one law for both mixing directions and explain
how it implements the equation in A2. The surface construction is your example.

Leave **02.3** for Part B: its pump block is skipped while `k_kg_yr=0`.
Run the definition cell, then the supplied comparison.''', 'Question — map reservoirs and mixing', False))
    rep('a3d16943', '# Exercise 02.2: name the two directed arrows and select transported_species.',
        '# Exercise 02.2: choose both arrows, transported_species and mixing_type.')
    rep('a3d16943', '    transported_species = [M.DIC, M.TA]\n    # END SOLUTION',
        "    transported_species = [M.DIC, M.TA]\n    mixing_type = 'scale_with_concentration'\n    # END SOLUTION")
    # Both occurrences become uses of the one masked scientific choice.
    put('a3d16943', get('a3d16943').replace("'ty': 'scale_with_concentration'", "'ty': mixing_type"))
    rep('a3d16943', '# Exercise 02.3 (Part B): choose pump_source, pump_sink and pump_scale.',
        '# Exercise 02.3 (Part B): choose pump_source, pump_sink, pump_type and pump_scale.')
    rep('a3d16943', '        pump_scale = k_kg_yr\n        # END SOLUTION',
        "        pump_scale = k_kg_yr\n        pump_type = 'scale_with_concentration'\n        # END SOLUTION")
    rep('a3d16943', "ctype='scale_with_concentration', scale=float(pump_scale)",
        'ctype=pump_type, scale=float(pump_scale)')
    rep('63486c2f', '''Why can equal upward/downward water transports change the approach to
equilibrium but not maintain a stationary DIC gradient without a pump? What would non-conservation tell you about your connections?''', '''Without a pump, why must surface and deep DIC become equal at equilibrium?
Why should this endpoint agree with the buffered one-box model? What would
non-conservation tell you about your connections?''')
    rep('63486c2f', '''fluxes balance, so $DIC_d^*=DIC_s^*$. Equal water transports preserve box
volumes.''', '''fluxes balance, so $DIC_d^*=DIC_s^*$. With the same total ocean mass, carbon,
TA and chemistry, the uniform ocean has the same equilibrium partition as 01.
Equal water transports preserve box volumes.''')
    rep('02-pump-assumption', '''The single arrow represents organic carbon leaving the surface and returning
to DIC at depth through remineralization (the breakdown of organic matter).
This is an **effective pump**: the model transfers DIC directly, without an
explicit organic-carbon reservoir, water transport or TA transfer. The coefficient
$k$ stays constant here; real biological export need not scale with the entire DIC pool.''', '''This **effective pump** transfers DIC directly from surface to deep water,
without water or TA transfer. It represents the combined effect of unresolved
processes; it has no explicit particles or organisms. The coefficient $k$ stays
constant here. Treat proportionality to the whole DIC pool as a supplied model
assumption, to be related to the lecture's real-ocean pumps in B4.''')
    rep('02-pump-budgets', 'the surface budget is $J_{mix,up}^{(TA)}-J_{mix,down}^{(TA)}$',
        'the surface budget is $J_{mix,up}^{(TA)}(t)-J_{mix,down}^{(TA)}(t)$')
    rep('02-pump-derivation', '### B3. Exercise: derive the expression before coding\n',
        '### B3. Exercise: derive the expression before coding\n\n'
        + mark('calibration-first') + ': use the reference DIC ratio to infer $k$.\n'
        'Agreement with that ratio will check implementation, rather than independently\n'
        'predict the gradient.\n')
    rep('02-pump-derivation', '''4. Complete **02.3** in `build_layers` (Part A) and rerun that definition cell.
   Enter your expression for $k$ in the calculation cell below, then run the
   supplied pump comparison at the same initial total carbon and TA. Report
   the implied reference export flux and the actual stationary export.''', '''4. Complete **02.3** in `build_layers`: choose the pump endpoints, `pump_type`
   and scale. Explain which law from A3 implements the assumption in B1, then
   rerun the definition cell. Enter your expression for $k$ below and run the
   supplied comparison at the same initial total carbon and TA.''')
    rep('02-pump-derivation', '''**Calibration-first:** the observed reference ratio is used to infer $k$.
Agreement with that ratio checks implementation; it is not an independent
prediction of the gradient. No independent export estimate is supplied here.

''', '')
    rep('02-pump-derivation', 'the ratio and mol/kg when calculating export in mol/yr.',
        'the ratio and mol/kg when calculating export in mol/yr. With the defaults,\n'
        '$k \\simeq 6.6644\\times10^{16}$ kg/yr. In 02.3, use the concentration-dependent\n'
        'law with surface DIC as source, deep DIC as sink and $k$ as its scale.')
    rep('a76005d4', 'Implied reference export (Tmol/yr):', 'Export at reference surface DIC (Tmol C/yr):')
    rep('02-pump-comparison', 'Actual stationary export (Tmol/yr):', 'Export at simulated pump-on equilibrium (Tmol C/yr):')
    rep('02-run-pump', '''upward mixing flux with the downward pump flux. Read the atmospheric and DIC
responses in the plots, then answer B4.''', '''upward mixing flux with the downward pump flux. Read atmospheric CO2 and the
two fluxes in the plots, and surface/deep DIC in the printed endpoints. The
calculation above evaluates export at **reference** surface DIC; the final print
below evaluates it at the **simulated pump-on equilibrium**. Compare them in B4.''')
    put('2957a52c', '''### B4. Interpret the pump-on/pump-off comparison

The runs start with the same carbon and TA inventories; only the pump changes.
''' + mark('Conditional model results') + ''' follow from the chosen inputs and assumptions.

''' + panel('''1. Which quantity was fitted? Use the printed DIC values and flux plot to explain
   why matching that quantity does not require a final atmosphere of 280 ppm.
2. Compare export evaluated at reference surface DIC with export at the simulated
   pump-on equilibrium. Why do they differ even though $k$ is unchanged?
3. Which pump from the lecture does this DIC-only transfer most closely resemble?
   Which features of the real process are simplified here?''', 'Question — interpret the matched experiment', False) + '\n\n' + panel(r'''The stationary **DIC ratio** was fitted; atmospheric CO2 and absolute DIC follow
from the inventory and model assumptions. At the 01 total carbon inventory,
the pump-on model reaches approximately 138.27 ppm, with surface/deep DIC of
1880.00/2073.53 µmol/kg. The flux plot shows downward pumping balanced by net
upward mixing at equilibrium.

| Export evaluated using | Surface DIC (µmol/kg) | Export (Tmol C/yr) |
| --- | ---: | ---: |
| Reference state | 2040.00 | 135.95 |
| Simulated pump-on equilibrium | 1880.00 | 125.29 |

The same law $J_{pump}=kDIC_s$ is evaluated at two different stationary states.
The lower simulated surface DIC gives a lower export. These are both model
fluxes, not observations. In Part C the extra carbon allows the full reference
state, and hence its export, to be recovered.

The transfer most closely resembles the **soft-tissue biological pump**:
carbon removed near the surface returns to DIC at depth through remineralization
(breakdown of organic matter). Here that sequence is replaced by one DIC arrow;
production, particles, nutrients and depth-dependent recycling are not resolved.
Uniform temperature omits the thermal mechanism of the solubility pump, and
the transfer lacks the TA change associated with the carbonate pump. Fitting
the full DIC ratio does not isolate a measured soft-tissue contribution.''') + '''

> **Optional context — comparing export estimates.** Published global organic-carbon
> export estimates span about **5–12 Pg C/yr**, with different methods and pathway
> definitions ([Nowicki et al., 2022](https://doi.org/10.1029/2021GB007083)).
> One Tmol C is approximately 0.012 Pg C. Our coefficient is fitted using a
> prescribed 20 Sv transport; the layer boundary is about 299 m, and upper-ocean
> recycling is unresolved. Before comparing magnitudes, match the export depth,
> pathways and reference period. A smaller effective flux alone cannot identify
> which omitted process accounts for the difference. No extra calculation is required.''')
    # Use stars for both stationary evaluations in the written answer.
    rep('2957a52c', '$J_{pump}=kDIC_s$', '$J_{pump}^*=kDIC_s^*$')
    rep('9aa6988c', '''At that reference state, the prepared geometry gives an ocean/atmosphere
<mark style="background-color: #fff0b3; color: #513d00; padding: 0.05em 0.2em; border-radius: 3px;"><strong>inventory ratio</strong></mark> of **62.4**, meaning 62.4 moles of ocean carbon per mole
of atmospheric carbon. This compares whole-reservoir inventories; it is not
the seawater equilibrium capacity $F$ discussed in the lecture.''', '''At that reference state, the prepared geometry gives the whole-reservoir
''' + mark('inventory ratio') + ''' $R=C_{ocn}/C_{atm}=62.4$: 62.4 moles of ocean carbon
per mole of atmospheric carbon.

**Link to the lecture (slides 18–21).** The lecture's $F$ is seawater equilibrium
carbon capacity. In the dry-air mole-fraction convention used here,
$F=DIC_s^*/x_{CO2}^* \\simeq 7.3$ mol air/kg seawater. For the uniform ocean in 01,
$R_0=F m_{ocn}/N_{atm} \\simeq 57$, where $m_{ocn}$ is ocean water mass and
$N_{atm}$ is atmospheric moles of air. In 02 the deep DIC excess increases the
inventory ratio to 62.4 at the reference state. Keep $F$ and $R$ distinct;
use the actual inventory below rather than the rounded lecture ratio.''')
    rep('9aa6988c', 'Pumped ocean/atmosphere carbon ratio, 62.4', 'Reference pumped inventory ratio, $R=62.4$')
    rep('9aa6988c', '''Predict the endpoint before running the model. The geometry, inferred TA and
fitted pump already make the reference state consistent; recovering it tests
the forcing implementation and conservation.''', 'Record your expected endpoint before running the model.')
    put('02-supplied-forcing', '''### C2. Run the supplied forcing and budget checks

A **restart** uses a previous run's final concentrations as the initial state
of a new run. Both runs below start from the Part B pump-on endpoint. The
**control** receives no input; the **forced run** receives your extra carbon
through the atmosphere. Their difference isolates the input's effect.

`Signal` prescribes the flux over time; its `mass` is the total carbon addition.
`Source` represents carbon outside the system, connected to the atmospheric
reservoir by `Species2Species`.

**The 1000-year pulse is a supplied choice, not a restriction.** It starts at
1000 yr and ends at 2000 yr. At fixed added mass, a longer square pulse has a
smaller flux rate. Duration changes the transient; after sufficient relaxation,
the final equilibrium should depend on the total addition. Keep the supplied
duration for this run; exploring other durations is optional.

Read the checks in order: **input** (integrated flux equals your addition),
**budget** (total carbon rises by the cumulative input and TA stays constant),
then **endpoint** (compare atmospheric CO2 and both DIC concentrations with the
reference state).

> **Supplied-code note.** The solver joins signal samples with straight lines;
> the code checks both the sampled sum and this interpolated integral. A different
> duration must be adequately resolved, keep the signal zero at the simulation's
> start and end, pass the integral check, and leave time to reach equilibrium.''')
    rep('0ae3d6c1', '''Explain why 62.4 and the mass-based initial inventory lead to the carbon amount
you used. Why should this implementation check return close to 280 ppm? If it
does not, inspect signal units, its integrated mass, carbon/TA conservation,
equilibration and chemistry settings before changing any model inputs.''', '''Does the final state agree with your prediction in C1? Explain why recovering
280 ppm checks the supplied forcing and carbon budget without independently
validating the effective pump. Point to the external carbon-input connection
and explain how it differs from the internal transfers in A/B.''')
    rep('0ae3d6c1', '''different atmospheric endpoint through nonlinear carbonate chemistry.''', '''different atmospheric endpoint through nonlinear carbonate chemistry.
The `synthetic_input` connection runs from an external `Source` to atmospheric
CO2, increasing combined carbon. Mixing, pumping and air–sea exchange only
redistribute carbon within that combined inventory.''')
    rep('0ae3d6c1', 'The native solver may flag pH changes',
        'If the reference state is not recovered, inspect signal units and integrated\n'
        'mass, conservation, equilibration and chemistry settings before changing inputs.\n\n'
        'The native solver may flag pH changes')
    put('213b58cd', '''**You have completed 02.** Keep your two derivations, including units, and your
explanations in this notebook; no separate submission is required. Continue to
03 for explicit circulation and biological/carbonate processes.''')

edit_notebook(names[0], one)
edit_notebook(names[1], two)
print('Updated instructor 01/02 and generated their student copies.')
