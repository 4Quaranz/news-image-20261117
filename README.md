# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/4Quaranz/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/4Quaranz/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

17 November 2026 — The World Today. A single front-page image that sums up the world's news of Tuesday 17 November 2026: the day's biggest stories, laid out the way a newspaper front page lays them out, so a reader gets the whole day at one glance. The image is a JPEG, 1024 by 1024 pixels.

The entry is a small Python program. It does not fetch or draw anything; the finished image ships in this repository as `entry.png`, and the program writes it out to `/output/entry.png`, byte for byte.

## How it works

`main.py` finds `entry.png` beside itself, streams it to `/output/entry.png` in 64 KiB blocks, and hashes both files with SHA-256 to confirm the copy is exact. No network is used and no pixels are generated at run time, so running the program twice writes identical bytes.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=scveefga&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
