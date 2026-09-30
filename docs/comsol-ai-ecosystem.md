# COMSOL + AI ecosystem

This repository vendors selected COMSOL/AI projects as Git submodules so their upstream history, licensing, and update paths remain intact.

Snapshot date: 2026-08-21.

## Selected projects

| Project | Role in the stack | Stars at review | License | Pinned commit |
| --- | --- | ---: | --- | --- |
| `wjc9011/COMSOL_Multiphysics_MCP` | Direct AI/MCP control surface for COMSOL Multiphysics | 654 | MIT | `99172f8f43c6753c2442c406cd5c6055ea8c5bef` |
| `MPh-py/MPh` | Pythonic COMSOL automation/scripting foundation | 576 | MIT | `d6efe2a2cad84424b48aec8f0fe03efe60d69289` |
| `svd-ai-lab/sim-cli` | Agent-oriented CAE runtime for COMSOL/Abaqus/Ansys | 210 | Apache-2.0 | `8af3059eb301f300abfc609f24ea1ea6e9ee2a45` |
| `deng-cy/deep_learning_topology_opt` | COMSOL-linked deep-learning topology optimization research code | 146 | MIT | `40600447fd3c36cf3757eb3b8f685bcb2e96a5f0` |
| `ethz-pes/AI-mag` | FEM + artificial-neural-network surrogate modeling/design workflow | 136 | BSD-2-Clause | `c71d3f6e68af15db3a70dc5381d5a0d3cd4668f6` |
| `svd-ai-lab/sim-plugin-comsol` | COMSOL plugin for `sim-cli`, including `.mph` inspection and live-session workflows | 65 | Apache-2.0 | `770999a377b08706e80be7a269c80a2f4f32aab8` |

## Why these six

The set intentionally covers different layers rather than collecting duplicate MCP servers:

1. **Direct LLM-to-COMSOL control** : `COMSOL_Multiphysics_MCP`.
2. **Stable Python automation layer** : `MPh`.
3. **General CAE agent runtime** : `sim-cli`.
4. **COMSOL-specific runtime bridge** : `sim-plugin-comsol`.
5. **Machine-learning-driven topology optimization** : `deep_learning_topology_opt`.
6. **FEM-generated data + neural surrogate modeling** : `AI-mag`.

Together they are a useful reference base for extending `eda-agent` from EDA-only workflows toward a broader engineering agent that can coordinate circuit design, multiphysics simulation, optimization, and learned surrogate models.

## Clone with the external modules

```bash
git clone --recurse-submodules https://github.com/yniantongtian-oss/eda-agent.git
```

For an existing clone:

```bash
git submodule update --init --recursive
```

## Updating a pinned upstream

Each submodule is intentionally pinned to a reviewed commit. Update one module only after checking upstream changes and its license:

```bash
cd external/comsol-ai/<module>
git fetch origin
git checkout <new-reviewed-commit>
cd ../../..
git add external/comsol-ai/<module>
git commit -m "Update COMSOL AI module: <module>"
```

## Integration direction for eda-agent

A sensible next architecture is to keep each upstream project isolated and build an `eda-agent` COMSOL backend/adaptor on top of their public interfaces. Avoid copying internal source into the core package unless there is a specific compatibility reason. This reduces license risk, keeps updates tractable, and makes it easier to benchmark multiple control paths (MCP, Python API, GUI/live-session bridge, and surrogate-model workflows).

Potential next milestones:

- Add `EDA_AGENT_BACKEND=comsol` with a minimal attach/ping/model-info surface.
- Reuse `MPh` for deterministic model loading, parameter changes, solve calls, and result extraction.
- Add an optional MCP compatibility adapter informed by `COMSOL_Multiphysics_MCP`.
- Use `sim-cli` / `sim-plugin-comsol` as an alternate live-session execution path.
- Add dataset export hooks for training surrogate models from parameter sweeps.
- Add optimization loops that combine COMSOL solves with learned surrogate models.
- Extend the dashboard with geometry/model tree, study status, solver progress, parameters, and result previews.

## License and provenance

The external repositories remain separate Git submodules and retain their original authorship and licenses. `eda-agent` does not relicense their contents. Consult each upstream repository before redistribution or modification.
