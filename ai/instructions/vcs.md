# Version Control

Work carefully with dirty worktrees. Do not revert user changes. If task changes require editing files with existing user edits, work with those edits.

In Git repositories, the agent may create a worktree if no task branch exists and may commit completed work. Do not push or open PRs unless explicitly asked.

In Arcadia or `arc` repositories, use the `arc` skill for all VCS actions. If work is not already on a task branch, create a branch from `trunk` before changing files. Commit completed work, but do not push or open PRs unless explicitly asked.

For `arc`, branch names should use the ticket key. Commit messages must start with the ticket key and be in Russian past tense, for example: `PRACTICUM-123: исправлена обработка ошибки`.

For Git, commit messages must be short imperative English.
