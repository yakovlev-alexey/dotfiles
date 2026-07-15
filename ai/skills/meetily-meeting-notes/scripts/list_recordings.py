#!/usr/bin/env python3
"""List Meetily recordings that still need meeting notes."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


DEFAULT_STALE_MINUTES = 10


def expand(path: str) -> Path:
    return Path(path).expanduser().resolve()


def local_day(iso_ts: str, local_tz) -> date | None:
    if not iso_ts:
        return None
    dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(local_tz).date()


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip().splitlines()
    data: dict[str, str] = {}
    for line in block:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def normalize_source_path(value: str) -> str:
    return str(expand(value))


def note_covers_recording(note_path: Path, recording_dir: Path, meta: dict) -> bool:
    text = note_path.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    for key in ("recording", "source"):
        raw = fm.get(key)
        if not raw:
            continue
        try:
            if expand(raw) == recording_dir:
                return True
        except Exception:
            if recording_dir.name in raw:
                return True

    created_at = meta.get("created_at", "")
    if not created_at:
        return False
    rec_day = created_at[:10]
    note_day = fm.get("date", "")
    if note_day != rec_day:
        return False

    title = (meta.get("meeting_name") or recording_dir.name).casefold()
    body = text.casefold()
    short = re.sub(r"^(zoom meeting|meeting)\s+", "", title).strip()
    return short in body or recording_dir.name.casefold() in body


def load_transcript(recording_dir: Path, meta: dict) -> dict | None:
    transcript_name = meta.get("transcript_file") or "transcripts.json"
    transcript_path = recording_dir / transcript_name
    if not transcript_path.exists():
        return None
    try:
        return json.loads(transcript_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def transcript_info(payload: dict | None) -> dict:
    if not payload:
        return {
            "has_transcript": False,
            "segment_count": 0,
            "last_updated": None,
            "last_segment_end": None,
            "duration_seconds": None,
        }
    segments = payload.get("segments") or []
    last = segments[-1] if segments else {}
    return {
        "has_transcript": bool(segments),
        "segment_count": len(segments),
        "last_updated": payload.get("last_updated"),
        "last_segment_end": last.get("audio_end_time"),
        "duration_seconds": last.get("audio_end_time"),
    }


def effective_status(meta: dict, info: dict, now: datetime, stale_minutes: int) -> str:
    raw_status = meta.get("status")
    if raw_status == "completed" or meta.get("completed_at"):
        return "completed"

    if not info["has_transcript"]:
        return raw_status or "recording"

    last_updated = info.get("last_updated")
    if last_updated:
        updated_at = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=timezone.utc)
        age = now.astimezone(timezone.utc) - updated_at.astimezone(timezone.utc)
        if age >= timedelta(minutes=stale_minutes):
            return "completed_inferred"

    return raw_status or "recording"


def is_processable(status: str, info: dict) -> bool:
    if status in {"completed", "completed_inferred"}:
        return info["has_transcript"]
    if status == "recording":
        return info["has_transcript"]
    return info["has_transcript"]


def load_meta(recording_dir: Path) -> dict | None:
    meta_path = recording_dir / "metadata.json"
    if not meta_path.exists():
        return None
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def resolve_notes_dirs(explicit: str | None) -> list[Path]:
    if explicit:
        return [expand(explicit)]

    env_dir = os.environ.get("MEETING_NOTES_DIR")
    if env_dir:
        return [expand(env_dir)]

    vault = os.environ.get("VAULT_PATH")
    if not vault:
        return [expand("~/Documents/meeting-notes")]

    personal_root = expand(vault) / "knowledge-base" / "personal"
    meeting_dirs = sorted(personal_root.glob("*/03 Встречи"))
    if meeting_dirs:
        return meeting_dirs

    return [expand("~/Documents/meeting-notes")]


def collect_notes(notes_dirs: list[Path]) -> list[Path]:
    notes: list[Path] = []
    for notes_dir in notes_dirs:
        if not notes_dir.exists():
            continue
        notes.extend(sorted(notes_dir.glob("**/*.md")))
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recordings-dir", default=os.environ.get("MEETILY_RECORDINGS_DIR", "~/Movies/meetily-recordings"))
    parser.add_argument("--notes-dir", help="Explicit notes directory; otherwise resolve from env/vault")
    parser.add_argument("--date", help="Local date YYYY-MM-DD (default: today)")
    parser.add_argument("--include-noted", action="store_true", help="Include recordings that already have notes")
    parser.add_argument("--stale-minutes", type=int, default=DEFAULT_STALE_MINUTES, help="Treat transcript as finished after N minutes without updates")
    args = parser.parse_args()

    recordings_dir = expand(args.recordings_dir)
    notes_dirs = resolve_notes_dirs(args.notes_dir)
    local_now = datetime.now().astimezone()
    local_tz = local_now.tzinfo or timezone.utc
    target_day = date.fromisoformat(args.date) if args.date else local_now.date()
    notes = collect_notes(notes_dirs)

    candidates = []
    for entry in sorted(recordings_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        meta = load_meta(entry)
        if not meta:
            continue

        created_day = local_day(meta.get("created_at", ""), local_tz)
        if created_day != target_day:
            continue

        payload = load_transcript(entry, meta)
        info = transcript_info(payload)
        status = effective_status(meta, info, local_now, args.stale_minutes)
        if not is_processable(status, info):
            continue

        noted = any(note_covers_recording(note, entry, meta) for note in notes)
        if noted and not args.include_noted:
            continue

        duration_seconds = meta.get("duration_seconds") or info.get("duration_seconds")
        candidates.append(
            {
                "dir": str(entry),
                "name": entry.name,
                "meeting_name": meta.get("meeting_name"),
                "created_at": meta.get("created_at"),
                "completed_at": meta.get("completed_at"),
                "duration_seconds": duration_seconds,
                "metadata_status": meta.get("status"),
                "effective_status": status,
                "language": meta.get("detected_summary_language"),
                "has_transcript": info["has_transcript"],
                "segment_count": info["segment_count"],
                "transcript_last_updated": info["last_updated"],
                "already_noted": noted,
            }
        )

    print(
        json.dumps(
            {
                "date": target_day.isoformat(),
                "notes_dirs": [str(p) for p in notes_dirs],
                "count": len(candidates),
                "recordings": candidates,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
