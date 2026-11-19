#!/usr/bin/env python3
"""news-image-20261119 entry: write the poster to the output directory.

The image is the repository's own entry.png, rendered at build time from
the verified news of 19 November 2026 (see gen_poster.py). This program
only copies those exact bytes, so two runs always produce identical output.
Standard library only; no network, no clock, no randomness.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Guard the gate: the copied file must still be a whole PNG within
    # the competition's caps (at most 1 MiB, at most 1024 by 1024).
    with open(dst, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    if width > 1024 or height > 1024:
        raise SystemExit("entry.png exceeds 1024x1024")
    if os.path.getsize(dst) > 1048576:
        raise SystemExit("entry.png exceeds 1 MiB")


if __name__ == "__main__":
    main()
