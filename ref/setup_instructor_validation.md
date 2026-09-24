# Setup verification and maintenance

These notes are for instructors and maintainers. Student-facing instructions
live in `ref/uv_setup.md`, `ref/anaconda_setup.md` and the temporary
`ref/setup_only_start_here.md` transition guide.

## Anaconda recipe status

Python 3.14 and the ESBMTK/PyCO2SYS pins match the teaching reference, but the
full dependency set is not locked. On 2026-09-23, a new
`esbmtk-practicals` environment was created from the YAML in an extracted copy
of the setup-only ZIP on Windows. `pip check`, the shared environment checker,
environment-local kernel registration, the complete Jupyter basics notebook and
an actual JupyterLab HTTP launch passed. The temporary pilot environment was
then removed without changing ESBMTK314 or the other existing environments.
macOS/Linux and novice-student pilots remain outstanding.

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
not a lockfile. Test the resolved package set on each supported platform before
release and repeat the fresh pilot after dependency changes. Do not export the
instructor environment's stale overlapping NumPy metadata. Students should use
one setup route for this course.

## Setup-only package

Run `python scripts/build_setup_package.py --rebuild-pdfs` from an environment
with ReportLab available. The builder uses a fixed allow-list and creates
`output/ESBMTK-practicals-setup-only.zip`. Inspect the ZIP contents before
distribution. It must not contain `notebooks/instructor`, `notebooks/student`,
`data` or `archive`.

The setup checker deliberately opens `setup_assets/workbook_probe.xlsx`, not the
Boudreau model workbook. Exercise data and exercise readiness are verified by
the notebook/model test suite, separately from this student installation check.
