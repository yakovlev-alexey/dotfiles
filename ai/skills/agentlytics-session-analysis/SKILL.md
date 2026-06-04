---
name: agentlytics-session-analysis
description: Use when analyzing today's agentic development sessions, prompt quality, agent collaboration habits, coding-agent trajectories, or Agentlytics MCP history across Codex, Cursor, OpenCode, Claude, and similar agent environments.
---

# Agentlytics Session Analysis

## Purpose

Use Agentlytics to audit today's agentic development sessions: prompt quality, context quality, trajectory efficiency, verification rigor, and collaboration habits.

The Agentlytics relay is local-only. For this workflow, broad local searches across all users are allowed when needed to discover the correct username, project path, or session ids.

## Prerequisites

1. Check whether the Agentlytics MCP server is available in the current session.
   - Prefer a cheap MCP call first: `get_user_activity` for a known username/project, or `search_sessions` for a known local project name.
   - If Agentlytics MCP tools are missing or return connection errors, tell the user to start the local relay:

```bash
agentlytics --relay
```

2. Check that history has been joined/synchronized.
   - If the database appears empty, if known usernames/projects return no activity, or if only stale data appears, ask for the username and tell the user to run:

```bash
agentlytics --join 192.168.1.164:4638 --username <username>
```

3. Verify the database is not empty before analysis.
   - Because the relay is strictly local, `list_users` is acceptable for discovery.
   - If a known username fails, use `search_sessions` without `username` for relevant project names, folder segments, or distinctive terms.
   - Once a real username is found, prefer scoped calls with that username.

## Today Window

Use the current local date from the environment. Treat "today" as the user's timezone day, not UTC, unless the user asks otherwise.

When the MCP API does not provide date filtering, fetch recent sessions and filter by `lastUpdated` date in the response. Include only sessions updated today, unless the user asks for a broader comparison.

## MCP Collection Workflow

1. Discover candidate sessions.
   - Known username: `get_user_activity(username, limit=50)`.
   - Unknown username: `list_users()` or `search_sessions(query, limit=20)` without username.
   - Useful queries: project names, repo folder names, ticket keys, distinctive task terms.

2. Group candidates by project, source, and task type.
   - Examples: debug, UI implementation, feature implementation, exploration, planning, review, CI/release, config/devex.
   - Pick a representative sample instead of reading every session when the day has many small sessions.

3. Fetch details with `get_session_detail(session_id, username)` for selected sessions.
   - Prioritize sessions with many messages/tool calls, failed checks, follow-up corrections, screenshots/logs, or ambiguous outcomes.
   - Include a few short successful sessions as a control group.

4. Use available activity metrics.
   - `totalMessages`, `toolCalls`, `models`, `source`, `folder`, `lastUpdated`.
   - Flag long sessions: more than 50 messages or more than 80 tool calls.

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

1. Data coverage: username(s), projects, date, number of sessions inspected.
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
- Do not expose secrets or sensitive personal data from session logs.
