"""Supplied plots for the guided practical; model construction stays in notebooks."""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from esbmtk import gas_exchange_fluxes

def plot_carbonate_process_plane(params, *, show_processes=False):
    """Local chemistry at the workbook L_b state, before exchange/transport.

    DIC is in umol C/kg and TA in ueq/kg. ESBMTK stores pressure in bar;
    PyCO2SYS requires dbar. This figure is not a model integration or restart.
    The default supplies an unannotated exercise; arrows are instructor-only.
    """
    import PyCO2SYS as pyco2
    from esbmtk import Q_

    box = params['boxes']['L_b']
    dic0 = Q_(box['dic']).to('umol/kg').magnitude
    ta0 = Q_(box['ta']).to('umol/kg').magnitude
    settings = dict(temperature=box['temperature'], salinity=box['salinity'],
                    pressure=10 * box['pressure'],
                    opt_k_carbonic=params['opt_k_carbonic'],
                    opt_pH_scale=params['opt_pH_scale'])

    def pco2(dic, ta):
        return pyco2.sys(par1=ta, par1_type=1, par2=dic, par2_type=2,
                         **settings)['pCO2']

    dic, ta = np.meshgrid(np.linspace(dic0 - 50, dic0 + 50, 81),
                          np.linspace(ta0 - 80, ta0 + 80, 81))
    fig, axis = plt.subplots(figsize=(8, 6))
    contours = axis.contour(dic, ta, pco2(dic, ta), levels=12,
                            colors='0.5', linewidths=0.8)
    axis.clabel(contours, inline=True, fontsize=8, fmt='%g')
    axis.plot(dic0, ta0, 'ko', label='Workbook reference (L_b)')
    if show_processes:
        # Equal 20 umol C/kg changes in the same water mass; model POC has no TA.
        for label, ddic, dta, color in (
            ('Model POC removal', -20, 0, '#1764ab'),
            ('CaCO3 formation', -20, -40, '#b34b1b'),
            ('CaCO3 dissolution', 20, 40, '#25824b'),
        ):
            axis.annotate('', xy=(dic0 + ddic, ta0 + dta), xytext=(dic0, ta0),
                          arrowprops=dict(arrowstyle='->', color=color, lw=2.5))
            change = float(pco2(dic0 + ddic, ta0 + dta) - pco2(dic0, ta0))
            axis.plot([], [], color=color, lw=2.5,
                      label=f'{label}: pCO2 change {change:+.1f} µatm')
    axis.set(xlabel='DIC (µmol C/kg)', ylabel='TA (µeq/kg)',
             title=('Local seawater pCO2 contours (µatm)\n'
                    f"L_b: {box['temperature']:g} °C, salinity {box['salinity']:g}, "
                    f"{box['pressure']:g} bar"))
    axis.legend(loc='upper left', fontsize=9, framealpha=0.95)
    fig.tight_layout()
    plt.show()
    return fig, axis


def plot_external_forcings(cases, *, pulse_start=1800.0):
    """Show the exact saved solver inputs before interpreting any response."""
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.3), layout='constrained')
    for column, (label, units) in enumerate((('OA', 'Tmol C/yr'),
                                            ('OAE', 'Tmol TA eq/yr'))):
        case = cases[label]
        time, flux = case.teaching_signal_time, case.teaching_signal_flux
        axes[column].plot(time, flux / 1e12, color=f'C{column}')
        axes[column].set(title=f'{label}: prescribed input', ylabel=units)
        axes[2].plot(time, flux / np.max(flux), color=f'C{column}',
                     linestyle='-' if column == 0 else '--', label=label)
    axes[2].set(title='Same shape and timing', ylabel='Fraction of own peak')
    axes[2].legend(frameon=False)
    for axis in axes:
        axis.axvline(pulse_start, color='0.5', linewidth=0.8, linestyle=':')
        axis.set(xlabel='Model year', ylim=(0, None))
        axis.grid(alpha=0.15)
    return fig, axes


def plot_matched_responses(cases, *, pulse_start=1800.0):
    """Four core diagnostic groups, each relative to its matched control."""
    control = cases['control']
    fig, axes = plt.subplots(4, 2, figsize=(10, 10), sharex=True)
    for column, label in enumerate(('OA', 'OAE')):
        case = cases[label]
        np.testing.assert_array_equal(case.time, control.time)
        axes[0, column].plot(case.time, (case.CO2_At.c - control.CO2_At.c) * 1e6)
        axes[1, column].plot(case.time, case.L_b.pH.c - control.L_b.pH.c)
        axes[2, column].plot(case.time, (case.D_b.DIC.c - control.D_b.DIC.c) * 1e6)
        axes[3, column].plot(case.time,
                            (case.D_b.Fdiss.c - control.D_b.Fdiss.c) / 1e12,
                            label='Dissolution')
        axes[3, column].plot(case.time,
                            (case.D_b.Fburial.c - control.D_b.Fburial.c) / 1e12,
                            label='Net burial', linestyle='--')
        axes[0, column].set_title(label)
        axes[3, column].set_xlabel('Model year')
        axes[3, column].legend(frameon=False)
        for axis in axes[:, column]:
            axis.axhline(0, color='0.5', linewidth=0.6)
            axis.axvline(pulse_start, color='0.7', linewidth=0.6)
            axis.grid(alpha=0.15)
    for axis, label in zip(axes[:, 0], ('Atmospheric CO2\nanomaly (ppm)',
                                      'Surface pH\nanomaly',
                                      'Deep DIC anomaly\n(umol/kg)',
                                      'Carbonate flux anomaly\n(Tmol C/yr)')):
        axis.set_ylabel(label)
    fig.suptitle('Carbon versus alkalinity input: forced minus matched control')
    fig.tight_layout()
    plt.show()
    return fig, axes

def plot_ta_free(M, config):
    fig, axes = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
    axes[0].plot(M.time, M.CO2_At.c * 1e6)
    axes[0].axhline(config.target_xco2_ppm, ls='--', color='gray', label='observed target')
    axes[0].set_ylabel('xCO2 (ppm)')
    axes[0].legend()
    axes[1].plot(M.time, M.Ocean.DIC.c * 1e6)
    axes[1].axhline(config.target_dic_umol_kg, ls='--', color='gray')
    axes[1].set(xlabel='Time (yr)', ylabel='DIC (umol/kg)')
    fig.tight_layout()
    plt.show()

def plot_equilibrium_curves(dic_grid, ocean_pco2, atm_pco2, config):
    """Supplied 01 plot: chemistry curves and the closed-inventory atmosphere.

    Intersections and their interpretation are left to the students. The
    second panel enlarges the region near the reference DIC, using linear axes.
    """
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
    for axis in axes:
        for (label, values), color in zip(ocean_pco2.items(), ("#c65b16", "#00857d")):
            axis.plot(dic_grid, values, label=f"ocn: {label}", color=color)
        axis.plot(dic_grid, atm_pco2, "--", color="#444444", label="atm: conserved carbon")
        axis.set(xlabel="DIC (µmol/kg)", ylabel="pCO₂ (µatm)")
        axis.grid(alpha=0.2)
    axes[0].set(xlim=(0, dic_grid[-1]), ylim=(0, 1.08 * max(atm_pco2)),
                title="Chemistry and carbon conservation")
    zoom_start = 0.93 * config.target_dic_umol_kg
    zoom = dic_grid >= zoom_start
    axes[1].set(xlim=(zoom_start, dic_grid[-1]),
                ylim=(0, 1.1 * max(atm_pco2[zoom])), title="Zoom near reference DIC")
    axes[0].legend(frameon=False, fontsize=9)
    plt.show()
    return fig, axes


def equilibration_time(case):
    """First saved time after which xCO2 stays within 1% of its final value.

    This threshold-based diagnostic depends on the initial state and tolerance;
    it is not an exponential relaxation constant or a test of stationarity.
    """
    x = case.CO2_At.c
    outside = np.flatnonzero(abs(x - x[-1]) > 0.01 * abs(x[-1]))
    return case.time[outside[-1] + 1] if len(outside) else case.time[0]


def plot_partition_comparison(buffered, partition, slower):
    fig, ax = plt.subplots(figsize=(7, 4))
    for label, case in [('near-empty ocean', buffered),
                        ('alternative partition', partition), ('half piston velocity', slower)]:
        ax.semilogy(case.time, case.CO2_At.c * 1e6, label=label)
        print(label, 'equilibration time (yr; 1% criterion):', equilibration_time(case))
    ax.set(xlim=(0, 300), xlabel='Time (yr)', ylabel='xCO2 (ppm)')
    ax.legend()
    plt.show()

def plot_pump_comparison(pump_off, pump_on, Jmix, Jpump):
    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    for label, case in [('pump off', pump_off), ('pump on', pump_on)]:
        axes[0].plot(case.time, case.CO2_At.c * 1e6, label=label)
    axes[0].set_ylabel('xCO2 (ppm)')
    axes[0].legend()
    axes[1].plot(pump_on.time, Jmix / 1e12, label='net mixing upward')
    axes[1].plot(pump_on.time, Jpump / 1e12, label='effective pump downward')
    axes[1].set(xlabel='Time (yr)', ylabel='Carbon flux (Tmol/yr)')
    axes[1].legend()
    plt.show()

def plot_synthetic_forcing(signal_time, signal_flux, forced, control):
    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    axes[0].plot(signal_time, signal_flux / 1e12)
    axes[0].set_ylabel('External C (Tmol/yr)')
    axes[1].plot(forced.time, forced.CO2_At.c * 1e6, label='finite addition')
    axes[1].plot(control.time, control.CO2_At.c * 1e6, label='matched control')
    axes[1].axhline(280, color='gray', ls='--')
    axes[1].set(xlabel='Time (yr)', ylabel='xCO2 (ppm)')
    axes[1].legend()
    plt.show()


def read_digitized(name, digitized):
    data = pd.read_csv(digitized / f'{name}.csv')
    return data.iloc[:, 0].to_numpy(), data.iloc[:, 1].to_numpy()


def plot_figure4(model, forcing, *, reference=False, digitized=None, pulse_start=1800.0):
    fig, axes = plt.subplots(4, 2, figsize=(13, 15), sharex=True)
    ax = axes.ravel()
    colors = {'L': 'C0', 'H': 'C1', 'D': 'C2'}

    for key, box, label in (
        ('L', model.L_b, 'Low latitude'),
        ('H', model.H_b, 'High latitude'),
        ('D', model.D_b, 'Deep box'),
    ):
        ax[0].plot(model.time, box.DIC.c * 1000, color=colors[key], label=label)
        ax[1].plot(model.time, box.TA.c * 1000, color=colors[key], label=label)
        ax[2].plot(model.time, box.pH.c, color=colors[key], label=label)

    gex_l = gas_exchange_fluxes(model.L_b.DIC, model.CO2_At, model.tutorial_params['piston_velocity'])
    gex_h = gas_exchange_fluxes(model.H_b.DIC, model.CO2_At, model.tutorial_params['piston_velocity'])
    ax[3].plot(model.time, gex_l, color='C0', label='Low-latitude GEX')
    ax[3].plot(model.time, gex_h, color='C1', label='High-latitude GEX')

    ax[4].plot(model.time, -model.D_b.zsat.c, color='C0', label=r'$z_{sat}$')
    ax[4].plot(model.time, -model.D_b.zcc.c, color='C1', label=r'$z_{cc}$')
    ax[4].plot(model.time, -model.D_b.zsnow.c, color='C2', label=r'$z_{snow}$')
    ax[5].plot(model.time, model.CO2_At.c * 1e6, color='C0', label='Atm CO2')

    signal = (
        model.carbon_signal if forcing == 'OA' else model.alkalinity_signal
    )
    ax[6].plot(model.time, signal.signal_data.m, color='C0', label=forcing)
    ax[7].plot(model.time, model.D_b.Fburial.c, color='C0', label='Net burial')
    ax[7].plot(model.time, model.D_b.Fdiss.c, color='C1', label='Dissolution')

    if reference:
        for panel, names in (
            (0, ('dic_l', 'dic_h', 'dic_d')),
            (1, ('TA_l', 'TA_h', 'TA_d')),
        ):
            for key, name in zip(('L', 'H', 'D'), names):
                x, y = read_digitized(name, digitized)
                ax[panel].plot(x, y, color=colors[key], linestyle=':', alpha=0.9)

        for key, name in zip(('L', 'H', 'D'), ('hplus_l', 'hplus_h', 'hplus_d')):
            x, y = read_digitized(name, digitized)
            ax[2].plot(x, -np.log10(y), color=colors[key], linestyle=':', alpha=0.9)

        for color, name in zip(('C0', 'C1'), ('EL', 'EH')):
            x, y = read_digitized(name, digitized)
            ax[3].plot(x, y * 1e13, color=color, linestyle=':', alpha=0.9)

        for color, name in zip(('C0', 'C1', 'C2'), ('zsat', 'zcc', 'zsnow')):
            x, y = read_digitized(name, digitized)
            ax[4].plot(x, -y, color=color, linestyle=':', alpha=0.9)

        x, y = read_digitized('pco2', digitized)
        ax[5].plot(x, y, color='C1', linestyle=':', label='Boudreau digitization')
        x, y = read_digitized('Cpulse', digitized)
        ax[6].plot(x, y, color='C1', linestyle=':', label='Published pulse')
        x, burial = read_digitized('Fburial', digitized)
        burial = burial * 1e13
        ax[7].plot(x, burial, color='C0', linestyle=':', alpha=0.9)
        ax[7].plot(x, 60e12 - burial, color='C1', linestyle=':', alpha=0.9)

    panel_titles = (
        'a) Dissolved inorganic carbon',
        'b) Total alkalinity',
        'c) pH',
        'd) Air–sea gas exchange',
        'e) Carbonate horizons',
        'f) Atm CO2',
        f'g) {forcing} forcing',
        'h) Carbonate burial and dissolution',
    )
    ylabels = (
        'DIC (mmol kg$^{-1}$)',
        'TA (meq kg$^{-1}$)',
        'pH',
        'Flux (mol C yr$^{-1}$)',
        'Elevation (m)',
        'Atmospheric CO2 (ppm)',
        'Input (mol C/yr)' if forcing == 'OA' else 'Input (mol TA eq/yr)',
        'Flux (mol C yr$^{-1}$)',
    )
    for axis, title, ylabel in zip(ax, panel_titles, ylabels):
        axis.set_title(title, loc='left')
        axis.set_ylabel(ylabel)
        axis.axvline(pulse_start, color='0.75', linewidth=0.7)
        axis.grid(alpha=0.15)
        axis.legend(frameon=False, fontsize=8)
    for axis in axes[-1, :]:
        axis.set_xlabel('Model year')
    fig.suptitle(
        f'{forcing}: complete Boudreau-like model with constant pumps',
        fontsize=15,
        y=1.01,
    )
    fig.tight_layout()
    return fig, axes


def response_summary(forced, control):
    pco2 = (forced.CO2_At.c - control.CO2_At.c) * 1e6
    ph = forced.L_b.pH.c - control.L_b.pH.c
    zsat = forced.D_b.zsat.c - control.D_b.zsat.c
    zcc = forced.D_b.zcc.c - control.D_b.zcc.c
    zsnow = forced.D_b.zsnow.c - control.D_b.zsnow.c
    burial = forced.D_b.Fburial.c - control.D_b.Fburial.c
    dissolution = forced.D_b.Fdiss.c - control.D_b.Fdiss.c
    return {
        'maximum pCO2 anomaly (ppm)': pco2.max(),
        'final pCO2 anomaly (ppm)': pco2[-1],
        'minimum surface pH anomaly': ph.min(),
        'maximum surface pH anomaly': ph.max(),
        'minimum zsat anomaly (m)': zsat.min(),
        'maximum zsat anomaly (m)': zsat.max(),
        'minimum zcc anomaly (m)': zcc.min(),
        'maximum zcc anomaly (m)': zcc.max(),
        'final zsnow anomaly (m)': zsnow[-1],
        'minimum burial anomaly (Tmol/yr)': burial.min() / 1e12,
        'maximum burial anomaly (Tmol/yr)': burial.max() / 1e12,
        'maximum dissolution anomaly (Tmol/yr)': dissolution.max() / 1e12,
    }
