"""Render the shared Markdown reference as a two-page A4 handout.

Run with a Python environment containing reportlab and pypdf. The course
ESBMTK environment does not need these optional authoring dependencies.
The Markdown owns the prose; build_coding_diagrams.py owns diagram geometry and
labels. Poppler's pdftoppm must be on PATH for PNG export. The same vector drawing
is embedded in the PDF; <!-- PAGEBREAK --> sets the page boundary.
"""

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Preformatted, Table, TableStyle, PageBreak,
)
from pypdf import PdfReader
from build_coding_diagrams import DIAGRAMS, build_assets


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ref/modelling_cheatsheet.md"
OUTPUT = ROOT / "output/pdf/modelling_cheatsheet.pdf"
INK = colors.HexColor("#183747")
TEAL = colors.HexColor("#007F83")
WIDTH = A4[0] - 76


def inline(text):
    """Format the small, deliberately supported Markdown subset."""
    # ASCII arrows avoid dependence on an unembedded Symbol font in PDF viewers.
    text = escape(text).replace("→", "-&gt;")
    text = re.sub(r"`([^`]+)`", r'<font name="Courier" size="8">\1</font>', text)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)


def main():
    build_assets()
    styles = {
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.2,
                               leading=12, spaceAfter=5, textColor=INK),
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=20,
                             leading=23, spaceAfter=7, textColor=INK),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.2,
                             leading=14, spaceBefore=7, spaceAfter=5,
                             keepWithNext=True, textColor=TEAL),
        "table": ParagraphStyle("table", fontName="Helvetica", fontSize=8.6,
                                leading=10.8, textColor=INK),
        "code": ParagraphStyle("code", fontName="Courier", fontSize=8,
                               leading=10, spaceBefore=3, spaceAfter=6,
                               backColor=colors.HexColor("#F0F5F7"),
                               borderPadding=6, alignment=TA_LEFT),
    }
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line == "<!-- PAGEBREAK -->":
            story.append(PageBreak())
        elif line.startswith("!["):
            match = re.fullmatch(r"!\[.*\]\(([^)]+)\)", line)
            if not match:
                raise ValueError(f"Unsupported image syntax: {line}")
            name = Path(match.group(1)).stem
            drawing = DIAGRAMS[name]()
            scale = WIDTH / drawing.width
            drawing.scale(scale, scale)
            drawing.width *= scale
            drawing.height *= scale
            story.append(drawing)
        elif line.startswith("```"):
            block = []
            i += 1
            while not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            story.append(Preformatted("\n".join(block), styles["code"]))
        elif line.startswith("| "):
            rows = []
            while i < len(lines) and lines[i].startswith("| "):
                if not re.fullmatch(r"[| :\-]+", lines[i]):
                    cells = lines[i].strip("| ").split(" | ")
                    rows.append([Paragraph(inline(cell), styles["table"])
                                 for cell in cells])
                i += 1
            table = Table(rows, colWidths=[WIDTH * .365, WIDTH * .635],
                          hAlign="LEFT", repeatRows=1)
            table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEEF0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                 [colors.white, colors.HexColor("#F5F8FA")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(table)
            continue
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), styles["h2"]))
        elif line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["h1"]))
        else:
            story.append(Paragraph(inline(line), styles["body"]))
        i += 1

    def footer(canvas, document):
        canvas.setStrokeColor(TEAL)
        canvas.line(38, 30, A4[0] - 38, 30)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(INK)
        canvas.drawString(38, 18, "ESBMTK practicals | Reference, not an extra assignment")
        canvas.drawRightString(A4[0] - 38, 18, f"{document.page} / 2")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=38, leftMargin=38,
        topMargin=32, bottomMargin=40,
        title="From conceptual model to code | ESBMTK practicals",
        author="ESBMTK practicals",
    )
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    count = len(PdfReader(OUTPUT).pages)
    if count != 2:
        raise RuntimeError(f"Expected two pages, got {count}; revise layout before distributing")
    print(f"Built {OUTPUT.relative_to(ROOT)} ({count} pages)")


if __name__ == "__main__":
    main()
