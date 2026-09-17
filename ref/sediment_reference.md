# Optional sediment reference

Outside the four-hour core. The executable module is supplied in notebook 03.

### 9.1 What the three depths mean

All depths are reported as positive metres below sea level.

| Quantity | Meaning | Type in this model |
| --- | --- | --- |
| $z_{\mathrm{sat}}$ | **Calcite saturation horizon:** depth where the water column changes from supersaturated to undersaturated, $\Omega_{\mathrm{calcite}}=1$ | algebraic diagnostic |
| $z_{\mathrm{cc}}$ | **Carbonate compensation depth:** idealized depth at which the arriving modern carbonate rain is completely dissolved | algebraic diagnostic |
| $z_{\mathrm{snow}}$ | **Carbonate snowline:** deepest boundary of the existing reactive CaCO₃ sediment inventory | prognostic state with memory |

Thus $z_{\mathrm{sat}}$ and $z_{\mathrm{cc}}$ respond immediately to current deep-ocean chemistry and export. The snowline can lag because previously deposited carbonate must dissolve before the sediment boundary moves upward. At the preindustrial steady state, $z_{\mathrm{snow}}$ lies close to $z_{\mathrm{cc}}$.

### 9.2 How ESBMTK calculates $z_{\mathrm{sat}}$ and $z_{\mathrm{cc}}$

Carbonate system 2 first calculates deep carbonate ion from deep DIC, TA, and hydrogen ion,

$$
[\mathrm{CO_3^{2-}}]
=\frac{[\mathrm{DIC}]}
{1+[\mathrm{H^+}]/K_2+[\mathrm{H^+}]^2/(K_1K_2)}.
$$

Pressure makes calcite less soluble upward and more soluble downward. ESBMTK represents the saturation carbonate concentration with a depth lookup table and solves the saturation condition $[\mathrm{Ca^{2+}}][\mathrm{CO_3^{2-}}]=K_{sp}(z)$. The implemented solution is

$$
z_{\mathrm{sat}}
=z_{\mathrm{sat},0}
\ln\left(
\frac{[\mathrm{Ca^{2+}}][\mathrm{CO_3^{2-}}]}{K_{sp,0}}
\right),
$$

clipped between the top of the sediment domain and the maximum ocean depth.

The compensation depth also depends on the total PIC rain $F_{\mathrm{export}}$,

$$
z_{\mathrm{cc}}
=z_{\mathrm{sat},0}
\ln\left(
\frac{F_{\mathrm{export}}[\mathrm{Ca^{2+}}]}
{K_{sp,0}A_Dk_c}
+\frac{[\mathrm{Ca^{2+}}][\mathrm{CO_3^{2-}}]}{K_{sp,0}}
\right).
$$

Here $A_D$ is the hypsometric seafloor area between $z_0$ and $z_{\max}$, and $k_c$ is the calcite dissolution coefficient. Lower deep-ocean carbonate makes both horizons shallower; greater carbonate rain makes $z_{\mathrm{cc}}$ deeper because more material can survive dissolution.

### 9.3 From ocean hypsometry to dissolution and burial

The model uses one-metre lookup tables for seafloor area and the carbonate concentration required for saturation. It divides the seafloor into chemically distinct depth intervals:

```text
z0                 zsat                    zcc                 zsnow       zmax
│ supersaturated     │ undersaturated        │ no modern rain     │ old CaCO3 │
│ background term    │ kinetic dissolution   │ survives           │ may dissolve
└────────────────────┴───────────────────────┴────────────────────┴────────────
```

The mean carbonate rain per unit depositional area is

$$
B_{A_D}=\frac{F_{\mathrm{export}}}{A_D}.
$$

ESBMTK sums four contributions: a prescribed background response above $z_{\mathrm{sat}}$, undersaturation-driven dissolution between $z_{\mathrm{sat}}$ and $z_{\mathrm{cc}}$, complete dissolution of modern rain below $z_{\mathrm{cc}}$, and dissolution of pre-existing sediment when $z_{\mathrm{snow}}>z_{\mathrm{cc}}$. In compact form,

$$
F_{\mathrm{diss}}
=B_{\mathrm{NS}}+B_{\mathrm{DS}}+B_{\mathrm{CC}}+B_{\mathrm{PDC}},
$$

$$
F_{\mathrm{burial}}
=F_{\mathrm{export}}-F_{\mathrm{diss}}.
$$

The dissolved fraction returns to the deep ocean as one DIC plus two TA equivalents per mole of CaCO₃,

$$
J_{\mathrm{deep,DIC}}=F_{\mathrm{diss}},
\qquad
J_{\mathrm{deep,TA}}=2F_{\mathrm{diss}}.
$$

The PIC connection was created with `bp='sink'`, so its nominal deep-ocean sink is bypassed. Carbonate system 2 adds only the dissolved fraction back to the water. The undissolved residual has therefore left the active ocean inventory and represents burial. There is no explicit sediment reservoir in carbonate system 2; a model requiring explicit sediment mass would need a different module.

### 9.4 Why $z_{\mathrm{snow}}$ is different

The snowline is initialized near 4750 m and is registered as an ESBMTK state variable. When the instantaneous compensation depth becomes deeper than the snowline, the snowline relaxes downward toward it. When the snowline is deeper than the compensation depth, previously deposited carbonate between them dissolves and the boundary shoals according to

$$
\frac{dz_{\mathrm{snow}}}{dt}
=-\frac{B_{\mathrm{PDC}}}
{A(z_{\mathrm{snow}})I_{\mathrm{CaCO_3}}},
$$

where $A(z_{\mathrm{snow}})$ is seafloor area per depth interval and $I_{\mathrm{CaCO_3}}$ is the dissolvable sediment inventory per unit area. This prognostic boundary gives carbonate compensation its memory and long response time.

During integration, carbonate system 2 repeatedly calculates the instantaneous $z_{\mathrm{sat}}$, $z_{\mathrm{cc}}$, and dissolution flux needed by the ODE, but only $z_{\mathrm{snow}}$ is retained as a dynamic state. After integration, `postprocess_carbonate_horizons` reconstructs the saved $z_{\mathrm{sat}}$, $z_{\mathrm{cc}}$, $F_{\mathrm{diss}}$, and $F_{\mathrm{burial}}$ series from the stored chemistry, PIC flux, and already-integrated snowline.
