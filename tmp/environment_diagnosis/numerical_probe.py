import crash_capture
import importlib, sys
import numpy as np
print('NUMPY', np.__version__, np.__file__, flush=True)
print('numpy solve', np.linalg.solve(np.eye(2), np.ones(2)), flush=True)
import scipy.linalg
print('scipy solve', scipy.linalg.solve(np.eye(2), np.ones(2)), flush=True)
print('IMPORT GSW', flush=True)
import gsw
print('gsw density', gsw.rho(35, 15, 0), flush=True)
print('IMPORT ESBMTK', flush=True)
from esbmtk import SeawaterConstants
print('esbmtk density', SeawaterConstants.get_density(None, 35, 16, 0), flush=True)
print('PASS', flush=True)
