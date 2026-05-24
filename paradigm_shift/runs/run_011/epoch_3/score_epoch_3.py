"""Epoch 3 scoring driver."""
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
ATOMS.update(_atoms_from(THIS_DIR / "atoms" / "altman_atoms.json"))
ATOMS.update(_atoms_from(THIS_DIR.parent / "epoch_1" / "atoms" / "pg_atoms.json"))
ATOMS.update(_atoms_from(THIS_DIR.parent / "epoch_2" / "atoms" / "karpathy_atoms.json"))

ARXIV_REUSED = {
    "ARXIV_R10_neuroai": Atom("ARXIV_R10_neuroai", "arxiv:2604.18637", "arxiv", "neuroai_authors",
        "NeuroAI bridges neuroscience and AI capability gaps via cognitive_function and body_world_coupling axes.",
        "mechanism", ["neuroscience", "cognitive_function"]),
    "ARXIV_R10_market_making": Atom("ARXIV_R10_market_making", "arxiv:2511.17621", "arxiv", "market_making_authors",
        "Market making mechanisms apply to multi-agent LLM safety via market_clearing and selection_pressure axes.",
        "mechanism", ["economics", "market_clearing"]),
    "ARXIV_R10_thermodynamics": Atom("ARXIV_R10_thermodynamics", "arxiv:2506.01506", "arxiv", "thermo_dl_authors",
        "Deep learning of thermodynamic laws; energy_constraint axis.",
        "mechanism", ["thermodynamics", "energy_constraint"]),
    "ARXIV_R10_evodevo": Atom("ARXIV_R10_evodevo", "arxiv:2506.12891", "arxiv", "evodevo_authors",
        "Evolutionary developmental biology supplies design principles (selection_pressure) for AI architectures.",
        "mechanism", ["biology", "evodevo", "selection_pressure"]),
}
ATOMS.update(ARXIV_REUSED)


HARNESS_INPUTS = {
    "CAND_011_E3_001": dict(arxiv_hit_count_24m=4,  recent_paper_count=10, saturation_cluster_distance=0.55, arxiv_citations_supporting=["2505.14235","2506.22355"],                     belinda_3q_passes=True),
    "CAND_011_E3_002": dict(arxiv_hit_count_24m=1,  recent_paper_count=3,  saturation_cluster_distance=0.85, arxiv_citations_supporting=["2506.01506"],                                       belinda_3q_passes=True),
    "CAND_011_E3_003": dict(arxiv_hit_count_24m=2,  recent_paper_count=5,  saturation_cluster_distance=0.70, arxiv_citations_supporting=["2511.17621"],                                       belinda_3q_passes=True),
    "CAND_011_E3_004": dict(arxiv_hit_count_24m=3,  recent_paper_count=8,  saturation_cluster_distance=0.55, arxiv_citations_supporting=["alphaevolve_2025","darwin_godel_machine_2025"], belinda_3q_passes=True),
    "CAND_011_E3_005": dict(arxiv_hit_count_24m=2,  recent_paper_count=6,  saturation_cluster_distance=0.75, arxiv_citations_supporting=[],                                                    belinda_3q_passes=True),
    "CAND_011_E3_006": dict(arxiv_hit_count_24m=2,  recent_paper_count=5,  saturation_cluster_distance=0.75, arxiv_citations_supporting=[],                                                    belinda_3q_passes=True),
    "CAND_011_E3_007": dict(arxiv_hit_count_24m=2,  recent_paper_count=4,  saturation_cluster_distance=0.80, arxiv_citations_supporting=["2506.12891"],                                       belinda_3q_passes=True),
    "CAND_011_E3_008": dict(arxiv_hit_count_24m=4,  recent_paper_count=20, saturation_cluster_distance=0.25, arxiv_citations_supporting=[],                                                    belinda_3q_passes=True),
    "CAND_011_E3_009": dict(arxiv_hit_count_24m=2,  recent_paper_count=7,  saturation_cluster_distance=0.60, arxiv_citations_supporting=[],                                                    belinda_3q_passes=True),
    "CAND_011_E3_010": dict(arxiv_hit_count_24m=0,  recent_paper_count=1,  saturation_cluster_distance=0.95, arxiv_citations_supporting=[],                                                    belinda_3q_passes=True),
    "CAND_011_E3_011": dict(arxiv_hit_count_24m=1,  recent_paper_count=3,  saturation_cluster_distance=0.80, arxiv_citations_supporting=[],                                                    belinda_3q_passes=True),
    "CAND_011_E3_012": dict(arxiv_hit_count_24m=3,  recent_paper_count=9,  saturation_cluster_distance=0.50, arxiv_citations_supporting=["2604.18637"],                                       belinda_3q_passes=True),
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
    print(f"Epoch 3: scored {len(scores)} | survivors >= 0.7: {len(surv)} | rejected: {len(rej)}")
    for s in scores:
        print(f"  {s['cand_id']:20s} composite={s['composite_score']:.4f}  label={s['rlhf_label_simulated']}  topic={s['joint_topic']}")
    upd = update_weights(scores, epoch_label="run_011_epoch_3")
    snapshot_weights(THIS_DIR / "weights_snapshot", "post_epoch_3")
    print("\nWeights after epoch 3:")
    for k, v in upd["weights_after"].items():
        print(f"  {k:30s}: {v}")
