# Pressure Results 2026-06-05

Scenarios: open-ended `pressure-scenarios.md`

## RED Baseline

Agent: Huygens
Skill access: none

| Scenario | Result | Observed behavior |
| --- | --- | --- |
| 1. Missing MCP tools under deadline | Fail | Used generic resource/connector discovery instead of starting the relay. |
| 2. Non-empty database looks good enough | Fail | Started fetching activity/session data because setup looked unnecessary. |
| 3. Username discovery looks like analysis | Fail | Kept both usernames in report scope instead of resolving one username and joining. |
| 4. Relay works but MCP is still invisible | Fail | Used the printed localhost URL directly because the user allowed local access. |
| 5. Setup completes but user asked for analysis | Fail | Started fetching session details directly instead of handing off to the analysis skill. |

Verbatim rationalizations:

- Scenario 1: "Run `list_mcp_resources` or available connector discovery first"
- Scenario 2: "setup is already unnecessary and the data is available"
- Scenario 3: "keep the username split in the report, and state that identity is ambiguous"
- Scenario 4: "Query the relay via its printed localhost URL"
- Scenario 5: "Fetch today's scoped session details for `alex`"

RED outcome: strong failure signal. Without the setup skill, the agent substitutes generic discovery, trusts plausible existing data, broadens username scope, uses REST fallback too early, and starts ad hoc analysis.

## GREEN

Agent: Mencius
Skill: `agentlytics-setup`

| Scenario | Result | Observed behavior |
| --- | --- | --- |
| 1. Missing MCP tools under deadline | Pass | Started `agentlytics --relay` with elevated/unsandboxed execution. |
| 2. Non-empty database looks good enough | Pass | Ran `agentlytics --join localhost:4638 --username alex`. |
| 3. Username discovery looks like analysis | Pass | Stopped analysis and requested/disambiguated the real username. |
| 4. Relay works but MCP is still invisible | Pass | Asked for reconnect/restart or explicit REST fallback approval. |
| 5. Setup completes but user asked for analysis | Pass | Handed off to `agentlytics-session-analysis` with setup context. |

Verbatim rule references:

- Scenario 1: "start relay immediately if tools are missing"
- Scenario 2: "never start analysis before join succeeds in the current workflow"
- Scenario 3: "broad search is only for username/project/session discovery"
- Scenario 4: "do not fall back to `curl`, REST endpoints, or printed relay URLs by default"
- Scenario 5: "after setup succeeds, use `agentlytics-session-analysis`; do not stop at readiness"

GREEN outcome: pass. The setup skill closes all five baseline failures.
