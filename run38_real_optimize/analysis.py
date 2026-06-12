#!/usr/bin/env python3
"""
analysis.py  —  Run 38: attack failures 1+3 with the new angles, scored on the
SCALED real-history GT (43 WebSearch-verified niches) on the real 791 banks.

Tests:
  A. static signals (Run 37's gen/cent/product) on 43 niches vs random — does the
     5x-larger GT change the verdict? per-niche distribution, not mean.
  B. ANGLE-2 bottleneck: RECALL (fraction of niches addressing a known bottleneck)
     vs PRECISION (within the efficiency cluster, 8 methods all hit the SAME
     attention bottleneck — can any signal pick the WINNERS from the faded ones?).
     This is the winner-vs-loser test with REAL outcomes (not random negatives),
     which is the only honest way around the survivorship-bias problem.
Contamination (R13): the niche families are dropped from the corpus before
computing signals (decontaminated 774-concept corpus).
"""
import json, os, re, random, statistics
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BANKS = os.path.join(HERE, "..", "run31_real_encyclopedia")
STOP = set("the a an of to and or in on for with by from as is are be that this it its into using "
           "use used uses which their they them then than over under within without between across each "
           "both more most less via at can may also such one two per based method model models approach".split())

# outcome labels for the efficiency cluster (REAL adoption, hindsight — flagged).
# winner = broadly adopted / still used 2024+; faded = largely superseded.
EFF_OUTCOME = {"Mamba": "winner", "Longformer": "winner",
               "Sparse Transformer": "faded", "Reformer": "faded", "Linformer": "faded",
               "Performer": "faded", "Nystromformer": "faded", "FNet": "faded"}


def toks(*xs):
    out = set()
    for x in xs:
        if not x:
            continue
        if isinstance(x, list):
            x = " ".join(x)
        for w in re.findall(r"[a-z][a-z0-9\-]{2,}", str(x).lower()):
            if w not in STOP and len(w) >= 4:
                out.add(w)
    return out


def load_corpus(drop):
    cs = []
    for fn, bf in (("life_bank.json", "branch"), ("tech_bank.json", "subfield")):
        raw = json.load(open(os.path.join(BANKS, fn)))
        items = raw if isinstance(raw, list) else raw.get("techniques", raw.get("concepts", []))
        for c in items:
            nm = (c.get("name") or "").lower()
            if any(k in nm for k in drop):
                continue
            br = (c.get(bf) or c.get("domain") or c.get("branch") or "?").split("/")[0].strip()
            cs.append({"branch": br, "tokens": toks(c.get("name"), c.get("capability_it_enables"),
                       c.get("summary_verbatim"), c.get("mechanism_atoms"), c.get("domain"))})
    return cs


def main():
    random.seed(38)
    niches = json.load(open(os.path.join(HERE, "niches_gt.json")))
    # decontaminate: drop niche family name-words from the corpus
    drop = set()
    for n in niches:
        for w in re.findall(r"[a-z]{4,}", n["name"].lower()):
            drop.add(w)
    drop |= {"flashattention", "mamba", "lora", "qlora", "transformer", "moe", "dropout", "adam"}
    corpus = load_corpus(drop)
    bt, df = defaultdict(set), Counter()
    for c in corpus:
        for t in c["tokens"]:
            bt[t].add(c["branch"]); df[t] += 1
    nb = len(set(c["branch"] for c in corpus)); nd = len(corpus)

    def gen(ks):
        v = [len(bt.get(k, set())) / nb for k in ks if k in bt]; return statistics.mean(v) if v else 0.0
    def cent(ks):
        v = [df.get(k, 0) / nd for k in ks if k in df]; return statistics.mean(v) if v else 0.0

    # random baseline
    R = {"gxc": [], "gen": [], "cent": []}
    for _ in range(20000):
        a, b = random.sample(corpus, 2)
        if a["tokens"] and b["tokens"]:
            g, c = gen(a["tokens"]), cent(b["tokens"])
            R["gxc"].append(g * c); R["gen"].append(g); R["cent"].append(c)
    for k in R: R[k].sort()
    def pct(arr, x): return round(sum(1 for r in arr if r <= x) / len(arr), 3)

    # A. static signals on 43 niches
    rows = []
    for n in niches:
        mk = toks(n.get("mechanism")); pk = toks(n.get("target_problem"))
        g, c = gen(mk), cent(pk)
        rows.append({"name": n["name"], "area": n["_area"], "gen": round(g, 4), "cent": round(c, 4),
                     "gxc": round(g * c, 6), "gxc_pct": pct(R["gxc"], g * c)})
    med = statistics.median(r["gxc"] for r in rows)
    below = sum(1 for r in rows if r["gxc_pct"] < 0.5)
    print(f"[A static signals] {len(rows)} real niches vs random (decontaminated corpus {nd} concepts).")
    print(f"  niche median gxc={round(med,6)} vs random mean={round(statistics.mean(R['gxc']),6)}")
    print(f"  niches scoring BELOW random median: {below}/{len(rows)} ({round(100*below/len(rows))}%)")
    print(f"  gxc-percentile distribution: min={min(r['gxc_pct'] for r in rows)} "
          f"q1={sorted(r['gxc_pct'] for r in rows)[len(rows)//4]} "
          f"median={statistics.median(r['gxc_pct'] for r in rows)} "
          f"q3={sorted(r['gxc_pct'] for r in rows)[3*len(rows)//4]} max={max(r['gxc_pct'] for r in rows)}")

    # B. bottleneck recall vs precision
    recall = sum(1 for n in niches if n.get("bottleneck_before"))
    print(f"\n[B bottleneck] RECALL: {recall}/{len(niches)} ({round(100*recall/len(niches))}%) real niches addressed a known pre-dating bottleneck.")
    eff = [r for r in rows if r["area"] == "efficiency"]
    print(f"  PRECISION test — efficiency cluster (all 8 hit the SAME attention bottleneck, all bottleneck_before=true):")
    print(f"  {'method':22}{'outcome':8}{'gen':8}{'cent':8}{'gxc_pct'}")
    for r in sorted(eff, key=lambda r: -r["gxc"]):
        oc = EFF_OUTCOME.get(r["name"], "?")
        print(f"  {r['name']:22}{oc:8}{r['gen']:<8}{r['cent']:<8}{r['gxc_pct']}")
    winners = [r["gxc"] for r in eff if EFF_OUTCOME.get(r["name"]) == "winner"]
    faded = [r["gxc"] for r in eff if EFF_OUTCOME.get(r["name"]) == "faded"]
    print(f"  winner mean gxc={round(statistics.mean(winners),6)} vs faded mean={round(statistics.mean(faded),6)} "
          f"-> separates winners from losers? {statistics.mean(winners) > statistics.mean(faded)}")
    print(f"  (all 8 share the bottleneck signal; bottleneck-framing gives RECALL of the hot area, not PRECISION on the winner)")

    json.dump({"n_niches": len(niches), "corpus_n": nd,
               "static_niche_median_gxc": round(med, 6), "random_mean_gxc": round(statistics.mean(R["gxc"]), 6),
               "niches_below_random_median": below, "bottleneck_recall": recall,
               "efficiency_cluster": [{"name": r["name"], "outcome": EFF_OUTCOME.get(r["name"]),
                                       "gxc": r["gxc"], "gxc_pct": r["gxc_pct"]} for r in eff],
               "winner_mean": round(statistics.mean(winners), 6), "faded_mean": round(statistics.mean(faded), 6),
               "all_rows": rows},
              open(os.path.join(HERE, "analysis_results.json"), "w"), indent=2)
    print("\nwrote analysis_results.json")


if __name__ == "__main__":
    main()
