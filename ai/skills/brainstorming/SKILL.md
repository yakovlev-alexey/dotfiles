---
name: brainstorming
description: Use when the user asks to brainstorm or explore a design, or when substantial uncertainty about goals, scope, architecture, or tradeoffs must be resolved before implementation. Clear, bounded implementation requests can proceed directly under the user's existing authorization.
---

# Brainstorming

Turn material design uncertainty into an implementable decision. Scale the discussion to the uncertainty and cost of error; follow the user's authorization and the project's conventions.

## Choose the amount of discussion

- **Clear, bounded change:** inspect the existing flow, state any minor assumption, implement, and verify. Do not introduce a design document or a new approval checkpoint solely because this skill was selected.
- **Explicit brainstorming or unclear outcome:** explore the question the user asked. Clarify only missing facts that change the result. Present a concise recommendation and meaningful alternatives; do not treat a request to explore as permission to implement.
- **Large, risky, or architectural decision:** inspect the current system, explain the choices and consequences, and obtain the user's decision on significant unresolved choices before implementation. If that decision is already recorded, continue from it.

## Resolve the design

1. Read the relevant code, configuration, documentation, and existing patterns. Identify the user's goal, constraints, and observable acceptance criteria.
2. Reflect the intended outcome briefly. Separate known requirements from assumptions. Ask focused questions where an answer changes scope, behavior, risk, or architecture.
3. Compare the smallest workable approach with meaningful alternatives. Reuse the project's mechanisms and avoid unrelated features, new layers, and speculative fallback paths.
4. Present the design at the level needed to make the decision. Use Mermaid for relationships and branching when clearer than prose; show a compact ASCII layout before adding or moving UI elements.
5. For substantial work, record the agreed requirements, decisions, boundaries, and acceptance criteria in the project's established format when that helps implementation. A short in-chat design is sufficient for bounded work. Do not create a separate spec, plan, or commit as a ritual.
6. Continue with implementation when it is within the agreed scope and authorization. Ask only about remaining significant choices or actions that require authorization. Preserve constraints already decided in the conversation.

## Exploration and obstacles

When no expected path exists, use small, disposable experiments to test consequential assumptions. Report what the experiment established before treating it as a design fact. If new evidence changes the agreed scope or exposes a significant tradeoff, explain it and offer options before changing the approach. Continue independent authorized work while awaiting that decision.

## Handoff

Carry the goal, decisions, and acceptance criteria into implementation. Verify the promised result in the target consumer and report material limitations. Use the project's implementation and testing workflow; do not require an unavailable planning skill.
