import ast
import base64
import hashlib
import json
import mimetypes
from pathlib import Path
import sys

import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
OUT = ROOT / 'tmp/01_02_coherence'
names = ['01_single_box_air_sea_CO2.ipynb', '02_two_layer_ocean_carbon_pump.ipynb']

class NormalizeChoices(ast.NodeTransformer):
    def visit_Assign(self, node):
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in {'mixing_type', 'pump_type'}:
            assert isinstance(node.value, ast.Constant) and node.value.value == 'scale_with_concentration'
            return None
        return self.generic_visit(node)

    def visit_Name(self, node):
        if node.id in {'mixing_type', 'pump_type'}:
            return ast.Constant(value='scale_with_concentration')
        return node

def code_ast(nb, normalize=False):
    text = '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
    if normalize:
        text = text.replace('Export at reference surface DIC (Tmol C/yr):', 'Implied reference export (Tmol/yr):')
        text = text.replace('Export at simulated pump-on equilibrium (Tmol C/yr):', 'Actual stationary export (Tmol/yr):')
    tree = ast.parse(text)
    return ast.dump(NormalizeChoices().visit(tree) if normalize else tree)

for name in names:
    before = json.loads((OUT / f'instructor_{name}').read_text(encoding='utf-8'))
    after = nbformat.read(ROOT / 'notebooks/instructor' / name, as_version=4)
    assert code_ast(before) == code_ast(after, True)
    if name.startswith('01'):
        after_json = json.loads((ROOT / 'notebooks/instructor' / name).read_text(encoding='utf-8'))
        assert [c for c in before['cells'] if c['cell_type'] == 'code'] == [c for c in after_json['cells'] if c['cell_type'] == 'code']
    for version in ('instructor', 'student'):
        nb = nbformat.read(ROOT / 'notebooks' / version / name, as_version=4)
        nbformat.validate(nb)
        html, _ = HTMLExporter().from_notebook_node(nb)
        # Keep local notebook images visible in the relocated preview HTML.
        preview = BeautifulSoup(html, 'html.parser')
        for img in preview.select('img[src]'):
            src = img['src']
            if src.startswith('../../ref/'):
                asset = (ROOT / 'notebooks' / version / src).resolve()
                assert asset.is_file(), asset
                mime = mimetypes.guess_type(asset.name)[0]
                encoded = base64.b64encode(asset.read_bytes()).decode('ascii')
                html = html.replace(src, f'data:{mime};base64,{encoded}')
        (OUT / f'{version}_{name[:2]}.html').write_text(html, encoding='utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        qs = soup.select('div[style*="#edf5ff"]')
        answers = soup.select('div[style*="#f3eefb"]')
        assert len(qs) == 6
        assert len(answers) == (0 if version == 'student' else (4 if name.startswith('01') else 5))
        assert all(p.find('p') for p in qs + answers)
        text = '\n'.join(c.source for c in nb.cells)
        for stale in ('not assessed', 'submit your', 'Finish 02', 'Finish 01', 'Keep it beside'):
            assert stale not in text, stale
        if version == 'student':
            assert all(not c.get('outputs') for c in nb.cells)
            assert 'BEGIN SOLUTION' not in text and 'END SOLUTION' not in text
            if name.startswith('02'):
                assert len(soup.select('table')) == 4
                assert text.count('NotImplementedError') == 5
                for answer in ('mixing_type =', 'pump_type =', 'k=Q\\rho', 'extra_carbon_mol =', '125.29', '6.6644'):
                    assert answer not in text, answer
        print(f'{version} {name[:2]}: valid; six question panels; {len(answers)} answer panels; masking and Markdown checked.')
    target = OUT / ('generated_' + name)
    build_student_notebook(ROOT / 'notebooks/instructor' / name, target)
    assert target.read_bytes() == (ROOT / 'notebooks/student' / name).read_bytes()
    print(f'{name}: generation matches exactly; scientific calculations unchanged after resolving the two law choices.')

hashes = json.loads((OUT / 'before_hashes.json').read_text())
allowed = {f'notebooks/{v}/{n}' for v in ('instructor', 'student') for n in names}
allowed |= {'TEACHING_GOALS.md', 'ref/design.md', 'WORKPLAN.md', 'ref/modelling_cheatsheet.md', 'output/pdf/modelling_cheatsheet.pdf'}
changed = {Path(p).as_posix() for p, old in hashes.items() if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != old}
assert not changed - allowed, changed - allowed
print('All other notebooks and dated archive files retain their starting hashes.')

# Diagnose the pre-existing out-of-scope generated-copy failure without changing 00.
name = '00_PyCO2SYS.ipynb'
target = OUT / ('generated_' + name)
build_student_notebook(ROOT / 'notebooks/instructor' / name, target)
expected = json.loads(target.read_text(encoding='utf-8'))
actual = json.loads((ROOT / 'notebooks/student' / name).read_text(encoding='utf-8'))
extra = [c for c in expected['cells'] if c not in actual['cells']]
assert len(extra) == 2 and all(not ''.join(c['source']).strip() for c in extra)
assert all(c in expected['cells'] for c in actual['cells'])
print('Remaining 00 mismatch consists of its two extra empty instructor cells; neither 00 file was changed.')
