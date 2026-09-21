from pathlib import Path
import yaml
from packaging.requirements import Requirement
recipe = yaml.safe_load(Path('environment-anaconda.yml').read_text(encoding='utf-8'))
assert recipe['name'] == 'esbmtk-practicals'
assert recipe['channels'] == ['conda-forge', 'nodefaults']
assert recipe['dependencies'][:2] == ['python=3.14', 'pip']
requirements = recipe['dependencies'][2]['pip']
for item in requirements:
    Requirement(item)
Path('tmp/anaconda_setup/requirements.txt').write_text('\n'.join(requirements) + '\n', encoding='utf-8')
print('YAML and all package requirement strings validate.')
import numpy as np
np.testing.assert_allclose(np.linalg.solve(np.eye(2), np.ones(2)), [1, 1])
print('Documented numerical check passes in the activated reference environment.')
