# Data workspace

Large/raw battery datasets are intentionally not committed to normal Git history.

Use:

```text
data/
├─ raw/
├─ validated/
├─ processed/
├─ features/
├─ external/
└─ manifests/
```

## Rules

- `raw/` is immutable.
- Every external dataset gets a source/license/citation/checksum manifest.
- Every processed dataset records the preprocessing version.
- Split manifests for ML are versioned so cross-cell evaluation can be reproduced.
- Use Git LFS or an external dataset/artifact store for large files.
- Never commit proprietary or license-restricted data without authorization.

See `../docs/05-data-standard.md` for the canonical schema and sign/unit conventions.