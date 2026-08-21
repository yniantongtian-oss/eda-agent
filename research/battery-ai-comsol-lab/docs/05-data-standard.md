# Battery research data standard

## 1. Goal

Use one data contract across experiment, PyBaMM, COMSOL, ML and digital-twin workflows so results can be compared without repeatedly guessing units, sign conventions or provenance.

## 2. Core identifiers

Every record should be joinable through explicit identifiers:

- `project_id`
- `cell_id`
- `test_id` or `simulation_id`
- `protocol_id`
- `parameter_set_id`
- `geometry_id` where relevant
- `model_id`
- `data_version`

## 3. Sign conventions

The project must declare one current convention and convert all inputs at ingestion boundaries.

Recommended canonical convention for stored measurement data:

- `current_A > 0`: discharge
- `current_A < 0`: charge

If an upstream solver uses the opposite convention, the adapter must document and convert it.

## 4. Canonical units

Store SI units in canonical processed data unless a field explicitly encodes another unit.

Examples:

- time: `s`
- current: `A`
- voltage: `V`
- temperature: `K` in solver-facing data, with optional `temperature_C` for human-facing exports
- capacity: `Ah`
- energy: `Wh` or SI Joule where required by the calculation layer; name the unit explicitly
- resistance: `ohm`
- pressure: `Pa`
- length: `m`

Never use an unlabeled `temperature`, `capacity`, or `resistance` column.

## 5. Time-series schema

Minimum processed cycling schema:

```text
time_s
current_A
voltage_V
temperature_K
capacity_throughput_Ah
energy_throughput_Wh
soc_estimate          optional
step_index            optional
cycle_index           optional
```

Additional sensor temperatures should use stable names such as:

```text
temperature_surface_mid_K
temperature_positive_tab_K
temperature_negative_tab_K
ambient_temperature_K
```

## 6. Simulation output schema

Simulation records should include run-level metadata plus tidy time series.

Run manifest example:

```yaml
simulation_id: sim_20260821_001
engine: pybamm
engine_version: ...
model_id: DFN_lumped_thermal
parameter_set_id: lfp_baseline_v1
geometry_id: null
protocol_id: discharge_1C
commit_sha: ...
config_sha256: ...
status: completed
warnings: []
```

For COMSOL:

```yaml
engine: comsol
comsol_version: ...
model_file_sha256: ...
study: study1
mesh_id: fine_v2
```

## 7. Field data

Large 2D/3D fields should not be flattened into ordinary CSV unless small.

Preferred options:

- HDF5,
- Zarr,
- NetCDF/xarray-compatible structures,
- solver-native files plus standardized reduced exports.

Record coordinates, units, field names and time/SOC state explicitly.

## 8. Data layers

```text
data/
├─ raw/          # immutable instrument/source files; normally gitignored
├─ validated/    # schema-checked, minimally transformed
├─ processed/    # normalized units/sign/time, analysis-ready
├─ features/     # derived features for ML/statistics
├─ external/     # public datasets + source manifest, normally not committed wholesale
└─ manifests/    # small provenance/metadata files suitable for Git
```

## 9. Public dataset registry

For external datasets, store a registry record rather than silently copying files:

```yaml
dataset_id: example_public_dataset
source_url: ...
citation: ...
license: ...
download_date: ...
checksum: ...
local_path: data/external/example_public_dataset
notes: ...
```

## 10. Quality flags

Do not delete questionable points by default. Use flags:

- `ok`
- `missing`
- `sensor_dropout`
- `out_of_range`
- `time_discontinuity`
- `manual_review`
- `excluded_with_reason`

Derived datasets should carry the exclusion rule and software version.

## 11. Train/validation/test metadata

ML-ready records must include group identifiers needed to prevent leakage:

- cell ID,
- lot/batch ID when known,
- protocol ID,
- temperature condition,
- cycle index,
- timestamp/order.

Splits should be materialized as versioned manifests, not recreated randomly each run.

## 12. Data checks

Automated checks should cover:

- monotonic time within a segment,
- finite voltage/current values,
- physically plausible temperature bounds for the declared test context,
- no duplicated `(test_id, time_s)` after normalization,
- consistent current sign convention,
- unit/schema validation,
- required metadata presence.

Out-of-range thresholds should be configurable and traceable to the experiment/model context.

## 13. Provenance

Every derived dataset or model result should answer:

- where did the source data come from?
- what code transformed it?
- which parameters/config were used?
- which commit produced it?
- what was excluded and why?
- what are the units and sign conventions?

If those questions cannot be answered, the artifact is exploratory rather than publication-grade.