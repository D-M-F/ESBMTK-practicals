"""Execute instructor notebook code in fresh processes without modifying sources.

Run from an activated ESBMTK environment. Plots go to tmp/notebook_qa for visual
inspection. Student notebooks intentionally stop at exercise placeholders.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [ROOT / "notebooks/00_PyCO2SYS.ipynb"] + sorted(
    (ROOT / "notebooks/instructor").glob("0[1-4]_*.ipynb"))


def execute(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from IPython.display import display
    import nbformat

    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    output = ROOT / "tmp/notebook_qa" / path.stem
    output.mkdir(parents=True, exist_ok=True)
    counter = 0

    def save_figures(*args, **kwargs):
        nonlocal counter
        for number in plt.get_fignums():
            counter += 1
            figure = plt.figure(number)
            figure.savefig(output / f"figure-{counter:02d}.png", dpi=120,
                           bbox_inches="tight")
            plt.close(figure)

    plt.show = save_figures
    namespace = {"__name__": "__main__", "display": display}
    # Exercise notebook path setup as it behaves when opened in Jupyter.
    os.chdir(path.parent)
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type == "code":
            print(f"{path.name}: cell {index}", flush=True)
            exec(compile(cell.source, f"{path.name}:cell-{index}", "exec"), namespace)
    save_figures()
    print(f"PASS {path.name}; {counter} figures", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="*", type=Path)
    parser.add_argument("--child", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.child:
        execute(args.child.resolve())
        return
    for path in args.notebooks or NOTEBOOKS:
        subprocess.run([sys.executable, "-u", str(Path(__file__).resolve()),
                        "--child", str(path.resolve())], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
