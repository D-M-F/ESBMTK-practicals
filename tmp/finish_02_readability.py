import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
path = ROOT / 'notebooks/instructor/02_two_layer_ocean_carbon_pump.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
definition = ('A **stationary state** has no further change in any reservoir inventory, even\n'
              'though individual transfers continue. Stars denote stationary concentrations:\n'
              '$DIC_s^*$ and $DIC_d^*$.')
for c in nb['cells']:
    text = ''.join(c['source'])
    if c['id'] == '63486c2f':
        text = text.replace('### A4. Explain the structural check',
                            '### A4. Explain the structural check\n\n' + definition)
    elif c['id'] == '02-pump-derivation':
        text = text.replace('\n\n' + definition, '')
        text = text.replace('ratio. Export is reported in Tmol C/yr, where 1 Tmol = $10^{12}$ mol.',
                            'ratio. The output uses Tmol C/yr for export and Pmol C for inventories:\n'
                            '1 Tmol = $10^{12}$ mol and 1 Pmol = $10^{15}$ mol.')
    elif c['id'] == '9aa6988c':
        text = text.replace('\n   The printed unit Pmol C means $10^{15}$ mol C.', '')
    c['source'] = text.splitlines(keepends=True)
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
build_student_notebook(path, ROOT / 'notebooks/student' / path.name)
