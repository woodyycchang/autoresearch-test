# R230 — life analogy

## Source domain: fly tying + hatch matching
- A fly-fisher carries a curated library of artificial flies designed to imitate the local stream's CURRENT hatch (emerging insect taxon at a given hour/day/season): mayfly dun, midge larva, caddisfly emerger, terrestrial beetle, etc.
- Each pattern is constructed from hackle (the radial barb-circle imitating insect legs), wings, tail, body materials chosen for visual + tactile + drift-behavior fidelity to the imitated taxon.
- Hatch matching is the discipline: identify the current emergent species, then select a fly whose pattern matches that taxon. The fish recognises pattern-fidelity at multiple cues (silhouette, color, drift speed, presentation).
- A fish "rises" to a fly because the FAKE has crossed enough cue thresholds; a fly that misses (wrong size, wrong color phase, wrong rise) is ignored.

## LLM analogy candidate
**Hatch-match jailbreak defence**: model maintains an internal "current hatch catalog" — a small, dynamically-updated set of templates of benign request signatures CURRENTLY ACTIVE in the user's workspace context (recent legitimate queries, project docs, declared task). An incoming request is scored against this current hatch's signature multi-cue (silhouette = syntactic shape, color = topic embedding, drift = causal continuation from prior turns, rise behavior = response-conditioning pattern). A query that does NOT match the current hatch on ≥3 of these cues is flagged for additional scrutiny (more aggressive refusal-temperature) regardless of whether content alone would trigger a refusal classifier. The fly-tying frame inverts the usual safety-classifier pipeline: rather than asking "is this query harmful in absolute terms," ask "does this query resemble the CURRENT user's legitimate hatch."

## What differs from prior art (claim)
ALERT (2601.03600) and Jailbreaking Leaves a Trace (2602.11495) detect anomalous internal representations relative to TRAINING distribution. The hatch-match frame uses LIVE per-user context as the reference hatch, not training. Intent-concealment work (2505.14316) is an ATTACK; the hatch-match is a DEFENCE based on per-user current task context. No surveyed work uses the multi-cue, taxon-templated, dynamically updated "current hatch" frame.
