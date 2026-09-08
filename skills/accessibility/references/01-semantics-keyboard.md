# § 1 — Semantics and keyboard navigation: the non-negotiable base

> Section 1 of `skills/accessibility`. Read it whenever a diff adds or changes an interactive element, a
> layer, or anything a keyboard has to reach. Points 6 to 8 are the WCAG 2.2 criteria closed on
> 2026-08-10 and are cited by number from `references/origin.md`.

1. Every interactive element (`button`, `a`, `input`) is a real native tag, never a `div`/`span` with an
   `onClick` simulating a button: otherwise it's lost to the keyboard and to screen readers. What the
   native tag carries for free is the whole contract — focusability, the role announced, keyboard
   activation, the disabled state, and the form submission behaviour. Rebuilding it means rebuilding all
   five, and the ones usually missing are the last three, so the control works with a mouse and does
   nothing on `Enter`.
2. Tab order follows the logical visual order: never a positive `tabindex` that breaks the DOM's natural
   order; `tabindex="-1"` only to deliberately remove an element from the flow. A positive value does
   not reorder locally — it lifts the element above every natural stop on the page, so one such value
   reorders the entire document and the effect is invisible until someone tabs through it.
3. Visible focus (`:focus-visible`) never removed by an `outline: none` with no replacement: a keyboard
   user must always see where they are. Without it the page is not degraded, it is unusable: activation
   becomes guesswork, and the reader's only recovery is to tab back to something they recognise and count
   forward.
4. Focus trap (modal, dropdown): focus stays inside the open component while it's active, and returns to
   the triggering element on close. Both halves matter and the second is the one skipped: focus left
   behind at the top of the document sends the reader back through the entire page to reach the control
   they just used, on every open and close.
5. Standard keyboard shortcuts respected: `Escape` closes a modal/dropdown, `Enter`/`Space` activates a
   focused button. These are what a reader already knows, so a component that ignores them costs them
   the discovery of whatever it does instead — and a layer with no `Escape` and its close button below
   the fold has no keyboard exit at all.
6. **A sticky header/footer/cookie banner never fully hides the focused element** (WCAG 2.2, Focus Not
   Obscured): a fixed-position overlay covering the bottom of the viewport is the recurring way a focus
   ring becomes invisible on `Tab` even though it's technically still "visible" in the DOM. The reader
   sees the focus disappear and reappear a few stops later, which reads as the ring being broken rather
   than as something covering it.
7. **Any drag-only interaction (reorder, resize, a slider dragged by its handle) needs a single-pointer
   alternative** that doesn't require dragging (buttons to move up/down, arrow-key support, a numeric
   input next to the slider) — WCAG 2.2, Dragging Movements. A user who can click but not drag precisely
   is otherwise locked out of the interaction entirely, not just inconvenienced.
8. **Touch/click target at least 24×24 CSS px**, or 24px of unobstructed spacing around a smaller one
   (WCAG 2.2, Target Size) — a row of small icon-only actions packed edge to edge is the usual offender.
   Packed edge to edge is also where the consequence is worst, because the neighbour of a small target is
   another action rather than empty space, so a near miss does something.
9. **A page needs headings that describe its structure, and their levels have to be right.** Heading
   navigation is how a screen-reader user skips to the part of the page they want, so a document whose
   headings were chosen for size has no outline to skip through — the reader is left reading it linearly,
   which on a dense screen is the difference between seconds and minutes. Levels are hierarchy, not
   typography (`business/interface-design` §1.3).
10. **Landmarks and a skip link, on any page with repeated navigation.** Without them the reader passes
    through the whole header and menu before reaching the content, on every page of the site. This is the
    highest-value thing on this list per line of code, and the one most often absent because it is
    invisible to a mouse user.
11. **A page's language is declared, and a passage in another language is marked.** The declaration is
    what selects the pronunciation rules a screen reader uses, so an undeclared page is read with the
    wrong phonetics throughout — intelligible to nobody, and a defect no visual check can see.
12. **Anything reachable by hover has to be reachable without it.** A menu, a tooltip or an action that
    appears only on hover does not exist for a keyboard, and on touch it either never appears or appears
    on the tap that was meant to activate something else. The keyboard-equivalent trigger is focus, and
    it has to be tested by tabbing rather than reasoned about.
13. **Content that moves, autoplays or updates on its own needs a way to stop it.** A carousel, a live
    ticker or an auto-refreshing list moves the thing the reader was reading — or was about to click —
    and for a reader using magnification the movement is the whole viewport. A pause control is the fix;
    honouring a reduced-motion preference is the other half.
14. **Never remove the keyboard's own affordances to tidy the interface.** Text selection disabled,
    context menus suppressed, paste blocked on an authentication field (§4.5), scrolling hijacked: each
    of these removes something a reader relies on, and the reason offered is always cosmetic.
15. **A single-page navigation has to move focus when the view changes.** Replacing the content without
    moving focus leaves a screen-reader user on the old element with no announcement that anything
    happened, so the reader concludes the link did nothing and activates it again.
