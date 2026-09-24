"""Build a standalone carbonate/buffering HTML; never rewrite notebooks.

Inspired by Middelburg (2019), Figs 5.3/5.8 and Eqs 5.18/5.20/5.21.
All derivatives hold DIC, temperature, salinity, pressure and other totals fixed.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import PyCO2SYS as pyco2
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from teaching_carbonate import carbonate_explorer_data
from teaching_config import TEACHING as config


def titration(pH, dic, settings):
    return pyco2.sys(par1=pH, par1_type=3, par2=dic, par2_type=2,
                     **{**settings, 'opt_buffers_mode': 0})


def buffer_components(pH, settings, reference_dic=2000.0, step=1e-4):
    """Capacity in ueq/kg/pH. Carbonate's contribution scales exactly with DIC."""
    plus = titration(pH + step, reference_dic, settings)
    minus = titration(pH - step, reference_dic, settings)

    def derivative(key):
        return (plus[key] - minus[key]) / (2 * step)

    carbonate = derivative('bicarbonate') + 2 * derivative('carbonate')
    borate = derivative('alkalinity_borate')
    water = derivative('hydroxide') - derivative('hydrogen_free')
    total = derivative('alkalinity')
    other = total - carbonate - borate - water
    # Sulfate/fluoride and other noncarbonate terms need retaining over pH 0–14.
    return dict(carbonate_per_dic=carbonate / reference_dic,
                borate=borate, water=water, other=other,
                approximate_per_dic=np.log(10) * plus['k_carbonic_2'] / 10.0**(-pH))


def build_data():
    reference_ta = float(config.reference_state()['alkalinity'])
    data = carbonate_explorer_data(config, reference_ta)
    settings = {**config.pyco2, 'opt_buffers_mode': 0}
    for sample in data['ranges'].values():
        dic, ta = np.meshgrid(sample['dic'], sample['ta'])
        state = pyco2.sys(par1=dic, par1_type=2, par2=ta, par2_type=1, **settings)
        ph = state['pH']
        plus = pyco2.sys(par1=dic+.001, par1_type=2, par2=ta, par2_type=1, **settings)
        minus = pyco2.sys(par1=dic-.001, par1_type=2, par2=ta, par2_type=1, **settings)
        B = (titration(ph+1e-4,dic,settings)['alkalinity'] -
             titration(ph-1e-4,dic,settings)['alkalinity']) / 2e-4
        fig = Figure()
        contours = fig.subplots().contour(dic,ta,ph,levels=MaxNLocator(nbins=8).tick_values(float(ph.min()),float(ph.max())))
        sample['ph_contours'] = [{'value':float(v),'paths':[a.tolist() for a in segs if len(a)>1]}
                                 for v,segs in zip(contours.levels,contours.allsegs)]
        fig.clear()
        sample.update(ph=ph.tolist(),ph_slope=((plus['pH']-minus['pH'])/.002).tolist(),
                      capacity=B.tolist())
        assert np.all(np.isfinite(B)) and np.all(B>0)
    ph_grid=np.linspace(0,14,561)
    components=buffer_components(ph_grid,settings)
    data['buffers']={'ph':ph_grid.tolist(), **{k:v.tolist() for k,v in components.items()}}
    # Store an independent finite-difference verification at several DIC values.
    for dic in [100, 2000, 2040, 2200]:
        direct=(titration(ph_grid+1e-4,dic,settings)['alkalinity']-
                titration(ph_grid-1e-4,dic,settings)['alkalinity'])/2e-4
        reconstructed=(dic*components['carbonate_per_dic']+components['borate']+
                       components['water']+components['other'])
        np.testing.assert_allclose(reconstructed,direct,rtol=3e-6,atol=1e-5)
        assert np.all(reconstructed>0)
    return data


def main():
    data=build_data()
    template=(ROOT/'ref/carbonate_buffer_explorer.html').read_text(encoding='utf-8')
    payload=json.dumps(data,ensure_ascii=False,allow_nan=False).replace('<','\\u003c')
    target=ROOT/'output/carbonate-chemistry-and-buffering.html'
    target.write_text(template.replace('__CARBONATE_DATA__',payload),encoding='utf-8')
    print('Built standalone HTML; component reconstruction checks passed:',target)


if __name__=='__main__':
    main()
