---
name: nuxt-semantic-element-first
description: "Use when a template needs a clickable/interactive control: use the native semantic element (or the toolkit's wrapper for it) first, never a clickable div/span."
---

# nuxt-semantic-element-first

Narrow trigger extracted from `skills/vue-nuxt-vuetify-conventions` §7.1, so a clickable non-semantic
element routes here directly instead of only through the whole Nuxt/Vue block.

## When
Writing or reviewing a template element that has a click handler, or any interactive behaviour, on a
`<div>`, `<span>`, or another non-interactive element.

## Steps
1. **Native semantic element first** — `<button>`, `<a>`, a form control — or the component
   toolkit's own wrapper for it. Never a clickable `<div>`/`<span>`.
2. **A `div` with a click handler has no role, isn't in the tab order, doesn't fire on Enter or
   Space, and announces as nothing** to assistive tech.
3. **Making it equivalent by hand costs a `tabindex`, a `role`, two key handlers and a disabled
   state** — all of which the native element or the toolkit's wrapper already provides for free.

## Output / checkpoint
Every interactive control in the diff is a native semantic element or the component toolkit's
purpose-built wrapper for it — no `@click` handler sits on a bare `<div>`/`<span>` standing in for a
button or a link.

## Guardrails
- If a non-semantic element genuinely needs the click behaviour (a card that navigates on click, say),
  it still needs the full manual accessibility treatment this rule exists to avoid — prefer wrapping
  the interactive part in a real `<button>`/`<a>` instead.
- The rest of the accessibility-in-templates section (colour not as the sole carrier of meaning, alt
  text, focus visibility) lives in `skills/vue-nuxt-vuetify-conventions` §7 — read it for the
  neighbouring rules this one sits beside.

## Origin
No external source: this is `skills/vue-nuxt-vuetify-conventions` §7.1 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
