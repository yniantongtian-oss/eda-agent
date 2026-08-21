# Notebook policy

Notebooks are for exploration, visualization and interactive inspection. Publication-critical transformations and model runs should move into importable scripts under `src/` or versioned research scripts.

Rules:

- keep notebooks small,
- do not embed large datasets,
- clear accidental secrets/paths,
- record the config/manifest used for plotted results,
- move reusable functions into `battery_lab`,
- generate final paper figures from scripts when the result matures.

Suggested notebooks:

1. `01_pybamm_model_ladder.ipynb`
2. `02_parameter_sensitivity.ipynb`
3. `03_comsol_pybamm_comparison.ipynb`
4. `04_experiment_alignment.ipynb`
5. `05_surrogate_benchmark.ipynb`
6. `06_soh_rul_generalization.ipynb`
7. `07_digital_twin_replay.ipynb`
