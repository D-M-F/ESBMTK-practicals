from pathlib import Path
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

name = '03_boudreau_three_box_model.ipynb'
before = nbformat.read(OUT/'before.ipynb',4)
source = ROOT/'notebooks/instructor'/name
nb = nbformat.read(source,4)
old_code = [c.source for c in before.cells if c.cell_type=='code' and not c.source.startswith('# Instructor reference:')]
new_code = [c.source for c in nb.cells if c.cell_type=='code' and not c.source.startswith('# Instructor reference:')]
assert sorted(old_code)==sorted(new_code), 'Executable model/plotting cells changed'
for role in ('instructor','student'):
    p=ROOT/'notebooks'/role/name
    n=nbformat.read(p,4)
    nbformat.validate(n)
    for c in n.cells:
        if c.cell_type=='code': compile(c.source,str(p),'exec')
    if role=='student':
        text='\n'.join(c.source for c in n.cells)
        assert '#f3eefb' not in text and 'BEGIN SOLUTION' not in text
        assert '03_04_boudreau_instructor.png' not in text
        assert sum(c.source.count('NotImplementedError') for c in n.cells)==4
        assert all(not c.get('outputs') for c in n.cells)
    else:
        if '--render-only' in sys.argv:
            saved=nbformat.read(OUT/'executed.ipynb',4)
            for cell, previous in zip(n.cells,saved.cells):
                if cell.cell_type=='code':
                    assert cell.source==previous.source
                    cell.outputs=previous.outputs
                    cell.execution_count=previous.execution_count
                    if cell.source.startswith('# Instructor reference:'):
                        from teaching_specification import flux_table_markdown
                        cell.outputs=[nbformat.v4.new_output('display_data',data={'text/markdown':flux_table_markdown()})]
        else:
            NotebookClient(n,timeout=600,kernel_name='esbmtk314',resources={'metadata':{'path':str(p.parent)}}).execute()
            nbformat.write(n,OUT/'executed.ipynb')
            print('Jupyter execution and all notebook scientific audits passed',flush=True)
    for c in n.cells:
        if c.cell_type=='markdown':
            def embed(m):
                alt,target=m.groups()
                data=base64.b64encode((p.parent/target).read_bytes()).decode()
                return f'![{alt}](data:image/png;base64,{data})'
            c.source=re.sub(r'!\[([^]]*)\]\(([^)]+)\)',embed,c.source)
    page,_=HTMLExporter().from_notebook_node(n)
    (OUT/f'{role}.html').write_text(page,encoding='utf-8')
    print('Validated and rendered',role,flush=True)
build_student_notebook(source,OUT/'generated.ipynb')
assert (OUT/'generated.ipynb').read_bytes()==(ROOT/'notebooks/student'/name).read_bytes()
allowed={str(Path('notebooks')/role/name) for role in ('instructor','student')}
changes=[]
for p,digest in json.loads((OUT/'protected.json').read_text()).items():
    if p not in allowed and hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=digest:
        changes.append(p)
assert not changes,changes
print('Exact student regeneration; unrelated notebook/archive/data hashes preserved.')
