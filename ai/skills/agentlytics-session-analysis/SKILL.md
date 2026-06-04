---
name: agentlytics-session-analysis
description: Use when analyzing agentic development sessions, prompt quality, agent collaboration habits, coding-agent trajectories, or Agentlytics MCP history across Codex, Cursor, OpenCode, Claude, and similar agent environments.
---

# Agentlytics Session Analysis

## Purpose

Use Agentlytics to audit agentic development sessions: prompt quality, context quality, trajectory efficiency, verification rigor, and collaboration habits.

Default date range: today in the user's local timezone. If the user asks for another period, analyze that explicit range instead.

The Agentlytics relay is local-only. For this workflow, broad local searches across all users are allowed when needed to discover the correct username, project path, or session ids.

## Prerequisites

1. Check whether the Agentlytics MCP server is available in the current session.
   - Prefer a cheap MCP call first: `get_user_activity` for a known username/project, or `search_sessions` for a known local project name.
   - If Agentlytics MCP tools are missing or return connection errors, do not inspect the installed package, probe REST endpoints, search local source, or spend time debugging tool registration. Start the local relay immediately:

```bash
agentlytics --relay
```

2. Check that history has been joined/synchronized.
   - After starting the relay, if the database appears empty, if known usernames/projects return no activity, or if only stale data appears, ask for the username if it is not already known and run the join command immediately:

```bash
agentlytics --join 192.168.1.164:4638 --username <username>
```

3. Verify the database is not empty before analysis.
   - Because the relay is strictly local, `list_users` is acceptable for discovery.
   - If a known username fails, use `search_sessions` without `username` for relevant project names, folder segments, or distinctive terms.
   - Once a real username is found, prefer scoped calls with that username.

Operational rule:
- Treat `agentlytics --relay` and, when needed, `agentlytics --join 192.168.1.164:4638 --username <username>` as the prescribed setup path. Do not substitute package inspection, endpoint probing, CLI help spelunking, or alternative discovery unless these commands fail after being run.

## Date Range

Use the current local date from the environment. Treat date ranges as the user's timezone day boundaries unless the user asks otherwise.

Range rules:
- No range specified: analyze today.
- Relative range specified: convert it to concrete dates in the response, e.g. "last 7 days" -> `YYYY-MM-DD..YYYY-MM-DD`.
- Absolute range specified: use the user's dates exactly; clarify only if the range is ambiguous.
- For a single day, include sessions whose `lastUpdated` falls on that local date.

When the MCP API does not provide date filtering, fetch recent sessions and filter by `lastUpdated` locally. If the requested range is older than the recent activity window, use `search_sessions` by project/task keywords and then filter returned `lastUpdated` values.

## MCP Collection Workflow

1. Discover candidate sessions.
   - Known username: `get_user_activity(username, limit=50)`; increase limit if the requested period is broad.
   - Unknown username: `list_users()` or `search_sessions(query, limit=20)` without username.
   - Useful queries: project names, repo folder names, ticket keys, distinctive task terms.

2. Filter by the requested date range.
   - Keep sessions whose `lastUpdated` is inside the range.
   - Preserve source/project diversity; do not over-sample one repo when several repos appear.

3. Group candidates by project, source, and task type.
   - Examples: debug, UI implementation, feature implementation, exploration, planning, review, CI/release, config/devex.
   - Pick a representative sample instead of reading every session when the range has many small sessions.

4. Fetch details with `get_session_detail(session_id, username)` for selected sessions.
   - Prioritize sessions with many messages/tool calls, failed checks, follow-up corrections, screenshots/logs, or ambiguous outcomes.
   - Include a few short successful sessions as a control group.

5. Use available activity metrics.
   - `totalMessages`, `toolCalls`, `models`, `source`, `folder`, `lastUpdated`.
   - Flag long sessions: more than 50 messages or more than 80 tool calls.

## Subagent Strategy

Use subagents when available and the analysis would otherwise flood the main context.

Good subagent targets:
- One long session: more than 50 messages or more than 80 tool calls.
- One batch of 3-6 short sessions from the same project/task type.
- One focused angle across sessions, such as CI debugging, UI prompts, verification quality, or domain-rule corrections.

Main agent responsibilities:
- Discover sessions, choose the date range, group candidates, and assign analysis work.
- Pass only the needed session transcript(s), metadata, and rubric to each subagent.
- Ask subagents for structured summaries, not long retellings.
- Merge subagent outputs into one final coaching report.

Do not use subagents for the initial MCP discovery step. Use them after candidate sessions are selected.

Subagent prompt template:

```text
You are auditing Agentlytics session transcript(s) for an orchestrating agent.
Your output must be compact, evidence-based, and directly mergeable into a final coaching report.

Input you will receive:
- session metadata: id, name, project/folder, source, model, lastUpdated, message/tool-call counts when available
- one full long transcript OR a small batch of related short transcripts
- optional focus area, such as CI debugging, UI prompts, verification, or domain-rule corrections

Analyze the full trajectory, not just the final answer:
- user's initial prompt and follow-up prompts
- context provided or missing
- agent exploration, tool use, edits, loops, and verification
- user corrections and whether they improved the outcome
- final evidence of completion or unresolved risk

For each session, return exactly this structure:

SESSION: <id or name>
TYPE: <debug | UI | feature | planning | explore | review | CI/release | config/devex | other>
SCORE: <1-10>
CONFIDENCE: <high | medium | low>
DIMENSIONS:
- goal_clarity: <1-5> - <one sentence>
- context_quality: <1-5> - <one sentence>
- scope_control: <1-5> - <one sentence>
- trajectory_efficiency: <1-5> - <one sentence>
- verification_rigor: <1-5> - <one sentence>
EVIDENCE:
- <2-4 concrete transcript facts; quote only short fragments, prefer paraphrase>
STRENGTH:
- <the best user behavior in this session>
INEFFICIENCY:
- <the highest-impact avoidable inefficiency>
REWRITE:
```text
<rewrite the starting prompt or the highest-impact correction prompt>
```
DURABLE_HABIT:
- <one habit to keep/change; phrase as user behavior, not agent behavior>
AGGREGATION_TAGS:
- <2-5 tags like missing-stderr, good-screenshot, oversized-thread, strong-domain-correction>

For a batch, add:
BATCH_PATTERNS:
- repeated_strengths: <1-3 bullets>
- repeated_inefficiencies: <1-3 bullets>
- candidate_persistent_rules: <only rules justified by at least 2 sessions; otherwise "none">

Rules:
- Do not produce a chronological summary.
- Do not invent missing evidence; mark confidence low when the transcript is truncated or redacted.
- Do not recommend broad AGENTS.md or skill rules from one isolated session.
- Do not expose secrets, tokens, private keys, or sensitive personal data.
- Keep the whole response concise enough for the orchestrator to merge without rereading the transcript.
```

If subagents are not available, analyze incrementally: fetch 1-3 session details at a time, write compact notes, then continue.

## Analysis Rubric

Score each meaningful session from 1-10 across these dimensions:

| Dimension | What to inspect |
| --- | --- |
| Goal clarity | Was the desired outcome explicit? |
| Context quality | Were logs, files, screenshots, errors, domain rules, or examples supplied early? |
| Scope control | Was the task sized for one agent run? Were non-goals stated? |
| Agent trajectory | Did the agent inspect before editing, avoid loops, and choose relevant tools? |
| Correction quality | Were user corrections timely, specific, and evidence-based? |
| Verification | Were tests, builds, screenshots, logs, or other pass/fail signals used? |
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

## Research-Grounded Heuristics

Use these principles when coaching the user:

- Evaluate the full trajectory, not only the final answer: messages, tool calls, retries, verification, and corrections.
- Prefer structured prompts: goal, context, scope, acceptance criteria, verification.
- For coding agents, treat issues and task descriptions as prompts. Small, well-scoped tasks usually outperform broad tasks.
- Require evidence before shipping: tests, build output, screenshots, logs, or a clear reason verification was not possible.
- Keep persistent instructions minimal. Add rules to AGENTS.md or skills only when repeated session evidence shows they prevent real failures.

## Output Format

Return a compact report:

1. Data coverage: username(s), projects, date range, number of sessions found and inspected.
2. Top strengths: 3-5 bullets with concrete examples.
3. Top inefficiencies: 3-5 bullets with concrete examples.
4. Session scorecard: table with session, type, score, key issue, best next habit.
5. Prompt rewrites: rewrite 2-4 weak or high-impact prompts.
6. Persistent improvements: suggest only minimal AGENTS.md/skill rules that are justified by repeated evidence.

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

- Do not stop after summarizing sessions; extract habits and rewrite prompts.
- Do not overfit to one bad session; separate one-off incidents from repeated patterns.
- Do not recommend broad AGENTS.md rules without evidence from multiple sessions.
- Do not load many full transcripts into the main context when subagents can summarize them.
- Do not expose secrets or sensitive personal data from session logs.
