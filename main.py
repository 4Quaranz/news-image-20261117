#!/usr/bin/env python3
"""Reproduce the news-image-20261117 entry artwork.

The entry is a single front-page image, "17 November 2026 - The World
Today", stored in this repository as entry.png. This module writes that
stored image to /output/entry.png. It downloads nothing and draws nothing:
the bytes already on disk are copied out unchanged, so every run produces
the exact same file.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ARTWORK = "entry.png"
DEFAULT_DESTINATION = Path("/output/entry.png")
CHUNK = 64 * 1024


def find_artwork() -> Path:
    """Locate the bundled artwork next to this file."""
    candidate = Path(__file__).resolve().parent / ARTWORK
    if not candidate.is_file():
        raise SystemExit(f"artwork missing: expected {candidate}")
    return candidate


def stream_copy(source: Path, destination: Path) -> tuple[int, str]:
    """Copy source to destination in blocks.

    Returns the byte count and the SHA-256 of the bytes read, so the caller
    can prove the copy is exact without re-reading the source.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    written = 0
    with source.open("rb") as reader, destination.open("wb") as writer:
        while True:
            block = reader.read(CHUNK)
            if not block:
                break
            digest.update(block)
            writer.write(block)
            written += len(block)
    return written, digest.hexdigest()


def digest_file(path: Path) -> str:
    """SHA-256 of a file, read back in blocks."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def main(argv: list[str]) -> int:
    destination = Path(argv[1]) if len(argv) > 1 else DEFAULT_DESTINATION
    source = find_artwork()
    try:
        total, source_digest = stream_copy(source, destination)
    except OSError as exc:
        print(f"error: cannot write {destination}: {exc}", file=sys.stderr)
        return 1
    written_digest = digest_file(destination)
    print(f"wrote {destination} ({total} bytes) from {source.name}")
    print(f"source sha256:      {source_digest}")
    print(f"output sha256:      {written_digest}")
    if written_digest != source_digest:
        print("error: output does not match source", file=sys.stderr)
        return 1
    print("verified: output matches source exactly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
