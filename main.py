#!/usr/bin/env python3
"""Copy the repo's entry.png to the output directory and validate it.

Standard library only. No network, no clock, no randomness.
"""
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"

MAX_DIM = 1024
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def png_size(data):
    """Read width/height from the IHDR chunk without any image library."""
    if len(data) < 33:
        fail("entry.png is too short to be a valid PNG")
    if data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk where one was expected")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        fail(f"cannot create output directory {out_dir}: {exc}")

    if not SOURCE.is_file():
        fail(f"source image missing: {SOURCE}")

    dest = out_dir / "entry.png"
    try:
        shutil.copyfile(SOURCE, dest)
    except OSError as exc:
        fail(f"cannot copy {SOURCE} to {dest}: {exc}")

    try:
        data = dest.read_bytes()
    except OSError as exc:
        fail(f"cannot read copied file {dest}: {exc}")

    if len(data) != SOURCE.stat().st_size:
        fail(f"copied entry.png is {len(data)} bytes, source is "
             f"{SOURCE.stat().st_size} bytes; copy is incomplete")
    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the {MAX_BYTES} byte limit")
    if not data.startswith(PNG_MAGIC):
        fail("entry.png does not start with PNG magic bytes")
    width, height = png_size(data)
    if width > MAX_DIM or height > MAX_DIM:
        fail(f"entry.png is {width}x{height}, over the {MAX_DIM}x{MAX_DIM} limit")

    print(f"{dest} {width}x{height} {len(data)} bytes")


if __name__ == "__main__":
    main()
