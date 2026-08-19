---
name: Bug report
about: Report a defect in the MCP server or an EDA backend
title: "[bug] "
labels: bug
assignees: ''
---

## Summary

A clear, one-paragraph description of what is wrong.

## Steps to reproduce

1.
2.
3.

## Expected behaviour

What you expected to happen.

## Actual behaviour

What actually happened. Paste error messages verbatim inside fenced code
blocks.

## Environment

- `eda-agent` version: <output of `eda-agent --version`>
- Python version: <output of `python --version`>
- Backend: <altium / kicad / easyeda / both>
- EDA application and version: <Altium Designer / KiCad / EasyEDA Pro>
- Operating system and version:
- MCP client (Claude Code / Codex / Claude Desktop / other):
- Toolset, if non-default: <full / minimal>

## Diagnostics

Include the smallest backend-specific evidence that reproduces the problem.
Redact proprietary paths, design data, credentials, and customer information.

- Altium: relevant workspace response / `last_fault.json`, plus whether the
  polling loop was running
- KiCad: the failing tool response and whether the KiCad API server was enabled
- EasyEDA Pro: the failing tool response, active editor tab, and whether the
  extension reported connected

```text
paste diagnostics here
```

## Additional context

Logs, screenshots, related issues, and whether the problem reproduces after a
fresh `eda-agent doctor` / reconnect where applicable.
