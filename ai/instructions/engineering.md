# Engineering Workflow

Read existing code and configuration before changing anything. Prefer local project patterns over new abstractions. Preserve the project's framework, toolchain, and conventions unless a migration is explicitly approved.

For global or live agent configuration, including global skills, use the `agent-config-in-dotfiles` skill and change the dotfiles source of truth before syncing generated files.

For implementation requests, investigate the request, specify the intended result at an appropriate level, resolve significant decisions, implement in the task's checkout, verify the result, and deliver a draft PR with evidence for repository changes. Research and design-only requests end with findings or a reviewable specification; implementation and publication require an implementation request or separate authorization.

Scale the specification to uncertainty and risk:

- For small, clear, low-risk changes, decide directly or describe the result and acceptance check in a few sentences.
- For moderately complex work, present a short specification in chat.
- For complex work involving interacting components or significant risks, create a specification document in the project's established format.

A specification describes the intended result, scope and constraints, the overall solution and consequential decisions, and observable acceptance criteria. Record material choices made by the agent as well as choices agreed with the user. Keep detailed execution steps, commands, scripts, and full artifact text for implementation unless they are themselves part of the required external contract.

Use `brainstorming` for substantial design uncertainty or an explicit request to explore a design. Ask the user to resolve significant open decisions that affect the result, scope, architecture, data, compatibility, risk, or substantial cost. Continue directly when those choices are already settled; do not require a separate approval for predictable implementation details.

Before approval, a specification document may be prepared as a separate reviewable artifact outside the source checkout. Once the significant choices are settled, carry it into the task branch with the implementation. Do not commit a specification to the default branch merely to obtain design approval.

When a plan includes adding new UI elements or moving existing UI elements, include a compact ASCII layout sketch showing the intended interface structure before implementation.

Obtain approval before adding new dependencies, doing large refactors, changing exported package APIs or documented endpoints, or creating database migrations when these decisions are not already covered by the user's request or the agreed specification.

Bring the touched area to a good state. Mention nearby problems when relevant, but do not fix neighboring areas without being asked.

Do supporting refactors inside the touched area when they improve ownership, decomposition, or clarity. Do not change the overall stack, testing architecture, or high-level architecture without an explicit request.
