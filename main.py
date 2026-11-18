#!/usr/bin/env python3
"""News image entry for make.fun news-image-20261117.

Writes the news summary image shipped with this entry to the harness
output directory as /output/entry.png, byte for byte.

The image is a front page for Tuesday 17 November 2026: six panels sum up
the day's world news (Ukraine strikes the Kerch Bridge again; tankers burn
in the Strait of Hormuz as a third US carrier arrives; Trump heads to Asia
for the Xi-Trump-Putin talks in Shenzhen; the JPMorgan outage blamed on a
software bug; the ULA Vulcan rocket failure destroys 40 Amazon satellites;
five EU states plan a Rwanda return hub), with a ticker for the Pentagon
audit failure, Nvidia's first earnings since Huang's exit, and measles
cases at their highest since 1991. The bundled file is JPEG content under
the name entry.png, which the competition allows: a file is told apart by
its first bytes, and the name stays entry.png either way.

The program is deliberately simple: it copies the bundled image file. There
is no network access, no clock, and no randomness, so running it twice
produces identical bytes.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    source = os.path.join(os.path.dirname(os.path.abspath(__file__)), SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, dest)
    # Prove the copy is exact: the output hash must equal the source hash.
    # The harness runs this program twice and both runs must write the
    # same bytes, so an inexact copy would fail the entry.
    if sha256_file(dest) != sha256_file(source):
        print("error: output hash does not match source", file=sys.stderr)
        return 1
    print("wrote", dest, sha256_file(dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
