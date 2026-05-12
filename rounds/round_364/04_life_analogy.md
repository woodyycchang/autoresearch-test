# Life Analogy — Bali subak rice-irrigation upstream-downstream temple coordination

The Balinese **subak** system is a UNESCO-protected millennium-old cooperative irrigation system. Key features:
- **3-tier partition**: ngulu (upstream) → maongin (midstream) → ngasep (downstream).
- **Water-temple coordination**: priests organize planting/harvesting/fallow schedules across all subaks.
- **Tactical synchronization**: simultaneous planting both upstream and downstream optimizes pest control (no continuous food source for pests).
- **Schedule precedes water flow**: upstream fields plant first, midstream next, downstream last — over ~2 weeks.
- **Self-interest balanced by ceremony**: water-temple ceremony enforces cooperation; without it, upstream farmers would withdraw all water.

The novel feature: **cooperation is enforced not by hierarchy or law but by SCHEDULED CEREMONIAL COORDINATION across the whole region** — the schedule is set top-down (water temple) but execution is decentralized.

## Analogical mapping → LLM cache coordination

- Upstream subak ↔ early-layer KV cache producer
- Downstream subak ↔ late-layer KV cache consumer
- Water-temple coordinator ↔ central scheduler producing schedule for KV-cache flow
- Simultaneous planting upstream+downstream ↔ synchronized prefill across pipeline stages
- Fallow cycle (tactical pest control) ↔ scheduled KV-eviction windows to prevent stale-context "pests"

The mechanism: a **3-tier KV-cache coordination layer** that schedules KV-prefill/eviction across pipeline stages via a central scheduler (water-temple) that enforces simultaneous upstream-and-downstream prefill windows and synchronized fallow (eviction) windows — preventing context drift and stale-KV "pests" that would arise from each stage greedily caching independently.
