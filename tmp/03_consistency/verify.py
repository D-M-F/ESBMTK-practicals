from pathlib import Path
import ast
import base64
import hashlib
import json
import re
import sys
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
from teaching_specification import flux_table_markdown

name = '03_boudreau_three_box_model.ipynb'
source = ROOT/'notebooks/instructor'/name
before = nbformat.read(OUT/'before.ipynb', 4)
nb = nbformat.read(source, 4)
old_codes = {c.id: c for c in before.cells if c.cell_type == 'code'}
new_codes = {c.id: c for c in nb.cells if c.cell_type == 'code'}
assert old_codes.keys() == new_codes.keys()
for id, old in old_codes.items():
    new = new_codes[id]
    assert old.source == new.source, id
    assert old.outputs == new.outputs, id
    assert old.execution_count == new.execution_count, id
assert sum(c.source.count('<!-- BEGIN SOLUTION -->') for c in before.cells) == sum(c.source.count('<!-- BEGIN SOLUTION -->') for c in nb.cells)
print('All executable code and existing outputs preserved; written solutions remain marked.', flush=True)

for role in ('instructor', 'student'):
    path = ROOT/'notebooks'/role/name
    n = nbformat.read(path, 4)
    nbformat.validate(n)
    assert len({c.id for c in n.cells}) == len(n.cells)
    for c in n.cells:
        if c.cell_type == 'code':
            compile(c.source, str(path), 'exec')
    if role == 'student':
        text = '\n'.join(c.source for c in n.cells)
        assert '#f3eefb' not in text and 'BEGIN SOLUTION' not in text
        assert '03_04_boudreau_instructor.png' not in text
        assert text.count('NotImplementedError') == 4
        assert text.count('Your expression') == 13
        assert flux_table_markdown(student=True) in text
        assert 'feedback' not in text.lower() and 'attribution' not in text.lower()
        assert 'W_0+D(t)-E(t)' not in text
        assert '2W_0+2D(t)-2E(t)' not in text
        assert 'state-dependent' not in text
        assert all(not c.get('outputs') for c in n.cells)
    else:
        if '--render-only' in sys.argv:
            saved = {c.id: c for c in nbformat.read(OUT/'executed.ipynb', 4).cells if c.cell_type == 'code'}
            for c in n.cells:
                if c.cell_type == 'code':
                    assert ast.dump(ast.parse(c.source)) == ast.dump(ast.parse(saved[c.id].source))
                    c.outputs = saved[c.id].outputs
                    c.execution_count = saved[c.id].execution_count
            print('Reused verified execution; all executable cells unchanged.', flush=True)
        else:
            import os
            os.environ['IPYTHONDIR'] = str(OUT/'ipython')
            NotebookClient(n, timeout=600, kernel_name='esbmtk314', resources={'metadata': {'path': str(path.parent)}}).execute()
            nbformat.write(n, OUT/'executed.ipynb')
            print('Executed 03: graph, C/TA budgets, restart and reusable-model agreement passed.', flush=True)
    for c in n.cells:
        if c.cell_type == 'markdown':
            def embed(m):
                alt, target = m.groups()
                data = base64.b64encode((path.parent/target).read_bytes()).decode()
                return f'![{alt}](data:image/png;base64,{data})'
            c.source = re.sub(r'!\[([^]]*)\]\(([^)]+)\)', embed, c.source)
    page, _ = HTMLExporter().from_notebook_node(n)
    (OUT/f'{role}.html').write_text(page, encoding='utf-8')
    print('Validated and rendered', role, flush=True)

build_student_notebook(source, OUT/'generated.ipynb')
assert (OUT/'generated.ipynb').read_bytes() == (ROOT/'notebooks/student'/name).read_bytes()
allowed = {str(Path('notebooks')/role/name) for role in ('instructor', 'student')}
changes = [p for p, digest in json.loads((OUT/'protected.json').read_text()).items()
           if p not in allowed and Path(p).suffix != '.log'
           and hashlib.sha256((ROOT/p).read_bytes()).hexdigest() != digest]
assert not changes, changes
print('Exact student regeneration; protected notebooks, archives, workbook, diagrams and worksheets unchanged.', flush=True)
