# Environment diagnosis and student setup proposal

Investigated 2026-09-21. The diagnosis below is verified on the current Windows
machine. The alternative student environment is a proposal, not a tested release
or a change to the course prerequisites. The existing ESBMTK314 environment
remains the reference for model verification.

## Reproduced Windows crash

Launching the ESBMTK314 `python.exe` directly without activation and evaluating
`numpy.linalg.solve(numpy.eye(2), numpy.ones(2))` reproduces the screenshot's
exception, `0xc06d007f`. Imports alone succeed and therefore are insufficient
as an environment check.

A temporary Windows exception handler captured the native delay-load failure:

```text
DLL: libiomp5md.dll
Function: __kmpc_global_thread_num
Windows error: 127 (procedure not found)
```

The loaded DLL is in the ESBMTK314 environment's `Library/bin`. Inspection of
its PE export table confirms that this function forwards to
`libomp.dll.__kmpc_global_thread_num`. The unactivated process has no environment
`Library/bin` on PATH and did not load `libomp.dll` in the captured failure.
Thus finding the first DLL by absolute path is insufficient to resolve its
forwarded dependency. Microsoft describes the corresponding
[delay-load exception](https://learn.microsoft.com/en-us/cpp/build/reference/error-handling-and-notification?view=msvc-170).

Controlled checks:

| Launch                                                     | Result                                                                     |
| ---------------------------------------------------------- | -------------------------------------------------------------------------- |
| Environment Python by absolute path; inherited PATH        | NumPy linear solve crashes with the captured exception                     |
| Same Python; environment directories prepended to PATH     | NumPy/SciPy solves and GSW/ESBMTK density calculations pass                |
| `conda run -n ESBMTK314 --no-capture-output python ...`    | The same numerical checks pass                                             |
| `conda run` with the registered `esbmtk314` Jupyter kernel | All seven instructor 01 code cells pass, including conservation assertions |

The verified remedy is to launch through Conda activation or `conda run`, not
merely choose an interpreter by absolute path. This agrees with
[Conda's Windows activation guidance](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment).
Earlier `DeadKernelError` messages alone did not identify this native failure;
the numerical reproducer supplied that missing evidence. There is no evidence
that the gas-exchange text or model equations caused the crash.

The environment also contains both `numpy-2.5.2.dist-info` (pip) and
`numpy-2.5.3.dist-info` (Conda), plus leftover `numpy.libs`. The imported NumPy
reports 2.5.3, while `importlib.metadata.version('numpy')` reports 2.5.2.
Conda history records installing GSW and NumPy after the earlier pip packages.
This leaves misleading metadata and makes a blind package-version export a poor
reproducibility baseline. It is a separate maintenance concern; it does not
establish that the installed NumPy code is broken when properly activated.
No packages, user kernels or global environment settings were changed during
this investigation.

Follow-up inspection of the live Jupyter processes confirmed that the user's
server and all ten notebook kernels were already using ESBMTK314 with its
`Library/bin` and other activation paths configured. The active notebooks also
specify the `esbmtk314` kernel. A separate numerical-check process launched with
a copy of a live kernel's environment passes NumPy/SciPy solves and GSW/ESBMTK
density calculations. Existing notebook sessions were not modified or restarted.
The reproduced unactivated-launch failure therefore does not establish a problem
with the user's current Jupyter launch. The earlier agent verification launches
bypassed activation; future automated checks must use the activated launcher.
Evidence: `tmp/environment_diagnosis/live_kernel_environment.log`.

Diagnostic logs and temporary instrumentation are in
`tmp/environment_diagnosis/`, particularly `dll_failure.log`,
`numerical_activated.log`, `conda_run.log`, and `conda_jupyter.log`.
The diagnostic processes suppress Windows crash dialogs locally; they do not
change system-wide error reporting or hide failures from the logs.

## Proposed student route: uv and a locked project

Anaconda is not a requirement of ESBMTK. The installed ESBMTK package declares
Python >=3.12 and Python-package dependencies, and it is available through pip.
Anaconda is one distribution; Conda is an environment manager. Neither is the
Python language or the notebook interface.

For these Python practicals, the proposed default is
[uv](https://docs.astral.sh/uv/getting-started/installation/), a standalone tool
that can [download Python](https://docs.astral.sh/uv/guides/install-python/) and
restore a project environment. Students need not have Python installed first.
Keep JupyterLab in that same project environment. Their R installation can
remain unchanged; RStudio and reticulate are not prerequisites for this course.

Supply these files with the practicals:

- `pyproject.toml`: Python compatibility and required packages.
- `.python-version`: the Python version chosen and checked by the instructor.
- `uv.lock`: the resolved dependency versions, committed after verification.
- A short launcher and numerical/chemistry environment check, with instructions
  to select the project Python kernel.

A TOML file describes the environment; it does not install anything by itself.
The lockfile prevents each student's first run from independently selecting a
new set of package versions. See uv's
[project layout](https://docs.astral.sh/uv/concepts/projects/layout/) and
[locking guidance](https://docs.astral.sh/uv/concepts/projects/sync/).

An initial manifest to evaluate is below. It is deliberately not installed at
the repository root yet, and no compatible lockfile has been generated or
tested. Preserve the currently verified Python 3.14 line initially; ESBMTK's

> =3.12 requirement does not prove that every combination of dependencies and
> these notebooks has been tested on every supported Python version.

```toml
[project]
name = "esbmtk-practicals"
version = "0.1.0"
requires-python = ">=3.14,<3.15"
dependencies = [
    "esbmtk==0.14.3.1.post0",
    "PyCO2SYS==1.8.3.4",
    "numpy",
    "scipy",
    "matplotlib",
    "pandas",
    "gsw",
    "openpyxl>=3.1,<4",
    "jupyterlab",
    "ipykernel",
]

[tool.uv]
package = false
```

After the instructor has supplied and tested the lockfile, the intended student
workflow is:

1. Install uv once using its standalone installer; no preinstalled Python is
   required. Download and extract the course folder; Git need not be required.
2. Open a terminal in that folder and run `uv sync --locked`.
3. Run `uv run --locked jupyter lab` and open `notebooks/student/`.

The first setup needs internet access to obtain the interpreter and packages.
Subsequent work uses the local environment. Launching Jupyter in the same
environment reduces server/kernel mismatches. The distributed notebooks currently
refer to the named ESBMTK314 kernel, so the rollout must either provide an
environment-local course kernelspec or adjust the distributed kernel metadata;
do not assume that an old globally registered kernel points to the new project.
The instructor and generated student notebook workflow must remain consistent.
See [uv's Jupyter guidance](https://docs.astral.sh/uv/guides/integration/jupyter/).

For students familiar only with R, provide a short orientation: JupyterLab is
the interface, Python is the runtime, and uv restores this course's packages
(roughly the role of restoring a project library). Students should not need to
choose dependency versions, troubleshoot DLL paths, or write TOML. The instructor
owns those files and the launcher.

## Alternatives and release checks

For students who already use Anaconda or Miniconda, a separate
[Anaconda setup guide](anaconda_setup.md) and
[`environment-anaconda.yml`](../environment-anaconda.yml) provide a dedicated
course environment, explicit kernel selection and an activated Jupyter launch.
This is an alternative recipe for testing, not a resolved lockfile or a
requirement to switch package managers. Conda installs Python/pip; pip installs
the complete course stack to keep package ownership unambiguous.

If using Conda-built numerical libraries remains preferable, Pixi provides a
TOML manifest and lockfile plus environment-aware launch tasks without requiring
the full Anaconda distribution. It can combine Conda and PyPI dependencies and
supports [pyproject.toml](https://pixi.prefix.dev/latest/python/pyproject_toml/).
It is a viable alternative, not an additional tool students should have to learn.

For genuinely zero local installation, a university-managed
[JupyterHub](https://jupyter.org/hub) can provide the prepared environment through
a browser. That is the lowest student setup burden if hosting and support are
available; it moves environment maintenance to the instructor/institution.

Before adopting the local uv route, create a clean environment and verify all
core instructor notebooks and relevant conservation tests on Windows and the
Mac platforms used by students. Confirm wheel availability, workbook loading,
plotting and project-local kernel selection. Include an actual small linear
solve in the setup check, since imports alone missed the current crash. Pilot
the setup with a student who has no Python installation. Only then update README
and TEACHING_GOALS to make this the supported prerequisite and record its setup
time separately from the four-hour practical.
