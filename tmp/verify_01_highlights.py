import hashlib
import json
from pathlib import Path
import sys
import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
out = ROOT / 'tmp/01_highlights'
name = '01_single_box_air_sea_CO2.ipynb'
src = ROOT / 'notebooks/instructor' / name
nb = json.loads(src.read_text(encoding='utf-8'))
# Keep highlights on complete concepts; use the singular definition of settling time.
for cell in nb['cells']:
    if cell['cell_type'] != 'markdown':
        continue
    text = ''.join(cell['source'])
    text = text.replace('<strong>settling time</strong></mark>s.\nHere, settling time',
                        '<strong>settling times</strong></mark>.\nHere, settling time')
    cell['source'] = text.splitlines(keepends=True)
src.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
build_student_notebook(src, ROOT / 'notebooks/student' / name)
before = json.loads((out / 'instructor_before.ipynb').read_text(encoding='utf-8'))
assert [c for c in before['cells'] if c['cell_type'] == 'code'] == [
    c for c in nb['cells'] if c['cell_type'] == 'code']
for version in ('instructor', 'student'):
    path = ROOT / 'notebooks' / version / name
    data = nbformat.read(path, as_version=4)
    nbformat.validate(data)
    html, _ = HTMLExporter().from_notebook_node(data)
    (out / f'{version}.html').write_text(html, encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    panels = soup.select('div[style*="border-left: 4px solid"]')
    questions = [p for p in panels if p.strong.text.startswith('Question')]
    answers = [p for p in panels if p.strong.text == 'Instructor answer']
    assert len(questions) == 7
    assert len(answers) == (4 if version == 'instructor' else 0)
    assert all(p.find('p') for p in panels)
    if version == 'student':
        assert html.count('Your explanation:') == 4
        assert '#f3eefb' not in html
    print(f'{version}: valid notebook; {len(questions)} questions; {len(answers)} answer panels; Markdown renders.')
target = out / 'student_check.ipynb'
build_student_notebook(src, target)
assert target.read_bytes() == (ROOT / 'notebooks/student' / name).read_bytes()
hashes = json.loads((out / 'before_hashes.json').read_text(encoding='utf-8'))
changed = [Path(p).as_posix() for p, digest in hashes.items() if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != digest]
assert set(changed) == {f'notebooks/instructor/{name}', f'notebooks/student/{name}'}
# Confirm the known 00 failure is serialization only, without modifying it.
target00 = out / '00_check.ipynb'
build_student_notebook(ROOT / 'notebooks/instructor/00_PyCO2SYS.ipynb', target00)
assert json.loads(target00.read_text(encoding='utf-8')) == json.loads(
    (ROOT / 'notebooks/student/00_PyCO2SYS.ipynb').read_text(encoding='utf-8'))
print('PASS: exact 01 generation; unchanged code/outputs, other notebooks and archive; 00 differs only in serialization.')
