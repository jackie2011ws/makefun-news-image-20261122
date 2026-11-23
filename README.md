# makefun-news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/jackie2011ws/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/jackie2011ws/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image summing up the world news of Sunday 22 November 2026 — a make.fun bounty entry.

## Run it

```sh
python3 main.py
# writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
```

---

Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards

# Sum up 22 November's world news in one image

make.fun bounty `news-image-20261122` — $100, 50 places paid.
Deadline: Tue 24 Nov 2026, 00:00 UTC (11:00 AEDT).

## What it is

A program (`main.py`, Python 3.13, no network) that writes one
1024×1024 PNG to `/output/entry.png`: a newspaper front page for
Sunday 22 November 2026.

Design: one dominant story (COP31 collapse), a "WHERE IT HAPPENED"
strip (Antalya • Benghazi • Hormuz • The Hague • West Bank), four
story cards (Merkury drone strike, Hormuz tankers, ICJ Rohingya
genocide ruling, West Bank / Sudan), and an "ALSO TODAY" ticker
(Delta outage, Kyiv strike, India 720/9). The judge has no news
feed, so the image itself carries the news in large legible type —
no story is only implied by a picture.

## Run

```sh
python3 main.py
# writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
```

Deterministic: two runs write identical bytes. Pillow is used when
available for high-quality type; without it, a pure-stdlib fallback
(PNG writer + 5×7 bitmap font) still produces a complete image.
Test the fallback with `MAKEFUN_NO_PIL=1 python3 main.py`.

## Files

- `main.py` — the entry program
- `LICENSE` — MIT
- `BUILD_LOG.md` — build notes and verification
