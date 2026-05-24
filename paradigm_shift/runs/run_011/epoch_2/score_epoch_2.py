"""Epoch 2 scoring driver."""
import json
import sys
from pathlib import Path

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR.parent.parent.parent))

from paradigm_shift.multi_parameter_scorer import (
    Atom, Candidate, score_candidates_for_epoch, split_survivors
)
from paradigm_shift.rlhf_weight_updater import update_weights, snapshot_weights


ATOMS_JSON = THIS_DIR / "atoms" / "karpathy_atoms.json"
SCORES_DIR = THIS_DIR / "scores"
PG_ATOMS_JSON = THIS_DIR.parent / "epoch_1" / "atoms" / "pg_atoms.json"


def _load(p, src_type_default):
    with open(p) as f:
        return json.load(f)


kp = _load(ATOMS_JSON, "blog")
pg = _load(PG_ATOMS_JSON, "essay")

ATOMS = {a["atom_id"]: Atom(
    a["atom_id"], a.get("post_title", a.get("essay_url", "")),
    a["source_type"], a["speaker_or_author"], a["text"], a["atom_type"], a["domain_tags"],
) for a in (kp["atoms"] + pg["atoms"])}

# arXiv reused
ARXIV_REUSED = {
    "ARXIV_R10_neuroai": Atom("ARXIV_R10_neuroai", "arxiv:2604.18637", "arxiv", "neuroai_authors",
        "NeuroAI bridges neuroscience and AI capability gaps via cognitive_function and body_world_coupling axes.",
        "mechanism", ["neuroscience", "cognitive_function"]),
    "ARXIV_R10_market_making": Atom("ARXIV_R10_market_making", "arxiv:2511.17621", "arxiv", "market_making_authors",
        "Market making mechanisms apply to multi-agent LLM safety via market_clearing and selection_pressure axes.",
        "mechanism", ["economics", "market_clearing"]),
    "ARXIV_R10_offline_logs": Atom("ARXIV_R10_offline_logs", "arxiv:2510.25441", "arxiv", "offline_log_authors",
        "Offline log learning as alternative to online RLHF; data_efficiency mechanism.",
        "mechanism", ["rl", "data_efficiency"]),
    "ARXIV_R10_thermodynamics": Atom("ARXIV_R10_thermodynamics", "arxiv:2506.01506", "arxiv", "thermo_dl_authors",
        "Deep learning of thermodynamic laws; energy_constraint axis.",
        "mechanism", ["thermodynamics", "energy_constraint"]),
    "ARXIV_R10_model_native_agents": Atom("ARXIV_R10_model_native_agents", "arxiv:2510.16720", "arxiv", "model_native_authors",
        "Model-native agents reject pipeline-prompt stitching; system_architecture critique of agent_pipeline.",
        "mechanism", ["ml", "system_architecture"]),
    "ARXIV_R10_evodevo": Atom("ARXIV_R10_evodevo", "arxiv:2506.12891", "arxiv", "evodevo_authors",
        "Evolutionary developmental biology supplies design principles (selection_pressure) for AI architectures.",
        "mechanism", ["biology", "evodevo", "selection_pressure"]),
    "ARXIV_R10_llm_economist": Atom("ARXIV_R10_llm_economist", "arxiv:2507.15815", "arxiv", "llm_economist_authors",
        "LLM economist applies mechanism_design to multi-agent policy.",
        "mechanism", ["economics", "mechanism_design"]),
}
ATOMS.update(ARXIV_REUSED)


HARNESS_INPUTS = {
    "CAND_011_E2_001": dict(arxiv_hit_count_24m=6,  recent_paper_count=12, saturation_cluster_distance=0.40, arxiv_citations_supporting=["2505.07634"],                                   belinda_3q_passes=True),
    "CAND_011_E2_002": dict(arxiv_hit_count_24m=3,  recent_paper_count=8,  saturation_cluster_distance=0.65, arxiv_citations_supporting=["2505.04842","2603.07360","2509.08269"],     belinda_3q_passes=True),
    "CAND_011_E2_003": dict(arxiv_hit_count_24m=0,  recent_paper_count=1,  saturation_cluster_distance=0.90, arxiv_citations_supporting=[],                                                belinda_3q_passes=True),
    "CAND_011_E2_004": dict(arxiv_hit_count_24m=5,  recent_paper_count=25, saturation_cluster_distance=0.20, arxiv_citations_supporting=["jpmorgan_guide_2025","yc_w25_data"],         belinda_3q_passes=True),
    "CAND_011_E2_005": dict(arxiv_hit_count_24m=0,  recent_paper_count=2,  saturation_cluster_distance=0.90, arxiv_citations_supporting=["2506.01506"],                                   belinda_3q_passes=True),
    "CAND_011_E2_006": dict(arxiv_hit_count_24m=0,  recent_paper_count=1,  saturation_cluster_distance=0.92, arxiv_citations_supporting=[],                                                belinda_3q_passes=True),
    "CAND_011_E2_007": dict(arxiv_hit_count_24m=0,  recent_paper_count=1,  saturation_cluster_distance=0.95, arxiv_citations_supporting=[],                                                belinda_3q_passes=True),
    "CAND_011_E2_008": dict(arxiv_hit_count_24m=1,  recent_paper_count=3,  saturation_cluster_distance=0.85, arxiv_citations_supporting=[],                                                belinda_3q_passes=True),
    "CAND_011_E2_009": dict(arxiv_hit_count_24m=1,  recent_paper_count=4,  saturation_cluster_distance=0.70, arxiv_citations_supporting=["2511.17621","2603.19328"],                    belinda_3q_passes=True),
    "CAND_011_E2_010": dict(arxiv_hit_count_24m=4,  recent_paper_count=15, saturation_cluster_distance=0.30, arxiv_citations_supporting=["2510.16720"],                                   belinda_3q_passes=True),
    "CAND_011_E2_011": dict(arxiv_hit_count_24m=2,  recent_paper_count=6,  saturation_cluster_distance=0.60, arxiv_citations_supporting=["2510.25441"],                                   belinda_3q_passes=True),
    "CAND_011_E2_012": dict(arxiv_hit_count_24m=0,  recent_paper_count=1,  saturation_cluster_distance=0.95, arxiv_citations_supporting=["2506.12891"],                                   belinda_3q_passes=True),
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
    scores = score_candidates_for_epoch(cands, SCORES_DIR)
    surv, rej = split_survivors(scores)
    print(f"Epoch 2: scored {len(scores)} | survivors >= 0.7: {len(surv)} | rejected: {len(rej)}")
    for s in scores:
        print(f"  {s['cand_id']:20s} composite={s['composite_score']:.4f}  label={s['rlhf_label_simulated']}  topic={s['joint_topic']}")
    upd = update_weights(scores, epoch_label="run_011_epoch_2")
    snapshot_weights(THIS_DIR / "weights_snapshot", "post_epoch_2")
    print("\nWeights after epoch 2:")
    for k, v in upd["weights_after"].items():
        print(f"  {k:30s}: {v}")
