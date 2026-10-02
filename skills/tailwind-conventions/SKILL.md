---
name: tailwind-conventions
description: "Use when writing or reviewing Tailwind CSS v4 utility markup or its CSS configuration: class detection and dynamic class names, theme variables, directives and custom utilities, reuse without duplication, dark mode, variants and breakpoints, and the v3 to v4 traps."
paths: "**/*.css, **/*.html, **/*.vue, **/*.svelte, **/*.tsx, **/*.jsx, **/*.astro, **/*.blade.php"
---

# tailwind-conventions

Step 6 of the pipeline (`WORKFLOW.md`), next to `skills/responsive-layout` (breakpoints, fluid sizing, layers,
specificity: the geometry and the stylesheet organisation) and `skills/accessibility` (contrast, focus, motion).
This block owns what is specific to the utility framework: how it finds classes, how its design tokens work, and
what it takes to write markup that survives a refactor. **Status: a base to confront with real work**, no in-house
project behind it yet (same status as `go-conventions`). Pinned to **Tailwind CSS 4.3** (read 2026-10-02,
`references/origin.md`); a project on v3 uses a JavaScript configuration file and several of the rules below
describe what it must change when it moves.

## When
As soon as a utility class list, a Tailwind stylesheet (`@import "tailwindcss"`, `@theme`, `@utility`,
`@apply`) or the build wiring for it is written or modified, during `code` (6).

## Steps

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Class detection, dynamic names, reuse and conflicts | a class name is built in code, a class list is repeated, or a component accepts extra classes | [`01-detection-reuse-conflicts.md`](./references/01-detection-reuse-conflicts.md) |
| 2 | Theme variables, directives, custom CSS, variants, dark mode | a token, a custom utility or variant, a dark theme or a stylesheet directive is written | [`02-theme-directives-variants.md`](./references/02-theme-directives-variants.md) |
| 3 | Build wiring and the v3 to v4 traps | the build is set up, a project upgrades, or v3 idioms appear in a v4 project | [`03-build-and-upgrade.md`](./references/03-build-and-upgrade.md) |

## Output / checkpoint
Markup and stylesheet compliant with the sections the change touched, built without a warning and compared
visually at the project's breakpoints and in each theme. No dedicated checkpoint: `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never an install: name the package, the person runs `pnpm add -D <package>`
(`CONVENTIONS.md`). Never build a class name by concatenation. Never fight the framework with `!important` or
a parallel stylesheet before checking that a theme variable, a variant or an `@utility` expresses the need. Do not
paste a long class list from an example without checking that every class exists at the pinned version: a renamed
utility fails silently, as a missing style.

## Origin
Rewritten from the framework's documentation, read 2026-10-02. The documentation site's repository carries no
open licence, so only mechanisms were taken and every sentence is ours; see
[`references/origin.md`](./references/origin.md). Read it when checking freshness, not when applying a rule.
