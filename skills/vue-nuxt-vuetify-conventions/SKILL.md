---
name: vue-nuxt-vuetify-conventions
description: Use when writing or reviewing Vue 3/Nuxt: the SFC shape, composables and stores, typing, naming, structure, i18n, accessibility in templates, the UI-toolkit-first rule, hydration safety, realtime, linter-derived correctness.
---

# vue-nuxt-vuetify-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing of frontend code on the Vue 3 + Nuxt stack with a
component library. Every rule below holds in a repo with **nothing installed** — that's the point of the
block (`CONVENTIONS.md`, rule A).

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue for this stack, it
is the authority on **its** house style — its package list, its named internal libraries, its file
layout — and it overrides this block on any point where the two differ. This block is the generic default,
not a competitor: it states the rule and the reason, so an agent can apply it on a project that has no
catalogue at all, and can recognise a house override as an override rather than as a contradiction.

**Applying an override is silent.** Write the code the governing rule actually requires and move on — never
report "a conflict between mentis and the house catalogue" to whoever's watching. That framing reads as
broken to a non-technical stakeholder even when the case is a normal, resolved one, and has already caused a
real project to get abandoned and restarted over nothing. Surface it as a specific, named question only when
no rule anywhere actually resolves the case — never as a general alarm.

**On a Laravel + Inertia.js app, there is no Nuxt runtime** (no Nuxt routing/auto-imports/`useFetch`/SSR
server) — a Vue page there is a plain SFC wired by Inertia, not a Nuxt page. This block's Nuxt-specific
sections don't have an equivalent in that architecture; see `skills/inertia-conventions` §4 before
flagging an Inertia repo against them.

## When
As soon as a `.vue` component, a Nuxt page, a composable, a store or a server route is written or modified,
during `code` (6) or `tdd` (5).

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; loading all of them for a change that only renames a variable is waste, and a section
read is a section that has to be applied. If you are reviewing a whole diff, pick the rows whose
trigger the diff meets, not the whole table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The shape of a component | a `.vue` file is created or restructured | [`01-shape-component.md`](./references/01-shape-component.md) |
| 2 | Composables and stores | logic moves out of a component, or a store is touched | [`02-composables-stores.md`](./references/02-composables-stores.md) |
| 3 | Typing | props, emits, refs or a store return type are written | [`03-typing.md`](./references/03-typing.md) |
| 4 | Naming and style | a symbol, a file or a CSS class has to be named | [`04-naming-style.md`](./references/04-naming-style.md) |
| 5 | Structure and dependencies | a file is placed, or an import crosses a layer | [`05-structure-dependencies.md`](./references/05-structure-dependencies.md) |
| 6 | i18n | any string the user will read | [`06-i18n.md`](./references/06-i18n.md) |
| 7 | Accessibility in templates | the template renders a control, a form or an image | [`07-accessibility-templates.md`](./references/07-accessibility-templates.md) |
| 8 | The component library | a UI element is built, or custom CSS is about to be written | [`08-component-library.md`](./references/08-component-library.md) |
| 9 | Nuxt: hydration safety and the choice of data primitive | SSR, `useFetch`/`useAsyncData`, or a value that only exists client-side | [`09-nuxt-hydration-safety.md`](./references/09-nuxt-hydration-safety.md) |
| 10 | Realtime events | a socket, a broadcast or a live update | [`10-realtime-events.md`](./references/10-realtime-events.md) |
| 11 | Reactivity and security correctness (linter-derived) | reviewing a diff, or chasing a reactivity bug | [`11-reactivity-security-correctness.md`](./references/11-reactivity-security-correctness.md) |
| 12 | Recurring review patterns (quality debt observed in the field) | reviewing a diff, for the debt that keeps coming back | [`12-recurring-review-patterns.md`](./references/12-recurring-review-patterns.md) |

## Output / checkpoint
Code compliant with the sections above. No dedicated checkpoint: compliance is checked by `gate` (7) and
`review` (8), like the rest of the code produced at the `code`/`tdd` step.

## Guardrails
No comments in the code produced. Don't reinvent a component the UI toolkit already provides. Don't duplicate
an existing composable before checking that no nearby one covers the need. `technical/` never imports
`functional/`. Where an org catalogue is installed and disagrees with a rule here, **it wins** — say so
explicitly rather than silently applying either one. When in doubt about a rule covered by neither, escalate
rather than guess.

## Origin
Rules mined from market catalogues, linters and internal review feedback, rewritten in the house
voice; the full provenance, the source stamps and the refresh log are in
[`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still
current, not when applying one.
