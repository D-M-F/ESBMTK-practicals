# Instructor review PDFs

Distribute `output/ESBMTK-instructor-review-00-04.zip` to lecturers who do not
have Jupyter. Extract the ZIP and open `START_HERE.txt`; the five PDFs are in
00–04 order. PDF reading needs no Python installation. The companion carbonate
explorer is an offline HTML file that opens in a normal browser.

The exports preserve all source cells, instructor answers, code and freshly
executed outputs. Every `<details>` disclosure is expanded. The export also
calls 04's supplied optional `show_input_reference()` and appends the linked
sediment reference to 03. Three static explorer views accompany the interactive
HTML. Directly linked local references are included, and PDF links are rewritten
to portable relative file destinations. External web links still need internet.
Some PDF viewers block local file navigation; open those files from the extracted
folder instead.

Only core 00–04 are executed. The dormant 04 extension, separate 05 and archive
are excluded. Source notebooks, student copies, scientific choices and teaching
time allocations are not changed by export. The files contain instructor answers.

## Rebuild

The numerical stage needs the activated ESBMTK314 environment and its registered
`esbmtk314` kernel, including nbclient, nbconvert and BeautifulSoup. The print
stage uses Node.js, Playwright and a Chromium-compatible browser. Packaging uses
Python with pypdf. Poppler and Pillow support visual QA.

From the repository root:

```powershell
conda run -n ESBMTK314 --no-capture-output python scripts/build_instructor_review.py
```

Download the pinned MathJax 3.2.2 `es5/tex-svg.js` bundle from
`https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js` into
`tmp/pdfs/instructor_review/mathjax/tex-svg.js`. It is used only to typeset the
PDFs; neither Jupyter nor MathJax is needed on the recipient's laptop.

With Playwright available to Node (or `NODE_PATH` pointing at the provided
package directory), select an installed Chromium browser if necessary:

```powershell
$env:BROWSER_EXECUTABLE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
node scripts/render_instructor_review.cjs
python scripts/package_instructor_review.py
```

The package stage asserts unchanged source hashes, no cell errors, complete
printed stream outputs and clean browser rendering checks. It adds metadata,
portable links and `execution_manifest.json`, then validates the ZIP. Source
hashes, package versions, page counts and final PDF hashes are recorded.

For layout-only iterations, use `--reuse-execution` on the first command.
This verifies source hashes before reusing executed copies; a source change
requires a fresh execution. Temporary executed notebooks and HTML live in
`tmp/pdfs/instructor_review/`; final artifacts live in
`output/pdf/instructor_review/`. Render the final PDFs with Poppler and inspect
all pages before distribution, especially diagrams, formulas, tables, optional
sections and question/answer panels.
