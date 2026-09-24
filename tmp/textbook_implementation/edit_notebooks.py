import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def source(nb, index):
    return ''.join(nb['cells'][index]['source'])

def put(nb, index, text):
    nb['cells'][index]['source'] = text.splitlines(keepends=True)

def replace(nb, index, old, new):
    text = source(nb, index)
    assert old in text, (index, old)
    put(nb, index, text.replace(old, new))

def cell(kind, ident, text, *, solution=False):
    c = dict(cell_type=kind, id=ident, metadata={'tags': ['solution-only']} if solution else {},
             source=text.splitlines(keepends=True))
    if kind == 'code':
        c.update(execution_count=None, outputs=[])
    return c

for path in sorted((ROOT / 'notebooks/instructor').glob('0[1-4]*.ipynb')):
    nb = json.loads(path.read_text(encoding='utf-8'))
    if path.name.startswith('01'):
        replace(nb, 12, '### After running: diagnose the result\n', r'''### After running: diagnose the result

Here $CO_2^*$ denotes the dissolved CO2/carbonic-acid pool. Recall the reaction

$$CO_2^* + H_2O \rightleftharpoons H^+ + HCO_3^-.$$
''')
        replace(nb, 12, 'Which initial chemical assumption prevents recovery of the reference partition?\nCan any process represented in this model change it?',
                'CO2 enters the water and its pH changes. Why does this not create or consume\nTA? Explain using the paired bicarbonate and proton contributions. Which\ninitial chemical assumption therefore persists and prevents recovery of the\nreference partition?')
        replace(nb, 12, 'Gas exchange adds DIC but no TA, so the initial TA = 0 persists.',
                'Each bicarbonate contributes +1 equivalent to TA and the accompanying proton\ncontributes −1: their contributions cancel. Subsequent acid–base repartitioning\nalso conserves TA, although pH changes. Gas exchange adds DIC but no TA, so the\ninitial TA = 0 persists.')
    elif path.name.startswith('02'):
        replace(nb, 15, 'and lowers atmospheric CO2.\n',
                'and lowers atmospheric CO2. **Primary production** fixes carbon into organic\nmatter; **export** carries organic carbon out of the surface layer;\n**remineralization** converts organic carbon back to dissolved inorganic carbon.\n')
        replace(nb, 15, 'What important features of the real process are omitted?',
                'Sketch production → export → remineralization beside its DIC arrow. Which\nsteps are collapsed into that arrow? Does it represent primary production,\nexport reaching the deep box, or permanent burial? Name one omitted control.')
        replace(nb, 15, 'particles and nutrients are not represented.',
                'it represents effective export reaching the deep box and remineralization\nthere, not total primary production or permanent burial. Surface recycling and\na separate particle inventory are omitted; mixing can return this carbon to\nthe surface. Nutrients, light and the depth distribution of recycling are\nexamples of omitted controls.')
        replace(nb, 16, 'per mole of atmospheric carbon.\n',
                'per mole of atmospheric carbon. This is a ratio of **existing carbon stocks**\nat the reference state, not the fraction of a future carbon addition absorbed\nby the ocean.\n')
    elif path.name.startswith('03'):
        replace(nb, 0, 'distinguish graph, budget and restart checks.',
                'explain contrasting organic/carbonate effects on pCO2; distinguish graph, budget and restart checks.')
        replace(nb, 0, 'This allocation needs a student pilot.',
                'Use 4–6 minutes of reconstruction/export discussion for the process arrows in place of repeated inventory-effect answers. This allocation needs a student pilot; if it does not fit, plan 60 minutes or make contour interpretation optional, without taking time from 00.')
        replace(nb, 6, '4. Complete the process-family table below. Write source/destination effects with signs.',
                '4. Complete the process-family table below. For the POC/PIC/D inventory-effects fields, use your local arrows below and identify the receiving/loss inventories; do not repeat the same signs in prose. Write the other source/destination effects with signs.')
        replace(nb, 6, 'For dissolution use the supplied functional form;',
                'On the supplied DIC–TA plot, start at the reference dot. Remove the same small\namount of DIC (20 µmol C/kg) through the **model’s POC pathway** and through\nCaCO3 formation. Draw the two arrows and use the contours to predict each\npCO2 change. Why do the signs differ? Reverse the carbonate arrow to explain\ndissolution. Reuse these arrows when choosing the linked rates in 03.4.\n\nFor dissolution use the supplied functional form;')
        replace(nb, 6, 'The completed flux table follows.',
                'Per unit of carbon removed from the same water mass, model POC has\n$(\\Delta DIC,\\Delta TA)=(-1,0)$ and lowers pCO2. CaCO3 formation has\n$(-1,-2)$ and raises pCO2 near this reference: removing TA reduces the\ncapacity to hold DIC in bicarbonate/carbonate forms, increasing dissolved CO2\ndespite carbon removal. Dissolution reverses the vector, $(+1,+2)$, and lowers\npCO2. TA changes are equivalents per mole C. POC is an equal-and-opposite\ninternal surface-to-deep carbon transfer; PIC removes surface DIC/TA into the\nsupplied carbonate module, and dissolution returns DIC/TA to the deep box.\nUse each box’s water mass to convert these inventory rates to concentrations.\n\nThe instructor arrows and completed flux table follow.')
        replace(nb, 15, '$m=\nho V$', r'$m=\rho V$')
        replace(nb, 15, '$m,DIC$', r'$m\,DIC$')
        replace(nb, 15, '$m,TA$', r'$m\,TA$')
        # Keep the exercise heading with the supplied figure, before its question.
        text = source(nb, 6)
        heading, body = text.split('<div', 1)
        put(nb, 6, '<div' + body)
        nb['cells'][7:7] = [cell('code', '03-carbonate-plane-key',
            '# Supplied implementation — instructor process arrows\n'
            'plot_carbonate_process_plane(P, show_processes=True);\n', solution=True)]
        nb['cells'][6:6] = [
            cell('markdown', '03-carbonate-plane-reading', heading +
                '**Supplied local chemistry diagram.** DIC is horizontal and TA vertical.\n'
                'Contours give seawater pCO2 in µatm. The dot uses the workbook’s L_b\n'
                'DIC/TA and box-specific temperature, salinity and pressure, with the\n'
                'benchmark chemistry options. It is an input reference, not the later\n'
                'stationary restart. The supplied function handles chemistry and plotting.\n\n'
                'Treat these as changes in one water parcel **before gas exchange and\n'
                'transport**. The model’s DIC-only POC closure omits nutrient TA effects\n'
                'described in A2. Equal carbon inventories transferred between boxes of\n'
                'unequal water mass do not give equal concentration changes.\n\n'
                '**Supplied implementation — local carbonate chemistry**\n'),
            cell('code', '03-carbonate-plane-plot',
                 'from teaching_plots import plot_carbonate_process_plane\n'
                 'plot_carbonate_process_plane(P);\n')]
    elif path.name.startswith('04'):
        replace(nb, 14, 'Consult e/h for the sediment answer',
                '**Chemical carbonate compensation** changes dissolution and preservation\nwith prescribed carbonate rain. **Biological carbonate compensation** also\ninvolves changing calcification/export. Local dissolved carbonate repartitioning\nis rapid, while gas exchange, transport and sediment adjustment have their own\ntimescales and can overlap.\n\nConsult e/h for the sediment answer')
        replace(nb, 17,
                '3. **Time and process:** identify a surface/deep response lag and use e/h to explain the linked 1 DIC : 2 TA transfers and sediment memory. What evidence would you need before claiming equilibration?\n4. **Claims and next test:** distinguish benchmark reproduction from a conditional prediction. Choose one fixed assumption and propose one changed input, matched control and diagnostic for a follow-up test. One or two sentences are enough; do not run a fourth case in the core.',
                '3. **Time and process:** contrast rapid dissolved-species repartitioning with dissolution/net burial: which conserves TA, and which changes active ocn TA? Identify a surface/deep lag and explain why a chemical horizon can move before the snowline. Is chemical or biological compensation represented? State the interval and evidence needed to claim stationarity.\n4. **Claims and next test:** distinguish benchmark reproduction from conditional prediction. Deep DIC increases in OA: does that show stronger biological export? Identify prescribed versus responding fluxes, then propose a matched experiment and diagnostic to test a biological-response hypothesis. Keep it brief; do not run a fourth case in the core.')
        text = source(nb, 17)
        start = text.index('3. Surface chemistry')
        end = text.index('\n\n</div>', start)
        text = text[:start] + '''3. Dissolved acid–base repartitioning conserves TA. Dissolution adds 1 DIC and 2 TA to the active ocn; net burial removes them. OA tends to increase dissolution/reduce burial, with OAE tending to oppose this. Surface changes lead the transported deep signal, but these processes overlap rather than forming a strictly serial sequence. Chemical horizons follow current conditions; the snowline also retains sediment history. These fixed-rain cases represent **chemical compensation**, without a biological export response. A stated interval after forcing ends, small sustained state tendencies and balanced boundary fluxes would support stationarity; the last point alone does not establish full equilibration.
4. The OA overlay checks reproduction of a published model, not independent observational validation. Responses remain conditional on its assumptions. POC and PIC export are prescribed identically in the control and forced cases, so their flux anomalies are zero. Transported tracer fluxes, air–sea exchange and dissolution can respond and change deep DIC. Fixed biology still sets the background carbon distribution and chemistry; increased deep DIC does not demonstrate stronger export. One test is a factorial comparison of fixed versus DIC-dependent POC export, each with its own matched unforced control and compatible baseline, keeping PIC fixed. Compare forced-minus-control POC flux and deep-DIC anomalies at the same stated time, and their difference between export laws; check the carbon/TA budgets. This tests a specified response hypothesis, not whether that law is realistic.''' + text[end:]
        put(nb, 17, text)
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

from scripts.build_student_notebooks import build_student_notebook
for path in sorted((ROOT / 'notebooks/instructor').glob('0[1-4]*.ipynb')):
    build_student_notebook(path, ROOT / 'notebooks/student' / path.name)
