# react-nextjs-conventions §10 — Accessibility and bundle weight

> Section 10 of `skills/react-nextjs-conventions`. Read it when a control is rendered, or a dependency added. The other sections and the guardrails stay in `SKILL.md`.

1. An icon-only button with no visible label needs an `aria-label`. Every `<img>` needs an `alt`: the
   description if it carries meaning, `alt=""` (never omitted) if it's purely decorative — a missing `alt`
   reads out the filename to a screen reader. The two halves are the same rule: a control or an image
   without a name is announced by whatever the browser can scrape, which is the URL, and a list of
   filenames is not navigable.
2. **When a control has visible text, the accessible name contains that text.** An `aria-label` that
   paraphrases the label ("Delete this invoice" over a button reading "Delete") replaces the name rather
   than adding to it, and voice control matches on the accessible name — so a user saying what they can see
   activates nothing. Add context with `aria-describedby`, or extend the visible text; do not overwrite it.
3. **A form control has a real label, associated by `id`.** A placeholder is not a label: it disappears the
   moment the user types, it is not announced by every screen reader, and it fails contrast in most themes.
   A visually hidden label is a legitimate answer; no label is not.
4. **An error message is wired to the field it belongs to.** Rendering the sentence next to the input is a
   visual association only; without `aria-describedby` and `aria-invalid` a screen reader user hears the
   error nowhere near the control, and a form that reports "3 errors" gives them no way to find them.
5. An open modal: focus placed on it, trapped inside, returned to the trigger on close. The return is the
   half that gets forgotten — without it, closing a dialog drops focus back to the top of the document, so
   the keyboard user's next action starts from the page header rather than from where they were.
6. **Every actionable element is reachable by keyboard, and focus is visible.** Removing the outline without
   supplying a replacement makes the application unusable without a mouse while looking tidier in
   screenshots. Focus order follows the visual order; a positive `tabIndex` overrides that order globally
   and is a bug in every case where it seems to help.
7. Native semantic elements over clickable `div`s; heading order without skipped levels. A `div` with an
   `onClick` is not focusable, not activated by Enter or Space, and not announced as a control — the three
   things a `<button>` gives for free, which is why reimplementing it always ships incomplete.
8. **Colour alone never carries meaning.** A red border with no message, or a status shown only as a
   coloured dot, is invisible to a colour-blind user and to anyone reading a monochrome print or a screen in
   sunlight. Pair it with text or a shape.
9. **A region that changes without a navigation has to announce itself.** Search results updating in place,
   a save confirmation, a validation summary appearing after submit — with no live region, a screen reader
   user is told nothing happened. This is also the case that automated audits miss, because the markup is
   valid at every instant.
10. **Respect `prefers-reduced-motion`.** An animation that is pleasant for most readers is a vestibular
    trigger for some, and the media query costs one block. The same applies to anything auto-playing or
    auto-scrolling.
11. Never block paste on an authentication field (password, one-time code). It is defended as security and
    is the opposite: it breaks password managers, so it pushes users toward passwords short enough to type
    from memory.
12. Never disable viewport zoom: if the layout breaks at 200%, the layout is the problem. Zoom is how a
    large share of users read anything, and disabling it converts a cosmetic defect into an unreadable page.
13. A default import from an icon lib, or a heavy module loaded at the level of a rarely visited route,
    bloats the bundle for nothing: named import / `next/dynamic`. Check that the package is actually
    tree-shakeable before trusting the named import to help — a CommonJS build ships whole either way, and
    the honest fix is then a direct path import or a different package.
14. **The client boundary decides the bundle, not the component's own size.** A `'use client'` at the top of
    a widely imported file pulls its entire import tree across, so a small component can be responsible for
    hundreds of kilobytes it never mentions. Push the boundary down to the leaf that genuinely needs
    interactivity, and keep heavy data-shaping on the server side of it.
15. **`ssr: false` is a cost, not a modifier.** It trades the server-rendered markup for a loading flash and
    a layout shift, so it is right when the component truly cannot exist without the DOM and wrong when it
    was added to silence a hydration warning — that warning is §5's problem, and hiding it here moves the
    bug rather than fixing it.
16. **Ask the platform before adding a dependency.** Date formatting, number and currency formatting,
    pluralisation, relative times and collation are all `Intl`, at zero bytes; a package added for one of
    them is weight plus a supply-chain surface (§9.16). The general form: a dependency in a diff is a number
    somebody can measure, and measuring it at review time is far cheaper than removing it a year later.
