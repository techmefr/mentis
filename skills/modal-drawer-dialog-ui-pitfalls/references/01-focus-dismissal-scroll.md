# modal-drawer-dialog-ui-pitfalls §1 — Focus, dismissal and scroll

Platform facts are recalled from public HTML and WAI-ARIA material and not re-read for this pass (see origin.md); the rest is own craft.

## 1.1 Dialog or page
1. **Symptom: a dialog with tabs, three steps and a table inside.** Cause: it was quicker to build than a route. A dialog suits a short, single decision or a small form that the user finishes or abandons without losing their place.
2. **Use a page (or a drawer with its own URL, §3.4) when the content is long, has steps, needs a link, or the user may want two things open at once.**
3. **Modal against non-modal**: a modal blocks the page and demands an answer; a non-modal panel (filters, details, chat) leaves the page usable. Choose per task, then apply the matching rules: the trap and inert page of §1.4 are for modals only.
4. **A transient message is not a dialog.** A toast or inline banner needs no focus move (`in-app-notifications-pitfalls`).

## 1.2 Name, focus in, focus back
1. **Symptom: a screen reader opens "dialog" with no name, or says nothing and keeps reading the page.** Fix: give the dialog a name from its visible title (`aria-labelledby`), and a description when the body has a message (`aria-describedby`); an alert dialog is for a confirmation that needs a decision.
2. **On open, move focus inside.** Target, in order of preference: the first field of a form, the dialog heading (made focusable without tab order) for reading-first content, the least destructive button for a destructive confirm. Never leave focus on the trigger.
3. **On close, return focus to the trigger.** Symptom: after closing, the next Tab starts at the top of the page. Keep a reference to the element that was focused before opening.
4. **When the trigger no longer exists** (the row was deleted, the menu item unmounted), return focus to a stated fallback: the list heading, the next row, or the page main region; decide it once.
5. **Focus must be visible** inside the dialog (`accessibility` §1), including the close button on a dark backdrop.
6. **Opening from a menu**: close the menu first, then open the dialog, and return to the menu's own button, not the vanished item.

## 1.3 Escape, backdrop and close controls
1. **Escape closes the top layer only.** Symptom: a combobox list open inside a dialog, Escape closes the dialog and loses the form. Fix: the innermost open layer consumes the key (`combobox-autocomplete-ui-pitfalls` §2.2).
2. **A visible close control with a name** ("Close", "Cancel") is always present; a swipe or backdrop click alone is not the only way out.
3. **Backdrop click closes only simple, non-dirty dialogs.** A form with typed data, a running upload or a required decision does not close on a stray click (§2.3).
4. **A press that starts inside the dialog and ends on the backdrop is not a backdrop click.** Symptom: selecting text and releasing outside closes it. Test the press and release targets together. Fix: record the target of the press (pointer down) and close on release only if both the press and the release were on the backdrop itself; a bare click handler on the backdrop element is not enough, because the click event fires on the common ancestor of press and release, which is the backdrop.
5. **A required decision has no hidden exit**: if the dialog cannot be dismissed, say why and provide the explicit button.

## 1.4 Trap and inert page
1. **Symptom: Tab walks into the page behind a modal and a screen reader reads it.** A dark overlay hides nothing from assistive technology.
2. **Prefer the platform**: the native dialog element opened as a modal makes the rest of the document inert, gives Escape and a backdrop, and manages the top layer. Check its support and its behaviours in the browsers you target before choosing a hand-built one. For an app that ships inside a webview shell, state the oldest webview version it targets and check the element against that, not against a desktop browser; if the version cannot be established, say so and treat the choice as unverified.
3. **A hand-built modal needs three things**: the page siblings marked inert (or hidden from the accessibility tree), a focus trap that wraps Tab and Shift+Tab at the ends, and the dialog role with `aria-modal`.
4. **The trap must handle content that changes**: a field that appears, a button that becomes disabled, and an empty dialog (focus the container).
5. **Live regions and toasts outside the dialog** are not reached; show errors for the dialog's actions inside it.
6. **A non-modal panel does not trap.** Tab may leave it, and Escape returns focus to the trigger.

## 1.5 Scroll lock and layout shift
1. **Symptom: the page scrolls behind the dialog, or jumps sideways when it opens.** Cause: the body scrollbar disappears, widening the page, or the lock is missing.
2. **Lock the document scroll while a modal is open and restore the exact position on close**; reserve the scrollbar width (stable gutter) so the layout does not shift.
3. **The dialog body scrolls, the header and actions stay**; a tall dialog on a short viewport must never push its buttons off screen.
4. **Count locks.** Two dialogs both locking and unlocking restore the page early; unlock only when the last one closes.
5. **Overscroll must not chain to the page behind** on touch devices (§3.1).
6. **Never lock scroll for a non-modal panel.**

## 1.6 Rendering and timing
1. **Render dialogs at the end of the document (portal)** so a parent's overflow, transform or stacking context cannot clip or reorder them.
2. **Do not mount heavy content before opening**, and do not leave a closed dialog's tabbable content in the tree.
3. **Animation must not delay focus**: move focus on open, not at the end of the transition, and honour reduced motion (`accessibility` §7).
4. **Remove the layer fully on close**, including listeners and the scroll lock, or the next open inherits stale state.
5. **Reset the form state on close** unless the user asked to keep a draft (§2.3).
6. **One component per dialog shape.** Symptom: the same backdrop, container and role markup is copied into many files, so a fix to dismissal, focus or scroll has to be made many times and is missed in some. Check: count the places that build the backdrop-and-container pair; more than one means a shared component is due.

## Checks
```
Keyboard only: open the dialog, Tab through it, Shift+Tab back, Escape; focus lands on the trigger and never in the page behind.
Screen reader: the dialog is announced with its name; the page behind is not readable.
Open with a long page scrolled to the middle: the page does not move; close it: the same position.
Select text inside the dialog and release the pointer on the backdrop: the dialog stays open.
```
