# AI config layer

`ai/` — канонический слой для инструкций, skills, plugins и MCP.

- `instructions/*.md` линкуются в `~/.agents/instructions`.
- `scripts/build-agents-md` генерирует inline `AGENTS.md` для `~/.agents`, Codex, Cursor и OpenCode.
- `skills/*` и `skills/skills.json` собираются в `~/.agents/skills`.
- `plugins/plugins.json` зарезервирован под local Codex marketplace.
- `mcp.json` генерирует live-конфиги Cursor, OpenCode и Codex.

Live-конфиги в home не редактируются вручную, а пересобираются через `./scripts/install-mcp`.
