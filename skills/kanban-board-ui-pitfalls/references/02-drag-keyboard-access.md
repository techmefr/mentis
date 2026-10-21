# kanban-board-ui-pitfalls §2 — Drag, keyboard and access

Sources: dnd-kit documentation, accessibility guide and keyboard sensor page (MIT, commit stamped in origin.md, read 2026-10-20) for the facts marked as such; the W3C WCAG 2.2 Understanding pages for 2.5.7, 2.5.8, 2.3.3 and 1.4.1 and the Media Queries Level 5 draft (W3C document licence, facts only, read 2026-10-20) for the criteria named; WAI-ARIA 1.2, Pointer Events Level 3 and the dnd-kit sensor pages and live region source (read 2026-10-20) where stated below; the rest is own craft.

## 2.1 A keyboard route for every drag
1. **Symptom: a board that cannot be used without a mouse.** A drag gesture is a pointer-only operation, and two criteria apply: a keyboard equivalent for every operation, and, under WCAG 2.2 SC 2.5.7 (level AA), a way to do anything that needs dragging with a single pointer and no dragging, unless dragging is essential (`accessibility` §1). Keyboard drag alone does not meet 2.5.7; the "Move to..." menu of §2.1.3 does.
2. **Make the drag handle or the card focusable and operable with both Enter and Space.** The library documents that its drag activator must take focus and respond to both keys, and that arrow keys then move the item, Enter or Space drops it and Escape cancels it. Keep those defaults.
3. **Offer a second, non-drag route that needs no gesture at all:** a "Move to..." menu on each card listing columns and positions ("Top of In progress", "After Fix login"), reachable by keyboard and by voice control. This is the more robust alternative, it is the single-pointer route that SC 2.5.7 asks for, and it also serves switch users, who find sustained key sequences hard.
4. **Arrow movement should land on meaningful targets,** the next card or column slot, not a fixed pixel step. The library says its default step is arbitrary and recommends tailoring it; for a sortable list it already jumps to the neighbouring item.
5. **Keep the keyboard order of the board natural:** columns left to right, cards top to bottom, reading order equal to visual order (`accessibility` §1).
6. **Escape cancels everywhere,** for pointer drags too, and puts the card back where it was.

## 2.2 Naming, instructions and announcements
1. **A draggable card needs identity, operation and state** (the three questions the library's guide asks): what it is, how to move it, where it now is.
2. **Instructions on focus:** attach a short description (pick up with Space, move with arrows, drop with Space, cancel with Escape) through an accessible description, in the user's language (`i18n-message-format-pitfalls`).
3. **Override a generic role description** such as "draggable" with a word for the product ("card"). The library ships a default and suggests customizing it.
4. **Announce every state change in a polite live region** (the library creates one element with role status, aria-live polite and aria-atomic true, and WAI-ARIA 1.2 makes the status role implicitly polite and atomic): picked up, moved over a column and position, dropped, cancelled, refused. Say the card title, the column name and the place ("Fix login, In progress, position 2 of 5"), not an internal id.
5. **Announce the outcome of the server, not only the drop:** "moved" after confirmation, or "could not move, column limit reached" on refusal (`kanban-board-ui-pitfalls` §1.5).
6. **Move focus on purpose:** after a keyboard drop focus stays on the moved card in its new place; after a failed move it returns to the card where it was. A re-render that recreates the element loses focus: key cards by id (`data-table-ui-pitfalls` §1.4).
7. **Do not build on aria-grabbed or aria-dropeffect.** WAI-ARIA 1.2 marks aria-grabbed as deprecated since 1.1 and tells authors to treat aria-dropeffect as deprecated, so state travels in the description and the announcements above.

## 2.3 Pointer and touch
1. **Symptom: on a phone the page scrolls instead of dragging, or dragging blocks scrolling.** Separate the gestures: a drag handle that starts a drag, the rest of the card scrolls. Long-press activation is a common alternative; state it in the instructions.
2. **Add a small activation distance or delay** so a click on the card (open details) is not read as a drag. Symptom: the details dialog never opens on touch. The library offers a distance constraint or a delay with a movement tolerance, mutually exclusive, and says the tolerance matters for touch because touch is less precise.
3. **Auto-scroll when the pointer nears the edge of the board or of a column,** vertically for long columns and horizontally for many columns. Without it a card cannot be dragged to a column off screen.
4. **Targets are large enough to hit**: at least 24 by 24 CSS pixels, or enough spacing around smaller ones (WCAG 2.2 SC 2.5.8, level AA, which also accepts an equivalent control elsewhere on the page). Drop zones are the whole column body, not a thin line (`accessibility`).
5. **Pointer capture and cancel:** release outside the window, on a disabled column or with a lost pointer cancels the drag and restores the card; never leave it floating. Pointer Events Level 3 lists the cases where the browser must cancel the stream by itself (it opens a modal dialog or menu, the device is disconnected or a hovering pen leaves range, the viewport is panned or zoomed, a native HTML drag-and-drop starts) and releases capture then; a screen orientation change, too many simultaneous pointers and accidental-touch rejection are listed only as cases where it may; treat pointercancel and lostpointercapture as drop-cancelled, not as a drop.
6. **A drag overlay (the ghost) must not become the only copy.** Keep the original in place, dimmed or outlined, so the board does not collapse and the layout does not jump.
7. **Set touch-action before the gesture starts.** Pointer Events Level 3 says a change to touch-action after the pointer went down is ignored for that gesture, and that the browser fires pointercancel when it takes the pointer over to pan or zoom the viewport; so a handle styled touch-action none in the stylesheet keeps the drag, and one set from the pointerdown handler loses it. Check: a touch drag on a real device or emulator does not end in pointercancel after a few pixels.

## 2.4 Do not rely on colour or animation
1. **WIP warnings, forbidden columns and conflicts use text and an icon as well as colour** (WCAG SC 1.4.1, level A: colour is not the only visual means of conveying information; `accessibility` §3).
2. **Respect reduced motion:** the settle animation after a drop becomes an immediate move when the `prefers-reduced-motion` media feature reports `reduce` (`accessibility` §7). WCAG SC 2.3.3 (level AAA) asks that motion triggered by interaction can be disabled unless essential, so treat it as the target, not a floor. Keep the drop indicator static and visible.
3. **Keep the drop indicator contrast sufficient** against both column backgrounds, in light and dark themes.
4. **Do not move focus or content under the user during a drag** (a live update inserting a card above the pointer shifts every drop target).

## Checks
- Complete a move, a cross-column move and a cancel with the keyboard alone; each is announced in a screen reader.
- The "Move to..." menu reaches every column and position without a drag.
- On a touch device the page still scrolls, and a tap opens the card.
- With reduced motion on, no animation runs on drop.
