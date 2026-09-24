from pathlib import Path
import hashlib
import json
import sys
import nbformat

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from teaching_specification import flux_table_markdown
from scripts.build_student_notebooks import build_student_notebook

OUT = Path(__file__).parent
source = ROOT / 'notebooks/instructor/03_boudreau_three_box_model.ipynb'
nb = nbformat.read(OUT / 'before.ipynb', 4)
if not (OUT / 'protected.json').exists():
    files = [p for folder in ('notebooks', 'archive', 'data') for p in (ROOT/folder).rglob('*')
             if p.is_file() and not p.name.startswith('~$') and p.suffix != '.log'
             and '.ipynb_checkpoints' not in p.parts and '__pycache__' not in p.parts]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (OUT / 'protected.json').write_text(json.dumps(hashes, indent=2))

BLUE = '<div style="background-color: #edf5ff; color: #173b61; border-left: 4px solid #3977b8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">'
PURPLE = '<div style="background-color: #f3eefb; color: #38224f; border-left: 4px solid #7952a8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">'
def question(text):
    return BLUE + '\n\n' + text.strip() + '\n\n</div>'
def answer(text):
    return '<!-- BEGIN SOLUTION -->\n' + PURPLE + '\n\n**Instructor answer**\n\n' + text.strip() + '\n\n</div>\n<!-- END SOLUTION -->'

nb.cells[0].source = nb.cells[0].source.replace('Diagram and Excel reconciliation (15)', 'Diagram, paired flux equations and Excel reconciliation (15)').replace('for the process arrows in place of repeated inventory-effect answers', 'for interpreting the paired fluxes on the contour plot').replace('flux table are the specification', 'paired flux equations are the specification')
nb.cells[2].source = r'''### Process rules for your equations

- Water carries both dissolved tracers at the **source concentration**. Draw the circulation loop L_b → H_b → D_b → L_b and both H_b ↔ D_b mixing directions.
- Each surface exchanges CO2 with the same finite atm. Use invasion and outgassing as in 01/02.
- Only L_b exports POC/PIC. The table supplies the benchmark's biological, carbonate and weathering assumptions beside their rows.
- Draw a distinct carbonate/sediment **process module** with an explicit dissolution return. Its snowline is a memory state; it has no explicit sediment-carbon inventory. Detailed sediment equations remain [optional](../../ref/sediment_reference.md).
'''

nb.cells[6].source = r'''## A3. Exercise 03.1: write the paired fluxes and label the diagram

![Box outlines for reconstruction](../../ref/figures/03_04_boudreau_student.png)

Use <mark style="background-color: #fff0b3; color: #513d00; padding: 0.05em 0.2em; border-radius: 3px;"><strong>amount fluxes</strong></mark> $J_a^{DIC}(t)$ [mol C/yr] and $J_a^{TA}(t)$ [equivalents/yr] for process $a$.
Positive follows the arrow: subtract at its source and add at its destination.
The DIC superscript tracks carbon removed from/returned to dissolved inventories, even when carried as CO2 or particles. Gas exchange and net burial can be negative.

| Symbol | Meaning / units |
| --- | --- |
| $DIC_i(t),TA_i(t)$ | Evolving box concentrations [mol C/kg, eq/kg]; $i=L_b,H_b,D_b$ |
| $Q_{ij},q_{ij}$ | Water volume transport [m³/yr] and physical mass transport $q_{ij}=\rho_iQ_{ij}$ [kg/yr] |
| $\rho_i,m_i$ | ESBMTK density $\rho(T_i,S_i,p_i)$ [kg/m³] and fixed box water mass $m_i=\rho_iV_i$ [kg] |
| $P_0,r,W_0$ | Prescribed POC carbon export [mol C/yr], PIC/POC rain ratio [dimensionless], weathering carbon input [mol C/yr] |
| $E(t),D(t),B_{net}(t)$ | Carbonate export, dissolution and signed net burial [mol C/yr] |

Here $p_i$ is water pressure; $pCO_{2,atm}$ below is atmospheric CO2 partial pressure.
F1–F8 are paper aliases, not new variables: use the descriptive process IDs below.
**Benchmark convention:** the physical $\rho Q$ relation is for dimensional reasoning. The existing benchmark uses a nominal litres/yr coefficient with mol/kg states; retain that implementation in 03.3. Correcting it would require a new baseline/restart.

### Supplied hints for chemistry and sediment response

For gas exchange, use area $A_i$ [m²], velocity $v_i$ [m/yr] and

$$c_i(t)=\mathcal C(DIC_i(t),TA_i(t);T_i,S_i,p_i),\qquad c_{eq,i}(t)=K_{0,i}pCO_{2,atm}(t).$$

Both $c_i$ (aqueous CO2) and $c_{eq,i}$ have units mol/m³; $K_{0,i}$ is the local solubility in compatible pressure units. Supplied chemistry handles conversions from mol/kg and dry-air CO2 fraction. Form the two directional transfers before taking their difference.

For dissolution, **use this supplied dependency function**, not the sediment equations:

$$D(t)=\mathcal D\!\left(E(t),DIC_d(t),TA_d(t),z_{snow}(t);T_d,S_d,p_d,\alpha,z_0\right).$$

Here $d$ means D_b; $z_{snow}$ records sediment history. The workbook's $\alpha,z_0$ are sediment parameters. This is a schematic dependency relation, not an ESBMTK call. `add_carbonate_system_2` supplies its implementation. For burial, compare rain with dissolution, allowing old sediment to dissolve; the residual is **not another drain**.
''' + '\n\n' + question(r'''**Question — equations on arrows**

1. Complete both flux columns, including zero effects. Use one family expression for repeated water/gas arrows. Keep only actual state dependencies; mark each row **fixed**, **state-dependent**, or **residual** beside its process ID.
2. Draw and label the arrows with these expressions. Add states and the active atm–ocn boundary; distinguish chemistry diagnostics and sediment memory. Check water balance at H_b.
3. For one internal arrow, use the supplied tendency rule below to show equal-and-opposite inventory changes. Do not rewrite the effects in prose.
''') + '\n\n' + flux_table_markdown(student=True) + r'''

For any internal dissolved transfer of $X=DIC$ or $TA$, **flux and concentration tendency differ**:

$$\left.\frac{dX_i}{dt}\right|_{i\to j}=-\frac{J^X_{ij}(t)}{m_i},\qquad
\left.\frac{dX_j}{dt}\right|_{i\to j}=+\frac{J^X_{ij}(t)}{m_j}.$$

Fill the table here or in the [student Excel worksheet](../../outputs/03_04_flux_specification/student.xlsx), whose amber fields are answer spaces. These are symbolic equations, not Excel calculation formulas or live model inputs.

<details>
<summary>Assumption notes: biology, weathering and fixed rates</summary>

The DIC-only POC closure omits nutrient/redox effects on TA. Nitrate uptake can increase TA and ammonium uptake can decrease it; a richer model needs the associated nutrient bookkeeping.

Weathering's 1 carbon : 2 TA is a **lumped boundary closure**, not a universal river composition. Carbonic-acid weathering of CaCO3 delivers two bicarbonates while consuming one CO2. River-only and combined atm–ocn accounting therefore differ. Here the source enters L_b with no explicit atm weathering sink. See [Middelburg et al. (2020), sections 4–6](https://doi.org/10.1029/2019RG000681).

Constant parameters do not imply constant fluxes: 02's export depended on $DIC_s(t)$ even with fixed $k$. Here both exports are fixed, but gas exchange and dissolution still respond to state. Additional pump feedbacks remain optional.

</details>
'''

nb.cells[8].source = answer(r'''The completed equations are tabulated below. POC, PIC and weathering are fixed; water-tracer transport, gas exchange and dissolution depend on state; net burial is a signed residual.

For any internal transfer, $m_i\dot X_i=-J^X$ and $m_j\dot X_j=+J^X$: their inventory sum is zero even when concentration changes differ. H_b gains and loses 25 Sv circulation plus 30 Sv mixing. DIC/TA and atm CO2 are reservoir states; pH/aqueous CO2 are chemistry diagnostics; snowline stores sediment history.

The paired carbonate fluxes give an aggregate active-system loss of $B_{net}$ carbon and $2B_{net}$ TA. Negative net burial returns old sediment. Do not apply a separate burial sink after PIC export and dissolution.

![Completed instructor specification](../../ref/figures/03_04_boudreau_instructor.png)
''')
# The reference is rendered as math in the notebook, from the same records as XLSX.
nb.cells[10].source = '''# Instructor reference: the student file omits this completed table.
from IPython.display import Markdown
from teaching_specification import flux_table_markdown
display(Markdown(flux_table_markdown()))
'''
nb.cells[10].outputs = []
nb.cells[10].execution_count = None

contour_intro = nbformat.v4.new_markdown_cell(r'''### Interpret your fluxes on the DIC–TA plane

Reuse 01's top view: DIC is horizontal, TA vertical, and each contour has constant seawater pCO2 [µatm]. The supplied plot recalculates chemistry for the workbook's L_b inputs and benchmark T/S/p, rather than 01's uniform conditions. Its dot is an input reference, **not the later stationary restart**. Treat each arrow as a local parcel change before transport and gas exchange.
''')
contour_question = nbformat.v4.new_markdown_cell(question(r'''**Question — interpret the paired fluxes**

From the dot, remove 20 µmol C/kg through POC export and separately through CaCO3 formation. Use your paired equations to draw the two DIC–TA vectors and predict the pCO2 changes from the contours. Why do the signs differ? Reverse the carbonate vector for dissolution. Reuse these vectors in 03.4; no additional flux-effects paragraph is needed.
''') + '\n\n' + answer(r'''Per mole C removed from the same parcel, model POC gives $(\Delta DIC,\Delta TA)=(-1,0)$ and lowers pCO2. CaCO3 formation gives $(-1,-2)$ and raises pCO2 near this reference: reduced TA leaves more of the remaining DIC as aqueous CO2. Dissolution reverses this to $(+1,+2)$ and lowers pCO2. TA changes are equivalents per mole C. These local vectors do not imply equal concentration changes between unequal box water masses.'''))
nb.cells = [*nb.cells[:7], nb.cells[8], nb.cells[10], contour_intro,
            nb.cells[7], contour_question, nb.cells[9], *nb.cells[11:]]
nbformat.write(nb, source)
build_student_notebook(source, ROOT / 'notebooks/student' / source.name)
print('Revised 03 and regenerated student copy.')
