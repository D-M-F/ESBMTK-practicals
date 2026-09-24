"""Export current teaching records for the optional XLSX authoring tool.

No workbook inputs are changed. Run from the repository root and pass the JSON
output to build_flux_worksheets.mjs. Student data have no concealed solutions.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from teaching_specification import flux_specification, implementation_references


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    payload = {role: {
        'FluxSpecification': flux_specification(student=role == 'student'),
        'WorkbookLinks': implementation_references(student=role == 'student'),
    } for role in ('student', 'instructor')}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
