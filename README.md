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
chsh -s "$(command -v zsh)"
```

## Managed

- shell: `zsh`, fallback `bash`, shared aliases/functions;
- prompt: Starship with managed `~/.config/starship.toml`;
- Git: shared `.gitconfig` plus generated `~/.gitconfig.local` from `scripts/personal`;
- Codex/Cursor/OpenCode skills through the shared `~/.agents/skills` layer;
- MCP registry from `ai/mcp.json`, with generated client-specific configs;
- `AGENTS.md` for agent directories is generated from `ai/instructions/*.md`;
- Homebrew inventory for macOS.
- WSL package bootstrap with Ubuntu/Debian analogs for the Homebrew inventory, plus `nvm`, LTS Node.js, `pnpm`, and Starship;
- Windows agent projection from WSL into the Windows user profile for `AGENTS.md`, skills, and local plugin metadata.

## Not Managed

Secrets, tokens, history, sessions, sqlite files, IDE extensions, app caches, `node_modules`, `~/.ssh` private keys, `.arc`/`.ya` runtime state, Codex worktrees, and runtime/cache directories are not committed or linked.

## Common Commands

```bash
./install --profile macos
./install --sync-only
./scripts/build-agents-md
./scripts/install-skills
./scripts/install-mcp
./scripts/install-wsl-packages
bash ./scripts/install-windows-agent-projection
./scripts/install-git-hooks
./scripts/check
./scripts/check-links
```

If the repository was cloned without submodules, initialize them before installing skills:

```bash
git submodule update --init --recursive
```

`./install` installs repository git hooks and runs `./scripts/check-links` after a normal installation. `./install --check` runs both repository static checks and live symlink checks. Git hooks rerun the link check after pull/merge or branch checkout when managed link sources have changed.

## Adding a New MCP

1. Add the server to `ai/mcp.json`.
2. If secrets are required, add the variable name to `personal.required`.
3. Run `./scripts/install-mcp`.
4. Verify with `./scripts/check`.

## Adding a New Skill

Use dotfiles as the source of truth; do not install directly into `~/.codex/skills` as the only change.

- public local skill: place it in the `ai/skills` submodule as `<name>/SKILL.md`;
- external/local source: add an entry to `ai/skills.json`;
- official third-party skill: prefer the upstream project repo that owns the tool, then add `"<owner>/<repo>": "<skill-name>"` to `ai/skills.json`.

For external skills, first verify the exact skill name and path. Good checks:

```bash
npx skills add https://github.com/<owner>/<repo> --list
gh api repos/<owner>/<repo>/contents/skills/<skill-name>/SKILL.md --jq '.html_url'
```

Registry examples:

```json
{
  "owner/repo": "skill-name",
  "owner/monorepo": ["skill-a", "skill-b"],
  "/absolute/local/skills": "local-skill"
}
```

Then:

```bash
./scripts/install-skills
test -f ~/.agents/skills/<skill-name>/SKILL.md
test -L ~/.codex/skills/<skill-name>
test -L ~/.cursor/skills/<skill-name>
./scripts/check
```

## AGENTS.md

`AGENTS.md` is not stored separately for Codex. The canonical source is `ai/instructions/*.md`. The `./scripts/build-agents-md` script builds an inline `AGENTS.md` with the contents of all instruction files and places it in `~/.agents/AGENTS.md`, `~/.codex/AGENTS.md`, `~/.cursor/AGENTS.md`, and `~/.config/opencode/AGENTS.md`.

## Windows Agents From WSL

On WSL, `./install --profile wsl` also runs `bash ./scripts/install-windows-agent-projection` when Windows interop is available. This copies generated agent runtime files into the Windows user profile:

```text
C:\Users\<you>\.agents
C:\Users\<you>\.codex
C:\Users\<you>\.cursor
C:\Users\<you>\.config\opencode
```

The projection copies `AGENTS.md`, skills, and local plugin metadata. It deliberately does not copy generated MCP/client config files because WSL configs can contain Linux commands and paths that are not valid for Windows-native agent processes.

For Codex Desktop on Windows, configure the app itself to run the agent in WSL: Settings -> Agent -> WSL, then restart the app. The integrated terminal is configured separately; choose WSL there too if you want new terminal sessions to open in Ubuntu. If multiple WSL distributions are installed, make Ubuntu the default from PowerShell:

```powershell
wsl -l -v
wsl --set-default Ubuntu
```

If Windows Terminal opens Ubuntu with `bash`, change the Ubuntu login shell from an interactive Ubuntu terminal:

```bash
chsh -s "$(command -v zsh)"
```

Then restart the distribution from PowerShell:

```powershell
wsl --terminate Ubuntu
```
