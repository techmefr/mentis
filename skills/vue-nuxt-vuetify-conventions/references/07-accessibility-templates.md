# vue-nuxt-vuetify-conventions §7 — Accessibility in templates

> Section 7 of `skills/vue-nuxt-vuetify-conventions`. Read it when the template renders a control, a form or an image. The other sections and the guardrails stay in `SKILL.md`.

1. **Native semantic element first** — or the toolkit's wrapper for it — never a clickable `div`/`span`.
   A `div` with a click handler has no role, is not in the tab order, does not fire on Enter or Space,
   and announces as nothing; making it equivalent takes `tabindex`, a `role`, two key handlers and a
   disabled state you now maintain by hand. The element already does all of that, and the toolkit's
   component renders the real one underneath.
2. **Heading order respected, no skipping levels.** Assistive tech navigates by heading list, so the
   hierarchy is the page's table of contents; a jump from `h2` to `h4` reads as a section that went
   missing. Size is a separate concern — style the heading, don't pick a level for how big it looks.
3. **Page shell wrapped in landmark elements**, one `main` per page, and a skip link that reaches it. A
   keyboard user otherwise walks the whole navigation on every single page before arriving at the
   content.
4. **Every icon-only control gets an accessible name.** And where a control has visible text, its
   accessible name must contain that text — voice control users say what they see, so a button reading
   "Save" but named "Submit form" cannot be operated by voice at all.
5. **Every toggleable / expandable / selectable / checked / current state exposed through the matching
   ARIA attribute**, not through a CSS class alone. The class paints it, the attribute announces it, and
   both must be driven by the same piece of state — a class bound to a `ref` while the attribute is
   written once in the markup is the shape that goes out of sync and lies about the state.
6. **An icon sitting next to visible text is decorative**: hide it from assistive tech rather than having
   it read twice, and make sure nothing focusable is nested inside something hidden that way.
7. **Async UI feedback announced through a live region** — toasts, status messages, form error summaries.
   The region has to be in the DOM *before* the message arrives; injecting the container and the text
   together announces nothing, which is the usual reason a toast is silent. Reserve the assertive level
   for things that genuinely interrupt, and keep the rest polite.
8. **An open modal**: focus placed on it, trapped inside, returned to the trigger on close, Escape closes
   it, and it is labelled by its own title. The background must not be reachable — a dialog whose page
   still tabs underneath looks modal and is not, and the user's focus disappears somewhere they cannot
   see.
9. **Never block paste on an authentication field, never disable viewport zoom.** Blocking paste breaks
   password managers, which is a security regression dressed as a security measure. If the layout breaks
   at 200%, the layout is the problem.
10. **A form field is labelled programmatically, not by its placeholder.** A placeholder vanishes the
    moment someone types, is often not read as a name, and fails contrast more often than not. A visible
    label tied to the input is the default; a visually hidden one is the fallback when the design
    refuses.
11. **An error is attached to the field it belongs to**, and it says how to fix the value rather than
    only that it is wrong. On a long form, messages that are not programmatically linked leave a screen
    reader user knowing something failed and unable to find where — and a summary at the top is only
    useful if each entry moves focus to its field.
12. **Required, invalid and disabled are conveyed programmatically, not by colour or an asterisk alone.**
    Colour is never the sole carrier of meaning — the same rule covers status chips, diff highlighting
    and chart series, all of which need a shape, a label or text to survive both colour blindness and a
    greyscale print.
13. **Focus stays visible.** Removing the outline without replacing it makes the whole app unusable by
    keyboard; if the toolkit's focus style clashes with the design, replace it with something at least as
    visible, never with nothing.
14. **Everything operable by keyboard, in DOM order.** A row action that only appears on hover, or a
    custom dropdown that opens on click alone, strands keyboard and touch users; and a `tabindex` above 0
    breaks the order for everyone, including the people it was meant to help. Order the DOM, don't
    renumber it.
15. **Images carry meaningful alternative text, or an explicitly empty one when decorative** — never the
    filename. For a chart, alternative text is not enough: the numbers have to be reachable as text or a
    table, because a sentence cannot carry a series.
16. **The page declares its language, and a passage in another language is marked.** Without it a screen
    reader pronounces French with an English voice, which is not a detail — it ranges from comic to
    unintelligible.
17. **Verify with the keyboard and at 200% before claiming any of this.** Automated checkers cover a
    minority of the criteria and pass a page that cannot be used: tab through the feature, operate it
    without a mouse, and zoom. That is the whole test, and it takes a minute.
18. **A focused element is never fully hidden behind a sticky header, a cookie banner or a pop-up.** WCAG
    2.2's Focus Not Obscured criterion exists because a keyboard user tabbing through a page with a fixed
    header can land on a control that scrolled directly underneath it — the browser says it's focused, the
    screen shows nothing there, and the user has no way to tell where they are. Test it by tabbing through
    a long page with anything sticky turned on. [w3.org/TR/WCAG22, 2.4.11 Focus Not Obscured]
19. **A clickable target is at least 24×24 CSS pixels, or spaced enough not to be hit by accident.** A row
    of icon-only actions packed edge to edge fails this even when each icon individually "works" — the
    failure is a mis-click on a touch device or with a tremor, not a missing label. Padding around a small
    icon counts toward the target size; the icon itself doesn't have to grow. [w3.org/TR/WCAG22, 2.5.8
    Target Size]
20. **Any drag interaction ships a single-pointer alternative.** A reorderable list, a slider or a map pan
    that only responds to a drag gesture locks out anyone who cannot perform one precisely — a tap-to-move
    button, up/down controls, or an editable numeric field next to the slider are what makes the same
    action reachable with one deliberate click instead of a sustained motion. [w3.org/TR/WCAG22, 2.5.7
    Dragging Movements]
21. **A help mechanism, once offered, stays in the same relative place on every page that offers one.** A
    support link that moves from the header on one screen to a floating button on the next forces a user
    who relies on a consistent layout — including one navigating by muscle memory or by a screen reader's
    landmark list — to relocate it from scratch each time; consistent placement is itself part of the
    contract, not a cosmetic nicety. [w3.org/TR/WCAG22, 3.2.6 Consistent Help]
22. **Don't ask for the same information twice in one flow.** Re-entering an email address or a reference
    number the user already typed two steps earlier is a redundant-entry failure, not just friction — the
    fix is carrying the value forward (pre-filled, or referenced instead of retyped) rather than trusting
    every user to copy it correctly a second time under time pressure. [w3.org/TR/WCAG22, 3.3.7 Redundant
    Entry]
23. **Authentication never depends solely on a cognitive test the user has to solve from memory.** A
    CAPTCHA with no accessible alternative, or a login step that requires transcribing a code with no
    paste and no password-manager support, blocks exactly the users an accessible login is supposed to
    serve; support paste (point 9 already bans blocking it) and offer at least one path — biometric,
    magic link, password manager — that does not depend on solving a puzzle. [w3.org/TR/WCAG22, 3.3.8
    Accessible Authentication]
