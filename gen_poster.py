#!/usr/bin/env python3
"""Deterministic newspaper poster for 19 November 2026.

Renders a fixed 1024x1024 image with PIL only. No network, no clock,
no randomness: the same run always produces the same bytes.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024
SIDE = 44
CONTENT = W - 2 * SIDE

PAPER = (250, 246, 238)
INK = (18, 18, 18)
GREY = (96, 96, 92)
LIGHT_GREY = (178, 172, 164)
RED = (163, 22, 33)
NAVY = (31, 56, 100)

FONTS = Path("/usr/share/fonts/truetype/dejavu")
_cache = {}


def font(kind, size):
    key = (kind, size)
    if key not in _cache:
        name = {
            "serif_b": "DejaVuSerif-Bold.ttf",
            "sans": "DejaVuSans.ttf",
            "sans_b": "DejaVuSans-Bold.ttf",
        }[kind]
        _cache[key] = ImageFont.truetype(str(FONTS / name), size)
    return _cache[key]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width."""
    lines = []
    cur = ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, lines, x, y, fnt, fill, leading):
    """Draw stacked lines; return the y just below the block."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def mixed_para(draw, tag, text, x, y, max_w, tag_fnt, body_fnt, leading):
    """One paragraph: red bold tag, then black text, wrapped together.

    Words carry their own font so the tag and body share lines cleanly.
    Returns the y just below the paragraph.
    """
    words = [(tag, tag_fnt, RED)] + [(w, body_fnt, INK) for w in text.split()]
    lines = []
    cur = []
    cur_w = 0.0
    space_w = draw.textlength(" ", font=body_fnt)
    for word, fnt, fill in words:
        ww = draw.textlength(word, font=fnt)
        add = ww if not cur else space_w + ww
        if cur and cur_w + add > max_w:
            lines.append(cur)
            cur = [(word, fnt, fill)]
            cur_w = ww
        else:
            cur.append((word, fnt, fill))
            cur_w += add
    if cur:
        lines.append(cur)
    for line_words in lines:
        cx = x
        for i, (word, fnt, fill) in enumerate(line_words):
            if i:
                cx += space_w
            draw.text((cx, y), word, font=fnt, fill=fill)
            cx += draw.textlength(word, font=fnt)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 28

    # ---- Masthead ----
    f_date = font("sans_b", 18)
    date_line = "THURSDAY \u00b7 19 NOVEMBER 2026"
    dw = d.textlength(date_line, font=f_date)
    d.text(((W - dw) / 2, y), date_line, font=f_date, fill=RED)
    y += 20 + 5

    f_title = font("serif_b", 60)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, y), title, font=f_title, fill=NAVY)
    y += 70 + 3

    f_sub = font("sans", 19)
    sub = "The day's world news in one image"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, y), sub, font=f_sub, fill=GREY)
    y += 24 + 9

    d.rectangle([SIDE, y, W - SIDE, y + 3], fill=INK)
    y += 3 + 3
    d.rectangle([SIDE, y, W - SIDE, y], fill=LIGHT_GREY)
    y += 1 + 10

    # ---- Lead story ----
    f_kick = font("sans_b", 16)
    d.text((SIDE, y), "SHENZHEN \u2014 LEAD STORY", font=f_kick, fill=RED)
    y += 20 + 4

    f_head = font("sans_b", 29)
    head_lines = wrap(
        d, "Trump, Xi and Putin meet today in a first-ever trilateral",
        f_head, CONTENT)
    assert len(head_lines) <= 2, f"lead headline needs {len(head_lines)} lines"
    y = block(d, head_lines, SIDE, y, f_head, INK, 37)
    y += 4

    f_dek = font("serif_b", 22)
    dek_lines = wrap(
        d, "Nuclear arms top the agenda in Shenzhen \u2014 but no deal is expected",
        f_dek, CONTENT)
    assert len(dek_lines) <= 2, f"dek needs {len(dek_lines)} lines"
    y = block(d, dek_lines, SIDE, y, f_dek, NAVY, 29)
    y += 5

    f_body = font("sans", 16)
    body_lines = wrap(
        d,
        "The three leaders have never met in this format. China confirmed "
        "the summit on Monday; the White House and Kremlin had already "
        "agreed. Officials caution against expecting a breakthrough, and "
        "Trump is not expected to raise Ukraine in the three-way talks.",
        f_body, CONTENT)
    assert len(body_lines) <= 3, f"lead body needs {len(body_lines)} lines"
    y = block(d, body_lines, SIDE, y, f_body, GREY, 21)
    y += 16

    # ---- Story grid: 2 columns x 3 rows ----
    cards = [
        ("MIDDLE EAST",
         "Iran fired on US sites in Kuwait; Bahrain hit a third time in a week",
         "Tehran says it struck US drone and missile sites overnight, the "
         "first attack on Kuwait since September. Vance vows no 'forever "
         "war' \u2014 but gives no end date."),
        ("THE HAGUE",
         "World court rules today in Myanmar genocide case",
         "The ICJ reads its judgment on Gambia's case over the 2017 "
         "crackdown that drove 700,000 Rohingya into Bangladesh. A genocide "
         "finding would be a first for a state."),
        ("INDONESIA",
         "Prabowo at APEC as Indonesia signs $71.8B in China deals",
         "The president joins today's leaders' meeting after witnessing "
         "deals on smart cities, appliances and coal-to-ethanol. He meets "
         "Xi on Friday."),
        ("GAMING",
         "GTA VI rolls out worldwide after a 13-year wait",
         "Rockstar's game unlocks at midnight local time, New Zealand "
         "first, on PS5 and Xbox Series X|S. Preorders top $1.5B; no PC "
         "version at launch."),
        ("US POLITICS",
         "Jeffries nominated 251\u201311, poised to be first Black Speaker",
         "House Democrats backed their leader in a closed-door vote; the "
         "floor vote is 3 January. Clark is set to be the first woman "
         "majority leader."),
        ("WEATHER",
         "Cyclone Akvan bears down on India's east coast",
         "Landfall due Friday on the Andhra coast, winds 100\u2013110 km/h; "
         "extremely heavy rain is likely today and tomorrow. Seven "
         "districts are on red alert."),
    ]
    gutter = 24
    col_w = (CONTENT - gutter) // 2
    f_tag = font("sans_b", 14)
    f_chead = font("sans_b", 18)
    f_cbody = font("sans", 15)
    row_h = 132
    for idx, (tag, headline, body) in enumerate(cards):
        col = idx % 2
        row = idx // 2
        x = SIDE + col * (col_w + gutter)
        cy = y + row * (row_h + 12)
        d.text((x, cy), tag, font=f_tag, fill=RED)
        cy += 18 + 3
        h_lines = wrap(d, headline, f_chead, col_w)
        assert len(h_lines) <= 2, f"card {idx + 1} headline needs {len(h_lines)} lines"
        cy = block(d, h_lines, x, cy, f_chead, INK, 23)
        cy += 3
        b_lines = wrap(d, body, f_cbody, col_w)
        assert len(b_lines) <= 3, f"card {idx + 1} body needs {len(b_lines)} lines"
        cy = block(d, b_lines, x, cy, f_cbody, GREY, 19)
        assert cy <= y + row * (row_h + 12) + row_h, f"card {idx + 1} overflows its row"
    y += 3 * row_h + 2 * 12

    # ---- In brief: 2 columns x 3 rows ----
    y += 10
    f_brief_h = font("sans_b", 16)
    d.text((SIDE, y), "IN BRIEF", font=f_brief_h, fill=INK)
    y += 20 + 5
    briefs = [
        ("PEW", "Islam projected to pass Christianity as the largest faith by 2035."),
        ("EUROPE", "EU proposes a \u20ac45B Ukraine loan, repaid only after Russian reparations."),
        ("SCIENCE", "Voyager 1 believed to have reached one light-day from Earth."),
        ("ESTONIA", "Estonia to shut its road border crossings with Russia from 1 Dec."),
        ("MARKETS", "Nvidia halts H-chip shipments to China; Fed points to more hikes."),
        ("YEMEN", "Houthis near Aden as government forces pull back from Bab el-Mandeb."),
    ]
    f_btag = font("sans_b", 15)
    f_bbody = font("sans", 15)
    brief_row_h = 42
    for idx, (tag, text) in enumerate(briefs):
        col = idx % 2
        row = idx // 2
        x = SIDE + col * (col_w + gutter)
        by = y + row * (brief_row_h + 8)
        end = mixed_para(d, tag + " \u2014", text, x, by, col_w,
                         f_btag, f_bbody, 19)
        assert end <= by + brief_row_h, f"brief {idx + 1} overflows its row"
    y += 3 * brief_row_h + 2 * 8

    # ---- Footer ----
    y += 14
    d.rectangle([SIDE, y, W - SIDE, y], fill=LIGHT_GREY)
    y += 1 + 7
    f_foot = font("sans", 15)
    foot = "All events of Thursday, 19 November 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, y), foot, font=f_foot, fill=GREY)
    y += 19

    assert y <= H, f"poster overflows: content ends at y={y}, height is {H}"
    img.save(OUT, format="PNG")
    print(f"{OUT} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
