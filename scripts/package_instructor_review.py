"""Validate the rendered core PDFs, make portable links and build the review ZIP.

Requires pypdf. Run after build_instructor_review.py and render_instructor_review.cjs.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
from urllib.parse import unquote, urlsplit
import zipfile

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject, TextStringObject

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/instructor_review"
WORK = ROOT / "tmp/pdfs/instructor_review"


def normalize(text):
    return re.sub(r"\s+", "", text).replace("\u200b", "")


def main():
    manifest = json.loads((WORK / "execution.json").read_text())
    qa = json.loads((WORK / "render-qa.json").read_text())
    assert len(manifest["notebooks"]) == len(qa) == 5
    assert all(not r[k] for r in qa for k in ("errors", "mathErrors", "closed", "brokenImages", "overflow"))
    for record in manifest["notebooks"]:
        source = ROOT / "notebooks/instructor" / record["source"]
        assert hashlib.sha256(source.read_bytes()).hexdigest() == record["sha256"]
        pdf = OUT / (source.stem + ".pdf")
        reader = PdfReader(pdf)
        text = normalize("\n".join(p.extract_text() for p in reader.pages))
        nb = json.loads((WORK / source.name).read_text(encoding="utf-8"))
        missing = []
        streams = 0
        for cell in nb["cells"]:
            for output in cell.get("outputs", []):
                assert output["output_type"] != "error"
                if output["output_type"] == "stream":
                    streams += 1
                    raw = "".join(output["text"])
                    raw = re.sub(r"\x1b\[[0-9;]*m", "", raw)
                    for line in raw.splitlines():
                        if normalize(line) and normalize(line) not in text:
                            missing.append(line)
        assert not missing, (pdf.name, missing)
        writer = PdfWriter()
        writer.clone_document_from_reader(reader)
        portable_links = 0
        for page in writer.pages:
            for ref in page.get("/Annots", []):
                ann = ref.get_object()
                action = ann.get("/A")
                if not action or action.get("/S") != "/URI":
                    continue
                uri = str(action.get("/URI", ""))
                if not uri.startswith("file:"):
                    continue
                parsed = urlsplit(uri)
                decoded = unquote(parsed.path).replace("\\", "/")
                marker = "/tmp/pdfs/instructor_review/"
                assert marker in decoded, uri
                relative = decoded.split(marker, 1)[1]
                target = OUT / relative
                assert target.is_file(), target
                if target.suffix == ".pdf":
                    number = int(parsed.fragment.split("=", 1)[1]) - 1 if parsed.fragment.startswith("page=") else 0
                    ann[NameObject("/A")] = DictionaryObject({
                        NameObject("/S"): NameObject("/GoToR"),
                        NameObject("/F"): TextStringObject(relative),
                        NameObject("/D"): ArrayObject([NumberObject(number), NameObject("/Fit")]),
                    })
                else:
                    action[NameObject("/URI")] = TextStringObject(relative)
                portable_links += 1
        writer.add_metadata({"/Title": source.stem.replace("_", " ") + " - Instructor review",
                             "/Author": "ESBMTK practicals",
                             "/Subject": "Executed instructor notebook; optional notes expanded"})
        staging = WORK / pdf.name
        writer.write(staging)
        shutil.copy2(staging, pdf)
        reopened = PdfReader(pdf)
        assert len(reopened.pages) == len(reader.pages)
        record.update(pdf=pdf.name, pages=len(reader.pages), stream_outputs_checked=streams,
                      portable_links=portable_links, pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest())
        print(f"PASS {pdf.name}: {record['pages']} pages, {streams} full stream outputs, {portable_links} portable links")

    # Convenient copies of diagrams and the completed flux worksheet referenced
    # by the supplied diagram guide (neither worksheet is a live model input).
    for relative in ("ref/figures/03_04_boudreau_instructor.png", "ref/figures/03_04_boudreau_student.png",
                     "ref/figures/03_04_boudreau_instructor.svg", "ref/figures/03_04_boudreau_student.svg",
                     "outputs/03_04_flux_specification/instructor.xlsx"):
        target = OUT / "references" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    manifest["render_checks"] = qa
    (OUT / "execution_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    lines = ["ESBMTK PRACTICALS - LECTURER REVIEW PACK", "Prepared 24 September 2026", "",
             "Extract the ZIP first. Open the PDFs in order 00, 01, 02, 03, 04.",
             "No Python, Jupyter, Conda or package installation is needed.", ""]
    lines += [f"{r['pdf']} ({r['pages']} pages)" for r in manifest["notebooks"]]
    lines += ["", "WHAT IS INCLUDED", "",
              "Complete instructor text and solutions, all code, fresh execution outputs,",
              "figures and tables. All eight expandable notes are open. Notebook 04's",
              "optional workbook lookup has also been executed. Notebook 03 includes",
              "the linked optional sediment reference as an appendix.", "",
              "Notebook 01 includes static views of the interactive carbonate explorer.",
              "Open 01_carbonate_explorer.html in a browser to rotate the surface or",
              "change sliders. It works offline without Jupyter.", "",
              "modelling_cheatsheet.pdf is the existing two-page coding reference.",
              "references/ contains directly cited local lecture/reference PDFs, diagrams,",
              "flux worksheets and source/reference text. Markdown and Python files are",
              "plain text and can be opened in any text editor; they need not be run.",
              "External web references still require internet. Some PDF viewers restrict",
              "local-file links; the same files can be opened directly from the folder.", "",
              "SCOPE AND EXECUTION", "",
              "These are snapshots of the current core instructor notebooks 00-04.",
              "The dormant attribution/feedback extension and separate 05 are excluded.",
              "Sources, teaching tasks and timetable are unchanged. These files contain",
              "instructor answers and are intended for lecturer review.", "",
              "Executed in the activated ESBMTK314 environment, Python " + manifest["python"].split()[0] + ".",
              "All five notebooks completed without cell errors; their embedded graph,",
              "inventory, forcing, restart and conservation checks passed. Passing these",
              "checks has the scientific limits explained in the notebooks.",
              "execution_manifest.json records package versions, source SHA-256 values,",
              "page counts and PDF SHA-256 values.", ""]
    (OUT / "START_HERE.txt").write_text("\n".join(lines), encoding="utf-8")
    archive = ROOT / "output/ESBMTK-instructor-review-00-04.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(OUT.rglob("*")):
            if path.is_file():
                z.write(path, "ESBMTK-instructor-review/" + path.relative_to(OUT).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len([n for n in z.namelist() if re.search(r"/0[0-4]_[^/]+\.pdf$", n)]) == 5
    print(f"Created {archive} ({archive.stat().st_size / 1024**2:.1f} MiB)")


if __name__ == "__main__":
    main()
