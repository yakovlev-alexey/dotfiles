# Version Control and Worktrees

Work carefully with dirty worktrees. Do not revert user changes. If task changes require editing files with existing user edits, work with those edits.

Read-only investigation can use the available checkout. Before changing code, use a separate task worktree by default: Git worktree for Git repositories, `arc-wt` for Arcadia. Reuse a suitable existing task worktree; otherwise create one from the agreed base. Preserve the source checkout and its unrelated changes. For documentation and configuration changes, use a suitable checkout without requiring a new worktree solely for the workflow.

Use the `arc` skill for Arcadia VCS operations and `arc-wt` for its worktree lifecycle. Follow repository conventions for branches and PRs.

An implementation request for repository changes authorizes a task branch, task-scoped commits, pushing that branch, and creating or updating a draft PR by default. Publish only the requested changes and their approved prerequisites. Inspect the diff against the target branch before pushing; exclude unrelated commits as well as unrelated working-tree changes. Read-only research and consultation do not require a PR.

Update an existing draft PR for the task instead of creating a duplicate. Link the specification or summarize the agreed result and important decisions, include evidence for the acceptance criteria, and identify failed or unavailable checks. If access or repository configuration blocks publication, report the concrete blocker and deliver the prepared changes and evidence.

Merging, publishing to the default branch, and force-pushing require separate explicit authorization. Stage only task-owned files or hunks, review the staged diff, and preserve unrelated staged changes. Never include secrets, credentials, sessions, caches, or unrelated runtime state in commits, PRs, or evidence.

For `arc`, branch names should use the ticket key. Commit messages must start with the ticket key and be in Russian past tense, for example: `PRACTICUM-123: исправлена обработка ошибки`.

For Git, commit messages must be short imperative English.
