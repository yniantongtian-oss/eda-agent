# Roadmap

This roadmap is ordered to create a validated research stack rather than maximizing feature count.

## Phase 0 — Foundation

Deliverables:

- repository structure and environment,
- canonical data/sign/unit convention,
- LFP/graphite PyBaMM baseline,
- experiment/simulation manifest schema,
- COMSOL automation adapter skeleton,
- reproducible test suite.

Exit gate:

- one command produces a baseline simulation and manifest,
- unit tests pass,
- outputs can be ingested by the common data schema.

## Phase 1 — Physics baseline

Tasks:

- SPM, SPMe and DFN comparison,
- isothermal vs lumped-thermal comparison,
- C-rate sweep,
- ambient-temperature sweep,
- parameter sensitivity ranking,
- solver/runtime benchmark.

Exit gate:

- each model's validity/cost is documented,
- baseline figures are script-generated,
- sensitivity results identify the parameters that matter most for the next experiments.

## Phase 2 — COMSOL electro-thermal model

Tasks:

- define generic cell geometry and parameter manifest,
- create 1D electrochemical consistency case,
- create 2D/3D thermal/current-collector geometry,
- mesh-convergence study,
- PyBaMM ↔ COMSOL comparison,
- automated parameter/study/export workflow using MPh where feasible.

Exit gate:

- deterministic script can set parameters, solve and export agreed metrics,
- key outputs are validated against lower-order model and/or experiment,
- mesh/solver convergence is recorded.

## Phase 3 — Experimental validation

Tasks:

- instrument/fixture registration,
- baseline capacity tests,
- pulse characterization,
- temperature measurements,
- EIS/GITT/PITT as available and scientifically justified,
- calibration/validation split,
- uncertainty/error analysis.

Exit gate:

- a held-out test condition is predicted with predeclared metrics,
- disagreement is decomposed into measurement, parameter and model-structure contributions where possible.

## Phase 4 — Degradation

Tasks:

- select one mechanism at a time,
- calibrate on multi-condition ageing data,
- compare mechanism signatures,
- add coupled mechanisms only when separately justified,
- validate across temperature/protocol.

Exit gate:

- capacity fade alone is not the only validation signal,
- parameter identifiability is discussed,
- model generalization is evaluated on held-out conditions.

## Phase 5 — COMSOL surrogate modeling

Tasks:

- define physically valid DOE bounds,
- generate high-fidelity dataset,
- benchmark GP/tree/MLP models,
- quantify interpolation and OOD error,
- add active learning,
- integrate uncertainty.

Exit gate:

- surrogate reaches a predeclared error target on held-out and boundary cases,
- uncertainty flags poor extrapolation,
- fresh COMSOL spot checks confirm optimized candidates.

## Phase 6 — BMS and digital twin

Tasks:

- ECM baseline,
- SOC estimator,
- physics-based reduced model,
- online parameter adaptation,
- SOH estimator,
- uncertainty tracking,
- replay on measured drive/current profiles.

Exit gate:

- online runtime target is met,
- held-out-cell/state errors are reported,
- failure/uncertainty behavior is visible instead of hidden.

## Phase 7 — Pack/module scale

Tasks:

- liionpack electrical network baseline,
- cell-to-cell variation,
- thermal coupling,
- module cooling model,
- fault/imbalance cases,
- pack-level digital-twin interface.

Exit gate:

- pack model reproduces expected conservation/current-sharing behavior,
- temperature variation and cell variability are explicit,
- validation exists at least at subsystem level.

## Phase 8 — Optimization and research publications

Candidate studies:

- cooling topology optimization,
- geometry/tab optimization,
- multi-objective electro-thermal design,
- fast-charge protocol optimization under degradation/temperature constraints,
- active-learning reduction of COMSOL simulation budget,
- hybrid physics + AI SOH/RUL,
- field surrogate / neural operator study.

Publication package for each study:

```text
paper-id/
├─ question.md
├─ methods.md
├─ configs/
├─ data-manifest/
├─ scripts/
├─ figures/
├─ tables/
├─ metrics.json
└─ reproduction.md
```

## Immediate issue backlog

1. Implement PyBaMM baseline runner.
2. Implement manifest/data-schema objects.
3. Add C-rate/temperature sweep runner.
4. Add COMSOL/MPh adapter with graceful optional dependency.
5. Add baseline LFP config.
6. Add tests for data/sign/unit contracts.
7. Add result plotting/report generation.
8. Add public-dataset registry.
9. Add PyBaMM ↔ COMSOL comparison harness.
10. Add first surrogate benchmark.

## Research priority rule

When deciding what to build next, prefer the task that reduces the largest scientific uncertainty or validation gap, not the task that produces the most impressive UI.