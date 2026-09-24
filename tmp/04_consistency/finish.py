import json, re, sys, base64
from pathlib import Path
import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
OUT=ROOT/'tmp/04_consistency'
p=ROOT/'notebooks/instructor/04_pump_strength_OA_OAE.ipynb'
nb=json.loads(p.read_text(encoding='utf-8'))
for c in nb['cells']:
    s=''.join(c['source'])
    s=s.replace('| d / f | Air–sea transfer and atm CO2 |', '| d / f | Air–sea transfer (positive into the ocn) and atm CO2 |')
    s=s.replace('OA raises atm CO2 and lowers surface pH; OAE initially does the reverse. Locate the forcing peak in B1 and compare it with B2\'s extrema: the deep signal develops more slowly as transport carries the perturbation downward, while declining positive input still adds material and sediment adjustment continues. A peak or the final plotted value alone is not equilibrium.', 'Both input rates peak near model year 2170; OA\'s atm CO2 maximum/surface pH minimum follow near 2300–2350, while its deep DIC is still rising at 3800. OAE lowers atm CO2 and raises surface pH; deep DIC initially rises too, then declines and becomes slightly negative relative to control late in the run. Declining positive input still adds material, and adjustment persists after input ends; a turning point is not equilibrium.')
    s=s.replace('OA\'s enhanced dissolution/reduced net burial retains or returns TA to the active ocn at two equivalents per mole of carbonate carbon. Changed net burial also changes total active carbon, so atm loss need not equal ocn gain exactly.', 'OA\'s enhanced dissolution/reduced net burial retains or returns TA to the active ocn at two equivalents per mole of carbonate carbon (h: burial is negative by about 2300). In OAE, increased net burial instead removes part of the added TA and carbon, weakening sustained uptake; atm loss need not equal ocn gain because this sediment boundary responds.')
    s=s.replace('OA shoals the chemical horizons while the snowline erodes more slowly: old carbonate remains below the new compensation depth and can dissolve although modern rain no longer survives there. OAE deepens the horizons and favors preservation; its snowline follows the compensation depth closely under the supplied rapid-deepening rule. This contrasts finite-stock erosion with an idealized deepening closure, rather than demonstrating symmetric sediment recovery.', 'At year 2800 in OA, the saturation horizon is at its 200 m bound, compensation depth near 2.0 km and snowline near 4.3 km: old sediment dissolves between the latter two, although modern rain cannot survive there. Dissolution exceeds the 60 Tmol C/yr modern rain, giving negative net burial. OAE instead deepens compensation depth/snowline to about 5.0 km with greater preservation; their near-overlap during deepening reflects the supplied closure, whereas later slight separation retains history as the chemical horizon retreats.')
    s=s.replace('OA\'s pronounced depth separation and dissolution response differ from OAE\'s smaller deepening and increased preservation.', 'After roughly 2800, OA deep DIC continues rising whereas OAE deep DIC declines; enhanced dissolution supplies carbon/TA in OA, while extra net burial in OAE removes them and reduces retained alkalinity.')
    c['source']=s.splitlines(keepends=True)
p.write_text(json.dumps(nb,indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
build_student_notebook(p,ROOT/'notebooks/student'/p.name)
build_student_notebook(p,OUT/'generated.ipynb')
assert (OUT/'generated.ipynb').read_bytes()==(ROOT/'notebooks/student'/p.name).read_bytes()
for role in ('student','instructor'):
    path=ROOT/'notebooks'/role/p.name
    n=nbformat.read(path,4)
    nbformat.validate(n)
    source='\n'.join(c.source for c in n.cells)
    if role=='student':
        assert '#f3eefb' not in source and 'BEGIN SOLUTION' not in source
        assert source.count('NotImplementedError')==3
        assert all(not c.get('outputs') for c in n.cells)
        assert source.count('**Your explanation:**')==2
    for c in n.cells:
        if c.cell_type=='code':
            compile(c.source,str(path),'exec')
        else:
            for link in re.findall(r'\]\(([^)]+)\)',c.source):
                if '://' not in link:
                    assert (path.parent/link).exists(),link
    # Put verified figures into the preview only; distributed copies stay output-free.
    for c in n.cells:
        if c.cell_type!='code': continue
        ix=None
        if 'plot_external_forcings(fixed' in c.source: ix=1
        if 'plot_matched_responses(fixed' in c.source: ix=2
        if "plot_figure4(fixed_cases['OA']" in c.source: ix=3
        if "plot_figure4(fixed_cases['OAE']" in c.source: ix=4
        if ix:
            data=base64.b64encode((OUT/f'figure-{ix:02}.png').read_bytes()).decode()
            c.outputs=[nbformat.v4.new_output('display_data',data={'image/png':data})]
    html,_=HTMLExporter().from_notebook_node(n)
    soup=BeautifulSoup(html,'html.parser')
    assert len(soup.select('table'))==3
    assert len(soup.select('div[style*="#edf5ff"]'))==4
    assert len(soup.select('div[style*="#f3eefb"]'))==(2 if role=='instructor' else 0)
    (OUT/f'{role}.html').write_text(html,encoding='utf-8')
    print('PASS',role,'validation, masking, compilation, links and HTML structure')
