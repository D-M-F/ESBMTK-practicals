from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

p = ROOT/'notebooks/instructor/03_boudreau_three_box_model.ipynb'
nb = json.loads(p.read_text(encoding='utf-8'))
original = json.loads(json.dumps(nb))
cell = next(c for c in nb['cells'] if c['id'] == '72dd4cbb')
text = ''.join(cell['source'])
paragraph = '`scale_with_concentration` names a specific proportional law. Saying a flux depends on changing model values is broader: `gasexchange` uses both atm and ocn CO2, and the supplied dissolution calculation also uses sediment history. These are different calculations, even though their fluxes can all change during a run.\n\n'
assert paragraph in text
cell['source'] = text.replace(paragraph, '').splitlines(keepends=True)
assert [c for c in nb['cells'] if c['cell_type']=='code'] == [c for c in original['cells'] if c['cell_type']=='code']
assert sum(a != b for a,b in zip(nb['cells'],original['cells'])) == 1
p.write_text(json.dumps(nb, indent=1, ensure_ascii=False)+'\n', encoding='utf-8')
build_student_notebook(p, ROOT/'notebooks/student'/p.name)
print('Removed only the B2 comparison paragraph; all code and outputs unchanged. Regenerated student 03.')
