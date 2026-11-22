#!/usr/bin/env python3
"""Draw the 22 Nov 2026 world-news front page, 1024x1024 PNG.
One image, 17 stories, each with a small hand-drawn pictogram.
All stories first reported on Sunday 22 November 2026, except the
Florida floods (first reported 21 November, still rising on the 22nd)."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (26, 47, 74)
RED = (176, 42, 32)
GREY = (90, 90, 86)
RULE = (180, 175, 165)
LEAD_BG = (232, 238, 244)
ICON_BG = (236, 233, 224)
GOLD = (255, 210, 90)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 36

def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(text, font, x, y, max_w, leading, color=INK):
    lines = wrap(text, font, max_w)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=color)
        y += leading
    return y, len(lines)

def hline(y, color=RULE, width=2):
    d.line([(M, y), (W - M, y)], fill=color, width=width)

# ---------- pictograms (each drawn in a 36x36 box at ox, oy) ----------
def icon_bg(ox, oy):
    d.rounded_rectangle([ox, oy, ox + 36, oy + 36], radius=6,
                        fill=ICON_BG)

def ico_missile(ox, oy):
    icon_bg(ox, oy)
    d.polygon([(ox + 18, oy + 4), (ox + 23, oy + 14), (ox + 18, oy + 24),
               (ox + 13, oy + 14)], fill=(120, 120, 120))
    d.polygon([(ox + 13, oy + 16), (ox + 8, oy + 24), (ox + 13, oy + 22)],
              fill=(90, 90, 90))
    d.polygon([(ox + 23, oy + 16), (ox + 28, oy + 24), (ox + 23, oy + 22)],
              fill=(90, 90, 90))
    d.polygon([(ox + 18, oy + 24), (ox + 21, oy + 31), (ox + 15, oy + 31)],
              fill=(230, 120, 30))
    d.line([(ox + 6, oy + 8), (ox + 10, oy + 12)], fill=RED, width=2)
    d.line([(ox + 30, oy + 8), (ox + 26, oy + 12)], fill=RED, width=2)

def ico_building(ox, oy):
    icon_bg(ox, oy)
    d.rectangle([ox + 8, oy + 8, ox + 24, oy + 31], fill=(120, 110, 95))
    d.rectangle([ox + 11, oy + 12, ox + 14, oy + 15], fill=(255, 230, 120))
    d.rectangle([ox + 17, oy + 12, ox + 20, oy + 15], fill=(255, 230, 120))
    d.rectangle([ox + 11, oy + 18, ox + 14, oy + 21], fill=(60, 60, 60))
    d.rectangle([ox + 17, oy + 18, ox + 20, oy + 21], fill=(60, 60, 60))
    d.polygon([(ox + 26, oy + 4), (ox + 28, oy + 9), (ox + 33, oy + 9),
               (ox + 29, oy + 13), (ox + 31, oy + 18), (ox + 26, oy + 15),
               (ox + 21, oy + 18), (ox + 23, oy + 13), (ox + 19, oy + 9),
               (ox + 24, oy + 9)], fill=(255, 200, 40))

def ico_shield(ox, oy):
    icon_bg(ox, oy)
    d.polygon([(ox + 18, oy + 5), (ox + 30, oy + 9), (ox + 30, oy + 19),
               (ox + 18, oy + 31), (ox + 6, oy + 19), (ox + 6, oy + 9)],
              fill=NAVY)
    d.rectangle([ox + 16, oy + 11, ox + 20, oy + 21], fill=GOLD)
    d.ellipse([ox + 16, oy + 23, ox + 20, oy + 27], fill=GOLD)

def ico_flags(ox, oy):
    icon_bg(ox, oy)
    d.rectangle([ox + 4, oy + 8, ox + 17, oy + 20], fill=(30, 60, 140))
    d.line([(ox + 10, oy + 8), (ox + 10, oy + 20)], fill=(255, 255, 255),
           width=2)
    d.line([(ox + 4, oy + 14), (ox + 17, oy + 14)], fill=(255, 255, 255),
           width=2)
    d.line([(ox + 10, oy + 8), (ox + 10, oy + 20)], fill=RED, width=1)
    d.line([(ox + 4, oy + 14), (ox + 17, oy + 14)], fill=RED, width=1)
    d.rectangle([ox + 19, oy + 8, ox + 32, oy + 20], fill=(30, 60, 140))
    for k in range(5):
        a = k * 2 * math.pi / 5 - math.pi / 2
        sx = ox + 25 + int(4 * math.cos(a))
        sy = oy + 14 + int(4 * math.sin(a))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 210, 60))
    d.rectangle([ox + 4, oy + 24, ox + 32, oy + 28], fill=(200, 200, 190))

def ico_robot(ox, oy):
    icon_bg(ox, oy)
    d.line([(ox + 18, oy + 4), (ox + 18, oy + 9)], fill=(80, 80, 80),
           width=2)
    d.ellipse([ox + 15, oy + 2, ox + 21, oy + 8], fill=RED)
    d.rounded_rectangle([ox + 7, oy + 9, ox + 29, oy + 28], radius=4,
                        fill=(150, 150, 150))
    d.ellipse([ox + 11, oy + 14, ox + 15, oy + 18], fill=(30, 200, 120))
    d.ellipse([ox + 21, oy + 14, ox + 25, oy + 18], fill=(30, 200, 120))
    d.line([(ox + 12, oy + 23), (ox + 24, oy + 23)], fill=(60, 60, 60),
           width=2)
    d.line([(ox + 7, oy + 16), (ox + 3, oy + 16)], fill=(80, 80, 80),
           width=2)
    d.line([(ox + 29, oy + 16), (ox + 33, oy + 16)], fill=(80, 80, 80),
           width=2)

def ico_pill(ox, oy):
    icon_bg(ox, oy)
    d.rounded_rectangle([ox + 5, oy + 12, ox + 31, oy + 24], radius=6,
                        outline=(40, 40, 40), width=2, fill=(255, 255, 255))
    d.rounded_rectangle([ox + 18, oy + 12, ox + 31, oy + 24], radius=6,
                        fill=(30, 130, 70))
    d.rounded_rectangle([ox + 5, oy + 12, ox + 18, oy + 24], radius=6,
                        fill=(255, 255, 255))
    d.text((ox + 18, oy + 28), "$", font=F(SANS_B, 11), fill=(30, 130, 70))

def ico_chip(ox, oy):
    icon_bg(ox, oy)
    d.rectangle([ox + 10, oy + 10, ox + 26, oy + 26], fill=(60, 140, 60))
    d.rectangle([ox + 15, oy + 15, ox + 21, oy + 21], fill=(30, 90, 30))
    for p in (12, 18, 24):
        d.line([(ox + p, oy + 6), (ox + p, oy + 10)], fill=(80, 80, 80),
               width=2)
        d.line([(ox + p, oy + 26), (ox + p, oy + 30)], fill=(80, 80, 80),
               width=2)
    d.ellipse([ox + 20, oy + 20, ox + 33, oy + 33], outline=NAVY, width=2)
    d.line([(ox + 30, oy + 30), (ox + 34, oy + 34)], fill=NAVY, width=2)

def ico_fire(ox, oy):
    icon_bg(ox, oy)
    d.polygon([(ox + 18, oy + 4), (ox + 26, oy + 14), (ox + 29, oy + 22),
               (ox + 24, oy + 31), (ox + 12, oy + 31), (ox + 7, oy + 22),
               (ox + 10, oy + 14)], fill=(230, 110, 20))
    d.polygon([(ox + 18, oy + 14), (ox + 23, oy + 20), (ox + 23, oy + 28),
               (ox + 13, oy + 28), (ox + 13, oy + 20)], fill=(255, 200, 40))
    d.rectangle([ox + 4, oy + 31, ox + 32, oy + 33], fill=(90, 70, 50))

def ico_flood(ox, oy):
    icon_bg(ox, oy)
    d.line([(ox + 5, oy + 13), (ox + 11, oy + 9), (ox + 17, oy + 13),
            (ox + 23, oy + 9), (ox + 29, oy + 13)], fill=(40, 90, 160),
           width=3)
    d.line([(ox + 5, oy + 21), (ox + 11, oy + 17), (ox + 17, oy + 21),
            (ox + 23, oy + 17), (ox + 29, oy + 21)], fill=(40, 90, 160),
           width=3)
    d.line([(ox + 5, oy + 29), (ox + 11, oy + 25), (ox + 17, oy + 29),
            (ox + 23, oy + 25), (ox + 29, oy + 29)], fill=(90, 140, 200),
           width=3)

def ico_ball(ox, oy):
    icon_bg(ox, oy)
    d.ellipse([ox + 5, oy + 11, ox + 31, oy + 25], fill=(150, 70, 30))
    d.line([(ox + 18, oy + 11), (ox + 18, oy + 25)], fill=(255, 255, 255),
           width=2)
    d.line([(ox + 10, oy + 13), (ox + 26, oy + 13)], fill=(255, 255, 255),
           width=1)
    d.line([(ox + 10, oy + 23), (ox + 26, oy + 23)], fill=(255, 255, 255),
           width=1)
    d.line([(ox + 12, oy + 28), (ox + 24, oy + 28)], fill=(60, 120, 60),
           width=3)

def ico_truck(ox, oy):
    icon_bg(ox, oy)
    d.rectangle([ox + 4, oy + 12, ox + 22, oy + 26], fill=(200, 200, 190),
                outline=(80, 80, 80))
    d.polygon([(ox + 22, oy + 16), (ox + 29, oy + 16), (ox + 32, oy + 22),
               (ox + 22, oy + 22)], fill=(40, 90, 160))
    d.ellipse([ox + 8, oy + 25, ox + 13, oy + 30], fill=(40, 40, 40))
    d.ellipse([ox + 24, oy + 25, ox + 29, oy + 30], fill=(40, 40, 40))
    d.text((ox + 8, oy + 15), "+", font=F(SANS_B, 14), fill=RED)

def ico_stars(ox, oy):
    icon_bg(ox, oy)
    d.ellipse([ox + 5, oy + 5, ox + 31, oy + 31], fill=(30, 60, 140))
    for k in range(8):
        a = k * math.pi / 4
        sx = ox + 18 + int(9 * math.cos(a))
        sy = oy + 18 + int(9 * math.sin(a))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 210, 60))
    d.line([(ox + 8, oy + 28), (ox + 28, oy + 8)], fill=RED, width=3)

def ico_megaphone(ox, oy):
    icon_bg(ox, oy)
    d.polygon([(ox + 6, oy + 15), (ox + 24, oy + 7), (ox + 24, oy + 25),
               (ox + 6, oy + 21)], fill=RED)
    d.rectangle([ox + 4, oy + 14, ox + 8, oy + 22], fill=(140, 20, 10))
    d.rectangle([ox + 12, oy + 22, ox + 17, oy + 29], fill=(140, 20, 10))
    d.arc([ox + 25, oy + 10, ox + 32, oy + 26], 300, 60, fill=NAVY,
          width=2)
    d.arc([ox + 28, oy + 7, ox + 35, oy + 29], 300, 60, fill=NAVY, width=2)

def ico_globe(ox, oy):
    icon_bg(ox, oy)
    d.ellipse([ox + 6, oy + 8, ox + 30, oy + 32], outline=(40, 90, 160),
              width=2)
    d.ellipse([ox + 12, oy + 12, ox + 20, oy + 19], fill=(60, 140, 70))
    d.ellipse([ox + 21, oy + 21, ox + 27, oy + 27], fill=(60, 140, 70))
    d.arc([ox + 13, oy + 8, ox + 23, oy + 32], 270, 90,
          fill=(40, 90, 160), width=1)
    d.line([(ox + 18, oy + 8), (ox + 18, oy + 32)], fill=(40, 90, 160),
           width=1)

# ---------- Masthead ----------
y = 14
d.text((W // 2, y), "THE WORLD IN ONE DAY", font=F(SANS_B, 16),
       fill=GREY, anchor="ma")
y += 24
d.text((W // 2, y), "WORLD NEWS", font=F(SERIF, 76), fill=INK, anchor="ma")
y += 86
d.line([(M, y), (W - M, y)], fill=INK, width=4)
y += 10
d.text((W // 2, y), "SUNDAY  22  NOVEMBER  2026", font=F(SANS_B, 24),
       fill=RED, anchor="ma")
y += 34
d.line([(M, y), (W - M, y)], fill=INK, width=4)

# ---------- Lead story ----------
lead_y = y + 12
d.rectangle([M, lead_y, W - M, lead_y + 134], fill=LEAD_BG, outline=NAVY,
            width=2)
lx, ly = M + 20, lead_y + 10
d.text((lx, ly), "1  •  LEAD STORY — ANTALYA / CLIMATE",
       font=F(SANS_B, 15), fill=NAVY)
ly += 24
ly, _ = para("COP31 collapses: no climate deal", F(SERIF, 30), lx, ly,
             700, 34)
ly += 2
para("The UN climate summit in Antalya ended with no agreement after "
     "two weeks of talks ran into overtime. The EU rejected a final "
     "draft with no mention of fossil fuels.",
     F(SANS, 16), lx, ly, 700, 21, color=(40, 40, 40))
# lead pictogram: globe with a red slash + torn pact
ix = W - M - 132
d.ellipse([ix + 6, lead_y + 14, ix + 66, lead_y + 74],
          outline=(40, 90, 160), width=3)
d.ellipse([ix + 18, lead_y + 24, ix + 32, lead_y + 36],
          fill=(60, 140, 70))
d.ellipse([ix + 36, lead_y + 46, ix + 50, lead_y + 58],
          fill=(60, 140, 70))
d.arc([ix + 22, lead_y + 14, ix + 50, lead_y + 74], 270, 90,
      fill=(40, 90, 160), width=2)
d.line([(ix + 36, lead_y + 14), (ix + 36, lead_y + 74)],
       fill=(40, 90, 160), width=2)
d.line([(ix + 8, lead_y + 70), (ix + 64, lead_y + 18)], fill=RED, width=5)
d.rectangle([ix + 74, lead_y + 30, ix + 112, lead_y + 66],
            fill=(255, 255, 255), outline=(120, 120, 120))
d.line([(ix + 80, lead_y + 40), (ix + 106, lead_y + 40)], fill=GREY,
       width=2)
d.line([(ix + 80, lead_y + 48), (ix + 106, lead_y + 48)], fill=GREY,
       width=2)
d.line([(ix + 80, lead_y + 56), (ix + 98, lead_y + 56)], fill=GREY,
       width=2)
d.text((ix, lead_y + 104), "ANTALYA", font=F(SANS_B, 13), fill=GREY)

y = lead_y + 134 + 10
hline(y, color=INK, width=2)
y += 12

# ---------- Grid: 2 columns x 6 rows ----------
cards = [
    ("2", "BAHRAIN — CONFLICT", RED, ico_missile,
     "Iran missiles hit Bahrain; 2 hurt",
     "Iran fired missiles and drones at US bases in Bahrain; a "
     "civilian site was hit, two hurt."),
    ("3", "KYIV — CONFLICT", RED, ico_building,
     "Russian drone hits Kyiv flats",
     "A Russian drone hit a five-storey block in Dymer, near Kyiv; "
     "one dead, 14 unaccounted for."),
    ("4", "BRUSSELS — POLITICS", NAVY, ico_shield,
     "NATO calls emergency Poland talks",
     "NATO will hold an emergency meeting on Monday after Russian "
     "missiles entered Poland."),
    ("5", "COPENHAGEN — ESPIONAGE", NAVY, ico_flags,
     "Denmark expels Russian attaché",
     "Denmark expelled Russia's military attaché over a foiled plot "
     "to kill rapper Kyivstoner."),
    ("6", "GENEVA — TECH", NAVY, ico_robot,
     "Killer-robot talks end with no deal",
     "UN talks in Geneva ended without binding rules on autonomous "
     "weapons; work runs to 2028."),
    ("7", "VIRGINIA — HEALTH", NAVY, ico_pill,
     "Measles kills child; 12th US death",
     "A Virginia child under five died of measles, the 12th US death "
     "of 2026, a 35-year high."),
    ("8", "WASHINGTON — TECH", NAVY, ico_chip,
     "Trump threatens tax on AI centres",
     "Trump threatened a 'tremendous tax' on US tech firms building "
     "AI data centres overseas."),
    ("9", "FLORIDA — DISASTER", RED, ico_flood,
     "Florida floods hit record levels",
     "Record flooding swamped Florida after days of rain; the "
     "St. Johns River passed its old high mark."),
    ("10", "LONDON — SPORT", NAVY, ico_ball,
     "England thrash All Blacks at home",
     "England thrashed New Zealand at Twickenham; the Wallabies "
     "edged Wales 29–26 in Cardiff."),
    ("11", "GAZA — CONFLICT", RED, ico_truck,
     "Strike hits Gaza aid vehicle; 3 dead",
     "An Israeli strike hit a vehicle delivering aid in Gaza, "
     "killing three, witnesses said."),
    ("12", "WASHINGTON — DIPLOMACY", NAVY, ico_stars,
     "Trump-Kim summit bid fails",
     "Trump sought a meeting with Kim Jong Un on his Asia trip; "
     "North Korea's terms sank it."),
    ("13", "EUROPE — SOCIETY", NAVY, ico_megaphone,
     "Cost-of-living protests spread",
     "Protests over living costs and public services spread across "
     "European cities."),
]
col_w = (W - 2 * M - 20) // 2
row_h = 94
gap = 6
warn = []
for i, (num, kick, kc, ico, head, summ) in enumerate(cards):
    cx = M + (i % 2) * (col_w + 20)
    cy = y + (i // 2) * (row_h + gap)
    d.rectangle([cx, cy, cx + col_w, cy + row_h], outline=RULE, width=2)
    ico(cx + 12, cy + 12)
    tx = cx + 58
    tw = col_w - 58 - 12
    d.text((tx, cy + 9), f"{num}  •  {kick}", font=F(SANS_B, 11), fill=kc)
    _, hl = para(head, F(SERIF, 19), tx, cy + 27, tw, 22)
    if hl > 1:
        warn.append(f"headline wraps: {head!r}")
    _, sl = para(summ, F(SANS, 13), tx, cy + 27 + hl * 22 + 2, tw, 16,
                 color=(40, 40, 40))
    if sl > 2:
        warn.append(f"summary wraps to {sl}: {summ!r}")

y = y + 6 * row_h + 5 * gap + 8

# ---------- Also-today strip ----------
d.rectangle([M, y, W - M, y + 84], fill=NAVY)
fy = y + 9
d.text((M + 16, fy), "ALSO TODAY", font=F(SANS_B, 13), fill=GOLD)
fy += 19
fy, _ = para("Mexico captures 'El Chapo Isidro'; 11 killed in Sinaloa "
             "raid  •  EU and Indonesia sign landmark trade deal after "
             "10 years of talks  •  Alcaraz to play Zverev in ATP "
             "Finals final  •  Kansas City Current win NWSL Championship",
             F(SANS, 14), M + 16, fy, W - 2 * M - 32, 18,
             color=(255, 255, 255))
fy += 3
d.text((M + 16, fy),
       "Every story above was first reported on Sunday 22 November 2026, except the Florida floods (21 November).",
       font=F(SERIF_R, 13), fill=(200, 210, 225))

out = "/home/hatch/workspace/makefun/news-image-20261122/entry.png"
img.save(out, optimize=True)
import os
print("saved", out, os.path.getsize(out), "bytes")
for w in warn:
    print("WARN:", w)
print("done")
