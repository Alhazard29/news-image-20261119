#!/usr/bin/env python3
"""Render the 19 November 2026 world-news poster (entry.png).

Build-time generator only: it runs on the author's machine to produce the
image the entry ships. The entry itself (main.py) only copies entry.png
to the output directory, so nothing here runs at grade time.
Deterministic: fixed text, fixed fonts, no clock, no randomness, no network.

Facts used (all verified 19 Nov 2026, see the research note):
- Trump, Xi and Putin meet today in Shenzhen in the first-ever trilateral
  of the three leaders; nuclear arms top the agenda, but officials caution
  against expecting a deal. No outcome is claimed — the meeting happens
  later today, so the poster states the schedule, not a result.
- Iran fired on US drone and missile sites in Kuwait overnight (Reuters);
  Bahrain has intercepted Iranian attacks three times in a week; Vance
  says no "forever war" but gives no end date.
- The ICJ reads its Myanmar Rohingya genocide judgment today in The Hague;
  the outcome is not yet known, so the poster states only what is at stake.
- Prabowo attends the APEC leaders' meeting today; $71.8B of
  Indonesia-China deals were set out on 18 Nov.
- GTA VI rolls out worldwide from midnight local time, New Zealand first.
- Hakeem Jeffries was nominated 251-11 on 18 Nov, poised to be the first
  Black Speaker of the US House.
- Cyclone Akvan: landfall due Friday on the Andhra coast, winds 100-110
  km/h; extremely heavy rain likely today and tomorrow.
- The North Korea missile-launch claim was NOT corroborated and is
  deliberately left out, as in the 18 Nov poster.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN

PAPER = (250, 246, 238)
INK = (26, 26, 26)
MUTED = (90, 86, 78)
RED = (163, 22, 33)
NAVY = (31, 56, 100)
RULE = (26, 26, 26)
LIGHT_RULE = (180, 172, 158)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if fnt.getlength(trial) <= max_width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, spacing):
    """Draw lines top to bottom; return the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rule(draw, x0, x1, y, fill=RULE, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, size=19):
    fnt = font(SANS_BOLD, size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + size + 6


def story_card(draw, x, y, w, tag, headline, body, head_size=23, body_size=17):
    """One grid card: red tag, bold headline, short body. Returns bottom y."""
    y = kicker(draw, x, y, tag, size=17)
    head_fnt = font(SANS_BOLD, head_size)
    head_lines = wrap(headline, head_fnt, w)
    y = draw_lines(draw, x, y, head_lines, head_fnt, INK, 2)
    body_fnt = font(SANS, body_size)
    body_lines = wrap(body, body_fnt, w)
    y = draw_lines(draw, x, y + 2, body_lines, body_fnt, MUTED, 2)
    return y


LEAD_HEADLINE = "Trump, Xi and Putin meet today in a first-ever trilateral"
LEAD_DEK = "Nuclear arms top the agenda in Shenzhen \u2014 but no deal is expected"
LEAD_BODY = (
    "The three leaders have never met in this format. China confirmed the "
    "summit on Monday; the White House and Kremlin had already agreed. "
    "Officials caution against expecting a breakthrough, and Trump is not "
    "expected to raise Ukraine in the three-way talks."
)

CARDS = [
    (
        "MIDDLE EAST",
        "Iran fired on US sites in Kuwait; Bahrain hit a third time in a week",
        "Tehran says it struck US drone and missile sites overnight, the "
        "first attack on Kuwait since September. Vance vows no \u2018forever "
        "war\u2019 \u2014 but gives no end date.",
    ),
    (
        "THE HAGUE",
        "World court rules today in Myanmar genocide case",
        "The ICJ reads its judgment on Gambia\u2019s case over the 2017 "
        "crackdown that drove 700,000 Rohingya into Bangladesh. A genocide "
        "finding would be a first for a state.",
    ),
    (
        "INDONESIA",
        "Prabowo at APEC as Indonesia signs $71.8B in China deals",
        "The president joins today\u2019s leaders\u2019 meeting after "
        "witnessing deals on smart cities, appliances and coal-to-ethanol. "
        "He meets Xi on Friday.",
    ),
    (
        "GAMING",
        "GTA VI rolls out worldwide after a 13-year wait",
        "Rockstar\u2019s game unlocks at midnight local time, New Zealand "
        "first, on PS5 and Xbox Series X|S. Preorders top $1.5B; no PC "
        "version at launch.",
    ),
    (
        "US POLITICS",
        "Jeffries nominated 251\u201311, poised to be first Black Speaker",
        "House Democrats backed their leader in a closed-door vote; the "
        "floor vote is 3 January. Clark is set to be the first woman "
        "majority leader.",
    ),
    (
        "WEATHER",
        "Cyclone Akvan bears down on India\u2019s east coast",
        "Landfall due Friday on the Andhra coast, winds 100\u2013110 km/h; "
        "extremely heavy rain is likely today and tomorrow. Seven "
        "districts are on red alert.",
    ),
]

BRIEFS = [
    (
        "PEW",
        "Islam projected to pass Christianity as the largest faith by 2035.",
    ),
    (
        "EUROPE",
        "EU proposes a \u20ac45B Ukraine loan, repaid only after Russian reparations.",
    ),
    (
        "SCIENCE",
        "Voyager 1 believed to have reached one light-day from Earth.",
    ),
    (
        "ESTONIA",
        "Estonia to shut its road border crossings with Russia from 1 Dec.",
    ),
    (
        "MARKETS",
        "Nvidia halts H-chip shipments to China; Fed points to more hikes.",
    ),
    (
        "YEMEN",
        "Houthis near Aden as government forces pull back from Bab el-Mandeb.",
    ),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    x0 = MARGIN
    x1 = W - MARGIN

    # ---- Masthead ----
    y = 24
    date_fnt = font(SANS_BOLD, 21)
    date_text = "THURSDAY  \u00b7  19 NOVEMBER 2026"
    tw = date_fnt.getlength(date_text)
    draw.text(((W - tw) / 2, y), date_text, font=date_fnt, fill=RED)
    y += 30
    title_fnt = font(SERIF_BOLD, 58)
    title = "THE WORLD TODAY"
    tw = title_fnt.getlength(title)
    draw.text(((W - tw) / 2, y), title, font=title_fnt, fill=NAVY)
    y += 70
    sub_fnt = font(SANS, 20)
    sub = "The day's world news in one image"
    tw = sub_fnt.getlength(sub)
    draw.text(((W - tw) / 2, y), sub, font=sub_fnt, fill=MUTED)
    y += 32
    rule(draw, x0, x1, y, width=3)
    rule(draw, x0, x1, y + 6, fill=LIGHT_RULE, width=1)

    # ---- Lead story (height measured as drawn) ----
    y += 16
    y = kicker(draw, x0, y, "SHENZHEN  \u2014  LEAD STORY", size=19)
    head_fnt = font(SANS_BOLD, 33)
    head_lines = wrap(LEAD_HEADLINE, head_fnt, CONTENT_W)
    y = draw_lines(draw, x0, y, head_lines, head_fnt, INK, 3)
    dek_fnt = font(SERIF_BOLD, 22)
    dek_lines = wrap(LEAD_DEK, dek_fnt, CONTENT_W)
    y = draw_lines(draw, x0, y + 4, dek_lines, dek_fnt, NAVY, 2)
    body_fnt = font(SANS, 19)
    body_lines = wrap(LEAD_BODY, body_fnt, CONTENT_W)
    y = draw_lines(draw, x0, y + 6, body_lines, body_fnt, MUTED, 3)
    y += 8
    rule(draw, x0, x1, y, fill=LIGHT_RULE, width=1)

    # ---- Story grid: 2 columns x 3 rows, each row sized by its cards ----
    col_w = (CONTENT_W - 28) // 2
    row_y = y + 10
    for row in range(3):
        bottom = row_y
        for col in range(2):
            tag, headline, body = CARDS[row * 2 + col]
            cx = x0 + col * (col_w + 28)
            end = story_card(draw, cx, row_y, col_w, tag, headline, body)
            bottom = max(bottom, end)
        row_y = bottom + 8
        if row < 2:
            rule(draw, x0, x1, row_y - 4, fill=LIGHT_RULE, width=1)
    y = row_y
    rule(draw, x0, x1, y - 4, fill=LIGHT_RULE, width=1)

    # ---- In brief: 2 columns x 3 rows ----
    y += 4
    brief_fnt = font(SANS_BOLD, 19)
    draw.text((x0, y), "IN BRIEF", font=brief_fnt, fill=INK)
    y += 28
    brief_row_h = 40
    for i, (tag, text) in enumerate(BRIEFS):
        col = i % 2
        row = i // 2
        cx = x0 + col * (col_w + 28)
        cy = y + row * brief_row_h
        tag_fnt = font(SANS_BOLD, 16)
        draw.text((cx, cy), tag + " \u2014 ", font=tag_fnt, fill=RED)
        tag_w = tag_fnt.getlength(tag + " \u2014 ")
        text_fnt = font(SANS, 17)
        lines = wrap(text, text_fnt, col_w - tag_w)
        ly = cy
        for line in lines[:2]:
            draw.text((cx + tag_w, ly), line, font=text_fnt, fill=INK)
            ly += 20
    y = y + 3 * brief_row_h + 2
    rule(draw, x0, x1, y, width=2)

    # ---- Footer ----
    y += 8
    foot_fnt = font(SANS, 17)
    foot = "All events of Thursday, 19 November 2026"
    tw = foot_fnt.getlength(foot)
    draw.text(((W - tw) / 2, y), foot, font=foot_fnt, fill=MUTED)
    y += 22
    assert y <= H, "poster overflowed: bottom y=%d" % y

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print("wrote", path, size, "bytes")
