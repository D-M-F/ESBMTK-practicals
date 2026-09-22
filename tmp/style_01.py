import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook

out = ROOT / 'tmp/01_highlights'
out.mkdir(exist_ok=True)
name = '01_single_box_air_sea_CO2.ipynb'
paths = list((ROOT / 'notebooks').rglob('*.ipynb')) + list((ROOT / 'archive').rglob('*'))
hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in paths if p.is_file()}
(out / 'before_hashes.json').write_text(json.dumps(hashes), encoding='utf-8')
source = ROOT / 'notebooks/instructor' / name
before = source.read_text(encoding='utf-8')
(out / 'instructor_before.ipynb').write_text(before, encoding='utf-8')
nb = json.loads(before)

def panel(body, label, answer=False):
    bg, border, ink = ('#f3eefb', '#7952a8', '#38224f') if answer else ('#edf5ff', '#3977b8', '#173b61')
    return (f'<div style="background-color: {bg}; color: {ink}; border-left: 4px solid {border}; '
            'padding: 12px 16px; margin: 16px 0; border-radius: 4px;">\n\n'
            f'**{label}**\n\n{body.strip()}\n\n</div>')

def mark(term):
    return ('<mark style="background-color: #fff0b3; color: #513d00; '
            f'padding: 0.05em 0.2em; border-radius: 3px;"><strong>{term}</strong></mark>')

texts = {i: ''.join(c['source']) for i, c in enumerate(nb['cells']) if c['cell_type'] == 'markdown'}
texts[0] += ('\n\n**Reading key:** ' + mark('Key term') + ' = concept to notice; '
             '<span style="background-color: #edf5ff; color: #173b61; padding: 2px 6px; '
             'border-radius: 3px;"><strong>Question</strong></span> = student prompt. '
             'Instructor answers use labelled purple panels in the instructor sheet. '
             'These reading cues complement the code labels above.')

# Highlight selected concepts at their introduction, not every occurrence or number.
for i, terms in {
    0: ['total carbon inventory'],
    2: ['system boundary', '**inputs minus outputs**'],
    4: ['dry-air CO2 mole fraction', 'numerical seed'],
    5: ['**Invasion**', '**Outgassing**', 'At equilibrium'],
    6: ['This diagnostic'],
    15: ['**calibration and software-consistency\ncheck**'],
    17: ['settling time'],
}.items():
    for term in terms:
        assert term in texts[i], term
        texts[i] = texts[i].replace(term, mark(term.strip('*')), 1)

# Keep every instructor panel inside the existing solution markers.
for i, text in texts.items():
    texts[i] = re.sub(r'<!-- BEGIN SOLUTION -->\n(.*?)\n<!-- END SOLUTION -->',
                     lambda m: '<!-- BEGIN SOLUTION -->\n' + panel(m[1], 'Instructor answer', True)
                     + '\n<!-- END SOLUTION -->', text, flags=re.S)

def wrap_range(i, start, end, label):
    text = texts[i]
    a = text.index(start)
    b = text.index(end, a) if end else len(text)
    texts[i] = text[:a] + panel(text[a:b], label) + '\n\n' + text[b:]

wrap_range(10, 'Point to the ocean', '<!-- BEGIN SOLUTION -->', 'Question — map and check')
wrap_range(10, '**Write a short prediction', None, 'Question — predict before running')
wrap_range(12, 'Revisit your prediction', '<!-- BEGIN SOLUTION -->', 'Question — diagnose after running')
wrap_range(13, '**Exercise 01.1', '<!-- BEGIN SOLUTION -->', 'Question — calculate and explain')
wrap_range(17, 'Predict the effect', 'Then run the supplied comparison.', 'Question — predict the comparisons')
wrap_range(17, 'Which change alters', None, 'Question — interpret the comparisons')
wrap_range(19, '**Finish 01', '<!-- BEGIN SOLUTION -->', 'Question — final synthesis')

for i, text in texts.items():
    nb['cells'][i]['source'] = text.splitlines(keepends=True)
assert [c for c in nb['cells'] if c['cell_type'] == 'code'] == [
    c for c in json.loads(before)['cells'] if c['cell_type'] == 'code']
source.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
build_student_notebook(source, ROOT / 'notebooks/student' / name)
print('Styled 01 and regenerated its student copy; all code cells are unchanged.')
