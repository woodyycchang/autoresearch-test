"""arXiv citation gate for Paradigm-Shift Finder Run 6.

A sub-claim is only considered GROUNDED if at least one of its supporting
search results points to an arxiv.org URL with a parseable identifier
(``arxiv.org/abs/XXXX.XXXXX``, ``arxiv.org/pdf/XXXX.XXXXX[v#]``, or
``arxiv.org/html/XXXX.XXXXX[v#]``). Blog posts, news, vendor pages, and
Wikipedia citations are rejected — they pass the original keyword-
overlap heuristic but provide no peer-review-style anchoring.

Rationale: Run 5 found that many "grounded" sub-claims were grounded
on marketing copy or Substack speculation. arXiv (or equivalent
peer-reviewed venue) is the cheapest available proxy for "someone
outside Claude's training corpus has stated this in a citable form".

The gate has two outputs per sub-claim:

  - ``arxiv_id``: parsed identifier or None
  - ``status``: ``"arXiv:<id>"`` on success, ``"NO_ARXIV_REJECT"`` otherwise
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

ARXIV_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})(?:v\d+)?",
    re.IGNORECASE,
)


def parse_arxiv_id(url: str) -> Optional[str]:
    if not url:
        return None
    m = ARXIV_RE.search(url)
    return m.group(1) if m else None


def gate_sub_claim(sub_claim: str, supporting_results: List[dict]) -> Tuple[str, Optional[str]]:
    """Return (status_string, arxiv_id_or_none).

    status_string is either ``"arXiv:<id>"`` or ``"NO_ARXIV_REJECT"``.
    """
    for r in supporting_results:
        aid = parse_arxiv_id(r.get("url", ""))
        if aid:
            return (f"arXiv:{aid}", aid)
    return ("NO_ARXIV_REJECT", None)


def gate_and_report(records: List[dict]) -> List[dict]:
    """records: [{"sub_claim": str, "supporting_results": [{url,title,snippet}, ...]}]

    Returns the same list with two new keys per record: ``arxiv_id`` and
    ``status``. Also returns counts of accepted / rejected.
    """
    accepted = rejected = 0
    out = []
    for rec in records:
        status, aid = gate_sub_claim(rec["sub_claim"], rec.get("supporting_results", []))
        rec = dict(rec)
        rec["status"] = status
        rec["arxiv_id"] = aid
        if status.startswith("arXiv:"):
            accepted += 1
        else:
            rejected += 1
        out.append(rec)
    return out, {"accepted": accepted, "rejected": rejected, "total": len(records)}
