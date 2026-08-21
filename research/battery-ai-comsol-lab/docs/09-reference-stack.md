# Reference stack

Snapshot: 2026-08-21.

This lab uses external software as reference engines and integration targets rather than copying their internals into the research package.

## COMSOL Multiphysics + Battery Design Module

Primary role:

- high-fidelity porous-electrode electrochemistry,
- 1D/2D/3D Newman-type battery models,
- electro-thermal coupling,
- geometry-dependent current/temperature fields,
- SEI/degradation studies,
- thermal-management and pack-scale studies,
- safety-oriented propagation modeling when used with validated inputs and appropriate research controls.

Official product page:

- https://www.comsol.com/battery-design-module

Automation layer in this project:

- MPh first for deterministic Python control,
- COMSOL MCP / sim-cli paths as optional agent orchestration layers.

## PyBaMM

Primary role:

- fast open physics-based battery models,
- SPM, SPMe and DFN model ladder,
- thermal and degradation options,
- rapid parameter studies,
- trusted lower-dimensional reference before expensive 3D studies.

Repository:

- https://github.com/pybamm-team/PyBaMM

Documentation:

- https://docs.pybamm.org/

## liionpack

Primary role:

- battery-pack electrical/network simulation built around PyBaMM,
- cell-to-cell variation and pack studies,
- lower-cost pack baseline before coupling high-fidelity thermal ROMs.

Repository:

- https://github.com/pybamm-team/liionpack

## MPh

Primary role:

- Pythonic COMSOL scripting/automation,
- deterministic parameter/study/export workflows.

Repository:

- https://github.com/MPh-py/MPh

## AI/agent COMSOL ecosystem already vendored by the parent repository

The parent `eda-agent` repository includes reviewed submodules for:

- `wjc9011/COMSOL_Multiphysics_MCP`
- `svd-ai-lab/sim-cli`
- `svd-ai-lab/sim-plugin-comsol`
- `deng-cy/deep_learning_topology_opt`
- `ethz-pes/AI-mag`
- `MPh-py/MPh`

The battery lab should consume these through stable interfaces rather than tightly coupling research logic to any one agent implementation.

## Selection rule

Use the simplest engine that can answer the scientific question:

```text
ECM / simple estimator
    ↓ when physics detail is needed
PyBaMM SPM/SPMe/DFN
    ↓ when geometry/local multiphysics matters
COMSOL 2D/3D
    ↓ after validation for repeated/online use
surrogate / ROM / digital twin
```

This hierarchy keeps expensive simulation focused on questions that actually require it and makes AI acceleration measurable.