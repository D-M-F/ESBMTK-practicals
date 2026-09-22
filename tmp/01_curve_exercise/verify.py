import base64
import hashlib
import json
import mimetypes
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
OUT = ROOT / 'tmp/01_curve_exercise'
name = '01_single_box_air_sea_CO2.ipynb'
src = ROOT / 'notebooks/instructor' / name
student = ROOT / 'notebooks/student' / name
build_student_notebook(src, OUT / 'generated.ipynb')
assert (OUT / 'generated.ipynb').read_bytes() == student.read_bytes()
for version in ('instructor', 'student'):
    path = ROOT / 'notebooks' / version / name
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)
    if version == 'instructor':
        if '--render-only' in sys.argv:
            executed = nbformat.read(OUT / 'executed.ipynb', as_version=4)
            for cell, previous in zip(nb.cells, executed.cells):
                if cell.cell_type == 'code':
                    assert cell.source == previous.source
                    cell.outputs = previous.outputs
                    cell.execution_count = previous.execution_count
        else:
            print('Executing complete instructor 01...', flush=True)
            # A scratch cwd keeps the ESBMTK logs outside active notebooks.
            NotebookClient(nb, timeout=180, kernel_name='python3',
                           resources={'metadata': {'path': str(OUT)}}).execute()
        nbformat.write(nb, OUT / 'executed.ipynb')
        outputs = [o for c in nb.cells if c.cell_type == 'code' for o in c.outputs]
        errors = [o for o in outputs if o.output_type == 'error']
        assert not errors, errors
        curve_cell = next(c for c in nb.cells if c.id == '01-curve-calculation')
        warnings = [o.text for o in curve_cell.outputs if o.output_type == 'stream']
        assert not warnings, warnings
        images = [o.data['image/png'] for o in curve_cell.outputs
                  if o.output_type in ('display_data', 'execute_result') and 'image/png' in o.data]
        assert len(images) == 1
        (OUT / 'curves.png').write_bytes(base64.b64decode(images[0]))
        streams = [o.text for o in outputs if o.output_type == 'stream']
        (OUT / 'execution_output.txt').write_text('\n'.join(streams), encoding='utf-8')
    else:
        text = '\n'.join(c.source for c in nb.cells)
        assert text.count('NotImplementedError') == 2
        assert '470' not in text and 'BEGIN SOLUTION' not in text
        assert all(not c.get('outputs') for c in nb.cells)
    html, _ = HTMLExporter().from_notebook_node(nb)
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.select('img[src]'):
        ref = img['src']
        if ref.startswith('../../ref/'):
            asset = (path.parent / ref).resolve()
            encoded = base64.b64encode(asset.read_bytes()).decode('ascii')
            html = html.replace(ref, f'data:{mimetypes.guess_type(asset.name)[0]};base64,{encoded}')
    (OUT / f'{version}.html').write_text(html, encoding='utf-8')
    answers = soup.select('div[style*="#f3eefb"]')
    assert len(answers) == (5 if version == 'instructor' else 0)
    assert len(soup.select('div[style*="#edf5ff"]')) == 8
    print(version, 'valid; questions/answers and student masking correct.', flush=True)

before = json.loads((OUT / 'before/notebooks/instructor' / name).read_text(encoding='utf-8'))
after = json.loads(src.read_text(encoding='utf-8'))
old_code = [c for c in before['cells'] if c['cell_type'] == 'code']
new_code = [c for c in after['cells'] if c['cell_type'] == 'code' and c['id'] != '01-curve-calculation']
assert old_code[1:] == new_code[1:], 'Existing model code/output changed'
hashes = json.loads((OUT / 'before_hashes.json').read_text())
allowed = {f'notebooks/{v}/{name}' for v in ('student', 'instructor')}
changed = {Path(p).as_posix() for p, old in hashes.items()
           if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != old}
assert not changed - allowed, changed - allowed
print('Only 01 notebook pair changed; all previous model cells/outputs and archives preserved.')
