import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from scripts.build_student_notebooks import build_student_notebook

path = root / 'notebooks/instructor/02_two_layer_ocean_carbon_pump.ipynb'
backup = root / 'tmp/pulse_duration_fix'
backup.mkdir(exist_ok=True)
(backup / path.name).write_bytes(path.read_bytes())
nb = json.loads(path.read_text(encoding='utf-8'))
for cell in nb['cells']:
    old = text = ''.join(cell['source'])
    if cell['id'] == '08782bde':
        text = text.replace('    integrated_signal,', '    finite_pulse_clock, integrated_signal,')
    elif cell['id'] == 'a3d16943':
        text = text.replace('def build_layers(k_kg_yr=0.0, state=None):\n    M = new_model()',
                            "def build_layers(k_kg_yr=0.0, state=None, *,\n"
                            "                 stop='30 kyr', max_timestep='20 yr'):\n"
                            '    M = new_model(stop=stop, max_timestep=max_timestep)')
    elif cell['id'] == '02-supplied-forcing':
        begin = text.index('**The 1000-year pulse')
        end = text.index('Read the checks in order', begin)
        text = text[:begin] + '''**Pulse duration is a choice, not a restriction.** Set `pulse_duration` below;
at fixed added mass, a longer square pulse has a smaller flux rate. Duration
changes the transient; after sufficient relaxation, the final equilibrium
should depend on the total addition. Exploring other durations is optional.

The supplied `finite_pulse_clock` helper refines the time grid automatically
for shorter pulses and aligns the pulse with that grid. `clock` is a dictionary
of timing settings; `**clock` passes those settings to both model constructors.
Use positive whole-year durations (for example `'100 yr'`, `'333 yr'` or
`'1 kyr'`). Keep the pulse inside the run and leave time after it to settle;
increase `run_stop` if the endpoint checks show that it has not settled yet.
After changing the duration, rerun this whole cell to build fresh models.

''' + text[end:]
        text = text.replace('> duration must be adequately resolved, keep the signal zero at the simulation\'s\n> start and end, pass the integral check, and leave time to reach equilibrium.',
                            '> grid must resolve the pulse and keep it zero at the simulation boundaries.\n'
                            '> The helper supplies that grid; the checks verify mass and equilibration.')
    elif cell['id'] == '02-forcing-example':
        assert "duration='100 yr'" in text
        text = text.replace('state = {b.name:',
                            "pulse_start = '1000 yr'\n"
                            "pulse_duration = '100 yr'  # Change this value to explore another duration.\n"
                            "run_stop = '30 kyr'\n"
                            "clock = finite_pulse_clock(start=pulse_start, duration=pulse_duration, stop=run_stop)\n"
                            'state = {b.name:')
        text = text.replace('build_layers(k, state=state)', 'build_layers(k, state=state, **clock)')
        text = text.replace("start='1000 yr', duration='100 yr',",
                            'start=pulse_start, duration=pulse_duration,')
    if text != old:
        cell['source'] = text.splitlines(keepends=True)
        if cell['cell_type'] == 'code':
            cell['outputs'] = []
            cell['execution_count'] = None
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
build_student_notebook(path, root / 'notebooks/student' / path.name)
print('Updated pulse clock and regenerated student 02; retained the user-selected 100-year duration.')
