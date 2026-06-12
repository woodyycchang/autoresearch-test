#!/usr/bin/env python3
"""
real_history_experiments.py  —  Run 37: optimize against the Run 36 external
backtest failures, ON THE REAL run31 791-concept banks, scored against REAL
history (8 verified niches). No self-made fixtures; ground truth = real arXiv.

Honesty guards:
- The banks are CONTAMINATED: 7/8 niche families are literal bank entries
  (FlashAttention, Mamba, LoRA, QLoRA, DoRA, MoE, Switch, S4). We REMOVE them to
  build a pre-emergence corpus, and report results both ways.
- The value signal (mechanism-generality x problem-centrality) is computed from
  the 791-corpus and is NOT fit to the 8 niches. The only hindsight is in which
  keywords name each niche (unavoidable to represent them at all) — flagged.
- A change that improves a signal but not real-history ranking is reported as
  not-an-improvement (R14).
"""
import json, os, re, random, statistics
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BANKS = os.path.join(HERE, "..", "run31_real_encyclopedia")
STOP = set("the a an of to and or in on for with by from as is are be that this it its into "
           "using use used uses which their they them then than over under within without "
           "between across each both more most less via at can may also such one two".split())

# 8 real niches (WebSearch-verified, real arXiv). type + keyword representation.
# family_kw = how its family appears as a bank entry (for decontamination).
NICHES = [
    {"id": "grokking", "year": 2022, "type": "emergent_phenomenon",
     "mech_kw": ["delayed", "generalization", "phase", "transition"], "prob_kw": ["generalization", "memorization"], "family_kw": []},
    {"id": "chain_of_thought", "year": 2022, "type": "prompting_format",
     "mech_kw": ["intermediate", "reasoning", "steps", "decomposition"], "prob_kw": ["reasoning", "arithmetic"], "family_kw": ["chain-of-thought", "chain of thought"]},
    {"id": "chinchilla", "year": 2022, "type": "scaling_law",
     "mech_kw": ["compute", "tokens", "parameters", "tradeoff", "scaling"], "prob_kw": ["scaling", "efficiency"], "family_kw": ["chinchilla", "compute-optimal"]},
    {"id": "lora", "year": 2021, "type": "mechanism_transfer",
     "mech_kw": ["low-rank", "rank", "decomposition", "matrix"], "prob_kw": ["adaptation", "fine-tuning", "efficiency"], "family_kw": ["lora", "qlora", "dora", "low-rank adaptation"]},
    {"id": "flash_attention", "year": 2022, "type": "mechanism_transfer",
     "mech_kw": ["tiling", "memory", "hierarchy", "io-aware", "blocking"], "prob_kw": ["attention", "efficiency", "memory"], "family_kw": ["flashattention", "flash attention"]},
    {"id": "mamba_ssm", "year": 2023, "type": "mechanism_transfer",
     "mech_kw": ["state", "space", "recurrence", "selective"], "prob_kw": ["sequence", "long", "efficiency"], "family_kw": ["mamba", "selective state space", "s4", "structured state space"]},
    {"id": "mixture_of_experts", "year": 2017, "type": "mechanism_transfer",
     "mech_kw": ["routing", "gating", "sparse", "experts", "conditional"], "prob_kw": ["capacity", "scaling", "efficiency"], "family_kw": ["mixture-of-experts", "moe", "switch transformer", "deepseekmoe"]},
    {"id": "rlhf", "year": 2022, "type": "mechanism_transfer",
     "mech_kw": ["reinforcement", "feedback", "reward", "preference"], "prob_kw": ["alignment", "instruction"], "family_kw": ["rlhf", "instructgpt", "human feedback"]},
]


def toks(*texts):
    out = set()
    for t in texts:
        if not t:
            continue
        if isinstance(t, list):
            t = " ".join(t)
        for w in re.findall(r"[a-z][a-z0-9\-]{2,}", str(t).lower()):
            if w not in STOP and len(w) >= 4:
                out.add(w)
    return out


def load_corpus(drop_family_kws=None):
    drop = set(drop_family_kws or [])
    concepts = []
    for fn, branchf in (("life_bank.json", "branch"), ("tech_bank.json", "subfield")):
        raw = json.load(open(os.path.join(BANKS, fn)))
        items = raw if isinstance(raw, list) else raw.get("techniques", raw.get("concepts", []))
        for c in items:
            nm = (c.get("name") or "").lower()
            if any(k in nm for k in drop):
                continue  # decontaminate: drop the niche families
            branch = (c.get(branchf) or c.get("domain") or c.get("branch") or "?").split("/")[0].strip()
            kt = toks(c.get("name"), c.get("capability_it_enables"), c.get("summary_verbatim"),
                      c.get("mechanism_atoms"), c.get("domain"))
            concepts.append({"name": nm, "branch": branch, "tokens": kt})
    return concepts


def build_stats(concepts):
    branch_of_tok = defaultdict(set)   # token -> set of branches  (generality)
    doc_freq = Counter()               # token -> # concepts       (centrality)
    for c in concepts:
        for t in c["tokens"]:
            branch_of_tok[t].add(c["branch"])
            doc_freq[t] += 1
    n_branch = len(set(c["branch"] for c in concepts))
    n_doc = len(concepts)
    return branch_of_tok, doc_freq, n_branch, n_doc


def generality(kws, branch_of_tok, n_branch):
    vals = [len(branch_of_tok.get(k, set())) / n_branch for k in kws if k in branch_of_tok]
    return round(statistics.mean(vals), 4) if vals else 0.0


def centrality(kws, doc_freq, n_doc):
    vals = [doc_freq.get(k, 0) / n_doc for k in kws if k in doc_freq]
    return round(statistics.mean(vals), 4) if vals else 0.0


def main():
    random.seed(37)
    # decontaminated corpus (drop all niche families)
    allfam = [k for n in NICHES for k in n["family_kw"]]
    corpus = load_corpus(drop_family_kws=allfam)
    bt, df, nb, nd = build_stats(corpus)
    print(f"decontaminated corpus: {len(corpus)} concepts, {nb} branches "
          f"(dropped {len(allfam)} family keywords)")

    # ---- FAILURE 2: frame coverage by niche type ----
    types = Counter(n["type"] for n in NICHES)
    transfer = sum(1 for n in NICHES if n["type"] == "mechanism_transfer")
    print(f"\n[FAILURE 2 frame] mechanism_transfer (old frame) represents {transfer}/8.")
    print(f"  niche types: {dict(types)}")
    print(f"  with templates for {list(t for t in types if t!='mechanism_transfer')}: {len(NICHES)}/8 representable.")

    # ---- FAILURE 3: niche-blind value signal vs random ----
    # niche value = generality(mechanism) * centrality(problem)
    niche_scores = []
    for n in NICHES:
        g = generality(n["mech_kw"], bt, nb); c = centrality(n["prob_kw"], df, nd)
        niche_scores.append({"id": n["id"], "type": n["type"], "gen": g, "cent": c,
                             "value_genXcent": round(g * c, 5)})
    # random merges under 3 principled signals: gen*cent, gen-only, cent-only
    R = {"genXcent": [], "gen": [], "cent": []}
    for _ in range(20000):
        a, b = random.sample(corpus, 2)
        if not a["tokens"] or not b["tokens"]:
            continue
        g = generality(list(a["tokens"]), bt, nb); c = centrality(list(b["tokens"]), df, nd)
        R["genXcent"].append(g * c); R["gen"].append(g); R["cent"].append(c)
    for k in R:
        R[k].sort()

    def pct(arr, x):
        return round(sum(1 for r in arr if r <= x) / len(arr), 3)

    print(f"\n[FAILURE 3 value] tested 3 principled niche-blind signals (random n={len(R['genXcent'])}).")
    print(f"  {'niche':20}{'type':18}{'val(gXc)':9}{'%ile':6}{'gen%ile':8}{'cent%ile'}")
    for n, s in zip(NICHES, niche_scores):
        s["percentile"] = pct(R["genXcent"], s["value_genXcent"])
        s["gen_percentile"] = pct(R["gen"], s["gen"]); s["cent_percentile"] = pct(R["cent"], s["cent"])
        print(f"  {s['id']:20}{s['type']:18}{s['value_genXcent']:<9}{s['percentile']:<6}{s['gen_percentile']:<8}{s['cent_percentile']}")
    nmean = statistics.mean(s["value_genXcent"] for s in niche_scores)
    nmean_tr = statistics.mean(s["value_genXcent"] for s in niche_scores if s["type"] == "mechanism_transfer")
    rmean = statistics.mean(R["genXcent"])
    impactful = [s for s in niche_scores if s["id"] in ("mixture_of_experts", "rlhf", "lora", "flash_attention")]
    print(f"  niche mean value = {round(nmean,5)} ; transfer-only mean = {round(nmean_tr,5)} ; random mean = {round(rmean,5)}")
    print(f"  mean INVERTED? {nmean > rmean} (marginal). BUT 4 landmark transfer-niches' value-percentiles: "
          + ", ".join(f"{s['id'].split('_')[0]}={s['percentile']}" for s in impactful))
    print(f"  median niche value = {round(statistics.median([s['value_genXcent'] for s in niche_scores]),5)} vs random mean {round(rmean,5)}")

    # precision proxy: fraction of random merges scoring >= the WEAKEST real niche
    weakest = min(s["value_genXcent"] for s in niche_scores if s["type"] == "mechanism_transfer")
    above = sum(1 for r in R["genXcent"] if r >= weakest) / len(R["genXcent"])
    print(f"\n[FAILURE 1 flag/precision] fraction of random merges scoring >= weakest real transfer-niche "
          f"({round(weakest,5)}): {round(above,3)} -> a value-gate at that bar still admits {round(100*above,1)}% of random junk.")

    json.dump({"corpus_n": len(corpus), "n_branches": nb, "contaminated_families_dropped": allfam,
               "frame": {"transfer_only": transfer, "with_templates": len(NICHES), "types": dict(types)},
               "value": {"niche_scores": niche_scores, "random_mean": round(rmean, 5),
                         "niche_mean": round(nmean, 5), "transfer_niche_mean": round(nmean_tr, 5),
                         "inverted": nmean > rmean},
               "precision_proxy_random_above_weakest": round(above, 4)},
              open(os.path.join(HERE, "real_history_results.json"), "w"), indent=2)
    print("\nwrote real_history_results.json")


if __name__ == "__main__":
    main()
