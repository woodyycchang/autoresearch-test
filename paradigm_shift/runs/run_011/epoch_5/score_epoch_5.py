"""Epoch 5 scoring driver."""
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
for sub in ["epoch_1/atoms/pg_atoms.json", "epoch_2/atoms/karpathy_atoms.json",
            "epoch_3/atoms/altman_atoms.json", "epoch_4/atoms/openai_atoms.json",
            "epoch_5/atoms/anthropic_atoms.json"]:
    ATOMS.update(_atoms_from(THIS_DIR.parent / sub))

ARXIV_REUSED = {
    "ARXIV_R10_neuroai": Atom("ARXIV_R10_neuroai", "arxiv:2604.18637", "arxiv", "neuroai_authors",
        "NeuroAI bridges neuroscience and AI capability gaps.", "mechanism", ["neuroscience"]),
    "ARXIV_R10_market_making": Atom("ARXIV_R10_market_making", "arxiv:2511.17621", "arxiv", "market_making",
        "Market making for multi-agent LLM safety.", "mechanism", ["economics", "market_clearing"]),
    "ARXIV_R10_thermodynamics": Atom("ARXIV_R10_thermodynamics", "arxiv:2506.01506", "arxiv", "thermo",
        "Deep learning of thermodynamic laws; energy_constraint.", "mechanism", ["thermodynamics", "energy_constraint"]),
    "ARXIV_R10_evodevo": Atom("ARXIV_R10_evodevo", "arxiv:2506.12891", "arxiv", "evodevo",
        "Evolutionary developmental biology design principles for AI.", "mechanism", ["biology", "selection_pressure"]),
}
ATOMS.update(ARXIV_REUSED)


HARNESS_INPUTS = {
    "CAND_011_E5_001": dict(arxiv_hit_count_24m=5, recent_paper_count=12, saturation_cluster_distance=0.40, arxiv_citations_supporting=["2604.08401","2505.04842"], belinda_3q_passes=True),
    "CAND_011_E5_002": dict(arxiv_hit_count_24m=2, recent_paper_count=8,  saturation_cluster_distance=0.55, arxiv_citations_supporting=["2510.14053","2511.17621","metr_2025"], belinda_3q_passes=True),
    "CAND_011_E5_003": dict(arxiv_hit_count_24m=1, recent_paper_count=6,  saturation_cluster_distance=0.65, arxiv_citations_supporting=["openai_c2pa_2026","glasswing_partners"], belinda_3q_passes=True),
    "CAND_011_E5_004": dict(arxiv_hit_count_24m=2, recent_paper_count=5,  saturation_cluster_distance=0.75, arxiv_citations_supporting=["glasswing_report_2026"], belinda_3q_passes=True),
    "CAND_011_E5_005": dict(arxiv_hit_count_24m=3, recent_paper_count=8,  saturation_cluster_distance=0.55, arxiv_citations_supporting=["2603.29231","2604.02734"], belinda_3q_passes=True),
    "CAND_011_E5_006": dict(arxiv_hit_count_24m=1, recent_paper_count=3,  saturation_cluster_distance=0.80, arxiv_citations_supporting=[], belinda_3q_passes=True),
    "CAND_011_E5_007": dict(arxiv_hit_count_24m=2, recent_paper_count=6,  saturation_cluster_distance=0.65, arxiv_citations_supporting=["2511.17621"], belinda_3q_passes=True),
    "CAND_011_E5_008": dict(arxiv_hit_count_24m=0, recent_paper_count=2,  saturation_cluster_distance=0.90, arxiv_citations_supporting=["2506.12891"], belinda_3q_passes=True),
    "CAND_011_E5_009": dict(arxiv_hit_count_24m=1, recent_paper_count=4,  saturation_cluster_distance=0.80, arxiv_citations_supporting=[], belinda_3q_passes=True),
    "CAND_011_E5_010": dict(arxiv_hit_count_24m=1, recent_paper_count=3,  saturation_cluster_distance=0.85, arxiv_citations_supporting=[], belinda_3q_passes=True),
    "CAND_011_E5_011": dict(arxiv_hit_count_24m=2, recent_paper_count=6,  saturation_cluster_distance=0.65, arxiv_citations_supporting=["2506.01506"], belinda_3q_passes=True),
    "CAND_011_E5_012": dict(arxiv_hit_count_24m=1, recent_paper_count=4,  saturation_cluster_distance=0.75, arxiv_citations_supporting=[], belinda_3q_passes=True),
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
    print(f"Epoch 5: scored {len(scores)} | survivors >= 0.7: {len(surv)} | rejected: {len(rej)}")
    for s in scores:
        print(f"  {s['cand_id']:20s} composite={s['composite_score']:.4f}  label={s['rlhf_label_simulated']}  topic={s['joint_topic']}")
    upd = update_weights(scores, epoch_label="run_011_epoch_5")
    snapshot_weights(THIS_DIR / "weights_snapshot", "post_epoch_5")
