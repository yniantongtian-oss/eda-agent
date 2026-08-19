# Delivery acceptance

This document defines what “delivery-ready” means for this repository. It is
intentionally stricter than “the source tree passed pytest” and intentionally
more precise than claiming every live EDA path has been exercised.

## Deliverable identity

The Python package version is declared in `pyproject.toml`. A delivery must be
traceable to one exact Git commit SHA and to CI results for that same SHA.

For version 0.5.0, the release candidate is acceptable only when all automated
gates below pass on the exact commit that will be delivered. Do not rebuild from
a different checkout and call it the same verified artifact.

## Automated acceptance gates

The `tests` GitHub Actions workflow is the automated source of truth. A
release-candidate commit must have all three jobs green:

1. **Python 3.11**: editable development install, whole-tree Python bytecode
   compilation, DelphiScript lint, Pascal bundle consistency, Free Pascal
   cross-validation, and the complete pytest suite.
2. **Python 3.12**: the same gate on the second advertised Python runtime.
3. **Package**: build the actual wheel and source distribution, verify package
   metadata and required files, install the wheel into a clean virtual
   environment, exercise the shipped console entry points, build the EasyEDA
   `.eext` from the installed wheel, generate SHA-256 checksums, and upload the
   verified artifacts.

A failure in any one of these jobs blocks delivery. Do not waive a failing gate
by deleting or skipping the check. Fix the source, packaging, documentation, or
verification logic that exposed the failure.

## What the downloadable artifact must contain

A successful package job uploads one immutable Actions artifact named
`eda-agent-dist-<commit-sha>` containing:

- the `.whl` built from that commit;
- the `.tar.gz` source distribution built from that commit;
- `eda-agent-bridge.eext`, built by the EasyEDA helper installed from that
  wheel; and
- `SHA256SUMS.txt` with the SHA-256 digest of all three deliverable files.

`scripts/verify_distribution.py` additionally checks that the wheel contains
its metadata, both console entry points, LICENSE, NOTICE, the bundled Altium
DelphiScript project, and the complete EasyEDA extension source/build payload.
The sdist must contain the corresponding source/release files as well.

To verify a downloaded bundle, compute SHA-256 for the wheel, sdist, and `.eext`
and compare the lowercase hexadecimal values with `SHA256SUMS.txt` before
installation/import.

## Clean-install acceptance

The package job creates a new virtual environment and installs the built wheel,
not the source checkout. The following must succeed from that installed wheel:

```text
eda-agent --version
eda-agent --help
eda-agent scripts-path
eda-agent-easyeda-extension path
eda-agent-easyeda-extension build --dest <writable-directory>
```

The path returned by `scripts-path` must exist. The EasyEDA source path must also
exist, and the build command must create a non-empty `eda-agent-bridge.eext` in
the writable destination. This proves both editor-side payloads are reachable
from an actual wheel installation rather than only from the repository checkout.

The EasyEDA build intentionally uses the canonical `extensions/easyeda/build.py`
logic and therefore requires Node.js for its function-body parse validation. CI
runs that exact build path before publishing the `.eext` artifact.

## Live EDA acceptance boundary

Automated CI cannot prove that vendor/editor-specific runtime behavior works in
an interactive installed editor. Do not describe CI success as proof that every
Altium, KiCad, or EasyEDA Pro command has been exercised live.

### Altium Designer

Before a production handoff that depends on Altium mutation paths, run the
applicable steps in [`RELEASE_VERIFICATION.md`](RELEASE_VERIFICATION.md) against
a disposable/copy project. That document records the checks that specifically
need Altium’s DelphiScript engine and visual/editor behavior rather than Free
Pascal or mocks.

At minimum, confirm:

- `app_ping` reports the expected Python and Altium script versions;
- the Altium self-test reports zero failures;
- the workflow-specific mutation/readback checks used by the delivery have been
  exercised on a copy or behind an application checkpoint; and
- any remaining item marked as not verified live is disclosed rather than
  silently treated as verified.

### KiCad

For a delivery that depends on KiCad, enable the KiCad API server in the target
KiCad version, connect with `EDA_AGENT_BACKEND=kicad`, and exercise the exact
read/mutation/export workflow being handed off on a disposable project. Record
KiCad version and the commands exercised in the delivery notes.

### EasyEDA Pro

For a delivery that depends on EasyEDA Pro, import the shipped
`eda-agent-bridge.eext`, enable external interaction, open the relevant design
document, connect to the local loopback bridge, and exercise the exact commands
needed by the handoff. Respect the backend’s per-command `verified_live`
reporting; a successful connection is not evidence that every API command was
live-verified.

See [`BACKENDS.md`](BACKENDS.md) for backend-specific limitations and safety
behavior.

## Security acceptance

The public `SECURITY.md` must name the current package development line and all
backends that actually ship. CI contains a guard that fails when the package
minor version moves without the security policy moving with it.

The product is designed for local trusted-user automation. Do not expose its
MCP stdio endpoint, Altium workspace IPC, EasyEDA bridge, or local dashboard to
untrusted/network callers without a separate authentication and authorization
layer.

## Handoff record

A complete handoff record should contain:

- repository and exact Git commit SHA;
- package version;
- link/name of the successful CI run;
- downloaded artifact name;
- SHA-256 values from `SHA256SUMS.txt`;
- target OS/Python and selected backend;
- target EDA application/version;
- live acceptance steps performed, if the delivery depends on live editor
  behavior; and
- any known limitation or live-unverified path relevant to the recipient’s
  workflow.

When those facts are recorded, another person can reproduce what was delivered
and distinguish automated evidence from live-editor evidence.
