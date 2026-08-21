# Paper reproduction registry

Each paper/research claim reproduced in this lab should get its own folder with explicit provenance.

```text
papers/<paper-id>/
├─ citation.md
├─ question.md
├─ methods.md
├─ source-links.md
├─ configs/
├─ scripts/
├─ expected-results.md
├─ reproduction.md
└─ discrepancies.md
```

## Reproduction levels

- **R0 — read/annotate:** equations, parameters, assumptions and missing details extracted.
- **R1 — qualitative:** trends reproduced.
- **R2 — quantitative:** reported metrics/curves reproduced within stated tolerance.
- **R3 — independent validation:** method tested on conditions/data not used in the paper.

Record discrepancies rather than tuning undocumented parameters until a figure visually matches.

Priority literature themes:

- DFN/SPM/SPMe model reduction,
- electro-thermal coupling,
- parameter identification/identifiability,
- degradation mechanism models,
- fast charging,
- thermal management,
- SOH/RUL generalization,
- physics-informed ML and surrogate modeling,
- battery digital twins.