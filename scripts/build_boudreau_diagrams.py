"""Build paired teaching schematics; read numerical labels from the 03/04 workbook.

Authoring dependencies: ReportLab, openpyxl and Poppler. No model is run and no
workbook or notebook is modified. The student drawing is built independently,
so its SVG contains no hidden instructor answers.
"""
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Drawing, Rect, Line, Polygon, String
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model_inputs import read_model_tables

W, H = 1560, 1270
INK, MUTED = HexColor('#183747'), HexColor('#526773')
BLUE, GREEN, ORANGE = map(HexColor, ('#246596', '#257763', '#AD6221'))
PURPLE, PALE, GOLD = map(HexColor, ('#7952A8', '#F3F7FA', '#FFF0B3'))


class Canvas:
    def __init__(self):
        self.d = Drawing(W, H)
        self.d.add(Rect(0, 0, W, H, fillColor=white, strokeColor=None))

    def text(self, x, y, value, size=18, color=INK, bold=False, max_width=None):
        font = 'Helvetica-Bold' if bold else 'Helvetica'
        if max_width is not None:
            assert stringWidth(value, font, size) <= max_width, value
        self.d.add(String(x, H-y, value, fontName=font, fontSize=size, fillColor=color))

    def rect(self, x, y, w, h, fill=PALE, stroke=BLUE, dashed=False):
        self.d.add(Rect(x, H-y-h, w, h, rx=9, ry=9, fillColor=fill,
                        strokeColor=stroke, strokeWidth=1.4,
                        strokeDashArray=[6, 5] if dashed else None))

    def arrow(self, points, color=BLUE, dashed=False, head=True):
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            self.d.add(Line(x1, H-y1, x2, H-y2, strokeColor=color,
                            strokeWidth=2.7, strokeDashArray=[6, 5] if dashed else None))
        if head:
            (a, b), (x, y) = points[-2:]
            dx, dy = x-a, y-b
            length = (dx*dx+dy*dy)**.5
            ux, uy = dx/length, dy/length
            self.d.add(Polygon([x,H-y,x-12*ux+5*uy,H-(y-12*uy-5*ux),
                                x-12*ux-5*uy,H-(y-12*uy+5*ux)],
                               fillColor=color, strokeColor=color))

    def box(self, x, y, w, h, title, detail):
        self.rect(x, y, w, h)
        self.text(x+14, y+29, title, 21, bold=True, max_width=w-28)
        self.text(x+14, y+55, detail, 17, max_width=w-28)


def inputs():
    tables = read_model_tables()
    p = {r['Parameter']: r['Value'] for r in tables['ProcessParameters']}
    actual = {(r['source'], r['sink'], r['flux_id'], r['Parameter'])
              for r in tables['TransportConnections']}
    expected = {('L_b','H_b','thc','thc'), ('H_b','D_b','thc','thc'),
                ('D_b','L_b','thc','thc'), ('H_b','D_b','mix_down','mixing'),
                ('D_b','H_b','mix_up','mixing')}
    if actual != expected or len(tables['TransportConnections']) != 5:
        raise ValueError('Workbook transport topology changed; revise schematic layout.')
    if {(r['Atmosphere'],r['Surface']) for r in tables['GasExchangeConnections']} != {
            ('CO2_At','L_b'), ('CO2_At','H_b')}:
        raise ValueError('Workbook gas topology changed; revise schematic layout.')
    if {r['Box ID'] for r in tables['OceanReservoirs']} != {'L_b','H_b','D_b'}:
        raise ValueError('Workbook ocean boxes changed.')
    return p


def diagram(student, p):
    c = Canvas()
    role = 'STUDENT WORKSHEET' if student else 'INSTRUCTOR REFERENCE'
    c.text(30, 42, '03 / 04   Boudreau-like carbon-cycle model', 32, bold=True)
    c.rect(1175, 16, 355, 40, HexColor('#EDF5FF') if student else HexColor('#F3EEFB'),
           BLUE if student else PURPLE)
    c.text(1193, 43, role, 21, BLUE if student else PURPLE, bold=True)
    c.text(30, 78, 'Two views of the same model: repeated L_b and D_b boxes represent the same ocean inventories.', 20)
    c.text(30, 108, 'Solid lines: material transfers. Dashed arrows: information. Grey dashed outline: active-system boundary.', 18, MUTED)

    c.rect(30, 130, 725, 565, white, HexColor('#BCCAD3'))
    c.rect(785, 130, 745, 565, white, HexColor('#BCCAD3'))
    c.text(50, 163, 'A   Circulation and air-sea exchange', 23, bold=True)
    c.text(805, 163, 'B   Export, dissolution and net burial', 23, bold=True)

    c.box(90, 190, 615, 65, 'Atmosphere / atm  [CO2_At]', 'State: dry-air CO2 mole fraction; fixed total air inventory')
    c.box(90, 365, 230, 85, 'Low latitude [L_b]', 'ocn states: DIC, TA')
    c.box(475, 365, 230, 85, 'High latitude [H_b]', 'ocn states: DIC, TA')
    c.box(90, 585, 615, 80, 'Deep ocean [D_b]', 'ocn states: DIC, TA; each box has its own geometry and T/S/P')
    for x in (180, 545):
        c.arrow([(x,255),(x,365)], GREEN)
        c.arrow([(x+55,365),(x+55,255)], GREEN)
    c.text(100, 295, 'G_L', 18, GREEN, True)
    c.text(100, 320, 'in / out', 16, GREEN)
    c.text(627, 295, 'G_H', 18, GREEN, True)
    c.text(627, 320, 'in / out', 16, GREEN)
    c.arrow([(320,405),(475,405)], head=not student)
    c.text(342, 385, 'T_LH' + ('  ?' if student else ''), 19, BLUE, True)
    c.text(341, 435, f"{p['thc']:g} Sv", 17, BLUE)
    c.arrow([(535,450),(535,585)])
    c.text(465, 505, 'T_HD', 18, BLUE, True)
    c.arrow([(130,585),(130,450)])
    c.text(148, 505, 'T_DL', 18, BLUE, True)
    c.text(148, 530, 'same circulation rate on all 3 legs', 16, MUTED)
    c.arrow([(620,450),(620,585)])
    c.arrow([(680,585),(680,450)])
    c.text(551, 555, 'M_down', 14, BLUE)
    c.text(687, 555, 'M_up', 14, BLUE)
    c.text(350, 684, f"Mixing: {p['mixing']:g} Sv in each direction", 16, BLUE)

    # The process module sits outside the active dissolved inventory boundary.
    c.rect(810, 248, 300, 398, None, MUTED, dashed=True)
    c.text(824, 634, 'ocn part of active atm + ocn', 17, MUTED)
    c.box(830, 268, 260, 75, 'Low latitude [L_b]', 'Same box as in panel A')
    c.box(830, 523, 260, 80, 'Deep ocean [D_b]', 'Same box as in panel A')
    c.text(842, 203, 'W  External weathering', 20, ORANGE, True)
    c.arrow([(955,211),(955,268)], ORANGE)
    c.arrow([(890,343),(890,523)], GREEN, head=not student)
    c.text(910, 410, 'POC' + ('  ?' if student else ''), 20, GREEN, True)
    c.text(910, 438, 'Export +', 17, GREEN)
    c.text(910, 461, 'remineralization', 17, GREEN)
    c.arrow([(1090,300),(1355,300),(1355,395)], ORANGE)
    c.text(1135, 282, 'PIC  CaCO3 export', 20, ORANGE, True)
    c.rect(1250, 395, 255, 130, HexColor('#FFF6EA'), ORANGE)
    c.text(1264, 424, 'Carbonate / sediment', 20, bold=True)
    c.text(1264, 451, 'process module', 21, bold=True)
    c.text(1264, 483, 'Snowline is a dynamic state;', 16)
    c.text(1264, 507, 'no explicit sediment C inventory.', 15)
    c.arrow([(1250,465),(1150,465),(1150,555),(1090,555)], ORANGE,
            head=not student)
    c.text(1118, 445, 'D  _________' if student else 'D  Dissolution', 18, ORANGE, True)
    c.arrow([(1090,584),(1188,584),(1188,505),(1250,505)], PURPLE, dashed=True)
    c.text(1122, 611, 'Deep carbonate chemistry', 16, PURPLE)
    c.text(1122, 634, 'informs sediment response', 16, PURPLE)
    c.arrow([(1415,525),(1415,615)], ORANGE)
    c.text(1275, 660, 'B  _____________' if student else 'B  Signed net burial', 19, ORANGE, True)
    c.text(1275, 682, 'Label residual flux' if student else 'Removal from active atm + ocn', 15, MUTED)
    c.text(805, 682, 'No POC or PIC export from H_b in this benchmark.', 16, MUTED)

    c.text(30, 733, 'Complete the transfer properties and use the workbook to locate each input.' if student
           else 'Transfer properties and workbook-to-code cross-reference', 23, bold=True)
    widths = [205, 505, 425, 365]
    xs = [30,235,740,1165]
    headers = ['Arrow / process', 'What moves / rate rule', 'Excel table or parameter', 'Native object / supplied code']
    for x,w,h in zip(xs,widths,headers):
        c.rect(x,752,w,37,HexColor('#E7EFF5'),white)
        c.text(x+10,777,h,17,bold=True,max_width=w-20)
    blank = lambda answer: '____________________________________' if student else answer
    rows = [
        ('T_* / M_*', blank('DIC + TA; J_X(t) = q x X_source(t)'), 'TransportConnections: source / sink / flux_id', 'scale_with_concentration'),
        ('G_L / G_H', blank('Carbon only; invasion minus outgassing'), 'GasExchangeConnections; piston_velocity', 'gasexchange; one object per surface'),
        ('POC', blank(f"DIC only; fixed {p['poc_export']:g} Tmol C/yr"), 'ProcessParameters: poc_export', 'POM'),
        ('PIC', blank(f"1 DIC : 2 TA; {p['poc_export']*p['rain_ratio']:g} Tmol C/yr"), 'poc_export x rain_ratio (PIC/POC)', 'PIC_DIC + PIC_TA; sink bypass'),
        ('W', f"1 DIC : 2 TA; {p['weathering_dic']:g} Tmol C/yr (supplied)", 'weathering_dic; TA = 2 x carbon input', 'weathering; Fw to L_b'),
        ('D', blank('1 DIC : 2 TA; calculated dissolution'), 'Calculated response, not a prescribed flux', 'carbonate system 2; diagnostic' if student else 'carbonate system 2; Fdiss'),
        ('B', blank('PIC - D; net removal in a 1:2 ratio'), 'Calculated response, not a prescribed flux', 'carbonate system 2; diagnostic' if student else 'Fburial diagnostic; implicit boundary'),
    ]
    for i,row in enumerate(rows):
        y=789+i*43
        c.rect(30,y,1500,43,white if i%2 else PALE,white)
        for j,(x,w,value) in enumerate(zip(xs,widths,row)):
            c.text(x+10,y+28,value,17,bold=j==0,max_width=w-20)

    c.rect(30,1104,1500,76,HexColor('#EDF5FF') if student else HexColor('#F3EEFB'),
           BLUE if student else PURPLE)
    if student:
        c.text(45,1130,'Question: add the three missing arrowheads, label D and B, and complete the six blank property cells.',19,bold=True)
        c.text(45,1158,'Check water balance at every box. Explain which transfers change the combined atm + ocn inventories.',19)
    else:
        c.text(45,1130,'Budget check: internal water, gas and POC transfers cancel. dC_atm+ocn/dt = W - B; dTA_ocn/dt = 2(W - B).',18,bold=True)
        c.text(45,1158,'Unforced baseline. B < 0 means net sediment loss: dissolution can exceed contemporary PIC rain.',19)
    c.text(30,1206,'Units: DIC in mol C/kg; TA in mol equivalents/kg. Carbon fluxes in Tmol C/yr; TA fluxes in Tmol equivalents/yr.',17,MUTED)
    c.text(30,1231,'Workbook: data/Boudreau_2010/model_definition.xlsx. Reservoir tables own geometry, T/S/P and initial states; restart replaces states.',17,MUTED)
    c.text(30,1256,'Teaching adaptation of the ESBMTK Boudreau benchmark (Wortmann et al., 2025, Fig. 3). See companion notes for transport units and source aliases.',16,MUTED)
    return c.d


def main():
    renderer = shutil.which('pdftoppm')
    if not renderer:
        raise RuntimeError('Poppler pdftoppm must be on PATH.')
    output = ROOT / 'ref/figures'
    output.mkdir(parents=True,exist_ok=True)
    p = inputs()
    for student in (False,True):
        name = '03_04_boudreau_' + ('student' if student else 'instructor')
        drawing = diagram(student,p)
        renderSVG.drawToFile(drawing,str(output / (name+'.svg')))
        with TemporaryDirectory(prefix='boudreau_diagram_') as tmp:
            pdf = Path(tmp)/'diagram.pdf'
            renderPDF.drawToFile(drawing,str(pdf))
            subprocess.run([renderer,'-singlefile','-scale-to','2340','-png',str(pdf),
                            str(output/name)],check=True)
        print(f'Built {name}.svg and .png')


if __name__ == '__main__':
    main()
