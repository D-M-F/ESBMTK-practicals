# Student setup with Anaconda

Already using Anaconda or Miniconda? Use the supplied
[`environment-anaconda.yml`](../environment-anaconda.yml); you do not need uv
or a separate Python installation. This creates a dedicated `esbmtk-practicals`
environment alongside your existing environments and R installation.

This is an alternative installation recipe for instructor/student pilots.
Python 3.14 and the ESBMTK/PyCO2SYS versions match the teaching reference, but
the full dependency set is not locked. A fresh installation on Windows/macOS
still needs to be checked before distributing it as a verified course setup.
On 2026-09-21, YAML/requirement validation and a Windows/Python 3.14 pip dry run
with installed packages ignored and prebuilt packages required both passed.
That verifies package resolution, not installation or model execution in a new
environment. The numerical check below passed in the activated reference environment.

## First setup

Download and extract the complete course folder. On Windows, open **Anaconda
Prompt** from the Start menu. On macOS/Linux, open a terminal where `conda`
works. Change into the course folder (replace the example path):

```text
cd "path/to/ESBMTK-practicals"
```

In Windows Anaconda Prompt, use `cd /d "D:\path\to\ESBMTK-practicals"` if
you also need to change drive. Run:

```text
conda env create -f environment-anaconda.yml
conda activate esbmtk-practicals
python -m pip check
python -m ipykernel install --sys-prefix --name esbmtk-practicals --display-name "ESBMTK practicals"
python -m jupyterlab
```

The initial installation requires internet access. Conda installs Python and
pip, then pip installs the course packages declared in the same file. The
kernel command registers this Python inside the new environment, rather than
replacing a globally registered kernel.

JupyterLab opens in your browser. Open `notebooks/student/`, then choose
**ESBMTK practicals** as the notebook kernel. If a notebook asks for the
instructor's `ESBMTK (Python 3.14)` kernel, select **ESBMTK practicals** instead.
Run cells with Shift+Enter. Student exercise placeholders are intentional and
must be completed as you work through the notebook.

If `esbmtk-practicals` already exists, activate it and check it rather than
re-running creation. To make a separate pilot environment without changing
an existing one, use `conda env create -f environment-anaconda.yml -n esbmtk-practicals-pilot`
and activate that name in the following commands.

## Check before class

From the activated environment, run this small numerical check. An import-only
check can miss a Windows numerical-library loading problem:

```text
python -c "import sys, numpy as np; print(sys.executable); np.testing.assert_allclose(np.linalg.solve(np.eye(2), np.ones(2)), [1, 1]); print('Numerical check passed')"
```

Inside a Jupyter notebook, `import sys; print(sys.executable)` should identify
the same environment. If it does not, select **ESBMTK practicals** as the kernel.
For an instructor pilot, run the existing model checks and notebook checker
from the course folder:

```text
python -m unittest discover -s tests -p test_simple_models.py -v
python scripts/check_notebooks.py
```

These pilot checks are instructor preparation, not additional student exercises.

## Restart JupyterLab after shutting it down

Run these commands only when JupyterLab is no longer running, for example after
restarting your laptop. Open Anaconda Prompt (or your Conda-enabled terminal),
enter the course folder, then run:

```text
conda activate esbmtk-practicals
python -m jupyterlab
```

If JupyterLab is already running, open existing notebooks in its file browser
or create one via **File > New > Notebook**, then select the course kernel.
**No terminal command is needed for each notebook.** Closing a browser tab
usually leaves JupyterLab running. Save your work before shutting it down.

As an alternative way to restart JupyterLab, from the course folder:

```text
conda run -n esbmtk-practicals --no-capture-output python -m jupyterlab
```

Launch Jupyter from this environment so its Python and library paths agree.
Selecting an environment's `python.exe` by absolute path is not equivalent to
activation on Windows. Existing Anaconda users can keep their familiar tools;
Navigator is optional, and these commands make the selected environment explicit.

## Instructor maintenance

The YAML uses Conda for Python/pip and pip for the complete scientific/Jupyter
stack. Avoid subsequently installing Conda copies of NumPy, SciPy or other
pip-owned packages into this environment. For dependency changes, revise the
recipe and verify a fresh environment. This follows
[Conda's guidance on combining Conda and pip](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#using-pip-in-an-environment).

The recipe intentionally has no machine-specific prefix or Windows-only build
strings. It is not a lockfile: package versions other than the explicitly pinned
ones can change. Freeze and test the resolved package set for each supported
platform before a course release; do not export the existing instructor
environment's stale overlapping NumPy metadata as the student specification.

See [the environment proposal](environment_setup_proposal.md) for the uv
alternative and the verified Windows crash diagnosis. Students should use one
setup route for this course, not combine uv and Conda in the same environment.
