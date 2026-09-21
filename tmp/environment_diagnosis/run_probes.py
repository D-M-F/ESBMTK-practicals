import os, subprocess, sys
from pathlib import Path
import crash_capture
root = Path.cwd()
probe = root / 'tmp/environment_diagnosis/probe.py'
modules = ['numpy', 'scipy.linalg', 'matplotlib.pyplot', 'PyCO2SYS', 'esbmtk', 'zmq', 'IPython', 'ipykernel']
for mode in ('inherited_path', 'environment_path'):
    env = os.environ.copy()
    if mode == 'environment_path':
        prefix = Path(sys.executable).parent
        env['PATH'] = os.pathsep.join(str(prefix / p) for p in ('', 'Library/bin', 'Scripts')) + os.pathsep + env['PATH']
    result = subprocess.run([sys.executable, '-u', str(probe), *modules], env=env, text=True, capture_output=True, timeout=45)
    text = f'MODE {mode}; EXIT {result.returncode} ({result.returncode & 0xffffffff:#x})\n{result.stdout}\n{result.stderr}'
    (root / 'tmp/environment_diagnosis' / (mode + '.log')).write_text(text, encoding='utf-8')
    print(text)
