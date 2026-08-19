# SPDX-License-Identifier: Apache-2.0
"""Keep the public security policy aligned with the shipped project metadata."""

from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _project_version() -> str:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return str(pyproject["project"]["version"])


def test_security_policy_names_current_version_line():
    version = _project_version()
    parts = version.split(".")
    assert len(parts) >= 2, f"unexpected project version: {version!r}"
    series = f"{parts[0]}.{parts[1]}.x"

    policy = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    assert f"| {series} (current development line) |" in policy, (
        f"SECURITY.md does not mark {series} as the current development line; "
        "update the supported-version policy when bumping the package version"
    )


def test_security_policy_covers_every_backend_and_no_removed_installer():
    policy = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    for backend in ("Altium", "KiCad", "EasyEDA"):
        assert backend in policy, f"SECURITY.md does not cover the {backend} backend"

    assert "installer/" not in policy, (
        "SECURITY.md still scopes a removed installer/ tree; keep the policy "
        "tied to surfaces that actually ship"
    )
