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

W, H = 1560, 850
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


def reconstruction_sheet():
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
