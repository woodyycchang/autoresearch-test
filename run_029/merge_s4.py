#!/usr/bin/env python3
"""Run 29 session 3 - Phase 2 consolidation. Merge phase1_s4 -> banks with
freshness (2512-2606) + dedupe. Concepts carry has_industrial_analog (R15)."""
import json, re, glob, os
ROOT = os.path.dirname(os.path.abspath(__file__))
FRESH = {"2512","2601","2602","2603","2604","2605","2606"}
def in_window(a):
    m = re.match(r"^(\d{4})\.\d{4,5}$", str(a).strip()); return bool(m) and m.group(1) in FRESH

tb = json.load(open(f"{ROOT}/tech_bank.json")); lb = json.load(open(f"{ROOT}/life_bank.json"))
eids = {t.get("arxiv_id") for t in tb["techniques"]}
etn  = {t.get("name","").lower() for t in tb["techniques"]}
eln  = {c.get("name","").lower() for c in lb["concepts"]}

tech_added, tech_rej = [], []
for f in sorted(glob.glob(f"{ROOT}/phase1_s4/tech_*.json")):
    d = json.load(open(f)); ag = d.get("team","?")
    for t in d.get("techniques", []):
        a = t.get("arxiv_id"); r = None
        if not in_window(a): r = f"out-of-window({a})"
        elif a in eids: r = f"dup-id({a})"
        elif t.get("name","").lower() in etn: r = f"dup-name"
        if r: tech_rej.append({"name":t.get("name"),"id":a,"why":r}); continue
        eids.add(a); etn.add(t.get("name","").lower())
        e = {"name":t.get("name"),"arxiv_id":a,"arxiv_date":t.get("arxiv_date"),"subfield":t.get("subfield"),
             "capability_it_enables":t.get("capability_enabled") or t.get("capability_it_enables"),
             "has_usable_code":bool(t.get("has_usable_code")),"code_url":t.get("code_evidence") or t.get("code_url"),
             "verbatim_quote":t.get("verbatim_quote"),"source":t.get("source"),"_source_agent":ag,"_session":4}
        tb["techniques"].append(e); tech_added.append(e)

life_added=[]; PEN={"none":0,"very-low":0,"low":0,"moderate":0,"high":0}; ANA={"no":0,"partial":0,"yes":0,"other":0}
for f in sorted(glob.glob(f"{ROOT}/phase1_s4/life_*.json")):
    d = json.load(open(f)); ag = d.get("team","?")
    for c in d.get("concepts", []):
        if c.get("name","").lower() in eln: continue
        eln.add(c.get("name","").lower())
        pen=(c.get("ai_penetration") or "").strip().lower()
        if pen in PEN: PEN[pen]+=1
        ana_raw=(c.get("has_industrial_analog") or "").strip().lower()
        ana = "no" if ana_raw.startswith("no") else ("partial" if ana_raw.startswith("partial") else ("yes" if ana_raw.startswith("yes") else "other"))
        ANA[ana]+=1
        e={"name":c.get("name"),"domain":c.get("domain"),"open_problem":c.get("open_problem"),
           "ai_penetration":pen,"has_industrial_analog":c.get("has_industrial_analog"),
           "app_market_check":c.get("app_market_check"),"verbatim_quote":c.get("verbatim_quote"),
           "source":c.get("source"),"_source_agent":ag,"_session":4}
        lb["concepts"].append(e); life_added.append(e)

json.dump(tb,open(f"{ROOT}/tech_bank.json","w"),indent=2,ensure_ascii=False)
json.dump(lb,open(f"{ROOT}/life_bank.json","w"),indent=2,ensure_ascii=False)
usable=[t for t in tech_added if t["has_usable_code"]]
json.dump({"_schema":"s3 Phase-2 pass: fresh+usable techniques (R13)","count":len(usable),"techniques":usable},
          open(f"{ROOT}/usable_fresh_techniques_s4.json","w"),indent=2,ensure_ascii=False)

# cross-tab: ai_penetration vs has_industrial_analog (the v2 discriminator test) over s3 concepts
xtab={}
for c in life_added:
    pen=c["ai_penetration"]; ana=(c.get("has_industrial_analog") or "")[:3].lower()
    ana="no" if ana.startswith("no") else ("par" if ana.startswith("par") else ("yes" if ana.startswith("yes") else "oth"))
    xtab.setdefault(ana,{}).setdefault(pen,0); xtab[ana][pen]+=1

print(f"TECH added {len(tech_added)} (rej {len(tech_rej)}) | usable {len(usable)} | vaporware {len(tech_added)-len(usable)} | tech_bank TOTAL {len(tb['techniques'])}")
for r in tech_rej: print("  REJ",r)
print(f"LIFE added {len(life_added)} | life_bank TOTAL {len(lb['concepts'])}")
print("  s3 penetration:",PEN)
print("  s3 has_industrial_analog:",ANA)
print("  s3 CROSS-TAB analog x penetration (the v2 test):")
for ana in ("no","par","yes","oth"):
    if ana in xtab: print(f"    analog={ana}: {xtab[ana]}")
print("\n  USABLE new techniques:")
for t in usable: print("   ",t["name"][:40],"|",t["arxiv_id"],"|",t["subfield"][:40])
