#!/usr/bin/env python3
"""
Sum up 22 November's world news in one image
make.fun bounty: news-image-20261122
$100, 50 places paid. Deadline: Tue 24 Nov 2026, 00:00 UTC (11:00 AEDT).

Entry: a program that writes one 1024x1024 PNG to /output/entry.png.
No network. Deterministic: two runs write identical bytes.

Design (what makes this different from a generic list):
  A newspaper front page, not a bullet list. One dominant story, a
  "where it happened" strip, and four story cards a picture editor can
  read at a glance. The judge has no news feed, so the image itself
  must carry the news: every story is named, placed and explained in
  its own words on the page, in large legible type.

  Stories (all corroborated by multiple wire / news sources on
  22 Nov 2026; wording is our own summary):
  1. COP31 climate talks in Antalya, Turkey, end with NO deal --
     nearly 200 countries fail to agree, fossil fuels the fault line.
  2. Suspected Ukrainian sea drones hit the Russian corvette Merkury
     at Benghazi naval base, Libya; Zelenskyy says Ukraine was behind it.
  3. Two supertankers hit mines and catch fire east of the Strait of
     Hormuz; Iran unveils an underground "missile city".
  4. The International Court of Justice rules Myanmar committed
     genocide against the Rohingya.
  5. West Bank settler attacks torch vehicles and homes; Israeli
     forces kill 2 in Gaza; Sudan drone strikes kill 4 near Khartoum
     and damage a UN building.
  Also: Delta outage delays 1,600+ flights; Russian strike on Kyiv
  kills 3; India declare 720/9 vs New Zealand.

Rendering: Pillow if available (DejaVu fonts), otherwise a pure
stdlib fallback (own PNG writer + 5x7 bitmap font) that still
produces a complete, legible image. Set MAKEFUN_NO_PIL=1 to test
the fallback.
"""

import os
import sys

W = H = 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT_PATH = os.path.join(OUT, "entry.png")

# --- palette ---------------------------------------------------------------
PAPER = (246, 241, 231)
INK = (20, 20, 20)
MUTED = (90, 85, 72)
RED = (180, 35, 24)
DARKRED = (140, 22, 14)
NAVY = (20, 36, 62)
NAVY2 = (28, 52, 88)
TEAL = (14, 107, 107)
GOLD = (201, 138, 27)
CREAM = (250, 247, 238)
RULE = (20, 20, 20)
LIGHTLINE = (210, 203, 186)

DATE_LINE = "SUNDAY  •  22 NOVEMBER 2026"
MASTHEAD = "THE WORLD IN ONE PICTURE"


# ===========================================================================
# PIL rendering (primary path)
# ===========================================================================
def _find_font(bold, serif):
    """Return a truetype path, or None."""
    candidates = []
    if serif:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
            "/usr/share/fonts/TTF/DejaVuSerif-Bold.ttf",
            "/usr/local/share/fonts/DejaVuSerif-Bold.ttf",
            "DejaVuSerif-Bold.ttf",
        ]
    elif bold:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
            "/usr/local/share/fonts/DejaVuSans-Bold.ttf",
            "DejaVuSans-Bold.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
            "/usr/local/share/fonts/DejaVuSans.ttf",
            "DejaVuSans.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def _font(ImageFont, size, bold=False, serif=False):
    path = _find_font(bold, serif)
    if path:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


def _wrap(draw, text, font, max_w):
    """Greedy word wrap to a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _text_block(draw, x, y, text, font, fill, max_w, leading):
    lines = _wrap(draw, text, font, max_w)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def _centre(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y


def render_pil():
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGB")

    # ---- paper frame ------------------------------------------------------
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)
    d.rectangle([14, 14, W - 15, H - 15], outline=LIGHTLINE, width=1)

    # ---- masthead ---------------------------------------------------------
    f_date = _font(ImageFont, 26, bold=True)
    mast_size = 60
    while mast_size > 40:
        f_mast = _font(ImageFont, mast_size, bold=True, serif=True)
        if d.textlength(MASTHEAD, font=f_mast) <= 928:
            break
        mast_size -= 2
    f_tag = _font(ImageFont, 21, bold=False)
    _centre(d, W // 2, 30, DATE_LINE, f_date, RED)
    _centre(d, W // 2, 62, MASTHEAD, f_mast, INK)
    d.line([(48, 138), (W - 48, 138)], fill=INK, width=3)
    d.line([(48, 144), (W - 48, 144)], fill=INK, width=1)
    _centre(
        d, W // 2, 154,
        "THE DAY'S BIGGEST STORIES  •  READ IT IN ONE LOOK",
        f_tag, MUTED,
    )

    # ---- hero: COP31 ------------------------------------------------------
    # Left: headline. Right: drawn globe, cracked, with NO DEAL stamp.
    hx, hy, hw = 48, 196, 560
    f_kick = _font(ImageFont, 24, bold=True)
    f_head = _font(ImageFont, 64, bold=True, serif=True)
    f_sub = _font(ImageFont, 24, bold=False)
    d.text((hx, hy), "LEAD  •  CLIMATE", font=f_kick, fill=RED)
    y = hy + 36
    for line in ["CLIMATE TALKS", "COLLAPSE"]:
        d.text((hx, y), line, font=f_head, fill=INK)
        y += 66
    y += 8
    y = _text_block(
        d, hx, y,
        "COP31 ends in Antalya with no deal. Nearly 200 countries "
        "fail to agree — fossil fuels are the fault line.",
        f_sub, INK, hw, 30,
    )

    # Globe, right of the headline.
    cx, cy, r = 810, 295, 100
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 232, 226),
              outline=NAVY, width=4)
    # abstract continents (stylised, not a map claim)
    d.polygon([(cx - 78, cy - 42), (cx - 30, cy - 62), (cx - 8, cy - 28),
               (cx - 48, cy - 6), (cx - 82, cy - 18)], fill=TEAL)
    d.polygon([(cx + 12, cy + 8), (cx + 62, cy - 6), (cx + 84, cy + 30),
               (cx + 40, cy + 58), (cx + 6, cy + 40)], fill=TEAL)
    d.polygon([(cx - 52, cy + 52), (cx - 6, cy + 44), (cx + 2, cy + 82),
               (cx - 38, cy + 92)], fill=(46, 140, 120))
    # latitude / longitude arcs
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=NAVY, width=2)
    d.ellipse([cx - 52, cy - r, cx + 52, cy + r], outline=NAVY, width=2)
    # the crack
    crack = [(cx - 30, cy - 108), (cx - 8, cy - 70), (cx - 26, cy - 34),
             (cx + 6, cy + 4), (cx - 12, cy + 44), (cx + 14, cy + 82),
             (cx - 2, cy + 112)]
    d.line(crack, fill=DARKRED, width=7, joint="curve")
    d.line(crack, fill=(255, 122, 89), width=3, joint="curve")
    # NO DEAL stamp, rotated
    stamp = Image.new("RGBA", (220, 68), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([4, 4, 215, 63], outline=RED, width=5)
    sd.text((110, 34), "NO DEAL", font=_font(ImageFont, 36, bold=True),
            fill=RED, anchor="mm")
    stamp = stamp.rotate(-14, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (cx - 105, cy + 72), stamp)
    d = ImageDraw.Draw(img, "RGB")

    # ---- where it happened strip -----------------------------------------
    sy = 500
    d.rectangle([36, sy, W - 36, sy + 108], fill=NAVY)
    f_strip = _font(ImageFont, 20, bold=True)
    f_city = _font(ImageFont, 22, bold=True)
    f_what = _font(ImageFont, 17, bold=False)
    d.text((60, sy + 12), "WHERE IT HAPPENED", font=f_strip, fill=GOLD)
    places = [
        ("ANTALYA", "climate talks fail"),
        ("BENGHAZI", "warship hit at sea"),
        ("HORMUZ", "tankers on fire"),
        ("THE HAGUE", "genocide ruled"),
        ("WEST BANK", "villages torched"),
    ]
    step = (W - 72 - 24) // 5
    for i, (city, what) in enumerate(places):
        px = 60 + i * step
        d.ellipse([px, sy + 44, px + 16, sy + 60], fill=GOLD)
        if i < 4:
            d.line([(px + 16, sy + 52), (px + step, sy + 52)],
                   fill=(120, 140, 170), width=2)
        d.text((px, sy + 62), city, font=f_city, fill=(255, 255, 255))
        d.text((px, sy + 88), what, font=f_what, fill=(190, 200, 215))
    # (x unused by design; positions are absolute per column)

    # ---- story cards ------------------------------------------------------
    f_tag2 = _font(ImageFont, 18, bold=True)
    f_card = _font(ImageFont, 28, bold=True, serif=True)
    f_body = _font(ImageFont, 20, bold=False)
    cards = [
        ("SEA WAR  •  LIBYA", RED,
         "Drone strike at sea",
         "Suspected Ukrainian sea drones hit the Russian corvette "
         "Merkury at Benghazi. Zelenskyy says Ukraine was behind it."),
        ("ENERGY  •  GULF", TEAL,
         "Tankers ablaze at Hormuz",
         "Two supertankers hit mines and catch fire east of the "
         "Strait of Hormuz. Iran unveils an underground "
         "\u201cmissile city\u201d."),
        ("JUSTICE  •  THE HAGUE", NAVY2,
         "Genocide, ruled",
         "The International Court of Justice rules that Myanmar "
         "committed genocide against its Rohingya minority."),
        ("OCCUPATION  •  WEST BANK", DARKRED,
         "Villages torched",
         "Settlers burn vehicles and homes in the West Bank. "
         "Israeli forces kill 2 in Gaza. Sudan drones kill 4 "
         "near Khartoum."),
    ]
    gx, gy = 36, 624
    cw, ch, gap = 464, 152, 20
    for i, (tag, colour, title, body) in enumerate(cards):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=CREAM,
                    outline=LIGHTLINE, width=1)
        d.rectangle([x, y, x + cw, y + 6], fill=colour)
        d.text((x + 18, y + 16), tag, font=f_tag2, fill=colour)
        d.text((x + 18, y + 40), title, font=f_card, fill=INK)
        _text_block(d, x + 18, y + 78, body, f_body, INK, cw - 36, 25)

    # ---- footer ticker ----------------------------------------------------
    fy = 956
    d.line([(36, fy), (W - 36, fy)], fill=INK, width=2)
    f_tick = _font(ImageFont, 19, bold=False)
    f_tick_b = _font(ImageFont, 19, bold=True)
    label = "ALSO TODAY   "
    d.text((36, fy + 12), label, font=f_tick_b, fill=RED)
    lw = d.textlength(label, font=f_tick_b)
    _text_block(
        d, 36 + lw, fy + 12,
        "Delta delays 1,600+ flights  •  Kyiv strike kills 3  •  "
        "India 720/9 vs New Zealand",
        f_tick, INK, W - 72 - lw, 28,
    )
    return img


# ===========================================================================
# Stdlib-only fallback (no Pillow): PNG writer + 5x7 bitmap font
# ===========================================================================
import struct
import zlib

_FONT5X7 = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    ";": ["00000", "01100", "01100", "00000", "01100", "00100", "01000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "?": ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
    "-": ["00000", "00000", "00000", "01110", "00000", "00000", "00000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    '"': ["01010", "01010", "00000", "00000", "00000", "00000", "00000"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    "%": ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "*": ["00000", "10101", "01110", "10101", "00000", "00000", "00000"],
    "=": ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    "<": ["00010", "00100", "01000", "10000", "01000", "00100", "00010"],
    ">": ["01000", "00100", "00010", "00001", "00010", "00100", "01000"],
    "#": ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
    "@": ["01110", "10001", "10111", "10101", "10110", "10000", "01110"],
    "$": ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
}


def _png_chunk(typ, data):
    chunk = struct.pack(">I", len(data)) + typ + data
    chunk += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return chunk


def _write_png(path, rgb, w, h):
    raw = b"".join(b"\x00" + bytes(rgb[y * w * 3:(y + 1) * w * 3])
                   for y in range(h))
    png = b"\x89PNG\r\n\x1a\n"
    png += _png_chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += _png_chunk(b"IDAT", zlib.compress(raw, 9))
    png += _png_chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


class _FB:
    """Tiny framebuffer with a 5x7 bitmap font."""

    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * w * h)

    def rect(self, x0, y0, x1, y1, col):
        for y in range(max(0, y0), min(self.h, y1)):
            for x in range(max(0, x0), min(self.w, x1)):
                i = (y * self.w + x) * 3
                self.px[i:i + 3] = bytes(col)

    def text(self, x, y, s, scale, col):
        s = s.upper()
        cx = x
        for ch in s:
            g = _FONT5X7.get(ch, _FONT5X7[" "])
            for r, row in enumerate(g):
                for c, bit in enumerate(row):
                    if bit == "1":
                        self.rect(cx + c * scale, y + r * scale,
                                  cx + (c + 1) * scale, y + (r + 1) * scale,
                                  col)
            cx += 6 * scale
        return cx

    def text_wrapped(self, x, y, s, scale, col, max_w, leading):
        words, lines, cur = s.upper().split(), [], ""
        for word in words:
            trial = (cur + " " + word).strip()
            if len(trial) * 6 * scale <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        for line in lines:
            self.text(x, y, line, scale, col)
            y += leading
        return y


def render_fallback():
    fb = _FB(W, H, PAPER)
    fb.rect(0, 0, W, 4, INK)
    fb.rect(0, H - 4, W, H, INK)
    y = 30
    fb.text(300, y, DATE_LINE, 3, RED)
    y += 44
    fb.text(48, y, "THE WORLD IN", 6, INK)
    y += 52
    fb.text(48, y, "ONE PICTURE", 6, INK)
    y += 58
    fb.rect(48, y, W - 48, y + 4, INK)
    y += 18
    fb.text(48, y, "THE DAY'S BIGGEST STORIES", 2, MUTED)
    y += 36
    fb.text(48, y, "CLIMATE TALKS", 5, INK)
    y += 44
    fb.text(48, y, "COLLAPSE", 5, INK)
    y += 48
    y = fb.text_wrapped(48, y,
                         "COP31 ends in Antalya with no deal. Nearly 200 "
                         "countries fail to agree - fossil fuels are the "
                         "fault line.", 2, INK, 928, 26)
    y += 8
    fb.text(48, y, "NO DEAL", 4, RED)
    y += 44
    fb.rect(36, y, W - 36, y + 84, NAVY)
    fb.text(60, y + 12, "WHERE IT HAPPENED", 2, GOLD)
    fb.text(60, y + 44,
            "ANTALYA - BENGHAZI - HORMUZ - THE HAGUE - WEST BANK",
            2, (255, 255, 255))
    y += 100
    for tag, title, body in [
        ("SEA WAR - LIBYA", "DRONE STRIKE AT SEA",
         "Suspected Ukrainian sea drones hit the Russian corvette "
         "Merkury at Benghazi. Zelenskyy says Ukraine was behind it."),
        ("ENERGY - GULF", "TANKERS ABLAZE AT HORMUZ",
         "Two supertankers hit mines and catch fire east of the "
         "Strait of Hormuz. Iran unveils an underground missile city."),
        ("JUSTICE - THE HAGUE", "GENOCIDE, RULED",
         "The International Court of Justice rules Myanmar committed "
         "genocide against its Rohingya minority."),
        ("WEST BANK", "VILLAGES TORCHED",
         "Settlers burn vehicles and homes. Israeli forces kill 2 "
         "in Gaza. Sudan drones kill 4 near Khartoum."),
    ]:
        fb.text(48, y, tag, 2, RED)
        y += 22
        fb.text(48, y, title, 3, INK)
        y += 30
        y = fb.text_wrapped(48, y, body, 2, INK, 928, 24)
        y += 10
    fb.rect(36, y, W - 36, y + 3, INK)
    y += 12
    fb.text(48, y, "ALSO: DELTA DELAYS 1600+ FLIGHTS - KYIV 3 KILLED",
            2, MUTED)
    return fb


def main():
    os.makedirs(OUT, exist_ok=True)
    use_pil = os.environ.get("MAKEFUN_NO_PIL") != "1"
    if use_pil:
        try:
            img = render_pil()
            img.save(OUT_PATH, format="PNG", optimize=True)
            print(f"wrote {OUT_PATH} via Pillow")
            return 0
        except Exception as exc:  # fall through to stdlib path
            print(f"Pillow render failed ({exc}); using stdlib fallback",
                  file=sys.stderr)
    fb = render_fallback()
    _write_png(OUT_PATH, fb.px, W, H)
    print(f"wrote {OUT_PATH} via stdlib fallback")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
