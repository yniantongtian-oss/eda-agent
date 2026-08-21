# AI / ML research program

## 1. Role of AI

AI is a computational tool inside a physics-and-experiment research loop. It should reduce expensive simulation cost, improve inference, identify patterns that simple models miss, or enable online estimation. It should not replace conservation laws, parameter provenance or validation.

## 2. Workstreams

### A. Surrogate models for COMSOL

Goal: approximate expensive outputs while preserving quantified error.

Candidate inputs:

- C-rate / current profile descriptors,
- ambient or coolant temperature,
- cooling boundary parameters,
- geometry design variables,
- selected electrochemical/thermal properties.

Targets:

- terminal-voltage features,
- maximum/average temperature,
- temperature nonuniformity,
- total heat generation,
- stress/strain summaries,
- pressure drop,
- field representations using PCA/POD/autoencoder coefficients.

Model families to compare:

- linear/ridge baseline,
- Gaussian process for smaller DOE datasets,
- gradient-boosted trees,
- MLP,
- sequence models for trajectories,
- neural operators where field-to-field mapping is justified.

Do not jump to a large neural network before reporting a simple baseline.

### B. SOH and RUL

Possible feature groups:

- capacity and coulombic-efficiency trends,
- incremental capacity / differential voltage features,
- EIS features,
- relaxation features,
- temperature statistics,
- resistance/ECM estimates,
- physics-derived latent parameters.

Evaluation must distinguish:

- random within-cell split,
- leave-cycle-block-out split,
- leave-cell-out split,
- leave-temperature/protocol-out split.

The last two are usually much harder and more meaningful for generalization.

Metrics:

- MAE/RMSE,
- calibration/coverage for probabilistic predictions,
- error by ageing stage,
- early-life prediction error,
- cross-cell/protocol performance.

### C. SOC/SOH hybrid estimation

Combine:

- ECM/SPM/SPMe state transition,
- Kalman/ensemble/particle filtering or optimization,
- ML residual correction or parameter mapper,
- uncertainty bounds.

The hybrid model must be benchmarked against the physics-only estimator.

### D. Inverse parameter estimation

Targets may include:

- diffusion/kinetic effective parameters,
- resistance/contact terms,
- thermal coefficients,
- selected degradation parameters.

Methods:

- gradient-based optimization where differentiable,
- derivative-free search,
- Bayesian optimization,
- simulation-based inference when justified.

Always run identifiability/sensitivity checks. A low fitting error does not imply a physically unique parameter set.

### E. Active learning and experiment selection

Use uncertainty or expected information gain to choose the next:

- C-rate,
- temperature,
- SOC window,
- pulse profile,
- COMSOL geometry design point.

Report the gain relative to random or fixed-grid sampling.

### F. PINNs and operator learning

These are research tracks, not default solvers.

Potential targets:

- reduced electrochemical PDE components,
- thermal field reconstruction,
- fast parametric field prediction.

Minimum evidence required:

- compare against a trusted numerical solver,
- report residual and observable error separately,
- test outside training collocation distribution,
- report training cost as well as inference cost.

## 3. Data leakage controls

Battery datasets are especially easy to leak because adjacent cycles from one cell are highly correlated.

Rules:

- split by cell before feature normalization when evaluating cross-cell generalization,
- fit scalers only on training data,
- never use future-cycle information in online/RUL features,
- preserve protocol/temperature metadata,
- version preprocessing code and feature definitions.

## 4. Uncertainty quantification

Recommended options:

- Gaussian-process predictive uncertainty,
- deep ensembles,
- quantile regression,
- conformal prediction,
- bootstrap across cells,
- Bayesian parameter posterior propagated through the physics model.

Report calibration, not only point error.

## 5. Surrogate acceptance gates

A surrogate should not replace a high-fidelity model in optimization until it passes:

1. held-out interpolation test,
2. boundary-condition test,
3. out-of-distribution stress test,
4. uncertainty/calibration check,
5. physical plausibility checks,
6. spot-validation against new COMSOL runs.

## 6. Multi-objective battery design

Candidate objectives:

- energy/power proxy,
- maximum temperature,
- thermal gradient,
- degradation proxy,
- pressure drop/pumping power,
- mass/volume,
- safety margin.

Candidate methods:

- Bayesian multi-objective optimization,
- NSGA-II or similar evolutionary search,
- surrogate-assisted optimization.

Constraints should be explicit and physically justified rather than hidden inside penalty weights.

## 7. Reproducible ML experiment record

Every training run should log:

```yaml
experiment_id: ml_YYYYMMDD_001
data_version: ...
split_strategy: leave_cell_out
features_version: ...
model_family: ...
hyperparameters: ...
random_seed: ...
training_cells: [...]
validation_cells: [...]
test_cells: [...]
metrics: {...}
commit_sha: ...
```

## 8. Initial AI milestones

### AI-1
Train simple regressors for PyBaMM-generated voltage/temperature summary outputs. Purpose: validate the data and experiment pipeline, not publish novelty.

### AI-2
Generate a modest COMSOL electro-thermal DOE and compare GP, tree boosting and MLP surrogates for `T_max`, `ΔT`, voltage summary and heat generation.

### AI-3
Use active learning to reduce the number of new COMSOL runs required to reach a target surrogate error.

### AI-4
Build physics-informed SOH features and test leave-cell-out generalization on public ageing datasets.

### AI-5
Integrate the best validated surrogate into a constrained optimization loop and verify final candidates with fresh COMSOL simulations.