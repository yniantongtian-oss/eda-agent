# COMSOL workspace

Use this directory for battery-specific COMSOL assets and small reproducible exports.

Recommended structure:

```text
comsol/
├─ models/       # .mph models; use Git LFS/external artifacts for large binaries
├─ manifests/    # model/study/mesh/parameter metadata
├─ scripts/      # deterministic MPh/COMSOL automation
├─ exports/      # small reference tables/images
└─ validation/   # PyBaMM/experiment comparison definitions
```

## Naming

Use semantic names:

```text
lfp_1d_dfn_revA.mph
cyl_generic_electrothermal_3d_revA.mph
module_cooling_plate_revA.mph
```

Every model should have a neighboring manifest containing chemistry, geometry revision, parameter-set source, COMSOL version, studies, mesh ID, solver notes and expected outputs.

## First COMSOL model sequence

1. `lfp_1d_dfn_revA` — 1D electrochemical consistency case.
2. `generic_cell_thermal_3d_revA` — geometry-driven heat conduction with externally supplied heat source.
3. `generic_cell_electrothermal_3d_revA` — electro-thermal coupling.
4. `generic_cell_mechanical_revA` — swelling/stress research model.
5. `module_cooling_revA` — module/cooling-system model.

Do not add untraceable commercial geometry or material properties. Unknown values belong in a parameter-estimation task, not in undocumented constants.