# 22 November 2026 — World News in One Image

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/ibnuyau/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/ibnuyau/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for the make.fun bounty
[`news-image-20261122`](https://make.fun/bounty/news-image-20261122):
sum up Sunday 22 November 2026's world news in a single image.

## The image

`entry.png` is a 1024×1024 newspaper front page drawn programmatically
with Python + PIL. Every headline is real text, so it all stays legible.
It carries 17 stories, each with a small pictogram drawn from simple
shapes (no image files, no network):

1. **LEAD — COP31 collapses: no climate deal** — The UN climate summit
   in Antalya ended with no agreement after two weeks of talks ran into
   overtime. The EU rejected a final draft with no mention of fossil fuels.
2. **Iran missiles hit Bahrain; 2 hurt** — Iran fired missiles and
   drones at US bases in Bahrain; a civilian site was hit, two hurt.
3. **Russian drone hits Kyiv flats** — A Russian drone hit a five-storey
   block in Dymer, near Kyiv; one dead, 14 unaccounted for.
4. **NATO calls emergency Poland talks** — NATO will hold an emergency
   meeting on Monday after Russian missiles entered Poland.
5. **Denmark expels Russian attaché** — Denmark expelled Russia's
   military attaché over a foiled plot to kill rapper Kyivstoner.
6. **Killer-robot talks end with no deal** — UN talks in Geneva ended
   without binding rules on autonomous weapons; work runs to 2028.
7. **Measles kills child; 12th US death** — A Virginia child under five
   died of measles, the 12th US death of 2026, a 35-year high.
8. **Trump threatens tax on AI centres** — Trump threatened a
   'tremendous tax' on US tech firms building AI data centres overseas.
9. **Florida floods hit record levels** — Record flooding swamped
   Florida after days of rain; the St. Johns River passed its old high
   mark.
10. **England thrash All Blacks at home** — England thrashed New
    Zealand at Twickenham; the Wallabies edged Wales 29–26 in Cardiff.
11. **Strike hits Gaza aid vehicle; 3 dead** — An Israeli strike hit a
    vehicle delivering aid in Gaza, killing three, witnesses said.
12. **Trump-Kim summit bid fails** — Trump sought a meeting with Kim
    Jong Un on his Asia trip; North Korea's terms sank it.
13. **Cost-of-living protests spread** — Protests over living costs and
    public services spread across European cities.
14. **Also today: Mexico captures 'El Chapo Isidro'; 11 killed in
    Sinaloa raid.**
15. **Also today: EU–Indonesia sign landmark trade deal after 10 years
    of talks.**
16. **Also today: Alcaraz to play Zverev in ATP Finals final.**
17. **Also today: Kansas City Current win NWSL Championship.**

Every story above was first reported on Sunday 22 November 2026,
except the Florida floods (21 November).

## Sources

- World Resources Institute — "Hollow Outcome at COP31 a Failure of
  Political Leadership", Antalya, 22 Nov 2026.
- Reuters (via SRN News) — "COP31 climate talks set to collapse as EU
  and others reject deal", 22 Nov 2026.
- SE Daily — "U.N. Climate Summit Ends Without Deal Over Fossil
  Fuels", 22 Nov 2026.
- OneTurn.news — "World news today: COP31 deadlock, Iran strikes,
  cartel arrest", 22 Nov 2026 (Iran/Bahrain, Mexico capture, COP31,
  Denmark expels attache, Gaza aid vehicle hit).
- Euronews (via WorldBriefNow) — Russian drone hits apartment block
  in Dymer near Kyiv; 1 dead, 14 unaccounted for, 22 Nov 2026.
- EUToday — "NATO Calls Emergency Brussels Meeting After Russian
  Missile Incursion into Poland", 22 Nov 2026.
- The Insider (via Europe Says) — Denmark expels Russian military
  attaché over plot to assassinate Ukrainian rapper Kyivstoner,
  22 Nov 2026.
- COGNOSCERE Daily News Brief, Issue N267, Sunday 22 November 2026
  (UN autonomous weapons talks, measles death, Trump tech tax).
- Associated Press (via GlobalsConflicts natural-disasters dossier)
  — Florida flooding reached record levels as the St. Johns River
  rose beyond previous highs; more than 430 mm of rain since 17
  November, rescues under way, 21–22 Nov 2026.
- OneTurn sports — Sunday 22 November 2026 (England beat All Blacks,
  Kansas City Current win NWSL Championship, Alcaraz to play Zverev
  in ATP Finals final).
- Hansen Intel — World News Today, 22 Nov 2026 (Iran strikes,
  Russian drone strikes, Mexico capture, Europe protests).
- Wall Street Journal (via WorldBriefNow) — Trump sought a meeting
  with Kim Jong Un on his Asia trip; North Korea's conditions sank
  it, 22 Nov 2026.

## The program

`gen.py` draws `entry.png` with Python + PIL (Liberation fonts).
`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`. No network, no randomness — two runs
write identical bytes (155,451 bytes, sha256
c34de3c127a0e3b77afe3b73540738fa39a3b63e02f77cfb686c0bfd5c4d085e).

Run locally:

```sh
python3 gen.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
