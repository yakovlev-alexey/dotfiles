# dotfiles

Personal dotfiles for macOS and WSL. This repository is the source of truth; live configs in the home directory are treated as the generated/runtime layer.

## Quick Start

```bash
git clone --recursive <repo-url> ~/Repos/dotfiles
cd ~/Repos/dotfiles
./scripts/personal setup
./install --profile macos
```

For WSL:

```bash
git clone --recursive <repo-url> ~/Repos/dotfiles
cd ~/Repos/dotfiles
PERSONAL_BACKEND=file ./scripts/personal setup
./install --profile wsl
```

## Managed

- shell: `zsh`, fallback `bash`, shared aliases/functions;
- Git: shared `.gitconfig` plus generated `~/.gitconfig.local` from `scripts/personal`;
- Codex/Cursor/OpenCode skills through the shared `~/.agents/skills` layer;
- MCP registry from `ai/mcp.json`, with generated client-specific configs;
- `AGENTS.md` for agent directories is generated from `ai/instructions/*.md`;
- Homebrew inventory for macOS.

## Not Managed

Secrets, tokens, history, sessions, sqlite files, IDE extensions, app caches, `node_modules`, `~/.ssh` private keys, `.arc`/`.ya` runtime state, Codex worktrees, and runtime/cache directories are not committed or linked.

## Common Commands

```bash
./install --profile macos
./install --sync-only
./scripts/build-agents-md
./scripts/install-skills
./scripts/install-mcp
./scripts/install-git-hooks
./scripts/check
./scripts/check-links
```

`./install` installs repository git hooks and runs `./scripts/check-links` after a normal installation. `./install --check` runs both repository static checks and live symlink checks. Git hooks rerun the link check after pull/merge or branch checkout when managed link sources have changed.

## Adding a New MCP

1. Add the server to `ai/mcp.json`.
2. If secrets are required, add the variable name to `personal.required`.
3. Run `./scripts/install-mcp`.
4. Verify with `./scripts/check`.

## Adding a New Skill

- local skill: place it in `ai/skills/<name>/SKILL.md`;
- external/local source: add an entry to `ai/skills/skills.json`.

Then:

```bash
./scripts/install-skills
```

## AGENTS.md

`AGENTS.md` is not stored separately for Codex. The canonical source is `ai/instructions/*.md`. The `./scripts/build-agents-md` script builds an inline `AGENTS.md` with the contents of all instruction files and places it in `~/.agents/AGENTS.md`, `~/.codex/AGENTS.md`, `~/.cursor/AGENTS.md`, and `~/.config/opencode/AGENTS.md`.
