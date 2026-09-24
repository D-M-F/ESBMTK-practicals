# Set up with Anaconda

For students who already use Anaconda or Miniconda on Windows, macOS or Linux.

**What you are setting up:** an *environment* is a separate Python installation with its own packages. Conda creates and activates the course environment, named `esbmtk-practicals`. JupyterLab is the interface you open in your browser; a *kernel* is the Python process that runs notebook cells. Your R installation stays unchanged. You do not need uv or another Python installer.

## 1  Download the supplied folder and open a terminal

Download the folder supplied by your instructor and extract the ZIP. It may be the setup-only package or, later, the complete course repository. On Windows, right-click it and choose **Extract All**. On macOS, double-click it. Work in the extracted folder, not inside the ZIP.

The folder must contain **environment-anaconda.yml**, **scripts**, **setup_assets** and **JUPYTER_BASICS.ipynb**. The YAML file is a package recipe supplied by your instructor; you do not need to write it.

**Windows:** click Start or the Windows search bar, type **Anaconda Prompt**, and open it. This terminal is already prepared to use Conda. A terminal is simply a window where you type commands. You do not need to open Navigator first.

**macOS:** press **Command+Space**, type **Terminal**, and press Return. **Linux:** open Terminal (often Ctrl+Alt+T). Use a terminal already configured for your Anaconda or Miniconda installation.

Type this command and press Enter:

```text
conda --version
```

A version number confirms Conda is available. If it is not recognised, use Anaconda Prompt on Windows. On macOS/Linux, ask your instructor to help connect your existing Conda installation to the terminal.

## 2  Know where to type commands

Run terminal commands **one line at a time**, pressing Enter and waiting for each to finish. They are not R code and do not go in RStudio or a notebook cell. Do not copy the prompt before a command, such as `(base) C:\Users\Alex>`.

The first installation needs internet access. **Test status:** a fresh environment created from the setup-only ZIP passed the package, numerical, chemistry, workbook, plotting, kernel, notebook and JupyterLab checks on Windows/Python 3.14. macOS/Linux still require instructor pilots. Reference: [Conda environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

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

**Check the folder:** on Windows, run `cd` by itself to print the location, then `dir` to list files. On macOS/Linux, use `pwd`, then `ls`. Find **environment-anaconda.yml**, **scripts**, **setup_assets** and **JUPYTER_BASICS.ipynb** before continuing. “From the supplied folder” means this terminal location.

## 4  Create, activate and check the environment

```text
conda env create -f environment-anaconda.yml
conda activate esbmtk-practicals
python -m pip check
python scripts/check_environment.py
```

Creation downloads Python and the course packages; wait for it to finish. Activation selects them for this terminal; the prompt should show **(esbmtk-practicals)**. If this course environment already exists, skip creation and run the other three commands.

Expect **No broken requirements found**, then **Environment check passed. Next: start JupyterLab.** The second check tests numerical calculations, chemistry, access to the supplied workbook probe and plotting. Stop and seek help if either check fails.

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

## 6  Complete the JupyterLab setup check

In JupyterLab's left file browser, double-click **JUPYTER_BASICS.ipynb**. Choose **esbmtk-practicals** (or **ESBMTK practicals** if registered with an earlier guide) if JupyterLab asks for a kernel. Follow the notebook from top to bottom, or select **Run > Run All Cells**. The last cell should print:

```text
Jupyter setup check passed
```

The notebook also introduces the cell shortcuts used during the practicals. **If both terminal checks and this notebook check pass, setup is complete.** You do not repeat creation or kernel registration each time.

## Open or create notebooks while JupyterLab is running

Use the left file browser to double-click any notebook supplied by your instructor. If it asks for the instructor's ESBMTK314 kernel, choose your course kernel instead. Create another notebook via **File > New > Notebook**. No terminal command is needed for each notebook. Save with Ctrl+S (Cmd+S on macOS).

## When you finish: save and shut down

Save your notebooks. Return to the terminal running JupyterLab, press **Ctrl+C**, and, if asked to shut down, type **y** and press Enter. Wait for the normal prompt to return, then close the browser tab and terminal. This stops notebook kernels: variables in memory are lost, but saved notebooks remain on disk.

**Closing the browser tab alone does not normally stop JupyterLab.** Reopen the local link still shown in its terminal if you only closed the tab; you do not need another server.

## Next time: open JupyterLab again

Open Anaconda Prompt or your Conda-enabled Terminal, repeat `cd` to the supplied folder (page 2), then run:

```text
conda activate esbmtk-practicals
python -m jupyterlab
```

Do this only when the server has stopped, including after restarting your laptop. Open your saved notebooks and rerun the cells needed to recreate variables.

## If a step fails

**File not found:** check the terminal folder (page 2). **Wrong Python or missing package:** activate the course environment, launch Jupyter there and select its kernel. **Windows Python crash:** use the activated prompt. For other errors, send your instructor the full error text, command and operating system.
