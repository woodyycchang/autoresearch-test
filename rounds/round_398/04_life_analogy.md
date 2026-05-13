# Life Analogy — Mongolian/Kazakh dombra (two-string lute)

The **dombra** is a 2-string Central Asian lute:
- String 1 plays the **melody** (varying pitch).
- String 2 holds a **drone** (constant reference pitch, typically a 5th below).
- The two strings are TUNED to a fixed interval (drone-melody offset is fixed).
- The drone provides a **stable reference** against which the melody is heard.
- Two channels of information delivered simultaneously: dynamic + stable.

The unique principle: **dual-channel output with one DYNAMIC and one STABLE channel referenced to each other** — both delivered simultaneously, with the stable channel acting as a fixed comparison reference.

## Analogical mapping → LLM consistency evaluation

- Dynamic melody string ↔ test prompt with paraphrase variation
- Drone string ↔ canonical reference prompt
- Tuned 5th interval ↔ specified expected response distance
- Simultaneous play ↔ paired evaluation runs

The mechanism: a **paired-prompt consistency diagnostic** — for each test prompt P, also issue a CANONICAL REFERENCE PROMPT Q (semantically equivalent but with canonical phrasing). Compute (a) f_P = response to P, (b) f_Q = response to Q. The DIAGNOSTIC SCORE = simultaneous (consistency_drift = D(f_P, f_Q) low) AND (correctness = D(f_P, gt) low). Bad scores indicate: prompt-brittleness OR poor accuracy OR both. Differs from single-prompt evaluation (no reference) and from independent multi-prompt eval (no paired diagnostic) by EXPLICITLY PAIRING each test with a canonical reference and measuring drift between them.
