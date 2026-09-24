import ast
import hashlib
import json
from pathlib import Path
import sys

import nbformat
from bs4 import BeautifulSoup
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

OUT = ROOT / 'tmp/02_main_story'
name = '02_two_layer_ocean_carbon_pump.ipynb'
before = json.loads((OUT / 'before.ipynb').read_text(encoding='utf-8'))
after = json.loads((ROOT / 'notebooks/instructor' / name).read_text(encoding='utf-8'))

def code(nb):
    return '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')

def checks(nb):
    tree = ast.parse(code(nb))
    return sorted(ast.dump(n) for n in ast.walk(tree) if isinstance(n, ast.Call)
                  and (isinstance(n.func, ast.Attribute) and n.func.attr == 'assert_allclose'
                       or isinstance(n.func, ast.Name) and n.func.id == 'audit'))

assert checks(before) == checks(after), 'A scientific check changed'
old_cells = {c['id']: c for c in before['cells']}
for c in after['cells']:
    if c['cell_type'] == 'code' and c['source'] == old_cells[c['id']]['source']:
        assert c == old_cells[c['id']], 'Unchanged cell outputs were modified'
for version in ('instructor', 'student'):
    n = nbformat.read(ROOT / 'notebooks' / version / name, as_version=4)
    nbformat.validate(n)
    page, _ = HTMLExporter().from_notebook_node(n)
    (OUT / f'{version}.html').write_text(page, encoding='utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    assert len(soup.select('details')) == 3
    assert all(d.select('p') for d in soup.select('details'))
    assert len(soup.select('div[style*="#edf5ff"]')) == 6
    assert len(soup.select('div[style*="#f3eefb"]')) == (5 if version == 'instructor' else 0)
    text = '\n'.join(c.source for c in n.cells)
    for removed in ('135.95', '125.29', '2073.53', 'Export evaluated using',
                    'Compare them in B4', 'comparing export estimates'):
        assert removed not in text, removed
    if version == 'student':
        assert text.count('NotImplementedError') == 5
        for answer in ('k=Q\\rho', 'extra_carbon_mol =', 'mixing_type =', 'pump_type =', '6.6644'):
            assert answer not in text, answer
        assert all(not c.get('outputs') for c in n.cells)
    print(f'{version}: valid, panels/details render, scientific answers masked appropriately.')
build_student_notebook(ROOT / 'notebooks/instructor' / name, OUT / 'generated.ipynb')
assert (OUT / 'generated.ipynb').read_bytes() == (ROOT / 'notebooks/student' / name).read_bytes()
allowed = {f'notebooks/{v}/{name}' for v in ('instructor', 'student')}
for p, digest in json.loads((OUT / 'before_hashes.json').read_text()).items():
    if p not in allowed:
        assert hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == digest, p
print('Generation exact; all numerical assertions/audits retained; other notebooks/archives unchanged.')
