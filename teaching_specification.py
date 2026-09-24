"""Teaching-only flux records for the 03 reconstruction and its worksheets.

Numerical inputs remain in the existing workbook. These records document the
specialized process wiring in model.py; they are not executable model inputs.
Student records contain prompts, never concealed instructor answers.
"""
from model_inputs import read_model_tables


BASELINE_PARAMETERS = (
    'thc', 'mixing', 'poc_export', 'rain_ratio', 'weathering_dic',
    'alpha', 'z0', 'piston_velocity', 'opt_k_carbonic', 'opt_pH_scale',
)


def flux_specification(*, student=False, latex=False):
    """Paired amount fluxes for each arrow, not concentration tendencies.

    Positive follows the listed arrow. Gas exchange and net burial are signed.
    DIC labels the carbon removed from/returned to dissolved inventories, even
    when transported as CO2 or particles. Latex is for notebook Markdown only;
    Excel receives readable text equations, never executable Excel formulas.
    """
    def equation(plain, math):
        return f'${math}$' if latex else plain

    rows = [
        ('Q_*', 'Water: i -> j',
         equation('rho_i Q_ij DIC_i(t)', r'\rho_i Q_{ij}DIC_i(t)'),
         equation('rho_i Q_ij TA_i(t)', r'\rho_i Q_{ij}TA_i(t)'),
         'Q_ij: water volume transport (m3/yr), from thc / mixing. Use source density and concentration.'),
        ('G_L / G_H', 'Gas: atm -> surface i (signed)',
         equation('v_i A_i [K0_i pCO2_atm(t) - c_i(t)]',
                  r'v_i A_i[K_{0,i}pCO_{2,atm}(t)-c_i(t)]'),
         equation('0', '0'),
         'piston_velocity, area; K0_i and c_i from local chemistry. Invasion minus outgassing.'),
        ('POC', 'Organic export: L_b -> D_b',
         equation('P_0', 'P_0'), equation('0', '0'),
         'P_0 = poc_export; fixed, fully remineralized at depth; DIC-only closure.'),
        ('PIC', 'Carbonate export: L_b -> module',
         equation('E(t) = r P_0', r'E(t)=rP_0'),
         equation('2 E(t)', r'2E(t)'),
         'r = rain_ratio (PIC/POC); CaCO3 formation removes 1 carbon and 2 TA equivalents.'),
        ('W', 'Weathering: outside -> L_b',
         equation('W_0', 'W_0'), equation('2 W_0', '2W_0'),
         'W_0 = weathering_dic; the model adds 2 TA equivalents per mole of DIC.'),
        ('D', 'Dissolution: module -> D_b',
         '$D(t)$ (supplied)' if latex else 'D(t) [supplied response]',
         equation('2 D(t)', r'2D(t)'),
         'D = sediment_response(E, DIC_d, TA_d, z_snow; T_d, S_d, p_d, alpha, z0). Reverse CaCO3 formation.'),
        ('B_net', 'Net burial: module -> outside (signed)',
         equation('B_net(t) = E(t) - D(t)', r'B_{net}(t)=E(t)-D(t)'),
         equation('2 B_net(t)', r'2B_{net}(t)'),
         'Compare carbonate rain and dissolution, including old sediment; residual, not an extra drain.'),
    ]
    columns = ('Process ID', 'Process / arrow', 'J_DIC (mol C/yr)',
               'J_TA (eq/yr)', 'Inputs / hint')
    result = [dict(zip(columns, row)) for row in rows]
    if student:
        for row in result:
            row['J_TA (eq/yr)'] = 'Your expression'
            if row['Process ID'] != 'D':
                row['J_DIC (mol C/yr)'] = 'Your expression'
            if row['Process ID'] == 'POC':
                row['Process / arrow'] = 'Organic export: your arrow'
    return result


def flux_table_markdown(*, student=False):
    """Editable student Markdown and a fitted instructor table from one source."""
    rows = flux_specification(student=student, latex=True)
    headers = ('Process', 'Arrow', r'$J^{DIC}(t)$ [mol C/yr]',
               r'$J^{TA}(t)$ [eq/yr]', 'Inputs / hint')
    if not student:
        # Establish widths before MathJax typesets the reference equations.
        # Automatic table layout can otherwise squeeze its own math columns.
        from html import escape
        widths = (8, 20, 28, 14, 30)
        header = ''.join(f'<th style="width:{width}%;text-align:left">{escape(label)}</th>'
                         for width, label in zip(widths, headers))
        body = ''.join('<tr>' + ''.join(f'<td style="vertical-align:middle">{escape(value)}</td>'
                                       for value in row.values()) + '</tr>' for row in rows)
        return '<table style="width:100%;table-layout:fixed"><thead><tr>' + header + \
               '</tr></thead><tbody>' + body + '</tbody></table>'
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(row.values()) + ' |' for row in rows])


def implementation_references(*, student=False):
    """No numerical duplicates. Reveal endpoints only in the reconciliation."""
    rows = [
        ('Q_*', 'TransportConnections (Transport)',
         '(source, sink, flux_id); Parameter -> thc or mixing',
         'create_bulk_connections; concentration-dependent law'),
        ('G_L / G_H', 'GasExchangeConnections (GasExchange)',
         'Atmosphere + Surface; Parameter -> piston_velocity',
         'Species2Species; gasexchange'),
        ('POC', 'ProcessParameters (Parameters)', 'poc_export',
         'POM: native fixed export/remineralization connection'),
        ('PIC', 'ProcessParameters (Parameters)', 'poc_export * rain_ratio',
         'PIC_DIC + PIC_TA; nominal deep sinks bypassed'),
        ('W', 'ProcessParameters + BoundaryNodes', 'weathering_dic; Fw',
         'ConnectionProperties; linked TA rate'),
        ('D', 'Calculated, no flux input row', 'alpha, z0; actual PIC flux object',
         'add_carbonate_system_2; Fdiss for plotting'),
        ('B_net', 'Calculated, no flux input row', 'PIC export and dissolution',
         'Fburial diagnostic; Fb is not an extra active drain'),
    ]
    if student:
        rows = [(a, b, c, 'Match after your reconstruction' if a in
                 ('Q_*', 'G_L / G_H', 'POC') else d)
                for a, b, c, d in rows]
    return [dict(zip(('Process ID', 'Workbook owner', 'Stable key / dependency',
                      'Supplied implementation'), row)) for row in rows]


def workbook_connections(path=None):
    """Endpoint-qualified identifiers remain unique if the workbook is sorted."""
    tables = read_model_tables() if path is None else read_model_tables(path)
    rows = []
    for r in sorted(tables['TransportConnections'], key=lambda r: r['Order']):
        rows.append({'ID': f"{r['source']}_to_{r['sink']}@{r['flux_id']}",
                     'Source': r['source'], 'Sink': r['sink'],
                     'Species': r['Species'], 'Parameter': r['Parameter']})
    for r in sorted(tables['GasExchangeConnections'], key=lambda r: r['Order']):
        rows.append({'ID': f"{r['Atmosphere']}_to_{r['Surface']}@gas",
                     'Source': r['Atmosphere'], 'Sink': r['Surface'],
                     'Species': r['Species'], 'Parameter': r['Parameter']})
    return rows
