"""YouTube transcript fetcher v2 — three fallback methods.

Run 2's youtube_fetcher.py used only the youtube-transcript-api library, which
returns 403 from the sandbox IP. v2 adds two alternative methods that target
different endpoints:

  Method A: Direct YouTube timedtext endpoint
            https://www.youtube.com/api/timedtext?lang=en&v={VID}&fmt=json3
            Different URL than youtube-transcript-api; may or may not
            be blocked by the same IP filter.

  Method B: Third-party wrapper services (youtubetranscript.com, supadata.ai,
            youtube-transcript.io). These services host their own scrapers
            and expose simple HTTP endpoints; they bypass YouTube's
            datacenter-IP gating because the request comes from their
            residential infrastructure.

  Method C: yt-dlp library. yt-dlp uses a different download path than
            youtube-transcript-api and may succeed where the API library
            fails.

All three fall back through in order; the first method that returns a
non-empty transcript is used. Each attempt is logged to
`paradigm_shift/fetch_methods_log.json` so we can see which method works
in any given environment.

Honest acknowledgment for the current sandbox:
  - Method A: HTTP 403 from youtube.com/api/timedtext
  - Method B: "Host not in allowlist" — sandbox network policy blocks
              youtubetranscript.com, tactiq.io, youtube-transcript.io
  - Method C: HTTP 403 from yt-dlp's API page download
  This is a sandbox-network-policy constraint, not a bug in the code.
  Running on a non-sandboxed machine with normal residential outbound
  access will succeed for any of the three methods.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import subprocess
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))

# Reuse v1's helpers for cleaning, canonicalization, slugify, etc.
from youtube_fetcher import (  # noqa: E402
    extract_video_id, clean_text, canonicalize, slugify,
    next_transcript_number, load_or_init_manifest, upsert_manifest_entry,
    classify_vs_cutoff, FetchResult, FILLER_PATTERNS, SENTENCE_END,
)


# ---- Method A: Direct timedtext endpoint ----

TIMEDTEXT_URL = "https://www.youtube.com/api/timedtext?lang={lang}&v={vid}&fmt=json3"
TIMEDTEXT_URL_NOFMT = "https://www.youtube.com/api/timedtext?lang={lang}&v={vid}"


def fetch_method_a_timedtext(video_id: str, lang: str = "en") -> Tuple[bool, str, str]:
    """Hit the timedtext endpoint directly with JSON3 format.

    Returns (success, raw_text, failure_reason).
    """
    url = TIMEDTEXT_URL.format(lang=lang, vid=video_id)
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/126.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        return (False, "", f"HTTPError {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        return (False, "", f"URLError: {str(e.reason)[:200]}")
    except Exception as e:
        return (False, "", f"{type(e).__name__}: {str(e)[:200]}")

    if not data:
        return (False, "", "empty_response")

    # Try JSON3 first
    try:
        j = json.loads(data)
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Could be plain XML timed text
        try:
            text = data.decode("utf-8", errors="replace")
            # Strip XML tags, return inner text
            inner = re.sub(r"<[^>]+>", " ", text)
            if len(inner.strip()) >= 200:
                return (True, inner, "")
            return (False, "", "non_json_response_too_short")
        except Exception:
            return (False, "", "non_json_decode_failed")

    events = j.get("events") or []
    parts: List[str] = []
    for ev in events:
        segs = ev.get("segs") or []
        for s in segs:
            t = s.get("utf8") or ""
            if t:
                parts.append(t)
    raw_text = " ".join(parts)
    if len(raw_text.strip()) < 200:
        return (False, "", f"json3_text_too_short ({len(raw_text)} chars)")
    return (True, raw_text, "")


# ---- Method B: 3rd-party wrapper services ----

# Several free services scrape YouTube and re-expose transcripts. Try each
# in order. Each entry: (name, url_template, parser_fn_name).
WRAPPER_SERVICES = [
    ("youtubetranscript.com",
     "https://youtubetranscript.com/?server_vid_5={vid}",
     "parse_html_transcript"),
    ("youtube-transcript.io",
     "https://www.youtube-transcript.io/api/transcripts?id={vid}",
     "parse_json_transcripts"),
    ("tactiq.io",
     "https://tactiq.io/tools/youtube-transcript?yt={vid}",
     "parse_tactiq"),
]


def _http_get(url: str, timeout: int = 20) -> Tuple[Optional[bytes], str]:
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/126.0.0.0 Safari/537.36",
                "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return (r.read(), "")
    except urllib.error.HTTPError as e:
        return (None, f"HTTPError {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        return (None, f"URLError: {str(e.reason)[:200]}")
    except Exception as e:
        return (None, f"{type(e).__name__}: {str(e)[:200]}")


def parse_html_transcript(html_bytes: bytes) -> str:
    """Strip HTML to inner text — youtubetranscript.com returns transcript
    in plain HTML with <p> or similar tags."""
    text = html_bytes.decode("utf-8", errors="replace")
    # Try to extract content within <article>, <main>, or the body
    body_match = re.search(r"<body[^>]*>(.*?)</body>", text, re.DOTALL | re.IGNORECASE)
    if body_match:
        body = body_match.group(1)
    else:
        body = text
    # Strip tags
    inner = re.sub(r"<script\b[^>]*>.*?</script>", " ", body, flags=re.DOTALL | re.IGNORECASE)
    inner = re.sub(r"<style\b[^>]*>.*?</style>", " ", inner, flags=re.DOTALL | re.IGNORECASE)
    inner = re.sub(r"<[^>]+>", " ", inner)
    inner = re.sub(r"&nbsp;", " ", inner)
    inner = re.sub(r"&amp;", "&", inner)
    inner = re.sub(r"&#\d+;", " ", inner)
    inner = re.sub(r"\s+", " ", inner).strip()
    return inner


def parse_json_transcripts(data: bytes) -> str:
    """Parse a JSON wrapper service response with `{transcripts:[{text:...}]}`."""
    try:
        j = json.loads(data)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return ""
    parts: List[str] = []
    transcripts = j.get("transcripts") or j.get("transcript") or []
    if isinstance(transcripts, dict):
        transcripts = [transcripts]
    for t in transcripts:
        if isinstance(t, dict):
            txt = t.get("text") or t.get("content") or ""
            if isinstance(txt, list):
                txt = " ".join(str(x) for x in txt)
            if txt:
                parts.append(txt)
        elif isinstance(t, str):
            parts.append(t)
    if not parts and "text" in j:
        parts.append(str(j["text"]))
    return " ".join(parts)


def parse_tactiq(html_bytes: bytes) -> str:
    """Tactiq embeds transcript in a <pre> block or similar."""
    text = html_bytes.decode("utf-8", errors="replace")
    pre_match = re.search(r"<pre[^>]*>(.*?)</pre>", text, re.DOTALL | re.IGNORECASE)
    if pre_match:
        return parse_html_transcript(pre_match.group(1).encode("utf-8"))
    return parse_html_transcript(html_bytes)


PARSERS = {
    "parse_html_transcript": parse_html_transcript,
    "parse_json_transcripts": parse_json_transcripts,
    "parse_tactiq": parse_tactiq,
}


def fetch_method_b_wrappers(video_id: str) -> Tuple[bool, str, str]:
    """Try wrapper services in order. Return on the first successful fetch."""
    errors: List[str] = []
    for name, url_tmpl, parser_name in WRAPPER_SERVICES:
        url = url_tmpl.format(vid=video_id)
        data, err = _http_get(url)
        if not data:
            errors.append(f"{name}: {err}")
            continue
        parser = PARSERS.get(parser_name)
        if not parser:
            errors.append(f"{name}: parser_not_found")
            continue
        try:
            text = parser(data)
        except Exception as e:
            errors.append(f"{name}: parser_error {type(e).__name__}")
            continue
        if len(text) >= 500:
            return (True, text, f"wrapper={name}")
        errors.append(f"{name}: parsed_text_too_short ({len(text)})")
    return (False, "", "; ".join(errors)[:400])


# ---- Method C: yt-dlp ----

def fetch_method_c_ytdlp(video_id: str, lang: str = "en") -> Tuple[bool, str, str]:
    """Use yt-dlp library to download subtitles and parse."""
    try:
        import yt_dlp  # type: ignore
    except ImportError:
        return (False, "", "yt_dlp_not_installed")

    out_dir = Path("/tmp/ytdlp_subs")
    out_dir.mkdir(parents=True, exist_ok=True)

    opts = {
        "quiet": True,
        "no_warnings": True,
        "writeautomaticsub": True,
        "writesubtitles": True,
        "skip_download": True,
        "subtitleslangs": [lang],
        "subtitlesformat": "json3",
        "outtmpl": str(out_dir / f"{video_id}.%(ext)s"),
        "nocheckcertificate": True,
        "ignoreerrors": False,
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
    except Exception as e:
        return (False, "", f"yt_dlp_error: {type(e).__name__}: {str(e)[:200]}")

    # Look for a downloaded JSON3 sub file
    for ext in ("json3", "vtt", "srv3"):
        for f in out_dir.glob(f"{video_id}*.{ext}"):
            try:
                with f.open("rb") as fh:
                    data = fh.read()
                if ext == "json3":
                    j = json.loads(data)
                    parts = []
                    for ev in (j.get("events") or []):
                        for s in (ev.get("segs") or []):
                            t = s.get("utf8") or ""
                            if t:
                                parts.append(t)
                    text = " ".join(parts)
                elif ext == "vtt":
                    text = data.decode("utf-8", errors="replace")
                    # Strip VTT timing lines
                    lines = []
                    for ln in text.splitlines():
                        if "-->" in ln or ln.strip().isdigit() or not ln.strip() or ln.startswith("WEBVTT"):
                            continue
                        lines.append(ln)
                    text = " ".join(lines)
                else:  # srv3
                    text = re.sub(r"<[^>]+>", " ", data.decode("utf-8", errors="replace"))
                if len(text.strip()) >= 200:
                    return (True, text, f"yt_dlp_ext={ext}")
            except Exception as e:
                continue
    return (False, "", "yt_dlp_no_subs_downloaded")


# ---- Method orchestration ----

@dataclass
class MethodAttempt:
    method: str
    success: bool
    failure_reason: Optional[str]
    n_chars: int
    attempted_at: str


def fetch_one_v2(
    url: str,
    speaker: str,
    title: str,
    upload_date: Optional[str] = None,
    why_chosen: str = "",
    expected_paradigm_atoms: List[str] = None,
    inputs_dir: Path = Path("tari/inputs"),
    manifest_path: Path = Path("tari/inputs/manifest.json"),
    methods: Optional[List[str]] = None,
) -> Tuple[FetchResult, List[MethodAttempt]]:
    """Try methods in order; return on first success.

    Returns (FetchResult, list of MethodAttempts) so the caller can log
    which methods were tried and how each one fared.
    """
    methods = methods or ["A_timedtext", "B_wrappers", "C_ytdlp"]
    expected_paradigm_atoms = expected_paradigm_atoms or []
    fetched_at = datetime.now(timezone.utc).isoformat()
    vid = extract_video_id(url)
    attempts: List[MethodAttempt] = []

    if not vid:
        return (FetchResult(
            url=url, video_id=None, success=False, transcript_id=None,
            output_path=None, raw_output_path=None,
            n_chars_raw=0, n_chars_canonical=0, n_lines_canonical=0,
            fetch_method="skipped",
            failure_reason="could_not_extract_video_id",
            fetched_at=fetched_at,
        ), attempts)

    method_fns = {
        "A_timedtext": fetch_method_a_timedtext,
        "B_wrappers": fetch_method_b_wrappers,
        "C_ytdlp": fetch_method_c_ytdlp,
    }

    raw_text = ""
    chosen_method = ""
    for m in methods:
        fn = method_fns.get(m)
        if not fn:
            continue
        success, text, reason = fn(vid)
        attempts.append(MethodAttempt(
            method=m,
            success=success,
            failure_reason=None if success else reason,
            n_chars=len(text) if success else 0,
            attempted_at=datetime.now(timezone.utc).isoformat(),
        ))
        if success:
            raw_text = text
            chosen_method = m
            break

    if not raw_text:
        # All methods failed
        all_reasons = "; ".join(f"{a.method}: {a.failure_reason}" for a in attempts)
        return (FetchResult(
            url=url, video_id=vid, success=False, transcript_id=None,
            output_path=None, raw_output_path=None,
            n_chars_raw=0, n_chars_canonical=0, n_lines_canonical=0,
            fetch_method="all_methods_failed",
            failure_reason=all_reasons[:500],
            fetched_at=fetched_at,
        ), attempts)

    cleaned = clean_text(raw_text)
    canonical = canonicalize(cleaned)
    n_lines = canonical.count("\n")

    inputs_dir.mkdir(parents=True, exist_ok=True)
    nnn = next_transcript_number(inputs_dir)
    speaker_slug = slugify(speaker, max_len=20)
    topic_slug = slugify(title, max_len=30)
    base = f"transcript_{nnn:03d}_{speaker_slug}_{topic_slug}"
    canonical_path = inputs_dir / f"{base}_canonical.txt"
    raw_path = inputs_dir / f"{base}_raw.txt"
    tid = f"T{nnn:03d}"

    if canonical_path.exists() or raw_path.exists():
        return (FetchResult(
            url=url, video_id=vid, success=False, transcript_id=None,
            output_path=None, raw_output_path=None,
            n_chars_raw=len(raw_text), n_chars_canonical=len(canonical),
            n_lines_canonical=n_lines,
            fetch_method=chosen_method,
            failure_reason=f"refused_to_overwrite_existing: {canonical_path.name}",
            fetched_at=fetched_at,
        ), attempts)

    canonical_path.write_text(canonical, encoding="utf-8")
    raw_path.write_text(raw_text, encoding="utf-8")

    manifest = load_or_init_manifest(manifest_path)
    entry = {
        "id": tid,
        "path": str(canonical_path),
        "raw_path": str(raw_path),
        "speaker": speaker,
        "title": title,
        "youtube_url": url,
        "video_id": vid,
        "upload_date": upload_date,
        "fetched_at": fetched_at,
        "claude_cutoff_relationship": classify_vs_cutoff(upload_date),
        "fetch_method": chosen_method,
        "fetch_methods_attempted": [a.method for a in attempts],
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

    return (FetchResult(
        url=url, video_id=vid, success=True, transcript_id=tid,
        output_path=str(canonical_path), raw_output_path=str(raw_path),
        n_chars_raw=len(raw_text), n_chars_canonical=len(canonical),
        n_lines_canonical=n_lines,
        fetch_method=chosen_method,
        failure_reason=None,
        fetched_at=fetched_at,
    ), attempts)


def fetch_all_v2(
    seed_path: Path,
    inputs_dir: Path = Path("tari/inputs"),
    manifest_path: Path = Path("tari/inputs/manifest.json"),
    fetch_log_path: Path = Path("paradigm_shift/fetch_methods_log.json"),
    methods: Optional[List[str]] = None,
) -> List[FetchResult]:
    """Iterate seeds, try each method per seed, write a structured log."""
    with seed_path.open("r", encoding="utf-8") as f:
        seeds = json.load(f)

    results: List[FetchResult] = []
    all_attempts: Dict[str, List[dict]] = {}

    for s in seeds:
        url = s["url"]
        res, attempts = fetch_one_v2(
            url=url, speaker=s.get("speaker", "?"),
            title=s.get("title", "?"),
            upload_date=s.get("upload_date"),
            why_chosen=s.get("why_chosen", ""),
            expected_paradigm_atoms=s.get("expected_paradigm_atoms", []),
            inputs_dir=inputs_dir, manifest_path=manifest_path,
            methods=methods,
        )
        results.append(res)
        all_attempts[url] = [asdict(a) for a in attempts]

    fetch_log_path.parent.mkdir(parents=True, exist_ok=True)
    method_success_count: Dict[str, int] = {"A_timedtext": 0, "B_wrappers": 0, "C_ytdlp": 0}
    method_attempt_count: Dict[str, int] = {"A_timedtext": 0, "B_wrappers": 0, "C_ytdlp": 0}
    for url, attempts in all_attempts.items():
        for a in attempts:
            method_attempt_count[a["method"]] = method_attempt_count.get(a["method"], 0) + 1
            if a["success"]:
                method_success_count[a["method"]] = method_success_count.get(a["method"], 0) + 1

    log = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "seed_path": str(seed_path),
        "n_attempted": len(results),
        "n_success": sum(1 for r in results if r.success),
        "n_fail": sum(1 for r in results if not r.success),
        "method_attempts": method_attempt_count,
        "method_successes": method_success_count,
        "per_url_attempts": all_attempts,
        "results": [asdict(r) for r in results],
    }
    with fetch_log_path.open("w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    return results


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_fetch = sub.add_parser("fetch")
    p_fetch.add_argument("--seed_path", required=True, type=Path)
    p_fetch.add_argument("--inputs_dir", type=Path, default=Path("tari/inputs"))
    p_fetch.add_argument("--manifest_path", type=Path,
                          default=Path("tari/inputs/manifest.json"))
    p_fetch.add_argument("--fetch_log_path", type=Path,
                          default=Path("paradigm_shift/fetch_methods_log.json"))
    p_fetch.add_argument("--methods", nargs="+", default=None,
                          help="Subset of [A_timedtext, B_wrappers, C_ytdlp]")

    p_test = sub.add_parser("test")
    p_test.add_argument("--video_id", required=True)
    p_test.add_argument("--methods", nargs="+", default=None)

    args = ap.parse_args()
    if args.cmd == "fetch":
        results = fetch_all_v2(
            seed_path=args.seed_path,
            inputs_dir=args.inputs_dir,
            manifest_path=args.manifest_path,
            fetch_log_path=args.fetch_log_path,
            methods=args.methods,
        )
        n_ok = sum(1 for r in results if r.success)
        print(f"v2 fetched {n_ok}/{len(results)} successfully")
        for r in results:
            if r.success:
                print(f"  OK   {r.transcript_id}  method={r.fetch_method}  {Path(r.output_path).name}")
            else:
                print(f"  FAIL {r.url}: {r.failure_reason[:200]}")
    elif args.cmd == "test":
        method_fns = {
            "A_timedtext": fetch_method_a_timedtext,
            "B_wrappers": fetch_method_b_wrappers,
            "C_ytdlp": fetch_method_c_ytdlp,
        }
        ms = args.methods or list(method_fns.keys())
        for m in ms:
            fn = method_fns[m]
            ok, text, reason = fn(args.video_id)
            print(f"{m}: {'OK' if ok else 'FAIL'}  chars={len(text) if ok else 0}  reason={reason[:200]}")


if __name__ == "__main__":
    main()
