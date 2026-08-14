# vue-nuxt-vuetify-conventions §7 — Accessibility in templates

> Section 7 of `skills/vue-nuxt-vuetify-conventions`. Read it when the template renders a control, a form or an image. The other sections and the guardrails stay in `SKILL.md`.

1. Native semantic element (or the toolkit's wrapper for it) first — never a clickable `div`/`span`.
2. Heading order respected, no skipping levels.
3. Page shell wrapped in landmark elements.
4. Every icon-only control gets an accessible name (`aria-label`).
5. Every toggleable / expandable / selectable / checked / current state exposed through the matching ARIA
   attribute, not through a CSS class alone.
6. An icon sitting next to visible text is decorative: hide it from assistive tech rather than having it
   read twice.
7. Async UI feedback (toasts, status messages, form error summaries) announced through a live region.
8. An open modal: focus placed on it, trapped inside, returned to the trigger on close.
9. Never block paste on an authentication field, never disable viewport zoom. If the layout breaks at 200%,
   the layout is the problem.
