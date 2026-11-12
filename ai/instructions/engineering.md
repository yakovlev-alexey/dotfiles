# Engineering Workflow

Read existing code and configuration before changing anything. Prefer local project patterns over new abstractions.

For global or live agent configuration, including global skills, use the `agent-config-in-dotfiles` skill and change the dotfiles source of truth before syncing generated files.

Make reasonable small changes directly within the user's authorized scope. For large, risky, or ambiguous work, propose a short plan first. Use `brainstorming` for substantial design uncertainty or an explicit request to explore a design; do not turn a clear, bounded implementation request into another approval cycle.

When a plan includes adding new UI elements or moving existing UI elements, include a compact ASCII layout sketch showing the intended interface structure before implementation.

Ask before adding new dependencies, doing large refactors, changing exported package APIs, changing documented endpoints, or creating database migrations.

Bring the touched area to a good state. Mention nearby problems when relevant, but do not fix neighboring areas without being asked.

Do supporting refactors inside the touched area when they improve ownership, decomposition, or clarity. Do not change the overall stack, testing architecture, or high-level architecture without an explicit request.
