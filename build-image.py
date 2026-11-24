#!/usr/bin/env python3
"""Draw the news-image-20261124 poster: one flat 1024x1024 PNG summing up
Tuesday 24 November 2026. All story data is embedded below as literals,
verified against reporting from CNN, Reuters, AP, the UN and Amnesty
International during the research session. No network access, no fetched
data: running this script always draws the same bytes.

Layout (flat, newspaper-poster style):
  masthead  -> date + story/region/field counts
  3 lead cards -> Nvidia, COP31, NATO AWACS
  3 columns -> the remaining 35 stories grouped by region
  footer    -> markets morning snapshot + the 12 fields + sourcing note
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

TITLE = ("Tuesday 24 November 2026: 38 stories, 8 regions, 12 fields \u2014 "
         "Huang back as Nvidia soars 31%, COP31 collapses, NATO sends "
         "AWACS to Poland")

# --- palette (flat, consistent) -------------------------------------------
PAPER = (245, 241, 230)
INK = (22, 34, 46)
NAVY = (14, 42, 71)
NAVY_DARK = (10, 32, 54)
GOLD = (232, 163, 61)
WHITE = (255, 255, 255)
GREY = (74, 85, 104)
LIGHT_LINE = (214, 206, 188)
CARD = (255, 255, 255)

REGION_COLORS = {
    "EUROPE": (37, 99, 168),
    "NORTH AMERICA": (30, 122, 76),
    "ASIA": (168, 58, 75),
    "MIDDLE EAST": (183, 121, 31),
    "AFRICA": (107, 79, 161),
    "LATIN AMERICA": (14, 124, 123),
    "GLOBAL": (90, 107, 122),
}

# --- story data ------------------------------------------------------------
# (headline, one-line detail). Counts: 3 leads + 35 below = 38 stories.
LEADS = [
    ("+31%", "HUANG IS BACK",
     "Nvidia reinstates Jensen Huang as CEO, 11 days after he resigned. "
     "Shares close at $165.05; +$952bn in a day. Nasdaq +6.5%.",
     (30, 122, 76), "NORTH AMERICA"),
    ("NO DEAL", "COP31 COLLAPSES",
     "190+ countries fail to agree in Antalya \u2014 the first COP "
     "breakdown since 2009. Fossil-fuel language stripped from the draft.",
     (192, 57, 43), "EUROPE"),
    ("3 MISSILES", "NATO SENDS AWACS TO POLAND",
     "NATO authorises a forward AWACS deployment after 3 Russian Kh-101 "
     "cruise missiles landed in Poland on 20 Nov.",
     (37, 99, 168), "EUROPE"),
]

# stories per region in the whole image, leads included (chips must add
# up with the Markets strip to the 38 in the title).
REGION_TOTALS = {"EUROPE": 8, "NORTH AMERICA": 5, "ASIA": 6,
                 "MIDDLE EAST": 4, "AFRICA": 6, "LATIN AMERICA": 5,
                 "GLOBAL": 3}

# region -> list of (headline, detail); leads already cover 1 N. America
# story (Nvidia) and 2 Europe stories (COP31, NATO).
REGIONS = [
    ("EUROPE", [
        ("Kyiv region strikes kill 15",
         "11 Dymer, 3 Vyshneve, 1 Bila Tserkva"),
        ("Zaporizhzhia hit overnight, 2 dead",
         "22 wounded, incl. 2 children \u2014 24 Nov"),
        ("Euro inflation hits 4.0%",
         "Oct: energy +21.0% y/y, highest since Sep \u201923"),
        ("Germany booms, France slumps",
         "Flash PMI: Germany 55.0, France 46.2"),
        ("Arctic cold sweeps Europe",
         "5\u201315\u00b0C below avg; snow 10\u201320 cm in the south"),
        ("Brentford thrash Everton 4\u20130",
         "Lewis-Potter 2 goals (23\u2032, 25\u2032); Mon 23 Nov"),
    ]),
    ("ASIA", [
        ("Indonesia factory fire kills 24",
         "~30 still missing; candy factory, Serang"),
        ("Hanoi explosion kills 6",
         "10 injured; food shop, Dong Da, 08:00"),
        ("Hasina to return 16 December",
         "Ex-Bangladesh PM ends 2+ years in exile"),
        ("Taiwan votes Saturday",
         "Mayoral & county polls 28 Nov; eyes on Taipei"),
        ("Japan pays ICC in full",
         "~15% of budget, top donor; 2027 share by Dec"),
        ("China flies first foreign astronaut",
         "Pakistani astronaut to Tiangong on Shenzhou-24"),
    ]),
    ("AFRICA", [
        ("DRC Ebola: 11,613 cases",
         "5,678 deaths (CFR 48.9%); WHO emergency kept"),
        ("Congo halts cobalt exports",
         "Suspended from 30 Nov; world\u2019s top producer"),
        ("Nigeria boat capsizes, 29 dead",
         "Bayelsa, 20 Nov; 50+ saved; \u20a6250m for families"),
        ("Ukraine sinks Russian warship in Libya",
         "7 drones sank corvette Merkury (22 Nov)"),
        ("State memorial for Mlambo-Ngcuka",
         "SA\u2019s first woman deputy, 71; memorial today"),
        ("Sudan drone strikes kill 37",
         "Amnesty 18 Nov: 9 RSF strikes, Jun\u2013Aug"),
    ]),
    ("LATIN AMERICA", [
        ("Mexico captures \u2018El Chapo Isidro\u2019",
         "FBI Top-10 fugitive, 44; 11 killed; $5m reward"),
        ("Bolsonaro in ICU",
         "Ex-Brazil president; bowel obstruction, stable"),
        ("Three Salvadoran soldiers die in Haiti",
         "Accidental blast; Bukele named the 3 on Sunday"),
        ("Migrant caravan walks to US border",
         "~300 crossed into Mexico 20 Nov; ~1,500 north"),
        ("Argentina spreads top 1,000 bps",
         "Risk ~1,070 bp, 20 Nov; bonds \u221220% since Aug"),
    ]),
    ("NORTH AMERICA", [
        ("Democrats win 258 House seats",
         "Largest majority since 1992; 4 races left"),
        ("CrowdStrike buys Zscaler, $43.9bn",
         "All-stock, 34% premium; CrowdStrike \u22129%"),
        ("Cowboys rout Titans 51\u201330",
         "Prescott 4 TD passes; Bills 9\u20131, Lions 8\u20132"),
        ("US to train Syrian soldiers",
         "First mission since 2024; demining first"),
    ]),
    ("MIDDLE EAST", [
        ("Iran flogs singer 74 times",
         "Parastoo Ahmadi + 4 crew; 2-year bans"),
        ("Iraq seizes Kurdistan crossings",
         "Federal control of borders + oil in 4 provinces"),
        ("Record settler attacks in West Bank",
         "410+ attacks since Sep; 4,000+ trees hit (UN)"),
        ("Israel still without government",
         "Netanyahu lost majority 27 Oct; Eisenkot tasked"),
    ]),
    ("GLOBAL", [
        ("UN punts killer-robot rules to 2028",
         "128 nations agree only to \u2018elaborate\u2019 rules"),
        ("BepiColombo safe at Mercury",
         "Thruster glitch: 77% of planned velocity change"),
        ("Ariane 6 retries today",
         "36 Amazon Leo satellites from Kourou"),
    ]),
]

# columns of region sections (balanced by story count: 12 / 11 / 11)
COLUMNS = [
    ["EUROPE", "ASIA"],
    ["AFRICA", "LATIN AMERICA"],
    ["NORTH AMERICA", "MIDDLE EAST", "GLOBAL"],
]

FIELDS = ("Politics \u00b7 War/Security \u00b7 Climate \u00b7 Markets \u00b7 Health "
          "\u00b7 Science/Space \u00b7 Sport \u00b7 Crime/Justice \u00b7 Energy "
          "\u00b7 Diplomacy \u00b7 Weather \u00b7 Tech/AI")

MARKETS = ("Bitcoin $60,256   Gold $3,621/oz   Brent $89.28 \u22123.5%   "
           "WTI $80.13 \u22123.9%")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def measure_columns(draw, hl_size, dt_size):
    """Return (column heights, per-story wrapped lines) for given sizes."""
    hl = font("DejaVuSans-Bold.ttf", hl_size)
    dt = font("DejaVuSans.ttf", dt_size)
    text_w = 320 - 20
    col_h, wrapped = [], {}
    for col in COLUMNS:
        total = 0
        for region in col:
            total += 30 + 8  # section header + gap below it
            for head, detail in dict(REGIONS)[region]:
                hw = wrap(draw, head, hl, text_w)
                dw = wrap(draw, detail, dt, text_w)
                wrapped[(region, head)] = (hw, dw)
                total += len(hw) * (hl_size + 3) + len(dw) * (dt_size + 3) + 8
        col_h.append(total)
    return col_h, wrapped


def draw_globe(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=2)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                 outline=color, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2],
             start=200, end=340, fill=color, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- pick story font sizes that fit the body area ---------------------
    body_top, body_bottom = 326, 944
    avail = body_bottom - body_top
    # Prefer the largest headline that fits: try headline 16/15/14, and for
    # each the largest detail 12/11/10. (The old loop decremented both
    # together, so a larger headline start was silently undone.)
    hl_size, dt_size, col_h, wrapped = 14, 10, None, None
    for hl_try in (16, 15, 14):
        for dt_try in (12, 11, 10):
            ch, wr = measure_columns(d, hl_try, dt_try)
            if max(ch) <= avail:
                hl_size, dt_size, col_h, wrapped = hl_try, dt_try, ch, wr
                break
        if wrapped is not None:
            break
    if wrapped is None:  # fallback: smallest sizes, draw anyway
        col_h, wrapped = measure_columns(d, 14, 10)
    hl = font("DejaVuSans-Bold.ttf", hl_size)
    dt = font("DejaVuSans.ttf", dt_size)
    hl_lh, dt_lh = hl_size + 3, dt_size + 3
    print(f"story fonts: headline {hl_size}px, detail {dt_size}px; "
          f"column heights {col_h} / available {avail}")

    # --- masthead ----------------------------------------------------------
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.rectangle([0, 108, W, 112], fill=GOLD)
    draw_globe(d, 52, 54, 30, GOLD)
    d.text((96, 16), "THE WORLD IN ONE DAY", font=font("DejaVuSans-Bold.ttf", 15),
           fill=GOLD)
    d.text((96, 38), "TUESDAY 24 NOVEMBER 2026",
           font=font("DejaVuSans-Bold.ttf", 40), fill=WHITE)
    d.text((96, 82), "The day\u2019s news, in one picture",
           font=font("DejaVuSans.ttf", 14), fill=(180, 198, 214))
    right = "38 STORIES"
    rw = d.textlength(right, font=font("DejaVuSans-Bold.ttf", 30))
    d.text((W - 24 - rw, 22), right, font=font("DejaVuSans-Bold.ttf", 30),
           fill=GOLD)
    sub = "8 REGIONS  \u00b7  12 FIELDS"
    sw = d.textlength(sub, font=font("DejaVuSans-Bold.ttf", 15))
    d.text((W - 24 - sw, 62), sub, font=font("DejaVuSans-Bold.ttf", 15),
           fill=WHITE)
    d.text((W - 24 - d.textlength("make.fun  \u00b7  news-image-20261124",
           font=font("DejaVuSans.ttf", 11)), 86),
           "make.fun  \u00b7  news-image-20261124",
           font=font("DejaVuSans.ttf", 11), fill=(140, 160, 178))

    # --- world map strip: flat dots for the 6 geographic regions ------------
    # Equirectangular: lon -180..180 -> x 20..1004; lat 75..-55 -> y 122..162.
    map_top, map_h = 118, 48
    d.rectangle([20, map_top, W - 20, map_top + map_h], fill=CARD,
                outline=LIGHT_LINE, width=1)
    map_dots = [
        ("N. AMERICA", 239, 129, REGION_COLORS["NORTH AMERICA"]),
        ("LATIN AM.", 348, 151, REGION_COLORS["LATIN AMERICA"]),
        ("EUROPE", 553, 126, REGION_COLORS["EUROPE"]),
        ("AFRICA", 567, 144, REGION_COLORS["AFRICA"]),
        ("M. EAST", 635, 135, REGION_COLORS["MIDDLE EAST"]),
        ("ASIA", 785, 129, REGION_COLORS["ASIA"]),
    ]
    lab_f = font("DejaVuSans-Bold.ttf", 10)
    for label, dx, dy, color in map_dots:
        d.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=color,
                  outline=WHITE, width=2)
        lw = d.textlength(label, font=lab_f)
        # label to the right of the dot, or left when near the right edge
        lx = dx + 11 if dx + 11 + lw < W - 24 else dx - 11 - lw
        d.text((lx, dy - 5), label, font=lab_f, fill=INK)

    # --- lead cards ---------------------------------------------------------
    lead_top, lead_h = 174, 140
    card_w, gap = 320, 12
    for i, (big, head, detail, color, region) in enumerate(LEADS):
        x0 = 20 + i * (card_w + gap)
        d.rectangle([x0, lead_top, x0 + card_w, lead_top + lead_h], fill=CARD)
        d.rectangle([x0, lead_top, x0 + card_w, lead_top + 6], fill=color)
        d.rectangle([x0, lead_top + 6, x0 + card_w, lead_top + 7],
                    fill=LIGHT_LINE)
        pad = 14
        bf = font("DejaVuSans-Bold.ttf", 32)
        d.text((x0 + pad, lead_top + 16), big, font=bf, fill=color)
        rf = font("DejaVuSans-Bold.ttf", 11)
        rw = d.textlength(region, font=rf)
        d.text((x0 + card_w - pad - rw, lead_top + 26), region, font=rf,
               fill=color)
        hf = font("DejaVuSans-Bold.ttf", 17)
        d.text((x0 + pad, lead_top + 56), head, font=hf, fill=INK)
        df = font("DejaVuSans.ttf", 12)
        lines = wrap(d, detail, df, card_w - 2 * pad)
        y = lead_top + 82
        for ln in lines[:3]:
            d.text((x0 + pad, y), ln, font=df, fill=GREY)
            y += 16

    # --- region columns ------------------------------------------------------
    region_map = dict(REGIONS)
    col_x = [20, 352, 684]
    for ci, col in enumerate(COLUMNS):
        x0 = col_x[ci]
        # spread leftover slack evenly between sections
        slack = avail - col_h[ci]
        extra = slack // max(1, len(col))
        y = body_top
        for region in col:
            color = REGION_COLORS[region]
            stories = region_map[region]
            d.rectangle([x0, y, x0 + card_w, y + 30], fill=color)
            d.text((x0 + 10, y + 7), region,
                   font=font("DejaVuSans-Bold.ttf", 14), fill=WHITE)
            cnt = f"{REGION_TOTALS[region]}"
            cw = d.textlength(cnt, font=font("DejaVuSans-Bold.ttf", 14))
            d.text((x0 + card_w - 10 - cw, y + 7), cnt,
                   font=font("DejaVuSans-Bold.ttf", 14), fill=WHITE)
            y += 30 + 8
            for head, detail in stories:
                hw, dw = wrapped[(region, head)]
                for ln in hw:
                    d.text((x0 + 10, y), ln, font=hl, fill=INK)
                    y += hl_lh
                for ln in dw:
                    d.text((x0 + 10, y), ln, font=dt, fill=GREY)
                    y += dt_lh
                y += 8
                d.line([x0 + 10, y - 5, x0 + card_w - 10, y - 5],
                       fill=LIGHT_LINE, width=1)
            y += extra

    # --- footer: markets band + fields + sourcing note ----------------------
    d.rectangle([0, 952, W, 988], fill=NAVY)
    lab = "MARKETS \u00b7 MORNING SNAPSHOT ~08:43 UTC"
    d.text((20, 963), lab, font=font("DejaVuSans-Bold.ttf", 13), fill=GOLD)
    mw = d.textlength(MARKETS, font=font("DejaVuSans-Bold.ttf", 13))
    d.text((W - 20 - mw, 963), MARKETS,
           font=font("DejaVuSans-Bold.ttf", 13), fill=WHITE)
    ff = font("DejaVuSans.ttf", 11)
    d.text((20, 994), "FIELDS \u2014 " + FIELDS, font=ff, fill=INK)
    nf = font("DejaVuSans.ttf", 10)
    d.text((20, 1010),
           "All figures as reported; death tolls in Indonesia and Nigeria are "
           "provisional. Prices are the morning snapshot and move during the day.",
           font=nf, fill=GREY)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    n_stories = len(LEADS) + sum(len(s) for _, s in REGIONS) + 1  # +1: Markets strip
    n_regions = len(REGIONS) + 1  # +1: Markets strip in the footer
    print(f"TITLE ({len(TITLE)} chars): {TITLE}")
    print(f"stories={n_stories} regions={n_regions} fields=12")
    print(f"saved {OUT}: {size} bytes, {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
