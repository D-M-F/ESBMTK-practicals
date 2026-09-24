import copy
import json
from pathlib import Path
import sys
import tempfile

import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

path = ROOT / 'notebooks/instructor/04_pump_strength_OA_OAE.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
before = copy.deepcopy(nb)
changed = []
for i, cell in enumerate(nb['cells']):
    text = ''.join(cell['source'])
    old = text
    if '## B3.' in text:
        text = text.replace('$z_{cc}$: compensation depth', '$z_{cc}$: carbonate compensation depth (CCD)')
        original = '**Read e together with h.** When compensation depth and snowline separate, the sediment present need not be in equilibrium with current rain and chemistry. In this implementation, erosion depends on the finite existing reactive stock; during deepening the snowline is made to follow the compensation depth rapidly. It does not resolve gradual accumulation of a new sediment column. Treat that part of the OA/OAE contrast as a model assumption.'
        replacement = r'''### Supplied snowline rule: shoaling and deepening differ

The CCD describes whether **today's carbonate rain** survives; the snowline describes where **carbonate sediment is already present**. Use the following model rules to interpret panels e/h. You are not expected to look up or derive the sediment code.

- **CCD shoaling (the main OA response):** the CCD moves into shallower water, leaving previously deposited carbonate below it. Modern rain there dissolves completely, but the existing sediment stock takes time to dissolve. The snowline therefore remains deeper than the CCD and moves upward more slowly: $z_{snow}>z_{cc}$. Their separation records sediment left from earlier conditions.
- **CCD deepening (the main OAE response):** newly arriving carbonate can survive at greater depths. The model lets the snowline follow the deepening CCD effectively instantly on these century-scale plots: $z_{snow}\approx z_{cc}$. This is a supplied assumption about the onset of preservation; it does not simulate the time needed to build a substantial carbonate-rich sediment layer. Numerical tracking can leave a small lag.

Here **instant** means relative to the moving CCD, not relative to the external TA input: transport and deep-water chemistry still take time to change. The rule follows the direction of depth change, not the OA/OAE label; a later shoaling CCD can leave a lagging snowline even in OAE. Read e together with h to connect depth separation to dissolution and net burial.'''
        assert original in text
        text = text.replace(original, replacement)
    if '## C.' in text:
        original = '3. **Critical depths and memory:** compare the directions and separation of $z_{sat}$, $z_{cc}$ and $z_{snow}$ in OA and OAE. What does the OA interval between compensation depth and snowline imply for old sediment, and why is OAE deepening not simply the reverse history? Relate the contrast to dissolution/net burial and the stated snowline assumption.'
        replacement = '3. **Critical depths and memory:** use B3\'s supplied rules and panels e/h. During OA shoaling, locate $z_{sat}$, the CCD and the snowline at about year 2800: what survives between the CCD and snowline, and how does this explain the snowline lag and net-burial sign? During OAE deepening, explain the near-overlap of CCD and snowline. Does this show instantaneous deep-ocean adjustment or instantaneous formation of a thick sediment layer? Distinguish the plotted result from the model assumption.'
        assert original in text
        text = text.replace(original, replacement)
        original = '3. At year 2800 in OA, the saturation horizon is at its 200 m bound, compensation depth near 2.0 km and snowline near 4.3 km: old sediment dissolves between the latter two, although modern rain cannot survive there. Dissolution exceeds the 60 Tmol C/yr modern rain, giving negative net burial. OAE instead deepens compensation depth/snowline to about 5.0 km with greater preservation; their near-overlap during deepening reflects the supplied closure, whereas later slight separation retains history as the chemical horizon retreats.'
        replacement = r'''3. **OA shoaling:** near year 2800, $z_{sat}\approx0.2$ km, $z_{cc}\approx2.0$ km and $z_{snow}\approx4.3$ km; modern rain cannot survive below the CCD, but previously deposited carbonate remains down to the snowline and must dissolve before that boundary can retreat, producing a lag and a memory of earlier conditions. Dissolution of this old stock lets total dissolution exceed the 60 Tmol C/yr modern rain, so net burial becomes negative. **OAE deepening:** the CCD and snowline move together toward about 5.0 km because the model assumes an effectively immediate extension of the preservation boundary as rain starts surviving deeper, with less dissolution and more burial. Their near-overlap is therefore consistent with the supplied rule, not evidence that deep-water chemistry responds instantly to surface TA or that a thick sediment layer forms instantly; the small later separation in OAE appears when its CCD starts shoaling again.'''
        assert original in text
        text = text.replace(original, replacement)
    if old != text:
        assert cell['cell_type'] == 'markdown'
        cell['source'] = text.splitlines(keepends=True)
        changed.append(i)
assert len(changed) == 2
assert [c for c in before['cells'] if c['cell_type']=='code'] == [c for c in nb['cells'] if c['cell_type']=='code']
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False)+'\n', encoding='utf-8')
target = ROOT / 'notebooks/student' / path.name
build_student_notebook(path, target)
with tempfile.TemporaryDirectory() as directory:
    check = Path(directory)/path.name
    build_student_notebook(path, check)
    assert check.read_bytes() == target.read_bytes()
for role in ('instructor','student'):
    n = nbformat.read(ROOT/'notebooks'/role/path.name, 4)
    nbformat.validate(n)
    source = '\n'.join(c.source for c in n.cells)
    if role=='student':
        assert '#f3eefb' not in source and 'BEGIN SOLUTION' not in source
        assert 'You are not expected to look up or derive the sediment code.' in source
        assert 'OA shoaling:** near year 2800' not in source
        assert source.count('NotImplementedError') == 3
        assert all(not c.get('outputs') for c in n.cells)
    html, _ = HTMLExporter().from_notebook_node(n)
    soup = BeautifulSoup(html, 'html.parser')
    assert len(soup.select('table')) == 3
    assert len(soup.select('div[style*="#edf5ff"]')) == 4
    assert len(soup.select('div[style*="#f3eefb"]')) == (2 if role=='instructor' else 0)
    assert 'Supplied snowline rule: shoaling and deepening differ' in soup.get_text()
    (ROOT/'tmp/04_consistency'/f'{role}_memory.html').write_text(html, encoding='utf-8')
print('PASS: two Markdown cells revised; all code/outputs unchanged; exact student regeneration, validation, masking and HTML structure.')
