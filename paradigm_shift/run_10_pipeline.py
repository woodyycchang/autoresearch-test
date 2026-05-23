"""Run 10 pipeline — persistent knowledge + arXiv injection + recursive multi-epoch.

Counter-method for RC_002 NARROW_INPUT_POOL (Run 9 binding constraint).
arXiv atoms from arxiv_atom_injector.py are merged with transcript atoms,
and the combinator applies a CROSS-SOURCE DIVERSITY BIAS that prefers
candidates containing at least one transcript atom AND at least one arXiv
atom.

Pipeline layers (extending Run 9):
  L0 persistent_knowledge_base load
  L1 transcript_atom load   (Run 7 cached 343 atoms)
  L1b arxiv_atom load        (30 atoms from arxiv_atom_injector)
  L2 atom_quality_v2 + arxiv quality filter
  L3 cross_speaker + cross_source diversity gate
  L3.5 semantic_coherence (TF-IDF subject overlap)
  L4 mechanism_vocab_check
  L5 belinda_3Q audit
  L6 self_publish_v6 (per-speaker; arXiv atoms always pass since paper IS the source)
  L7 community_saturation_check (with arXiv-bias-aware queries)
  L8 cross_source_diversity_score (NEW: rank by transcript+arXiv mix)

The harness (Claude main agent) is responsible for issuing real WebSearch
and Read calls; this module computes deterministic gates and writes state.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Iterable

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))

PERSISTENT_KB_PATH = THIS_DIR / "persistent_knowledge_base.json"
RUN_010_DIR = THIS_DIR / "runs" / "run_010"
ARXIV_ATOMS_PATH = THIS_DIR / "arxiv_atoms" / "arxiv_atoms_run10.json"
RUN_7_ATOMS_DIR = THIS_DIR / "runs" / "run_007" / "atoms_quality_filtered"


# ---------- Speaker map (inherited from Run 9) ----------
TRANSCRIPT_TO_SPEAKER = {
    "T001": "belinda_li",
    "T002": "yu_sun",
    "T003": "nicholas_roberts",
    "T004": "valerie_chen",
    "T005": "amrith_setlur",
    "T007": "karpathy",
    "T008": "silicon_valley",
    "T009": "sam_altman",
    "T010": "hinton",
    "T011": "lecun",
    "T012": "hinton",
    "T013": "karpathy",
    "T014": "naval_ravikant",
}
NON_ACADEMIC_PITCH_TRANSCRIPTS = {"T004", "T008", "T009", "T014"}

# ---------- Self-publish keyword tables (inherited from Run 9 v6) ----------
SPEAKER_SELF_PUBLISH_KEYWORDS_V6 = {
    "belinda_li": ["self-model", "self models", "world model and user model",
                   "coherent and updatable models", "world the user and the self"],
    "yu_sun": ["test-time training", "ttt", "test time training", "rnn that hides", "linear attention test"],
    "hinton": ["forward-forward", "forward forward", "ff algorithm", "outsmart us",
               "mortal computation"],
    "lecun": ["jepa", "joint embedding predictive", "self-supervised learning of",
              "energy-based model"],
    "karpathy": ["software 2.0", "software 3.0", "intro to llms", "andrej karpathy"],
    "nicholas_roberts": ["scaling laws for data", "data-constrained"],
    "amrith_setlur": ["credit assignment for reasoning", "rl finetuning with"],
    "valerie_chen": ["human-ai collaboration design", "interactive ai"],
}

# ---------- Mechanism vocabulary (inherited from Run 9 epoch 2 + Run 10 epoch 4 cross-disc expansion) ----------
MECHANISM_VOCAB = {
    "gradient": ["gradient", "backprop", "gradient descent", "preconditioned gradient",
                 "gradient conflict", "gradient flow", "adaptation"],
    "attention": ["attention", "self-attention", "attention head", "attention score",
                  "cross-attention"],
    "reward": ["reward", "reward function", "reward signal", "reward hacking",
               "verifiable reward", "advantage sign", "incentive"],
    "memory": ["memory", "parametric memory", "external memory", "key-value",
               "retrieval", "kv cache"],
    "routing": ["routing", "router", "expert selection", "moe", "mixture of experts",
                "dirichlet router", "coordination"],
    "embedding": ["embedding", "representation", "latent", "joint embedding",
                  "predictive embedding"],
    "prediction": ["next-token prediction", "next-word prediction", "video prediction",
                   "future prediction", "predictive", "prediction through interaction"],
    "scaling": ["scaling law", "compute-optimal", "chinchilla", "scale",
                "parameter count", "training tokens"],
    "circuit": ["circuit", "feature circuit", "subgraph", "ablation", "causal graph"],
    "specialization": ["specialization", "modular", "expert", "task-specific", "modularity"],
    "alignment": ["alignment", "rlhf", "preference", "reward model"],
    "evaluation": ["benchmark", "evaluation", "human study", "novelty judge"],
    # ===== Cross-disciplinary mechanism axes (Run 10 epoch 4 R-fix for RC_008) =====
    "selection_pressure": ["selection", "adaptation", "biological organization",
                            "evolutionary", "evo-devo", "fitness", "developmental"],
    "energy_constraint": ["energy", "thermodynamic", "sparse event-driven",
                           "energy efficiency", "statistical mechanics", "entropy",
                           "energy-based"],
    "market_clearing": ["market", "market-based", "auction", "mechanism design",
                         "stackelberg", "competition", "coordination", "economic"],
    "body_world_coupling": ["body", "physical world", "interact", "embodied",
                             "co-design of body", "sensorimotor", "robot"],
    "cognitive_function": ["cognitive", "cognition", "brain-inspired", "cognitive neuroscience",
                            "psychology", "synthesis", "neural"],
    "data_efficiency": ["sample efficiency", "data scarcity", "few-shot", "offline",
                         "warm-start", "data-efficient", "low-resource"],
    "system_architecture": ["serving", "scheduling", "inference", "kv cache",
                             "trajectory", "efficiency", "throughput", "latency"],
}


# ---------- Data classes ----------

@dataclass
class Atom:
    atom_id: str
    transcript_id: str
    atom_type: str
    text: str  # verbatim_quote or arXiv snippet
    source: str  # "TRANSCRIPT" or "ARXIV"
    speaker: str = ""
    topic: str = ""
    paper_id: str = ""
    paper_section_ref: str = ""
    line_span: Optional[Tuple[int, int]] = None

    def __post_init__(self):
        if not self.speaker:
            self.speaker = TRANSCRIPT_TO_SPEAKER.get(self.transcript_id, "unknown")


@dataclass
class Candidate:
    candidate_id: str
    atom_a_id: str
    atom_b_id: str
    atom_c_id: Optional[str]
    source_mix: str  # "TT", "TA", "AA", "TTA", "TAA", "AAA", etc.
    speakers: List[str]
    topics: List[str]
    combinator: str
    coherence_score: float = 0.0
    mechanism_overlap: List[str] = field(default_factory=list)
    diversity_score: float = 0.0
    self_publish_flag: bool = False
    saturation_status: str = "UNCHECKED"
    belinda_status: str = "UNCHECKED"


# ---------- L0: persistent KB load ----------

def load_persistent_kb() -> Dict:
    if not PERSISTENT_KB_PATH.exists():
        return {
            "root_causes_identified": [],
            "counter_papers": [],
            "applied_fixes": [],
            "epoch_history": [],
        }
    with PERSISTENT_KB_PATH.open() as fh:
        return json.load(fh)


def append_to_persistent_kb(new_data: Dict) -> None:
    kb = load_persistent_kb()
    for rc in new_data.get("root_causes_identified", []):
        kb["root_causes_identified"].append(rc)
    for cp in new_data.get("counter_papers", []):
        kb["counter_papers"].append(cp)
    for af in new_data.get("applied_fixes", []):
        kb["applied_fixes"].append(af)
    for eh in new_data.get("epoch_history", []):
        kb["epoch_history"].append(eh)
    kb["last_updated_at"] = datetime.now(timezone.utc).isoformat()
    with PERSISTENT_KB_PATH.open("w") as fh:
        json.dump(kb, fh, indent=2)


def known_root_cause_ids(kb: Dict) -> set:
    return {rc["id"] for rc in kb.get("root_causes_identified", [])}


# ---------- L1: load transcript atoms ----------

def load_transcript_atoms() -> List[Atom]:
    atoms: List[Atom] = []
    for path in sorted(RUN_7_ATOMS_DIR.glob("*.json")):
        if path.name.startswith("_"):
            continue  # skip index / metadata files
        with path.open() as fh:
            data = json.load(fh)
        if "atom_id" not in data:
            continue
        ls = data.get("line_span")
        ls_tuple: Optional[Tuple[int, int]] = tuple(ls) if isinstance(ls, list) and len(ls) == 2 else None
        atom = Atom(
            atom_id=data["atom_id"],
            transcript_id=data["transcript_id"],
            atom_type=data["atom_type"],
            text=data["verbatim_quote"],
            source="TRANSCRIPT",
            line_span=ls_tuple,
        )
        atoms.append(atom)
    return atoms


# ---------- L1b: load arXiv atoms ----------

def load_arxiv_atoms() -> List[Atom]:
    if not ARXIV_ATOMS_PATH.exists():
        return []
    with ARXIV_ATOMS_PATH.open() as fh:
        payload = json.load(fh)
    atoms: List[Atom] = []
    for a in payload["atoms"]:
        atom = Atom(
            atom_id=a["atom_id"],
            transcript_id=a["transcript_id"],
            atom_type=a["atom_type"],
            text=a["text"],
            source="ARXIV",
            topic=a["topic"],
            paper_id=a["paper_id"],
            paper_section_ref=a["paper_section_ref"],
            line_span=None,
        )
        atom.speaker = f"ARXIV_{a['paper_id']}"
        atoms.append(atom)
    return atoms


# ---------- L2: atom quality v2 (Run 9 inheritance) ----------

PAST_TENSE_RECOLLECTION_MARKERS = [
    r"\bat the time\b", r"\bback then\b", r"\bI used to\b",
    r"\bwe used to\b", r"\bin the (past|old days)\b",
    r"\bwere seen as\b", r"\bI was\b\s+\w+ing",
]
TRUNCATED_MIDSENTENCE_TAILS = [
    r"\bbetween [a-zA-Z ]+ and\.$",
    r"\b(of|and|or|the|a|an)\s*\.$",
]
VAGUE_META_MARKERS = [
    r"^\s*in this talk\b",
    r"^\s*today I'?ll\b",
    r"^\s*let'?s take a look\b",
]


def passes_quality_v2(atom: Atom) -> Tuple[bool, str]:
    if atom.source == "ARXIV":
        # arXiv atoms come from peer-reviewed abstracts; they bypass past-tense
        # rejection but still get truncation + vague-meta checks.
        for pat in TRUNCATED_MIDSENTENCE_TAILS:
            if re.search(pat, atom.text):
                return False, "TRUNCATED_MIDSENTENCE"
        return True, "OK"
    text = atom.text
    if atom.atom_type == "PREDICTION":
        for pat in PAST_TENSE_RECOLLECTION_MARKERS:
            if re.search(pat, text):
                return False, "PAST_TENSE_RECOLLECTION"
    for pat in TRUNCATED_MIDSENTENCE_TAILS:
        if re.search(pat, text):
            return False, "TRUNCATED_MIDSENTENCE"
    for pat in VAGUE_META_MARKERS:
        if re.search(pat, text):
            return False, "VAGUE_META"
    if len(text.split()) < 6:
        return False, "TOO_SHORT"
    return True, "OK"


# ---------- L3: cross-speaker + cross-source diversity gate ----------

def cross_speaker_ok(atoms: List[Atom]) -> bool:
    speakers = {a.speaker for a in atoms}
    return len(speakers) >= 2


def cross_source_ok(atoms: List[Atom]) -> bool:
    sources = {a.source for a in atoms}
    return len(sources) >= 2  # at least one TRANSCRIPT + one ARXIV


# ---------- L3.5: semantic coherence (TF-IDF Jaccard on tokens) ----------

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "of", "to", "in", "on",
    "for", "with", "and", "or", "but", "as", "by", "at", "from", "that",
    "this", "it", "i", "we", "you", "he", "she", "they", "their", "our",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "so", "if", "then", "than", "also", "very", "just", "now", "here",
    "there", "where", "when", "how", "why", "what", "who", "which",
}


def tokenize(text: str) -> set:
    tokens = re.findall(r"[a-zA-Z]{3,}", text.lower())
    return {t for t in tokens if t not in STOPWORDS}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def coherence_score(atoms: List[Atom]) -> float:
    token_sets = [tokenize(a.text) for a in atoms]
    pairs = []
    for i in range(len(token_sets)):
        for j in range(i + 1, len(token_sets)):
            pairs.append(jaccard(token_sets[i], token_sets[j]))
    if not pairs:
        return 0.0
    return sum(pairs) / len(pairs)


# ---------- L4: mechanism vocabulary check ----------

def mechanism_overlap(atoms: List[Atom]) -> List[str]:
    overlapping = []
    for axis_name, keywords in MECHANISM_VOCAB.items():
        if all(any(kw in atom.text.lower() for kw in keywords) for atom in atoms):
            overlapping.append(axis_name)
    return overlapping


# ---------- L6: self-publish v6 ----------

def is_self_publish(atom: Atom) -> bool:
    if atom.source == "ARXIV":
        return False  # arXiv atoms are the source — no self-publish gate
    speaker = atom.speaker
    if speaker not in SPEAKER_SELF_PUBLISH_KEYWORDS_V6:
        return False
    text_lc = atom.text.lower()
    for kw in SPEAKER_SELF_PUBLISH_KEYWORDS_V6[speaker]:
        if kw in text_lc:
            return True
    return False


# ---------- L8: cross-source diversity score (Run 10 NEW) ----------

def diversity_score(atoms: List[Atom]) -> float:
    """Score combining cross-source + cross-speaker + mechanism overlap.

    Higher = more paradigm-shift-like.
    """
    score = 0.0
    sources = {a.source for a in atoms}
    if "TRANSCRIPT" in sources and "ARXIV" in sources:
        score += 0.5  # cross-source bonus
    speakers = {a.speaker for a in atoms}
    score += 0.1 * (len(speakers) - 1)  # cross-speaker bonus
    mech = mechanism_overlap(atoms)
    score += 0.2 * len(mech)  # mechanism cohesion bonus
    coh = coherence_score(atoms)
    if 0.05 <= coh <= 0.40:
        # sweet spot: too low = unrelated, too high = saying same thing
        score += 0.3
    return score


# ---------- Candidate combination (pair-level, cross-source biased) ----------

def source_mix_label(atoms: List[Atom]) -> str:
    return "".join("T" if a.source == "TRANSCRIPT" else "A" for a in atoms)


def combine_pairs(transcript_atoms: List[Atom], arxiv_atoms: List[Atom]) -> List[Candidate]:
    """Generate pair candidates with cross-source bias.

    Priority order:
    1. transcript × arxiv (TA)  — primary cross-source diversity
    2. arxiv × arxiv (AA)       — secondary, for cross-topic arXiv pairs
    (transcript × transcript pairs SKIPPED — Run 9 exhausted that regime.)
    """
    candidates: List[Candidate] = []
    cand_idx = 0

    # TA pairs
    for ta in transcript_atoms:
        for ax in arxiv_atoms:
            cand_idx += 1
            cid = f"CAND_run_010_{cand_idx:05d}"
            atoms = [ta, ax]
            c = Candidate(
                candidate_id=cid,
                atom_a_id=ta.atom_id,
                atom_b_id=ax.atom_id,
                atom_c_id=None,
                source_mix=source_mix_label(atoms),
                speakers=[a.speaker for a in atoms],
                topics=[a.topic for a in atoms if a.topic],
                combinator="cross_source_pair",
            )
            c.coherence_score = coherence_score(atoms)
            c.mechanism_overlap = mechanism_overlap(atoms)
            c.diversity_score = diversity_score(atoms)
            c.self_publish_flag = any(is_self_publish(a) for a in atoms)
            candidates.append(c)

    # AA pairs (only across different topics + different papers)
    for i in range(len(arxiv_atoms)):
        for j in range(i + 1, len(arxiv_atoms)):
            a1, a2 = arxiv_atoms[i], arxiv_atoms[j]
            if a1.topic == a2.topic:
                continue  # within-topic arXiv pairs are redundant
            if a1.paper_id == a2.paper_id:
                continue
            cand_idx += 1
            cid = f"CAND_run_010_{cand_idx:05d}"
            atoms = [a1, a2]
            c = Candidate(
                candidate_id=cid,
                atom_a_id=a1.atom_id,
                atom_b_id=a2.atom_id,
                atom_c_id=None,
                source_mix=source_mix_label(atoms),
                speakers=[a.speaker for a in atoms],
                topics=[a1.topic, a2.topic],
                combinator="cross_topic_arxiv_pair",
            )
            c.coherence_score = coherence_score(atoms)
            c.mechanism_overlap = mechanism_overlap(atoms)
            c.diversity_score = diversity_score(atoms)
            c.self_publish_flag = False  # arXiv atoms exempt
            candidates.append(c)

    return candidates


# ---------- Layer drops orchestrator ----------

def run_pipeline(epoch: int, out_dir: Path,
                 coherence_min: float = 0.05,
                 coherence_max: float = 0.40,
                 mechanism_min: int = 1,
                 diversity_min: float = 0.6) -> Dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    log: Dict = {"epoch": epoch, "started_at": datetime.now(timezone.utc).isoformat()}

    # L0
    kb = load_persistent_kb()
    log["L0_persistent_kb"] = {
        "known_root_causes": len(kb.get("root_causes_identified", [])),
        "counter_papers": len(kb.get("counter_papers", [])),
        "applied_fixes": len(kb.get("applied_fixes", [])),
        "prior_epochs": len(kb.get("epoch_history", [])),
    }

    # L1
    transcript_atoms = load_transcript_atoms()
    arxiv_atoms = load_arxiv_atoms()
    log["L1_transcript_atoms_raw"] = len(transcript_atoms)
    log["L1b_arxiv_atoms_raw"] = len(arxiv_atoms)

    # L2 atom quality
    t_pass = [a for a in transcript_atoms if passes_quality_v2(a)[0]]
    a_pass = [a for a in arxiv_atoms if passes_quality_v2(a)[0]]
    log["L2_transcript_after_quality"] = len(t_pass)
    log["L2_arxiv_after_quality"] = len(a_pass)
    log["L2_transcript_rejected"] = len(transcript_atoms) - len(t_pass)

    # L3+L3.5 combinatorial
    candidates = combine_pairs(t_pass, a_pass)
    log["L3_raw_candidates"] = len(candidates)

    # Apply gates
    after_speaker = [c for c in candidates if len(set(c.speakers)) >= 2]
    log["L3_cross_speaker"] = len(after_speaker)

    after_coherence = [c for c in after_speaker
                       if coherence_min <= c.coherence_score <= coherence_max]
    log["L3.5_after_coherence"] = len(after_coherence)

    after_mechanism = [c for c in after_coherence if len(c.mechanism_overlap) >= mechanism_min]
    log["L4_after_mechanism_check"] = len(after_mechanism)

    after_self_publish = [c for c in after_mechanism if not c.self_publish_flag]
    log["L6_after_self_publish"] = len(after_self_publish)

    after_diversity = [c for c in after_self_publish if c.diversity_score >= diversity_min]
    log["L8_after_diversity_score"] = len(after_diversity)

    # Sort by diversity desc for top picks
    after_diversity.sort(key=lambda c: -c.diversity_score)

    # Save
    candidates_path = out_dir / "candidates_after_all_layers.json"
    with candidates_path.open("w") as fh:
        json.dump([asdict(c) for c in after_diversity], fh, indent=2)
    log["L8_survivors_path"] = str(candidates_path.relative_to(THIS_DIR))
    log["L8_survivor_count"] = len(after_diversity)
    log["top_survivors"] = [c.candidate_id for c in after_diversity[:10]]
    log["completed_at"] = datetime.now(timezone.utc).isoformat()

    # Save epoch log
    log_path = out_dir / "epoch_log.json"
    with log_path.open("w") as fh:
        json.dump(log, fh, indent=2)

    return log


def main():
    epoch = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    out_dir = RUN_010_DIR / f"epoch_{epoch}"
    log = run_pipeline(epoch=epoch, out_dir=out_dir)
    print(json.dumps(log, indent=2))


if __name__ == "__main__":
    main()
