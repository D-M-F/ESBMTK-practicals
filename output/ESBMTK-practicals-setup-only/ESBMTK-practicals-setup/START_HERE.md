# Start here: ESBMTK setup package

This temporary package lets you install and test the software before the
practical exercises are released. It contains no exercise notebooks or course
data. When the exercises are ready, your instructor will send a link to the
complete GitHub repository.

Keep this folder until you have successfully opened the complete course
repository.

## 1  Choose one setup route

Use **uv** if you do not already use Python or Anaconda. Open
`SETUP_WITH_UV.pdf` and follow it from the beginning.

Use **Anaconda** only if you already have Anaconda or Miniconda and prefer to
manage the course through Conda. Open `SETUP_WITH_ANACONDA.pdf`.

Complete one route only. Both routes install the same course software.

## 2  Confirm the setup in JupyterLab

After the terminal check passes and JupyterLab opens, double-click
`JUPYTER_BASICS.ipynb`. Follow the notebook from top to bottom and use **Run >
Run All Cells** once. The last cell should print:

```text
Jupyter setup check passed
```

The notebook introduces the keyboard shortcuts used during the practicals and
tests Python, numerical calculations, plotting and access to a small Excel
workbook. The workbook contains no exercise data.

## 3  Open this setup folder again

The installation guide for your route contains a **Next time** section. You do
not reinstall Python or recreate the environment each time. Always start
JupyterLab from a terminal whose current folder is this extracted setup folder.

## 4  Move to the complete course repository later

Download the complete repository ZIP from the link supplied by your instructor
and extract it into a **new folder**. Do not extract it over this setup folder,
and do not copy `.venv` into the new folder.

Open a terminal and change into the new complete course folder, using the same
folder-navigation method as in your setup guide. Then follow the route you used
below.

### uv transition

Run these commands from the new complete course folder:

```text
uv sync --locked
uv run --locked python scripts/check_environment.py
uv run --locked python -m ipykernel install --sys-prefix --name esbmtk-practicals
uv run --locked jupyter lab
```

uv stores `.venv` inside each project folder. The first command therefore
creates a new environment for the complete repository, while normally reusing
packages already present in uv's download cache.

### Anaconda transition

Run these commands from the new complete course folder:

```text
conda activate esbmtk-practicals
python scripts/check_environment.py
python -m jupyterlab
```

The named Conda environment is independent of the folder, so you normally reuse
the environment created during this setup. Run
`conda env update -f environment-anaconda.yml` only if your instructor says the
course dependencies changed.

After the check passes, use JupyterLab's file browser to open the course
notebooks supplied in the complete repository.
