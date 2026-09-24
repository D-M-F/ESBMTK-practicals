import json, os, sys
from pathlib import Path
import nbformat
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from IPython.display import display
from nbconvert import HTMLExporter
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
OUT = ROOT / 'tmp/04_consistency'
p = ROOT / 'notebooks/instructor/04_pump_strength_OA_OAE.ipynb'
nb = nbformat.read(p, 4)
ns = {'__name__':'__main__','display':display}
figures = []
def save(*args, **kwargs):
    for num in plt.get_fignums():
        fig = plt.figure(num)
        dest = OUT / f'figure-{len(figures)+1:02}.png'
        fig.savefig(dest, dpi=120, bbox_inches='tight')
        figures.append(dest.name)
        plt.close(fig)
plt.show = save
os.chdir(p.parent)
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code':
        print('Executing cell', i, flush=True)
        exec(compile(cell.source, f'04:cell-{i}', 'exec'), ns)
save()
cases = ns['fixed_cases']
from teaching_plots import response_summary
metrics = {}
for label in ('OA', 'OAE'):
    case = cases[label]
    flux, time = case.teaching_signal_flux, case.teaching_signal_time
    row = response_summary(case, cases['control'])
    row.update(forcing_peak_year=float(time[np.argmax(flux)]), final_forcing=float(flux[-1]),
               max_depth_gap=float(np.max(case.D_b.zsnow.c-case.D_b.zcc.c)))
    for year in (1800, 2100, 2300, 2800, 3800):
        i = np.argmin(abs(case.time-year))
        row[str(year)] = {k:float(getattr(case.D_b, k).c[i]) for k in ('zsat','zcc','zsnow','Fburial','Fdiss')}
    metrics[label] = row
(OUT / 'metrics.json').write_text(json.dumps(metrics, indent=2, default=float))
print(json.dumps(metrics, indent=2, default=float), flush=True)
print('PASS all notebook cells and audits;', len(figures), 'figures', flush=True)
