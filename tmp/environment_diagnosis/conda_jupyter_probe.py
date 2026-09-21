import crash_capture
import os
from pathlib import Path
import nbformat
from nbclient import NotebookClient
root = Path.cwd()
os.environ['IPYTHONDIR'] = str(root / 'tmp/environment_diagnosis/standard_ipython')
# No manual PATH changes and no sitecustomize injection: conda run owns activation.
nb = nbformat.read(root / 'notebooks/instructor/01_single_box_air_sea_CO2.ipynb', as_version=4)
def before(cell, cell_index, **kwargs):
    if cell.cell_type == 'code':
        print(f'Executing cell {cell_index}', flush=True)
NotebookClient(nb, timeout=90, kernel_name='esbmtk314', on_cell_start=before,
               resources={'metadata': {'path': str(root)}}).execute()
nbformat.write(nb, root / 'tmp/environment_diagnosis/conda_jupyter_01.ipynb')
print('PASS: all seven notebook cells executed through the registered ESBMTK314 Jupyter kernel.')
