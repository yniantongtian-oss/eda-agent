# Safety and thermal-runaway research boundary

## 1. Scope

This track is for **prediction, detection, prevention, containment and propagation mitigation**. It supports computational modeling and analysis of appropriately collected safety data.

This repository does not provide operational instructions for deliberately initiating thermal runaway, internal short circuits, overcharge abuse, puncture, crushing, heating-to-failure or other hazardous battery abuse tests. Such work requires dedicated facilities, trained personnel, institutional procedures and applicable standards.

## 2. Safe research questions

Examples:

- How does cell spacing affect modeled heat transfer between neighboring cells?
- Which cooling boundaries reduce peak temperature or propagation potential?
- Which measurable voltage/temperature/impedance residuals may act as early-warning indicators?
- How conservative is a reduced-order thermal model relative to a high-fidelity reference?
- How does uncertainty in thermal properties change predicted safety margins?
- Where should sensors be placed to improve detection coverage?

## 3. Modeling hierarchy

### S0 — normal-operation thermal envelope

Establish a validated normal-operation electro-thermal model before extrapolating toward abnormal conditions.

### S1 — externally specified conservative heat source

For propagation-oriented thermal studies, use documented/validated heat-release inputs or bounded source terms as data, rather than inventing reaction kinetics.

### S2 — calibrated reaction model

Only use reaction kinetics when parameters have defensible sources and the model is validated against appropriate safety data.

### S3 — module/pack propagation model

Study:

- heat conduction paths,
- cell spacing,
- barriers,
- cooling boundaries,
- enclosure effects,
- sensor placement,
- uncertainty bounds.

## 4. Required uncertainty reporting

Safety outputs should be conservative and explicit about uncertainty.

Track at minimum:

- thermal conductivity uncertainty,
- heat capacity uncertainty,
- contact resistance,
- convection/cooling uncertainty,
- source-term uncertainty,
- geometry/contact uncertainty.

Avoid presenting a single deterministic temperature threshold as universally predictive when the model/data do not support that precision.

## 5. Detection research

Candidate non-invasive signals:

- voltage residual,
- current/voltage consistency,
- surface temperature and rate of rise,
- spatial temperature gradient,
- impedance changes where available,
- gas/pressure signals only when suitable sensors and safe datasets exist.

Detection evaluation should report:

- false positive rate,
- false negative rate,
- detection lead time on the available dataset,
- robustness to sensor noise/failure,
- cross-cell generalization.

## 6. Sensor-placement optimization

This is a useful COMSOL + AI problem:

1. generate spatial thermal fields from validated or conservative scenarios,
2. define candidate sensor locations,
3. optimize coverage/observability,
4. validate against unseen scenarios,
5. report sensor-count vs detection-performance tradeoff.

## 7. Cooling and propagation mitigation

Possible design variables:

- inter-cell spacing,
- cooling-plate geometry,
- thermal interface properties,
- barrier materials represented by verified property data,
- coolant boundary conditions,
- enclosure conduction paths.

Objectives can include:

- peak neighboring-cell temperature,
- thermal gradient,
- time-integrated thermal exposure,
- pressure drop / cooling-energy proxy,
- mass/volume proxy.

## 8. Data policy

Safety datasets require the same provenance rules as normal cycling data plus:

- source/test facility,
- scenario label,
- instrumentation layout,
- sampling/synchronization details,
- censoring/missing-data notes,
- licensing/usage restrictions.

If data come from literature, preserve citation and do not infer undocumented test details.

## 9. Model validation language

Use calibrated wording:

- `matches the reference dataset within ...`
- `provides a conservative bound under the tested conditions`
- `has not been validated for ...`

Avoid broad claims such as `predicts thermal runaway` unless the model has appropriate multi-condition validation.

## 10. First safe project

**Thermal propagation susceptibility surrogate**

- Start from a validated normal-operation thermal model.
- Introduce a bounded external heat-source scenario from documented/reference data.
- Sweep spacing, boundary cooling and contact properties.
- Train an uncertainty-aware surrogate for neighboring-cell thermal exposure.
- Optimize mitigation variables under geometric/cooling constraints.
- Verify candidate designs with fresh high-fidelity simulations.

This produces publishable methodology without requiring hazardous experimental instructions.