---
name: frontend-slice-architecture
description: Use when organizing TypeScript frontend files, vertical product slices, common shared code, imports, exports, file names, folders, barrels, or frontend package boundaries.
---

# Frontend Slice Architecture

## Overview

Organize frontend code by vertical product behavior. Folder names should reveal what the user can do: `landing`, `profile`, `settings`, `checkout`, `budget-plan`, `user-dashboard`.

## Preferred Shape

```text
src/
  App.tsx
  styles.css
  slices/
    profile/
      components/
      pages/
      widgets/
      store/
        model/
        selectors/
        queries/
        commands/
      utils/
      constants/
  common/
    components/
      ui/
    utils/
```

Allowed slice segments are `components`, `pages`, `widgets`, `store`, `utils`, and `constants`. Add another only when the product purpose is obvious.

## File Rules

- Keep one entity per file: one component, widget, page, story, selector, query, command, store, helper, or conceptual constants group.
- Create separate folders only for `components`, `pages`, and `widgets`.
- Put `utils`, `commands`, `selectors`, `queries`, `constants`, and model files directly inside their segment folders.
- Name folders and files in lowercase kebab-case.
- Always use named exports. Storybook CSF files may default-export their `meta` object.
- Never create or rely on `index.ts`, `index.tsx`, or barrel files.

## Reuse Rules

Use `common/` only for code already reused by multiple slices or intentionally designed for imminent reuse. Discourage imports between slices. If cross-slice reuse is unavoidable, import the smallest concrete named file.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Broad `common/` extraction | Keep code slice-local until reuse is real or imminent |
| Barrel files for convenience | Import concrete files directly |
| `common/query-client/query-client.ts` style folders | Use `common/query-client.ts` for non-component files |
| One-file folders for utilities or stores | Put non-component files directly in their segment |

