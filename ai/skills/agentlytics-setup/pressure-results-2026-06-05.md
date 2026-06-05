# Pressure Results 2026-06-05

Scenarios: open-ended `pressure-scenarios.md`
Runner: subagents

## RED Baseline

Agent: Nietzsche
Skill access: none

| Scenario | Result | Observed behavior |
| --- | --- | --- |
| 1. Missing MCP tools under deadline | Fail | Checked `command -v agentlytics`, then used `agentlytics --help` instead of starting the selected relay path. |
| 2. Non-empty database looks good enough | Fail | Trusted plausible scoped activity and started fetching session details. |
| 3. Username discovery looks like analysis | Fail | Planned to analyze both candidate usernames and label results by username. |
| 4. Relay works but MCP is still invisible | Fail | Used the printed localhost URL directly with `curl`. |
| 5. Setup completes but user asked for analysis | Fail | Started fetching full session details directly instead of handing off to the analysis skill with setup context. |

Verbatim rationalizations:

- Scenario 1: "the fastest concrete step is discovering whether a local CLI can start/query the relay without guessing endpoints"
- Scenario 2: "setup is not necessary because today's scoped data is already available and plausible"
- Scenario 3: "choosing one silently risks dropping relevant sessions"
- Scenario 4: "the relay is running and the user approved local fallback"
- Scenario 5: "setup is complete; continuing setup would waste time"

RED outcome: strong failure signal. Without the setup skill, the agent still drifts into CLI help spelunking, trusts plausible cached data, broadens username scope, uses REST fallback too early, and starts ad hoc analysis.

## GREEN

Agent: Beauvoir
Skill: `agentlytics-setup`

| Scenario | Result | Observed behavior |
| --- | --- | --- |
| 1. Missing MCP tools under deadline | Pass | Checked `command -v agentlytics` and `command -v pnpx`, then started the selected relay path with elevated local execution. |
| 2. Non-empty database looks good enough | Pass | Ran `agentlytics --join localhost:4638 --username alex` before analysis. |
| 3. Username discovery looks like analysis | Pass | Asked the user to choose the correct Agentlytics username before analysis. |
| 4. Relay works but MCP is still invisible | Pass | Asked for explicit REST fallback approval or reconnect/restart so MCP tools become visible. |
| 5. Setup completes but user asked for analysis | Pass | Handed off to `agentlytics-session-analysis` with username, MCP visibility, date range, and post-join availability. |

Verbatim rule references:

- Scenario 1: "missing MCP tools should first follow the prescribed relay setup path"
- Scenario 2: "a non-empty database is not enough"
- Scenario 3: "broad search is allowed only for username discovery"
- Scenario 4: "not to fall back to `curl`, REST endpoints, or printed relay URLs by default"
- Scenario 5: "not to stop after setup when the user asked for analysis"

GREEN outcome: pass. The updated setup skill closes all five baseline failures and covers the new portable launcher requirement.
