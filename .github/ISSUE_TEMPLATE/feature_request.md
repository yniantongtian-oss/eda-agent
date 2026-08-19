---
name: Feature request
about: Propose a new tool, capability, or workflow
title: "[feature] "
labels: enhancement
assignees: ''
---

## Use case

What are you trying to accomplish? Describe the design or automation workflow
that needs this. Concrete examples are far more useful than speculative API
additions.

## Target backend

- [ ] Backend-agnostic / design-agent layer
- [ ] Altium Designer
- [ ] KiCad
- [ ] EasyEDA Pro
- [ ] More than one backend

## Proposed solution

What should the new tool / parameter / behaviour look like? Include a sketch of
the MCP tool signature if you can.

```text
proposed_tool(arg1: str, arg2: int) -> dict
```

## Alternatives considered

Existing tools you tried, workarounds you rejected, and why.

## Relevant EDA API surface

If you know the relevant Altium DelphiScript, KiCad IPC, or EasyEDA Pro API
(interface/class/method and documented limitations), link to the reference or
paste the smallest useful snippet. For backend-agnostic work, identify the
existing snapshot/plan/tool contract that is closest.

## Safety and compatibility

Could the proposed capability delete, overwrite, route, import, synchronize, or
otherwise make a hard-to-reverse design change? If so, describe the confirmation
or checkpoint behaviour you expect.

## Additional context

Datasheets, mockups, links to related issues, and example projects with
proprietary details removed.
