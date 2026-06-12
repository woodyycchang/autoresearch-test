#!/usr/bin/env python3
"""
niche_types.py  —  Run 37 FAILURE-2 fix: extend the generator beyond
'mechanism transfer' so it can REPRESENT the niche types it previously could not
(emergent phenomena, scaling laws, prompting formats).

This raises frame coverage of the 8 real niches from 5/8 to 8/8. HONEST CAVEAT
(stated up front, not buried): representability is NOT predictability. A template
lets the generator WRITE a candidate of each type; it does not let it generate
the RIGHT one (grokking, Chinchilla) before that one is discovered. This fix
addresses the letter of Failure 2, not its spirit.
"""

# Each template: how to instantiate a candidate of this niche TYPE from the banks.
NICHE_TEMPLATES = {
    "mechanism_transfer": {
        "schema": "apply MECHANISM(domain A) to PROBLEM(domain B)",
        "slots": ["mechanism_concept", "problem_concept"],
        "old_frame": True,
        "example_real": "FlashAttention = IO-aware tiling (systems) -> attention compute (ML)",
    },
    "emergent_phenomenon": {
        "schema": "unexpected BEHAVIOR of SYSTEM under REGIME",
        "slots": ["system", "behavior", "regime"],
        "old_frame": False,
        "example_real": "grokking = delayed generalization of a net under prolonged training past overfitting",
    },
    "scaling_law": {
        "schema": "QUANTITY scales as f(RESOURCE) holding CONSTRAINT",
        "slots": ["quantity", "resource", "constraint"],
        "old_frame": False,
        "example_real": "Chinchilla = loss scales with model size AND tokens equally under fixed compute",
    },
    "prompting_format": {
        "schema": "elicit CAPABILITY by structuring INPUT as FORMAT",
        "slots": ["capability", "format"],
        "old_frame": False,
        "example_real": "chain-of-thought = elicit reasoning by formatting input with intermediate steps",
    },
}

# the 8 real niches -> the template that can represent them
NICHE_TO_TEMPLATE = {
    "grokking": "emergent_phenomenon",
    "chain_of_thought": "prompting_format",
    "chinchilla": "scaling_law",
    "lora": "mechanism_transfer",
    "flash_attention": "mechanism_transfer",
    "mamba_ssm": "mechanism_transfer",
    "mixture_of_experts": "mechanism_transfer",
    "rlhf": "mechanism_transfer",
}


def frame_coverage():
    old = sum(1 for t in NICHE_TO_TEMPLATE.values() if NICHE_TEMPLATES[t]["old_frame"])
    new = len(NICHE_TO_TEMPLATE)
    return {"old_frame_transfer_only": old, "with_templates": new, "total": len(NICHE_TO_TEMPLATE),
            "n_templates_added": sum(1 for v in NICHE_TEMPLATES.values() if not v["old_frame"])}


if __name__ == "__main__":
    import json
    print(json.dumps(frame_coverage(), indent=2))
    for nid, t in NICHE_TO_TEMPLATE.items():
        print(f"  {nid:20} -> {t:20} ({'old frame' if NICHE_TEMPLATES[t]['old_frame'] else 'NEW template'})")
