---
name: meetily-meeting-notes
description: Summarize local Meetily meeting recordings into structured notes. Scans ~/Movies/meetily-recordings (default today), skips already-noted recordings, matches calendar events for title and participants, writes a markdown note. Use when the user asks to summarize meetings, process Meetily recordings, write meeting notes from transcripts, or catch up on today's calls.
---

# Meetily Meeting Notes

Turn local Meetily recordings into structured meeting notes.

## Paths


| Setting      | Env var                  | Default                       |
| ------------ | ------------------------ | ----------------------------- |
| Recordings   | `MEETILY_RECORDINGS_DIR` | `~/Movies/meetily-recordings` |
| Notes output | `MEETING_NOTES_DIR`      | see below                     |


### Where to write notes

Resolve output in this order:

1. explicit path from the user or `--notes-dir`
2. infer from working directory if it contains notes, knowledge base, or Obsidian vault
3. `MEETING_NOTES_DIR`
4. fallback: `~/Documents/meeting-notes`

Before writing, read the local meeting template if it exists and 1-2 recent notes for style and frontmatter.

If no local template exists, use the fallback template in section 5.

## Workflow

```
1. List candidates  →  2. Skip existing notes  →  3. Match calendar  →  4. Summarize  →  5. Write note
```



### 1. List candidates

Default scope: **today** in local timezone. Override with `--date YYYY-MM-DD` or a user-provided range.

```bash
python3 scripts/list_recordings.py
python3 scripts/list_recordings.py --date 2026-07-15
python3 scripts/list_recordings.py --notes-dir "$VAULT_PATH/meeting-notes"
```

Include a recording when:

- `metadata.json` exists
- `transcripts.json` has at least one segment

Do **not** trust `metadata.status` alone. Meetily often leaves `status: recording` after the call ends.

Use `effective_status` from the helper:

- `completed` — metadata says finished
- `completed_inferred` — transcript exists and `transcript_last_updated` is older than 10 minutes
- `recording` — only when there is no transcript yet

Skip only folders with no transcript at all.

### 2. Skip existing notes

Search all resolved notes directories recursively.

A recording is already covered if any note has:

- frontmatter `source:` or `recording:` pointing to the recording folder, or
- same `date` and the recording folder/name in the body

If found, report it and skip unless the user asked to refresh that note.

### 3. Match calendar

Use any calendar tool available in the session (MCP, calendar skill, API).

Match window:

- start ← `metadata.created_at`
- end ← `metadata.completed_at`, else `transcript_last_updated`, else last segment time

Pick the event with the best overlap. Prefer events where the user is organizer or attendee.

From the matched event, take:

- title
- start/end time
- participants (names or emails)
- location / conference link if useful

If no calendar access or no match:

- title ← `metadata.meeting_name`
- participants ← infer from transcript (names, greetings, self-introductions)
- say explicitly that calendar enrichment was unavailable



### 4. Summarize

Read `transcripts.json` segments in order. Build the note from transcript facts, enriched with calendar metadata.

Write in the language of the meeting. Prefer `metadata.detected_summary_language` when present; otherwise follow the transcript.

Do not invent decisions, owners, or deadlines that are not supported by the transcript or calendar context.

Link people with existing vault pages when wikilinks already exist in `01 Люди/`.

### 5. Write note

Filename for personal vaults: `YYYY-MM-DD — <short-title>.md`

#### Fallback template

Use this in users request language only when no local vault template exists:

```markdown
---
date: YYYY-MM-DD
start: HH:MM
end: HH:MM
title: Meeting title
participants:
  - Name
source: meetily
recording: /absolute/path/to/recording-folder
calendar_event: optional event id or link
created: YYYY-MM-DDTHH:MM:SS
---

# Meeting title

## Participants
## Summary
## Key points
## Decisions
## Action items
## Open questions
## Source
```

After writing, show the user: path, title, participants, effective status, and a 2–3 sentence summary.

## Edge cases


| Case                                                         | Action                                                           |
| ------------------------------------------------------------ | ---------------------------------------------------------------- |
| Metadata still says `recording`, transcript stopped updating | Treat as finished (`completed_inferred`)                         |
| Multiple recordings same day                                 | Process all unprocessed ones; mention count upfront              |
| Overlapping recordings                                       | Match each recording to the closest calendar event by overlap    |
| Very long transcript                                         | Summarize fully; quote only short verbatim fragments when useful |
| No transcript yet                                            | Report "still recording" and stop                                |
| User asks for one meeting                                    | Filter by time, title, or folder name                            |




## Do not

- Commit secrets from transcripts or calendar payloads
- Hardcode a specific calendar provider or company stack
- Replace an existing note without explicit user request
- Write meeting notes into a generic shared folder when a personal vault path is available

