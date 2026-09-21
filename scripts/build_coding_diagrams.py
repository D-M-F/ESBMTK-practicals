"""Vector diagrams for the coding reference and notebook 01.

ReportLab drawings are the shared source for SVG, PNG and the handout PDF.
PNG export uses pdftoppm (Poppler) on PATH; no extra student dependency is needed.
"""

from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory

from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Drawing, Rect, Line, Polygon, String
from reportlab.lib import colors


ROOT = Path(__file__).resolve().parents[1]
INK = colors.HexColor("#183747")
TEAL = colors.HexColor("#007F83")
BLUE = colors.HexColor("#246596")
PALE = colors.HexColor("#EDF5F7")
GRAY = colors.HexColor("#607582")
WHITE = colors.white


class Diagram:
    """Use top-down coordinates for easy alignment of labelled elements."""

    def __init__(self, height):
        self.height = height
        self.drawing = Drawing(1080, height)
        self.rect(0, 0, 1080, height, WHITE, WHITE)

    def rect(self, x, y, w, h, fill=PALE, stroke=TEAL):
        self.drawing.add(Rect(x, self.height-y-h, w, h, rx=9, ry=9,
                              fillColor=fill, strokeColor=stroke, strokeWidth=1.5))

    def text(self, x, y, value, size=18, font="Helvetica", color=INK):
        self.drawing.add(String(x, self.height-y, value, fontName=font,
                                fontSize=size, fillColor=color))

    def code(self, x, y, value, size=17):
        self.text(x, y, value, size, "Courier", BLUE)

    def arrow(self, points, dashed=False, both=False):
        color = TEAL if dashed else BLUE
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            self.drawing.add(Line(x1, self.height-y1, x2, self.height-y2,
                                  strokeColor=color, strokeWidth=2.5,
                                  strokeDashArray=[7, 5] if dashed else None))
        def head(tail, tip):
            x, y = tip
            dx, dy = x-tail[0], y-tail[1]
            length = (dx*dx+dy*dy)**.5
            ux, uy = dx/length, dy/length
            coords = [x, self.height-y,
                      x-11*ux+5*uy, self.height-(y-11*uy-5*ux),
                      x-11*ux-5*uy, self.height-(y-11*uy+5*ux)]
            self.drawing.add(Polygon(coords, fillColor=color, strokeColor=color))
        head(points[-2], points[-1])
        if both:
            head(points[1], points[0])


def box_code_map():
    d = Diagram(640)
    d.rect(12, 10, 1056, 330, WHITE, GRAY)
    d.text(28, 36, "MODEL CONTAINER", 18, "Helvetica-Bold")
    d.code(242, 36, "M = Model(...)")
    d.text(428, 36, "clock + units + registered objects (not the physical boundary)", 17)
    for x, name in ((26, "A"), (724, "B")):
        d.rect(x, 53, 330, 273)
        d.text(x+14, 80, f"BOX {name}", 20, "Helvetica-Bold")
        d.code(x+103, 80, f"Reservoir -> M.{name}", 18)
        d.text(x+14, 108, "Geometry", 17, "Helvetica-Bold")
        d.code(x+14, 129, "volume=... / geometry=...", 17)
        d.text(x+14, 158, "Tracers / evolving states", 17, "Helvetica-Bold")
        d.code(x+14, 179, f"M.{name}.DIC.c, M.{name}.TA.c", 17)
        d.text(x+14, 208, "Initial concentrations", 17, "Helvetica-Bold")
        d.code(x+14, 229, "concentration={M.DIC: ...}", 17)
        d.text(x+14, 258, "Conditions: temperature, salinity, pressure", 15)
        d.code(x+14, 279, "seawater_parameters={...}", 17)
        d.text(x+14, 310, "Own geometry, states and starting values", 15, color=GRAY)
    d.text(386, 83, "CONNECTION / RATE LAW", 18, "Helvetica-Bold")
    d.code(386, 110, "Species2Species(...)", 18)
    d.code(386, 141, "source=M.A.DIC", 18)
    d.code(386, 165, "sink=M.B.DIC", 18)
    d.code(386, 195, "ctype=...", 18)
    d.code(386, 219, "rate=... / scale=...", 18)
    d.arrow([(356, 248), (724, 248)])
    d.text(376, 274, "-J(t)", 18, "Helvetica-Bold", BLUE)
    d.text(630, 274, "+J(t)", 18, "Helvetica-Bold", BLUE)
    d.text(446, 274, "mol/time", 17)
    d.text(386, 307, "Same amount; opposite signs", 17)
    d.text(26, 365, "Solid arrow = material transfer. Dashed arrow = information used in a calculation.", 18)
    d.arrow([(190, 326), (190, 342), (13, 342), (13, 441), (28, 441)], dashed=True)
    d.text(26, 397, "PROCESSES AND CALCULATED QUANTITIES", 18, "Helvetica-Bold", TEAL)
    for x,w in ((26,358),(399,314),(728,326)):
        d.rect(x, 410, w, 183, PALE, GRAY)
    d.text(40, 439, "Carbonate chemistry", 19, "Helvetica-Bold")
    d.code(40, 465, "add_carbonate_system_1(...)", 17)
    d.code(40, 488, "or add_carbonate_system_2(...)", 17)
    d.text(40, 514, "Uses DIC, TA and T/S/P; computes", 17)
    d.text(40, 537, "CO2(aq) and chemical diagnostics.", 17)
    d.code(40, 560, "M.A.CO2aq", 17)
    d.text(40, 582, "pH / saturation: diagnostics, not transfers", 16)
    d.text(413, 439, "Species coupling", 19, "Helvetica-Bold")
    d.code(413, 465, "Species2Species(...)", 17)
    d.text(413, 495, "If a process changes different", 17)
    d.text(413, 518, "species, define the linked fluxes", 17)
    d.text(413, 541, "and stoichiometric balance.", 17)
    d.text(413, 575, "Conversion is not automatic.", 17, "Helvetica-Bold")
    d.text(742, 439, "External forcing", 19, "Helvetica-Bold")
    d.code(742, 465, "Source / Sink + connection", 17)
    d.code(742, 489, "Signal(...)", 17)
    d.text(742, 518, "Crosses the physical boundary;", 17)
    d.text(742, 541, "enters the whole-system budget.", 17)
    d.text(742, 575, "Signal sets the time variation.", 17)
    d.text(26, 622, "M.DIC = species definition; M.A.DIC = that species in A; .c = concentration time series.", 18)
    return d.drawing


def air_sea_code_map():
    d = Diagram(602)
    d.rect(12, 10, 1056, 340, WHITE, GRAY)
    d.text(28, 37, "01: ATMOSPHERE + OCEAN", 20, "Helvetica-Bold")
    d.code(375, 37, "M = new_model(...)", 19)
    d.text(637, 37, "clock, units and chemistry choices", 18)
    d.rect(26, 57, 298, 268)
    d.text(40, 85, "ATMOSPHERE", 20, "Helvetica-Bold")
    d.code(40, 111, "GasReservoir(...)", 18)
    d.text(40, 146, "CO2 state (mole fraction)", 18)
    d.code(40, 172, "M.CO2_At.c", 19)
    d.text(40, 208, "Atmospheric size (mol air)", 18)
    d.code(40, 234, "reservoir_mass=...", 18)
    d.text(40, 270, "Initial CO2", 18)
    d.code(40, 296, "species_ppm=...", 18)
    d.rect(746, 57, 308, 268)
    d.text(760, 85, "OCEAN", 20, "Helvetica-Bold")
    d.code(760, 110, "initialize_reservoirs(...)", 17)
    d.text(760, 142, "DIC and TA states (mol/kg)", 18)
    d.code(760, 166, "M.Ocean.DIC.c", 19)
    d.code(760, 190, "M.Ocean.TA.c", 19)
    d.text(760, 222, "Inputs from box_parameters(...)", 17)
    d.code(760, 246, "'c': initial concentrations", 16)
    d.code(760, 270, "'g': area + volume", 16)
    d.code(760, 294, "'T', 'S', 'P': conditions", 16)
    d.text(351, 85, "GAS EXCHANGE", 20, "Helvetica-Bold")
    d.code(351, 111, "exchange = Species2Species(...)", 18)
    d.code(351, 142, "source=M.CO2_At", 18)
    d.code(351, 166, "sink=M.Ocean.DIC", 18)
    d.code(351, 190, "species=M.CO2", 18)
    d.code(351, 214, "ctype='gasexchange'", 18)
    d.code(351, 238, "piston_velocity=...", 18)
    d.text(352, 260, "Jgas,in(t): atmosphere to ocean", 17)
    d.arrow([(324, 270), (746, 270)])
    d.text(352, 297, "Jgas,out(t): ocean to atmosphere", 17)
    d.arrow([(746, 307), (324, 307)])
    d.text(352, 333, "One connection computes Jin - Jout", 17)
    d.text(26, 377, "Solid = carbon transfer.", 18)
    d.text(26, 402, "Dashed = information, not material.", 18)
    d.rect(366, 421, 688, 134, PALE, GRAY)
    d.text(382, 448, "CARBONATE CHEMISTRY (supplied calculation)", 19, "Helvetica-Bold", TEAL)
    d.code(382, 475, "add_carbonate_system_1([M.Ocean])", 19)
    d.text(382, 501, "Current DIC, TA + T/S/P determine aqueous CO2.", 18)
    d.code(382, 531, "ref_species=M.Ocean.CO2aq", 19)
    d.arrow([(914, 325), (914, 351), (1065, 351), (1065, 489), (1054, 489)], dashed=True)
    d.arrow([(530, 421), (530, 350), (682, 350), (682, 242)], dashed=True)
    d.text(27, 436, "One exchanged species", 19, "Helvetica-Bold")
    d.code(27, 462, "M.CO2", 19)
    d.text(27, 492, "updates the ocean's DIC state.", 18)
    d.text(27, 518, "CO2(aq) informs the flux law.", 18)
    d.text(27, 581, "Helper connect_atmosphere(...) creates the atmosphere + gas connection shown above.", 19)
    return d.drawing


DIAGRAMS = {"box_code_map": box_code_map, "01_air_sea_code_map": air_sea_code_map}


def build_assets():
    renderer = shutil.which("pdftoppm")
    if not renderer:
        raise RuntimeError("Add Poppler's pdftoppm to PATH to build diagram PNGs")
    output = ROOT / "ref/figures"
    output.mkdir(parents=True, exist_ok=True)
    for name, make in DIAGRAMS.items():
        drawing = make()
        renderSVG.drawToFile(drawing, str(output / f"{name}.svg"))
        with TemporaryDirectory(prefix="esbmtk_diagram_") as tmp:
            pdf = Path(tmp) / f"{name}.pdf"
            renderPDF.drawToFile(drawing, str(pdf))
            subprocess.run([renderer, "-singlefile", "-scale-to", "2160", "-png",
                            str(pdf), str(output / name)], check=True)
        print(f"Built {name}.svg and {name}.png")


if __name__ == "__main__":
    build_assets()
