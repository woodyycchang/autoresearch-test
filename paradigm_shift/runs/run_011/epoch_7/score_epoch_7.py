"""Epoch 7 scoring driver."""
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
            "epoch_5/atoms/anthropic_atoms.json","epoch_6/atoms/hn_atoms.json",
            "epoch_7/atoms/search_atoms.json"]:
    ATOMS.update(_atoms_from(THIS_DIR.parent / sub))

ARXIV_REUSED = {
    "ARXIV_R10_neuroai": Atom("ARXIV_R10_neuroai","arxiv:2604.18637","arxiv","na","NeuroAI bridge.","mechanism",["neuroscience"]),
    "ARXIV_R10_market_making": Atom("ARXIV_R10_market_making","arxiv:2511.17621","arxiv","mm","Market making safety.","mechanism",["economics","market_clearing"]),
    "ARXIV_R10_thermodynamics": Atom("ARXIV_R10_thermodynamics","arxiv:2506.01506","arxiv","td","Thermodynamics deep learning.","mechanism",["thermodynamics","energy_constraint"]),
    "ARXIV_R10_evodevo": Atom("ARXIV_R10_evodevo","arxiv:2506.12891","arxiv","ed","EvoDevo for AI.","mechanism",["biology","selection_pressure"]),
}
ATOMS.update(ARXIV_REUSED)


HARNESS_INPUTS = {
    "CAND_011_E7_001": dict(arxiv_hit_count_24m=3, recent_paper_count=8, saturation_cluster_distance=0.55, arxiv_citations_supporting=["2512.24695","PMC11275831","2511.10101"], belinda_3q_passes=True),
    "CAND_011_E7_002": dict(arxiv_hit_count_24m=2, recent_paper_count=6, saturation_cluster_distance=0.70, arxiv_citations_supporting=["nested_learning_paper","claude_opus_4_7"], belinda_3q_passes=True),
    "CAND_011_E7_003": dict(arxiv_hit_count_24m=2, recent_paper_count=5, saturation_cluster_distance=0.75, arxiv_citations_supporting=["2512.24601"], belinda_3q_passes=True),
    "CAND_011_E7_004": dict(arxiv_hit_count_24m=1, recent_paper_count=4, saturation_cluster_distance=0.80, arxiv_citations_supporting=["2512.24601","2506.01506"], belinda_3q_passes=True),
    "CAND_011_E7_005": dict(arxiv_hit_count_24m=5, recent_paper_count=15, saturation_cluster_distance=0.35, arxiv_citations_supporting=["2506.02996","2603.29090","2601.17094"], belinda_3q_passes=True),
    "CAND_011_E7_006": dict(arxiv_hit_count_24m=2, recent_paper_count=6, saturation_cluster_distance=0.65, arxiv_citations_supporting=["2511.05963"], belinda_3q_passes=True),
    "CAND_011_E7_007": dict(arxiv_hit_count_24m=1, recent_paper_count=4, saturation_cluster_distance=0.80, arxiv_citations_supporting=["2603.29090","2506.12891"], belinda_3q_passes=True),
    "CAND_011_E7_008": dict(arxiv_hit_count_24m=1, recent_paper_count=3, saturation_cluster_distance=0.85, arxiv_citations_supporting=["2601.17094"], belinda_3q_passes=True),
    "CAND_011_E7_009": dict(arxiv_hit_count_24m=2, recent_paper_count=6, saturation_cluster_distance=0.65, arxiv_citations_supporting=["primeintellect_rlmenv","glasswing_2026"], belinda_3q_passes=True),
    "CAND_011_E7_010": dict(arxiv_hit_count_24m=3, recent_paper_count=10, saturation_cluster_distance=0.50, arxiv_citations_supporting=["2506.02996","2511.05963"], belinda_3q_passes=True),
    "CAND_011_E7_011": dict(arxiv_hit_count_24m=1, recent_paper_count=3, saturation_cluster_distance=0.85, arxiv_citations_supporting=["2512.24695"], belinda_3q_passes=True),
    "CAND_011_E7_012": dict(arxiv_hit_count_24m=2, recent_paper_count=6, saturation_cluster_distance=0.70, arxiv_citations_supporting=["pfn_2024"], belinda_3q_passes=True),
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
    print(f"Epoch 7: scored {len(scores)} | survivors >= 0.7: {len(surv)} | rejected: {len(rej)}")
    for s in scores:
        print(f"  {s['cand_id']:20s} composite={s['composite_score']:.4f}  label={s['rlhf_label_simulated']}  topic={s['joint_topic']}")
    upd = update_weights(scores, epoch_label="run_011_epoch_7")
    snapshot_weights(THIS_DIR / "weights_snapshot", "post_epoch_7")
