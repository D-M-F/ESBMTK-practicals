"""Build the student setup-only ZIP from an explicit file allow-list."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "output/ESBMTK-practicals-setup-only.zip"
ARCHIVE_ROOT = "ESBMTK-practicals-setup"
FIXED_TIMESTAMP = (2026, 9, 23, 0, 0, 0)

# Only these files can enter the student package. In particular, no files from
# notebooks/instructor, notebooks/student, data or archive are discovered.
PACKAGE_FILES = {
    "START_HERE.md": ROOT / "ref/setup_only_start_here.md",
    "SETUP_WITH_UV.pdf": ROOT / "output/pdf/student_setup_uv.pdf",
    "SETUP_WITH_ANACONDA.pdf": ROOT / "output/pdf/student_setup_anaconda.pdf",
    "JUPYTER_BASICS.ipynb": ROOT / "JUPYTER_BASICS.ipynb",
    "pyproject.toml": ROOT / "pyproject.toml",
    "uv.lock": ROOT / "uv.lock",
    ".python-version": ROOT / ".python-version",
    "environment-anaconda.yml": ROOT / "environment-anaconda.yml",
    "scripts/check_environment.py": ROOT / "scripts/check_environment.py",
    "setup_assets/workbook_probe.xlsx": ROOT / "setup_assets/workbook_probe.xlsx",
}


def rebuild_pdfs() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_setup_pdfs.py")],
        cwd=ROOT,
        check=True,
    )


def build_package(output: Path = DEFAULT_OUTPUT) -> Path:
    missing = [str(path) for path in PACKAGE_FILES.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing setup-package files:\n" + "\n".join(missing))

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for destination, source in sorted(PACKAGE_FILES.items()):
            info = ZipInfo(f"{ARCHIVE_ROOT}/{destination}", FIXED_TIMESTAMP)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes(), compress_type=ZIP_DEFLATED,
                             compresslevel=9)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--rebuild-pdfs",
        action="store_true",
        help="Regenerate both PDF guides before assembling the ZIP.",
    )
    args = parser.parse_args()
    if args.rebuild_pdfs:
        rebuild_pdfs()
    result = build_package(args.output.resolve())
    print(result)


if __name__ == "__main__":
    main()

