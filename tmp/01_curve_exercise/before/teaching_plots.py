"""Supplied plots for the guided practical; model construction stays in notebooks."""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from esbmtk import gas_exchange_fluxes

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
    ax[5].plot(model.time, model.CO2_At.c * 1e6, color='C0', label='pCO2')

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
        'f) Atmospheric pCO2',
        f'g) {forcing} forcing',
        'h) Carbonate burial and dissolution',
    )
    ylabels = (
        'DIC (mmol kg$^{-1}$)',
        'TA (mmol kg$^{-1}$)',
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
