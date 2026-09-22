# Set up with Anaconda

For students who already use Anaconda or Miniconda on Windows, macOS or Linux.

**What you are setting up:** an *environment* is a separate Python installation with its own packages. Conda creates and activates the course environment, named `esbmtk-practicals`. JupyterLab is the interface you open in your browser; a *kernel* is the Python process that runs notebook cells. Your R installation stays unchanged. You do not need uv or another Python installer.

## 1  Download the course and open a terminal

Download the complete course folder from your instructor and extract the ZIP. On Windows, right-click it and choose **Extract All**. On macOS, double-click it. Work in the extracted folder, not inside the ZIP.

The folder must contain **environment-anaconda.yml**, **scripts**, **notebooks** and **data**, together with the other supplied course files. The YAML file is a package recipe supplied by your instructor; you do not need to write it.

**Windows:** click Start or the Windows search bar, type **Anaconda Prompt**, and open it. This terminal is already prepared to use Conda. A terminal is simply a window where you type commands. You do not need to open Navigator first.

**macOS:** press **Command+Space**, type **Terminal**, and press Return. **Linux:** open Terminal (often Ctrl+Alt+T). Use a terminal already configured for your Anaconda or Miniconda installation.

Type this command and press Enter:

```text
conda --version
```

A version number confirms Conda is available. If it is not recognised, use Anaconda Prompt on Windows. On macOS/Linux, ask your instructor to help connect your existing Conda installation to the terminal.

## 2  Know where to type commands

Run terminal commands **one line at a time**, pressing Enter and waiting for each to finish. They are not R code and do not go in RStudio or a notebook cell. Do not copy the prompt before a command, such as `(base) C:\Users\Alex>`.

The first installation needs internet access. **Pilot status:** package resolution was checked on Windows/Python 3.14; a fresh Anaconda installation and cross-platform pilots remain outstanding. The separate uv route has its own verification record. Reference: [Conda environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

<!-- PAGEBREAK -->

# Install and open the course

Keep using the Anaconda Prompt or Terminal window from page 1.

## 3  Tell the terminal which folder to use

The terminal's **current folder** can differ from the folder shown in your file browser. `cd` means change directory (folder). If Alex extracted the course into Downloads, the command would be:

**Windows Anaconda Prompt:** `/d` also changes the drive if needed.

```text
cd /d "C:\Users\Alex\Downloads\ESBMTK-practicals"
```

**macOS / Linux:**

```text
cd "$HOME/Downloads/ESBMTK-practicals"
```

Use your actual folder name and location, including a suffix such as `-main`. On Windows, open the folder in File Explorer, click its address bar and copy that path between the quotes after `cd /d`.

**Check the folder:** on Windows, run `cd` by itself to print the location, then `dir` to list files. On macOS/Linux, use `pwd`, then `ls`. Find **environment-anaconda.yml**, **scripts**, **notebooks** and **data** before continuing. “From the course folder” means this terminal location.

## 4  Create, activate and check the environment

```text
conda env create -f environment-anaconda.yml
conda activate esbmtk-practicals
python -m pip check
python scripts/check_environment.py
```

Creation downloads Python and the course packages; wait for it to finish. Activation selects them for this terminal; the prompt should show **(esbmtk-practicals)**. If this course environment already exists, skip creation and run the other three commands.

Expect **No broken requirements found**, then **Environment check passed. Next: start JupyterLab.** The second check tests numerical calculations, chemistry, workbook access and plotting. Stop and seek help if either check fails.

## 5  Register the course kernel and start JupyterLab

Stay in this activated terminal and course folder. Register the kernel once:

```text
python -m ipykernel install --sys-prefix --name esbmtk-practicals
python -m jupyterlab
```

JupyterLab opens in your browser. Keep the terminal open; its prompt will not return while the server runs. If no browser opens, copy the local `http://localhost:.../lab` or `http://127.0.0.1:.../lab` link printed there into your browser. Keep the full link private.

<!-- PAGEBREAK -->

# Check success and start working

The steps below take place in JupyterLab, then in the terminal when you finish.

## 6  Confirm that JupyterLab uses the course Python

Click **File > New > Notebook** and choose **esbmtk-practicals** (or **ESBMTK practicals** if registered with the earlier guide). Paste this code into the first cell, then press **Shift+Enter**:

```python
import sys
import numpy as np
import esbmtk
import PyCO2SYS
print(sys.executable)
np.testing.assert_allclose(np.linalg.solve(np.eye(2), np.ones(2)), [1, 1])
print("Setup check passed")
```

The Python path should identify the `esbmtk-practicals` environment and match the interpreter printed by the terminal check. Expect **Setup check passed**. **If both terminal checks and this notebook check passed, setup is complete.** You do not repeat creation or kernel registration each time.

## Open or create notebooks while JupyterLab is running

Use the left file browser to open **notebooks/student/**, then double-click a course notebook. If it asks for the instructor's ESBMTK314 kernel, choose your course kernel instead. Create another notebook via **File > New > Notebook**. No terminal command is needed for each notebook. Save with Ctrl+S (Cmd+S on macOS). Marked exercise placeholders are intentional.

## When you finish: save and shut down

Save your notebooks. Return to the terminal running JupyterLab, press **Ctrl+C**, and, if asked to shut down, type **y** and press Enter. Wait for the normal prompt to return, then close the browser tab and terminal. This stops notebook kernels: variables in memory are lost, but saved notebooks remain on disk.

**Closing the browser tab alone does not normally stop JupyterLab.** Reopen the local link still shown in its terminal if you only closed the tab; you do not need another server.

## Next time: open JupyterLab again

Open Anaconda Prompt or your Conda-enabled Terminal, repeat `cd` to the course folder (page 2), then run:

```text
conda activate esbmtk-practicals
python -m jupyterlab
```

Do this only when the server has stopped, including after restarting your laptop. Open your saved notebooks and rerun the cells needed to recreate variables.

## If a step fails

**File not found:** check the terminal folder (page 2). **Wrong Python or missing package:** activate the course environment, launch Jupyter there and select its kernel. **Windows Python crash:** use the activated prompt. For other errors, send your instructor the full error text, command and operating system.

<!-- INSTRUCTOR NOTES -->

## Instructor verification and maintenance

The three pages above are the source for the student PDF. The following notes
are instructor preparation, not additional student exercises.

Python 3.14 and the ESBMTK/PyCO2SYS pins match the teaching reference, but the
full dependency set is not locked. On 2026-09-21, YAML/requirement validation
and a Windows/Python 3.14 pip dry run with installed packages ignored and
prebuilt packages required passed. This verifies resolution, not a fresh
Anaconda installation or model execution. The shared environment checker also
passes in the activated reference environment; it does not establish that a
new Anaconda recipe has been tested on every platform.

For an isolated pilot, create the environment with
`conda env create -f environment-anaconda.yml -n esbmtk-practicals-pilot`, then
activate that name in subsequent commands. Select its registered kernel and
verify the matching interpreter path. Run these model checks from the course folder:

```text
python -m unittest discover -s tests -p test_simple_models.py -v
python scripts/check_notebooks.py
```

For an environment-aware launch from a terminal with Conda available, an
alternative is `conda run -n esbmtk-practicals --no-capture-output python -m jupyterlab`.
Selecting a Conda environment's `python.exe` by absolute path alone does not
activate Windows DLL lookup. See the [environment diagnosis](environment_setup_proposal.md).

The YAML uses Conda for Python/pip and pip for the complete scientific/Jupyter
stack. Avoid adding Conda copies of those pip-owned packages later. Revise the
recipe and verify a fresh environment for dependency changes, following
[Conda's pip guidance](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#using-pip-in-an-environment).
The recipe has no machine-specific prefix or Windows-only build strings; it is
not a lockfile. Freeze and test the resolved package set for supported platforms
before release. Do not export the instructor environment's stale overlapping
NumPy metadata. Students should use one setup route for this course.
