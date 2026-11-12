# Workflow

Apply this workflow to every task, with effort proportional to its uncertainty and risk:

1. Investigate the goal, relevant sources, existing materials, and current state.
2. Specify the intended result, scope and constraints, overall approach, consequential decisions, and observable acceptance criteria.
3. Resolve significant open decisions with the user. Continue directly when those choices are already settled.
4. Prepare the working context. Use a task worktree by default before changing repository files; use the appropriate tools and destination for other work.
5. Produce the requested result within the agreed scope. A research or design-only request produces findings or a specification, without authorizing subsequent implementation or publication.
6. Verify the result and material claims against the acceptance criteria; collect evidence and identify remaining limitations.
7. Deliver the result and evidence in the requested form. For repository changes, create or update the task's draft PR.

Scale the specification to the task:

- For small, clear, low-risk tasks, decide directly or describe the result and acceptance check in a few sentences.
- For moderately complex work, present a short specification in chat.
- For complex work with interacting parts or significant risks, create a specification document in the established format.

Record material choices made by the agent as well as choices agreed with the user. Keep detailed execution steps, commands, scripts, and full artifact text for execution unless they are themselves part of the required contract.

Use `brainstorming` for substantial uncertainty about goals or approach, or an explicit request to explore a design. Ask about significant choices affecting the result, scope, architecture, data, compatibility, risk, or substantial cost; do not introduce approval checkpoints for already-settled decisions.

Before approval, a specification document can be a separate reviewable artifact in an appropriate destination. Carry the agreed specification into the working context; for repository work, include it in the task branch rather than committing it to the default branch to obtain approval.

For repository work, inspect the existing code and configuration, prefer local patterns, and preserve the framework, toolchain, and conventions unless a migration is explicitly approved. Obtain approval for new dependencies, large refactors, exported API or documented endpoint changes, and migrations when not already covered by the request or agreed specification.

When adding or moving UI elements, show a compact ASCII layout before implementation. Keep supporting refactors within the touched area and agreed scope; do not add unrelated improvements or change the overall stack or testing architecture without an explicit request.

For global or live agent configuration, use `agent-config-in-dotfiles` and change the dotfiles source before syncing generated files.
