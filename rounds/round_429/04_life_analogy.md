# Life Analogy — Hmong paj ntaub story cloth pictorial narrative

The **Hmong paj ntaub story cloth**:
- Hmong women's embroidery on flat cloth; pictorial panels narrating Hmong oral tradition.
- Each cloth = sequence of figure-panels (village life, migration, military, folktale).
- Geometric border framing encloses the entire serialized narrative.
- Originated in 1970s Thai refugee camps for income + cultural memory.

**PAJ-NTAUB-PANEL**: a panel-bordered narrative cascade for long-form generation. The model produces output as a sequence of K bordered panels P_1...P_K; each panel P_i contains (a) a frame token sequence encoding panel-i identity + position-in-narrative + topic-anchor, (b) the panel body, (c) a closing frame echoing the topic-anchor for verification. Across panels, panel-i's closing frame is consumed by panel-i+1's opening frame as a verified handoff signal. Combines Chain-of-Agents-style segment-wise generation with explicit FRAME-BORDER-AS-VERIFICATION token sequences that bracket each panel.

## Adjacency
- Chain-of-Agents NeurIPS 2024 (sequential segment handoff)
- NEXUSSUM Hierarchical Long-Form Narrative ACL 2025
- Narrative Weaver 2603.06688 (multi-modal long-range consistency)
- Story-generation survey Findings EMNLP 2025

Expected FAIL — segment-cascade long-form generation + explicit handoff verification is well-covered 2025-2026 design.
