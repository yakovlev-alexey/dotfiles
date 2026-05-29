# CLI Tools

Prefer modern project-aware tools over default legacy commands.

| Instead of | Prefer | Why |
| --- | --- | --- |
| `grep` | `rg` or `ugrep` | Fast recursive search, ignore support, useful filtering. |
| `find` | `rg --files` or `fd` | Fast file listing, extension filters, safer execution. |
| `ls` | `eza` when available | Better tree, git, and metadata output. |
| `cat` for code | `bat` when available | Syntax highlighting and line numbers. |
| `sed` for simple replace | `sd` when available | Simpler literal replacements and safer previews. |
| JSON parsing with shell text tools | `jq` | Structured JSON reads and transforms. |
| YAML/TOML/XML/CSV ad hoc parsing | `yq` | Structured multi-format reads and transforms. |
| GitHub web fetches | `gh` when authenticated | API access for PRs, issues, files, and metadata. |
| `npm` | `pnpm` | Default package manager when no lockfile decides otherwise. |

For JS/TS package management, follow the existing lockfile. If no lockfile exists, use `pnpm`.

Avoid slow recursive commands when a fast project-aware alternative exists.

In non-interactive shells, avoid commands that wait for input. Disable pagers or use non-interactive flags where needed.
