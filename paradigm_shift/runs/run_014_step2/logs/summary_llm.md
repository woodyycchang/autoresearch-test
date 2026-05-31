# LLM summary (session aa70f8fd-7a95-4905-bbb6-d27f0a446cd1)

The automated run evaluated three candidate research niches (CAND_S2_001, CAND_S2_002, CAND_S2_003) using real WebSearch prior-art queries and a deterministic gate process. CAND_S2_001 ("Genome-Style Regulatory Routing for Mixture-of-Experts Models") scored a composite of 0.7584 with 7 real arXiv hits and 4 recent papers, passing gate_2 and gate_4 but failing gate_1's threshold. CAND_S2_002 ("Competency-Driven Test-Time Training as Morphogenetic Weight Adaptation") scored 0.6107 with 6 arXiv hits and 5 recent papers, and failed gate_1, gate_2, and gate_4. CAND_S2_003 ("Compute-Driven Capability Scaling as General-Purpose Transformation") scored 0.3933 with 8 arXiv hits but 0 recent papers (its community search returned 7 non-paper news/think-tank results), and failed gate_1. All three candidates failed at least one gate and none survived, yielding a verdict of NICHE_NOT_FOUND. Because no candidate survived the gates, no surviving candidate underwent a real, executed prior-art collision check; for CAND_S2_001, gate_3 was not executed (gate_3_executed = false) and was run only as a demonstration, which recorded a collision (gate_3_collided = true).

```json
{
  "n_candidates": 3,
  "n_survivors": 0,
  "verdict": "NICHE_NOT_FOUND",
  "per_candidate": [
    {"cand_id": "CAND_S2_001", "composite": 0.7584, "real_arxiv_hit_count": 7, "survived": false},
    {"cand_id": "CAND_S2_002", "composite": 0.6107, "real_arxiv_hit_count": 6, "survived": false},
    {"cand_id": "CAND_S2_003", "composite": 0.3933, "real_arxiv_hit_count": 8, "survived": false}
  ]
}
```
