from pathlib import Path
import sys
import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
name = '03_boudreau_three_box_model.ipynb'
source = ROOT/'notebooks/instructor'/name
student = ROOT/'notebooks/student'/name
before_execution = nbformat.read(OUT/'executed.ipynb', 4)
nb = nbformat.read(source, 4)
assert [c.source for c in nb.cells if c.cell_type=='code'] == [c.source for c in before_execution.cells if c.cell_type=='code']
for p in (source, student):
    n = nbformat.read(p, 4)
    nbformat.validate(n)
    text = '\n'.join(c.source for c in n.cells)
    assert 'Saying a flux depends on changing model values is broader' not in text
    if p == student:
        assert text.count('NotImplementedError') == 4
        assert '#f3eefb' not in text
        assert all(not c.get('outputs') for c in n.cells)
    b2 = next(c for c in n.cells if c.id == '72dd4cbb')
    html, _ = HTMLExporter().from_notebook_node(nbformat.v4.new_notebook(cells=[b2]))
    soup = BeautifulSoup(html, 'html.parser')
    assert 'coefficient × current source concentration' in soup.get_text()
    assert 'Question — implement your water arrows' in soup.get_text()
    assert len(soup.find_all('table')) == 1
    (OUT/f'{p.parent.name}_b2.html').write_text(html, encoding='utf-8')
build_student_notebook(source, OUT/'generated.ipynb')
assert (OUT/'generated.ipynb').read_bytes() == student.read_bytes()
print('PASS: notebook validity, exact generation, masking, rendered B2 table/question; code matches the previously audited execution.')
