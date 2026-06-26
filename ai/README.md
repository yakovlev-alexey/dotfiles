# AI config layer

`ai/` is the canonical layer for instructions, skills, plugins, and MCP.

- `instructions/*.md` are linked into `~/.agents/instructions`.
- `scripts/build-agents-md` generates inline `AGENTS.md` files for `~/.agents`, Codex, and OpenCode, plus an always-on Cursor `.mdc` rule.
- `hooks/policies/guards/*` are rendered by `scripts/install-agent-hooks` into native Cursor, Codex, Claude Code, and OpenCode hooks.
- `skills/*` and `skills.json` are assembled into `~/.agents/skills`.
- Public personal skills are installed from the remote skills repository through `skills.json`.
- `plugins/plugins.json` is reserved for the local Codex marketplace.
- `mcp.json` generates live configs for Cursor, OpenCode, and Codex.

Live configs in the home directory are not edited manually; they are rebuilt through `./scripts/install-mcp` and `./scripts/install-agent-hooks`.
