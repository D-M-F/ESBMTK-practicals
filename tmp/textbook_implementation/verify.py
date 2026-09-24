import base64
import hashlib
import json
from pathlib import Path
import re
import sys

import nbformat
from nbconvert import HTMLExporter
from nbclient import NotebookClient
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
OUT = Path(__file__).resolve().parent
from scripts.build_student_notebooks import build_student_notebook

for source in sorted((ROOT/'notebooks/instructor').glob('0[1-4]*.ipynb')):
    nb = nbformat.read(source, 4)
    before = nbformat.read(OUT/source.name, 4)
    old_code = {c.id: c.source for c in before.cells if c.cell_type == 'code'}
    now_code = {c.id: c.source for c in nb.cells if c.cell_type == 'code'}
    assert all(now_code[k] == v for k, v in old_code.items())
    assert set(now_code) - set(old_code) <= {'03-carbonate-plane-key', '03-carbonate-plane-plot'}
    if source.name.startswith('03'):
        if '--skip-kernel' in sys.argv:
            executed = nbformat.read(OUT/('executed_'+source.name), 4)
            outputs = {c.id: c for c in executed.cells if c.cell_type == 'code'}
            for c in nb.cells:
                if c.cell_type == 'code':
                    assert c.source == outputs[c.id].source
                    c.outputs = outputs[c.id].outputs
                    c.execution_count = outputs[c.id].execution_count
        else:
            NotebookClient(nb, timeout=600, kernel_name='esbmtk314',
                           resources={'metadata': {'path': str(source.parent)}}).execute()
            nbformat.write(nb, OUT/('executed_'+source.name))
            print('03 Jupyter kernel execution passed', flush=True)
    for role in ('instructor', 'student'):
        path = ROOT/'notebooks'/role/source.name
        n = nb if role == 'instructor' else nbformat.read(path, 4)
        nbformat.validate(n)
        full = '\n'.join(c.source for c in n.cells)
        if role == 'student':
            assert all(not c.get('outputs') for c in n.cells)
            assert '#f3eefb' not in full and 'BEGIN SOLUTION' not in full
            assert 'show_processes=True' not in full
            assert 'bicarbonate contributes +1' not in full
            assert 'flux anomalies are zero' not in full
        for c in n.cells:
            if c.cell_type == 'code':
                compile(c.source, str(path), 'exec')
            elif c.cell_type == 'markdown':
                for target in re.findall(r'\]\(([^)]+)\)', c.source):
                    if '://' not in target:
                        assert (path.parent / target.split('#')[0]).is_file(), target
                def embed(m):
                    alt, target = m.groups()
                    if '://' in target:
                        return m.group(0)
                    b64 = base64.b64encode((path.parent/target).read_bytes()).decode()
                    return f'![{alt}](data:image/png;base64,{b64})'
                c.source = re.sub(r'!\[([^]]*)\]\(([^)]+)\)', embed, c.source)
        page, _ = HTMLExporter().from_notebook_node(n)
        soup = BeautifulSoup(page, 'html.parser')
        assert soup.select('div[style*="#edf5ff"]')
        assert bool(soup.select('div[style*="#f3eefb"]')) == (role == 'instructor')
        (OUT/f'{role}_{source.stem}.html').write_text(page, encoding='utf-8')
    target = OUT/('generated_'+source.name)
    build_student_notebook(source, target)
    assert target.read_bytes() == (ROOT/'notebooks/student'/source.name).read_bytes()
    print('Validated, rendered and masking/generation checked:', source.name, flush=True)

import numpy as np
import PyCO2SYS as pyco2
from esbmtk import Q_
from presets import load_boudreau_parameters
p = load_boudreau_parameters()
b = p['boxes']['L_b']
d, a = (Q_(b[k]).to('umol/kg').magnitude for k in ('dic', 'ta'))
pc = pyco2.sys(par1=a+np.array([0, 0, -40, 40]), par1_type=1,
               par2=d+np.array([0, -20, -20, 20]), par2_type=2,
               temperature=b['temperature'], salinity=b['salinity'],
               pressure=10*b['pressure'], opt_k_carbonic=p['opt_k_carbonic'],
               opt_pH_scale=p['opt_pH_scale'])['pCO2']
assert pc[1] < pc[0] < pc[2] and pc[3] < pc[0]
print('Local pCO2: reference, POC, formation, dissolution (µatm):', pc)
print('Pressure:', b['pressure'], 'bar =', 10*b['pressure'], 'dbar')

manifest = json.loads((ROOT/'tmp/03_04_revision/before_hashes.json').read_text())
protected = {k:v for k,v in manifest.items() if k.startswith(('data', 'archive')) or
             (k.startswith('notebooks') and '00_PyCO2SYS' in k)}
for name, digest in protected.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
print('Protected data/archive/00 hashes unchanged:', len(protected))
