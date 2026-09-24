import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / 'tmp/03_04_revision'
OUT.mkdir(parents=True, exist_ok=True)
paths = [*ROOT.glob('notebooks/**/*.ipynb'), *ROOT.glob('archive/**/*'),
         *ROOT.glob('data/Boudreau_2010/**/*')]
hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in paths if p.is_file() and not p.name.startswith('~$')}
(OUT / 'before_hashes.json').write_text(json.dumps(hashes, indent=2))
for n in ('03_boudreau_three_box_model.ipynb', '04_pump_strength_OA_OAE.ipynb'):
    (OUT / n).write_bytes((ROOT / 'notebooks/instructor' / n).read_bytes())

if '--numerics' in sys.argv:
    import numpy as np
    from model import initialize_model, run_model, postprocess_carbonate_horizons
    from presets import load_boudreau_parameters
    from teaching_audits import audit_complete_model
    m = initialize_model(load_boudreau_parameters(), stop='20 yr', max_timestep='1 yr')
    m.read_state(directory=str(ROOT / 'data/Boudreau_2010/steady_state'))
    run_model(m)
    postprocess_carbonate_horizons(m)
    for b in (m.L_b, m.H_b, m.D_b):
        for sp in ('DIC', 'TA'):
            a = getattr(b, sp).c
            print(b.name, sp, 'max drift umol/kg', float(np.max(np.abs(a-a[0]))*1e6))
    for label, a, scale in [('atm', m.CO2_At.c, 1e6), ('snow',m.D_b.zsnow.c,1)]:
        print(label, 'max drift',float(np.max(np.abs(a-a[0]))*scale))
    print(audit_complete_model(m))
    for c in m.loc:
        print(c.id,c.source.full_name,c.sink.full_name,c.ctype, 'sp', c.source.sp.name)
