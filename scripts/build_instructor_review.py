"""Execute core instructor notebooks and prepare HTML for the PDF review pack.

Run with conda run -n ESBMTK314 --no-capture-output python ...
Sources are never rewritten. Use --reuse-execution for print-layout iterations.
The companion render_instructor_review.cjs prints the prepared HTML.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import mimetypes
import os
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import unquote, quote

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tmp/pdfs/instructor_review"
OUT = ROOT / "output/pdf/instructor_review"
SOURCES = sorted((ROOT / "notebooks/instructor").glob("0[0-4]_*.ipynb"))

CSS = r"""
@page { size: A4; margin: 15mm 13mm 17mm; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: white; color: #202b38; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10pt; line-height: 1.42; }
#notebook, #notebook-container, main { padding: 0 !important; margin: 0 !important; width: 100% !important; box-shadow: none !important; }
.cell, .inner_cell, .input, .output_wrapper, .output, .output_area, .text_cell_render, .input_area { display: block !important; width: 100% !important; height: auto !important; max-height: none !important; overflow: visible !important; }
.cell { margin: 0 0 12px; padding: 0; }
.prompt, .anchor-link { display: none !important; }
h1 { font-size: 22pt; line-height: 1.16; color: #143850; margin: 12px 0 18px; }
h2 { font-size: 15pt; line-height: 1.25; margin: 24px 0 10px; color: #143850; }
h3 { font-size: 12pt; margin: 19px 0 8px; color: #143850; }
h4 { font-size: 10.5pt; margin: 15px 0 7px; }
h1,h2,h3,h4,summary { break-after: avoid; }
p { margin: 8px 0; }
ul,ol { padding-left: 22px; }
li { margin: 4px 0; }
a { color: #205b86; text-decoration: underline; overflow-wrap: anywhere; }
pre, code { font-family: Consolas, 'Courier New', monospace; font-size: 8pt; }
pre { white-space: pre-wrap !important; overflow-wrap: anywhere; word-break: normal; line-height: 1.36; margin: 0; tab-size: 4; }
.input_area { background: #f3f5f7; border: 1px solid #d8dfe5; border-left: 3px solid #899ba8; border-radius: 3px; padding: 9px 11px; }
.output_area { padding: 4px 0; }
.output_stderr { background: #fff4e4; }
.output_text pre, .output_stream pre { font-size: 7.6pt; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 8pt; line-height: 1.35; }
th,td { border: 1px solid #ccd6df; padding: 6px; text-align: left; vertical-align: top; overflow-wrap: anywhere; }
th { background: #edf2f6; font-weight: 600; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
img { display: block; max-width: 100% !important; height: auto !important; max-height: 230mm; object-fit: contain; margin: 10px auto; break-inside: avoid; }
.output_png, .output_svg, .output_jpeg { break-inside: avoid; }
details { display: block; border: 1px solid #cbd7e1; padding: 10px 12px; margin: 12px 0; }
summary { font-weight: 650; color: #34516b; margin-bottom: 8px; }
details > * { content-visibility: visible !important; }
mark { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
div[style*='background-color'] { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
.export-note { background: #edf2f6; border-top: 3px solid #2c617e; padding: 12px 14px; margin-bottom: 18px; font-size: 9pt; }
.export-note p { margin: 4px 0; }
.appendix { break-before: page; }
.math { overflow: visible !important; }
mjx-container { max-width: 100%; }
mjx-container[display='true'] { margin: 12px 0 !important; break-inside: avoid; }
"""


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reuse-execution", action="store_true")
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    os.environ["IPYTHONDIR"] = str(WORK / "ipython")
    os.environ["JUPYTER_RUNTIME_DIR"] = str(WORK / "runtime")
    manifest_path = WORK / "execution.json"
    manifest = json.loads(manifest_path.read_text()) if args.reuse_execution else {
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "environment": "ESBMTK314",
        "python": sys.version,
        "packages": {p: importlib.metadata.version(p) for p in
                     ("esbmtk", "PyCO2SYS", "numpy", "scipy", "nbclient", "nbconvert")},
        "notebooks": [],
    }
    for path in SOURCES:
        sha = digest(path)
        executed = WORK / path.name
        if args.reuse_execution and any(r["source"] == path.name for r in manifest["notebooks"]):
            record = next(r for r in manifest["notebooks"] if r["source"] == path.name)
            assert record["sha256"] == sha, f"Source changed since execution: {path}"
            nb = nbformat.read(executed, 4)
        else:
            nb = nbformat.read(path, 4)
            nbformat.validate(nb)
            # Full tables and static plots for the print copy only.
            nb.cells.insert(0, nbformat.v4.new_code_cell(
                "# PDF export setup: retain complete table results and static figures.\n"
                "%matplotlib inline\n"
                "import pandas as pd\n"
                "pd.set_option('display.max_rows', None)\n"
                "pd.set_option('display.max_columns', None)\n"
                "pd.set_option('display.max_colwidth', None)\n"
            ))
            if path.name.startswith("04_"):
                i = next(i for i, c in enumerate(nb.cells) if "def show_input_reference():" in c.source)
                nb.cells.insert(i + 1, nbformat.v4.new_code_cell(
                    "# PDF export: execute the optional workbook lookup in full.\nshow_input_reference()"))
            def progress(cell, cell_index, **kwargs):
                if cell.cell_type == "code" and cell.source.strip():
                    print(f"{path.stem}: executing cell {cell_index}", flush=True)
            NotebookClient(nb, timeout=1800, kernel_name="esbmtk314",
                           allow_errors=False, on_cell_start=progress,
                           resources={"metadata": {"path": str(path.parent)}}).execute()
            nb.cells.pop(0)
            nbformat.write(nb, executed)
            errors = [o for c in nb.cells for o in c.get("outputs", []) if o.output_type == "error"]
            assert not errors
            assert digest(path) == sha, "Source notebook was modified"
            manifest["notebooks"].append({
                "source": path.name, "sha256": sha,
                "executed_code_cells": sum(c.cell_type == "code" and c.execution_count is not None for c in nb.cells),
                "outputs": sum(len(c.get("outputs", [])) for c in nb.cells),
                "errors": len(errors),
            })
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
            print(f"PASS {path.name}", flush=True)

        nb = nbformat.reads(nbformat.writes(nb), 4)
        title = nb.cells[0].source.splitlines()[0].lstrip("# ")
        preamble = nbformat.v4.new_markdown_cell(
            '<div class="export-note"><strong>LECTURER REVIEW | INSTRUCTOR EDITION</strong>'
            '<p>Executed in ESBMTK314. All instructor solutions, code, execution outputs and '
            'optional disclosures are included. No Jupyter installation is needed to read this PDF.</p>'
            f'<p>Source: <code>{path.name}</code><br>Execution: {manifest["executed_utc"][:10]}.'
            ' The source notebooks are unchanged.</p></div>')
        nb.cells.insert(1, preamble)
        if path.name.startswith("03_"):
            appendix = (ROOT / "ref/sediment_reference.md").read_text(encoding="utf-8")
            nb.cells.append(nbformat.v4.new_markdown_cell(
                '<div class="appendix" id="sediment-reference"></div>\n\n'
                + appendix.replace("# Optional sediment reference", "# Appendix: optional sediment reference", 1)))
        exporter = HTMLExporter(template_name="basic")
        exporter.exclude_input_prompt = True
        exporter.exclude_output_prompt = True
        body, _ = exporter.from_notebook_node(nb)
        soup = BeautifulSoup(body, "html.parser")
        for details in soup.find_all("details"):
            details["open"] = "open"
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if src and not src.startswith(("data:", "http:", "https:")):
                asset = (path.parent / src).resolve()
                if not asset.is_file():
                    raise FileNotFoundError(asset)
                mime = mimetypes.guess_type(asset.name)[0] or "application/octet-stream"
                img["src"] = f"data:{mime};base64," + base64.b64encode(asset.read_bytes()).decode()
        for frame in soup.find_all("iframe"):
            if frame.has_attr("srcdoc"):
                (OUT / "01_carbonate_explorer.html").write_text(frame["srcdoc"], encoding="utf-8")
                replacement = soup.new_tag("div", attrs={"class": "explorer-print"})
                replacement.append(BeautifulSoup(
                    '<p><strong>Interactive carbonate explorer: static review view.</strong> '
                    'The companion <a href="01_carbonate_explorer.html">01_carbonate_explorer.html</a> '
                    'opens offline in a browser without Jupyter. The PDF shows the default '
                    'surface, contours and slice at the reference TA; use the companion for rotation and sliders.</p>'
                    '<img src="explorer-oblique.png" alt="Carbonate surface at the reference TA">'
                    '<img src="explorer-top.png" alt="Top view and pCO2 contours">'
                    '<img src="explorer-slice.png" alt="Constant-TA cutting plane, tangent and atmosphere line">', "html.parser"))
                frame.replace_with(replacement)
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.endswith("sediment_reference.md") and path.name.startswith("03_"):
                a["href"] = "#sediment-reference"
            elif href.endswith("modelling_cheatsheet.md"):
                a["href"] = "modelling_cheatsheet.pdf"
            elif ".ipynb" in href and any(s.name in href for s in SOURCES):
                target = next(s for s in SOURCES if s.name in href)
                a["href"] = target.stem + ".pdf"
            elif href.startswith("../../"):
                local, _, fragment = href.partition("#")
                reference = (path.parent / unquote(local)).resolve()
                if not reference.is_relative_to(ROOT) or not reference.is_file():
                    raise ValueError(f"Invalid local reference: {href}")
                target = OUT / "references" / reference.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(reference, target)
                a["href"] = quote(target.relative_to(OUT).as_posix()) + ("#" + fragment if fragment else "")
        # nbconvert protects mathematics in spans/divs; MathJax processes those.
        document = ('<!doctype html><html><head><meta charset="utf-8">'
                    f'<title>{title}</title><style>{CSS}</style>'
                    '<script>window.MathJax={tex:{inlineMath:[["$","$"],["\\\\(","\\\\)"]],'
                    'displayMath:[["$$","$$"],["\\\\[","\\\\]"]]},'
                    'svg:{fontCache:"none"},options:{enableMenu:false}};</script>'
                    '<script defer src="mathjax/tex-svg.js"></script></head><body>'
                    + str(soup) + '</body></html>')
        (WORK / f"{path.stem}.html").write_text(document, encoding="utf-8")
        print(f"HTML {path.stem}: {len(soup.find_all('details'))} expanded notes", flush=True)
    shutil.copy2(ROOT / "output/pdf/modelling_cheatsheet.pdf", OUT / "modelling_cheatsheet.pdf")
    print("Execution and HTML preparation complete.", flush=True)


if __name__ == "__main__":
    main()
