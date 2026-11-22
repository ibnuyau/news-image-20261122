"""World news front page for Sunday 22 November 2026.

Draws a 1024x1024 newspaper front page with Python + PIL: a masthead,
one large lead story, a grid of twelve stories with small hand-drawn
pictograms, an "also today" strip and a footer. Everything is drawn
with real text and simple shapes; there is no network access and no
randomness, so running the script twice writes identical bytes.
"""

import hashlib
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
INK = (25, 25, 25)
RED = (139, 0, 0)
GREY = (100, 100, 100)
RULE = (180, 180, 180)
LIGHT = (235, 235, 235)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, text, font, x, y, max_w, leading, color=INK, max_lines=None):
    """Draw wrapped text, return the y just below the last line."""
    lines = wrap(draw, text, font, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font, fill=color)
        y += leading
    return y


# ---------------------------------------------------------------- icons
# Each icon draws inside the square (x, y, s) with the given colour.

def ico_globe(d, x, y, s, c):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=c, width=2)
    d.line([x + s * 0.08, cy, x + s * 0.92, cy], fill=c, width=2)
    d.line([x + s * 0.2, cy - r * 0.62, x + s * 0.8, cy - r * 0.62], fill=c, width=2)
    d.line([x + s * 0.2, cy + r * 0.62, x + s * 0.8, cy + r * 0.62], fill=c, width=2)


def ico_missile(d, x, y, s, c):
    d.polygon([(x + s * 0.5, y + s * 0.05), (x + s * 0.68, y + s * 0.45),
               (x + s * 0.5, y + s * 0.38), (x + s * 0.32, y + s * 0.45)],
              outline=c, width=3)
    d.line([x + s * 0.5, y + s * 0.4, x + s * 0.5, y + s * 0.7], fill=c, width=3)
    d.polygon([(x + s * 0.32, y + s * 0.55), (x + s * 0.5, y + s * 0.7),
               (x + s * 0.68, y + s * 0.55)], outline=c, width=2)
    d.polygon([(x + s * 0.42, y + s * 0.72), (x + s * 0.5, y + s * 0.95),
               (x + s * 0.58, y + s * 0.72)], fill=c)


def ico_drone(d, x, y, s, c):
    cx, cy = x + s / 2, y + s / 2
    d.rectangle([cx - s * 0.12, cy - s * 0.1, cx + s * 0.12, cy + s * 0.1],
                outline=c, width=2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            rx, ry = cx + sx * s * 0.32, cy + sy * s * 0.3
            d.line([cx, cy, rx, ry], fill=c, width=2)
            d.ellipse([rx - s * 0.13, ry - s * 0.06, rx + s * 0.13, ry + s * 0.06],
                      outline=c, width=2)


def ico_star(d, x, y, s, c):
    cx, cy = x + s / 2, y + s / 2
    pts = []
    for i in range(10):
        r = s * 0.46 if i % 2 == 0 else s * 0.19
        a = math.pi * i / 5 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, outline=c, width=2)


def ico_flag(d, x, y, s, c):
    d.rectangle([x + s * 0.1, y + s * 0.15, x + s * 0.9, y + s * 0.85], fill=c)
    d.rectangle([x + s * 0.32, y + s * 0.15, x + s * 0.44, y + s * 0.85], fill=(255, 255, 255))
    d.rectangle([x + s * 0.1, y + s * 0.42, x + s * 0.9, y + s * 0.58], fill=(255, 255, 255))
    d.line([x + s * 0.1, y + s * 0.15, x + s * 0.1, y + s * 0.98], fill=c, width=3)


def ico_robot(d, x, y, s, c):
    d.rounded_rectangle([x + s * 0.18, y + s * 0.22, x + s * 0.82, y + s * 0.78],
                        radius=s * 0.08, outline=c, width=3)
    d.line([x + s * 0.5, y + s * 0.22, x + s * 0.5, y + s * 0.08], fill=c, width=3)
    d.ellipse([x + s * 0.45, y + s * 0.02, x + s * 0.55, y + s * 0.12], fill=c)
    d.ellipse([x + s * 0.32, y + s * 0.38, x + s * 0.42, y + s * 0.48], fill=c)
    d.ellipse([x + s * 0.58, y + s * 0.62, x + s * 0.68, y + s * 0.72], fill=c)
    d.line([x + s * 0.35, y + s * 0.62, x + s * 0.65, y + s * 0.62], fill=c, width=2)


def ico_virus(d, x, y, s, c):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.28
    for i in range(8):
        a = math.pi * i / 4
        d.line([cx + r * 0.9 * math.cos(a), cy + r * 0.9 * math.sin(a),
                cx + r * 1.5 * math.cos(a), cy + r * 1.5 * math.sin(a)],
               fill=c, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=3)
    d.ellipse([cx - r * 0.35, cy - r * 0.35, cx + r * 0.1, cy + r * 0.1], fill=c)


def ico_dollar(d, x, y, s, c):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=3)
    fnt = load(SANS_B, int(s * 0.52))
    d.text((cx, cy), "$", font=fnt, fill=c, anchor="mm")


def ico_waves(d, x, y, s, c):
    for k in range(3):
        base = y + s * 0.28 + k * s * 0.24
        pts = []
        for i in range(21):
            px = x + s * 0.06 + (s * 0.88) * i / 20
            py = base + s * 0.06 * math.sin(i * math.pi / 5)
            pts.append((px, py))
        d.line(pts, fill=c, width=3)


def ico_ball(d, x, y, s, c):
    d.ellipse([x + s * 0.08, y + s * 0.28, x + s * 0.92, y + s * 0.72],
              outline=c, width=3)
    d.arc([x + s * 0.3, y + s * 0.05, x + s * 0.7, y + s * 0.95],
          start=300, end=60, fill=c, width=2)
    d.line([x + s * 0.44, y + s * 0.44, x + s * 0.56, y + s * 0.56], fill=c, width=2)


def ico_truck(d, x, y, s, c):
    d.rectangle([x + s * 0.06, y + s * 0.3, x + s * 0.6, y + s * 0.68],
                outline=c, width=3)
    d.polygon([(x + s * 0.6, y + s * 0.38), (x + s * 0.82, y + s * 0.38),
               (x + s * 0.92, y + s * 0.68), (x + s * 0.6, y + s * 0.68)],
              outline=c, width=3)
    for wx in (0.24, 0.72):
        cx = x + s * wx
        d.ellipse([cx - s * 0.09, y + s * 0.68, cx + s * 0.09, y + s * 0.86],
                  outline=c, width=2)


def ico_flags(d, x, y, s, c):
    d.line([x + s * 0.3, y + s * 0.1, x + s * 0.3, y + s * 0.9], fill=c, width=3)
    d.line([x + s * 0.7, y + s * 0.1, x + s * 0.7, y + s * 0.9], fill=c, width=3)
    d.polygon([(x + s * 0.3, y + s * 0.12), (x + s * 0.62, y + s * 0.24),
               (x + s * 0.3, y + s * 0.36)], fill=c)
    d.polygon([(x + s * 0.7, y + s * 0.12), (x + s * 0.38, y + s * 0.24),
               (x + s * 0.7, y + s * 0.36)], outline=c, width=2)


def ico_megaphone(d, x, y, s, c):
    d.polygon([(x + s * 0.12, y + s * 0.42), (x + s * 0.85, y + s * 0.18),
               (x + s * 0.85, y + s * 0.66), (x + s * 0.12, y + s * 0.58)],
              outline=c, width=3)
    d.line([x + s * 0.3, y + s * 0.58, x + s * 0.24, y + s * 0.85], fill=c, width=3)
    d.arc([x + s * 0.82, y + s * 0.15, x + s * 0.98, y + s * 0.69],
          start=270, end=90, fill=c, width=2)


# ---------------------------------------------------------------- stories

LEAD = ("LEAD",
        "COP31 collapses: no climate deal",
        "The UN climate summit in Antalya ended with no agreement after "
        "two weeks of talks ran into overtime. The EU rejected a final "
        "draft with no mention of fossil fuels.")

GRID = [
    ("MIDDLE EAST", "Iran missiles hit Bahrain; 2 hurt",
     "Iran fired missiles and drones at US bases in Bahrain; a civilian "
     "site was hit, two hurt.", ico_missile),
    ("UKRAINE", "Russian drone hits Kyiv flats",
     "A Russian drone hit a five-storey block in Dymer, near Kyiv; one "
     "dead, 14 unaccounted for.", ico_drone),
    ("NATO", "NATO calls emergency Poland talks",
     "NATO will hold an emergency meeting on Monday after Russian "
     "missiles entered Poland.", ico_star),
    ("EUROPE", "Denmark expels Russian attaché",
     "Denmark expelled Russia's military attaché over a foiled plot to "
     "kill rapper Kyivstoner.", ico_flag),
    ("GENEVA", "Killer-robot talks end with no deal",
     "UN talks in Geneva ended without binding rules on autonomous "
     "weapons; work runs to 2028.", ico_robot),
    ("USA", "Measles kills child; 12th US death",
     "A Virginia child under five died of measles, the 12th US death of "
     "2026, a 35-year high.", ico_virus),
    ("USA", "Trump threatens tax on AI centres",
     "Trump threatened a 'tremendous tax' on US tech firms building AI "
     "data centres overseas.", ico_dollar),
    ("FLORIDA — DISASTER", "Florida floods hit record levels",
     "Record flooding swamped Florida after days of rain; the St. Johns "
     "River passed its old high mark.", ico_waves),
    ("SPORT", "England thrash All Blacks at home",
     "England thrashed New Zealand at Twickenham; the Wallabies edged "
     "Wales 29–26 in Cardiff.", ico_ball),
    ("GAZA", "Strike hits Gaza aid vehicle; 3 dead",
     "An Israeli strike hit a vehicle delivering aid in Gaza, killing "
     "three, witnesses said.", ico_truck),
    ("ASIA", "Trump-Kim summit bid fails",
     "Trump sought a meeting with Kim Jong Un on his Asia trip; North "
     "Korea's terms sank it.", ico_flags),
    ("EUROPE", "Cost-of-living protests spread",
     "Protests over living costs and public services spread across "
     "European cities.", ico_megaphone),
]

ALSO = [
    "Mexico captures 'El Chapo Isidro'; 11 killed in Sinaloa raid.",
    "EU–Indonesia sign landmark trade deal after 10 years of talks.",
    "Alcaraz to play Zverev in ATP Finals final.",
    "Kansas City Current win NWSL Championship.",
]

FOOTER = ("Every story above was first reported on Sunday 22 November 2026, "
          "except the Florida floods (21 November).")


def draw_page():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    f_title = load(SERIF_B, 62)
    f_date = load(SANS, 20)
    f_kicker = load(SANS_B, 20)
    f_lead_head = load(SERIF_B, 42)
    f_lead_sum = load(SANS, 23)
    f_ckick = load(SANS_B, 14)
    f_chead = load(SERIF_B, 20)
    f_csum = load(SANS, 16)
    f_atitle = load(SANS_B, 16)
    f_aitem = load(SANS, 15)
    f_foot = load(SANS, 14)

    # ---- masthead
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 16), title, font=f_title, fill=INK)
    date_line = "Sunday 22 November 2026  ·  World news in one image"
    dw = d.textlength(date_line, font=f_date)
    d.text(((W - dw) / 2, 84), date_line, font=f_date, fill=GREY)
    d.line([MARGIN, 108, W - MARGIN, 108], fill=INK, width=3)
    d.line([MARGIN, 113, W - MARGIN, 113], fill=INK, width=1)

    # ---- lead story
    y = 126
    d.text((MARGIN, y), LEAD[0], font=f_kicker, fill=RED)
    y += 28
    text_w = W - 2 * MARGIN - 140
    y = para(d, LEAD[1], f_lead_head, MARGIN, y, text_w, 48,
             max_lines=2)
    y = para(d, LEAD[2], f_lead_sum, MARGIN, y + 4, text_w, 28,
             max_lines=3)
    ico_globe(d, W - MARGIN - 118, 128, 118, RED)
    d.line([MARGIN, 296, W - MARGIN, 296], fill=RULE, width=1)

    # ---- grid of twelve stories, two columns, six rows
    col_w = (W - 2 * MARGIN - 24) // 2
    row_h = 96
    grid_top = 308
    for i, (kicker, head, summ, icon) in enumerate(GRID):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 24)
        cy = grid_top + row * row_h
        icon(d, x, cy + 2, 42, RED)
        tx = x + 52
        tw = col_w - 52
        d.text((tx, cy), kicker, font=f_ckick, fill=RED)
        y2 = para(d, head, f_chead, tx, cy + 19, tw, 23, max_lines=2)
        para(d, summ, f_csum, tx, y2 + 1, tw, 19, max_lines=2)

    # ---- also today strip
    strip_top = grid_top + 6 * row_h + 10
    d.rectangle([MARGIN, strip_top, W - MARGIN, strip_top + 88],
                fill=(248, 248, 248), outline=RULE, width=1)
    d.text((MARGIN + 12, strip_top + 8), "ALSO TODAY", font=f_atitle, fill=RED)
    item_w = (W - 2 * MARGIN - 24 - 24) // 2
    left_y = para(d, "•  " + ALSO[0], f_aitem, MARGIN + 12,
                 strip_top + 30, item_w, 19, max_lines=2)
    para(d, "•  " + ALSO[1], f_aitem, MARGIN + 12, left_y + 2,
         item_w, 19, max_lines=2)
    right_x = MARGIN + 12 + item_w + 24
    right_y = para(d, "•  " + ALSO[2], f_aitem, right_x,
                   strip_top + 30, item_w, 19, max_lines=2)
    para(d, "•  " + ALSO[3], f_aitem, right_x, right_y + 2,
         item_w, 19, max_lines=2)

    # ---- footer
    foot_lines = wrap(d, FOOTER, f_foot, W - 2 * MARGIN)
    fy = strip_top + 88 + 12
    for line in foot_lines:
        lw = d.textlength(line, font=f_foot)
        d.text(((W - lw) / 2, fy), line, font=f_foot, fill=GREY)
        fy += 18
    return img, fy


def main():
    img, bottom = draw_page()
    img.save("entry.png")
    data = open("entry.png", "rb").read()
    print("size:", img.size, "bottom y:", bottom)
    print("bytes:", len(data))
    print("sha256:", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
