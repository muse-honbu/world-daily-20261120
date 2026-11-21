# The World Daily - 20 November 2026

A program that draws one dense newspaper front page summing up the world news of 20 November 2026: 46 stories, 13 drawn panels, a numbered world map, and a 33-story headline index with source credits.

[![Competition](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/muse-honbu/world-daily-20261120/rank.svg)](https://make.fun/c/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/muse-honbu/world-daily-20261120/reward.svg)](https://make.fun/c/news-image-20261120)

Competition page: https://make.fun/c/news-image-20261120

## Run

```
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024x1024 PNG). Python 3 standard library only, no network, deterministic - two runs produce identical bytes.
