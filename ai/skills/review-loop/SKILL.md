---
name: review-loop
description: "Используй только по явному запросу пользователя запустить review-loop или по вызову $review-loop; мануальный цикл независимого ревью текущего изменения."
---

# review-loop

Точка входа мануального пресета `crowdtech/review-loop-manual` для Codex.

Прочитай и выполни инструкции общего скилла:

`/Users/yakovlev-alex/arcadia/crowdsourcing/ai/presets/review-loop/skills/review-loop-orchestrator/SKILL.md`

Этот каталог — `<SKILL_ROOT>` для инструкций оркестратора. Шаблоны ревьюеров
лежат в `prompts/clean-slate.md` и `prompts/validator.md`, журнал ведёт
`scripts/ledger.py` из того же каталога.

Аргументы вызова задают параметры цикла, как в исходной команде
`/Users/yakovlev-alex/arcadia/crowdsourcing/ai/presets/review-loop/commands/review-loop.md`:

- `$review-loop` — максимум 3 раунда, один независимый ревьюер `clean-slate` на раунд.
- `$review-loop 5 раундов` — другой лимит, фиксируемый при первой передаче диффа.
- `$review-loop 3 раунда, 4 ревьюера: архитектура, безопасность, QA, производительность` — несколько ревьюеров, отдельный subagent и запись для каждого.

Если общий скилл отсутствует, остановись и сообщи, что рабочая копия Аркадии
неполна или скилл перемещён.
