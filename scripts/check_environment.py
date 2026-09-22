"""Small pre-class check: run with `uv run --locked python scripts/check_environment.py`."""

from io import BytesIO
from pathlib import Path
import sys


def main():
    import numpy as np
    import scipy.linalg
    import PyCO2SYS as pyco2
    import esbmtk
    import gsw
    import pandas as pd
    import openpyxl
    import jupyterlab
    import ipykernel
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    root = Path(__file__).resolve().parents[1]
    print(f"Python: {sys.version.split()[0]}")
    print(f"Interpreter: {sys.executable}")
    np.testing.assert_allclose(np.linalg.solve(np.eye(2), np.ones(2)), [1, 1])
    np.testing.assert_allclose(scipy.linalg.solve(np.eye(2), np.ones(2)), [1, 1])
    sample = pyco2.sys(par1=2300, par1_type=1, par2=2000, par2_type=2,
                      temperature=15, salinity=35)
    assert np.isfinite(float(sample["pH"]))
    assert np.isfinite(float(gsw.rho(35, 15, 0)))
    workbook = openpyxl.load_workbook(
        root / "data/Boudreau_2010/model_definition.xlsx", read_only=True,
    )
    try:
        assert workbook.sheetnames
    finally:
        workbook.close()
    figure = Figure(figsize=(2, 2))
    FigureCanvasAgg(figure)
    figure.subplots().plot([0, 1], [0, 1])
    image = BytesIO()
    figure.savefig(image, format="png")
    assert image.getbuffer().nbytes > 0
    print("Numerical libraries, chemistry, workbook and plotting: OK")
    print("Environment check passed. Next: start JupyterLab.")


if __name__ == "__main__":
    main()
