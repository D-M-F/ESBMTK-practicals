"""Build the offline instructor preview; activate the course environment first."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from teaching_carbonate import carbonate_explorer_html
from teaching_config import TEACHING as config


def main():
    # This standalone instructor preview uses the fitted reference; notebook 01
    # instead passes the student's own inferred_ta after the masked exercise.
    inferred_ta = float(config.reference_state()['alkalinity'])
    output = ROOT / 'output' / 'dic-ta-pco2-explorer.html'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(carbonate_explorer_html(config, inferred_ta), encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
