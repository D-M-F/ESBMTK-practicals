from pathlib import Path
from html import escape
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
p = ROOT/'notebooks/instructor/03_boudreau_three_box_model.ipynb'
nb = json.loads(p.read_text(encoding='utf-8'))
for cell in nb['cells']:
    cell['source'] = [line.replace('Optional lookup repeats these routes with their paper aliases.',
                                  'Optional lookup summarizes the same routes by unique connection ID.')
                      for line in cell['source']]
c = next(c for c in nb['cells'] if c['id'] == '03-flux-notation')
s = ''.join(c['source'])
if '| Symbol |' in s:
    start, end = s.index('| Symbol |'), s.index('\n\nHere $p_i$')
    rows = [[v.strip() for v in line.strip('|').split('|')] for line in s[start:end].splitlines()]
    head = '<thead><tr><th style="width:30%;text-align:left">Symbol</th><th style="width:70%;text-align:left">Meaning / units</th></tr></thead>'
    body = '<tbody>'+''.join('<tr>'+''.join('<td style="text-align:left;vertical-align:top">'+escape(v)+'</td>' for v in row)+'</tr>' for row in rows[2:])+'</tbody>'
    table = '<table style="width:100%;table-layout:fixed">'+head+body+'</table>'
    c['source'] = (s[:start]+table+s[end:]).splitlines(keepends=True)
p.write_text(json.dumps(nb, indent=1, ensure_ascii=False)+'\n', encoding='utf-8')
build_student_notebook(p, ROOT/'notebooks/student'/p.name)
