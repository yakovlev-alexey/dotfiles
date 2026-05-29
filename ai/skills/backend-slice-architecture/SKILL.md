---
name: backend-slice-architecture
description: Use when building or refactoring Node.js, Fastify, PostgreSQL, Prisma, Zod, OpenAPI, backend vertical slices, endpoints, usecases, commands, queries, domain rules, or transactions.
---

# Backend Slice Architecture

## Overview

Structure backend code by vertical product slices and pragmatic clean architecture layers. Use screaming architecture names first, then layer names inside each slice.

## Preferred Shape

```text
apps/api/src/
  slices/
    profile/
      domain/
      usecases/
      commands/
      queries/
      endpoints/
      plugins/
      schemas/
```

## Flow

```text
endpoint -> usecase -> commands / queries -> Prisma
                  -> domain rules
```

## Layer Rules

- `domain`: reusable business rules, policies, assertions, calculations, and normalizers. Domain may use Prisma generated types as data shapes, but must not access Prisma Client, Fastify, HTTP, environment, or external services.
- `usecases`: one business operation per file. Usecases compose domain rules plus commands and queries. Usecases should not call Prisma directly except to open a transaction boundary.
- `commands`: one write operation per file. Commands hide Prisma mutations and may accept an optional Prisma transaction client.
- `queries`: one read operation per file. Queries hide Prisma reads and may accept an optional Prisma transaction client.
- `endpoints`: one Fastify route per file. Endpoints own HTTP contract, auth hooks, request parsing, status codes, and response mapping.
- `plugins`: slice-level Fastify plugin files that register endpoint files.
- `schemas`: one Zod schema or tightly coupled schema group per file.

Commands and queries must not call each other. Usecases compose them. Transactions are opened in usecases when a business operation needs atomicity.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Backend slice starts with top-level `controllers/`, `services/`, `repositories/` | Put those concerns inside product slices and clean layers |
| Usecase calls Prisma for normal reads/writes | Move Prisma access into commands and queries |
| Command calls query or query calls command | Compose them in the usecase |
| Domain object class mirrors Prisma model | Use Prisma generated types internally; put reusable rules in domain functions |

For complete examples, read `references/backend-slice-examples.md`.

