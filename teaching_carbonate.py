"""Supplied offline surface/contour/slice explorer for notebook 01.

The browser only displays chemistry computed by PyCO2SYS under the shared
configuration. No widget extension, CDN, browser chemistry or model run is used.
"""
from html import escape
import json
from pathlib import Path

import numpy as np


def carbonate_explorer_data(config, inferred_ta, *, initial_dic=0.01):
    """Sample exact constant-TA curves; retain the inferred state in both grids.

    Concentrations are umol C/kg (DIC) and ueq/kg (TA); pCO2 is uatm.
    Sensitivity uses a centred 0.001 umol/kg DIC perturbation at constant TA.
    Chemistry states may exceed the closed model's inventory; the atmosphere
    line is present only where its carbon inventory is nonnegative.
    """
    import PyCO2SYS as pyco2
    from matplotlib.figure import Figure
    from matplotlib.ticker import MaxNLocator
    from simple_models import atmospheric_pco2_curve

    inferred_ta = float(inferred_ta)
    if not np.isfinite(inferred_ta) or inferred_ta <= 200:
        raise ValueError("The explorer requires a finite inferred TA above 200 ueq/kg")
    if not np.isfinite(initial_dic) or initial_dic <= 0.001:
        raise ValueError("initial_dic must exceed the 0.001 umol/kg sensitivity step")
    reference_dic = config.target_dic_umol_kg
    mass = config.ocean_volume_m3 * config.density_kg_m3
    maximum_dic = config.total_carbon_mol / mass * 1e6
    ranges = {
        "local": (reference_dic - 100, reference_dic + 100,
                  inferred_ta - 100, inferred_ta + 100),
        "full": (initial_dic, maximum_dic * (1 - 1e-6), 0, inferred_ta + 200),
    }
    result = {
        "conditions": (f"{config.temperature:g} °C · salinity {config.salinity:g} · "
                       f"{config.pressure_bar:g} bar · carbonate constants "
                       f"{config.opt_k_carbonic} · pH scale {config.opt_pH_scale}"),
        "reference_dic": reference_dic, "reference_ta": inferred_ta,
        "maximum_dic": maximum_dic, "ranges": {},
    }
    for name, (xmin, xmax, ymin, ymax) in ranges.items():
        dic = np.unique(np.append(np.linspace(xmin, xmax, 81), reference_dic))
        ta = np.unique(np.append(np.linspace(ymin, ymax, 41), inferred_ta))
        xx, yy = np.meshgrid(dic, ta)

        def chemistry(x):
            return pyco2.sys(par1=x, par1_type=2, par2=yy, par2_type=1,
                             **config.pyco2)["pCO2"]

        pco2 = chemistry(xx)
        slope = (chemistry(xx + 0.001) - chemistry(xx - 0.001)) / 0.002
        if not np.all(np.isfinite(pco2)) or not np.all(pco2 > 0):
            raise ValueError("Nonfinite or nonpositive carbonate surface")
        valid = dic <= maximum_dic
        atmosphere = np.full(dic.shape, np.nan)
        atmosphere[valid] = atmospheric_pco2_curve(dic[valid], config)
        # Precompute labelled isolines from the same mesh, without a GUI backend.
        fig = Figure()
        ax = fig.subplots()
        levels = MaxNLocator(nbins=8).tick_values(float(pco2.min()), float(pco2.max()))
        contours = ax.contour(dic, ta, pco2, levels=levels)
        lines = [{"value": float(level), "paths": [segment.tolist() for segment in segments
                  if len(segment) > 1]}
                 for level, segments in zip(contours.levels, contours.allsegs)]
        fig.clear()
        result["ranges"][name] = {
            "dic": dic.tolist(), "ta": ta.tolist(), "pco2": pco2.tolist(),
            "slope": slope.tolist(), "contours": lines,
            "atmosphere": [float(v) if np.isfinite(v) else None for v in atmosphere],
            "ta_index": int(np.argmin(abs(ta - inferred_ta))),
            "dic_index": int(np.argmin(abs(dic - reference_dic))),
        }
    return result


def carbonate_explorer_html(config, inferred_ta, *, initial_dic=0.01):
    """Return a self-contained, offline HTML document (also suitable for srcdoc)."""
    data = carbonate_explorer_data(config, inferred_ta, initial_dic=initial_dic)
    template = (Path(__file__).parent / "ref" / "carbonate_explorer.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c")
    return template.replace("__CARBONATE_DATA__", payload)


def show_carbonate_explorer(config, inferred_ta, *, initial_dic=0.01):
    """Display an isolated offline iframe in Jupyter; rerun the cell to activate.

    A Save offline copy button inside the explorer downloads the same HTML for
    use in a separate browser window, without writing into the repository.
    """
    from IPython.display import IFrame

    document = carbonate_explorer_html(config, inferred_ta, initial_dic=initial_dic)
    return IFrame('about:blank', width='100%', height=820, extras=[
        'title="DIC–TA–pCO2: surface, contours and slices"',
        'sandbox="allow-scripts allow-downloads"',
        'srcdoc="' + escape(document, quote=True) + '"',
    ])
