"""Build the two student setup handouts; requires ReportLab and Windows fonts."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Table,
    TableStyle, KeepTogether,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf"
FONTS = Path("C:/Windows/Fonts")
for name, filename in (("Body", "calibri.ttf"), ("Bold", "calibrib.ttf"),
                       ("Italic", "calibrii.ttf"), ("Mono", "consola.ttf")):
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Bold", italic="Italic", boldItalic="Bold")
INK = colors.HexColor("#163047")
TEAL = colors.HexColor("#087F8C")
MUTED = colors.HexColor("#516574")
WIDTH = A4[0] - 88
STYLES = {
    "title": ParagraphStyle("title", fontName="Bold", fontSize=27, leading=31, textColor=INK, spaceAfter=8),
    "sub": ParagraphStyle("sub", fontName="Body", fontSize=12, leading=16, textColor=MUTED, spaceAfter=15),
    "head": ParagraphStyle("head", fontName="Bold", fontSize=13, leading=17, textColor=TEAL, spaceBefore=11, spaceAfter=5, keepWithNext=True),
    "body": ParagraphStyle("body", fontName="Body", fontSize=11, leading=14.7, textColor=INK, spaceAfter=7),
    "small": ParagraphStyle("small", fontName="Body", fontSize=9.4, leading=12.2, textColor=MUTED, spaceAfter=6),
    "code": ParagraphStyle("code", fontName="Mono", fontSize=9.3, leading=13, textColor=INK),
}


def p(text, style="body"):
    return Paragraph(text, STYLES[style])


def code(text):
    # Never silently wrap or clip a command: keep each executable line intact.
    for line in text.splitlines():
        assert pdfmetrics.stringWidth(line, "Mono", 9.3) <= WIDTH - 24, line
    box = Table([[Preformatted(text, STYLES["code"])]], colWidths=[WIDTH])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF4F7")),
        ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#D7E2E8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return KeepTogether([box, Spacer(1, 8)])


def markdown_story(relative_path):
    """Render the student portion of a setup guide into PDF flowables."""
    import re

    def inline(text):
        text = escape(text)
        text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
                      r'<link href="\2" color="#087F8C">\1</link>', text)
        text = re.sub(r"`([^`]+)`", r'<font name="Mono" size="10">\1</font>', text)
        text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
        return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)

    source = (ROOT / relative_path).read_text(encoding="utf-8-sig")
    blocks = source.split("<!-- INSTRUCTOR NOTES -->")[0].split("\n\n")
    story = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block == "<!-- PAGEBREAK -->":
            story.append(PageBreak())
        elif block.startswith("# "):
            story.extend([p("ESBMTK PRACTICALS / STUDENT SETUP", "small"),
                          p(inline(block[2:]), "title")])
        elif block.startswith("## "):
            story.append(p(inline(block[3:]), "head"))
        elif block.startswith("```"):
            lines = block.splitlines()
            assert lines[-1] == "```"
            story.append(code("\n".join(lines[1:-1])))
        else:
            story.append(p(inline(block.replace("\n", " "))))
    return story


def uv():
    return markdown_story("ref/uv_setup.md")


def anaconda():
    return markdown_story("ref/anaconda_setup.md")


def build(name, route, story, pages=2, edition="Pilot edition - 21 September 2026"):
    OUT.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUT / name), pagesize=A4, rightMargin=44, leftMargin=44,
                            topMargin=39, bottomMargin=43, title=f"ESBMTK student setup - {route}",
                            author="ESBMTK practicals", pageCompression=1)
    def page(canvas, document):
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(2)
        canvas.line(44, A4[1] - 25, A4[0] - 44, A4[1] - 25)
        canvas.setFont("Body", 8.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(44, 25, f"ESBMTK practicals | {route} | {edition}")
        canvas.drawRightString(A4[0] - 44, 25, f"{document.page} / {pages}")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    print(OUT / name)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=("uv", "anaconda"))
    args = parser.parse_args()
    if args.only != "anaconda":
        count = (ROOT / "ref/uv_setup.md").read_text(encoding="utf-8").count("<!-- PAGEBREAK -->") + 1
        build("student_setup_uv.pdf", "uv", uv(), pages=count,
              edition="Student guide - 22 September 2026")
    if args.only != "uv":
        count = (ROOT / "ref/anaconda_setup.md").read_text(encoding="utf-8-sig").count("<!-- PAGEBREAK -->") + 1
        build("student_setup_anaconda.pdf", "Anaconda", anaconda(), pages=count,
              edition="Pilot edition - 22 September 2026")
