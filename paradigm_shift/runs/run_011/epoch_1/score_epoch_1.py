"""Epoch 1 scoring driver — paste of harness inputs derived from web_search."""
import json
import sys
from pathlib import Path

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR.parent.parent.parent))

from paradigm_shift.multi_parameter_scorer import (
    Atom, Candidate, score_candidates_for_epoch, split_survivors
)
from paradigm_shift.rlhf_weight_updater import update_weights, snapshot_weights


PG_ATOMS_JSON = THIS_DIR / "atoms" / "pg_atoms.json"
SCORES_DIR = THIS_DIR / "scores"


with open(PG_ATOMS_JSON) as f:
    pg = json.load(f)
PG_ATOMS = {a["atom_id"]: Atom(
    atom_id=a["atom_id"],
    source_id=a["essay_url"],
    source_type=a["source_type"],
    speaker_or_author=a["speaker_or_author"],
    text=a["text"],
    atom_type=a["atom_type"],
    domain_tags=a["domain_tags"],
) for a in pg["atoms"]}

# Inline arXiv atoms reused from Run 10 cross-disciplinary pool
ARXIV_REUSED = {
    "ARXIV_R10_neuroai": Atom(
        "ARXIV_R10_neuroai", "arxiv:2604.18637", "arxiv", "neuroai_authors",
        "NeuroAI bridges neuroscience and AI capability gaps via cognitive_function and body_world_coupling axes.",
        "mechanism", ["neuroscience", "cognitive_function"]),
    "ARXIV_R10_market_making": Atom(
        "ARXIV_R10_market_making", "arxiv:2511.17621", "arxiv", "market_making_authors",
        "Market making mechanisms apply to multi-agent LLM safety via market_clearing and selection_pressure axes.",
        "mechanism", ["economics", "market_clearing"]),
    "ARXIV_R10_offline_logs": Atom(
        "ARXIV_R10_offline_logs", "arxiv:2510.25441", "arxiv", "offline_log_authors",
        "Offline log learning as alternative to online RLHF; data_efficiency mechanism.",
        "mechanism", ["rl", "data_efficiency"]),
    "ARXIV_R10_thermodynamics": Atom(
        "ARXIV_R10_thermodynamics", "arxiv:2506.01506", "arxiv", "thermo_dl_authors",
        "Deep learning of thermodynamic laws; energy_constraint axis.",
        "mechanism", ["thermodynamics", "energy_constraint"]),
    "ARXIV_R10_model_native_agents": Atom(
        "ARXIV_R10_model_native_agents", "arxiv:2510.16720", "arxiv", "model_native_authors",
        "Model-native agents reject pipeline-prompt stitching; system_architecture critique of agent_pipeline.",
        "mechanism", ["ml", "system_architecture"]),
    "ARXIV_R10_evodevo": Atom(
        "ARXIV_R10_evodevo", "arxiv:2506.12891", "arxiv", "evodevo_authors",
        "Evolutionary developmental biology supplies design principles (selection_pressure) for AI architectures.",
        "mechanism", ["biology", "evodevo", "selection_pressure"]),
    "ARXIV_R10_llm_economist": Atom(
        "ARXIV_R10_llm_economist", "arxiv:2507.15815", "arxiv", "llm_economist_authors",
        "LLM economist applies mechanism_design to multi-agent policy.",
        "mechanism", ["economics", "mechanism_design"]),
}

ATOMS = {**PG_ATOMS, **ARXIV_REUSED}


# Harness-supplied saturation inputs from epoch 1 web_searches.
# UPDATED after deep saturation search on putative survivors:
#   CAND_008: arxiv:2506.12891 bridges evodevo->AI; 2603.14664, 2603.07360 cover selection_pressure as curriculum strategy. Saturated.
#   CAND_005: PMC12883739 (entropy externalization free-energy), 2507.00181 (cognitive engagement decline), 2504.05328 (Watts-per-Intelligence). Saturated.
HARNESS_INPUTS = {
    "CAND_011_E1_001": dict(arxiv_hit_count_24m=8,  recent_paper_count=12, saturation_cluster_distance=0.50, arxiv_citations_supporting=["2506.08872","2508.16628"], belinda_3q_passes=True),
    "CAND_011_E1_002": dict(arxiv_hit_count_24m=2,  recent_paper_count=6,  saturation_cluster_distance=0.80, arxiv_citations_supporting=[],                             belinda_3q_passes=True),
    "CAND_011_E1_003": dict(arxiv_hit_count_24m=3,  recent_paper_count=5,  saturation_cluster_distance=0.65, arxiv_citations_supporting=["2511.17621"],                belinda_3q_passes=True),
    "CAND_011_E1_004": dict(arxiv_hit_count_24m=1,  recent_paper_count=4,  saturation_cluster_distance=0.80, arxiv_citations_supporting=["2510.25441"],                belinda_3q_passes=True),
    "CAND_011_E1_005": dict(arxiv_hit_count_24m=4,  recent_paper_count=8,  saturation_cluster_distance=0.45, arxiv_citations_supporting=["2506.08872","2507.00181","2504.05328"], belinda_3q_passes=True),
    "CAND_011_E1_006": dict(arxiv_hit_count_24m=1,  recent_paper_count=2,  saturation_cluster_distance=0.90, arxiv_citations_supporting=[],                             belinda_3q_passes=True),
    "CAND_011_E1_007": dict(arxiv_hit_count_24m=2,  recent_paper_count=5,  saturation_cluster_distance=0.75, arxiv_citations_supporting=["2510.16720"],                belinda_3q_passes=True),
    "CAND_011_E1_008": dict(arxiv_hit_count_24m=3,  recent_paper_count=5,  saturation_cluster_distance=0.55, arxiv_citations_supporting=["2506.12891","2603.14664","2603.07360"], belinda_3q_passes=True),
    "CAND_011_E1_009": dict(arxiv_hit_count_24m=0,  recent_paper_count=1,  saturation_cluster_distance=0.92, arxiv_citations_supporting=[],                             belinda_3q_passes=True),
    "CAND_011_E1_010": dict(arxiv_hit_count_24m=4,  recent_paper_count=8,  saturation_cluster_distance=0.60, arxiv_citations_supporting=["2507.15815"],                belinda_3q_passes=True),
    "CAND_011_E1_011": dict(arxiv_hit_count_24m=5,  recent_paper_count=7,  saturation_cluster_distance=0.70, arxiv_citations_supporting=["2506.08872"],                belinda_3q_passes=True),
    "CAND_011_E1_012": dict(arxiv_hit_count_24m=0,  recent_paper_count=1,  saturation_cluster_distance=0.95, arxiv_citations_supporting=[],                             belinda_3q_passes=True),
}


def build_candidates():
    with open(THIS_DIR / "candidates.json") as f:
        spec = json.load(f)
    cands = []
    for c in spec["candidates"]:
        a = ATOMS[c["atom_a"]]
        b = ATOMS[c["atom_b"]]
        h = HARNESS_INPUTS[c["cand_id"]]
        cands.append(Candidate(
            cand_id=c["cand_id"], atom_a=a, atom_b=b,
            joint_topic=c["joint_topic"],
            **h,
        ))
    return cands


if __name__ == "__main__":
    cands = build_candidates()
    scores = score_candidates_for_epoch(cands, SCORES_DIR)
    surv, rej = split_survivors(scores)
    print(f"Epoch 1: scored {len(scores)} | survivors >= 0.7: {len(surv)} | rejected: {len(rej)}")
    for s in scores:
        print(f"  {s['cand_id']:20s} composite={s['composite_score']:.4f}  label={s['rlhf_label_simulated']}  topic={s['joint_topic']}")
    upd = update_weights(scores, epoch_label="run_011_epoch_1")
    snapshot_weights(THIS_DIR / "weights_snapshot", "post_epoch_1")
    print("\nWeight update applied:")
    for k, v in upd["weights_after"].items():
        print(f"  {k:30s}: {v}")
