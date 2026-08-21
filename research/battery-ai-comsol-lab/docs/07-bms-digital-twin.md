# BMS and digital twin architecture

## 1. Objective

Build an online model that synchronizes with measured current, voltage and temperature, estimates hidden states, adapts selected parameters and reports uncertainty. The digital twin should be traceable back to validated offline physics models.

## 2. Layered architecture

```text
Sensors / test replay
        ↓
Data validation + time alignment
        ↓
State estimator
  ├─ SOC
  ├─ temperature states
  ├─ hysteresis / ECM states
  └─ selected physics states
        ↓
Parameter adaptation
  ├─ resistance
  ├─ capacity/SOH
  ├─ thermal coefficients
  └─ selected reduced-model parameters
        ↓
Prediction layer
  ├─ voltage
  ├─ temperature
  ├─ available power/energy
  └─ risk/anomaly indicators
        ↓
Uncertainty + diagnostics
```

## 3. Model ladder

### Online baseline: ECM

Use a Rint/Thevenin family model first to establish:

- sign convention,
- state update loop,
- parameter storage,
- estimator tests,
- runtime budget.

### Physics-informed online model

Candidate reduced models:

- SPM,
- SPMe,
- reduced thermal state model,
- learned surrogate derived from validated COMSOL/PyBaMM data.

### Hybrid correction

ML may learn:

- residual voltage correction,
- parameter maps vs SOC/temperature/SOH,
- anomaly score,
- uncertainty inflation.

Hybrid corrections must not silently violate physical bounds.

## 4. SOC estimation

Benchmarks to include:

- coulomb counting,
- OCV-corrected estimate where valid,
- EKF/UKF or ensemble alternatives,
- physics-based estimator.

Report:

- initial-state sensitivity,
- sensor-bias sensitivity,
- temperature dependence,
- dynamic-profile error.

## 5. SOH estimation

State variables can include:

- usable capacity,
- DC/internal resistance,
- model parameters associated with degradation,
- uncertainty/confidence.

Avoid defining SOH as a single universal number without stating the operational definition.

## 6. Online parameter adaptation

Adapt only parameters with sufficient observability in the available signal window.

Possible strategies:

- recursive least squares for ECM terms,
- dual Kalman filtering,
- moving-horizon estimation,
- Bayesian/ensemble updates,
- constrained optimization.

Guardrails:

- physical bounds,
- rate-of-change limits,
- observability check,
- fallback to prior when data quality is poor.

## 7. Thermal digital twin

A reduced thermal model should be calibrated against 3D/experimental temperature behavior and preserve:

- average temperature,
- hotspot estimate or conservative bound,
- cooling-boundary dependence,
- sensor-location mapping.

The reduced model can use RC thermal networks, modal/POD models or a validated ML surrogate.

## 8. Fault and anomaly indicators

Potential indicators:

- model residual growth,
- unexpected resistance jump,
- temperature residual/local gradient anomaly,
- imbalance across parallel/series cells,
- sensor inconsistency,
- uncertainty explosion.

An anomaly score should be tied to interpretable residuals and thresholds whenever possible.

## 9. Pack-level twin

At pack scale, include:

- cell electrical topology,
- cell-to-cell parameter variation,
- balancing state,
- thermal neighborhood/cooling zone,
- current-sharing effects,
- sensor placement.

`liionpack` is a useful open baseline for electrical pack simulation; high-fidelity thermal behavior can be supplied by reduced models derived from COMSOL studies.

## 10. API contract

A future online twin interface should resemble:

```python
state = twin.initialize(config)
state = twin.step(
    dt_s=0.1,
    current_A=12.3,
    voltage_V=3.29,
    temperatures_K={"surface_mid": 301.2},
)

prediction = twin.predict(horizon_s=30)
health = twin.health()
```

Returned objects should expose estimate, uncertainty and diagnostic flags.

## 11. Validation

Use replay datasets with known timestamps. Evaluate:

- SOC error,
- voltage prediction error,
- temperature prediction error,
- SOH/capacity error,
- runtime per step,
- uncertainty calibration,
- recovery from bad/missing sensors.

## 12. First implementation milestones

1. ECM + coulomb-counting baseline.
2. EKF/UKF SOC estimator.
3. temperature-dependent ECM parameter map.
4. PyBaMM-generated synthetic validation.
5. measured-data replay.
6. reduced thermal model calibrated to COMSOL.
7. SOH parameter adaptation.
8. pack-level cell-variation simulation.
9. uncertainty-aware hybrid residual model.