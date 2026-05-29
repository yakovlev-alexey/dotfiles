---
name: fullstack-contracts
description: Use when sharing frontend and backend TypeScript types, Zod schemas, API contracts, OpenAPI schemas, request or response models, generated clients, or package boundaries.
---

# Fullstack Contracts

## Overview

Keep shared frontend/backend code minimal. Share API contracts and types deliberately, vertically, and only at the boundary.

## Preferred Shape

```text
packages/
  types/
    src/
      slices/
        profile/
          profile-contracts.ts
          profile-schemas.ts
```

## Rules

- Shared types and contracts belong in `packages/types`.
- Shared contracts must be vertically sliced by product behavior.
- Do not create a broad shared domain package by default.
- Frontend code must not import backend implementation code directly.
- Use Zod at boundaries: request params/query/body, environment variables, and external service responses.
- Keep public API responses controlled by Zod schemas instead of leaking entire Prisma models.
- Generate or derive OpenAPI from route schemas when the project has tooling for it.
- Keep Prisma models and migrations central where Prisma requires them.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Frontend imports backend code directly | Share only vertical contracts/types from `packages/types` |
| Shared package grows into domain logic | Keep shared code to boundary contracts unless there is a concrete reason |
| API response leaks full Prisma model | Map through an explicit Zod response schema |
| Contract package is organized by technical type | Organize by product slice |

