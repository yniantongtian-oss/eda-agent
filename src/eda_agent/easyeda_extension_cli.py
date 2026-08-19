# SPDX-License-Identifier: Apache-2.0
"""Locate or build the EasyEDA Pro editor extension shipped in the wheel."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def packaged_extension_dir() -> Path:
    """Return the read-only extension source directory inside the package."""
    return Path(__file__).resolve().parent / "easyeda_extension"


def _copy_extension_source(dest: Path, *, force: bool) -> Path:
    source = packaged_extension_dir()
    required = ("build.py", "main.js", "extension.json", "BUILD_STAMP.json")
    missing = [name for name in required if not (source / name).is_file()]
    if missing:
        raise RuntimeError(
            "installed wheel is missing EasyEDA extension payload: "
            + ", ".join(missing)
        )

    dest = dest.expanduser().resolve()
    if dest.exists():
        if not force:
            entries = list(dest.iterdir()) if dest.is_dir() else [dest]
            if entries:
                raise RuntimeError(
                    f"destination is not empty: {dest}; use --force to replace "
                    "the packaged extension source files"
                )
        if not dest.is_dir():
            raise RuntimeError(f"destination exists and is not a directory: {dest}")
    else:
        dest.mkdir(parents=True)

    # Copy only the immutable source payload. Generated dist/ and .eext files
    # are deliberately absent from the wheel and are created in this writable
    # destination by the canonical extension build script.
    for item in source.iterdir():
        if item.is_file():
            shutil.copy2(item, dest / item.name)
    return dest


def _build(dest: Path, *, force: bool) -> Path:
    if shutil.which("node") is None:
        raise RuntimeError(
            "Node.js is required by the EasyEDA extension build to validate "
            "the generated entry point with the same function-body parse shape "
            "used by EasyEDA. Install Node.js and run this command again."
        )

    work = _copy_extension_source(dest, force=force)
    proc = subprocess.run([sys.executable, str(work / "build.py")], cwd=work)
    if proc.returncode != 0:
        raise RuntimeError(f"EasyEDA extension build failed with exit code {proc.returncode}")

    package = work / "eda-agent-bridge.eext"
    if not package.is_file() or package.stat().st_size == 0:
        raise RuntimeError(
            f"extension build returned success but did not create a usable {package.name}"
        )
    return package


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="eda-agent-easyeda-extension",
        description=(
            "Locate or build the EasyEDA Pro editor extension bundled with "
            "the installed eda-agent wheel."
        ),
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("path", help="Print the packaged extension source directory")

    build = sub.add_parser(
        "build",
        help="Copy the packaged extension to a writable directory and build .eext",
    )
    build.add_argument(
        "--dest",
        type=Path,
        default=Path.cwd() / "eda-agent-easyeda-extension",
        help=(
            "Writable build directory (default: ./eda-agent-easyeda-extension)"
        ),
    )
    build.add_argument(
        "--force",
        action="store_true",
        help="Allow replacing packaged source files in a non-empty destination",
    )

    args = parser.parse_args()
    command = args.command or "path"

    try:
        if command == "path":
            source = packaged_extension_dir()
            if not source.is_dir():
                raise RuntimeError(
                    "installed package does not contain the EasyEDA extension payload"
                )
            print(source)
            return 0

        if command == "build":
            package = _build(args.dest, force=args.force)
            print(package)
            return 0

        parser.error(f"unknown command: {command}")
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
