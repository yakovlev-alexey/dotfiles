---
name: web-app-design
description: Use when deciding which TypeScript web app architecture guidance applies, especially for Astro, React, Vite, shadcn/ui, Fastify, Prisma, Zod, TanStack Query, Nano Stores, vertical slices, contracts, or test strategy.
---

# Web App Design

## Overview

Use this as the user's TypeScript web app architecture guide. Prefer vertical product slices, small named files, page-owned layout, focused widgets, clean backend layers, minimal shared contracts, and Testing Trophy coverage.

## Existing Projects First

For existing projects, preserve the project's established framework, package manager, test runner, routing, styling system, and folder conventions unless the user asks for migration. Apply these rules incrementally around touched files.

Use greenfield defaults only for new apps, fresh scaffolds, or explicit migrations.

## Dispatch

| Situation | Use |
| --- | --- |
| New app, scaffold, monorepo, package defaults | `web-app-project-defaults` |
| Frontend folders, slices, imports, exports, shared code | `frontend-slice-architecture` |
| React pages, widgets, components, layout CSS, Storybook states | `react-page-widget-composition` |
| Frontend server state, UI state, filters, drafts, mutations | `frontend-state-and-data` |
| Node/Fastify/Prisma backend slices, endpoints, usecases, transactions | `backend-slice-architecture` |
| Shared frontend/backend schemas, API contracts, OpenAPI boundaries | `fullstack-contracts` |
| Static, integration, E2E, and unit test balance | `web-app-testing` |

## Core Rules

- Organize by vertical product behavior: `landing`, `profile`, `settings`, `checkout`, `budget-plan`, `user-dashboard`.
- Use `common/` only for real reuse or intentionally imminent reuse.
- Discourage imports between slices; when unavoidable, import the smallest concrete file.
- Do not create or rely on `index.ts`, `index.tsx`, or barrel files.
- Keep frontend/backend sharing minimal and vertical.
- Do not let greenfield stack preferences override an existing project's working conventions.

## Verification Scenarios

Before deployment, pressure-test agents against these scenarios:

- Existing Vite app using npm: agent must not convert package manager or scaffold Turborepo.
- Feature touching one product area: agent must identify the owning slice before adding files.
- Cross-slice reuse temptation: agent must avoid broad `common/` or barrel extraction.

