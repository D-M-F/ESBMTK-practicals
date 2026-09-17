"""Shared carbonate choices and explicit teaching geometry for practicals 00–02.

The Boudreau benchmark in presets.py deliberately keeps its own box conditions.
ESBMTK pressure is in bar; PyCO2SYS pressure is in dbar.
The 02 layer split is derived from a prescribed pumped ocean/atmosphere ratio;
the whole-ocean geometry and 01 initial carbon inventory remain independent of it.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TeachingConfig:
    temperature: float = 16.0
    salinity: float = 35.0
    pressure_bar: float = 0.0
    opt_k_carbonic: int = 10
    opt_pH_scale: int = 2
    opt_buffers_mode: int = 1
    atmosphere_mol: float = 1.77e20
    ocean_area_m2: float = 3.60e14
    ocean_depth_m: float = 3750.0
    pumped_ocean_atmosphere_ratio: float = 62.4  # prescribed reference inventory ratio
    target_xco2_ppm: float = 280.0
    target_dic_umol_kg: float = 2040.0
    target_deep_dic_umol_kg: float = 2250.0
    mixing_sv: float = 20.0  # independent transport assumption

    @property
    def chemistry(self):
        return {key: getattr(self, key) for key in
                ("opt_k_carbonic", "opt_pH_scale", "opt_buffers_mode")}

    @property
    def pyco2(self):
        return dict(self.chemistry, temperature=self.temperature,
                    salinity=self.salinity, pressure=10 * self.pressure_bar)

    @property
    def density_kg_m3(self):
        from esbmtk import SeawaterConstants

        # The public method uses only S, T, P; no chemistry or fitted state.
        return float(SeawaterConstants.get_density(
            None, self.salinity, self.temperature, self.pressure_bar))

    @property
    def ocean_volume_m3(self):
        return self.ocean_area_m2 * self.ocean_depth_m

    @property
    def surface_depth_m(self):
        """Prepare the 02 layer split from the chosen 62.4 reference ratio.

        At the reference xCO2 and DIC values, solve
          rho*A*[h*DIC_s + (H-h)*DIC_d] = R*C_atm
        for h. DIC is converted from umol/kg to mol/kg. This is an algebraic
        calibration of the teaching geometry, not an observed mixed-layer depth
        or a fit to the model run. No approximate baseline ratio (57) is used.
        """
        surface_dic = self.target_dic_umol_kg * 1e-6
        deep_dic = self.target_deep_dic_umol_kg * 1e-6
        if deep_dic <= surface_dic:
            raise ValueError("reference deep DIC must exceed surface DIC")
        atmospheric_carbon = self.atmosphere_mol * self.target_xco2_ppm * 1e-6
        mass_per_depth = self.density_kg_m3 * self.ocean_area_m2
        depth = (mass_per_depth * self.ocean_depth_m * deep_dic
                 - self.pumped_ocean_atmosphere_ratio * atmospheric_carbon
                 ) / (mass_per_depth * (deep_dic - surface_dic))
        if not 0 < depth < self.ocean_depth_m:
            raise ValueError("prescribed inventory ratio must give a surface depth within the ocean")
        return depth

    @property
    def surface_volume_m3(self):
        if not 0 < self.surface_depth_m < self.ocean_depth_m:
            raise ValueError("surface depth must be within the ocean")
        return self.ocean_area_m2 * self.surface_depth_m

    @property
    def deep_volume_m3(self):
        return self.ocean_volume_m3 - self.surface_volume_m3

    @property
    def total_carbon_mol(self):
        return (self.atmosphere_mol * self.target_xco2_ppm * 1e-6
                + self.ocean_volume_m3 * self.density_kg_m3
                * self.target_dic_umol_kg * 1e-6)

    def reference_state(self):
        """Infer TA from two observed targets; this is a calibration."""
        import PyCO2SYS as pyco2

        return pyco2.sys(par1=self.target_dic_umol_kg, par1_type=2,
                         par2=self.target_xco2_ppm, par2_type=9, **self.pyco2)


TEACHING = TeachingConfig()
