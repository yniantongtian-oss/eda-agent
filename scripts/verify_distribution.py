# SPDX-License-Identifier: Apache-2.0
"""Verify that release artifacts are complete and internally consistent.

This intentionally uses only the Python standard library so it can run after
``python -m build`` without adding another release-time dependency.
"""

from __future__ import annotations

import email
import sys
import tarfile
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def _exactly_one(pattern: str) -> Path:
    matches = sorted(DIST.glob(pattern))
    if len(matches) != 1:
        raise AssertionError(
            f"expected exactly one {pattern!r} artifact in {DIST}, found: "
            f"{[p.name for p in matches]}"
        )
    return matches[0]


def _has_suffix(names: set[str], suffix: str) -> bool:
    suffix = suffix.replace("\\", "/")
    return any(name.replace("\\", "/").endswith(suffix) for name in names)


def _require_suffixes(kind: str, names: set[str], suffixes: tuple[str, ...]) -> None:
    missing = [suffix for suffix in suffixes if not _has_suffix(names, suffix)]
    if missing:
        raise AssertionError(f"{kind} is missing required files: {missing}")


def _project_metadata() -> tuple[str, str]:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]
    return str(project["version"]), str(project["requires-python"])


def verify_wheel(wheel: Path, version: str, requires_python: str) -> None:
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        _require_suffixes(
            "wheel",
            names,
            (
                "eda_agent/scripts/Altium_API.PrjScr",
                "eda_agent/scripts/Dispatcher.pas",
                "eda_agent/scripts/Main.pas",
                "eda_agent/easyeda_extension/BUILD_STAMP.json",
                "eda_agent/easyeda_extension/build.py",
                "eda_agent/easyeda_extension/extension.json",
                "eda_agent/easyeda_extension/main.js",
                "eda_agent/easyeda_extension_cli.py",
                ".dist-info/METADATA",
                ".dist-info/entry_points.txt",
                "/LICENSE",
                "/NOTICE",
            ),
        )

        metadata_name = next(
            name for name in names if name.endswith(".dist-info/METADATA")
        )
        metadata = email.message_from_bytes(archive.read(metadata_name))
        if metadata.get("Version") != version:
            raise AssertionError(
                f"wheel metadata version {metadata.get('Version')!r} != {version!r}"
            )
        if metadata.get("Requires-Python") != requires_python:
            raise AssertionError(
                "wheel Requires-Python "
                f"{metadata.get('Requires-Python')!r} != {requires_python!r}"
            )

        entry_points_name = next(
            name for name in names if name.endswith(".dist-info/entry_points.txt")
        )
        entry_points = archive.read(entry_points_name).decode("utf-8")
        expected_entries = (
            "eda-agent = eda_agent.server:main",
            "eda-agent-easyeda-extension = eda_agent.easyeda_extension_cli:main",
        )
        missing_entries = [entry for entry in expected_entries if entry not in entry_points]
        if missing_entries:
            raise AssertionError(
                f"wheel console entry points are missing: {missing_entries}"
            )


def verify_sdist(sdist: Path) -> None:
    with tarfile.open(sdist, "r:gz") as archive:
        names = set(archive.getnames())
        _require_suffixes(
            "sdist",
            names,
            (
                "/README.md",
                "/LICENSE",
                "/NOTICE",
                "/pyproject.toml",
                "/scripts/altium/Altium_API.PrjScr",
                "/scripts/altium/Dispatcher.pas",
                "/extensions/easyeda/BUILD_STAMP.json",
                "/extensions/easyeda/build.py",
                "/extensions/easyeda/extension.json",
                "/extensions/easyeda/main.js",
                "/src/eda_agent/easyeda_extension_cli.py",
                "/src/eda_agent/server.py",
            ),
        )


def main() -> int:
    if not DIST.is_dir():
        raise AssertionError(f"distribution directory does not exist: {DIST}")

    version, requires_python = _project_metadata()
    wheel = _exactly_one("*.whl")
    sdist = _exactly_one("*.tar.gz")

    verify_wheel(wheel, version, requires_python)
    verify_sdist(sdist)

    print(
        "distribution verification passed: "
        f"{wheel.name}, {sdist.name}, version={version}, "
        f"requires-python={requires_python}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"distribution verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
