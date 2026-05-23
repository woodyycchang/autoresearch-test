"""Run 9 epoch 2 — shared-mechanism vocabulary gate (counter ROOT_CAUSE_5).

Reject candidates where the atoms don't share any mechanism keyword.  Inspired by
arXiv:2510.22312 (LacMaterial) — analogies must share a mechanism vocabulary, not just a
surface subject.
"""
from __future__ import annotations

import re

MECHANISM_VOCABULARY = {
    "gradient_descent": ["gradient descent", "gradient", "backpropagation", "back propagation", "sgd"],
    "attention": ["attention", "self-attention", "multi-head", "attention head"],
    "reward_signal": ["reward", "rlhf", "ppo", "dpo", "reward model", "preference"],
    "data_distribution": ["data", "dataset", "distribution", "sample", "corpus"],
    "memory_state": ["memory", "context", "hidden state", "kv cache", "cache"],
    "interpretability": ["circuit", "probe", "interpretability", "feature", "sparse autoencoder", "sae"],
    "scaling": ["scaling", "scale", "scaling law", "parameter", "compute"],
    "evaluation": ["benchmark", "evaluation", "eval", "metric", "accuracy"],
    "verification": ["verify", "verification", "verifier", "proof", "formal"],
    "agent_action": ["agent", "tool", "action", "plan", "execute"],
    "language_structure": ["syntax", "linguistic", "grammar", "semantic", "symbolic"],
    "embedding": ["embedding", "vector", "representation", "latent"],
    "training_loop": ["training", "fine-tune", "pre-train", "epoch", "update"],
    "generative_model": ["generative", "generator", "gan", "diffusion", "vae", "predict next"],
    "self_supervised": ["self-supervised", "ssl", "contrastive", "masked"],
}


def mechanism_tags(text: str) -> set:
    """Extract mechanism-vocabulary tags present in text (case-insensitive)."""
    t = text.lower()
    tags = set()
    for tag, keywords in MECHANISM_VOCABULARY.items():
        for kw in keywords:
            if kw in t:
                tags.add(tag)
                break
    return tags


def shared_mechanism(text_a: str, text_b: str) -> set:
    """Return intersection of mechanism tags between two atoms."""
    return mechanism_tags(text_a) & mechanism_tags(text_b)


def check_pair(atom_a_quote: str, atom_b_quote: str) -> tuple:
    """Return (PASS|FAIL, shared_tags)."""
    shared = shared_mechanism(atom_a_quote, atom_b_quote)
    if shared:
        return "PASS", shared
    return "FAIL", set()
