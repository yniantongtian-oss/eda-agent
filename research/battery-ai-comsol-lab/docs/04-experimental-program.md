# Experimental program

## 1. Purpose

Experiments exist to answer a scientific question, identify parameters, validate models, or test a hypothesis. Every protocol must therefore state which model quantity or research claim it supports.

## 2. Experimental levels

### E0 — Instrument and fixture characterization

Before cell testing:

- current/voltage measurement verification,
- temperature-sensor verification,
- channel synchronization check,
- fixture/contact-resistance characterization,
- ambient/chamber stability check.

### E1 — Baseline capacity and efficiency

Typical outputs:

- charge/discharge capacity,
- energy,
- coulombic efficiency,
- energy efficiency,
- DC resistance estimates,
- temperature rise.

The exact voltage limits, rest times and current rates must come from the tested cell's legitimate specification and laboratory safety procedure.

### E2 — Dynamic pulse characterization

Purpose:

- ECM parameter identification,
- dynamic voltage validation,
- SOC-dependent resistance/time constants.

Record full current/voltage/temperature time series and the SOC initialization procedure.

### E3 — EIS

Purpose:

- impedance signatures,
- temperature/SOC dependence,
- ageing diagnostics,
- model discrimination.

Store frequency, real/imaginary impedance, amplitude, DC bias/SOC, temperature and instrument settings.

### E4 — GITT/PITT or relaxation-oriented tests

Purpose:

- diffusion/transport-related parameter inference,
- OCP/relaxation behavior,
- physics-model calibration.

### E5 — Thermal characterization

Possible measurements:

- surface temperature at multiple positions,
- chamber/ambient temperature,
- heat-flux/calorimetric data if suitable equipment is available,
- cooling/contact-condition metadata.

### E6 — Ageing matrix

Independent factors can include:

- temperature,
- C-rate,
- depth of discharge,
- SOC window,
- calendar storage SOC,
- charge protocol.

Do not build an enormous factorial matrix without power/identifiability planning. Start from the hypotheses and the model sensitivities.

## 3. Required test metadata

Every test run should have a manifest containing at least:

```yaml
test_id: cell001_baseline_001
cell_id: cell001
chemistry: LFP_graphite
format: cylindrical
manufacturer: null
model_number: null
lot_id: null
nominal_capacity_Ah: null
instrument_id: cycler01
fixture_id: fixtureA
ambient_control: chamber01
temperature_setpoint_C: 25.0
protocol_id: capacity_v1
operator: null
start_time_utc: ...
software_version: ...
notes: ...
```

Unknown values should remain `null`; never invent commercial-cell specifications.

## 4. Raw data policy

Raw instrument exports are immutable.

Recommended pipeline:

```text
raw/ → validated/ → processed/ → features/ → model-ready/
```

Rules:

- never overwrite raw files,
- preserve original timestamps,
- document unit conversions,
- flag rather than silently delete anomalies,
- store preprocessing version in every derived artifact.

## 5. Sensor synchronization

For electro-thermal comparison, timing errors can dominate apparent model error during transients.

Check:

- current/voltage sample clock,
- temperature channel latency,
- external DAQ clock alignment,
- chamber controller timestamps.

If synchronization is estimated post hoc, store the offset and method.

## 6. Replicates and cell-to-cell variability

Single-cell results should not automatically be generalized to a chemistry or cell family.

Where resources permit:

- use multiple cells per condition,
- randomize or block by lot/fixture/channel,
- report between-cell variation,
- avoid tuning a model to the same cell used for final validation.

## 7. Parameter-identification tests

Map parameters to evidence:

| Parameter family | Candidate evidence |
|---|---|
| Capacity / inventory | low-rate capacity, OCV/SOC characterization |
| ECM resistance/time constants | pulse tests, EIS |
| OCP | half-cell/reference data or trusted parameter sets |
| Diffusion-related | GITT/PITT, EIS, dynamic response with identifiability analysis |
| Thermal properties | literature/direct measurement + thermal transients |
| Heat generation | electro-thermal fit, calorimetry where available |
| Ageing parameters | multi-condition longitudinal ageing data |

## 8. Model validation datasets

Keep calibration and validation conditions separate.

A useful first design:

- calibration: 0.5C and 1C at 25 °C,
- validation: different C-rate and at least one different temperature,
- stress test: profile or boundary condition not used during calibration.

Exact conditions should be adapted to the cell specification and available equipment.

## 9. Experimental safety boundary

All cell testing must follow the battery/cell manufacturer's limits, institutional lab rules and equipment safety procedures. Abuse and thermal-runaway testing requires purpose-built facilities, trained personnel and dedicated risk controls; this repository does not provide instructions for initiating dangerous failure events.

## 10. First experimental package

The initial reproducible package should include:

1. cell registration form,
2. instrument/fixture registration,
3. baseline capacity protocol metadata,
4. pulse-test metadata,
5. multi-point temperature channel mapping,
6. raw-file checksum manifest,
7. preprocessing script,
8. PyBaMM/COMSOL comparison notebook or script,
9. uncertainty/error report.