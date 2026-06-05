---
name: agentlytics-setup
description: Use when starting the Agentlytics relay, joining or refreshing local Agentlytics history, discovering the username, or handling missing Agentlytics MCP visibility before session analysis.
---

# Agentlytics Setup

## Purpose

Use this skill to make Agentlytics ready for analysis: relay reachable, MCP tools visible when possible, username known, and local history freshly synchronized.

The Agentlytics relay is local-only. Broad local searches across all users are allowed only to discover the correct username, project path, or session ids.

**NEXT SKILL:** After setup succeeds, use `agentlytics-session-analysis` for date filtering, session selection, scoring, prompt rewrites, and coaching.

## Setup Workflow

1. Check whether Agentlytics MCP tools are visible.
   - Prefer a cheap MCP call first: `get_user_activity` for a known username/project, or `search_sessions` for a known local project name.
   - If tools are missing or return connection errors, start the relay immediately:

```bash
agentlytics --relay
```

   - Do not inspect the installed package, probe REST endpoints, search local source, or debug tool registration before trying the prescribed relay path.
   - If the runtime uses sandboxing, approval gates, or restricted local networking, request an unsandboxed/elevated local process before running the relay. Binding to `localhost:4638` can fail inside sandboxes.
   - Portable approval wording: "Allow starting the local Agentlytics relay so it can bind to localhost:4638?"
   - In Codex, use `sandbox_permissions: require_escalated`.

2. Discover the username if needed.
   - Use `list_users()` only for discovery.
   - Use unscoped `search_sessions(query, limit=20)` for relevant project names, folder segments, or distinctive task terms.
   - Do not analyze across all users. Once the real username is found, prefer scoped calls with that username.
   - If discovery is ambiguous, ask the user for the username.

3. Refresh history before any analysis.

```bash
agentlytics --join localhost:4638 --username <username>
```

   - This is mandatory even when the database is non-empty, because the local database can be stale.
   - If the runtime uses sandboxing, approval gates, or restricted local networking, request an unsandboxed/elevated local process for this command too.
   - Portable approval wording: "Allow Agentlytics to join the local relay and synchronize session history for <username>?"

4. Verify the post-join database is usable.
   - Confirm scoped activity or search results exist for the selected username.
   - If a known username fails, use unscoped discovery again only to find the right username.
   - If the database is still empty, report that analysis cannot start from local Agentlytics data.

## Operational Rules

- Never start session analysis before `agentlytics --join localhost:4638 --username <username>` has run successfully in the current workflow.
- Treat `agentlytics --relay` and `agentlytics --join localhost:4638 --username <username>` as the setup path.
- Do not substitute package inspection, endpoint probing, CLI help spelunking, or alternative discovery unless the prescribed commands fail after the runtime's required approval/elevation.
- Use Agentlytics MCP tools for discovery and details.
- Do not fall back to `curl`, local REST endpoints, or printed relay URLs by default.
- If MCP tools are still not visible after relay starts and join succeeds, report that the current thread cannot see the MCP server and ask whether to reconnect/restart the thread or explicitly approve REST fallback.

## Handoff To Analysis

When setup succeeds, pass these facts into `agentlytics-session-analysis`:

- username used for join
- whether MCP tools are visible in the current thread
- requested date range, if any
- project/folder hints discovered during setup
- any caveat about empty, ambiguous, or stale-looking data

## Common Mistakes

- Do not treat a non-empty database as fresh enough. Run join anyway.
- Do not use broad user discovery as permission to analyze across users.
- Do not debug Agentlytics internals before running the relay and join commands.
- Do not use REST fallback without explicit user approval.
- Do not stop after setup when the user asked for analysis; hand off to `agentlytics-session-analysis`.
- Do not edit this skill without running the pressure scenarios in `pressure-scenarios.md`.
