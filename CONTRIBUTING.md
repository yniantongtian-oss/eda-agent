# Contributing to eda-agent

Thanks for your interest. `eda-agent` is an early-stage MCP server for live EDA
automation. The default and most complete backend is Altium Designer through a
DelphiScript bridge; KiCad and EasyEDA Pro are optional backends with their own
native/local integration paths.

Keep non-trivial changes focused and explain the user-visible problem before the
implementation. If Issues are enabled on the repository you are contributing
to, use an issue for architecture-level proposals first. On forks where Issues
are disabled, a narrowly scoped pull request with a clear problem statement is
preferred over an undocumented architectural rewrite.

## Ground rules

- Be respectful. See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
- Security-sensitive issues do **not** go in public issues or PRs. See
  [`SECURITY.md`](SECURITY.md).
- By contributing you agree your contribution is licensed under Apache-2.0.
- Do not include customer designs, credentials, private library paths, or other
  proprietary material in fixtures, logs, screenshots, or examples.

## Development environment

Required for the Python/offline suite:

- Python 3.11 or 3.12 (both are continuously tested in CI)
- `pip install -e .[dev]` from the repository root

Required for the full Altium path:

- Windows 10 / 11
- A licensed Altium Designer installation
- The bundled DelphiScript project installed with `eda-agent install-scripts`

Backend-specific optional setup:

- KiCad 9+ with its API server enabled, plus `pip install -e .[kicad,dev]`
- EasyEDA Pro with the extension under `extensions/easyeda/` imported and its
  external-interaction permission enabled
- Free Pascal (`fpc`) for the Pascal/Python cross-validation tests

The full supported CI runtime is Windows because the Altium bridge requires it.
Some backend-neutral, KiCad, and EasyEDA code is platform-neutral, but this
repository does not claim an additional operating system as release-certified
until CI explicitly tests it.

## Running the agent locally

Install the development package first:

```bash
pip install -e .[dev]
eda-agent --version
```

Select one backend per MCP server process:

```bash
eda-agent --backend altium
eda-agent --backend kicad
eda-agent --backend easyeda
```

For Altium:

1. Run `eda-agent install-scripts`.
2. In Altium, load `Altium_API.PrjScr` and run
   `Dispatcher > StartMCPServer`.
3. Connect your MCP client to the local `eda-agent` stdio server.
4. Use `eda-agent doctor` when diagnosing a bridge/setup problem.

For KiCad, enable **Preferences > Plugins > KiCad API server** before connecting.
For EasyEDA Pro, import the shipped extension, enable external interaction for
extensions/scripts, open a design tab, and let the extension connect to the
local loopback bridge.

See [`docs/BACKENDS.md`](docs/BACKENDS.md) for the backend-specific contract and
known limitations.

## Tests

Before requesting review, run the same basic gates CI runs:

```bash
python -m compileall -q src tests scripts
python -m pytest tests/ -q
python scripts/altium/lint.py
python scripts/altium/build.py
```

Free Pascal makes `tests/test_cross_validate.py` exercise the compiled Pascal
helpers rather than skipping that part of the suite.

**A normal test run must not touch a live EDA design.** Live integration checks
must remain explicitly opt-in. For Altium, `EDA_AGENT_INTEGRATION=1 pytest`
enables the live-Altium integration suite; without that environment variable the
integration directory is collection-gated so fixtures cannot open or modify a
real project accidentally.

The integration suite is intentionally read-only. A test that would mutate a
live design is rejected by the non-destructive integration guard. Verification
that must modify something belongs in `docs/RELEASE_VERIFICATION.md`, should use
a disposable/copy project, and should checkpoint before destructive operations.

The Pascal scripts cannot be fully unit-tested without a running Altium
instance. The linter, bundle build, and Free Pascal cross-validation are the
pre-Altium checks; the release verification document records the live checks
that still require the real DelphiScript engine.

## Release artifact verification

An editable install can pass while the wheel users receive is incomplete. CI
therefore builds the real wheel and source distribution and runs:

```bash
python scripts/verify_distribution.py
```

The verifier checks package metadata, the console entry point, required
LICENSE/NOTICE files, and the bundled Altium scripts. CI then installs the wheel
into a clean virtual environment and smoke-tests `eda-agent --version`,
`eda-agent --help`, and `eda-agent scripts-path`.

If this gate fails, fix the package. Do not weaken the verifier merely to make a
release green.

## Writing a guard

A good part of this suite is guards: tests that compare a fact stated in one
place against the code that decides it, because the two drift and nothing else
notices. Four practices have caught real mistakes here and are worth copying.

**Mutate the defect it exists to catch.** A guard that has never failed has not
been tested. Break the thing on purpose, confirm the guard fails, put it back.
Several guards in this suite passed on their first run while checking nothing,
and only mutation found that.

**Assert the check found something.** If the guard parses a table, a document or
a registry, assert the parse was non-empty and roughly the expected size. A
renamed heading otherwise turns the guard into a test that passes because it
read zero rows. Existing examples include
`test_the_scan_sees_what_it_claims_to`,
`test_the_widened_scan_actually_sees_something`, and
`test_the_check_can_actually_fail`.

**Do not let the guard match its own explanation.** If it searches for a literal
and a nearby comment names that literal, the comment can satisfy the search.
Build awkward sentinel characters programmatically or otherwise exclude the
explanation from the scan.

**Prefer behaviour to literals, and remember a count cannot see a name.** A
behavioural conversion test is stronger than two constants that can drift in
the same way. A tool-count test is not enough to prove documentation names real
tools, which is why this repository also carries name-resolution guards.

The security-policy version guard follows the same rule: bumping the package
minor line without updating `SECURITY.md` must fail CI rather than silently
publishing stale support information.

## Pull requests

- Keep PRs focused. One concern per PR when practical.
- Include a clear description of the problem, chosen approach, and safety
  implications.
- State the affected backend(s): Altium, KiCad, EasyEDA Pro, or backend-neutral.
- Add or update tests when behaviour changes.
- Keep public tool names/schemas backward compatible unless the PR explicitly
  documents a breaking change.
- If you touch Pascal, remember that Altium caches scripts; live reviewers must
  reload/restart before verifying the change.
- If you touch release/build logic, the package-artifact job must pass from a
  clean wheel, not just an editable checkout.

The pull-request template contains the current delivery checklist and should be
completed rather than deleted for substantial changes.

## Commit messages

Write the subject as a plain imperative sentence saying what the commit changes,
wrapping the body at about 72 columns:

```text
Keep the test suite away from the machine-global workspace pointer

Longer body if needed: what was wrong, and why this is the fix.
```

Do not use a `type(scope):` prefix. Do not create standalone housekeeping
commits when the cleanup is an inseparable part of the substantive change.

## Reporting bugs

Use [`.github/ISSUE_TEMPLATE/bug_report.md`](.github/ISSUE_TEMPLATE/bug_report.md)
when Issues are enabled. Include the selected backend, `eda-agent --version`,
Python/OS information, the EDA application/version, MCP client, and the smallest
redacted backend-specific diagnostic that reproduces the failure.

Security-sensitive reports must follow [`SECURITY.md`](SECURITY.md) instead of a
public issue.

## Suggesting features

Use [`.github/ISSUE_TEMPLATE/feature_request.md`](.github/ISSUE_TEMPLATE/feature_request.md)
when Issues are enabled, or carry the same information into a focused PR when
they are not. Concrete workflows, the target backend, relevant vendor/API
surface, and safety requirements are more useful than speculative tool names.
