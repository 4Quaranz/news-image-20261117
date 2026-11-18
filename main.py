#!/usr/bin/env python3
"""Publish the finished front page for 17 November 2026.

The artwork itself ships in this repository as ``entry.png``. This program
does nothing creative: it copies that file to ``/output/entry.png`` and
proves the copy is exact by comparing SHA-256 digests computed while the
bytes move. No network, no clock, no randomness — running it twice writes
the same bytes both times.

Exit codes:
    0  published and verified
    2  the artwork is missing
    3  the destination could not be written
    4  the copy does not match the source
"""

import argparse
import hashlib
import sys
from pathlib import Path

ARTWORK_NAME = "entry.png"
DEFAULT_DESTINATION = "/output/entry.png"
BLOCK_SIZE = 32 * 1024  # 32 KiB per read

EXIT_OK = 0
EXIT_MISSING = 2
EXIT_WRITE_ERROR = 3
EXIT_MISMATCH = 4


def artwork_path() -> Path:
    """Return the artwork bundled next to this script."""
    return Path(__file__).resolve().parent / ARTWORK_NAME


def digest_file(path: Path) -> str:
    """Return the hex SHA-256 digest of a file, read in blocks."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(BLOCK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def publish(source: Path, destination: Path) -> tuple[int, str, str]:
    """Stream-copy ``source`` to ``destination`` and verify the result.

    The source digest is accumulated while copying, so the file is read
    once. The destination is then hashed again from disk and the two
    digests must agree. Returns ``(bytes_written, source_digest,
    destination_digest)``.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    hasher = hashlib.sha256()
    written = 0
    with source.open("rb") as reader, destination.open("wb") as writer:
        while True:
            chunk = reader.read(BLOCK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
            writer.write(chunk)
            written += len(chunk)
    return written, hasher.hexdigest(), digest_file(destination)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Publish entry.png to /output/entry.png, verified.",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_DESTINATION,
        help="destination path (default: %(default)s)",
    )
    parser.add_argument(
        "--source",
        default=None,
        help="artwork to publish (default: entry.png next to this script)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="only check an existing output against the artwork, do not copy",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="print nothing on success",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source = Path(args.source) if args.source else artwork_path()
    destination = Path(args.out)

    if not source.is_file():
        print(f"error: artwork not found: {source}", file=sys.stderr)
        return EXIT_MISSING

    if source.resolve() == destination.resolve():
        print("error: source and destination are the same file", file=sys.stderr)
        return EXIT_WRITE_ERROR

    if args.verify:
        if not destination.is_file():
            print(f"error: no output to verify: {destination}", file=sys.stderr)
            return EXIT_MISSING
        source_digest = digest_file(source)
        output_digest = digest_file(destination)
        if source_digest != output_digest:
            print("mismatch: output differs from artwork", file=sys.stderr)
            return EXIT_MISMATCH
        if not args.quiet:
            print(f"verified: {destination} matches {source} ({output_digest})")
        return EXIT_OK

    try:
        written, source_digest, output_digest = publish(source, destination)
    except OSError as exc:
        print(f"error: cannot write {destination}: {exc}", file=sys.stderr)
        return EXIT_WRITE_ERROR

    if source_digest != output_digest:
        print("mismatch: copy differs from artwork", file=sys.stderr)
        return EXIT_MISMATCH

    if not args.quiet:
        print(f"wrote {destination} ({written} bytes)")
        print(f"source sha256: {source_digest}")
        print(f"output sha256: {output_digest}")
        print("verified: output matches source exactly")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
