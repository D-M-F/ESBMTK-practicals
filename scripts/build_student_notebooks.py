"""Create student notebooks by masking marked instructor solutions.

The instructor notebook is the source of truth.  Code between
``# BEGIN SOLUTION`` and ``# END SOLUTION`` and Markdown between the analogous
HTML comments is replaced with an explicit exercise placeholder.  Cells tagged
``solution-only`` are removed entirely.
"""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
INSTRUCTOR = ROOT / "notebooks" / "instructor"
STUDENT = ROOT / "notebooks" / "student"
NOTEBOOKS = (
    "00_PyCO2SYS.ipynb",
    "01_single_box_air_sea_CO2.ipynb",
    "02_two_layer_ocean_carbon_pump.ipynb",
    "03_boudreau_three_box_model.ipynb",
    "04_pump_strength_OA_OAE.ipynb",
)
EXTENSION_NOTEBOOKS = (
    "extensions/04_attribution_and_feedbacks.ipynb",
    "extensions/05_independent_model.ipynb",
)


def _mask_code(source: str) -> str:
    pattern = re.compile(
        r"(?ms)^(?P<indent>[ \t]*)# BEGIN SOLUTION\s*$.*?"
        r"^(?P=indent)# END SOLUTION\s*$"
    )

    def replacement(match: re.Match) -> str:
        indent = match.group("indent")
        return (
            f'{indent}raise NotImplementedError('
            '"Exercise: replace this line with your solution")'
        )

    return pattern.sub(replacement, source)


def _mask_markdown(source: str) -> str:
    return re.sub(
        r"(?ms)<!-- BEGIN SOLUTION -->.*?<!-- END SOLUTION -->",
        "> **Your explanation:** replace this placeholder with your answer.",
        source,
    )


def build_student_notebook(source_path: Path, target_path: Path) -> None:
    notebook = json.loads(source_path.read_text(encoding="utf-8"))
    cells = []
    for cell in notebook["cells"]:
        tags = cell.get("metadata", {}).get("tags", [])
        if "solution-only" in tags:
            continue
        source = "".join(cell.get("source", []))
        if cell["cell_type"] == "code":
            source = _mask_code(source)
            cell["outputs"] = []
            cell["execution_count"] = None
        elif cell["cell_type"] == "markdown":
            source = _mask_markdown(source)
        cell["source"] = source.splitlines(keepends=True)
        cells.append(cell)

    notebook["cells"] = cells
    rendered = json.dumps(notebook, indent=1, ensure_ascii=False) + "\n"
    if "BEGIN SOLUTION" in rendered or "END SOLUTION" in rendered:
        raise ValueError(f"unmasked solution marker remains in {source_path}")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(rendered, encoding="utf-8")


def main() -> None:
    for name in (*NOTEBOOKS, *EXTENSION_NOTEBOOKS):
        source = INSTRUCTOR / name
        target = STUDENT / name
        if not source.is_file():
            raise FileNotFoundError(source)
        build_student_notebook(source, target)
        print(f"built {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
