import crash_capture
import importlib, sys
for name in sys.argv[1:]:
    print('IMPORT', name, flush=True)
    module = importlib.import_module(name)
    print('OK', name, getattr(module, '__file__', None), flush=True)
print('ALL IMPORTS PASS', flush=True)
