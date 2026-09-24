from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
p = ROOT/'notebooks/instructor/03_boudreau_three_box_model.ipynb'
nb = json.loads(p.read_text(encoding='utf-8'))
for c in nb['cells']:
    s = ''.join(c['source'])
    if c['id'] == '5998b397':
        s = s.replace('and sediment snowline, along with auxiliary chemistry values.',
                      'and the **snowline** (the deepest boundary of existing reactive carbonate sediment), along with auxiliary chemistry values.')
    if c['id'] == '8df51381':
        s = s.replace('The **snowline** is the deepest boundary of existing reactive carbonate sediment. It records sediment history; the module has no explicit sediment-carbon inventory.',
                      'Its snowline records sediment history; the module has no explicit sediment-carbon inventory.')
    if c['id'] == '03-flux-hints':
        s = s.replace('Reference: biological TA effects, weathering and flux laws', 'Reference: biological TA effects and weathering')
        s = s.replace("\nA constant coefficient does not imply a constant flux: in 02, $kDIC_s(t)$ scales with surface DIC even when $k$ stays fixed. Gas exchange and dissolution also respond to changing model values, but use their own calculations rather than simple scaling with source concentration.\n", '')
    c['source'] = s.splitlines(keepends=True)
p.write_text(json.dumps(nb, indent=1, ensure_ascii=False)+'\n', encoding='utf-8')
build_student_notebook(p, ROOT/'notebooks/student'/p.name)
