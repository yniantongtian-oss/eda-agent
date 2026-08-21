# COMSOL battery modeling architecture

## 1. Purpose

COMSOL is the high-fidelity layer for questions that depend on local geometry, coupled fields, tab/current-collector effects, anisotropic heat transfer, mechanical constraint, cooling topology or pack-scale spatial gradients.

The repository should avoid using COMSOL as an opaque black box. Every model should expose its assumptions, parameter sources, boundary conditions, mesh strategy, solver settings and exported observables.

## 2. Model hierarchy

### M0 — 1D electrochemistry reference

Use a 1D porous-electrode model to establish electrochemical consistency with PyBaMM DFN/P2D.

Suggested physics:

- charge conservation in solids/electrolyte,
- lithium transport in solid particles,
- electrolyte mass transport,
- Butler–Volmer reaction kinetics,
- OCP and transport-property functions.

Validation outputs:

- voltage vs time/capacity,
- local reaction current,
- electrode/electrolyte potentials,
- solid/electrolyte concentrations.

### M1 — Electro-thermal cell

Couple electrochemistry to heat transfer.

Heat sources may include, depending on model fidelity:

- irreversible reaction heat,
- ohmic/Joule heating,
- reversible/entropic heat,
- contact/interconnect losses if represented.

Key outputs:

- volume-averaged temperature,
- maximum temperature,
- temperature gradient,
- heat-generation partition,
- voltage/temperature coupling error relative to lower-order models.

### M2 — 2D/3D current-collector and tab model

Purpose:

- current nonuniformity,
- tab placement effects,
- local Joule heating,
- spatial temperature gradients.

Geometry must be revision-controlled. The exported model manifest should include dimensions and material assignments.

### M3 — Electro-chemo-mechanical model

Potential couplings:

- state-of-lithiation → eigenstrain/expansion,
- diffusion-induced stress,
- layer stack constraint,
- casing/contact pressure,
- stress-dependent transport/kinetics only when scientifically justified and parameterized.

### M4 — Cooling-system / module model

Possible domains:

- battery solids,
- cooling plate,
- coolant channels,
- interfaces/contact resistances,
- external enclosure.

Objectives:

- maximum cell temperature,
- cell-to-cell temperature spread,
- pressure drop / pumping-power proxy,
- thermal uniformity,
- robustness to cell variation and boundary uncertainty.

### M5 — Safety-oriented thermal propagation model

Use conservative source terms and validated thermal properties. The focus is prevention, detection and propagation mitigation. Do not treat an unvalidated reaction-kinetics model as predictive safety truth.

## 3. Parameter namespaces

Recommended COMSOL parameter groups:

```text
geom_*     geometry
mat_*      material properties
echem_*    electrochemical parameters
therm_*    thermal parameters
mech_*     mechanical parameters
age_*      degradation parameters
bc_*       boundary conditions
study_*    study/sweep controls
mesh_*     mesh controls
```

Keep user-facing engineering units in the source manifest, but normalize computational inputs explicitly.

## 4. Geometry conventions

Every geometry should have:

- a unique `geometry_id`,
- semantic dimensions rather than anonymous `L1`, `L2`, ...,
- named selections for active materials, separators, collectors, tabs, cooling contacts and external surfaces,
- a version note whenever topology changes.

Example:

```text
geometry_id: cyl_18650_revA
cell_radius_mm: 9.0
cell_height_mm: 65.0
positive_tab_width_mm: ...
negative_tab_width_mm: ...
```

Do not claim real commercial-cell geometry unless its provenance is known.

## 5. Mesh strategy

Each model family should define:

- mesh rationale,
- minimum local element size in high-gradient regions,
- boundary-layer treatment when needed,
- at least three mesh levels for convergence checks,
- a reported convergence metric.

Suggested convergence quantities:

- terminal voltage,
- maximum temperature,
- integral heat generation,
- maximum stress,
- pressure drop.

A result used for publication should state the chosen mesh and convergence delta.

## 6. Solver discipline

Track:

- study type,
- time-step/relative tolerance controls,
- nonlinear solver settings where changed from defaults,
- continuation/ramping strategy,
- convergence warnings,
- wall time and machine metadata for benchmarking.

If a solve is stabilized through artificial parameter changes, that must be recorded in the run manifest.

## 7. COMSOL automation contract

The Python integration should expose a narrow deterministic surface rather than arbitrary GUI automation as the first choice:

```python
open_model(path)
set_parameters(mapping)
run_study(study_name)
export_table(name, path)
export_image(name, path)
read_global(expressions)
save_copy(path)
close_model()
```

`MPh` is the preferred first automation layer. MCP/agent tooling can orchestrate these operations, but the scientific workflow should remain scriptable without an LLM.

## 8. Required model manifest

Every `.mph` or exported model bundle should have a neighboring YAML/JSON manifest containing:

```yaml
model_id: lfp_dfnt_3d_revA
comsol_version: unknown
geometry_id: cyl_generic_revA
chemistry: LFP_graphite
parameter_set: baseline_v1
study: discharge_1C_25C
mesh: fine_v2
inputs:
  ambient_temperature_K: 298.15
  c_rate: 1.0
outputs:
  - terminal_voltage_V
  - max_temperature_K
  - avg_temperature_K
  - total_heat_W
validation:
  reference_dataset: null
  metric: null
```

## 9. Cross-validation with PyBaMM

For comparable 1D electrochemical cases:

1. use the same parameter source where possible,
2. align initial SOC/state definitions,
3. align current sign convention,
4. align temperature assumptions,
5. compare voltage/capacity and internal-state summaries,
6. separate discretization/solver differences from physical-model differences.

The target is not numerically identical output. The goal is to explain discrepancies.

## 10. Design-of-experiments for AI surrogate generation

Before launching large COMSOL sweeps:

- identify parameters with physical bounds,
- remove redundant/unidentifiable dimensions,
- choose Latin-hypercube/Sobol/space-filling design as appropriate,
- reserve edge/out-of-domain cases for robustness testing,
- record failed/converged runs instead of silently dropping them.

Possible inputs:

- C-rate,
- ambient/coolant temperature,
- convection coefficient,
- thermal contact resistance,
- tab dimensions/locations,
- electrode thickness/porosity within justified ranges,
- coolant flow rate for pack studies.

Possible surrogate targets:

- voltage trajectory summaries,
- maximum temperature,
- temperature spread,
- heat generation,
- pressure drop,
- stress metrics,
- selected field coefficients/POD modes.

## 11. Folder convention

```text
comsol/
├─ README.md
├─ models/        # .mph files when size/licensing/project policy permits
├─ manifests/     # YAML/JSON manifests
├─ scripts/       # COMSOL/MPh automation scripts
├─ exports/       # small canonical reference exports
└─ validation/    # comparison configs and metric definitions
```

Large binary `.mph` files should generally be stored with Git LFS or an external artifact/data store rather than ordinary Git history.