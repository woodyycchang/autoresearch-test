# Life Analogy — Igbo umunna kindred-spokesperson hierarchical governance

The **umunna** (Igbo kindred patrilineage governance):
- Patrilineal extended family from a founding ancestor.
- Eldest male **okpara** presides over kindred assembly.
- Multiple kindreds in a village; each kindred has spokesperson at village council.
- Inter-kindred council deliberates village affairs; spokesperson carries kindred's position.
- Intra-kindred: dense direct-democracy discussion among male members.
- Pre-colonial Igbo: highly decentralized governance through this 2-tier structure.

**UMUNNA-KINDRED-SPOKESPERSON-2-TIER**: 2-tier hierarchical multi-agent LLM with cluster-spokesperson aggregation. (1) **K kindred clusters** of M_k LLM agents each (each cluster trained on distinct subset / persona). (2) **Intra-kindred dense communication**: within cluster k, all M_k agents communicate freely (full-mesh) to form a cluster position p_k via internal consensus. (3) **Okpara spokesperson selection**: each cluster elects an okpara o_k (the agent with highest agreement-score within cluster) who carries position p_k to the inter-kindred council. (4) **Inter-kindred council (low bandwidth)**: only K spokespeople communicate; final decision = consensus over {p_1, ..., p_K} via weighted voting (weight = kindred-size M_k). (5) **Decision propagation**: outcome cascades back to kindred members via okpara broadcast. (6) **Umuada complementary track**: K kindred-daughters cluster (separate persona class) provides parallel evaluation; final decision combines umunna + umuada (gender-balanced complementary input). (7) Differs from R392 MAASAI-ILPAYIANI (age-grade) + R403 WELSH-PENILLION + R411 IROQUOIS-CONDOLENCE + R443 ALUNA-COUNCIL (4-tier) + R449 MAPUCHE-PURRUN + R463 HOKULEA + R465 SALGAN + R488 MAQAM-LEAD-TARJAMAH + R500 QULLIQ-HEARTH-FLAMEKEEPER by 2-tier kindred-cluster + okpara-spokesperson + inter-kindred low-bandwidth council + umuada complementary parallel track.

## Adjacency
- TalkHier 2502.11098 (closest — structured hierarchical communication)
- Hierarchical Multi-Agent Taxonomy 2508.12683
- AgentNet++ 2512.00614 (3-level + cluster heads + meta-graph)
- Multi-Agent Collaboration Survey 2501.06322

Expected FAIL — hierarchical multi-agent + cluster-head + spokesperson voting paradigm fully covers.
