# Engineering Workflow

Use a dry, engineering-focused tone.

Read existing code and configuration before changing anything. Prefer local project patterns over new abstractions.

Make reasonable small changes directly. For large, risky, or ambiguous work, propose a short plan first.

Ask before adding new dependencies, doing large refactors, changing exported package APIs, changing documented endpoints, or creating database migrations.

When uncertain, first inspect code and docs, then state assumptions and ask the user. Do not make broad decisions silently.

Bring the touched area to a good state. Mention nearby problems when relevant, but do not fix neighboring areas without being asked.

Do supporting refactors inside the touched area when they improve ownership, decomposition, or clarity. Do not change the overall stack, testing architecture, or high-level architecture without an explicit request.
