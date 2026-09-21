import crash_capture
import os, sys, traceback
from pathlib import Path
import nbformat
from nbclient import NotebookClient
root = Path.cwd()
prefix = Path(sys.executable).parent
os.environ['PATH'] = os.pathsep.join(str(prefix / p) for p in ('', 'Library/bin', 'Scripts')) + os.pathsep + os.environ['PATH']
os.environ['PYTHONPATH'] = str(root / 'tmp/environment_diagnosis')
os.environ['IPYTHONDIR'] = str(root / 'tmp/environment_diagnosis/ipython')
nb = nbformat.read(root / 'notebooks/instructor/01_single_box_air_sea_CO2.ipynb', as_version=4)
def before(cell, cell_index, **kwargs):
    if cell.cell_type == 'code':
        print(f'RUNNING CELL {cell_index}: {cell.source[:150]!r}', flush=True)
try:
    NotebookClient(nb, timeout=60, kernel_name='python3', on_cell_start=before, resources={'metadata': {'path': str(root)}}).execute()
    print('ALL NOTEBOOK CELLS PASSED', flush=True)
finally:
    nbformat.write(nb, root / 'tmp/environment_diagnosis/kernel_result.ipynb')
