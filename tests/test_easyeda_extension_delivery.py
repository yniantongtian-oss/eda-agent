# SPDX-License-Identifier: Apache-2.0
"""Delivery guards for the EasyEDA editor half shipped with eda-agent."""

from __future__ import annotations

from pathlib import Path

import pytest

from eda_agent.easyeda_extension_cli import (
    _copy_extension_source,
    packaged_extension_dir,
)

REQUIRED = {
    "BUILD_STAMP.json",
    "README.md",
    "build.py",
    "capabilities.json",
    "extension.json",
    "iframe_template.html",
    "main.js",
}


def test_easyeda_extension_payload_is_available_in_this_install():
    source = packaged_extension_dir()
    assert source.is_dir(), f"EasyEDA extension payload directory is missing: {source}"
    present = {path.name for path in source.iterdir() if path.is_file()}
    assert REQUIRED <= present, f"EasyEDA extension payload is missing: {sorted(REQUIRED - present)}"


def test_easyeda_extension_payload_copies_to_a_writable_build_dir(tmp_path: Path):
    dest = tmp_path / "extension"
    copied = _copy_extension_source(dest, force=False)
    assert copied == dest.resolve()
    assert REQUIRED <= {path.name for path in copied.iterdir() if path.is_file()}
    assert not (copied / "dist").exists()
    assert not (copied / "eda-agent-bridge.eext").exists()


def test_easyeda_extension_copy_excludes_prebuilt_packages(tmp_path: Path, monkeypatch):
    source = tmp_path / "source"
    source.mkdir()
    for name in REQUIRED:
        (source / name).write_text("source payload", encoding="utf-8")
    (source / "eda-agent-bridge.eext").write_bytes(b"old build")
    (source / "previous.EEXT").write_bytes(b"another old build")
    monkeypatch.setattr(
        "eda_agent.easyeda_extension_cli.packaged_extension_dir", lambda: source)

    copied = _copy_extension_source(tmp_path / "destination", force=False)

    assert {path.name for path in copied.iterdir()} == REQUIRED


def test_easyeda_extension_copy_refuses_to_overwrite_nonempty_dest(tmp_path: Path):
    dest = tmp_path / "extension"
    dest.mkdir()
    sentinel = dest / "keep.txt"
    sentinel.write_text("do not overwrite silently", encoding="utf-8")

    with pytest.raises(RuntimeError, match="destination is not empty"):
        _copy_extension_source(dest, force=False)

    assert sentinel.read_text(encoding="utf-8") == "do not overwrite silently"
