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
OUT = ROOT / 'tmp/02_readability'
NAME = '02_two_layer_ocean_carbon_pump.ipynb'
before = json.loads((OUT / 'instructor_before.ipynb').read_text(encoding='utf-8'))
after = nbformat.read(ROOT / 'notebooks/instructor' / NAME, as_version=4)
def executable(nb):
    return ast.dump(ast.parse('\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')))
assert executable(before) == executable(after)
print('Executable code and its ordering are unchanged.')
for version in ('instructor', 'student'):
    nb = nbformat.read(ROOT / 'notebooks' / version / NAME, as_version=4)
    nbformat.validate(nb)
    html, _ = HTMLExporter().from_notebook_node(nb)
    (OUT / f'{version}.html').write_text(html, encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    questions = soup.select('div[style*="#edf5ff"]')
    answers = soup.select('div[style*="#f3eefb"]')
    assert len(questions) == 7
    assert len(answers) == (5 if version == 'instructor' else 0)
    assert len(soup.select('table')) == 2
    assert all(p.find('p') for p in questions + answers)
    if version == 'student':
        assert 'k=Q' not in html
        assert '267.6326' not in html
        assert 'extra_carbon_mol =' not in '\n'.join(c.source for c in nb.cells)
        assert '62.4)C_{atm,280}-C_0' not in html
        assert html.count('Your explanation:') == 5
        assert sum(c.source.count('NotImplementedError') for c in nb.cells) == 5
        assert all(not c.get('outputs') for c in nb.cells)
    print(f'{version}: valid; 7 questions, {len(answers)} answers, 2 rendered tables; masking checked.')
check = OUT / 'student_check.ipynb'
build_student_notebook(ROOT / 'notebooks/instructor' / NAME, check)
assert check.read_bytes() == (ROOT / 'notebooks/student' / NAME).read_bytes()
hashes = json.loads((OUT / 'before_hashes.json').read_text())
changed = {Path(p).as_posix() for p, digest in hashes.items() if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != digest}
assert changed == {f'notebooks/instructor/{NAME}', f'notebooks/student/{NAME}'}, changed
print('Exact student generation; all other notebooks and archive files unchanged.')
for name in ('00_PyCO2SYS.ipynb', '01_single_box_air_sea_CO2.ipynb'):
    build_student_notebook(ROOT / 'notebooks/instructor' / name, OUT / name)
    expected = json.loads((OUT / name).read_text(encoding='utf-8'))
    actual = json.loads((ROOT / 'notebooks/student' / name).read_text(encoding='utf-8'))
    if expected != actual:
        extra = [c for c in expected['cells'] if c not in actual['cells']]
        missing = [c for c in actual['cells'] if c not in expected['cells']]
        print('Unrelated mismatch in', name, ':', len(extra), 'extra generated cells;', len(missing), 'other student cells.')
        assert all(not ''.join(c['source']).strip() for c in extra) and not missing
