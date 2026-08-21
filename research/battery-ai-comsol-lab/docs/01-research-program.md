# Research program

## 1. Scientific scope

The program treats rechargeable-battery research as a hierarchy of coupled questions rather than a single simulation task. The primary system is a Li-ion cell, then module/pack, with deliberate support for multiple chemistries and form factors.

### Theme A — Electrochemical performance

Questions:

- Which transport/kinetic limitations dominate at a given temperature and C-rate?
- How sensitive are voltage, usable capacity and overpotential to particle size, porosity, conductivity, diffusion and reaction-rate parameters?
- Which parameters are identifiable from voltage/current/temperature alone, and which require EIS, GITT/PITT or destructive characterization?

Models:

- equivalent circuit for control-oriented baselines,
- SPM and SPMe for rapid screening,
- DFN/P2D for reference electrochemical behavior,
- COMSOL 1D/2D/3D for geometry-dependent local fields.

Primary observables:

- terminal voltage,
- electrode/electrolyte potential,
- solid/electrolyte concentration,
- reaction current density,
- overpotential,
- heat generation,
- lithium inventory and active-material state.

### Theme B — Electro-thermal coupling

Questions:

- How do tabs, anisotropic thermal conductivity, cooling boundaries and pack placement affect temperature gradients?
- When does a lumped temperature model cease to be valid?
- What is the accuracy/cost tradeoff between PyBaMM thermal models and 3D COMSOL models?

Deliverables:

- validated heat-generation model,
- 3D cell temperature field,
- hotspot/gradient metrics,
- reduced-order thermal surrogate.

### Theme C — Mechanics and swelling

Questions:

- How does state of lithiation drive particle/electrode/cell swelling?
- Where do diffusion-induced stresses become important?
- How do stack pressure and casing constraints change electrochemical/thermal response?

Deliverables:

- electrochemical-to-mechanical coupling map,
- stress/strain field studies,
- sensitivity to mechanical boundary conditions,
- candidate observables for pressure/strain-based state estimation.

### Theme D — Degradation

Mechanisms to study separately before coupling:

- SEI growth,
- lithium plating,
- loss of active material,
- particle cracking where supported,
- porosity/tortuosity evolution,
- resistance growth,
- calendar ageing,
- temperature-accelerated side reactions.

Research rule: do not infer a unique degradation mechanism from capacity fade alone. Fit/validate against multiple observables whenever possible.

### Theme E — Safety and abuse modeling

Scope is computational and measurement-oriented: detection, characterization, prevention and propagation mitigation. See `08-safety-thermal-runaway.md` for explicit safety boundaries.

Questions:

- Which measurable precursors correlate with unsafe thermal escalation?
- How do cooling geometry and cell spacing affect propagation risk?
- Can a reduced-order safety model preserve conservative temperature/risk bounds?

### Theme F — AI / machine learning

AI is used where it adds measurable value:

- surrogate modeling for expensive multiphysics solves,
- inverse parameter estimation,
- SOH/RUL prediction,
- anomaly/fault detection,
- experiment selection / active learning,
- Bayesian optimization of design parameters,
- uncertainty-aware digital twins.

AI models must always be compared with physics and simple statistical baselines.

## 2. Cell formats

The architecture should support:

- cylindrical cells,
- prismatic cells,
- pouch cells,
- coin/half-cell research fixtures where appropriate.

Each dataset/model record must declare format and geometry revision. Geometry-dependent COMSOL outputs must never be mixed without that metadata.

## 3. Chemistry matrix

Priority order:

1. LFP/graphite — baseline and thermal/safety studies.
2. NMC/graphite — high-energy comparison and degradation work.
3. NCA/graphite — optional high-energy comparison.
4. LTO-based systems — fast-charge and longevity comparison.
5. Solid-state systems — future branch once material/interface models and data are available.

## 4. Model-validation ladder

For every major study:

1. analytical or simple sanity check where possible,
2. PyBaMM SPM/SPMe baseline,
3. PyBaMM DFN reference,
4. COMSOL model for geometry/local-field questions,
5. experimental comparison,
6. uncertainty/sensitivity analysis,
7. surrogate/ROM only after the parent physics model is validated.

## 5. Parameter identification program

Parameter classes:

- geometric: thickness, area, porosity, particle radius;
- thermodynamic: OCP functions, entropic coefficient;
- kinetic: exchange-current terms, rate constants;
- transport: solid/electrolyte diffusivity, conductivity, transference;
- thermal: heat capacity, conductivity, convection/contact terms;
- degradation: side-reaction parameters and activation energies;
- mechanical: modulus, Poisson ratio, expansion coefficients where modeled.

Methods:

- literature/parameter-set prior,
- direct measurement,
- EIS/GITT/PITT-informed estimates,
- deterministic least squares,
- Bayesian inference or ensemble methods,
- profile likelihood / Fisher-information checks for identifiability.

## 6. Experiment-to-model loop

```text
scientific question
      ↓
minimal model + expected signature
      ↓
experiment design
      ↓
raw data + metadata
      ↓
calibration / parameter estimation
      ↓
validation on held-out conditions
      ↓
error + uncertainty analysis
      ↓
model refinement or hypothesis rejection
```

## 7. Minimum publication-grade evidence

Before treating a result as publication-ready, require:

- independent validation condition(s),
- clear data split logic for ML,
- repeatability or uncertainty accounting,
- parameter-source traceability,
- model/solver convergence checks where relevant,
- baseline comparison,
- sensitivity analysis,
- versioned scripts that regenerate figures and tables.

## 8. Candidate first papers/projects

### Project P1 — Electro-thermal model cross-validation

Compare PyBaMM DFN + thermal against COMSOL electro-thermal simulation across C-rate and ambient temperature. Quantify where low-dimensional thermal assumptions break down.

### Project P2 — AI surrogate for 3D battery thermal field

Generate a controlled COMSOL design-of-experiments dataset and train a surrogate to predict peak temperature and spatial temperature metrics. Include uncertainty and out-of-distribution tests.

### Project P3 — Physics + ML SOH estimation

Combine interpretable physics-derived features with sequence models or gradient boosting for SOH prediction. Test cross-temperature and cross-cell generalization.

### Project P4 — Cooling geometry optimization

Use COMSOL for high-fidelity training/validation, a surrogate for search, and Bayesian or multi-objective optimization for peak temperature, gradient, pressure drop and energy cost.

### Project P5 — Digital twin with online parameter adaptation

Run a reduced-order electro-thermal model online, update selected parameters from measured voltage/current/temperature, and track SOC/SOH with uncertainty.