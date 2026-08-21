# Experiment workspace

This directory stores **protocol definitions, manifests, calibration notes and analysis scripts**. Raw instrument files belong under the gitignored data workspace or an external data store.

Recommended layout:

```text
experiments/
├─ protocols/
├─ cells/
├─ instruments/
├─ fixtures/
├─ runs/
└─ analysis/
```

## First protocol set

- baseline capacity/energy characterization,
- dynamic pulse characterization,
- temperature-mapped constant-current cycles,
- EIS metadata template,
- GITT/PITT metadata template where suitable equipment and expertise exist,
- longitudinal ageing matrix.

Actual operating limits must come from the tested cell specification and laboratory safety procedures. Do not infer them from the generic simulation baseline.

See `../docs/04-experimental-program.md`.