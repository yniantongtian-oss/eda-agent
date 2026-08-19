# eda-agent bridge for EasyEDA Pro

This is the editor half of the EasyEDA Pro backend. The Python MCP server
listens locally; this extension runs inside EasyEDA Pro and connects back to
it. Both halves are required.

## Install from a source checkout

Build the extension package from the repository root:

```bash
python extensions/easyeda/build.py
```

The build creates:

```text
extensions/easyeda/eda-agent-bridge.eext
```

In EasyEDA Pro, open **Settings > Extensions** and import that `.eext` file.
EasyEDA installs a file, not the source directory.

The build is deliberately small but strict. `main.js` has no imports, so the
entry point can be produced without a JavaScript bundler. The build script:

- stamps the source build id;
- refuses source changes that were not accompanied by an extension-version
  bump when EasyEDA would otherwise silently keep the old installed version;
- strips ES-module export keywords because EasyEDA parses the entry as an
  `AsyncFunction` body rather than importing it as a module;
- asks Node.js to compile the generated entry using that function-body shape;
  and
- creates the `.eext` archive with `extension.json` at its root and the built
  `dist/index.js` at the path named by the manifest.

Node.js is therefore required for the build-time parse validation.

## Install from an eda-agent wheel

The wheel contains the complete EasyEDA extension source/build payload. After
installing `eda-agent`, build a writable copy with:

```bash
eda-agent-easyeda-extension build --dest easyeda-extension
```

Then import:

```text
easyeda-extension/eda-agent-bridge.eext
```

To locate the read-only payload bundled inside the installed package:

```bash
eda-agent-easyeda-extension path
```

Do not build directly inside `site-packages`; the helper copies the payload to
the writable destination first. In an editable development install, the same
command automatically uses the repository's `extensions/easyeda/` source tree.

The repository CI performs this exact wheel-installed build before publishing
its verified delivery artifact, so a successful package job includes a ready
`eda-agent-bridge.eext` alongside the wheel, source distribution and SHA-256
checksums.

## Connecting

Start the MCP server with the EasyEDA backend selected, for example:

```bash
eda-agent --backend easyeda
```

The extension connects on load. The **eda-agent** menu on PCB and schematic
pages also provides **Connect** and **Disconnect** for reconnecting after the
server restarts.

By default the Python side listens on the first free loopback port in
`49620-49629`. The extension scans that range and, when `fetch` is available,
checks `GET /health` for the `eda-agent-bridge` service identity before opening
the WebSocket command channel. It retries, so server/editor start order does
not need to be coordinated.

`EDA_AGENT_EASYEDA_HOST` and `EDA_AGENT_EASYEDA_PORT` can pin the Python side
when a fixed local endpoint is required. The intended deployment is loopback;
this protocol is not hardened for hostile or public networks.

EasyEDA may require its external-interaction permission for extensions and
standalone scripts before it will attempt the connection. Also open a PCB or
schematic design tab: project-home, settings, library and other non-design tabs
do not expose the same runtime API surface.

## Protocol

The server sends:

```text
{id, command, params}
```

The extension answers:

```text
{id, result}
```

or:

```text
{id, error}
```

Requests are correlated by id so a slow response cannot be mistaken for the
answer to a later call. The envelope is created centrally in `main.js`; tests
also check that Python command names, extension handlers, manifest registration
and the build entry point stay aligned.

## Verification model

Static/offline checks and live-editor verification are deliberately reported as
different evidence.

The extension and Python backend mechanically check command names, handler
parameters, documented API method usage, transport framing, build/manifest
consistency and destructive-command guards. Those checks catch protocol and
integration-contract mistakes without claiming that an editor accepted a call.

Live EasyEDA Pro sessions are recorded per command. The Python backend reads the
measurement record and reports `verified_live` for the command actually used.
Some commands have live round-trip evidence; commands without such evidence
remain `verified_live: false`. A successful connection or one verified command
does not promote the rest of the backend to verified.

Use the backend's measured-shape/verification tools before depending on a reply
field whose runtime shape matters, and disclose `verified_live: false` paths in
a production handoff rather than treating them as proven.

## Units and layers

The public MCP tools use mils. EasyEDA's PCB and schematic canvases do not use
the same native scale, so the Python backend owns the schematic conversion in
one place instead of asking callers to know editor-specific units.

Layers cross the bridge by name, not by copied numeric ids. For example,
`TOP`, `BOTTOM`, `TOP_SILKSCREEN` and `BOARD_OUTLINE` are resolved against the
runtime's own layer enum. This avoids quietly placing geometry on the wrong
layer when numeric enum values differ.

## Destructive operations

Commands that can remove, rewrite, route, import or otherwise discard work are
confirmation-gated. The important checks are implemented on both sides where a
reflective/invoke path could otherwise bypass a named-tool guard.

Use `easyeda_checkpoint` before a destructive workflow. The EasyEDA checkpoint
protects the open document; it is not a project-directory snapshot like the
Altium checkpoint mechanism.

For the current backend capability matrix, known limitations and live
verification semantics, see [`../../docs/BACKENDS.md`](../../docs/BACKENDS.md).
For delivery acceptance requirements, see
[`../../docs/DELIVERY_ACCEPTANCE.md`](../../docs/DELIVERY_ACCEPTANCE.md).
