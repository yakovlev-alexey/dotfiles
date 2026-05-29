# Industry Grounding

Read this when deciding how strictly to apply `web-app-design` guidance or when explaining why the rules exist.

## Sources To Prefer

- Feature-Sliced Design docs: vertical product slices, slice isolation, and grouping modules by business/product meaning.
- Clean Coder "Screaming Architecture": naming architecture after the application domain instead of framework mechanics.
- React docs: composition with `children`, controlled components, lifting state up, and explicit state ownership.
- Astro docs: choosing Astro for mostly static pages with isolated interactive islands.
- TanStack Query docs: server state, async data, cache invalidation, and mutation behavior.
- Nano Stores docs: small frontend-specific shared state and Astro island state.
- Testing Trophy: static checks plus many integration/E2E tests and few targeted unit tests.
- Fastify, Prisma, Zod, and Turborepo docs for current setup details.

## Practical Mapping

The preferred `src/slices/<slice>/<segment>` structure is FSD-inspired but intentionally simpler than canonical FSD layers. Do not force canonical `pages/widgets/features/entities/shared` top-level layers unless an existing project already uses them.

Map common FSD concepts like this:

- FSD slices -> `src/slices/<product-area>`
- FSD shared -> `src/common`
- FSD `ui` segment -> `components`, `pages`, and `widgets`
- FSD `model` segment -> `store`
- FSD `lib` segment -> `utils`
- FSD public API -> useful contrast, but this design forbids `index` files and barrel files

## Reference Links

- Feature-Sliced Design overview: https://feature-sliced.github.io/documentation/docs/get-started/overview
- Feature-Sliced Design slices and segments: https://feature-sliced.github.io/documentation/docs/reference/slices-segments
- Screaming Architecture: https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html
- React passing JSX as children: https://react.dev/learn/passing-props-to-a-component
- React sharing state between components: https://react.dev/learn/sharing-state-between-components
- Astro islands architecture: https://docs.astro.build/en/concepts/islands/
- TanStack Query overview: https://tanstack.com/query/latest
- Nano Stores: https://github.com/nanostores/nanostores
- Testing Trophy: https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- Fastify TypeScript: https://fastify.dev/docs/latest/Reference/TypeScript/
- Prisma PostgreSQL quickstart: https://docs.prisma.io/docs/prisma-orm/quickstart/postgresql
- Zod: https://zod.dev/
- Turborepo docs: https://turborepo.com/repo/docs

