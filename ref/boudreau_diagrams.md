# Boudreau-like model: paired teaching schematics

These standalone drafts support review of the proposed 03/04 diagram exercise.
They have not yet replaced notebook material or changed the required workload.

- [Instructor diagram, PNG](figures/03_04_boudreau_instructor.png)
  ([editable vector SVG](figures/03_04_boudreau_instructor.svg))
- [Student worksheet, PNG](figures/03_04_boudreau_student.png)
  ([editable vector SVG](figures/03_04_boudreau_student.svg))

Panel A shows circulation and directional gas terms. Panel B shows the same
low-latitude and deep boxes, with biological and sediment processes separated
for readability. Repeated boxes are not additional inventories. The grey outline
in B shows only the ocean portion of the active atmosphere/ocean system.

The student version omits three arrowheads (T_LH, POC and D), two process names
(D and B), and six transfer-property cells. Reservoir identities, weathering,
process-module wiring and workbook/code references are supplied. It is an
annotation exercise; students need not reproduce the artwork. The proposed use
is to replace part of 03's existing diagram inspection, with the completed
reference reused in 04. No change to the provisional timetable is established
by producing these drafts.

## Scientific and implementation conventions

- Every water arrow carries both DIC and TA at the source concentration. The
  three T arrows form L_b -> H_b -> D_b -> L_b. The two M arrows are equal
  opposing high-latitude/deep exchanges. The drawing reads their numerical
  volume rates from the workbook. In the physical law, q = rho Q has units
  kg/yr and J_X(t) = q X_source(t) has units mol/yr. As notebook 03 explains,
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
- The instructor budget is for the unforced baseline. In 04, atmospheric carbon
  forcing and surface-TA forcing add their respective external budget terms.
  Optional state-dependent pump feedbacks are not represented here.
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

| Teaching label | ESBMTK paper figure alias | Meaning |
| --- | --- | --- |
| W | F1 | Carbonate weathering |
| B | F2 | Net carbonate burial |
| T_LH, T_HD, T_DL | F3 | Three separate circulation legs |
| M_down, M_up | F4 | Two directed mixing transfers |
| POC | F5 | Organic export and remineralization |
| PIC | F6 | Carbonate export |
| G_L, G_H | F7/F8 pair | Surface gas exchange |
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
