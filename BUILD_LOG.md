# Build log — Sum up 22 November's world news in one image

Bounty: https://make.fun/bounty/news-image-20261122
$100 total, 50 places paid (1st $20, 2nd $12, 3rd $6, 4th–10th $2,
11th–50th $1.20). Free entry, no fee.
Deadline verified live: Tue 24 Nov 2026, 00:00 UTC = 11:00 AEDT.
Checked 23 Nov 2026 ~12:02 UTC on make.fun home page and the bounty
page (both crawled <1 min before reading). Still open at build time,
~12 hours left. Escrow $100 USDC on Solana since 22 Nov 00:03:50 UTC.

## News research (23 Nov 2026, ~12:03 UTC)

Searched world news for Sunday 22 Nov 2026 (news vertical + general).
Stories used are the ones corroborated by multiple sources
(Open Chronicle brief, KPFA evening news, AP/KIRO wires, Standard
Topic archive, Daily Summary):

1. COP31 climate talks, Antalya, Turkey — ended with no agreement;
   fossil fuels the fault line. (lead story)
2. Suspected Ukrainian sea drones hit Russian corvette Merkury at
   Benghazi naval base, Libya; Zelenskyy says Ukraine was behind it.
3. Two supertankers hit mines and catch fire east of the Strait of
   Hormuz; Iran unveils an underground "missile city".
4. ICJ rules Myanmar committed genocide against the Rohingya.
5. West Bank settler attacks torch vehicles/homes; Israeli forces
   kill 2 in Gaza; Sudan drone strikes kill 4 near Khartoum and
   damage a UN building.
Also: Delta outage delays 1,600+ flights; Russian strike on Kyiv
kills 3; India declare 720/9 vs New Zealand.

Deliberately left out a less-corroborated item (a US House majority
claim seen in only one summary) rather than risk an inaccurate
headline the picture-editor judge would spot.

## Design decisions

- Newspaper front page, not a bullet list: one dominant headline,
  a "WHERE IT HAPPENED" strip, four story cards, an "ALSO TODAY"
  ticker. The judge has no news feed, so the image itself must
  carry the news in large legible type.
- Creative visual: cracked globe + rotated red "NO DEAL" stamp for
  the COP31 lead, instead of a plain headline block.
- Palette: off-white paper, ink black, deep red, navy, teal, gold.

## Revisions

1. First render: masthead clipped, hero text overflowed into the
   strip, NO DEAL stamp hidden, card text overflowed, footer
   overlapped. Fixed by auto-fitting the masthead, two-line hero
   headline, moving the strip to y=500, taller card budget with
   shorter copy, and an indented footer ticker.
2. Second render: clean except strip sub-labels clipping and a
   miscounted "six stories" tagline. Fixed both.
3. Stdlib fallback: first version overflowed the bottom and
   overlapped. Rewrote it with a running-y budget; final version
   is complete and legible.

## Verification (23 Nov 2026, ~12:06 UTC)

- `python3 main.py` (Pillow path): writes /output/entry.png,
  1024x1024 RGB PNG, 136 KB (< 1 MiB limit).
- Determinism: two runs, identical SHA-256
  e283eeafc6033f16ea4bf6bacb87e17367ddf9447615d0e9a94a6ab8a64bb36a
- Fallback (`MAKEFUN_NO_PIL=1`): writes a complete 1024x1024 PNG,
  14 KB, visually checked — all stories and the ALSO line visible.
- `python3 -m py_compile main.py`: OK. No network used by the
  program. Local Python is 3.12.3; code uses only stdlib + optional
  Pillow, compatible with Python 3.13.

## Still needed for submission (NOT done)

- A public GitHub repository owned by Sheng's GitHub account
  (created after the competition opened, 22 Nov 00:03 UTC),
  OSI licence (MIT included here), with main.py at the root.
  No GitHub account details were available to this session, so
  no repo was created or pushed.
- AI coding-agent transcripts of the sessions that built it,
  bundled as required by make.fun (bundle / transcripts).
- Entry submission on make.fun before Tue 24 Nov 00:00 UTC,
  signed with the connected Solana wallet (@jackie2011ws) —
  entry message "make.fun entry v1", signature valid 10 minutes.
  Do not submit after the deadline; the last submission before
  the deadline is the final entry (max 10/day, 20 total).
