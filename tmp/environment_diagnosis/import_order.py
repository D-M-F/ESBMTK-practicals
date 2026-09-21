import crash_capture
import os, subprocess, sys
from pathlib import Path
root = Path.cwd()
probe = root / 'tmp/environment_diagnosis/probe.py'
orders = {
 'jupyter_first': ['zmq', 'IPython', 'ipykernel', 'numpy', 'scipy.linalg', 'matplotlib.pyplot', 'esbmtk'],
 'esbmtk_first': ['esbmtk', 'scipy.linalg', 'numpy', 'matplotlib.pyplot'],
}
for label, modules in orders.items():
    result = subprocess.run([sys.executable, '-u', str(probe), *modules], text=True, capture_output=True, timeout=45)
    text = f'MODE {label}; EXIT {result.returncode} ({result.returncode & 0xffffffff:#x})\n{result.stdout}\n{result.stderr}'
    (root / 'tmp/environment_diagnosis' / (label + '.log')).write_text(text, encoding='utf-8')
    print(text)
