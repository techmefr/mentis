# combobox-autocomplete-ui-pitfalls §2 — Keyboard and ARIA

Facts about roles and attributes are recalled from the public WAI-ARIA specification and authoring practices, not re-read for this pass (see origin.md). The rest is own craft.

## 2.1 Focus stays in the input
1. **Symptom: after pressing the down arrow the caret disappears and typing does nothing.** Cause: focus moved into the list. In the combobox pattern the DOM focus stays on the input for the whole interaction.
2. **Point at the active option by reference**: the input carries the id of the active option in `aria-activedescendant`, and the option has a visible highlight. Clear the reference when the list closes or no option is active.
3. **Options are not tab stops.** Tab leaves the field (and closes the list); it does not walk the options.
4. **The highlight must scroll into view** when the list is taller than its box, with the same move for keyboard and for programmatic updates.

## 2.2 Keys
1. **Down opens the list and moves to the next option; Up moves to the previous.** Decide wrap or stop at the ends and keep it consistent; do not open the list on plain focus unless the field is a "show recent on focus" one (§1.1).
2. **Enter chooses the highlighted option only when the list is open and an option is active.** Symptom: Enter submits the surrounding form with half a word. Fix: prevent the default submit in that case; with the list closed or nothing active, Enter behaves as the form expects.
3. **Escape closes the list; a second Escape clears the text** (a common, optional convention). It must not also close a dialog that contains the field on the first press (`modal-drawer-dialog-ui-pitfalls` §1.3).
4. **Home and End move the caret in the input**; do not capture them for the list unless the list is a pure listbox with a documented reason.
5. **Typing always edits the text**, including when an option is highlighted. Letter keys must not jump the highlight.
6. **Free text with inline completion** (the field completes the rest of the word, selected) is its own pattern: keep the selection range, and make Backspace remove the suggestion first.

## 2.3 Roles, states and relations
1. **The input has the combobox role and says it is expandable**: `aria-expanded` true or false, and `aria-controls` pointing at the popup. Native `<input>` with a `list` and a datalist is the fallback where its limits (styling, async) are acceptable.
2. **The popup is a listbox whose children are options**; each option has an id and a selected state when it is the committed one (`aria-selected`), and the listbox has a name.
3. **Say what kind of suggestions the field gives** with `aria-autocomplete`: list when the field does not change its text, inline or both when it completes.
4. **Required context** (`accessibility` §8): an option outside a listbox, or an owner without children, breaks navigation.
5. **A grouped list uses group roles with names**, not bold text only.
6. **A label is mandatory.** The visible label is associated with the input; a placeholder is not a label (`accessibility` §4).
7. **Do not set `aria-hidden` or `inert` on the popup while it is the active relation**; assistive technology drops it.

## 2.4 Announcements
1. **Symptom: a screen reader user types and hears nothing about results.** Cause: the list changed visually only.
2. **Use one polite live region for the result count and the state**: "5 results", "no results", "loading", "error, try again". Update it after the list settles (§1.3), not on every keystroke.
3. **Do not put the count inside the input's label**; it makes the field read the number on every focus.
4. **Announce the selection** ("Paris selected") when it is not obvious from the new field value; chips in a multi-select announce add and remove (§3.4).
5. **Keep the messages short and in the user's language** (`i18n-message-format-pitfalls` for plurals).

## 2.5 Touch and small screens
1. **Symptom: the on-screen keyboard hides the list, or the page zooms when the field is focused.** Fix: font size of at least 16 CSS pixels on the input (iOS zooms below it), and a list that fits above the keyboard or a full-screen picker on narrow viewports.
2. **Targets are touch-sized** (`accessibility` §1) and spaced so a scroll is not a selection.
3. **A scroll in the list must not close it**; a tap outside must. Test with a real touch device or emulation, not a mouse.
4. **Do not rely on hover** to reveal the clear button or any option detail.

## Checks
```
Keyboard only: type, Down, Down, Enter, Tab; the value is set and no form was submitted early.
Screen reader pass: the field reads its role, label and expanded state; a result count is spoken once after typing stops.
Automated: every option id referenced by aria-activedescendant exists; no option sits outside a listbox.
```
