---
name: solid-ownership-pitfalls
description: "Use when writing, reviewing or testing SolidJS 1.x code where state silently resets or leaks: components called as functions, Show or Match whose child keeps state when the value changes, the same component in several branches, hooks or signals created inside effects and memos, props.children read twice, store updates from server data, functions stored in a store, module-level signals under server rendering, boolean values on enumerated attributes (aria-expanded, draggable, spellcheck, contenteditable), innerHTML, custom-element props, and tests (render with an arrow, createRoot, renderHook, async queries, fake timers, portals)."
---

# solid-ownership-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the SolidJS mistakes that render correctly the first time and then
reset state, leak it between users, or never react. The sections share one premise: **a Solid component runs
once, and every reactive primitive belongs to the owner that was active when it was created**; anything that
creates a primitive in the wrong owner, or outside one, breaks quietly. Each rule says what you see when it is
missed.

**Version scope: Solid 1.x.** At the time of reading the stable release line is 1.9 and a 2.0 line exists only
as a release candidate. A 2.0 migration section was therefore not written; a 2.0 project needs its own source
read first (see the origin notes).

Standalone block, written because the broader Solid conventions block exists only on an unmerged branch. It is
meant to be merged into the same-named framework block when that lands (see
[`references/origin.md`](./references/origin.md)). Until then it cites only blocks present on the main branch.

## When
- A form or a widget inside a `Show`, `Switch` or `Match` keeps the previous record's state, or a child
  remounts and loses state when a layout branch changes.
- A component is invoked as `Component(props)`, or a hook is called inside an effect, a memo or a computed.
- A page rendered on the server shows another user's data, or an ARIA state is wrong in the accessibility tree.
- Server data is written into a store, or a callback is stored in one.
- A test passes without reacting, hangs under fake timers, or cannot find portal content.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Ownership and control flow: component calls, keyed Show, stable mount, primitives in effects, children | state resets or leaks, or a branch remounts | [`01-ownership-and-control-flow.md`](./references/01-ownership-and-control-flow.md) |
| 2 | Stores, server rendering, DOM attributes and custom elements | a store is fed from outside, the app is server-rendered, or an attribute is bound to a boolean | [`02-stores-ssr-and-dom.md`](./references/02-stores-ssr-and-dom.md) |
| 3 | Testing Solid code | a Solid test is written or one passes without reacting | [`03-testing.md`](./references/03-testing.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the parent was made to re-run and the child's state was seen
to survive (§1), two records were switched in sequence and the form showed the second record (§1), two
requests were made to the server render and the second showed none of the first user's state (§2), the test
was mutated to fail and was seen to fail (§3). A rule only read is not verified.

## Guardrails
- Never call a component as a function; render it with JSX, `Dynamic`, or a captured reference (§1).
- Never create a signal, memo, resource or hook inside an effect or a memo (§1).
- Never create reactive state at module scope in an application that is server-rendered (§2).
- Never write `aria-expanded={isOpen()}` or its equivalents with a boolean; pass the string token (§2).
- Never render markup from user input through `innerHTML` without sanitising; see `security-hardening` (§2).
- Never test reactivity with a component rendered outside the test library's arrow wrapper (§3).
- Accessibility semantics beyond the attribute-type rule belong to `accessibility`.

## Origin
Rewritten from the official Solid documentation (component, control-flow, store, root and testing pages),
the eslint-plugin-solid rule documentation (MIT) and one MIT Solid best-practices rule set, read 2026-10-08.
🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
