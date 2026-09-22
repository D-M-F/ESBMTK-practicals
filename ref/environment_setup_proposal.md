# Environment diagnosis and student setup status

Investigated 2026-09-21; uv setup verified on Windows on 2026-09-22.
The existing ESBMTK314 environment remains the instructor reference. The supplied
uv route now provides an independently installed student environment; macOS/Linux
and novice-student setup pilots remain outstanding.

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

## Implemented student route: uv and a locked project

Students without Python can use the [uv setup guide](uv_setup.md) and its
[three-page PDF](../output/pdf/student_setup_uv.pdf). uv installs a managed Python
interpreter and a separate project environment; Anaconda, RStudio and reticulate
are not prerequisites. Existing R installations stay unchanged.

Distribute the complete course folder, including:

- [`pyproject.toml`](../pyproject.toml): Python compatibility and required packages.
- [`.python-version`](../.python-version): tested Python 3.14.7.
- [`uv.lock`](../uv.lock): resolved versions and package hashes.
- [`scripts/check_environment.py`](../scripts/check_environment.py): actual
  numerical solves, chemistry, workbook access and plotting checks.
- Course modules, notebooks and `data/`, including the model workbook and restarts.

Do not distribute a machine-specific `.venv` or temporary validation files.
Students do not generate TOML or a lockfile: they extract the supplied folder,
install uv, navigate to that folder, and run the guide's commands. The manifest
uses `python-preference = "only-managed"` to avoid borrowing a Conda interpreter.
`uv sync --locked` restores the supplied package resolution without changing it.
See uv's [project layout](https://docs.astral.sh/uv/concepts/projects/layout/) and
[locking guidance](https://docs.astral.sh/uv/concepts/projects/sync/).

Register the `esbmtk-practicals` kernel with `--sys-prefix` inside this environment
and launch JupyterLab with `uv run --locked jupyter lab`. Select that kernel if a
distributed notebook requests the instructor's ESBMTK314 kernel. Registration
does not replace globally registered kernels. The guide distinguishes creating
notebooks in an already-running server, saving/shutting down, and relaunching;
closing a browser tab alone does not normally stop the server. See
[uv's Jupyter guidance](https://docs.astral.sh/uv/guides/integration/jupyter/).

### Windows verification, 2026-09-22

Using uv 0.12.17 with an empty project environment and a separately downloaded
managed Python 3.14.7, the locked installation and environment checker pass.
All core instructor notebooks 00-04 execute, including their numerical audits.
An actual local JupyterLab server serves its UI, starts the project kernel,
executes imports and a linear solve, shuts down cleanly and relaunches correctly.
No existing Conda environment or user notebook session was changed.

The full test suite has 56 passes and one failing test for generated student-copy
equality. A subsequent check in the reference Conda environment finds extra empty
code cells in instructor sources 00 and 01 (two and one respectively), absent
from their student copies; all other parsed content matches. This source/copy
mismatch is separate from installation and does not affect notebook execution.
Existing notebook edits were preserved; reconcile the copies before release.

Evidence is retained locally in `tmp/uv_validation/`: `lock.log`, `sync.log`,
`check.log`, `tests.log`, `notebooks.log` and `lifecycle.log`. The PDF's
three rendered pages were visually checked. The Windows uv installer itself was
not exercised on a clean laptop: uv was installed into an isolated test directory.

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

Before a cross-platform release, repeat the locked installation and checks on
the macOS/Linux platforms used by students. Windows package installation, workbook
loading, plotting, project-local kernel selection and core notebook execution
are already verified. Pilot the documented initial uv installer and setup with a
student who has no Python installation, and measure setup time separately from
the four-hour practical. Preserve `--locked`; update the manifest and lockfile
together only as an instructor maintenance action followed by verification.
