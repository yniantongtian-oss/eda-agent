# Battery AI + COMSOL Research Lab

A research-grade battery modeling, simulation, experiment, and AI workspace designed to connect **COMSOL Multiphysics**, **PyBaMM**, electrochemical experiments, machine learning, optimization, BMS algorithms, and digital-twin workflows.

> Status: initial research architecture. The project is intentionally model- and chemistry-agnostic. It starts with a reproducible LFP/graphite electrochemical baseline and a separate LG M50 electro-thermal reference so thermal studies do not silently borrow unsupported properties.

## Research objective

Build one coherent workflow from physics to experiment to AI:

**cell design → electrochemical model → thermal/mechanical multiphysics → experiment → parameter identification → degradation model → surrogate model → optimization → BMS/digital twin → pack-level validation**.

The repository is organized so each layer can be used independently, while sharing the same parameter, metadata, validation, and provenance conventions.

## Core research tracks

1. **Electrochemistry** — SPM, SPMe, DFN/P2D, transport, kinetics, concentration and potential fields.
2. **Thermal behavior** — lumped, 2D/3D heat generation and conduction, cooling boundary conditions, anisotropic thermal properties.
3. **Mechanical coupling** — electrode swelling, diffusion-induced stress, casing constraint, contact/pressure effects.
4. **Ageing and degradation** — SEI growth, lithium plating, loss of active material, porosity change, resistance growth, calendar/cycle ageing.
5. **Safety / thermal runaway** — prevention, detection, conservative heat-source and propagation-oriented modeling with safety-first experimental boundaries.
6. **AI and surrogate models** — SOH/RUL, reduced-order surrogates, PINN/operator-learning experiments, Bayesian optimization, uncertainty quantification.
7. **BMS and digital twin** — SOC/SOH estimation, model adaptation, parameter tracking, fault indicators, state synchronization with measured data.
8. **Pack/system studies** — electrical interconnects, cell variation, thermal gradients, cooling topology, module/pack observability.

## Directory map

```text
battery-ai-comsol-lab/
├─ README.md
├─ pyproject.toml
├─ configs/                 # reproducible parameter/configuration files
├─ src/battery_lab/         # Python research package
├─ tests/                   # unit and data-contract tests
├─ comsol/                  # COMSOL model conventions and exported artifacts
├─ experiments/             # experiment protocols and metadata templates
├─ data/                    # data contract; raw data is not committed
├─ notebooks/               # exploratory analyses only
├─ papers/                  # paper reproduction registry
└─ docs/
   ├─ 01-research-program.md
   ├─ 02-comsol-modeling.md
   ├─ 03-ai-ml-program.md
   ├─ 04-experimental-program.md
   ├─ 05-data-standard.md
   ├─ 06-roadmap.md
   ├─ 07-bms-digital-twin.md
   ├─ 08-safety-thermal-runaway.md
   └─ 09-reference-stack.md
```

## Recommended model ladder

Do not start every question with a full 3D multiphysics solve. Use the cheapest model that can answer the question and escalate only when validation shows it is necessary.

| Level | Model | Primary use |
|---|---|---|
| L0 | ECM / Rint / Thevenin | controls, online estimation, fast pack studies |
| L1 | SPM | fast physics-based screening |
| L2 | SPMe | electrolyte effects with moderate cost |
| L3 | DFN/P2D | cell electrochemistry and parameter studies |
| L4 | DFN + thermal | electro-thermal coupling |
| L5 | 2D/3D COMSOL multiphysics | geometry, tabs, cooling, local gradients, mechanics |
| L6 | validated surrogate / ROM | optimization, real-time digital twin, large sweeps |

## Reproducible physics baselines

### A. LFP/graphite electrochemical baseline

`configs/lfp_graphite_baseline.yaml` uses PyBaMM `Prada2013` with an isothermal DFN. This is deliberate: the parameter set is useful for an A123-style LFP electrochemical reference but does not provide a complete thermal-property set. The associated C-rate sweep is `configs/lfp_crate_sweep.yaml`.

### B. LG M50 electro-thermal reference

`configs/lgm50_electrothermal_baseline.yaml` uses PyBaMM `ORegan2022` with DFN + lumped thermal physics. The source parameterization was developed for thermal-electrochemical modeling of a high-energy cylindrical LG M50 cell. The C-rate × temperature sweep is `configs/lgm50_crate_temperature_sweep.yaml`.

Neither baseline is a specification for the actual cell you may later test. Real-cell comparison requires measured or otherwise validated geometry, electrochemical, thermal and operating-limit data.

## Environment

Python 3.11+ is recommended.

```bash
cd research/battery-ai-comsol-lab
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -e .[dev]
```

COMSOL automation is optional and isolated behind the `comsol` extra:

```bash
pip install -e .[comsol]
```

A valid COMSOL installation/license is still required. The Python wrapper does not redistribute COMSOL.

## Quick start

LFP electrochemical baseline:

```bash
battery-pybamm --config configs/lfp_graphite_baseline.yaml --out runs/lfp_baseline
```

Electro-thermal baseline:

```bash
battery-pybamm --config configs/lgm50_electrothermal_baseline.yaml --out runs/lgm50_thermal
```

C-rate × temperature sweep:

```bash
battery-sweep --config configs/lgm50_crate_temperature_sweep.yaml
```

Each run exports tidy CSV plus a JSON manifest containing the exact input config, model choice, timestamps and software metadata.

## Research discipline

Every result intended for comparison or publication should carry:

- chemistry and cell-format declaration,
- parameter-set name/version/source,
- model equations/assumptions or model identifier,
- geometry revision where relevant,
- boundary/initial conditions,
- solver settings,
- experiment/test ID,
- raw-data provenance,
- preprocessing version,
- code commit SHA,
- metric definition and uncertainty/replicate information.

## Upstream tools worth integrating

The surrounding `eda-agent` repository already includes reviewed COMSOL/AI projects. For battery-specific work, this lab is designed to interoperate with:

- **PyBaMM** — fast physics-based battery models in Python.
- **liionpack** — pack simulation built on PyBaMM.
- **MPh** — Pythonic COMSOL automation.
- **COMSOL Multiphysics MCP / sim-cli / sim-plugin-comsol** — alternative AI/agent control paths for COMSOL.

Upstream code should remain upstream where possible. This lab owns the integration contracts, reproducible workflows, battery-domain models, experiments, validation and research outputs.

## What counts as success

A research track is considered mature only when it has:

1. a clearly stated scientific question,
2. a reproducible baseline,
3. sensitivity/identifiability analysis,
4. experimental or trusted-reference validation,
5. uncertainty/error reporting,
6. at least one ablation or competing-model comparison,
7. a scripted path from raw inputs to final figures/tables.

See `docs/01-research-program.md` and `docs/06-roadmap.md` for the full program.
