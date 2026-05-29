---
name: web-app-testing
description: Use when choosing test coverage for TypeScript web apps, React workflows, backend slices, static checks, integration tests, E2E tests, unit tests, Storybook states, or Testing Trophy tradeoffs.
---

# Web App Testing

## Overview

Follow the Testing Trophy / Testing Cup preference: strong static checks, many integration and E2E tests for user-facing behavior, and focused unit tests for dense pure logic.

## Preference Order

- Maintain strong static checks: TypeScript, linting, formatting, schema checks, and build checks.
- Prefer integration and E2E tests for user-facing behavior and cross-slice workflows.
- Write focused unit tests for dense pure logic, fragile transformations, or edge-heavy utilities.
- Avoid large volumes of shallow component unit tests that duplicate implementation details.

## Frontend Guidance

Use E2E or integration tests for real workflows: routing, forms, mutations, cache invalidation, error states, and cross-component behavior.

Use Storybook state coverage when Storybook already exists, when building a component library/design system, or when the user asks for Storybook.

## Backend Guidance

Use integration tests for endpoint contracts, auth behavior, validation, usecase composition, database reads/writes, and transaction behavior.

Use unit tests for domain functions with dense rules or edge-heavy transformations.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Unit-test-heavy coverage | Prefer static checks plus integration/E2E coverage |
| Testing implementation details of presentational components | Test user-visible behavior or Storybook states |
| Skipping schema validation in tests | Exercise Zod request/response boundaries |
| Only testing pure functions while workflows break | Add integration or E2E coverage for the workflow |

