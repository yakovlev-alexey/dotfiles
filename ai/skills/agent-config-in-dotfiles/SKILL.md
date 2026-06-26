---
name: agent-config-in-dotfiles
description: Use only when changing global or live agent configuration managed by the dotfiles repo, including MCP servers, skills, plugins, global AGENTS.md/instructions, Codex/Cursor/OpenCode/Claude settings, approval rules, or files under ~/.agents, ~/.codex, ~/.cursor, ~/.config/opencode, or similar agent config directories. Do not use for ordinary project-local AGENTS.md files unless the user is changing this dotfiles-managed instruction layer.
---

# Agent Config In Dotfiles

## Rule

Agent configuration must be changed through the dotfiles repository, not by editing live generated files directly.

Canonical repository:

```text
$HOME/Repos/dotfiles
```

If that path does not exist, check these fallbacks before editing live config:

```text
/Users/yakovlev-alex/Repos/dotfiles
/home/yakovlev-alex/Repos/dotfiles
```

## What Counts As Global Agent Configuration

Use this skill for changes to:

- MCP servers, MCP auth wiring, generated `mcp.json`, or Codex `mcp_servers`.
- Skills, external skill registries, local skill folders, skill projections, or skill installation scripts.
- Plugins, local plugin marketplaces, plugin manifests, or plugin installation scripts.
- Dotfiles-managed or live global `AGENTS.md` files, instruction files, global agent rules, and prompt/instruction layers.
- Do not use this skill for ordinary project-local `AGENTS.md` creation or edits unless the project is this dotfiles repo or the user explicitly wants to change global agent behavior.
- Codex, Cursor, OpenCode, Claude, or similar agent client config.
- Approval rules, sandbox rules, automation config, or agent tool/runtime settings.

## Workflow

1. Go to `$HOME/Repos/dotfiles`.
2. Edit the canonical source:
   - instructions: `ai/instructions/*.md`
   - generated `AGENTS.md`: run `./scripts/build-agents-md`
   - MCP: `ai/mcp.json`, then `./scripts/install-mcp`
   - dotfiles-owned skills: `ai/skills/<skill-name>/SKILL.md`, then `./scripts/install-skills`
   - public personal skills: `~/Repos/skills/<skill-name>/SKILL.md`, publish to the public skills repository, then `./scripts/install-skills`
   - external skills: `ai/skills.json`, then `./scripts/install-skills`
   - agent hooks: `ai/hooks/policies/guards/<hook-name>/`, then `./scripts/install-agent-hooks`
   - plugins: `ai/plugins/plugins.json`, then `./scripts/install-plugins`
   - Codex config template: `codex/*.template.toml`
   - OpenCode config template: `opencode/*.template.json`
3. Run validation:

```bash
./scripts/check
```

4. Review the diff:

```bash
git diff
git status --short
```

5. Commit and push the dotfiles change:

```bash
git add -A
git commit -m "Update agent configuration"
git push
```

## Adding Global Skills

Keep global skill installs reproducible through `ai/skills` and `ai/skills.json`; do not treat a direct install into `~/.codex/skills` or `~/.agents/skills` as complete.

Use `~/Repos/skills` for authoring public personal skills that should be maintained in the separate public skills repository. Keep skills that are specific to this dotfiles setup in `ai/skills`. Install public skills from the remote repository in `ai/skills.json`, not from a local checkout.

1. Verify the source and exact skill name first.
   - For OpenAI curated skills, use the skill-installer helper list.
   - For official third-party skills, prefer the upstream project repo that owns the tool.
   - Useful checks:

```bash
pnpx skills add https://github.com/<owner>/<repo> --list
gh api repos/<owner>/<repo>/contents/skills/<skill-name>/SKILL.md --jq '.html_url'
```

2. Add the registry entry:

```json
{
  "owner/public-skills-repo": "*",
  "owner/repo": "skill-name",
  "owner/monorepo": ["skill-a", "skill-b"],
  "/absolute/local/skills": "local-skill"
}
```

3. Sync and verify all projections:

```bash
./scripts/install-skills
test -f ~/.agents/skills/<skill-name>/SKILL.md
test -L ~/.codex/skills/<skill-name>
test -L ~/.cursor/skills/<skill-name>
./scripts/check
```

If `./scripts/install-skills` reports `staged skill not found`, the registry value probably does not match the source skill name; rerun the source check and correct `ai/skills.json`.

## Guardrails

- Do not commit secrets, tokens, auth files, sessions, history, caches, SQLite files, or generated runtime state.
- Do not edit generated live files as the source of truth. If a live file must be regenerated for local use, regenerate it from dotfiles scripts.
- If the requested change came from experimenting in a live agent UI, promote the final desired state back into dotfiles before considering the task complete.
- If there is no git remote yet, still commit locally and tell the user that push is blocked by missing remote.
