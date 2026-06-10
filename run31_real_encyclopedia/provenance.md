# Run 31 — Phase 0 Provenance (REAL, sourced, verbatim — NOT bootstrapped)

Core fix vs Run 30: Run 30 bootstrapped 297 INVENTED concepts (tech 105 + life 192). Run 31 forbids invention — every entry below traces to a REAL searched source with a verbatim quote (R5/R12).

**Sourcing method:** 16 parallel harvester agents used WebSearch over real Wikipedia / arXiv. WebFetch to wikipedia.org / arxiv.org returned HTTP 403 in this environment, so verbatim text was captured from the real Wikipedia/arXiv excerpts returned by WebSearch; the canonical article/abstract URL is recorded for every concept. Every concept therefore traces to a real searched source.

## Cumulative bank size
- **life_bank.json = 576**  (385 freshly harvested Run 31 + 191 merged-in REAL Run 29)
- **tech_bank.json = 215**  (110 freshly harvested Run 31 + 105 merged-in REAL Run 29)
- Verbatim+source present on 100% of entries (aggregator dropped 0 for missing source/verbatim).

## Per-agent harvest (Run 31, real Wikipedia/arXiv)
| Agent | Branch | Concepts | Example source URLs |
|---|---|---:|---|
| LIFE-ARTS | arts / music | 30 | https://en.wikipedia.org/wiki/Counterpoint ; https://en.wikipedia.org/wiki/Harmony |
| LIFE-EARTH-ASTRO | earth & space science / geology | 28 | https://en.wikipedia.org/wiki/Plate_tectonics ; https://en.wikipedia.org/wiki/Subduction |
| LIFE-ENGTECH | engineering / control systems | 32 | https://en.wikipedia.org/wiki/Proportional-integral-derivative_controller ; https://en.wikipedia.org/wiki/Centrifugal_governor |
| LIFE-FOOD-AGRI | food / fermentation | 32 | https://en.wikipedia.org/wiki/Sourdough ; https://en.wikipedia.org/wiki/Miso |
| LIFE-GAMES | games / rating systems | 28 | https://en.wikipedia.org/wiki/Elo_rating_system ; https://en.wikipedia.org/wiki/Swiss-system_tournament |
| LIFE-GEO-CULT | geography / cultures | 29 | https://en.wikipedia.org/wiki/Polynesian_navigation ; https://en.wikipedia.org/wiki/Micronesian_navigation |
| LIFE-HIST | history / archaeology | 28 | https://en.wikipedia.org/wiki/Stratigraphy_(archaeology) ; https://en.wikipedia.org/wiki/Seriation_(archaeology) |
| LIFE-LANG | language / phonology | 30 | https://en.wikipedia.org/wiki/Vowel_harmony ; https://en.wikipedia.org/wiki/Assimilation_(phonology) |
| LIFE-MED | medicine / immunology | 29 | https://en.wikipedia.org/wiki/Adaptive_immune_system ; https://en.wikipedia.org/wiki/Clonal_selection |
| LIFE-NATSCI-BIO | natural science / biology | 35 | https://en.wikipedia.org/wiki/Quorum_sensing ; https://en.wikipedia.org/wiki/Action_potential |
| LIFE-NATSCI-PHYSCHEM | natural science / physics | 34 | https://en.wikipedia.org/wiki/Classical_mechanics ; https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion |
| LIFE-RELPHIL | religion / ritual | 30 | https://en.wikipedia.org/wiki/Rite_of_passage ; https://en.wikipedia.org/wiki/Liminality |
| LIFE-SOCSCI | social science / economics | 36 | https://en.wikipedia.org/wiki/Vickrey_auction ; https://en.wikipedia.org/wiki/Nash_equilibrium |
| TECH-MATH-PHYS-CS | optimization | 39 | https://arxiv.org/abs/2410.15731 ; https://arxiv.org/abs/2012.07401 |
| TECH-ML-CORE | efficient attention / systems | 36 | https://arxiv.org/abs/2205.14135 ; https://arxiv.org/abs/2307.08691 |
| TECH-ML-FRONTIER | reinforcement learning / policy gradient | 36 | https://arxiv.org/abs/1707.06347 ; https://arxiv.org/abs/2203.02155 |

## Run 29 merge-in spot-check (anti-hallucination on inherited banks)
- Mamba-3 (arXiv 2603.15569) — CONFIRMED real: ICLR 2026 poster, arxiv.org/abs/2603.15569.
- Cheese affinage / grading iron (academyofcheese.org) — CONFIRMED real: verbatim quote present on source page.

## Life-bank branch distribution (harvested Run 31)
- natural science: 62
- engineering: 32
- arts: 30
- social science: 30
- language: 29
- medicine: 29
- earth & space science: 28
- geography: 28
- history: 28
- food: 20
- games: 20
- philosophy: 14
- agriculture: 10
- religion: 10
- sport: 5
- daily life: 3
- mythology: 3
- crafts: 2
- theology: 2