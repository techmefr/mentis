# combobox-autocomplete-ui-pitfalls §2 — Keyboard and ARIA

Facts credited to "APG combobox" and "APG select-only" were checked on 2026-10-20 against the W3C ARIA authoring practices pages (facts only, own words; see origin.md). Points without a credit are own craft or recalled, not re-read. Third pass 2026-10-20: the authoring practices list-autocomplete example, listbox pattern and WCAG 2.2 Understanding pages for SC 4.1.3, 3.3.2 and 1.4.11 were read (facts only, own words).

## 2.1 Focus stays in the input
1. **Symptom: after pressing the down arrow the caret disappears and typing does nothing.** Cause: focus moved into the list. In the combobox pattern the DOM focus stays on the input for the whole interaction (APG combobox). The one exception is a popup that is a dialog: dialogs cannot use an active-descendant reference, so DOM focus moves into them.
2. **Point at the active option by reference**: the input carries the id of the active option in `aria-activedescendant`, and the option has a visible highlight (APG combobox); the browser does not scroll that target into view for you, so the script must (§2.1.4). The highlight needs at least 3:1 contrast with adjacent colours (WCAG 2.2 SC 1.4.11). Clear the reference when the list closes or no option is active.
3. **Options are not tab stops.** Tab leaves the field (and closes the list); it does not walk the options.
4. **The highlight must scroll into view** when the list is taller than its box, with the same move for keyboard and for programmatic updates.

## 2.2 Keys
1. **Down opens the list and moves to the first option (or to the one after an already auto-selected suggestion); Up, optional, moves to the last.** Alt+Down opens the list without moving, Alt+Up from the list returns to the input and closes it (APG combobox). Decide wrap or stop at the ends (the list-autocomplete example wraps from last to first, the select-only example stops at the ends) and keep it consistent; do not open the list on plain focus unless the field is a "show recent on focus" one (§1.1).
2. **Enter chooses the highlighted option only when the list is open and an option is active** (APG combobox: Enter accepts the suggestion in an editable combobox). Symptom: Enter submits the surrounding form with half a word. Fix: prevent the default submit in that case; with the list closed or nothing active, Enter behaves as the form expects.
3. **Escape closes the list; a second Escape clears the text** (optional in APG combobox, which says it may clear a combobox whose popup is already hidden; the list-autocomplete example does clear the text when the list is closed). It must not also close a dialog that contains the field on the first press (`modal-drawer-dialog-ui-pitfalls` §1.3).
4. **Home and End move the caret in the input** while focus is in the text. The APG combobox page lists them as optional keys of the popup only (re-read 2026-10-20): either move to the first or last option, or, for an editable field, send focus back to the input with the caret at the start or end. Do not capture them from the input for the list without a documented reason.
5. **Typing always edits the text**, including when an option is highlighted. Letter keys must not jump the highlight. (Not true of the select-only variant, §2.6.3, which has no text.)
6. **Free text with inline completion** (the field completes the rest of the word, selected) is its own pattern: keep the selection range, and make Backspace remove the suggestion first.

## 2.3 Roles, states and relations
1. **The input has the combobox role and says it is expandable**: `aria-expanded` true when the popup is visible and false when hidden, and `aria-controls` pointing at the popup, needed only while it is visible (APG combobox; the older ownership attribute is no longer the recommended relation). The popup role defaults to listbox; for a grid, tree or dialog popup the combobox must also declare which with `aria-haspopup`. Native `<input>` with a `list` and a datalist is the fallback where its limits (styling, async) are acceptable.
2. **The popup is a listbox whose children are options**; each option has an id, and the listbox has a name. Selection state: in the authoring practices list-autocomplete example `aria-selected` is true only on the option that is visually highlighted, which is the one the input references with the active-descendant attribute; do not mark a second option selected because it equals the saved value. The listbox pattern says to use `aria-selected` or `aria-checked` for the selection state, never both, and suggests `aria-selected` for single and `aria-checked` for multiple selection as a default: pick one convention for the whole product. A multi-select listbox also carries `aria-multiselectable`.
3. **Say what kind of suggestions the field gives** with `aria-autocomplete`: none when suggestions do not depend on the typed text, list when they correspond to it, both when a list is shown and an inline completion is also offered (APG combobox). The authoring practices page names only none, list and both; the inline-only value of the ARIA specification was not found in the excerpt read and stays unchecked.
4. **Required context** (`accessibility` §8): an option outside a listbox, or an owner without children, breaks navigation. The ARIA 1.2 role text (read 2026-10-20) confirms that a listbox must own options or groups; the required context of an option itself was not reached and stays unverified.
5. **A grouped list uses group roles with names**, not bold text only.
6. **A label is mandatory.** The visible label is associated with the input (WCAG 3.3.2: labels or instructions are provided, and are presented to everyone, not only through an accessible name); a placeholder is not a label (`accessibility` §4).
7. **Do not set `aria-hidden` or `inert` on the popup while it is the active relation**; assistive technology drops it.

## 2.4 Announcements
1. **Symptom: a screen reader user types and hears nothing about results.** Cause: the list changed visually only.
2. **Use one live region for the result count and the state** (WCAG 4.1.3 requires a status message to be exposed without moving focus, and names a status role as the technique for results; the authoring practices list-autocomplete example itself announces no count, so this is an addition for real searches): "5 results", "no results", "loading", "error, try again". Update it after the list settles (§1.3), not on every keystroke.
3. **Do not put the count inside the input's label**; it makes the field read the number on every focus.
4. **Announce the selection** ("Paris selected") when it is not obvious from the new field value; chips in a multi-select announce add and remove (§3.4).
5. **Keep the messages short and in the user's language** (`i18n-message-format-pitfalls` for plurals).

## 2.5 Touch and small screens
1. **Symptom: the on-screen keyboard hides the list, or the page zooms when the field is focused.** Fix: font size of at least 16 CSS pixels on the input (iOS zooms below it), and a list that fits above the keyboard or a full-screen picker on narrow viewports.
2. **Targets are touch-sized** (`accessibility` §1) and spaced so a scroll is not a selection.
3. **A scroll in the list must not close it**; a tap outside must. Test with a real touch device or emulation, not a mouse.
4. **Do not rely on hover** to reveal the clear button or any option detail.

## 2.6 Select-only variant (button and list, no text input)
Keys and focus checked against APG select-only on 2026-10-20 (credited per point); the rest is own guidance (see origin.md). Sections 2.1.5, 2.2.4, 2.2.5 and 2.2.6 assume a text input and do not apply; the rest of this file does.
1. **Symptom: a custom select that looks like the native one and works only with a mouse.** The control is a focusable element with the combobox role (a button is the usual base), a listbox popup and options; there is no caret, so the keys differ from §2.2.
2. **Focus stays on the control, and the active option is named by reference** exactly as in §2.1.2: `aria-activedescendant` on the control, an id on every option, `aria-expanded` and `aria-controls`. Symptom: the highlight is a CSS class only, so a screen reader hears nothing about the active option. Check: every option has an id and the control's reference points at an existing one.
3. **Keys** (APG select-only): on the closed control, Down, Alt+Down, Enter and Space open the list without changing the value; Up opens it and moves to the first option; Home and End open it and move to the first and last option; a printable character opens it and moves to the first matching option. With the list open, Up and Down move one option and stop at the ends, Home and End jump to the ends, PageUp and PageDown move by ten; Enter, Space and Alt+Up commit the option, close the list and keep focus on the control; Escape closes without changing the value; repeated typing of one character cycles through options starting with it and a quick run matches a longer prefix. Moving through options never changes the value, only a commit does.
4. **Tab closes the list**. The select-only example commits the highlighted option on Tab and moves focus to the next element, and notes that this differs from the native select, which closes without moving focus on Tab (APG select-only); decide once which you follow and test it. Symptom: a keyboard user tabs away and the list stays open over the page. Check: Tab with the list open.
5. **Scroll the active option into view** (§2.1.4); a language or country list overflows its box.
6. **Empty and missing cases**: arrow keys on an empty option list must not compute an index from a zero length (a modulo by zero gives an invalid index); a stored value that is not among the options shows a stated placeholder or the stored label, not a blank (§1, the selected value outside the loaded options); a disabled option is skipped, not committed.
7. **Inside a dialog, Escape closes the list only.** A select handler that does not stop the key lets a container's own Escape listener close the dialog on the same press (§2.2.3). Check with a select in a dialog: first Escape closes the list, second closes the dialog.
8. **Close on outside press and on focus loss**, with the same rules as §2.5.3.

## Checks
```
Keyboard only: type, Down, Down, Enter, Tab; the value is set and no form was submitted early.
Screen reader pass: the field reads its role, label and expanded state; a result count is spoken once after typing stops.
Automated: every option id referenced by aria-activedescendant exists; no option sits outside a listbox.
Select-only: Home, End, a typed letter and Tab behave as in 2.6; an empty option list does not throw.
```
