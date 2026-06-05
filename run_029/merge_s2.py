#!/usr/bin/env python3
"""Run 29 session 2 - Phase 2 consolidation.
Merge phase1_s2 sourcing files into the persistent append-only banks with
freshness (2512-2606) + dedupe checks. Prints summary; writes banks back."""
import json, re, sys, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))
def load(p): return json.load(open(os.path.join(ROOT, p)))
def save(p, d): json.dump(d, open(os.path.join(ROOT, p), "w"), indent=2, ensure_ascii=False)

FRESH = {"2512","2601","2602","2603","2604","2605","2606"}
def in_window(arxiv_id):
    m = re.match(r"^(\d{4})\.\d{4,5}$", str(arxiv_id).strip())
    return bool(m) and m.group(1) in FRESH

tech_bank = load("tech_bank.json")
life_bank = load("life_bank.json")
existing_ids = {t.get("arxiv_id") for t in tech_bank["techniques"]}
existing_tech_names = {t.get("name","").lower() for t in tech_bank["techniques"]}
existing_life_names = {c.get("name","").lower() for c in life_bank["concepts"]}

# ---- TECHNIQUES ----
tech_added, tech_rejected = [], []
for f in sorted(glob.glob(os.path.join(ROOT,"phase1_s2/tech_*.json"))):
    d = json.load(open(f)); agent = d.get("team","?")
    for t in d.get("techniques", []):
        aid = t.get("arxiv_id")
        reason = None
        if not in_window(aid): reason = f"out-of-window ({aid})"
        elif aid in existing_ids: reason = f"dup arxiv_id ({aid})"
        elif t.get("name","").lower() in existing_tech_names: reason = f"dup name ({t.get('name')})"
        if reason:
            tech_rejected.append({"name":t.get("name"),"arxiv_id":aid,"reason":reason,"agent":agent}); continue
        existing_ids.add(aid); existing_tech_names.add(t.get("name","").lower())
        entry = {
            "name": t.get("name"), "arxiv_id": aid, "arxiv_date": t.get("arxiv_date"),
            "subfield": t.get("subfield"),
            "capability_it_enables": t.get("capability_enabled") or t.get("capability_it_enables"),
            "has_usable_code": bool(t.get("has_usable_code")),
            "code_url": t.get("code_evidence") or t.get("code_url"),
            "verbatim_quote": t.get("verbatim_quote"), "source": t.get("source"),
            "_source_agent": agent, "_session": 2,
        }
        tech_bank["techniques"].append(entry); tech_added.append(entry)

# ---- CONCEPTS ----
life_added = []
PEN = {"none":0,"very-low":0,"low":0,"moderate":0,"high":0}
for f in sorted(glob.glob(os.path.join(ROOT,"phase1_s2/life_*.json"))):
    d = json.load(open(f)); agent = d.get("team","?")
    for c in d.get("concepts", []):
        if c.get("name","").lower() in existing_life_names: continue
        existing_life_names.add(c.get("name","").lower())
        pen = (c.get("ai_penetration") or "").strip().lower()
        if pen in PEN: PEN[pen]+=1
        entry = {
            "name": c.get("name"), "domain": c.get("domain"),
            "open_problem": c.get("open_problem"), "ai_penetration": pen,
            "app_market_check": c.get("app_market_check"),
            "verbatim_quote": c.get("verbatim_quote"), "source": c.get("source"),
            "_source_agent": agent, "_session": 2,
        }
        life_bank["concepts"].append(entry); life_added.append(entry)

save("tech_bank.json", tech_bank); save("life_bank.json", life_bank)

# usable_fresh (Phase-2 pass) for session 2
usable = [t for t in tech_added if t["has_usable_code"]]
save("usable_fresh_techniques_s2.json", {
    "_schema":"session-2 Phase-2 pass: fresh+usable techniques (R13)",
    "count": len(usable), "techniques": usable})

print("=== TECH ===")
print(f"new techniques ADDED: {len(tech_added)} | rejected: {len(tech_rejected)}")
print(f"  usable: {len(usable)} | vaporware(no code): {len(tech_added)-len(usable)}")
print(f"tech_bank TOTAL now: {len(tech_bank['techniques'])}")
for r in tech_rejected: print("  REJECT:", r["name"], "-", r["reason"])
print("\n  ADDED (name | arxiv | date | usable | subfield):")
for t in tech_added:
    print(f"   {t['name']} | {t['arxiv_id']} | {t['arxiv_date']} | {t['has_usable_code']} | {t['subfield']}")
print("\n=== LIFE ===")
print(f"new concepts ADDED: {len(life_added)}")
print(f"life_bank TOTAL now: {len(life_bank['concepts'])}")
print("  session-2 penetration distribution:", PEN)
print("\n  ADDED (name | penetration | app_market | domain):")
for c in life_added:
    print(f"   {c['name']} | {c['ai_penetration']} | {c.get('app_market_check')} | {c['domain']}")
