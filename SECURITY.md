# Security Policy

## Supported versions

`eda-agent` is still alpha software. Security fixes target the current
development line and, until that line is tagged, the latest tagged release.
There are no LTS branches.

| Version | Supported |
| ------- | --------- |
| 0.5.x (current development line) | :white_check_mark: |
| 0.4.x (latest tagged release) | :white_check_mark: until 0.5.0 is released |
| < 0.4 | :x: |

After 0.5.0 is released, 0.4.x becomes unsupported unless a security advisory
explicitly says otherwise.

## Reporting a vulnerability

Please **do not** open a public GitHub issue or pull request for security
problems.

For this fork, email reports privately to **yniantongtian@163.com** with:

- A description of the issue and its impact
- Steps to reproduce, including a minimal MCP call sequence or protocol
  payload when relevant
- The affected `eda-agent` version and exact commit SHA if known
- The selected backend and EDA application/version involved
- Whether the issue also reproduces on the upstream `salitronic/eda-agent`
  repository
- Any suggested mitigation

You should receive an acknowledgement within 7 days. If the report is
confirmed, a fix will be prepared and released; coordinated disclosure timing
will be agreed with the reporter.

If the same vulnerability reproduces unchanged in upstream
`salitronic/eda-agent`, coordinate disclosure with the upstream project as well.
Do not substitute a public upstream issue for a private security report.

## Scope

In scope:

- The Python MCP server (`src/eda_agent/`)
- The Altium DelphiScript bridge (`scripts/altium/`) and its file-based IPC
- The KiCad backend and its KiCad IPC API integration
- The EasyEDA Pro backend, including the loopback WebSocket bridge and
  `extensions/easyeda/`
- The local web dashboard and other local control surfaces shipped by this
  repository
- Release/package integrity for the `eda-agent` Python distribution
- Fork-specific CI, packaging, EasyEDA delivery helpers, and release artifacts

Out of scope:

- Vulnerabilities in Altium Designer, KiCad, or EasyEDA Pro themselves: report
  those to the respective vendor/project
- Vulnerabilities in upstream Python packages: report those to their
  maintainers (this project will update dependency constraints when a fix is
  available)
- Issues that require an attacker who already has unrestricted interactive
  access to the same host user account and do not cross an additional trust
  boundary

## Threat model

`eda-agent` is designed as a **local automation service**, not a network-facing
multi-user service.

- The Altium backend uses a workspace directory under the user's profile for
  request/response IPC. Filesystem permissions are the trust boundary; the IPC
  protocol itself does not authenticate callers.
- The KiCad backend talks to KiCad's local IPC API. Enabling that API grants
  local automation access to the open design.
- The EasyEDA Pro backend listens on loopback and accepts the editor extension
  over a local WebSocket bridge. It is intentionally not hardened for hostile
  network exposure.
- The web dashboard is intended for loopback/local use only.

A caller that can reach one of these control paths may be able to modify the
open electronic design. Destructive operations have confirmation/checkpoint
guards where the backend supports them, but those guards are not a substitute
for access control.

Do not expose the workspace directory, MCP stdio transport, EasyEDA bridge, or
web dashboard to untrusted callers. Do not rebind local services to a public or
shared network interface without adding an authentication and authorization
layer appropriate to that environment.
