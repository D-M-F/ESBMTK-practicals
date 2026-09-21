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


def notice(title, text):
    box = Table([[p(f"<b>{title}</b><br/>{text}", "small")]], colWidths=[WIDTH])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF5DE")),
        ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor("#D99B25")),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return KeepTogether([box, Spacer(1, 8)])


def title(route, subtitle):
    return [p("ESBMTK PRACTICALS  /  STUDENT SETUP", "small"), p(route, "title"), p(subtitle, "sub")]


CHECK = '''import sys
import numpy as np
import esbmtk
import PyCO2SYS

print(sys.executable)
np.testing.assert_allclose(np.linalg.solve(np.eye(2), np.ones(2)), [1, 1])
print("Setup check passed")'''


def check_section(expected):
    return [
        p("Run a quick check", "head"),
        p("In JupyterLab, create a new Python notebook with the course kernel. "
          "Paste this into a cell and press <b>Shift+Enter</b>:"),
        code(CHECK),
        p(f"Expect <b>Setup check passed</b>. The printed Python path should contain "
          f"<b>{expected}</b>. This checks imports and a real numerical calculation; "
          "it does not complete any course exercise."),
    ]


def uv():
    story = title("Set up with uv", "For students without Python or Anaconda. Windows, macOS and Linux.")
    story += [
        notice("Before you start - pilot edition", "Use the instructor-issued course folder containing "
               "<b>pyproject.toml</b>, <b>.python-version</b> and <b>uv.lock</b>. "
               "If any are missing, obtain the complete folder before continuing. "
               "The uv files and lockfile are not yet included in the current repository."),
        p("You need an internet connection for the first setup. uv downloads Python and "
          "the required packages; your existing R installation can stay as it is. "
          "Use this route or the Anaconda route for the course."),
        p("1  Install uv once", "head"),
        p("<b>Windows:</b> open PowerShell and run:"),
        code("winget install --id=astral-sh.uv -e"),
        p("<b>macOS / Linux:</b> open Terminal and run:"),
        code("curl -LsSf https://astral.sh/uv/install.sh | sh"),
        p('Close and reopen the terminal, then run <b>uv --version</b>. If WinGet is unavailable, '
          'use the Windows installer at <link href="https://docs.astral.sh/uv/getting-started/installation/" color="#087F8C">'
          'docs.astral.sh/uv/getting-started/installation/</link>.', "small"),
        p("2  Open the course folder", "head"),
        p("Extract the downloaded course archive first. In your terminal, enter the folder "
          "containing pyproject.toml. Replace the example path with your own:"),
        code('cd "path/to/ESBMTK-practicals"'),
        p("Type commands into the terminal, not into RStudio or a notebook cell. "
          "Run one line at a time; wait until the prompt returns.", "small"),
        p("3  Create the course environment", "head"),
        code("uv sync --locked"),
        p("Wait for the installation to finish. uv creates a <b>.venv</b> folder and uses "
          "the package versions selected by your instructor. Keep this folder inside the course folder."),
        PageBreak(),
    ]
    story += title("Open your notebooks", "uv route / finish setup, check it, and return next time")
    story += [
        p("4  Register the kernel and launch JupyterLab", "head"),
        p("From the same course folder, run these two commands. Kernel registration is a one-time step:"),
        code("uv run --locked python -m ipykernel install --sys-prefix --name esbmtk-practicals\n"
             "uv run --locked jupyter lab"),
        p("JupyterLab opens in your browser. Open <b>notebooks/student/</b>. "
          "Select <b>esbmtk-practicals</b> in the kernel selector, including if the notebook "
          "asks for the instructor's ESBMTK314 kernel. A kernel is the Python process running your cells."),
    ]
    story += check_section(".venv")
    story += [
        p("Restart JupyterLab after shutting it down", "head"),
        p("Only when JupyterLab is no longer running (for example, after restarting your laptop), "
          "open a terminal in the course folder and run:"),
        code("uv run --locked jupyter lab"),
        p("If JupyterLab is already running, open existing notebooks in its file browser or "
          "create one via <b>File &gt; New &gt; Notebook</b>, then select the course kernel. "
          "<b>No terminal command is needed for each notebook.</b> Closing a browser tab "
          "usually leaves JupyterLab running. Save your work before shutting it down."),
        p("If something does not work", "head"),
        p("<b>uv not found:</b> reopen the terminal after installation.<br/>"
          "<b>Missing or outdated lockfile:</b> ask for the complete course folder; keep --locked.<br/>"
          "<b>Wrong Python path or missing module:</b> choose esbmtk-practicals and restart that kernel.<br/>"
          "<b>Exercise / NotImplementedError:</b> a marked student placeholder is expected; follow the exercise."),
        p('Help: <link href="https://docs.astral.sh/uv/guides/integration/jupyter/" color="#087F8C">'
          'docs.astral.sh/uv/guides/integration/jupyter/</link>. For other errors, send your instructor '
          'the complete error message and your operating system.', "small"),
    ]
    return story


def anaconda():
    story = title("Set up with Anaconda", "For students who already use Anaconda or Miniconda.")
    story += [
        notice("Before you start - pilot edition", "You need the full course folder, including "
               "<b>environment-anaconda.yml</b>, and internet for the first setup. "
               "Package resolution has been checked on Windows/Python 3.14; "
               "fresh-installation and macOS pilots remain to be completed."),
        p("This route creates a separate <b>esbmtk-practicals</b> environment. "
          "You do not need uv or a separate Python installer, and your existing R setup stays unchanged."),
        p("1  Open the course folder in a terminal", "head"),
        p("Extract the downloaded course archive. On Windows, open <b>Anaconda Prompt</b> "
          "from the Start menu. On macOS/Linux, use a terminal where conda works. "
          "Replace the example path with the folder containing environment-anaconda.yml."),
        p("<b>Windows Anaconda Prompt:</b> /d also changes the drive."),
        code('cd /d "D:\\path\\to\\ESBMTK-practicals"'),
        p("<b>macOS / Linux:</b>"),
        code('cd "path/to/ESBMTK-practicals"'),
        p("2  Create and activate the environment", "head"),
        p("Run one line at a time and wait for each command to finish:"),
        code("conda env create -f environment-anaconda.yml\n"
             "conda activate esbmtk-practicals\n"
             "python -m pip check"),
        p("The terminal prompt should show <b>(esbmtk-practicals)</b>. The last command "
          "should report <b>No broken requirements found</b>. If this environment already exists, "
          "activate and check it instead of creating it again."),
        p("3  Register the kernel and launch JupyterLab", "head"),
        code("python -m ipykernel install --sys-prefix --name esbmtk-practicals\n"
             "python -m jupyterlab"),
        p("Kernel registration is needed only once. It adds the course kernel inside this "
          "environment. JupyterLab then opens in your browser; keep the terminal open."),
        PageBreak(),
    ]
    story += title("Open your notebooks", "Anaconda route / select the kernel, check it, and return next time")
    story += [
        p("4  Select the course kernel", "head"),
        p("Open <b>notebooks/student/</b> in JupyterLab. Select <b>esbmtk-practicals</b> "
          "in the kernel selector. If the notebook asks for the instructor's ESBMTK314 "
          "kernel, choose your course kernel instead. If you previously followed the longer "
          "Markdown guide, the same kernel may be labelled <b>ESBMTK practicals</b>."),
    ]
    story += check_section("esbmtk-practicals")
    story += [
        p("Restart JupyterLab after shutting it down", "head"),
        p("Only when JupyterLab is no longer running (for example, after restarting your laptop), "
          "open Anaconda Prompt or your Conda-enabled terminal, enter the course folder and run:"),
        code("conda activate esbmtk-practicals\npython -m jupyterlab"),
        p("If JupyterLab is already running, open existing notebooks in its file browser or "
          "create one via <b>File &gt; New &gt; Notebook</b>, then select the course kernel. "
          "<b>No terminal command is needed for each notebook.</b> Closing a browser tab "
          "usually leaves JupyterLab running. Save your work before shutting it down."),
        p("If something does not work", "head"),
        p("<b>conda not found:</b> on Windows, use Anaconda Prompt.<br/>"
          "<b>YAML file not found:</b> enter the extracted folder containing environment-anaconda.yml.<br/>"
          "<b>Missing module / wrong Python path:</b> activate the environment, launch Jupyter there, "
          "and select the course kernel.<br/>"
          "<b>Windows Python crash:</b> launch from the activated prompt; send your instructor "
          "the error if it persists. Do not reinstall packages at random.<br/>"
          "<b>Exercise / NotImplementedError:</b> a marked student placeholder is expected."),
        p('Conda help: <link href="https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html" '
          'color="#087F8C">Managing environments</link>. For other errors, send the complete error message '
          'and your operating system to your instructor.', "small"),
    ]
    return story


def build(name, route, story):
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
        canvas.drawString(44, 25, f"ESBMTK practicals | {route} | Pilot edition - 21 September 2026")
        canvas.drawRightString(A4[0] - 44, 25, f"{document.page} / 2")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    print(OUT / name)


if __name__ == "__main__":
    build("student_setup_uv.pdf", "uv", uv())
    build("student_setup_anaconda.pdf", "Anaconda", anaconda())
