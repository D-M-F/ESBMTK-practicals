import crash_capture
import os, sys
from pathlib import Path
out = Path(__file__).parent / f'process-{os.getpid()}.txt'
out.write_text(f'Executable: {sys.executable}\nArguments: {sys.argv}\nPATH: {os.environ.get("PATH")}\n', encoding='utf-8')
