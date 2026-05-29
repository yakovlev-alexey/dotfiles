---
name: web-app-project-defaults
description: Use when creating a new TypeScript web app, greenfield full-stack app, monorepo scaffold, Astro site, React app, Vite app, Fastify API, Prisma service, or shadcn/ui project.
---

# Web App Project Defaults

## Overview

Use these defaults for new projects, fresh scaffolds, and explicit migrations. For existing projects, preserve established conventions unless the user asks to migrate.

## Defaults

- Use `pnpm` for package management.
- Use TypeScript for app code, config, tests, and scripts where supported.
- Use Astro for static or content-led sites.
- Use React for interactive apps, dashboards, editors, authenticated products, games, and stateful tools.
- Use Vite when the chosen framework does not already provide a build tool.
- Use shadcn/ui for UI atoms, preferably under `src/common/components/ui`.
- Use Node.js, Fastify, PostgreSQL, Prisma, OpenAPI, and Zod for backend services.
- Use Turborepo for new full-stack web app projects.

## Greenfield Shape

```text
apps/
  web/
  api/
packages/
  types/
```

Shared frontend/backend contracts belong in `packages/types`; keep them vertically sliced by product behavior.

## Setup Notes

- Install and configure shadcn/ui with the current official command, usually `pnpm dlx shadcn@latest`.
- Configure one TanStack Query client for React apps that use server state, usually in `src/common/query-client.ts`.
- Configure path aliases for `src/`, `src/common`, and concrete slice files when the project already uses aliases or the setup benefits from them.
- Add static, integration, and E2E test scripts appropriate to the app.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Applying these defaults to an existing project | Preserve existing conventions unless migration is requested |
| Creating a broad shared domain package | Keep shared contracts in vertical `packages/types` slices |
| Using custom route parsing in a normal React app | Use React Router or another established routing library |

