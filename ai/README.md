# AI config layer

`ai/` is the canonical layer for instructions, skills, plugins, and MCP.

- `instructions/*.md` are linked into `~/.agents/instructions`.
- `scripts/build-agents-md` generates inline `AGENTS.md` files for `~/.agents`, Codex, and OpenCode, plus an always-on Cursor `.mdc` rule.
- `hooks/policies/guards/*` are rendered by `scripts/install-agent-hooks` into native Cursor, Codex, Claude Code, and OpenCode hooks.
- `skills/*` and `skills.json` are assembled into `~/.agents/skills`.
- Public personal skills are installed from the remote skills repository through `skills.json`.
- `plugins/plugins.json` is reserved for the local Codex marketplace.
- `mcp.json` generates live configs for Cursor, OpenCode, Codex, and Claude Code.
- `telegram-mcp.ref` pins [chigwell/telegram-mcp](https://github.com/chigwell/telegram-mcp) for `./scripts/install-telegram-mcp`.

Live configs in the home directory are not edited manually; they are rebuilt through `./scripts/install-mcp` and `./scripts/install-agent-hooks`.

## Telegram MCP (read-only)

Uses [chigwell/telegram-mcp](https://github.com/chigwell/telegram-mcp) with `TELEGRAM_EXPOSED_TOOLS=read-only` — search and read only, no send/edit/delete.

Setup:

```bash
./scripts/install-uv                               # Homebrew on macOS, installer on WSL/Linux
./scripts/install-telegram-mcp                     # uv tool install from pinned git tag
./scripts/mcp/telegram-generate-session --qr       # one-time; save output
./scripts/personal set TELEGRAM_API_ID
./scripts/personal set TELEGRAM_API_HASH
./scripts/personal set TELEGRAM_SESSION_STRING
./scripts/install-mcp
```

Do not install the PyPI package `telegram-mcp`; it is unrelated to chigwell's project.

