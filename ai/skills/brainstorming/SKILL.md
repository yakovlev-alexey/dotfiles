---
name: brainstorming
description: Use when the user asks to brainstorm or explore a design, or when substantial uncertainty about goals, scope, architecture, or tradeoffs must be resolved before implementation. Clear, bounded implementation requests with low uncertainty and risk can proceed directly under the user's existing authorization.
---

# Brainstorming

Turn material design uncertainty into an implementable decision. Scale the discussion to the uncertainty and cost of error; follow the user's authorization and the project's conventions.

## Choose the amount of discussion

- **Small, clear, low-risk change:** inspect the existing flow, decide directly or describe the result and acceptance check in a few sentences, implement, and verify. Do not introduce a design document or a new approval checkpoint solely because this skill was selected.
- **Explicit brainstorming or unclear outcome:** explore the question the user asked. Clarify only missing facts that change the result. Present a concise recommendation and meaningful alternatives; do not treat a request to explore as permission to implement.
- **Moderately complex work:** prepare a short specification in chat and resolve consequential open choices before implementation.
- **Complex work with interacting components or significant risks:** prepare a specification document in the project's established format. Explain the choices and consequences, and obtain the user's decision on significant unresolved choices before implementation. If that decision is already recorded, continue from it.

## Resolve the design

1. Read the relevant code, configuration, documentation, and existing patterns. Identify the user's goal, constraints, and observable acceptance criteria.
2. Reflect the intended outcome briefly. Separate known requirements from assumptions. Ask focused questions where an answer changes scope, behavior, risk, or architecture.
3. Compare the smallest workable approach with meaningful alternatives. Reuse the project's mechanisms and avoid unrelated features, new layers, and speculative fallback paths.
4. Present the design at the level needed to make the decision. Use Mermaid for relationships and branching when clearer than prose; show a compact ASCII layout before adding or moving UI elements.
5. Write the specification in the chosen form: intended result, scope and constraints, overall solution and consequential decisions, and observable acceptance criteria. Record material choices made by the agent and those agreed with the user. Keep detailed execution steps, commands, scripts, and full artifact text for implementation unless they are part of the required external contract. Before approval, a document can be a separate reviewable artifact outside the source checkout; carry it into the task branch for implementation. Do not commit it to the default branch merely to obtain approval.
6. Continue with implementation when it is within the agreed scope and authorization. Ask only about remaining significant choices or actions that require authorization. Preserve constraints already decided in the conversation.

## Exploration and obstacles

When no expected path exists, use small, disposable experiments to test consequential assumptions. Report what the experiment established before treating it as a design fact. If new evidence changes the agreed scope or exposes a significant tradeoff, explain it and offer options before changing the approach. Continue independent authorized work while awaiting that decision.

## Handoff

Carry the goal, specification, decisions, and acceptance criteria into implementation. Follow the repository's worktree and draft PR workflow. Verify the promised result in the target consumer and deliver evidence for the acceptance criteria, identifying failed or unavailable checks. Use the project's implementation and testing workflow; do not require an unavailable planning skill or introduce approval checkpoints for already-settled decisions.
