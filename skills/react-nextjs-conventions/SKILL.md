---
name: react-nextjs-conventions
description: Use when writing or reviewing React/Next.js: structure and naming, typing, hooks discipline, immutability, memo, server-state libraries, validation at boundaries, App Router, effects and security correctness.
---

# react-nextjs-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing of code on the React 18/19 + Next.js stack. Every
rule below holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A). Complementary to `legolas`
(the diff review agent): here we write the code, legolas re-reads it afterwards.

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue for this stack, it
is the authority on **its** house style and overrides this block wherever the two differ. This block is the
generic default. Two house conventions in particular genuinely split across real codebases — `type` vs
`interface` for object shapes, and where tests live — and this block says "pick one and apply it uniformly"
rather than pretending there's a universal answer.

**Applying an override is silent.** Write the code the governing rule actually requires and move on — never
report "a conflict between mentis and the house catalogue" to whoever's watching. That framing reads as
broken to a non-technical stakeholder even when the case is a normal, resolved one, and has already caused a
real project to get abandoned and restarted over nothing. Surface it as a specific, named question only when
no rule anywhere actually resolves the case — never as a general alarm.

**On a Laravel + Inertia.js app with React pages, there is no Next.js runtime** (no App Router, no
Next data fetching) — a page there is a plain component wired by Inertia. This block's Next-specific
sections don't have an equivalent in that architecture; see `skills/inertia-conventions` §4 before
flagging an Inertia repo against them.

## When
As soon as a `.tsx` component, a Next.js route, a hook, a store slice or a query hook is written or modified,
during `code` (6) or `tdd` (5).

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; loading all of them for a change that only renames a variable is waste, and a section
read is a section that has to be applied. If you are reviewing a whole diff, pick the rows whose
trigger the diff meets, not the whole table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Components and files | a component is created or split | [`01-components-files.md`](./references/01-components-files.md) |
| 2 | Naming | a symbol or a file has to be named | [`02-naming.md`](./references/02-naming.md) |
| 3 | Typing | props, state or a generic is typed | [`03-typing.md`](./references/03-typing.md) |
| 4 | Control flow | conditional rendering, lists, early returns | [`04-control-flow.md`](./references/04-control-flow.md) |
| 5 | State, effects, hooks | a hook is written, or an effect added | [`05-state-effects-hooks.md`](./references/05-state-effects-hooks.md) |
| 6 | Server state and stores | TanStack Query, Zustand or RTK | [`06-server-state-stores.md`](./references/06-server-state-stores.md) |
| 7 | Next.js | the App Router, a server component, a route handler | [`07-next-js.md`](./references/07-next-js.md) |
| 8 | The component library | a UI element is built, or custom CSS is about to be written | [`08-component-library.md`](./references/08-component-library.md) |
| 9 | Security, never negotiable | always, on any diff | [`09-security-never-negotiable.md`](./references/09-security-never-negotiable.md) |
| 10 | Accessibility and bundle weight | a control is rendered, or a dependency added | [`10-accessibility-bundle-weight.md`](./references/10-accessibility-bundle-weight.md) |

## Output / checkpoint
Code compliant with the sections above. No dedicated checkpoint: compliance is checked by `gate` (7) and by
`legolas` at review time in the `review` step (8).

## Guardrails
No comments in the code produced. Never modify a generated component file in place: always go through a
wrapper. Don't duplicate an existing hook or selector before checking that no nearby one covers the need.
This block writes code, it doesn't review diffs; for the review, that's `legolas`. Where an org catalogue is
installed and disagrees with a rule here, **it wins** — say so explicitly rather than silently applying
either one. When in doubt about a rule covered by neither, escalate rather than guess.

## Origin
Rules mined from market catalogues, linters and internal review feedback, rewritten in the house
voice; the full provenance, the source stamps and the refresh log are in
[`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still
current, not when applying one.
