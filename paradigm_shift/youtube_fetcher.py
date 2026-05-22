"""YouTube transcript fetcher for Paradigm-Shift Finder.

Primary path: youtube-transcript-api on YouTube video IDs.
Fallback path: WebFetch on blog-posted transcripts (handled by the
                orchestrator/agent loop; this module exposes a hook so
                pre-fetched text from any source can be ingested via the
                same canonicalization pipeline).

Output contract:
  - Each fetched transcript is canonicalized (one sentence per line, matching
    tari/inputs/*_canonical.txt format) and written to
    tari/inputs/transcript_NNN_<speaker_slug>_<topic_slug>.txt
  - NNN is the next integer after the highest existing transcript_NNN_.
  - Raw (pre-canonical) transcript is also written as
    tari/inputs/transcript_NNN_<speaker_slug>_<topic_slug>_raw.txt
  - tari/inputs/manifest.json is updated/created with the new entry.
  - paradigm_shift/fetch_log.json records every attempt (success+reason).

Honest acknowledgments:
  - youtube-transcript-api returns 403 from datacenter / sandbox IPs because
    YouTube blocks transcript scraping from non-residential IPs. The fetcher
    surfaces this as a structured failure reason in fetch_log.json rather
    than crashing.
  - Auto-captions contain filler ("uh", "um", "[Music]", etc). The cleaner
    in this module removes the obvious filler but cannot fix transcription
    errors at the word level.
  - The fetcher NEVER overwrites an existing transcript_NNN file. The
    sequence is monotonically increasing across runs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse


# ---- Video ID extraction ----

YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com",
                 "music.youtube.com", "youtu.be"}


def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from a URL."""
    if not url:
        return None
    try:
        parsed = urlparse(url)
    except Exception:
        return None
    host = (parsed.hostname or "").lower()
    if host not in YOUTUBE_HOSTS:
        return None
    if host == "youtu.be":
        # https://youtu.be/<id>
        return (parsed.path or "/").lstrip("/").split("/")[0] or None
    # /watch?v=<id>
    if parsed.path == "/watch":
        qs = parse_qs(parsed.query)
        v = qs.get("v", [None])[0]
        return v
    # /embed/<id> or /v/<id> or /shorts/<id>
    m = re.match(r"^/(?:embed|v|shorts)/([A-Za-z0-9_\-]{6,})", parsed.path or "")
    if m:
        return m.group(1)
    return None


# ---- Filler / noise cleaning ----

FILLER_PATTERNS = [
    re.compile(r"\[(?:music|applause|laughter|inaudible|noise|crosstalk|silence)\]", re.IGNORECASE),
    re.compile(r"\((?:music|applause|laughter|inaudible|noise|crosstalk|silence)\)", re.IGNORECASE),
    re.compile(r"\b(?:uh|um|uhh|umm|er|erm|hmm|mm)\b[,.\s]*", re.IGNORECASE),
    re.compile(r"\s+"),  # collapse runs of whitespace (applied last)
]


def clean_text(text: str) -> str:
    """Remove filler tokens and bracketed audio cues, collapse whitespace."""
    s = text
    # Remove bracketed audio cues
    s = FILLER_PATTERNS[0].sub("", s)
    s = FILLER_PATTERNS[1].sub("", s)
    # Remove filler words
    s = FILLER_PATTERNS[2].sub("", s)
    # Collapse whitespace
    s = FILLER_PATTERNS[3].sub(" ", s).strip()
    return s


# ---- Canonical line-wrapping (sentence-per-line, matching existing transcripts) ----

SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def canonicalize(raw_text: str) -> str:
    """Wrap text to one sentence per line to match existing canonical format.

    Existing canonical transcripts (e.g. belinda_li_self_models_canonical.txt)
    use sentence-per-line. We follow that pattern rather than fixed-width wrap
    so the downstream TARI snippet decomposer and line-number provenance work
    identically.
    """
    sentences = SENTENCE_END.split(raw_text)
    lines = [s.strip() for s in sentences if s.strip()]
    return "\n".join(lines) + "\n"


# ---- Filename slug ----

def slugify(s: str, max_len: int = 30) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    if len(s) > max_len:
        s = s[:max_len].rstrip("_")
    return s


# ---- Next transcript number ----

TRANSCRIPT_NUMBER_RE = re.compile(r"^(?:transcript_(\d{3})|INPUT_TRANSCRIPT_(\d{3}))")


def next_transcript_number(inputs_dir: Path) -> int:
    """Find the highest existing transcript_NNN and return NNN+1.

    Looks at filenames matching transcript_NNN_*.txt or INPUT_TRANSCRIPT_NNN_*
    (the legacy provenance filename for T001). The earliest transcript
    (belinda_li_self_models.txt) is T001 and is not auto-numbered, so we count
    it explicitly: any belinda_li_* file in inputs_dir is treated as occupying
    001 if no transcript_001_* exists.
    """
    used: List[int] = []
    has_belinda = False
    for f in inputs_dir.iterdir():
        if not f.is_file():
            continue
        name = f.name
        m = TRANSCRIPT_NUMBER_RE.match(name)
        if m:
            n_str = m.group(1) or m.group(2)
            if n_str:
                used.append(int(n_str))
        if name.startswith("belinda_li_"):
            has_belinda = True
    if has_belinda and 1 not in used:
        used.append(1)
    if not used:
        return 1
    return max(used) + 1


# ---- Manifest update ----

def load_or_init_manifest(manifest_path: Path) -> dict:
    if manifest_path.exists():
        with manifest_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "manifest_version": "v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "transcripts": [],
    }


def upsert_manifest_entry(manifest: dict, entry: dict):
    """Insert if transcript_id not present; otherwise replace."""
    tid = entry["id"]
    for i, e in enumerate(manifest.get("transcripts", [])):
        if e.get("id") == tid:
            manifest["transcripts"][i] = entry
            return
    manifest.setdefault("transcripts", []).append(entry)


# ---- Cutoff classification ----

CLAUDE_CUTOFF = datetime(2026, 1, 1, tzinfo=timezone.utc)


def classify_vs_cutoff(upload_date_iso: Optional[str]) -> str:
    if not upload_date_iso:
        return "unknown_upload_date"
    try:
        d = datetime.fromisoformat(upload_date_iso.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return "unparseable_upload_date"
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    if d < CLAUDE_CUTOFF:
        return "pre_cutoff"
    return "post_cutoff"


# ---- Primary fetch path: youtube-transcript-api ----

@dataclass
class FetchResult:
    url: str
    video_id: Optional[str]
    success: bool
    transcript_id: Optional[str]
    output_path: Optional[str]
    raw_output_path: Optional[str]
    n_chars_raw: int
    n_chars_canonical: int
    n_lines_canonical: int
    fetch_method: str          # "youtube_transcript_api" | "manual_text" | "skipped"
    failure_reason: Optional[str]
    fetched_at: str


def fetch_youtube_via_api(video_id: str, languages: Tuple[str, ...] = ("en",)) -> Tuple[bool, str, str]:
    """Try fetching the transcript via youtube-transcript-api.

    Returns (success, raw_text, failure_reason). raw_text is "" on failure.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
    except ImportError as e:
        return (False, "", f"youtube_transcript_api_not_installed: {e}")

    api = YouTubeTranscriptApi()
    try:
        r = api.fetch(video_id, languages=languages)
    except Exception as e:
        # Common failure modes (datacenter IP block, no captions, etc.) come
        # through as YouTubeRequestFailed / TranscriptsDisabled / etc.
        reason = f"{type(e).__name__}: {str(e)[:240].replace(chr(10), ' ')}"
        return (False, "", reason)

    snippets = getattr(r, "snippets", None)
    if not snippets:
        return (False, "", "no_snippets_returned")
    parts: List[str] = []
    for s in snippets:
        t = getattr(s, "text", "") or ""
        if t:
            parts.append(t)
    raw_text = " ".join(parts)
    return (True, raw_text, "")


# ---- Fetch driver ----

def fetch_one(
    url: str,
    speaker: str,
    title: str,
    upload_date: Optional[str] = None,
    why_chosen: str = "",
    expected_paradigm_atoms: List[str] = None,
    inputs_dir: Path = Path("tari/inputs"),
    manifest_path: Path = Path("tari/inputs/manifest.json"),
    fallback_text: Optional[str] = None,
    dry_run: bool = False,
) -> FetchResult:
    """Fetch one transcript and write canonical+raw files. Update manifest.

    fallback_text: if provided, use this text instead of attempting YouTube
                   fetch (useful when an external agent has pre-fetched the
                   content via WebFetch from a transcript blog).
    """
    fetched_at = datetime.now(timezone.utc).isoformat()
    expected_paradigm_atoms = expected_paradigm_atoms or []

    vid = extract_video_id(url)

    if fallback_text:
        success, raw_text, reason = (True, fallback_text, "")
        method = "manual_text"
    else:
        if not vid:
            return FetchResult(
                url=url, video_id=None, success=False, transcript_id=None,
                output_path=None, raw_output_path=None,
                n_chars_raw=0, n_chars_canonical=0, n_lines_canonical=0,
                fetch_method="skipped",
                failure_reason="could_not_extract_video_id",
                fetched_at=fetched_at,
            )
        success, raw_text, reason = fetch_youtube_via_api(vid)
        method = "youtube_transcript_api"

    if not success:
        return FetchResult(
            url=url, video_id=vid, success=False, transcript_id=None,
            output_path=None, raw_output_path=None,
            n_chars_raw=0, n_chars_canonical=0, n_lines_canonical=0,
            fetch_method=method,
            failure_reason=reason,
            fetched_at=fetched_at,
        )

    # Clean filler from raw
    cleaned = clean_text(raw_text)
    if len(cleaned) < 200:
        return FetchResult(
            url=url, video_id=vid, success=False, transcript_id=None,
            output_path=None, raw_output_path=None,
            n_chars_raw=len(raw_text), n_chars_canonical=0, n_lines_canonical=0,
            fetch_method=method,
            failure_reason=f"cleaned_text_too_short ({len(cleaned)} chars)",
            fetched_at=fetched_at,
        )

    # Canonicalize
    canonical = canonicalize(cleaned)
    n_lines = canonical.count("\n")

    # Allocate filename
    inputs_dir.mkdir(parents=True, exist_ok=True)
    nnn = next_transcript_number(inputs_dir)
    speaker_slug = slugify(speaker, max_len=20)
    topic_slug = slugify(title, max_len=30)
    base = f"transcript_{nnn:03d}_{speaker_slug}_{topic_slug}"
    canonical_path = inputs_dir / f"{base}_canonical.txt"
    raw_path = inputs_dir / f"{base}_raw.txt"
    tid = f"T{nnn:03d}"

    if canonical_path.exists() or raw_path.exists():
        # Safety: NEVER overwrite. Surface as failure.
        return FetchResult(
            url=url, video_id=vid, success=False, transcript_id=None,
            output_path=None, raw_output_path=None,
            n_chars_raw=len(raw_text), n_chars_canonical=len(canonical),
            n_lines_canonical=n_lines,
            fetch_method=method,
            failure_reason=f"refused_to_overwrite_existing: {canonical_path.name} or {raw_path.name}",
            fetched_at=fetched_at,
        )

    if not dry_run:
        canonical_path.write_text(canonical, encoding="utf-8")
        raw_path.write_text(raw_text, encoding="utf-8")

        # Update manifest
        manifest = load_or_init_manifest(manifest_path)
        entry = {
            "id": tid,
            "path": str(canonical_path),
            "raw_path": str(raw_path),
            "speaker": speaker,
            "title": title,
            "youtube_url": url if vid else None,
            "video_id": vid,
            "upload_date": upload_date,
            "fetched_at": fetched_at,
            "claude_cutoff_relationship": classify_vs_cutoff(upload_date),
            "fetch_method": method,
            "why_chosen": why_chosen,
            "expected_paradigm_atoms": expected_paradigm_atoms,
            "n_chars_canonical": len(canonical),
            "n_lines_canonical": n_lines,
        }
        upsert_manifest_entry(manifest, entry)
        manifest["updated_at"] = fetched_at
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with manifest_path.open("w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

    return FetchResult(
        url=url, video_id=vid, success=True, transcript_id=tid,
        output_path=str(canonical_path), raw_output_path=str(raw_path),
        n_chars_raw=len(raw_text), n_chars_canonical=len(canonical),
        n_lines_canonical=n_lines,
        fetch_method=method,
        failure_reason=None,
        fetched_at=fetched_at,
    )


def fetch_all(
    seed_path: Path,
    inputs_dir: Path = Path("tari/inputs"),
    manifest_path: Path = Path("tari/inputs/manifest.json"),
    fetch_log_path: Path = Path("paradigm_shift/fetch_log.json"),
    fallback_text_map: Optional[Dict[str, str]] = None,
) -> List[FetchResult]:
    """Iterate over the seed URL list and fetch each.

    seed_path JSON schema:
        [
          {"url": "...", "speaker": "...", "title": "...",
           "upload_date": "YYYY-MM-DD",
           "why_chosen": "...", "expected_paradigm_atoms": ["prediction", ...]},
          ...
        ]

    fallback_text_map: {url: pre_fetched_text}. If a URL is in this map, it
                      bypasses youtube-transcript-api and uses the supplied
                      text directly (filler cleaning + canonicalization still
                      apply).
    """
    with seed_path.open("r", encoding="utf-8") as f:
        seeds = json.load(f)

    fallback_text_map = fallback_text_map or {}
    results: List[FetchResult] = []
    for s in seeds:
        url = s["url"]
        fb = fallback_text_map.get(url)
        r = fetch_one(
            url=url,
            speaker=s.get("speaker", "unknown"),
            title=s.get("title", "untitled"),
            upload_date=s.get("upload_date"),
            why_chosen=s.get("why_chosen", ""),
            expected_paradigm_atoms=s.get("expected_paradigm_atoms", []),
            inputs_dir=inputs_dir,
            manifest_path=manifest_path,
            fallback_text=fb,
        )
        results.append(r)

    # Write fetch log
    fetch_log_path.parent.mkdir(parents=True, exist_ok=True)
    n_success = sum(1 for r in results if r.success)
    n_fail = sum(1 for r in results if not r.success)
    log = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "seed_path": str(seed_path),
        "n_attempted": len(results),
        "n_success": n_success,
        "n_fail": n_fail,
        "failure_reason_distribution": _bucket_failures(results),
        "results": [asdict(r) for r in results],
    }
    # Append to existing log if present
    if fetch_log_path.exists():
        with fetch_log_path.open("r", encoding="utf-8") as f:
            prior = json.load(f)
        if "history" not in prior:
            prior = {"history": [prior]}
        prior["history"].append(log)
        prior["last_run"] = log
        with fetch_log_path.open("w", encoding="utf-8") as f:
            json.dump(prior, f, indent=2, ensure_ascii=False)
    else:
        with fetch_log_path.open("w", encoding="utf-8") as f:
            json.dump({"history": [log], "last_run": log}, f, indent=2, ensure_ascii=False)

    return results


def _bucket_failures(results: List[FetchResult]) -> Dict[str, int]:
    buckets: Dict[str, int] = {}
    for r in results:
        if r.success:
            continue
        # Categorize: take prefix before colon
        reason = r.failure_reason or "unknown"
        bucket = reason.split(":", 1)[0].split(" ", 1)[0]
        buckets[bucket] = buckets.get(bucket, 0) + 1
    return buckets


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_fetch = sub.add_parser("fetch")
    p_fetch.add_argument("--seed_path", required=True, type=Path)
    p_fetch.add_argument("--inputs_dir", type=Path, default=Path("tari/inputs"))
    p_fetch.add_argument("--manifest_path", type=Path,
                          default=Path("tari/inputs/manifest.json"))
    p_fetch.add_argument("--fetch_log_path", type=Path,
                          default=Path("paradigm_shift/fetch_log.json"))
    p_fetch.add_argument("--fallback_text_map_path", type=Path, default=None,
                          help="JSON {url: pre_fetched_text} for URLs where "
                               "youtube_transcript_api fails (sandbox/IP block)")

    p_test = sub.add_parser("test_one")
    p_test.add_argument("--url", required=True)
    p_test.add_argument("--speaker", required=True)
    p_test.add_argument("--title", required=True)

    args = ap.parse_args()
    if args.cmd == "fetch":
        fb_map = None
        if args.fallback_text_map_path and args.fallback_text_map_path.exists():
            with args.fallback_text_map_path.open("r", encoding="utf-8") as f:
                fb_map = json.load(f)
        results = fetch_all(
            seed_path=args.seed_path,
            inputs_dir=args.inputs_dir,
            manifest_path=args.manifest_path,
            fetch_log_path=args.fetch_log_path,
            fallback_text_map=fb_map,
        )
        n_ok = sum(1 for r in results if r.success)
        n_fail = len(results) - n_ok
        print(f"fetched {n_ok}/{len(results)} successfully ({n_fail} failed)")
        for r in results:
            if r.success:
                print(f"  OK   {r.transcript_id}  {Path(r.output_path).name}")
            else:
                print(f"  FAIL {r.url}: {r.failure_reason[:100]}")
    elif args.cmd == "test_one":
        r = fetch_one(url=args.url, speaker=args.speaker, title=args.title,
                      dry_run=True)
        print(json.dumps(asdict(r), indent=2))


if __name__ == "__main__":
    main()
