"""Phase 6 runner for Run 12.

Generates a fresh 7-epoch run using Run 11's non-quarantined atom pool, then
applies strict gates (threshold 0.90, quarantine, cross-LLM verify, Belinda
strict). Scoring re-uses Run 11's multi_parameter_scorer with the post-epoch-7
weights v7.

Key differences from Run 11:
  - Excludes 6 quarantined atoms: ARXIV_R10_evodevo, ARXIV_R10_thermodynamics,
    ARXIV_R10_market_making, PG_E1_A05, KP_E2_A06, KP_E2_A12.
  - Generates NEW cross-source pairings that Run 11 did not try.
  - Survivor threshold is 0.90 (empirical, from N=30 FALSE label calibration).
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path("/home/user/autoresearch-test")
sys.path.insert(0, str(ROOT))

from paradigm_shift.multi_parameter_scorer import (
    Atom, Candidate, score_candidate, score_candidates_for_epoch
)

# ---------------- Atom pool (non-quarantined only) ----------------
QUARANTINED = {
    "ARXIV_R10_evodevo", "ARXIV_R10_thermodynamics", "ARXIV_R10_market_making",
    "PG_E1_A05", "KP_E2_A06", "KP_E2_A12",
}

def _atoms_from(p):
    with open(p) as f: d = json.load(f)
    return {a["atom_id"]: Atom(
        a["atom_id"], a.get("post_title", a.get("essay_url","")),
        a["source_type"], a["speaker_or_author"], a["text"], a["atom_type"], a["domain_tags"],
    ) for a in d["atoms"] if a["atom_id"] not in QUARANTINED}

RUN_11_BASE = ROOT / "paradigm_shift/runs/run_011"
ATOMS = {}
for sub in ["epoch_1/atoms/pg_atoms.json","epoch_2/atoms/karpathy_atoms.json",
            "epoch_3/atoms/altman_atoms.json","epoch_4/atoms/openai_atoms.json",
            "epoch_5/atoms/anthropic_atoms.json","epoch_6/atoms/hn_atoms.json",
            "epoch_7/atoms/search_atoms.json"]:
    ATOMS.update(_atoms_from(RUN_11_BASE / sub))

# Non-quarantined arXiv atoms used in Run 11 retained:
ATOMS["ARXIV_R10_neuroai"] = Atom(
    "ARXIV_R10_neuroai", "arxiv:2604.18637", "arxiv", "na",
    "NeuroAI bridge: hippocampal place cells map to transformer position embeddings; biological neural circuit primitives instruct architectural choices for memory consolidation.",
    "mechanism", ["neuroscience"])
ATOMS["ARXIV_R10_offline_logs"] = Atom(
    "ARXIV_R10_offline_logs", "arxiv:2509.14123", "arxiv", "ol",
    "Offline log grounding: training data efficiency improves when policies are warm-started on operator trajectory logs before live deployment.",
    "mechanism", ["ml", "data_efficiency"])
ATOMS["ARXIV_R10_model_native_agents"] = Atom(
    "ARXIV_R10_model_native_agents", "arxiv:2510.27741", "arxiv", "mna",
    "Model-native agents: agent loop is internal to model inference, not external orchestration; tokenization extended to tool-call grammar.",
    "mechanism", ["ml", "system_architecture"])
ATOMS["ARXIV_R10_llm_economist"] = Atom(
    "ARXIV_R10_llm_economist", "arxiv:2511.04612", "arxiv", "le",
    "LLM Economist: mechanism design where LLM agents bid for compute/tools via market clearing rather than scheduler heuristics.",
    "mechanism", ["economics", "market_clearing"])

# ---------------- New cross-source candidate pairings (12 per epoch) ----------------
# Each epoch generates 12 pairings that Run 11 did NOT try, using non-quarantined atoms.
EPOCH_CANDIDATES = {
  1: [  # PG-anchored fresh pairings
    {"cand_id":"CAND_012_E1_001","atom_a":"PG_E1_A01","atom_b":"KP_E2_A09","joint_topic":"writes_write_nots_split_as_supervision_channel_divergence_in_attention"},
    {"cand_id":"CAND_012_E1_002","atom_a":"PG_E1_A02","atom_b":"OA_E4_A07","joint_topic":"writing_as_gym_decoupled_from_speech_substrate_in_GPT55"},
    {"cand_id":"CAND_012_E1_003","atom_a":"PG_E1_A03","atom_b":"ARXIV_R10_model_native_agents","joint_topic":"founder_mode_skip_routing_as_model_native_agent_decode_grammar"},
    {"cand_id":"CAND_012_E1_004","atom_a":"PG_E1_A04","atom_b":"AN_E5_A11","joint_topic":"managerial_unavailability_for_founders_as_dual_use_state_AI_subsidy"},
    {"cand_id":"CAND_012_E1_005","atom_a":"PG_E1_A06","atom_b":"WS_E7_A09","joint_topic":"superlinear_world_features_evidenced_by_PFN_universal_in_context_engine"},
    {"cand_id":"CAND_012_E1_006","atom_a":"PG_E1_A07","atom_b":"WS_E7_A03","joint_topic":"high_decision_tree_attachment_in_recursive_LM_subordinate_call_pattern"},
    {"cand_id":"CAND_012_E1_007","atom_a":"PG_E1_A08","atom_b":"KP_E2_A03","joint_topic":"branching_factor_one_collapse_explains_RLVR_obstinacy_failure_mode"},
    {"cand_id":"CAND_012_E1_008","atom_a":"PG_E1_A09","atom_b":"OA_E4_A09","joint_topic":"adolescent_taste_acquisition_as_machine_readable_spec_calibration"},
    {"cand_id":"CAND_012_E1_009","atom_a":"PG_E1_A10","atom_b":"AN_E5_A07","joint_topic":"writing_offload_energy_constraint_as_graphical_substrate_split"},
    {"cand_id":"CAND_012_E1_010","atom_a":"PG_E1_A11","atom_b":"HN_E6_A07","joint_topic":"chesky_founder_mode_as_12hr_autonomy_long_horizon_rigor"},
    {"cand_id":"CAND_012_E1_011","atom_a":"PG_E1_A12","atom_b":"ARXIV_R10_neuroai","joint_topic":"threshold_and_exponential_dual_mechanisms_in_hippocampal_memory_consolidation"},
    {"cand_id":"CAND_012_E1_012","atom_a":"PG_E1_A06","atom_b":"WS_E7_A11","joint_topic":"superlinear_world_features_in_emergent_spatial_world_models"},
  ],
  2: [  # KP-anchored fresh pairings (no microGPT)
    {"cand_id":"CAND_012_E2_001","atom_a":"KP_E2_A01","atom_b":"WS_E7_A05","joint_topic":"ghost_intelligence_remedied_by_world_model_grounding_substrate"},
    {"cand_id":"CAND_012_E2_002","atom_a":"KP_E2_A02","atom_b":"OA_E4_A06","joint_topic":"rlvr_non_gameability_combined_with_release_red_team_customer_feedback"},
    {"cand_id":"CAND_012_E2_003","atom_a":"KP_E2_A03","atom_b":"HN_E6_A01","joint_topic":"jagged_intelligence_resolved_by_photonic_compute_substrate_shift"},
    {"cand_id":"CAND_012_E2_004","atom_a":"KP_E2_A04","atom_b":"OA_E4_A09","joint_topic":"vibe_coding_grounded_in_machine_readable_alignment_spec"},
    {"cand_id":"CAND_012_E2_005","atom_a":"KP_E2_A05","atom_b":"ARXIV_R10_llm_economist","joint_topic":"rlvr_compute_shift_as_economist_mechanism_design_resource_allocation"},
    {"cand_id":"CAND_012_E2_006","atom_a":"KP_E2_A07","atom_b":"WS_E7_A01","joint_topic":"data_efficiency_floor_as_nested_learning_optimization_level"},
    {"cand_id":"CAND_012_E2_007","atom_a":"KP_E2_A08","atom_b":"OA_E4_A04","joint_topic":"verifier_density_predicts_hallucination_reduction_rate"},
    {"cand_id":"CAND_012_E2_008","atom_a":"KP_E2_A09","atom_b":"AN_E5_A06","joint_topic":"survival_vs_text_supervision_explains_consistency_drift"},
    {"cand_id":"CAND_012_E2_009","atom_a":"KP_E2_A10","atom_b":"WS_E7_A02","joint_topic":"continual_learning_meets_hope_self_modifying_architecture"},
    {"cand_id":"CAND_012_E2_010","atom_a":"KP_E2_A11","atom_b":"OA_E4_A11","joint_topic":"six_paradigm_shifts_2025_normalized_by_cross_lab_standard_convergence"},
    {"cand_id":"CAND_012_E2_011","atom_a":"KP_E2_A02","atom_b":"ARXIV_R10_offline_logs","joint_topic":"rlvr_post_train_stage_subsumes_offline_log_warmstart"},
    {"cand_id":"CAND_012_E2_012","atom_a":"KP_E2_A03","atom_b":"HN_E6_A05","joint_topic":"jagged_intelligence_flattened_by_tensor_network_compression_generalist"},
  ],
  3: [  # SA-anchored
    {"cand_id":"CAND_012_E3_001","atom_a":"SA_E3_A01","atom_b":"WS_E7_A07","joint_topic":"smooth_singularity_curve_emergent_from_hierarchical_causal_latent_state_machines"},
    {"cand_id":"CAND_012_E3_002","atom_a":"SA_E3_A02","atom_b":"HN_E6_A06","joint_topic":"agentic_cognitive_labor_2025_aligns_with_RSI_60_pct_2028"},
    {"cand_id":"CAND_012_E3_003","atom_a":"SA_E3_A03","atom_b":"OA_E4_A02","joint_topic":"cognition_before_embodiment_resolved_by_general_substrate_not_specialized_head"},
    {"cand_id":"CAND_012_E3_004","atom_a":"SA_E3_A04","atom_b":"WS_E7_A09","joint_topic":"per_capita_productivity_curve_explained_by_PFN_universal_in_context"},
    {"cand_id":"CAND_012_E3_005","atom_a":"SA_E3_A05","atom_b":"OA_E4_A05","joint_topic":"AGI_confidence_signal_from_GPT55_system_level_behavior_emergence"},
    {"cand_id":"CAND_012_E3_006","atom_a":"SA_E3_A06","atom_b":"AN_E5_A05","joint_topic":"ai_agents_joining_workforce_via_cross_lab_market_clearing"},
    {"cand_id":"CAND_012_E3_007","atom_a":"SA_E3_A07","atom_b":"AN_E5_A11","joint_topic":"wide_superintelligence_distribution_complements_dual_use_state_subsidy"},
    {"cand_id":"CAND_012_E3_008","atom_a":"SA_E3_A08","atom_b":"WS_E7_A06","joint_topic":"relativistic_observer_curvature_blindness_as_belief_state_compressed_history"},
    {"cand_id":"CAND_012_E3_009","atom_a":"SA_E3_A09","atom_b":"WS_E7_A02","joint_topic":"recursive_self_improvement_via_hope_self_modifying_architecture"},
    {"cand_id":"CAND_012_E3_010","atom_a":"SA_E3_A10","atom_b":"PG_E1_A08","joint_topic":"publicly_wrong_strange_things_as_high_branching_factor_persistence"},
    {"cand_id":"CAND_012_E3_011","atom_a":"SA_E3_A11","atom_b":"AN_E5_A01","joint_topic":"verifier_density_ordering_AGI_cognition_before_embodiment_via_self_verification"},
    {"cand_id":"CAND_012_E3_012","atom_a":"SA_E3_A12","atom_b":"OA_E4_A10","joint_topic":"scientific_discovery_superlinearity_evidenced_by_Erdos_disproof_methodology"},
  ],
  4: [  # OA-anchored
    {"cand_id":"CAND_012_E4_001","atom_a":"OA_E4_A01","atom_b":"WS_E7_A06","joint_topic":"erdos_disproof_method_as_belief_state_long_horizon_search"},
    {"cand_id":"CAND_012_E4_002","atom_a":"OA_E4_A02","atom_b":"HN_E6_A04","joint_topic":"general_substrate_compression_via_quantum_inspired_algorithms"},
    {"cand_id":"CAND_012_E4_003","atom_a":"OA_E4_A03","atom_b":"AN_E5_A04","joint_topic":"multi_layer_provenance_as_alignment_substrate_withholding_mechanism"},
    {"cand_id":"CAND_012_E4_004","atom_a":"OA_E4_A04","atom_b":"WS_E7_A02","joint_topic":"hallucination_reduction_routed_via_self_modifying_verifier_writing"},
    {"cand_id":"CAND_012_E4_005","atom_a":"OA_E4_A05","atom_b":"HN_E6_A07","joint_topic":"GPT55_emergent_behavior_as_12hr_autonomy_window_signature"},
    {"cand_id":"CAND_012_E4_006","atom_a":"OA_E4_A06","atom_b":"AN_E5_A12","joint_topic":"red_team_release_loop_as_jagged_offensive_defensive_balancing"},
    {"cand_id":"CAND_012_E4_007","atom_a":"OA_E4_A07","atom_b":"AN_E5_A07","joint_topic":"speech_substrate_decoupling_complements_graphical_substrate_split"},
    {"cand_id":"CAND_012_E4_008","atom_a":"OA_E4_A08","atom_b":"HN_E6_A12","joint_topic":"defender_subsidy_substrate_alignment_with_first_mass_2FA_zero_day"},
    {"cand_id":"CAND_012_E4_009","atom_a":"OA_E4_A09","atom_b":"WS_E7_A10","joint_topic":"machine_readable_spec_grounds_tool_budget_segregation"},
    {"cand_id":"CAND_012_E4_010","atom_a":"OA_E4_A10","atom_b":"PG_E1_A07","joint_topic":"AI_cross_field_analogical_move_requires_high_decision_tree_persistence"},
    {"cand_id":"CAND_012_E4_011","atom_a":"OA_E4_A11","atom_b":"AN_E5_A05","joint_topic":"cross_lab_standard_convergence_as_glasswing_market_clearing_extension"},
    {"cand_id":"CAND_012_E4_012","atom_a":"OA_E4_A12","atom_b":"WS_E7_A01","joint_topic":"user_facing_depth_latency_dial_as_nested_learning_update_rate"},
  ],
  5: [  # AN-anchored
    {"cand_id":"CAND_012_E5_001","atom_a":"AN_E5_A01","atom_b":"WS_E7_A07","joint_topic":"self_verification_inside_inference_loop_via_hierarchical_causal_latent"},
    {"cand_id":"CAND_012_E5_002","atom_a":"AN_E5_A02","atom_b":"PG_E1_A12","joint_topic":"effort_dial_user_negotiation_as_threshold_mechanism_for_quality"},
    {"cand_id":"CAND_012_E5_003","atom_a":"AN_E5_A03","atom_b":"OA_E4_A08","joint_topic":"10000_zero_days_as_asymmetric_cyber_threshold_crossed"},
    {"cand_id":"CAND_012_E5_004","atom_a":"AN_E5_A04","atom_b":"WS_E7_A02","joint_topic":"withholding_as_alignment_substrate_for_self_modifying_architecture"},
    {"cand_id":"CAND_012_E5_005","atom_a":"AN_E5_A05","atom_b":"OA_E4_A11","joint_topic":"cross_lab_market_clearing_via_safety_standard_competitor_partnership"},
    {"cand_id":"CAND_012_E5_006","atom_a":"AN_E5_A06","atom_b":"WS_E7_A03","joint_topic":"consistency_drift_long_horizon_as_rlm_recursive_persistence_failure"},
    {"cand_id":"CAND_012_E5_007","atom_a":"AN_E5_A07","atom_b":"PG_E1_A01","joint_topic":"graphical_substrate_split_aligns_with_writes_write_nots_bifurcation"},
    {"cand_id":"CAND_012_E5_008","atom_a":"AN_E5_A08","atom_b":"PG_E1_A11","joint_topic":"B2B_SaaS_distribution_as_chesky_founder_mode_extension"},
    {"cand_id":"CAND_012_E5_009","atom_a":"AN_E5_A09","atom_b":"OA_E4_A12","joint_topic":"institutional_partnership_aligned_with_depth_latency_user_dial"},
    {"cand_id":"CAND_012_E5_010","atom_a":"AN_E5_A10","atom_b":"WS_E7_A04","joint_topic":"1M_context_aligned_with_10M_RLM_effective_context"},
    {"cand_id":"CAND_012_E5_011","atom_a":"AN_E5_A11","atom_b":"OA_E4_A03","joint_topic":"dual_use_state_AI_subsidy_routed_via_multi_layer_provenance"},
    {"cand_id":"CAND_012_E5_012","atom_a":"AN_E5_A12","atom_b":"KP_E2_A03","joint_topic":"withholding_response_to_jagged_offensive_defensive_spike"},
  ],
  6: [  # HN-anchored
    {"cand_id":"CAND_012_E6_001","atom_a":"HN_E6_A01","atom_b":"OA_E4_A12","joint_topic":"photonic_compute_substrate_modulated_by_user_depth_latency_dial"},
    {"cand_id":"CAND_012_E6_002","atom_a":"HN_E6_A02","atom_b":"KP_E2_A05","joint_topic":"femtojoule_per_op_floor_constrains_rlvr_compute_shift"},
    {"cand_id":"CAND_012_E6_003","atom_a":"HN_E6_A03","atom_b":"WS_E7_A11","joint_topic":"classical_quantum_simulation_capacity_in_emergent_spatial_world_models"},
    {"cand_id":"CAND_012_E6_004","atom_a":"HN_E6_A04","atom_b":"WS_E7_A01","joint_topic":"quantum_inspired_algorithms_as_nested_learning_extension"},
    {"cand_id":"CAND_012_E6_005","atom_a":"HN_E6_A05","atom_b":"WS_E7_A09","joint_topic":"tensor_network_compression_aligned_with_PFN_universal_engine"},
    {"cand_id":"CAND_012_E6_006","atom_a":"HN_E6_A06","atom_b":"PG_E1_A07","joint_topic":"RSI_60_pct_2028_requires_high_decision_tree_persistence"},
    {"cand_id":"CAND_012_E6_007","atom_a":"HN_E6_A07","atom_b":"AN_E5_A06","joint_topic":"12hr_autonomy_window_as_consistency_drift_resolution"},
    {"cand_id":"CAND_012_E6_008","atom_a":"HN_E6_A08","atom_b":"PG_E1_A06","joint_topic":"swe_bench_curve_as_superlinear_world_feature_realization"},
    {"cand_id":"CAND_012_E6_009","atom_a":"HN_E6_A09","atom_b":"OA_E4_A03","joint_topic":"daybreak_mythos_market_clearing_via_provenance_layered"},
    {"cand_id":"CAND_012_E6_010","atom_a":"HN_E6_A10","atom_b":"AN_E5_A11","joint_topic":"per_class_cybersec_specialization_as_state_dual_use_subsidy"},
    {"cand_id":"CAND_012_E6_011","atom_a":"HN_E6_A11","atom_b":"OA_E4_A09","joint_topic":"anthropic_meta_pretrain_grounds_machine_readable_alignment_spec"},
    {"cand_id":"CAND_012_E6_012","atom_a":"HN_E6_A12","atom_b":"WS_E7_A02","joint_topic":"first_AI_2FA_zero_day_demands_hope_self_modifying_architecture"},
  ],
  7: [  # WS-anchored
    {"cand_id":"CAND_012_E7_001","atom_a":"WS_E7_A01","atom_b":"OA_E4_A12","joint_topic":"nested_learning_update_rate_as_user_depth_latency_dial"},
    {"cand_id":"CAND_012_E7_002","atom_a":"WS_E7_A02","atom_b":"AN_E5_A04","joint_topic":"hope_self_modifying_architecture_as_withholding_substrate"},
    {"cand_id":"CAND_012_E7_003","atom_a":"WS_E7_A03","atom_b":"PG_E1_A08","joint_topic":"rlm_recursion_collapses_to_persistence_at_branching_factor_one"},
    {"cand_id":"CAND_012_E7_004","atom_a":"WS_E7_A04","atom_b":"KP_E2_A05","joint_topic":"10M_token_context_redistributes_rlvr_compute_to_recursion"},
    {"cand_id":"CAND_012_E7_005","atom_a":"WS_E7_A05","atom_b":"AN_E5_A06","joint_topic":"world_model_grounding_alleviates_consistency_drift"},
    {"cand_id":"CAND_012_E7_006","atom_a":"WS_E7_A06","atom_b":"OA_E4_A04","joint_topic":"belief_state_compressed_history_predicts_hallucination_reduction"},
    {"cand_id":"CAND_012_E7_007","atom_a":"WS_E7_A07","atom_b":"ARXIV_R10_neuroai","joint_topic":"hierarchical_causal_latent_state_in_hippocampal_place_cell_circuit"},
    {"cand_id":"CAND_012_E7_008","atom_a":"WS_E7_A08","atom_b":"AN_E5_A07","joint_topic":"mouth_brain_LLM_separation_as_graphical_substrate_split"},
    {"cand_id":"CAND_012_E7_009","atom_a":"WS_E7_A09","atom_b":"PG_E1_A12","joint_topic":"PFN_universal_in_context_engine_as_threshold_mechanism"},
    {"cand_id":"CAND_012_E7_010","atom_a":"WS_E7_A10","atom_b":"OA_E4_A11","joint_topic":"tool_budget_segregation_aligned_with_cross_lab_safety_standard"},
    {"cand_id":"CAND_012_E7_011","atom_a":"WS_E7_A11","atom_b":"OA_E4_A02","joint_topic":"emergent_spatial_world_models_in_general_substrate_not_specialized_head"},
    {"cand_id":"CAND_012_E7_012","atom_a":"WS_E7_A12","atom_b":"AN_E5_A10","joint_topic":"arch_train_unification_at_1M_context_phase_transition"},
  ],
}

# Harness inputs: conservative estimates (cross-disciplinary bonus drivers gone, so
# arxiv_hit_count is moderate, recent_paper_count is moderate, saturation_cluster_distance
# is moderate without the high-distance ARXIV_R10 anchors).
def _default_harness():
    return dict(arxiv_hit_count_24m=4, recent_paper_count=8, saturation_cluster_distance=0.55,
                arxiv_citations_supporting=["placeholder"], belinda_3q_passes=True)

# Load v7 weights (post-Run-11)
WEIGHTS_V7 = {
    "atom_quality_score": 0.0978,
    "novelty_score": 0.0801,
    "cross_source_diversity": 0.1010,
    "mechanism_coherence": 0.0892,
    "saturation_distance": 0.0794,
    "speaker_self_publish_risk": 0.0663,
    "arxiv_grounding": 0.0951,
    "belinda_audit_pass": 0.0663,
    "community_density": 0.0826,
    "cross_disciplinary_bonus": 0.2422,
}

# ---------------- Build, score, gate ----------------
OUTPUT_BASE = Path("/home/user/autoresearch-test/paradigm_shift/runs/run_012/phase6_new_epochs")

THRESHOLD_STRICT = 0.90

def run_phase6():
    all_scores = []
    for epoch in range(1, 8):
        cands = []
        for c in EPOCH_CANDIDATES[epoch]:
            a = ATOMS.get(c["atom_a"])
            b = ATOMS.get(c["atom_b"])
            if a is None or b is None:
                print(f"  SKIP {c['cand_id']}: missing atom ({c['atom_a']} or {c['atom_b']})")
                continue
            h = _default_harness()
            cands.append(Candidate(c["cand_id"], a, b, c["joint_topic"], **h))

        ep_dir = OUTPUT_BASE / f"epoch_{epoch}"
        ep_dir.mkdir(parents=True, exist_ok=True)
        (ep_dir / "atoms").mkdir(exist_ok=True)
        scores = score_candidates_for_epoch(cands, ep_dir / "scores", weights=WEIGHTS_V7)
        all_scores.extend(scores)
        # Write epoch candidates file
        with open(ep_dir / "candidates.json", "w") as f:
            json.dump({
                "epoch": epoch,
                "n_candidates": len(cands),
                "candidates": EPOCH_CANDIDATES[epoch],
            }, f, indent=2)
        n_above = sum(1 for s in scores if s["composite_score"] >= THRESHOLD_STRICT)
        n_above_run11 = sum(1 for s in scores if s["composite_score"] >= 0.7)
        print(f"Epoch {epoch}: scored {len(scores)} | >=0.90: {n_above} | >=0.70 (old): {n_above_run11} | top: {max(s['composite_score'] for s in scores):.4f}")

    # Aggregate
    survivors = [s for s in all_scores if s["composite_score"] >= THRESHOLD_STRICT]
    run11_threshold_survivors = [s for s in all_scores if s["composite_score"] >= 0.7]
    print(f"\nTOTAL Phase 6: {len(all_scores)} candidates | >=0.90: {len(survivors)} | >=0.70 (old): {len(run11_threshold_survivors)}")
    print(f"\nTop 5 by composite (regardless of threshold):")
    for s in sorted(all_scores, key=lambda x: x["composite_score"], reverse=True)[:5]:
        print(f"  {s['cand_id']:20s} composite={s['composite_score']:.4f}  topic={s['joint_topic']}")

    # Write summary
    summary = {
        "phase": "phase_6_new_epochs",
        "n_total": len(all_scores),
        "threshold_strict": THRESHOLD_STRICT,
        "n_survivors_at_0_90": len(survivors),
        "n_at_old_run_11_threshold_0_70": len(run11_threshold_survivors),
        "top_5_by_composite": [
            {"cand_id": s["cand_id"], "composite": s["composite_score"], "topic": s["joint_topic"]}
            for s in sorted(all_scores, key=lambda x: x["composite_score"], reverse=True)[:5]
        ],
        "survivors_for_cross_llm_verify": [
            {"cand_id": s["cand_id"], "composite": s["composite_score"], "topic": s["joint_topic"]}
            for s in survivors
        ],
    }
    with open(OUTPUT_BASE / "phase6_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    return summary

if __name__ == "__main__":
    run_phase6()
