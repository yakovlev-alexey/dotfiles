---
name: react-page-widget-composition
description: Use when building or refactoring React pages, route targets, widgets, presentational components, widget nesting, page-owned layout, colocated CSS, render props, or Storybook states.
---

# React Page Widget Composition

## Overview

Pages compose workflows and own layout. Widgets connect state or behavior to stateless UI. Components stay presentational by default.

## Composition Rules

- Keep routing at the app/root boundary. `App.tsx` may own route setup, app-level providers, loading state, and route-to-page wiring.
- Pages are route targets and workflow composers; pages must not import or render other pages.
- Pages may connect to stores, queries, commands, and selectors when the page owns the workflow.
- Components receive data, callbacks, and positioning class names through props. They should not own business state.
- Widgets may read state, call queries/commands, bind events, and compose stateless components.
- Widgets must not import or render other widgets. Use `children` or named slots, then compose widgets on the page.
- Split widgets that own multiple workflows.

## Widget-Owned UI

If a presentational component exists only for one controlling widget, keep it inside the widget folder:

```text
widgets/
  profile-stats/
    profile-stats.tsx
    profile-stats.css
    profile-stats.widget.tsx
    profile-stats.widget.stories.tsx
```

Do not duplicate the same UI under both `components/` and `widgets/`.

## CSS Ownership

- `src/styles.css`: global design tokens, reset/base elements, and truly global utilities only.
- `src/App.tsx`: imports `styles.css` directly.
- Page CSS: page-owned layout and placement.
- Component or widget CSS: classes rendered by that component or widget.

Use basic BEM-style classes such as `month-details`, `month-details__label`, and simple modifier classes for real state or variants.

## Storybook

Create stories for standalone components and widgets when Storybook already exists, when building a component library/design system, or when the user asks for Storybook. Showcase meaningful states: empty, loading, error, disabled, long-content, and happy path.

For complete examples, read `references/react-slice-examples.md`.

