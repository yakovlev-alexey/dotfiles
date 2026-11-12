---
name: brainstorming
description: Use when the user asks to brainstorm or explore an approach, or when substantial uncertainty about goals, scope, design, or tradeoffs must be resolved before execution. Clear, bounded requests with low uncertainty and risk can proceed directly under the user's existing authorization.
---

# Brainstorming

Turn material uncertainty into an actionable decision for any task. Scale the discussion to the uncertainty and cost of error; follow the user's authorization and established conventions.

## Choose the amount of discussion

- **Small, clear, low-risk task:** inspect the relevant context, decide directly or describe the result and acceptance check in a few sentences, execute, and verify. Do not introduce a design document or a new approval checkpoint solely because this skill was selected.
- **Explicit brainstorming or unclear outcome:** explore the question the user asked. Clarify only missing facts that change the result. Present a concise recommendation and meaningful alternatives; do not treat a request to explore as permission to implement.
- **Moderately complex work:** prepare a short specification in chat and resolve consequential open choices before execution.
- **Complex work with interacting parts or significant risks:** prepare a specification document in the established format. Explain the choices and consequences, and obtain the user's decision on significant unresolved choices before execution. If that decision is already recorded, continue from it.

## Resolve the design

1. Inspect relevant sources, existing materials, and current state. Identify the user's goal, constraints, and observable acceptance criteria.
2. Reflect the intended outcome briefly. Separate known requirements from assumptions. Ask focused questions where an answer changes scope, behavior, risk, or architecture.
3. Compare the smallest workable approach with meaningful alternatives. Reuse existing work and mechanisms; avoid unrelated additions and unnecessary complexity.
4. Present the design at the level needed to make the decision. Use Mermaid for relationships and branching when clearer than prose; show a compact ASCII layout before adding or moving UI elements.
5. Write the specification in the chosen form: intended result, scope and constraints, overall approach and consequential decisions, and observable acceptance criteria. Record material choices made by the agent and those agreed with the user. Keep detailed execution steps and full artifact text for execution unless they are part of the required contract. Prepare a reviewable document in an appropriate destination; for repository work, carry it into the task branch rather than committing it to the default branch to obtain approval.
6. Execute the agreed work when it is within scope and authorization. A request for research or design alone produces findings or a specification, not authorization for subsequent implementation or publication. Ask only about remaining significant choices or actions; preserve constraints already decided in the conversation.

## Exploration and obstacles

When no expected path exists, use small, disposable experiments to test consequential assumptions. Report what the experiment established before treating it as a design fact. If new evidence changes the agreed scope or exposes a significant tradeoff, explain it and offer options before changing the approach. Continue independent authorized work while awaiting that decision.

## Handoff

Carry the goal, decisions, and acceptance criteria into the requested work. Deliver the result with appropriate evidence: sources for findings, a checked artifact for writing or planning, or observed outcomes for changes and actions. Follow worktree and draft PR rules when changing repository files. Identify limitations and unverified criteria; do not require an unavailable planning skill or reopen settled decisions.
