---
name: frontend-state-and-data
description: Use when handling frontend server state, async reads, mutations, cache invalidation, optimistic updates, UI filters, selected entities, drafts, wizard progress, Nano Stores, or TanStack Query.
---

# Frontend State And Data

## Overview

Keep most business logic on the backend. Frontend orchestration should submit intent, call the backend, update or invalidate server-state caches, and render results.

## Server State

Use TanStack Query for server state, async reads, mutations, cache invalidation, retries, background refresh, and optimistic cache updates when needed.

For writes, use `useMutation`; pass a slice command as `mutationFn`.

```ts
const saveProfileMutation = useMutation({
  mutationFn: saveProfileCommand,
  onSuccess: async () => {
    await queryClient.invalidateQueries({ queryKey: ["profile"] });
  },
});
```

## Frontend State

Use Nano Stores for frontend-specific shared state:

- UI filters
- selected entities
- drafts
- wizard progress
- Astro island state
- local collaboration flags
- derived client state not naturally owned by the backend

Suggest another state solution only with concrete motivation. Example: use Yjs or another CRDT-oriented tool for real-time collaborative document/data sync.

## Store File Roles

- `model` files hold Nano Store atoms/maps.
- Selectors derive data from state.
- Query files define TanStack Query options, keys, and request bindings.
- Command files provide mutation functions or frontend state changes.

Prefer small named files over repositories, service objects, or grouped store objects.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Server data copied into Nano Stores | Keep it in TanStack Query; let Nano Stores feed query keys or mutation inputs |
| Server writes bypass `useMutation` | Use `useMutation({ mutationFn: command })` |
| `store` becomes a repository object | Split into named query, command, selector, and model files |

For examples, read `references/query-nanostores-examples.md`.

