# Life Analogy — Macrotermes termite-mound passive ventilation

Macrotermes africanus build mounds with a **central chimney** + multiple **peripheral flutes**. The flutes have thin walls and high surface-to-volume ratio; the chimney has thick walls and high thermal mass. Solar radiation heats flutes rapidly during the day → hot air rises in flutes, cool air sinks in chimney → closed convection cell flushes CO2 and brings fresh air. At night the gradient reverses: chimney is warmer (slow to cool), so air rises in chimney and falls in flutes. No active pumping; the diurnal temperature oscillation alone drives ventilation.

Key features:
- **Two thermal-mass regimes**: low-mass (flutes) and high-mass (chimney) units.
- **Passive forcing**: external diurnal cycle, no internal control.
- **Phase-reversal**: the gradient driving circulation flips daily.
- **CO2 flush**: byproducts accumulated by colony metabolism are passively cleared on each cycle.

## Analogical mapping → LLM training schedule

- Diurnal temperature oscillation ↔ external periodic training perturbation (e.g., cosine LR cycle, alternating LR/WD phase)
- Flutes (low thermal mass, fast-respond) ↔ shallow / high-LR parameter groups
- Chimney (high thermal mass, slow-respond) ↔ deep / low-LR parameter groups
- Convection cell flushes CO2 ↔ each oscillation cycle flushes accumulated gradient-noise / activation drift
- Phase-reversal ↔ gradient flow direction reverses between LR-high and LR-low phases

The mechanism: a **two-group parameter partition** (low-mass / fast-adapt vs high-mass / slow-adapt) coupled to a deliberate periodic external forcing (alternating LR phases), so that *natural* periodic gradient circulation flushes accumulated activation noise without active gating or buffer replay.
