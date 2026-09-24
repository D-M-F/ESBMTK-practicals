from pathlib import Path
import json
import sys
import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
p = ROOT/'notebooks/instructor/03_boudreau_three_box_model.ipynb'
nb = json.loads(p.read_text(encoding='utf-8'))
before = json.loads(json.dumps(nb))
c = next(c for c in nb['cells'] if c['id']=='9d724902')
s = ''.join(c['source'])
old = "Reuse A3's symbols: weathering supplies $W_0$ mol C/yr and $2W_0$ equivalents/yr; $E(t)$ is carbonate export and $D(t)$ is dissolution, both in mol C/yr. Follow their arrows across the boundary."
new = "Reuse A3's symbols: weathering supplies $W_0$ mol C/yr and $2W_0$ equivalents/yr. Net burial $B_{net}(t)$ is carbonate export minus dissolution, in mol C/yr; positive net burial removes material from the active inventories."
assert old in s
s = s.replace(old,new)
old = '2. Write $dC_{atm+ocn}/dt$ and $dA_{ocn}/dt$ as **inputs minus outputs**, using $W_0$, $E(t)$ and $D(t)$. Use the paired DIC/TA effects from your flux table.\n3. Define $B_{net}(t)$ as carbonate export minus dissolution and rewrite both balances using it. Why would subtracting a further burial flux count the same loss twice?'
new = '2. Write $dC_{atm+ocn}/dt$ and $dA_{ocn}/dt$ as **inputs minus outputs**, using weathering $W_0$ and net burial $B_{net}(t)$. Use the paired DIC/TA effects from your flux table.'
assert old in s
s = s.replace(old,new)
start = s.index('**2. Add boundary inputs')
end = s.index('\nThe inventories are constant',start)
s = s[:start]+r'''**2. Balance weathering against net burial.** Using A3's $B_{net}(t)=E(t)-D(t)$,

$$\frac{dC_{atm+ocn}}{dt}=W_0-B_{net}(t),$$
$$\frac{dA_{ocn}}{dt}=2W_0-2B_{net}(t).$$

The factor two follows the model's weathering and carbonate stoichiometry: two TA equivalents per mole C. The balance equations have units mol C/yr and equivalents/yr, respectively. Negative net burial represents a net return from sediment to the dissolved inventories.
'''+s[end:]
c['source'] = s.splitlines(keepends=True)
assert sum(a!=b for a,b in zip(before['cells'],nb['cells']))==1
assert [c for c in before['cells'] if c['cell_type']=='code']==[c for c in nb['cells'] if c['cell_type']=='code']
p.write_text(json.dumps(nb,indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
student=ROOT/'notebooks/student'/p.name
build_student_notebook(p,student)
for path in (p,student):
    n=nbformat.read(path,4)
    nbformat.validate(n)
    cell=next(c for c in n.cells if c.id=='9d724902')
    assert 'further burial' not in cell.source and 'twice' not in cell.source
    if path==student:
        assert 'W_0-B_{net}(t)' not in cell.source
        assert '#f3eefb' not in cell.source
    page,_=HTMLExporter().from_notebook_node(nbformat.v4.new_notebook(cells=[cell]))
    soup=BeautifulSoup(page,'html.parser')
    assert len(soup.select('ol > li'))==2
    (Path(__file__).parent/f'{path.parent.name}_c2.html').write_text(page,encoding='utf-8')
print('C2 now asks two budget questions. Both versions validate and render; solution masking, code and outputs preserved.')
