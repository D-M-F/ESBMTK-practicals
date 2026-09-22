import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
path = ROOT / 'notebooks/instructor/01_single_box_air_sea_CO2.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
for c in nb['cells']:
    text = ''.join(c['source'])
    text = text.replace('Both plot axes use\npCO2 in **µatm**;',
                        'Both seawater and atmosphere curves use\npCO2 in **µatm**;')
    text = text.replace('Keep your TA calculation and explanations in this notebook;',
                        'Keep your calculations, curves and explanations in this notebook;')
    c['source'] = text.splitlines(keepends=True)
path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
build_student_notebook(path, ROOT / 'notebooks/student' / path.name)
