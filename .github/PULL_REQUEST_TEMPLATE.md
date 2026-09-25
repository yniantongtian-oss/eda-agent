## Summary

What does this PR change, and why?

## Linked issue

Closes #

## Type of change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would change existing behaviour)
- [ ] Documentation only
- [ ] Refactor / chore (no behavioural change)
- [ ] Release / packaging / CI hardening

## Areas touched

- [ ] Python MCP server (`src/eda_agent/`)
- [ ] Altium bridge (`scripts/altium/`)
- [ ] KiCad backend
- [ ] EasyEDA Pro backend / extension (`extensions/easyeda/`)
- [ ] Packaging / release artifacts
- [ ] Tests / CI
- [ ] Docs / contributor support

## Testing

- [ ] Python 3.11 tests pass
- [ ] Python 3.12 tests pass
- [ ] `python -m compileall -q src tests scripts` passes
- [ ] Pascal cross-validation passes (if Pascal touched)
- [ ] Release artifact build + clean-wheel smoke test passes (if packaging changed)
- [ ] Manually exercised in the affected EDA application when behaviour requires
      live verification; describe what you ran below

Notes:

## Safety / compatibility checklist

- [ ] No secrets, customer designs, credentials, or proprietary library paths
      are included in the diff or test fixtures
- [ ] Public tool names / schemas remain compatible, or the breaking change is
      explicitly documented
- [ ] If a Pascal file changed, reviewers know Altium caches scripts and must
      reload/restart before live verification
- [ ] Destructive EDA operations retain confirmation/checkpoint guards where
      applicable
- [ ] User-facing docs and security policy remain consistent with the backends
      and version actually shipped
