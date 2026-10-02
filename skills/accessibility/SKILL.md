---
name: accessibility
description: "Use when writing or reviewing a frontend page or app, technical accessibility checklist: HTML semantics, focus and keyboard, contrast, ARIA, forms. Sourced from WCAG 2.2 level AA."
---

# accessibility

Step 6 of the pipeline (`WORKFLOW.md`), complementing
`vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`: applies to every page/component meant for
real users (not to internal scripts or dev-only tooling). The rules are written against the web standards
(HTML, WAI-ARIA, WCAG), not against a framework or an assistant. Every rule below holds in a repo with
**nothing installed** (`CONVENTIONS.md`, rule A).

**Boundary with an org design catalogue.** Where one exists, its accessibility skill checks a **mockup**
against a numeric threshold before any code exists — this block is the **code-time** pass on what's
actually rendered — semantics, focus order, ARIA, form wiring — which a mockup can't show. Don't restate a
mockup-time threshold here: that's the earlier step's job. RGAA itself is different in kind from a
threshold and is self-sufficient in this block (§5): a French/public-sector project, a French client above
the private-sector threshold, or a request for an accessibility declaration is handled here without
depending on an external catalogue.

**Applying an override is silent.** Where an org catalogue or another standard governs a mockup-time
threshold, write what it requires and move on — never report "a conflict between mentis and the house
rules" to whoever's watching. Surface it as a specific, named question only when no rule anywhere actually
resolves the case.

## When
As soon as a frontend component/page is written or modified, during `code` (6) or at review time
(`review`, 8) if the diff touches UI.

## Steps

**Read only the sections the diff actually touches.** The rules live one file per section under
`references/`; an interactive element or a layer is §1, a custom widget is §1 and §2, colours or a
zoom-sensitive layout are §3, and anything with a field in it is §4, a table, list or embed is §6, audio, video or motion is §7, and a
tabs, accordion, carousel or other composite widget is §8.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Semantics and keyboard navigation | an interactive element, a layer, or anything a keyboard reaches | [`01-semantics-keyboard.md`](./references/01-semantics-keyboard.md) |
| 2 | ARIA: only when native HTML isn't enough | before adding any `role` or `aria-*`, or building a custom widget | [`02-aria.md`](./references/02-aria.md) |
| 3 | Contrast and visual perception | colours, sizes, a theme, or a zoom-sensitive layout | [`03-contrast-perception.md`](./references/03-contrast-perception.md) |
| 4 | Forms | a field, a validation path, a multi-step flow, an authentication screen | [`04-forms.md`](./references/04-forms.md) |
| 5 | RGAA — the French legal standard, its test methodology, and the déclaration d'accessibilité | the project is French/public-sector, or a French client is above the private-sector threshold, or an accessibility declaration is requested | [`05-rgaa.md`](./references/05-rgaa.md) |
| 6 | Document structure and embedded content: tables, lists, definition lists, unique ids, frames and objects, image text, things not done without a reason | a diff adds a table, a list, an embed, a generated identifier, an image with text or a caption | [`06-document-structure.md`](./references/06-document-structure.md) |
| 7 | Media, motion and orientation: captions, descriptions, autoplay, flashes, smooth scroll, parallax, orientation | audio or video, anything that moves on its own or on scroll, or anything that depends on orientation | [`07-media-motion.md`](./references/07-media-motion.md) |
| 8 | ARIA validity and component recipes: valid roles, required context, required names; tabs, accordion, tooltip, carousel, breadcrumb, pagination, search, upload, custom element | §2 has decided ARIA is needed, or one of these components is being built | [`08-aria-validity-widgets.md`](./references/08-aria-validity-widgets.md) |

## Output / checkpoint
The sections reviewed on the diff touched; for a broader audit of a page/site already in production
(not just the diff in progress), see the `link` agent.

## Guardrails
- Don't confuse WCAG compliance with the real experience: a tooled audit (axe-core, Lighthouse) doesn't
  replace a manual keyboard/screen-reader test on the critical journeys (§2.12, §3.11).
- No ARIA added out of reflex "to look tidy": only when native HTML isn't enough (§2.1, §2.11).
- **Never remove a visible focus indicator** (§1.3), and never leave a focusable element inside a hidden
  subtree (§2.7).
- **Never state a threshold from memory** — read it from the standard, or from the org catalogue's
  accessibility skill for a mockup-time value, or from §5 for an RGAA figure (`skills/source-freshness`).
- This block has no dedicated in-house production experience yet: to be confronted with the first real a11y
  audit, not to be treated as proven doctrine.

## Origin
WCAG 2.2 (level AA), MDN and the W3C ARIA APG, rewritten as an actionable checklist. The full provenance,
the 2026-08-10 WCAG 2.2 re-check and the refresh log are in
[`references/origin.md`](./references/origin.md).
