"""Epoch 6 scoring driver."""
import json, sys
from pathlib import Path

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR.parent.parent.parent))

from paradigm_shift.multi_parameter_scorer import (
    Atom, Candidate, score_candidates_for_epoch, split_survivors
)
from paradigm_shift.rlhf_weight_updater import update_weights, snapshot_weights


def _atoms_from(p):
    with open(p) as f: d = json.load(f)
    return {a["atom_id"]: Atom(
        a["atom_id"], a.get("post_title", a.get("essay_url","")),
        a["source_type"], a["speaker_or_author"], a["text"], a["atom_type"], a["domain_tags"],
    ) for a in d["atoms"]}


ATOMS = {}
for sub in ["epoch_1/atoms/pg_atoms.json","epoch_2/atoms/karpathy_atoms.json",
            "epoch_3/atoms/altman_atoms.json","epoch_4/atoms/openai_atoms.json",
            "epoch_5/atoms/anthropic_atoms.json","epoch_6/atoms/hn_atoms.json"]:
    ATOMS.update(_atoms_from(THIS_DIR.parent / sub))

ARXIV_REUSED = {
    "ARXIV_R10_neuroai": Atom("ARXIV_R10_neuroai","arxiv:2604.18637","arxiv","neuroai",
        "NeuroAI bridges neuroscience and AI.","mechanism",["neuroscience"]),
    "ARXIV_R10_market_making": Atom("ARXIV_R10_market_making","arxiv:2511.17621","arxiv","mm",
        "Market making for multi-agent LLM safety.","mechanism",["economics","market_clearing"]),
    "ARXIV_R10_thermodynamics": Atom("ARXIV_R10_thermodynamics","arxiv:2506.01506","arxiv","td",
        "Deep learning of thermodynamic laws; energy_constraint.","mechanism",["thermodynamics","energy_constraint"]),
    "ARXIV_R10_evodevo": Atom("ARXIV_R10_evodevo","arxiv:2506.12891","arxiv","ed",
        "Evolutionary developmental biology design principles for AI.","mechanism",["biology","selection_pressure"]),
}
ATOMS.update(ARXIV_REUSED)


HARNESS_INPUTS = {
    "CAND_011_E6_001": dict(arxiv_hit_count_24m=3, recent_paper_count=8,  saturation_cluster_distance=0.55, arxiv_citations_supporting=["2306.06604","2108.12648","elight_2025"], belinda_3q_passes=True),
    "CAND_011_E6_002": dict(arxiv_hit_count_24m=2, recent_paper_count=4,  saturation_cluster_distance=0.75, arxiv_citations_supporting=["2306.06604","2506.01506"], belinda_3q_passes=True),
    "CAND_011_E6_003": dict(arxiv_hit_count_24m=1, recent_paper_count=5,  saturation_cluster_distance=0.75, arxiv_citations_supporting=["jupiter_2026"], belinda_3q_passes=True),
    "CAND_011_E6_004": dict(arxiv_hit_count_24m=1, recent_paper_count=4,  saturation_cluster_distance=0.80, arxiv_citations_supporting=["2510.23089"], belinda_3q_passes=True),
    "CAND_011_E6_005": dict(arxiv_hit_count_24m=2, recent_paper_count=6,  saturation_cluster_distance=0.65, arxiv_citations_supporting=["2510.23089","flatiron_2026"], belinda_3q_passes=True),
    "CAND_011_E6_006": dict(arxiv_hit_count_24m=4, recent_paper_count=15, saturation_cluster_distance=0.35, arxiv_citations_supporting=["jack_clark_2026","sakana_dgm","alphaevolve_2025"], belinda_3q_passes=True),
    "CAND_011_E6_007": dict(arxiv_hit_count_24m=2, recent_paper_count=8,  saturation_cluster_distance=0.55, arxiv_citations_supporting=["2603.29231","2604.02734","metr_2026"], belinda_3q_passes=True),
    "CAND_011_E6_008": dict(arxiv_hit_count_24m=2, recent_paper_count=8,  saturation_cluster_distance=0.55, arxiv_citations_supporting=["2509.16941","2512.18470","2602.09447"], belinda_3q_passes=True),
    "CAND_011_E6_009": dict(arxiv_hit_count_24m=1, recent_paper_count=5,  saturation_cluster_distance=0.70, arxiv_citations_supporting=["openai_daybreak_2026","glasswing_2026"], belinda_3q_passes=True),
    "CAND_011_E6_010": dict(arxiv_hit_count_24m=0, recent_paper_count=2,  saturation_cluster_distance=0.90, arxiv_citations_supporting=["mdash_2026","2506.12891"], belinda_3q_passes=True),
    "CAND_011_E6_011": dict(arxiv_hit_count_24m=1, recent_paper_count=4,  saturation_cluster_distance=0.75, arxiv_citations_supporting=["karpathy_anthropic_2026"], belinda_3q_passes=True),
    "CAND_011_E6_012": dict(arxiv_hit_count_24m=3, recent_paper_count=12, saturation_cluster_distance=0.40, arxiv_citations_supporting=["hacker_news_2fa_2026","glasswing_2026"], belinda_3q_passes=True),
}


def build_candidates():
    with open(THIS_DIR / "candidates.json") as f:
        spec = json.load(f)
    cands = []
    for c in spec["candidates"]:
        a = ATOMS[c["atom_a"]]
        b = ATOMS[c["atom_b"]]
        h = HARNESS_INPUTS[c["cand_id"]]
        cands.append(Candidate(c["cand_id"], a, b, c["joint_topic"], **h))
    return cands


if __name__ == "__main__":
    cands = build_candidates()
    scores = score_candidates_for_epoch(cands, THIS_DIR / "scores")
    surv, rej = split_survivors(scores)
    print(f"Epoch 6: scored {len(scores)} | survivors >= 0.7: {len(surv)} | rejected: {len(rej)}")
    for s in scores:
        print(f"  {s['cand_id']:20s} composite={s['composite_score']:.4f}  label={s['rlhf_label_simulated']}  topic={s['joint_topic']}")
    upd = update_weights(scores, epoch_label="run_011_epoch_6")
    snapshot_weights(THIS_DIR / "weights_snapshot", "post_epoch_6")
