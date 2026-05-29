# dotfiles

Персональные dotfiles для macOS и WSL. Репозиторий является source of truth, live-конфиги в домашнем каталоге считаются generated/runtime слоем.

## Быстрый старт

```bash
git clone --recursive <repo-url> ~/Repos/dotfiles
cd ~/Repos/dotfiles
./scripts/personal setup
./install --profile macos
```

Для WSL:

```bash
git clone --recursive <repo-url> ~/Repos/dotfiles
cd ~/Repos/dotfiles
PERSONAL_BACKEND=file ./scripts/personal setup
./install --profile wsl
```

## Что управляется

- shell: `zsh`, fallback `bash`, общие aliases/functions;
- Git: общий `.gitconfig` + generated `~/.gitconfig.local` из `scripts/personal`;
- Codex/Cursor/OpenCode skills через общий слой `~/.agents/skills`;
- MCP registry из `ai/mcp.json` с генерацией client-specific конфигов;
- `AGENTS.md` для agent-директорий генерируется из `ai/instructions/*.md`;
- Homebrew inventory для macOS.

## Что не управляется

Не коммитятся и не линкуются секреты, токены, history, sessions, sqlite, IDE extensions, app caches, `node_modules`, `~/.ssh` private keys, `.arc`/`.ya` runtime state, Codex worktrees и runtime/cache директории.

## Частые команды

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

`./install` устанавливает git hooks репозитория и запускает
`./scripts/check-links` после обычной установки. `./install --check` запускает и
статические проверки репозитория, и проверку live symlink-ов. Git hooks повторно
запускают проверку ссылок после pull/merge или checkout ветки, если менялись
управляемые источники ссылок.

## Добавление нового MCP

1. Добавить сервер в `ai/mcp.json`.
2. Если нужны секреты, добавить имя переменной в `personal.required`.
3. Запустить `./scripts/install-mcp`.
4. Проверить `./scripts/check`.

## Добавление нового skill

- локальный skill: положить в `ai/skills/<name>/SKILL.md`;
- внешний/local source: добавить запись в `ai/skills/skills.json`.

Затем:

```bash
./scripts/install-skills
```

## AGENTS.md

`AGENTS.md` не хранится отдельно для Codex. Канон — `ai/instructions/*.md`. Скрипт `./scripts/build-agents-md` собирает inline `AGENTS.md` с содержимым всех instruction-файлов и раскладывает его в `~/.agents/AGENTS.md`, `~/.codex/AGENTS.md`, `~/.cursor/AGENTS.md` и `~/.config/opencode/AGENTS.md`.
