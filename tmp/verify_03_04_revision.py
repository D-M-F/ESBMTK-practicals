import hashlib
import json
from pathlib import Path
import re
import sys

import nbformat
from bs4 import BeautifulSoup
from nbconvert import HTMLExporter
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_student_notebooks import build_student_notebook
OUT = ROOT / 'tmp/03_04_revision'
names = ('03_boudreau_three_box_model.ipynb', '04_pump_strength_OA_OAE.ipynb',
         'extensions/05_independent_model.ipynb')
for name in names:
    source = ROOT / 'notebooks/instructor' / name
    nb = nbformat.read(source, 4)
    if '--execute' in sys.argv:
        client = NotebookClient(nb, timeout=600, kernel_name='esbmtk314',
                                resources={'metadata': {'path': str(source.parent)}})
        client.execute()
        nbformat.write(nb, OUT / ('executed_' + source.name))
        print('Jupyter execution passed:',name,flush=True)
    for role in ('instructor','student'):
        p = ROOT / 'notebooks' / role / name
        n = nb if role == 'instructor' else nbformat.read(p, 4)
        nbformat.validate(n)
        source_text = '\n'.join(c.source for c in n.cells)
        if role == 'student':
            assert all(not c.get('outputs') for c in n.cells)
            assert '#f3eefb' not in source_text
            assert 'BEGIN SOLUTION' not in source_text
        for cell in n.cells:
            if cell.cell_type == 'code':
                compile(cell.source, str(p), 'exec')
            if cell.cell_type == 'markdown':
                for target in re.findall(r'\]\(([^)]+)\)', cell.source):
                    if '://' not in target:
                        assert (p.parent / target.split('#')[0]).is_file(), (p,target)
        # Embed local notebook figures in HTML so temp preview paths resolve.
        for cell in n.cells:
            if cell.cell_type == 'markdown':
                import base64
                def image_link(match):
                    alt, target = match.groups()
                    if '://' in target:
                        return match.group(0)
                    image = p.parent / target
                    return f'![{alt}](data:image/png;base64,{base64.b64encode(image.read_bytes()).decode()})'
                cell.source = re.sub(r'!\[([^]]*)\]\(([^)]+)\)', image_link, cell.source)
        page, _ = HTMLExporter().from_notebook_node(n)
        soup = BeautifulSoup(page, 'html.parser')
        assert soup.select('table') or name.startswith('extensions/')
        assert soup.select('div[style*="#edf5ff"]')
        (OUT / f'{role}_{p.stem}.html').write_text(page,encoding='utf-8')
        print('Rendered and validated:',role,name,flush=True)
    dest=OUT/('generated_'+source.name)
    build_student_notebook(source,dest)
    assert dest.read_bytes() == (ROOT/'notebooks/student'/name).read_bytes()

# Preserve unrelated notebooks and all benchmark/archive data. Report any user
# changes separately rather than restoring them from the starting snapshot.
before = json.loads((OUT / 'before_hashes.json').read_text())
allowed = {str(Path('notebooks')/v/n) for v in ('instructor','student') for n in names}
others=[]
for path, digest in before.items():
    if path in allowed:
        continue
    if hashlib.sha256((ROOT/path).read_bytes()).hexdigest() != digest:
        others.append(path)
assert not any(p.startswith(('archive', 'data')) for p in others), others
print('Benchmark/archive hashes unchanged. Other changes during task:',others)
print('All affected student copies match their instructor sources exactly.')
