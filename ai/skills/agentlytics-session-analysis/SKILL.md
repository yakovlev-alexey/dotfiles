---
name: agentlytics-session-analysis
description: Use when analyzing agentic development sessions, prompt quality, agent collaboration habits, coding-agent trajectories, or Agentlytics MCP history across Codex, Cursor, OpenCode, Claude, and similar agent environments.
---

# Agentlytics Session Analysis

## Purpose

Use this after Agentlytics setup is complete to audit sessions: prompt quality, context quality, trajectory efficiency, verification rigor, outcome, and collaboration habits.

**REQUIRED SETUP:** Before analysis, use `agentlytics-setup` or confirm it already succeeded in the current workflow. The database must be freshly joined with the selected Agentlytics `--join localhost:4638 --username <username>` command, and MCP tools should be visible or the user must have approved the documented fallback path.

If setup is missing or stale, stop analysis and run `agentlytics-setup` first.

## MCP Collection Workflow

1. Discover candidate sessions.
   - Known username: `get_user_activity(username, limit=50)`; increase limit if the requested period is broad.
   - Useful queries: project names, repo folder names, ticket keys, distinctive task terms.

2. Filter by the requested date range.
   - Keep sessions whose `lastUpdated` is inside the range.
   - Preserve source/project diversity; do not over-sample one repo when several repos appear.

3. Group candidates by project, source, and task type.
   - Examples: debug, UI implementation, feature implementation, exploration, planning, review, CI/release, config/devex.
   - Pick a representative sample only when the user asked for sampled coverage or the selected sessions stay below delegation thresholds. Any report based on a subset must say coverage is sampled.

4. Fetch details with `get_session_detail(session_id, username)` for selected sessions.
   - Prioritize sessions with many messages/tool calls, failed checks, follow-up corrections, screenshots/logs, or ambiguous outcomes.
   - Include a few short successful sessions as a control group.

5. Use available activity metrics.
   - `totalMessages`, `toolCalls`, `models`, `source`, `folder`, `lastUpdated`.
   - Flag long sessions: more than 50 messages or more than 80 tool calls.

## Subagent Strategy

Use subagents when available and the analysis would otherwise flood the main context.

Delegation threshold:
- More than 8 candidate sessions in the requested date range.
- More than 250 total messages across candidate sessions.
- More than 300 total tool calls across candidate sessions.
- Any single session with more than 50 messages or more than 80 tool calls.

If any threshold is met, subagent delegation is mandatory for full-range analysis. Do not fetch a representative subset and present it as a full-range analysis.

To satisfy tool policies that require explicit delegation, the user's request should say something like: "Use `agentlytics-session-analysis` and explicitly delegate long sessions or batches to subagents." If that wording is missing and subagent tools require explicit permission, stop after discovery, report the threshold that was met, and ask for explicit permission to delegate. Do not continue with partial manual analysis unless the user explicitly asks for a sampled report.

Good subagent targets:
- One long session: more than 50 messages or more than 80 tool calls.
- One batch of 3-6 short sessions from the same project/task type.
- One focused angle across sessions, such as CI debugging, UI prompts, verification quality, or domain-rule corrections.

Main agent responsibilities:
- Discover sessions, choose the date range, group candidates, and assign analysis work.
- Pass only the needed session transcript(s), metadata, and rubric to each subagent.
- Ask subagents for structured summaries, not long retellings.
- Merge subagent outputs into one final coaching report.

Do not use subagents for the initial MCP discovery step. Use them after candidate sessions are selected. If subagent tools are not exposed in the current tool list, use tool discovery for sub-agent tools. If the threshold is met and subagents are unavailable or permission is missing, stop and ask for permission, a narrower scope, or an explicitly sampled report; do not analyze only part of the sessions and imply complete coverage.

If subagents are not available and no delegation threshold was met, analyze incrementally: fetch 1-3 session details at a time, write compact notes, then continue. If a threshold was met, use incremental analysis only after the user explicitly narrows the scope or accepts sampled coverage.

For the exact delegated output contract, use `subagent-prompt.md`.

## Analysis Dimensions

Give qualitative feedback for each meaningful session across these dimensions. Avoid numeric ratings; explain what was strong, weak, missing, or not assessable and what concrete behavior would improve the next run.

| Dimension | What to inspect |
| --- | --- |
| Goal clarity | Was the desired outcome explicit? |
| Context quality | Were logs, files, screenshots, errors, domain rules, or examples supplied early? |
| Scope control | Was the task sized for one agent run? Were non-goals stated? |
| Trajectory efficiency | Did the agent inspect before editing, avoid loops, and choose relevant tools? |
| Correction quality | Were user corrections timely, specific, and evidence-based? |
| Verification rigor | Were tests, builds, screenshots, logs, or other pass/fail signals used? |
| Outcome | Did the session end with a concrete, reviewable result? |

## Patterns To Look For

Positive signals:
- File paths, line ranges, logs, screenshots, exact error text.
- Acceptance criteria and "do not edit/touch" boundaries.
- Requests to inspect existing patterns before implementation.
- Explicit verification commands or expected evidence.
- Early domain corrections when the agent makes a bad assumption.

Efficiency risks:
- Vague starts that require multiple clarifications.
- Large implementation threads that mix exploration, planning, coding, and bugfixes.
- Missing stderr/job names/artifact paths in CI debugging.
- UI work without screenshot, ASCII layout, or reference component.
- Domain rules added after implementation instead of before.
- "Fix it" prompts without current behavior, expected behavior, and verification target.

## Output Format

Return a compact report:

1. Data coverage: username(s), projects, date range, number of sessions found, delegated, and inspected. State clearly whether coverage is complete or sampled. If sampled, say which selection criteria were used.
2. Top strengths: 3-5 bullets with concrete examples.
3. Top inefficiencies: 3-5 bullets with concrete examples.
4. Session findings: table with session, type, strongest dimension, weakest dimension, key issue, best next habit.
5. Prompt rewrites: rewrite 2-4 weak or high-impact prompts.
6. Persistent improvements: suggest only minimal AGENTS.md/skill rules that are justified by repeated evidence. For sampled coverage, suggest persistent rules only when the pattern repeats inside the inspected sample and label them as provisional.

## Prompt Rewrite Template

```text
Goal:

Context:
- files/logs/screenshots:
- current behavior:
- expected behavior:

Scope:
- do:
- do not:

Acceptance criteria:
- behavior:
- edge cases:
- verification:

Before editing:
- inspect existing pattern
- explain short plan
- for UI changes, show an ASCII layout
```

## Common Mistakes

- Do not analyze before `agentlytics-setup` has refreshed history in this workflow.
- Do not stop after summarizing sessions; extract habits and rewrite prompts.
- Do not overfit to one bad session; separate one-off incidents from repeated patterns.
- Do not recommend broad AGENTS.md rules without evidence from multiple sessions.
- Do not load many full transcripts into the main context when subagents can summarize them.
- Do not analyze a subset and write conclusions as if all sessions were inspected.
- Do not expose secrets or sensitive personal data from session logs.
- Do not edit this skill without running the pressure scenarios in `pressure-scenarios.md`.
