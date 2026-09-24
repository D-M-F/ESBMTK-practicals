import json
from pathlib import Path
import sys
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from scripts.build_student_notebooks import build_student_notebook
p = root / 'notebooks/instructor/02_two_layer_ocean_carbon_pump.ipynb'
n = json.loads(p.read_text(encoding='utf-8'))
for c in n['cells']:
    if c['id'] == '02-structural-check':
        s = ''.join(c['source'])
        assert ")print('Checks passed:" in s
        c['source'] = s.replace(")print('Checks passed:", ")\nprint('Checks passed:").splitlines(keepends=True)
p.write_text(json.dumps(n, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
build_student_notebook(p, root / 'notebooks/student' / p.name)
