from pathlib import Path
import sys
import tempfile
import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
name = '04_pump_strength_OA_OAE.ipynb'
with tempfile.TemporaryDirectory() as folder:
    target = Path(folder)/name
    build_student_notebook(ROOT/'notebooks/instructor'/name,target)
    assert target.read_bytes() == (ROOT/'notebooks/student'/name).read_bytes()
for role in ('instructor','student'):
    n=nbformat.read(ROOT/'notebooks'/role/name,4)
    nbformat.validate(n)
    source='\n'.join(c.source for c in n.cells)
    if role=='student':
        assert '#f3eefb' not in source and 'BEGIN SOLUTION' not in source
        assert 'You are not expected to look up or derive the sediment code.' in source
        assert 'OA shoaling:** near year 2800' not in source
        assert source.count('NotImplementedError')==3
        assert all(not c.get('outputs') for c in n.cells)
    # Inspect teaching Markdown structure independently of saved result tables.
    for c in n.cells:
        if c.cell_type=='code': c.outputs=[]
    html,_=HTMLExporter().from_notebook_node(n)
    soup=BeautifulSoup(html,'html.parser')
    assert len(soup.select('table'))==3
    assert len(soup.select('div[style*="#edf5ff"]'))==4
    assert len(soup.select('div[style*="#f3eefb"]'))==(2 if role=='instructor' else 0)
    assert 'Supplied snowline rule: shoaling and deepening differ' in soup.get_text()
    (ROOT/'tmp/04_consistency'/f'{role}_memory.html').write_text(html,encoding='utf-8')
    print('PASS',role,'validation, exact regeneration, masking and HTML structure')
