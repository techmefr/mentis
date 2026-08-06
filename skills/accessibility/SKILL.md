---
name: accessibility
description: Use when writing or reviewing a frontend page/app (Nuxt/React), technical accessibility checklist: HTML semantics, focus/keyboard, contrast, ARIA, forms. No dedicated a11y production experience in house at this stage, sourced from WCAG 2.2 (level AA) and established guidelines (MDN, W3C).
---

# accessibility

Step 6 of the pipeline (`WORKFLOW.md`), complementing
`vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`: applies to every page/component meant for
real users (not to internal scripts or dev-only tooling).

**Boundary with an org design catalogue.** Where one exists, its accessibility skill checks a **mockup**
against RGAA before any code exists, and `references/README.md` already names it as the single source for
RGAA thresholds. This block is the **code-time** pass on what's actually rendered — semantics, focus order,
ARIA, form wiring — which a mockup can't show. Don't restate a threshold here: read it from that skill.

## When
As soon as a frontend component/page is written or modified, during `code` (6) or at review time
(`review`, 8) if the diff touches UI.

## Steps

### 1. Semantics and keyboard navigation: the non-negotiable base
1. Every interactive element (`button`, `a`, `input`) is a real native tag, never a `div`/`span` with an
   `onClick` simulating a button: otherwise it's lost to the keyboard and to screen readers.
2. Tab order follows the logical visual order: never a positive `tabindex` that breaks the DOM's natural
   order; `tabindex="-1"` only to deliberately remove an element from the flow.
3. Visible focus (`:focus-visible`) never removed by an `outline: none` with no replacement: a keyboard
   user must always see where they are.
4. Focus trap (modal, dropdown): focus stays inside the open component while it's active, and returns to
   the triggering element on close.
5. Standard keyboard shortcuts respected: `Escape` closes a modal/dropdown, `Enter`/`Space` activates a
   focused button.

### 2. ARIA: only when native HTML isn't enough
1. Golden rule: no ARIA rather than wrong ARIA; an incorrect `role` or `aria-*` is worse than its
   absence (a contract betrayed for assistive technologies).
2. `aria-label`/`aria-labelledby` on every interactive element with no visible text (icon only, close
   button): never a button that's mute to a screen reader.
3. `aria-live` (`polite`/`assertive`) on dynamic content areas that have to be announced (notification,
   a form error appearing after submission): otherwise the change is invisible to anyone not using their
   eyes.
4. `aria-expanded`/`aria-selected`/`aria-current` placed on the components that have the visual
   equivalent (accordion, tab, active item): the visual state must have an exposed equivalent.

### 3. Contrast and visual perception
1. Text/background contrast ≥ 4.5:1 (normal text) or 3:1 (large text ≥ 18px bold/24px): WCAG AA level,
   checked against the design system's real colours, not eyeballed.
2. Information is never carried by colour alone (e.g. red = error): always doubled with text, an icon or
   a pattern.
3. Content resizable up to 200% (browser zoom) with no loss of content or functionality: no width frozen
   in `px` that breaks under zoom.

### 4. Forms: the most frequently broken point
1. Every field has an associated `<label>` (`for`/`id` or wrapping), never a placeholder alone as a
   label: the placeholder disappears as soon as you type.
2. Error message associated with the field through `aria-describedby`, announced at the moment it
   appears (not only displayed visually).
3. Required fields marked with `required`/`aria-required`, not only by a visual asterisk with no exposed
   equivalent.

## Output / checkpoint
The four sections reviewed on the diff touched; for a broader audit of a page/site already in production
(not just the diff in progress), see the `link` agent.

## Guardrails
- Don't confuse WCAG compliance with the real experience: a tooled audit (axe-core, Lighthouse) doesn't
  replace a manual keyboard/screen-reader test on the critical journeys.
- No ARIA added out of reflex "to look tidy": only when native HTML isn't enough (see the golden rule in
  section 2).
- This block has no dedicated in-house production experience yet: to be confronted with the first real a11y
  audit, not to be treated as proven doctrine.

## Origin
Sourced from WCAG 2.2 (level AA, success criteria taken over), MDN (HTML semantics, ARIA authoring
practices), W3C ARIA APG (modal/accordion/tab patterns). Mechanisms rewritten as an actionable
checklist, no copied text. Market research, no internal production feedback at this stage: same status
as `seo`.
