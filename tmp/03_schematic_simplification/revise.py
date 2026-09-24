from pathlib import Path
import sys
import re
import hashlib
import json
import nbformat

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT))
from teaching_specification import flux_table_markdown
from scripts.build_student_notebooks import build_student_notebook
if not (OUT/'protected.json').exists():
    paths=[p for folder in ('notebooks','archive','data') for p in (ROOT/folder).rglob('*')
           if p.is_file() and not p.name.startswith('~$') and p.suffix!='.log'
           and '.ipynb_checkpoints' not in p.parts and '__pycache__' not in p.parts]
    (OUT/'protected.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}))

source=ROOT/'notebooks/instructor/03_boudreau_three_box_model.ipynb'
nb=nbformat.read(OUT/'before.ipynb',4)
for cell in nb.cells:
    if cell.cell_type!='markdown': continue
    s=cell.source
    s=s.replace(r'| $Q_{ij},q_{ij}$ | Water volume transport [m³/yr] and physical mass transport $q_{ij}=\rho_iQ_{ij}$ [kg/yr] |',
                r'| $Q_{ij}$ | Water volume transport from $i$ to $j$ [m³/yr]; $\rho_iQ_{ij}$ converts it to mass transport [kg/yr] |')
    s=re.sub(r'Weathering\x27s 1 carbon : 2 TA is a .*?https://doi.org/10.1029/2019RG000681\)\.',
             'The model adds **1 mole of DIC and 2 equivalents of TA** through weathering. Real riverine input need not have exactly this 1:2 ratio.',s,flags=re.S)
    s=s.replace(r'For a directed physical water transport, $q_{i\to j}=\rho Q_{i\to j}$ in kg/yr and'+'\n'+
                r'$$J_{i\to j}^{(X)}(t)=q_{i\to j}X_i(t),\qquad X=\mathrm{DIC\ or\ TA}.$$',
                r'For water volume transport $Q_{ij}$ [m³/yr], the physical tracer flux is'+'\n'+
                r'$$J_{ij}^{X}(t)=\rho_iQ_{ij}X_i(t),\qquad X=\mathrm{DIC\ or\ TA}.$$')
    if '| Process | Arrow |' in s:
        start=s.index('| Process | Arrow |')
        end=s.index('\n\nFor any internal dissolved transfer',start)
        s=s[:start]+flux_table_markdown(student=True)+s[end:]
        s=s.replace('F1–F8 are paper aliases, not new variables: use the descriptive process IDs below.',
                    'Label water arrows with $Q$ (circulation: $Q_{LH},Q_{HD},Q_{DL}$; mixing: $Q_{mix,down},Q_{mix,up}$). The paired $J$ equations describe the tracers they carry. F1–F8 remain paper aliases.')
    if s.startswith('### Supplied weathering connection'):
        s='''### Supplied weathering connection

The workbook supplies `weathering_dic`; the loader sets the TA input to twice that rate. Run the supplied connection.
'''
    cell.source=s
nbformat.write(nb,source)
build_student_notebook(source,ROOT/'notebooks/student'/source.name)

p=ROOT/'scripts/build_boudreau_diagrams.py'
text=p.read_text()
text=text.replace('W, H = 1560, 1270','W, H = 1560, 850')
start=text.index('def reconstruction_sheet():')
end=text.index('\ndef main():',start)
replacement='''def reconstruction_sheet():
    """An uncluttered outline; answers live only in the instructor drawing."""
    c = Canvas()
    c.text(30, 42, '03.1   Label the model with your flux equations', 30, bold=True)
    c.text(30, 80, 'Add states, arrows and the active atm + ocn boundary. Repeated boxes are the same reservoirs.', 21)
    for x, title in ((30, 'A   Water and gas'), (785, 'B   Export and carbonate processes')):
        c.rect(x, 125, 745 if x == 785 else 725, 575, white, HexColor('#BCCAD3'))
        c.text(x+20, 160, title, 23, bold=True)
    c.box(90, 190, 615, 65, 'atm [CO2_At]', 'State:')
    c.box(90, 365, 230, 85, 'Low latitude [L_b]', 'States:')
    c.box(475, 365, 230, 85, 'High latitude [H_b]', 'States:')
    c.box(90, 585, 615, 80, 'Deep ocean [D_b]', 'States:')
    c.box(830, 268, 260, 75, 'Low latitude [L_b]', 'Same box as in A')
    c.box(830, 523, 260, 80, 'Deep ocean [D_b]', 'Same box as in A')
    c.rect(1250, 395, 255, 130, HexColor('#FFF6EA'), ORANGE)
    c.text(1264, 424, 'Carbonate / sediment', 20, bold=True)
    c.text(1264, 453, 'process module', 21, bold=True)
    c.text(1264, 483, 'Snowline memory;', 17)
    c.text(1264, 508, 'no sediment C stock.', 17)
    c.text(30, 745, 'Q: water volume transport. J: paired DIC and TA amount fluxes from your table.', 22, bold=True)
    c.text(30, 781, 'Include gas exchange, POC, PIC, weathering, dissolution and signed net burial. A paper sketch is sufficient.', 20)
    c.text(30, 826, 'Course adaptation of Wortmann et al. (2025), Fig. 3. Source corrections and input links are in notebook 03.', 17, MUTED)
    return c.d


def diagram(student, p):
    if student:
        return reconstruction_sheet()
    c = Canvas()
    c.text(30, 42, '03 / 04   Model schematic', 32, bold=True)
    c.text(1140, 42, 'INSTRUCTOR REFERENCE', 23, PURPLE, True)
    c.text(30, 80, 'Repeated boxes are the same reservoirs. Use the companion table for paired DIC / TA equations.', 21)
    c.rect(30, 125, 725, 575, white, HexColor('#BCCAD3'))
    c.rect(785, 125, 745, 575, white, HexColor('#BCCAD3'))
    c.text(50, 160, 'A   Water and gas', 23, bold=True)
    c.text(805, 160, 'B   Export and carbonate processes', 23, bold=True)
    c.box(90, 190, 615, 65, 'atm [CO2_At]', 'State: CO2 mole fraction')
    c.box(90, 365, 230, 85, 'Low latitude [L_b]', 'DIC, TA')
    c.box(475, 365, 230, 85, 'High latitude [H_b]', 'DIC, TA')
    c.box(90, 585, 615, 80, 'Deep ocean [D_b]', 'DIC, TA')
    for x in (180, 545):
        c.arrow([(x,255),(x,365)], GREEN)
        c.arrow([(x+55,365),(x+55,255)], GREEN)
    c.text(100, 304, 'G_L', 20, GREEN, True)
    c.text(625, 304, 'G_H', 20, GREEN, True)
    c.arrow([(320,405),(475,405)])
    c.text(364, 385, 'Q_LH', 20, BLUE, True)
    c.arrow([(535,450),(535,585)])
    c.text(450, 495, 'Q_HD', 19, BLUE, True)
    c.arrow([(130,585),(130,450)])
    c.text(150, 505, 'Q_DL', 19, BLUE, True)
    c.arrow([(620,450),(620,585)])
    c.arrow([(680,585),(680,450)])
    c.text(551, 553, 'Q_mix,down', 13, BLUE)
    c.text(685, 575, 'Q_mix,up', 13, BLUE)
    c.text(105, 683, f"Circulation: {p['thc']:g} Sv on each leg. Mixing: {p['mixing']:g} Sv each way.", 18, BLUE)
    c.rect(810, 248, 300, 398, None, MUTED, dashed=True)
    c.box(830, 268, 260, 75, 'Low latitude [L_b]', 'Same box as in A')
    c.box(830, 523, 260, 80, 'Deep ocean [D_b]', 'Same box as in A')
    c.text(824, 634, 'ocn part of active atm + ocn', 17, MUTED)
    c.text(855, 209, 'W: weathering', 20, ORANGE, True)
    c.arrow([(955,218),(955,268)], ORANGE)
    c.arrow([(890,343),(890,523)], GREEN)
    c.text(912, 427, 'POC', 21, GREEN, True)
    c.arrow([(1090,300),(1355,300),(1355,395)], ORANGE)
    c.text(1140, 283, 'PIC (E)', 20, ORANGE, True)
    c.rect(1250, 395, 255, 130, HexColor('#FFF6EA'), ORANGE)
    c.text(1264, 424, 'Carbonate / sediment', 20, bold=True)
    c.text(1264, 453, 'process module', 21, bold=True)
    c.text(1264, 483, 'Snowline memory;', 17)
    c.text(1264, 508, 'no sediment C stock.', 17)
    c.arrow([(1250,465),(1150,465),(1150,555),(1090,555)], ORANGE)
    c.text(1117, 444, 'D: dissolution', 18, ORANGE, True)
    c.arrow([(1090,584),(1188,584),(1188,505),(1250,505)], PURPLE, dashed=True)
    c.text(1120, 626, 'Deep chemistry', 17, PURPLE)
    c.arrow([(1415,525),(1415,615)], ORANGE)
    c.text(1270, 652, 'B_net: net burial', 20, ORANGE, True)
    c.text(1270, 678, 'Signed residual, no extra drain', 16, MUTED)
    c.text(30, 745, 'Q: water volume transport [Sv]. 1 Sv = 10^6 m3/s. J equations: companion flux table.', 21, bold=True)
    c.text(30, 781, 'Solid arrows: material transfer. Dashed arrow: information. Grey outline: active ocean inventories.', 20)
    c.text(30, 826, 'Course adaptation of Wortmann et al. (2025), Fig. 3. Parameters and Excel-to-code links remain in notebook 03.', 17, MUTED)
    return c.d

'''
p.write_text(text[:start]+replacement+text[end:],encoding='utf-8')
print('Revised notebook 03, student copy and diagram source.')
