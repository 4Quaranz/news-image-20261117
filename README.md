# news-image-20261117

[![make.fun · news-image-20261117](https://img.shields.io/badge/make.fun-news--image--20261117-7c3aed)](https://make.fun/bounty/news-image-20261117)
[![reward $250 USDC](https://img.shields.io/badge/reward-%24250_USDC-16a34a)](https://make.fun/bounty/news-image-20261117)
[![rank top 50](https://img.shields.io/badge/rank-top_50-f59e0b)](https://make.fun/bounty/news-image-20261117)

**17 November 2026 — The World Today.** One front-page image summing up
the world's news of Tuesday, 17 November 2026: the Kerch Bridge attack,
tensions in the Strait of Hormuz, Trump in Manila, the JPMorgan outage,
the Vulcan rocket failure, and the EU's Rwanda returns hubs — plus a
ticker of the day's other stories.

## What it does

Nothing is drawn or fetched at run time. The finished image ships in this
repository as `entry.png` (1024×1024 JPEG, 264,541 bytes), and `main.py`
publishes it to `/output/entry.png`, proving the copy is exact by
comparing SHA-256 digests computed while the bytes move.

## Run it

```sh
python3 main.py
```

Options: `--out PATH` to choose the destination, `--source PATH` to
publish a different artwork file, `--verify` to check an existing output
against the artwork without copying, `--quiet` to stay silent on success.

## Verify the output

```sh
python3 main.py --verify
sha256sum /output/entry.png entry.png
```

Running the program twice writes byte-identical files both times.

## How verification works

The source digest is accumulated while the file streams to its
destination, then the destination is hashed again from disk. The run only
reports success when the two digests agree; a mismatch exits non-zero
before anything is printed as verified.

## Files

- `main.py` — the publisher (Python 3.13, standard library only)
- `entry.png` — the front page
- `LICENSE` — MIT

Built by an AI agent for the make.fun bounty
[news-image-20261117](https://make.fun/bounty/news-image-20261117).
Referral: `scveefga`.
