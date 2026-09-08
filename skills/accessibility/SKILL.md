---
name: accessibility
description: "Use when writing or reviewing a frontend page or app, technical accessibility checklist: HTML semantics, focus and keyboard, contrast, ARIA, forms. Sourced from WCAG 2.2 level AA."
---

# accessibility

Step 6 of the pipeline (`WORKFLOW.md`), complementing
`vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`: applies to every page/component meant for
real users (not to internal scripts or dev-only tooling). Every rule below holds in a repo with
**nothing installed** (`CONVENTIONS.md`, rule A).

**Boundary with an org design catalogue.** Where one exists, its accessibility skill checks a **mockup**
against RGAA before any code exists, and `references/README.md` already names it as the single source for
RGAA thresholds. This block is the **code-time** pass on what's actually rendered — semantics, focus order,
ARIA, form wiring — which a mockup can't show. Don't restate a threshold here: read it from that skill.

**Applying an override is silent.** Where that skill or another standard governs, write what it requires
and move on — never report "a conflict between mentis and the house rules" to whoever's watching. Surface
it as a specific, named question only when no rule anywhere actually resolves the case.

## When
As soon as a frontend component/page is written or modified, during `code` (6) or at review time
(`review`, 8) if the diff touches UI.

## Steps

**Read only the sections the diff actually touches.** The rules live one file per section under
`references/`; an interactive element or a layer is §1, a custom widget is §1 and §2, colours or a
zoom-sensitive layout are §3, and anything with a field in it is §4.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Semantics and keyboard navigation | an interactive element, a layer, or anything a keyboard reaches | [`01-semantics-keyboard.md`](./references/01-semantics-keyboard.md) |
| 2 | ARIA: only when native HTML isn't enough | before adding any `role` or `aria-*`, or building a custom widget | [`02-aria.md`](./references/02-aria.md) |
| 3 | Contrast and visual perception | colours, sizes, a theme, or a zoom-sensitive layout | [`03-contrast-perception.md`](./references/03-contrast-perception.md) |
| 4 | Forms | a field, a validation path, a multi-step flow, an authentication screen | [`04-forms.md`](./references/04-forms.md) |

## Output / checkpoint
The sections reviewed on the diff touched; for a broader audit of a page/site already in production
(not just the diff in progress), see the `link` agent.

## Guardrails
- Don't confuse WCAG compliance with the real experience: a tooled audit (axe-core, Lighthouse) doesn't
  replace a manual keyboard/screen-reader test on the critical journeys (§2.12, §3.11).
- No ARIA added out of reflex "to look tidy": only when native HTML isn't enough (§2.1, §2.11).
- **Never remove a visible focus indicator** (§1.3), and never leave a focusable element inside a hidden
  subtree (§2.7).
- **Never state a threshold from memory** — read it from the standard or from the org catalogue's
  accessibility skill (`skills/source-freshness`).
- This block has no dedicated in-house production experience yet: to be confronted with the first real a11y
  audit, not to be treated as proven doctrine.

## Origin
WCAG 2.2 (level AA), MDN and the W3C ARIA APG, rewritten as an actionable checklist. The full provenance,
the 2026-08-10 WCAG 2.2 re-check and the refresh log are in
[`references/origin.md`](./references/origin.md).
