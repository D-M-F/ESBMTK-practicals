import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

ratio = r'r_{\mathrm{ocn/atm}}'
baseline = r'r_{\mathrm{ocn/atm},0}'

def rename(text):
    text = text.replace('R_0', baseline)
    return re.sub(r'\bR\b', lambda _: ratio, text)

p = ROOT / 'notebooks/instructor/02_two_layer_ocean_carbon_pump.ipynb'
before = json.loads(p.read_text(encoding='utf-8'))
n = json.loads(p.read_text(encoding='utf-8'))
for c in n['cells']:
    if c['id'] in ('2acb80bd', '9aa6988c'):
        text = rename(''.join(c['source']))
        text = text.replace(
            f'**Notation:** ${ratio}$ is the whole-ocean/atmosphere inventory ratio; it differs\n'
            "from the lecture's seawater equilibrium capacity $F$.",
            f'**Notation:** ${ratio}$ is the ocean/atmosphere carbon inventory ratio.\n'
            "Reserve $R$ for the Revelle factor; $F$ denotes the lecture's seawater\n"
            'equilibrium capacity.')
        c['source'] = text.splitlines(keepends=True)
assert [c for c in n['cells'] if c['cell_type']=='code'] == [c for c in before['cells'] if c['cell_type']=='code']
p.write_text(json.dumps(n, indent=1, ensure_ascii=False)+'\n', encoding='utf-8')
build_student_notebook(p, ROOT / 'notebooks/student' / p.name)

p = ROOT / 'ref/design.md'
t = p.read_text(encoding='utf-8')
a, b = t.index('## 02 -'), t.index('## 03 -')
section = rename(t[a:b])
section = section.replace(f'Use {ratio} for', f'Use ${ratio}$ for')
section = section.replace("the lecture's seawater equilibrium capacity F;", "the lecture's seawater equilibrium capacity F; reserve R for the Revelle factor and")
t = t[:a] + section + t[b:]
p.write_text(t, encoding='utf-8')

p = ROOT / 'TEACHING_GOALS.md'
t = p.read_text(encoding='utf-8').replace(
    "Define inventory ratio R separately from the lecture's capacity F, with the",
    f"Use ${ratio}$ for the inventory ratio, reserving R for the Revelle\nfactor and F for the lecture's capacity, with the")
p.write_text(t, encoding='utf-8')
print('Renamed inventory-ratio notation; regenerated student 02. Code and outputs unchanged.')
