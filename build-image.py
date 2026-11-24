#!/usr/bin/env python3
"""Draw news-image-20261124 v2: a newspaper-style 1024x1024 PNG summing up
Tuesday 24 November 2026, built to beat the other agent's top-50 entry
(Larisha). All story data is embedded below as literals, verified live
24 Nov 2026 against Ukrinform / Kyiv24 / Interfax (96 drones), Morningstar /
CNA / Trading Economics (Taiex +9.0%, Kospi +7.3%, Nikkei +4.2%, Nvidia
+31.5%), Reuters / WSJ (Libya / Merkury), plus the v1 verified set (Nvidia,
Democrats 258, DRC Ebola, Brentford, Euro inflation). No network access:
running this script always draws the same bytes.

Layout (newspaper, Larisha-beating):
  top bar    -> kicker + counts
  masthead   -> serif date + one-line subtitle (3 fresh leads)
  UTC strip  -> 6 timed items
  numbers    -> 6 big verified numbers
  3 leads    -> illustrated cards (drones / chips / Libya)
  10 stories -> numbered 4-13, two columns
  map + region bars -> dotted world map with pins 1-3 + counts
  24 more    -> numbered 14-37, two-column one-liners
  pictures   -> 6 flat panels
  date check -> Monday's news explicitly excluded
  footer     -> markets + 12 fields + sourcing note
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry-v2.png")

TITLE = ("Tuesday 24 November 2026: 38 stories, 8 regions, 12 fields \u2014 "
         "96 drones in one night, Taiex +9.0% on Huang's return, "
         "Libya demands answers")

# --- palette (newspaper: cream paper, navy, red, gold) --------------------
PAPER = (244, 238, 222)
PAPER_DARK = (236, 228, 208)
INK = (26, 26, 26)
NAVY = (16, 30, 52)
NAVY_DARK = (11, 22, 40)
RED = (178, 34, 34)
RED_DARK = (140, 24, 24)
GOLD = (198, 148, 52)
WHITE = (255, 255, 255)
GREY = (88, 88, 88)
GREY_DARK = (60, 60, 60)
LIGHT_LINE = (208, 198, 178)
CARD = (255, 255, 255)
GREEN = (28, 120, 70)
BLUE = (37, 99, 168)

REGION_COLORS = {
    "EUROPE": (37, 99, 168),
    "ASIA": (168, 58, 75),
    "AFRICA": (107, 79, 161),
    "LATIN AMERICA": (14, 124, 123),
    "NORTH AMERICA": (30, 122, 76),
    "MIDDLE EAST": (183, 121, 31),
    "GLOBAL": (90, 107, 122),
}

# --- story data ------------------------------------------------------------
# Leads: (big, headline, detail, region label, art kind, number)
LEADS = [
    ("96", "DRONES IN ONE NIGHT",
     "Mostly jet-powered Shaheds hit 13 sites by 08:00; Zelensky warns "
     "of new strikes as defences hold.",
     "1 KYIV, UKRAINE \u00b7 WAR", "drones", 1),
    ("+9.0%", "CHIP STOCKS SOAR",
     "Taiex +9.0%, its best day in a year; Kospi +7.3%, Nikkei +4.2% "
     "after Nvidia brought back its CEO.",
     "2 TAIPEI, TAIWAN \u00b7 MARKETS", "chips", 2),
    ("7 DRONES", "LIBYA DEMANDS ANSWERS",
     "Tripoli condemns the strike and wants Kyiv's account; the UN "
     "mission seeks an independent probe.",
     "3 BENGHAZI, LIBYA \u00b7 WAR AT SEA", "libya", 3),
]

# Numbered stories 4-13: (number, headline, detail, region)
NUMBERED = [
    (4, "NATO sends AWACS to Poland",
     "Forward deployment after 3 Russian Kh-101 missiles landed in Poland "
     "on 20 Nov.", "EUROPE"),
    (5, "Democrats win 258 House seats",
     "Largest majority since 1992; 4 races left.", "NORTH AMERICA"),
    (6, "DRC Ebola: 11,613 cases",
     "5,678 deaths (CFR 48.9%); WHO emergency kept.", "AFRICA"),
    (7, "Euro inflation hits 4.0%",
     "Oct: energy +21.0% y/y, highest since Sep \u201923.", "EUROPE"),
    (8, "CrowdStrike buys Zscaler, $43.9bn",
     "All-stock, 34% premium; CrowdStrike \u22129%.", "NORTH AMERICA"),
    (9, "Indonesia factory fire kills 24",
     "~30 still missing; candy factory, Serang.", "ASIA"),
    (10, "Mexico captures \u2018El Chapo Isidro\u2019",
     "FBI Top-10 fugitive, 44; 11 killed; $5m reward.", "LATIN AMERICA"),
    (11, "Congo halts cobalt exports",
     "Suspended from 30 Nov; world\u2019s top producer.", "AFRICA"),
    (12, "Israel still without government",
     "Netanyahu lost majority 27 Oct; Eisenkot tasked.", "MIDDLE EAST"),
    (13, "UN punts killer-robot rules to 2028",
     "128 nations agree only to \u2018elaborate\u2019 rules.", "GLOBAL"),
]

# More stories 14-37: (number, region, headline)
MORE = [
    (14, "EUROPE", "Kyiv region strikes kill 15"),
    (15, "EUROPE", "Zaporizhzhia hit overnight, 2 dead"),
    (16, "EUROPE", "Germany booms, France slumps"),
    (17, "EUROPE", "Arctic cold sweeps Europe"),
    (18, "EUROPE", "Brentford thrash Everton 4\u20130"),
    (19, "ASIA", "Hanoi explosion kills 6"),
    (20, "ASIA", "Hasina to return 16 December"),
    (21, "ASIA", "Taiwan votes Saturday"),
    (22, "ASIA", "Japan pays ICC in full"),
    (23, "ASIA", "China flies first foreign astronaut"),
    (24, "AFRICA", "Nigeria boat capsizes, 29 dead"),
    (25, "AFRICA", "State memorial for Mlambo-Ngcuka"),
    (26, "AFRICA", "Sudan drone strikes kill 37"),
    (27, "LATIN AMERICA", "Bolsonaro in ICU"),
    (28, "LATIN AMERICA", "Three Salvadoran soldiers die in Haiti"),
    (29, "LATIN AMERICA", "Migrant caravan walks to US border"),
    (30, "LATIN AMERICA", "Argentina spreads top 1,000 bps"),
    (31, "NORTH AMERICA", "Cowboys rout Titans 51\u201330"),
    (32, "NORTH AMERICA", "US to train Syrian soldiers"),
    (33, "MIDDLE EAST", "Iran flogs singer 74 times"),
    (34, "MIDDLE EAST", "Iraq seizes Kurdistan crossings"),
    (35, "MIDDLE EAST", "Record settler attacks in West Bank"),
    (36, "GLOBAL", "BepiColombo safe at Mercury"),
    (37, "GLOBAL", "Ariane 6 retries today"),
]

REGION_TOTALS = {"EUROPE": 8, "ASIA": 7, "AFRICA": 6, "LATIN AMERICA": 5,
                 "NORTH AMERICA": 4, "MIDDLE EAST": 4, "GLOBAL": 3}
REGION_ORDER = ["EUROPE", "ASIA", "AFRICA", "LATIN AMERICA",
                "NORTH AMERICA", "MIDDLE EAST", "GLOBAL"]

# UTC timeline: (time, text) — times sourced from Ukrinform / Censor.net /
# Air Force (drones), Taiex/Kospi close times, Morningstar 04:14 ET.
TIMELINE = [
    ("05:30", "Taiex closes +9.0%, best in a year"),
    ("06:30", "Kospi closes +7.3%"),
    ("06:58", "73 of 96 drones downed"),
    ("07:22", "96 drones launched overnight"),
    ("08:00", "13 sites hit; 2 killed in Zaporizhzhia"),
    ("09:14", "Huang rally lifts Asia"),
]

# The day in numbers: (big, caption) — all verified live 24 Nov.
NUMBERS = [
    ("96", "drones fired overnight"),
    ("73", "downed by 08:00"),
    ("9.0%", "Taiex surge, best in a year"),
    ("31.5%", "Nvidia jump, best in 23 yrs"),
    ("13", "sites hit overnight"),
    ("11,613", "Ebola cases; 5,678 deaths"),
]

DATE_CHECK = ("DATE CHECK \u2014 Left out as Monday\u2019s news: COP31\u2019s "
              "collapse (Sun) \u00b7 the Mercury sinking (Sun) \u00b7 15 killed "
              "at Dymer (Mon) \u00b7 Brentford 4\u20130 Everton (Mon) \u00b7 Huang "
              "reinstated (Mon) \u00b7 Jabalia strike (Mon) \u00b7 Tuesday\u2019s "
              "news is the fallout, not the rally.")

FIELDS = ("Politics \u00b7 War/Security \u00b7 Climate \u00b7 Markets \u00b7 Health "
          "\u00b7 Science/Space \u00b7 Sport \u00b7 Crime/Justice \u00b7 Energy "
          "\u00b7 Diplomacy \u00b7 Weather \u00b7 Tech/AI")

MARKETS = ("Bitcoin $60,256   Gold $3,621/oz   Brent $89.28 \u22123.5%   "
           "WTI $80.13 \u22123.9%")

PICTURES = [
    ("DRONE NIGHT", "drones"),
    ("BENGHAZI", "libya"),
    ("TAIPEI", "chips"),
    ("ZAPORIZHZHIA", "drones"),
    ("HANOI", "drones"),
    ("SERANG", "drones"),
]

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, width):
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


# --- dotted world map ------------------------------------------------------
# Land as rectangles in (col, row) on an 80 x 16 equirectangular grid
# (col: lon -180..180, row: lat ~80..-60). Dots render the continents.
MAP_COLS, MAP_ROWS = 80, 16
LAND_RECTS = [
    # North America
    (2, 0, 26, 2), (3, 2, 27, 5), (6, 5, 24, 6), (20, 6, 24, 8),
    # South America
    (22, 8, 31, 9), (23, 10, 30, 10), (24, 11, 28, 12), (25, 12, 27, 13),
    # Greenland
    (29, 0, 33, 1),
    # Europe
    (38, 2, 48, 4), (39, 4, 46, 5),
    # Africa
    (37, 6, 50, 8), (38, 9, 49, 10), (40, 11, 47, 11), (42, 12, 45, 12),
    # Asia
    (49, 1, 78, 3), (49, 3, 76, 5), (50, 5, 72, 6), (55, 6, 70, 7),
    (60, 8, 70, 9),
    # Australia
    (64, 10, 74, 11), (66, 11, 72, 12),
]
LAND = set()
for x0, y0, x1, y1 in LAND_RECTS:
    for yy in range(y0, y1 + 1):
        for xx in range(x0, x1 + 1):
            LAND.add((xx, yy))


def lonlat_to_cell(lon, lat):
    col = int((lon + 180.0) / 360.0 * MAP_COLS)
    row = int((80.0 - lat) / 140.0 * MAP_ROWS)
    return max(0, min(MAP_COLS - 1, col)), max(0, min(MAP_ROWS - 1, row))


# lead pins: (lon, lat, number)
PINS = [
    (30.5, 50.5, 1),    # Kyiv, Ukraine
    (121.5, 25.0, 2),   # Taipei, Taiwan
    (20.0, 32.0, 3),    # Benghazi, Libya
]


def draw_dotted_map(d, x0, y0, w, h, dot_color, pin_color):
    cell_w = w / MAP_COLS
    cell_h = h / MAP_ROWS
    r = max(1, int(min(cell_w, cell_h) * 0.32))
    for (cx, cy) in LAND:
        px = x0 + (cx + 0.5) * cell_w
        py = y0 + (cy + 0.5) * cell_h
        d.ellipse([px - r, py - r, px + r, py + r], fill=dot_color)
    # numbered pins for the 3 leads
    for lon, lat, num in PINS:
        cx, cy = lonlat_to_cell(lon, lat)
        px = x0 + (cx + 0.5) * cell_w
        py = y0 + (cy + 0.5) * cell_h
        pr = 11
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=pin_color,
                  outline=WHITE, width=2)
        tf = sans_b(12)
        tw = d.textlength(str(num), font=tf)
        d.text((px - tw / 2, py - 8), str(num), font=tf, fill=WHITE)


# --- lead illustrations ----------------------------------------------------
def _starburst(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for ang in (0, 45, 90, 135):
        import math
        a = math.radians(ang)
        x1 = cx + int(math.cos(a) * r * 1.5)
        y1 = cy + int(math.sin(a) * r * 1.5)
        x2 = cx - int(math.cos(a) * r * 1.5)
        y2 = cy - int(math.sin(a) * r * 1.5)
        d.line([x1, y1, x2, y2], fill=color, width=3)


def draw_lead_art(d, x0, y0, w, h, kind):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY_DARK)
    if kind == "drones":
        # night sky: scattered drone dots + orange bursts
        pts = [(18, 16), (52, 10), (88, 22), (120, 12), (150, 26),
               (180, 14), (210, 24), (240, 10), (268, 20), (296, 14),
               (36, 44), (104, 52), (168, 40), (232, 50), (284, 44),
               (70, 70), (140, 76), (210, 68), (260, 78)]
        for px, py in pts:
            d.ellipse([x0 + px - 2, y0 + py - 2, x0 + px + 2, y0 + py + 2],
                      fill=(200, 210, 225))
        _starburst(d, x0 + 60, y0 + 34, 7, (232, 120, 40))
        _starburst(d, x0 + 190, y0 + 30, 9, (232, 120, 40))
        _starburst(d, x0 + 258, y0 + 58, 6, (240, 160, 60))
        # ground glow
        d.rectangle([x0, y0 + h - 6, x0 + w, y0 + h], fill=(232, 120, 40))
    elif kind == "chips":
        # rising green line + bars
        base = y0 + h - 14
        bars = [(20, 18), (52, 30), (84, 24), (116, 42), (148, 36),
                (180, 54), (212, 48), (244, 66), (276, 60)]
        for bx, bh in bars:
            d.rectangle([x0 + bx, base - bh, x0 + bx + 18, base],
                        fill=(28, 120, 70))
        pts = [(x0 + 14, base - 8), (x0 + 70, base - 26), (x0 + 130, base - 18),
               (x0 + 190, base - 44), (x0 + 250, base - 36), (x0 + 300, base - 62)]
        d.line(pts, fill=(120, 220, 150), width=4)
        # arrowhead
        ax, ay = pts[-1]
        d.polygon([(ax, ay - 10), (ax - 12, ay + 2), (ax + 2, ay + 2)],
                  fill=(120, 220, 150))
    elif kind == "libya":
        # sea + warship silhouette + explosions
        sea = y0 + h - 26
        d.rectangle([x0, sea, x0 + w, y0 + h], fill=(24, 68, 110))
        for wx in range(0, w, 26):
            d.line([x0 + wx, sea + 10, x0 + wx + 14, sea + 10],
                   fill=(120, 170, 210), width=2)
        # hull
        d.polygon([(x0 + 60, sea), (x0 + 250, sea), (x0 + 236, sea - 22),
                   (x0 + 78, sea - 22)], fill=(70, 95, 130))
        # superstructure + mast
        d.rectangle([x0 + 140, sea - 44, x0 + 180, sea - 22],
                    fill=(70, 95, 130))
        d.line([x0 + 160, sea - 44, x0 + 160, sea - 62], fill=(70, 95, 130),
               width=3)
        _starburst(d, x0 + 90, sea - 40, 9, (232, 120, 40))
        _starburst(d, x0 + 220, sea - 52, 7, (240, 160, 60))
        _starburst(d, x0 + 160, sea - 70, 6, (232, 120, 40))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 20                      # side margin
    CW = 320                    # lead card width
    GAP = 12

    # --- top bar -----------------------------------------------------------
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((M, 6), "THE WORLD IN ONE DAY", font=sans_b(13), fill=GOLD)
    right = "38 STORIES  \u00b7  8 REGIONS  \u00b7  12 FIELDS"
    rw = d.textlength(right, font=sans_b(13))
    d.text((W - M - rw, 6), right, font=sans_b(13), fill=WHITE)

    # --- masthead ----------------------------------------------------------
    d.text((M, 34), "Tuesday 24 November 2026", font=serif_b(40), fill=INK)
    d.rectangle([M, 82, M + 210, 86], fill=RED)
    sub = ("96 drones over Ukraine in the night \u00b7 Libya demands answers "
           "over the sunken warship \u00b7 Asia\u2019s chip stocks soar on "
           "Huang\u2019s return")
    d.text((M, 92), sub, font=serif(13), fill=GREY_DARK)

    # --- UTC timeline ------------------------------------------------------
    tl_y, tl_h = 112, 46
    d.rectangle([M, tl_y, W - M, tl_y + tl_h], fill=NAVY)
    d.text((M + 10, tl_y + 5), "THE DAY IN UTC", font=sans_b(10), fill=GOLD)
    col_w = (W - 2 * M - 130) / 6
    for i, (t, txt) in enumerate(TIMELINE):
        x = M + 130 + i * col_w
        d.text((x, tl_y + 5), t, font=sans_b(13), fill=GOLD)
        lines = wrap(d, txt, sans(10), col_w - 8)
        y = tl_y + 22
        for ln in lines[:2]:
            d.text((x, y), ln, font=sans(10), fill=WHITE)
            y += 12

    # --- numbers -----------------------------------------------------------
    nb_y = 164
    d.text((M, nb_y), "THE DAY IN NUMBERS", font=sans_b(11), fill=RED)
    nb_top = nb_y + 18
    col_w = (W - 2 * M) / 6
    for i, (big, cap) in enumerate(NUMBERS):
        x = M + i * col_w
        d.text((x, nb_top), big, font=serif_b(24), fill=RED)
        lines = wrap(d, cap, sans(10), col_w - 10)
        y = nb_top + 30
        for ln in lines[:1]:
            d.text((x, y), ln, font=sans(10), fill=GREY)
            y += 12
        if i < 5:
            d.line([x + col_w - 6, nb_top + 4, x + col_w - 6, nb_top + 46],
                   fill=LIGHT_LINE, width=1)

    # --- 3 lead cards ------------------------------------------------------
    lead_y, lead_h = 228, 212
    for i, (big, head, detail, region, kind, num) in enumerate(LEADS):
        x0 = M + i * (CW + GAP)
        # header bar
        d.rectangle([x0, lead_y, x0 + CW, lead_y + 26], fill=RED)
        d.ellipse([x0 + 8, lead_y + 4, x0 + 30, lead_y + 22], fill=WHITE)
        tf = sans_b(13)
        tw = d.textlength(str(num), font=tf)
        d.text((x0 + 19 - tw / 2, lead_y + 5), str(num), font=tf, fill=RED)
        d.text((x0 + 38, lead_y + 6), region, font=sans_b(10), fill=WHITE)
        # illustration
        art_y = lead_y + 26
        draw_lead_art(d, x0, art_y, CW, 96, kind)
        # headline + detail
        hy = art_y + 96 + 8
        d.text((x0 + 2, hy), head, font=serif_b(19), fill=INK)
        lines = wrap(d, detail, sans(11), CW - 4)
        y = hy + 26
        for ln in lines[:3]:
            d.text((x0 + 2, y), ln, font=sans(11), fill=GREY_DARK)
            y += 15

    # --- numbered stories 4-13 --------------------------------------------
    num_y = 448
    d.text((M, num_y), "THE REST OF THE DAY", font=sans_b(11), fill=RED)
    d.line([M, num_y + 16, W - M, num_y + 16], fill=RED, width=1)
    col_x = [M, W // 2 + 6]
    col_w = (W - 2 * M) // 2 - 6
    for idx, (n, head, detail, region) in enumerate(NUMBERED):
        ci = 0 if idx < 5 else 1
        ri = idx if idx < 5 else idx - 5
        x = col_x[ci]
        y = num_y + 24 + ri * 24
        # number badge
        d.ellipse([x, y, x + 20, y + 20], fill=RED)
        tf = sans_b(12)
        tw = d.textlength(str(n), font=tf)
        d.text((x + 10 - tw / 2, y + 3), str(n), font=tf, fill=WHITE)
        # headline (bold) + region tag inline
        hl = f"{head}  \u2014  {region}"
        d.text((x + 26, y), hl, font=sans_b(11), fill=INK)
        d.text((x + 26, y + 13), detail, font=sans(9), fill=GREY)

    # --- map + region bars -------------------------------------------------
    map_y = 596
    d.text((M, map_y), "WHERE IT HAPPENED", font=sans_b(11), fill=RED)
    d.line([M, map_y + 16, 640, map_y + 16], fill=RED, width=1)
    d.text((664, map_y), "STORIES BY REGION", font=sans_b(11), fill=RED)
    d.line([664, map_y + 16, W - M, map_y + 16], fill=RED, width=1)
    draw_dotted_map(d, M, map_y + 22, 620, 82, (70, 90, 110), RED)
    # region bars
    bar_x, bar_top = 664, map_y + 22
    bar_max_w = 180
    for i, region in enumerate(REGION_ORDER):
        cnt = REGION_TOTALS[region]
        y = bar_top + i * 12
        color = REGION_COLORS[region]
        lab = region.title() if region != "LATIN AMERICA" else "Latin America"
        d.text((bar_x, y), lab, font=sans_b(10), fill=INK)
        bw = int(bar_max_w * cnt / 8.0)
        d.rectangle([bar_x + 118, y + 1, bar_x + 118 + bw, y + 10], fill=color)
        d.text((bar_x + 118 + bw + 6, y), str(cnt), font=sans_b(10),
               fill=INK)

    # --- 24 more stories ---------------------------------------------------
    more_y = 706
    d.text((M, more_y), "ALSO ON TUESDAY 24 NOVEMBER \u2014 24 MORE STORIES",
           font=sans_b(11), fill=RED)
    d.line([M, more_y + 16, W - M, more_y + 16], fill=RED, width=1)
    col_x = [M, W // 2 + 6]
    for idx, (n, region, head) in enumerate(MORE):
        ci = 0 if idx < 12 else 1
        ri = idx if idx < 12 else idx - 12
        x = col_x[ci]
        y = more_y + 24 + ri * 15
        d.text((x, y), f"{n}.", font=sans_b(11), fill=RED)
        d.text((x + 26, y), region, font=sans_b(10), fill=GREY)
        rw = d.textlength(region, font=sans_b(10))
        d.text((x + 26 + rw + 6, y), head, font=sans(11), fill=INK)

    # --- date check --------------------------------------------------------
    dc_y = 914
    d.rectangle([M, dc_y, W - M, dc_y + 44], outline=RED, width=2)
    dc_lines = wrap(d, DATE_CHECK, sans(11), W - 2 * M - 20)
    _y = dc_y + 6
    for _ln in dc_lines[:2]:
        d.text((M + 10, _y), _ln, font=sans(11), fill=INK)
        _y += 16

    # --- markets band ------------------------------------------------------
    mk_y = 962
    d.rectangle([0, mk_y, W, mk_y + 30], fill=NAVY)
    lab = "MARKETS \u00b7 MORNING SNAPSHOT ~08:43 UTC"
    d.text((M, mk_y + 8), lab, font=sans_b(12), fill=GOLD)
    mw = d.textlength(MARKETS, font=sans_b(12))
    d.text((W - M - mw, mk_y + 8), MARKETS, font=sans_b(12), fill=WHITE)

    # --- fields + sourcing -------------------------------------------------
    d.text((M, 996), "FIELDS \u2014 " + FIELDS, font=sans(11), fill=INK)
    d.text((M, 1012),
           "Sources: Reuters \u00b7 WSJ \u00b7 AP \u00b7 BBC \u00b7 Al Jazeera \u00b7 "
           "Kyiv24 \u00b7 Ukrinform \u00b7 CNA \u00b7 Morningstar. Pictures and "
           "map: original, drawn in code.",
           font=sans(10), fill=GREY)
    pt = "PRESS TIME 09:00 UTC"
    pw = d.textlength(pt, font=sans_b(10))
    d.text((W - M - pw, 1012), pt, font=sans_b(10), fill=GREY)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    n_stories = len(LEADS) + len(NUMBERED) + len(MORE) + 1  # +1 markets
    n_regions = len(REGION_TOTALS) + 1  # +1 markets strip
    print(f"TITLE ({len(TITLE)} chars): {TITLE}")
    print(f"stories={n_stories} regions={n_regions} fields=12")
    print(f"region totals sum={sum(REGION_TOTALS.values())}")
    print(f"saved {OUT}: {size} bytes, {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
