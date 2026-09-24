# Boudreau-like model: paired teaching schematics

Notebook 03 begins with paired DIC/TA amount-flux equations and schematic
reconstruction, followed by reconciliation with Excel and native construction.
Notebook 04 reuses that specification for its forcing choices. See
[TEACHING_GOALS.md](../TEACHING_GOALS.md) for the implemented workload and
[the original proposal](exercise_revision_proposal.md) for the design rationale.

- [Instructor diagram, PNG](figures/03_04_boudreau_instructor.png)
  ([editable vector SVG](figures/03_04_boudreau_instructor.svg))
- [Student worksheet, PNG](figures/03_04_boudreau_student.png)
  ([editable vector SVG](figures/03_04_boudreau_student.svg))
- [Student flux table, XLSX](../outputs/03_04_flux_specification/student.xlsx)
- [Instructor flux table, XLSX](../outputs/03_04_flux_specification/instructor.xlsx)

Panel A shows circulation and directional gas terms. Panel B shows the same
low-latitude and deep boxes, with biological and sediment processes separated
for readability. Repeated boxes are not additional inventories. The grey outline
in B shows only the ocean portion of the active atmosphere/ocean system.
The schematics show topology and short process labels; equations, units and
workbook links live in the companion table rather than a second table inside
the drawing.

The student version now supplies box outlines and the distinct process-module
symbol, without completed arrows, state labels or boundary. Students may annotate
it or sketch on paper. A companion table leaves thirteen flux expressions and
the POC arrow blank; its dissolution dependency function and units are supplied.
Students identify which changing values affect each rate, which rates are fixed,
and the export/dissolution difference that defines net burial.
The same table
appears in notebook Markdown, so Excel editing is optional. This replaces passive
diagram inspection and repeated lookup work; the provisional 15-minute opening
allocation and 55-minute total for 03 require a pilot. Chemistry/dissolution
hints and a J/m tendency rule support the equation task. The existing DIC–TA
contour exercise follows it; fuller scientific caveats are expandable notes.

## Scientific and implementation conventions

- Every water arrow carries both DIC and TA at the source concentration. The
  three Q_LH/Q_HD/Q_DL arrows form L_b -> H_b -> D_b -> L_b. The two Q_mix arrows are equal
  opposing high-latitude/deep exchanges. The drawing reads their numerical
  volume rates from the workbook. Q_ij is water volume transport [m3/yr];
  J_ij^X(t) = rho_i Q_ij X_i(t) is the tracer amount flux. As notebook 03 explains,
  the reproduced ESBMTK benchmark instead uses its historical numerical
  litres/yr transport coefficient with mol/kg states. The figure does not
  correct or recalibrate that implementation. Conversion to Tmol/yr requires
  division by 10^12. Reservoir inventories use ESBMTK water densities.
- Each G pair shows two conceptual carbon transfers evaluated by one native
  net gas-exchange connection. The gas species is CO2; ocean DIC is updated.
  TA is unchanged. Gas exchange depends on the current atmosphere and local
  aqueous CO2 under the box-specific thermodynamic conditions.
- POC is the benchmark's fixed, DIC-only export/remineralization closure.
  Its lack of a TA effect is a model assumption. No high-latitude POC or PIC
  export is represented.
- Biological TA effects require nutrient/redox bookkeeping in a more complete
  model. Fixed export differs from 02's concentration-scaled k DIC_s(t), even though
  k is constant. Dissolution and gas exchange still respond to evolving states.
- Weathering adds 1 mole of DIC and 2 equivalents of TA in this model.
  Real riverine input need not have exactly this 1:2 ratio.
- PIC leaves low-latitude dissolved inventories as 1 mol DIC and 2 mol TA
  equivalents per mole of CaCO3. The nominal deep sink of the PIC connections
  is bypassed. Only calculated dissolution returns to deep dissolved states.
  The module contains a snowline state, not an explicit sediment-carbon stock.
- B = PIC - D is a signed diagnostic residual, not an additional deep-water
  drain to apply after export and dissolution. Its downward arrow indicates
  positive net burial. B can be negative when previously deposited carbonate
  dissolves. Thus the net effect of PIC and D on the active system is -B for
  carbon and -2B for TA. Adding a separate B sink would double-count the loss.
  The workbook's Fb boundary node does not imply such a separate active drain.
- The notebook's budget is for the unforced baseline. In 04, atmospheric carbon
  forcing and surface-TA forcing add their respective external budget terms.
- Workbook initial concentrations are distinct from the archived stationary
  restart. A changed baseline requires a new stationary control; these diagrams
  are not evidence that a modified baseline is stationary.

## Workbook and literature cross-reference

Numerical labels are read from named tables in
[`model_definition.xlsx`](../data/Boudreau_2010/model_definition.xlsx).
The cross-reference retains the actual table/parameter and native-object names.
POC, PIC and weathering topology and the sediment equations remain specialized
Python construction; the workbook does not yet contain a general process-arrow
table. Dissolution and burial are calculated responses, not editable flux inputs.
The builder checks the expected transport and gas topology before rendering.

The separate `FluxSpecification`/`WorkbookLinks` teaching worksheets document
these properties without changing the production schema. `teaching_specification.py`
owns process metadata; endpoint-qualified workbook IDs avoid ambiguity between
the three `thc` records. No numerical baseline inputs are copied as new settings.
Student worksheets have amber answer spaces, no hidden answer tab or formulas.
The instructor reference is not embedded in the generated student notebook.

| Teaching label | ESBMTK paper figure alias | Meaning |
| --- | --- | --- |
| W | F1 | Carbonate weathering |
| B | F2 | Net carbonate burial |
| Q_LH, Q_HD, Q_DL | F3 | Three separate circulation legs |
| Q_mix,down, Q_mix,up | F4 | Two directed mixing transfers |
| POC | F5 | Organic export and remineralization |
| PIC | F6 | Carbonate export |
| G_L, G_H | F7, F8 respectively | Surface gas exchange |
| D | Explicitly separated here | Carbonate dissolution |

Source: [Wortmann et al. (2025), section 3 and Figure 3](https://gmd.copernicus.org/articles/18/1155/2025/#section3),
implementing the Boudreau et al. (2010) model. These are new teaching drawings of
the repository's Boudreau-like implementation, not reproductions of the original
paper artwork. Descriptive labels avoid relying on the paper's inconsistent POC
F3 reference. The workbook/code use PIC/POC = 0.3; weathering supplies inorganic
carbon. Neither the inverted ratio nor the organic-carbon wording in the
ESBMTK paper's prose is carried into the diagrams.

## Regeneration

Run `python scripts/build_boudreau_diagrams.py` in an authoring environment with
ReportLab, openpyxl and Poppler's `pdftoppm` on PATH. This builds both SVGs and
PNGs from one source, without changing the workbook, notebooks or model. The
student drawing is constructed without instructor-only strings, rather than
covering answers with opaque shapes. Rendering is deterministic for fixed inputs
and tool versions apart from renderer metadata.

For the separate XLSX files, run `scripts/export_flux_specification.py` with a
temporary JSON output path, then `scripts/build_flux_worksheets.mjs` with that
JSON path, `outputs/03_04_flux_specification` and a temporary preview directory.
The JS builder requires the authoring-only `@oai/artifact-tool` package; it is not
a student dependency. It generates both roles from shared metadata, clears only
student answer cells, checks exports and renders both sheets. After metadata
changes, also align the notebook's exercise table and regenerate student copies.
