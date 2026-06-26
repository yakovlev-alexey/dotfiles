# Dotfiles Skills

Skills in this directory are part of this dotfiles setup but do not belong in the
public skills repository.

Use one directory per skill:

```text
ai/skills/<skill-name>/SKILL.md
```

Public skills are installed from the remote skills repository through `ai/skills.json`.
Dotfiles-owned skills are copied from this directory by `./scripts/install-skills`.

Do not store secrets, tokens, credentials, private keys, runtime state, or local
caches in skills.
