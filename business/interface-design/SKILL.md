---
name: interface-design
description: "Use when producing or auditing a mockup, or deciding an interface's shape before it is coded: containers, states, design tokens, button hierarchy, chips versus buttons."
---

# interface-design

Business layer (`business/README.md`), design. Sits **before** step 6: these are decisions made in a mockup
or in a conversation, where changing them costs a rectangle rather than a refactor.

**Relation to a design system.** Every number in a real design system is arbitrary and owned — its spacing
scale, its type scale, its button heights, its icon sizes. This block therefore states **the discipline and
the decision trees, never the numbers**: where a design system exists, its tokens are the authority and no
value here overrides one. Where none exists, the rule is "pick a scale and never leave it", which is the part
that actually holds across projects (rule C: nothing named, no house values).

**Applying an override is silent.** Where a design system's tokens or components govern, write what they
require and move on — never report "a conflict between mentis and the house rules" to whoever's watching.
Surface it as a specific, named question only when no rule anywhere actually resolves the case.

**Boundaries.** How text is exposed to assistive technology and to the keyboard, in the shipped code →
`skills/accessibility`. The words themselves → `business/ux-writing`. What the screen is for → `skills/spec`
and `business/product-ownership`.

## When
When a screen is being designed or audited before implementation; when a UI element's shape is being chosen;
when a mockup arrives and has to be checked before someone builds it.

## Steps

**Read §0 every time, then only the sections the task actually touches.** The rules live one file per
section under `references/`. Settling the mode is not optional and costs one file; loading all seven to
answer one question is waste.

| § | Covers | Read it when | File |
|---|---|---|---|
| 0 | Producing versus auditing, and never recalling a threshold | always, before anything else | [`00-mode.md`](./references/00-mode.md) |
| 1 | Tokens, not values | any spacing, size or type value is being chosen | [`01-tokens.md`](./references/01-tokens.md) |
| 2 | Which container | deciding between a toast, modal, drawer, sheet or page | [`02-containers.md`](./references/02-containers.md) |
| 3 | Every state, not the happy path | the screen loads or displays dynamic data | [`03-states.md`](./references/03-states.md) |
| 4 | Buttons and chips | action hierarchy, a toolbar, a filter bar, status indicators | [`04-buttons-chips.md`](./references/04-buttons-chips.md) |
| 5 | Icon and text together | an icon sits next to a label, or a control is icon-only | [`05-icon-text.md`](./references/05-icon-text.md) |
| 6 | Gathering references | looking for prior art before designing a screen | [`06-references.md`](./references/06-references.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes before implementation starts: every value taken from a
scale rather than invented, a stated container choice, all required states drawn, one primary action per
context, and chips typed by kind. A mockup missing any of these produces implementation questions that get
answered by guesswork at step 6.

## Guardrails
- **Never start without settling producing versus auditing** (§0), and never let an audit rewrite the
  designer's intent (§0.2).
- **Never invent a spacing, size or type value outside the scale** (§1.1). If the scale is wrong, change the
  scale.
- **Never carry a value across projects** (§1.9) — a step remembered from the last one is a number with no
  owner in this one.
- **Never ship a data-driven screen without its loading, empty and error states** (§3.1–§3.3).
- **Never put a destructive confirmation in a toast, or a long form in a modal** (§2.6).
- **Never guess an accessibility threshold** (§0.7) — a specific number cited from memory is exactly the
  failure `skills/source-freshness` exists for. Defer to `skills/accessibility` and its cited standard.
- Where a design system exists, **its tokens and components win** over anything here; this block is the
  discipline, not the values.
- This block reviews interfaces, it doesn't write code, and it doesn't rewrite a designer's intent: a
  disagreement about intent goes back to the designer.

## Origin
An org design-system skill catalogue (10 skills), rules extracted, de-identified and rewritten generically
with every house value deliberately left out. The full provenance and the refresh log are in
[`references/origin.md`](./references/origin.md).
