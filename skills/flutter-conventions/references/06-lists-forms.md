# flutter-conventions §6 — Lists and forms

> Section 6 of `skills/flutter-conventions`. Read it when a list, a pagination, a form, the keyboard. The other sections and the guardrails stay in `SKILL.md`.

1. A long list uses the lazy builder, never a fully materialised children list. The materialised form builds
   every item before the first frame, so a list of two thousand rows costs two thousand widget trees to show
   ten — the symptom is a screen that takes a second to open and a scroll that stutters on a mid-range
   device, which is most devices.
2. **A lazy list still needs a bounded height.** Nested inside another scrollable or an unconstrained
   column it either throws the unbounded-height error of §3.2 or, if given a shrink-wrap escape hatch,
   quietly builds every item anyway and loses the entire benefit. The right answer is a bounded slot, not a
   flag that silences the message.
3. **`itemCount` and the data are one thing.** Kept separately — a count cached in state, a list replaced
   under it — the builder is asked for an index that no longer exists, and the crash arrives from the
   framework rather than from the line that was wrong.
4. **A row's state needs the row's identity.** Without a key tied to the item, reordering or filtering
   reuses the element in place, so an expanded row, a checked box or a half-typed cell stays with the
   position instead of the record. When the row contains an input, what the user typed moves to another
   item, and the save is real.
5. **A row is built while the user is scrolling.** Anything expensive in it — parsing, formatting, a
   full-resolution image decode (§8.15) — happens at the frame rate, so it belongs above the list, not in
   the item. Keep the item widget dumb and const where it can be (§2.2).
6. Paged list: load the next page near the end, show a loading footer, mark the end of the list, and handle
   the error-mid-scroll case. Pull-to-refresh resets to the first page.
7. **The next-page trigger fires more than once.** A scroll listener runs on every pixel, so the threshold
   is crossed on many consecutive frames and the same page is requested repeatedly; the guard is a flag in
   the state holder saying a load is in flight (§7.16), not a debounce on the scroll.
8. **Changing the filter resets the cursor.** Otherwise page two of the previous query appends to page one
   of the new one, and the list shows a mixture that matches no filter at all — with a total that is wrong
   and an end-of-list marker that arrives early.
9. **A refresh keeps the list visible.** Returning the screen to its initial loading state discards the
   scroll position and the content the user was reading (§4.9); the refresh indicator exists so that the
   list can stay on screen while it happens.
10. A form field validates through the form's own validator mechanism, showing **inline per-field errors**,
    not one global message. A global "invalid data" makes the user hunt through a screen they have already
    filled in, and on a phone that means scrolling past the keyboard to find a field they cannot see.
11. **Server-side rejections map back to their fields too.** A field-level failure returned by the API and
    rendered as a snack bar is the same problem as point 10 with an extra network round trip, and it is the
    common one — client validation is user experience, the server's rules are the authority, and both have
    to land in the same place on screen.
12. Choose the validation timing deliberately (on submit, or as-you-type after first interaction);
    validating from the first keystroke flags an empty field the user is still typing into. The middle
    ground that usually works is to validate a field when it loses focus and to re-validate as-you-type only
    once it has already been flagged.
13. **Normalise before validating.** A trailing space from an autocomplete, a full-width character from a
    phone keyboard, mixed case in an email — the input is rejected for something the user cannot see, and
    they retype the same value. Trim and normalise at the edge, once.
14. Disable the submit control while a submission is in flight — a double tap is one order twice. The
    disabled state derives from the state holder's status rather than from a separate boolean, so that the
    button and the guard cannot disagree (§7.16).
15. **A text controller belongs to the widget that created it**, and is disposed there (§1.13). The state
    holder receives the value, never the controller — that is what keeps the form testable without a screen
    and what stops a controller outliving the widget it was drawn for (§7.8).
16. Keyboard: avoid covering the focused field, scroll it into view, set the right keyboard type and action
    (next/done), and let a tap outside dismiss. The keyboard is an inset, not an overlay (§3.12), so a form
    that does not account for it hides its own submit button — and the last field's action submits, or the
    user has to dismiss the keyboard to find it.
17. **Set the autofill and input hints.** A password field that is not marked as one defeats the password
    manager, so the user picks something they can type; a one-time-code field that does not accept the
    platform's suggestion, or that blocks paste, makes a six-digit code a memory exercise. Both are read as
    security measures and are the opposite.
18. **A long form is worth a draft.** The app is terminated in the background as a matter of course (§5.14),
    and coming back to an empty form after ten minutes of typing is the failure users describe as losing
    their work — because they did.
19. **A sticky section header belongs to a `CustomScrollView`'s slivers, not a rebuilt widget above the
    list.** `SliverPersistentHeader` pins the current section's label while the rest scrolls underneath it;
    combining several independently-scrolled pieces — a header, a grid, a footer — into one `CustomScrollView`
    keeps them in a single scroll physics and a single lazy-build pass, instead of nesting scrollables that
    each need the bounded-height treatment of point 2.
20. **A reorderable list's key has to survive the reorder, not just the initial build.** `ReorderableListView`
    moves the element identified by a widget's key to its new index; a key derived from the item's current
    position rather than its stable identity moves the wrong element's state along with it — the same
    failure as point 4, but triggered by the drag gesture instead of a filter or a fetch.
21. **A multi-step form keeps every step's data in one place for the whole flow**, not scoped to the widget
    for the step currently visible. A `Stepper` or a paged form whose fields live in each step's own local
    state loses page one's answers the moment page one is disposed for page two — the state holder outlives
    the step widgets exactly the way point 15 says the controller does not need to.
22. **On a failed submit, move focus to the first invalid field.** A screen that shows inline errors
    (point 10) but leaves focus wherever it was makes a screen-reader user hunt through the whole form for
    what changed, and a sighted user scroll for it manually; moving focus and scrolling that field into view
    together turns the error summary into something the user lands on rather than something they have to
    find.
23. **A search field the user types into is a debounced trigger, not a request source.** The screen-state
    concern in §4.17 has a form-side cause: a `TextField.onChanged` wired straight to a query fires once per
    keystroke, and even where the state holder discards the stale answers (§4.16), the backend still does the
    work for every intermediate value the user was going to overwrite a moment later.
24. **A number or date entered by the user is parsed and formatted for the device's locale, not a fixed
    format.** A decimal separator, a date order or a digit grouping that differs from the user's own settings
    turns a correctly-typed value into a rejected one, or worse, a silently different number — 1,234 read as
    one thousand two hundred thirty-four in one locale and one point two three four in another is not a
    display detail, it changes what gets submitted.
25. **Autofill and paste apply to more than the password and one-time-code fields of point 17.** An address,
    a name or a phone number field that isn't tagged with the right autofill hint forces a re-type of data
    the platform already has on file for every other app the user has filled it into once — the six-digit
    code is the visible case, but the same defeat happens quietly on every field a form author didn't think
    of as "sensitive enough" to tag.
26. **Tab order on a form is a separate decision from visual order.** The framework builds a default
    traversal from the tree's structure, which usually matches the layout — until a row is built with a
    trailing icon button before its label, or a field is wrapped in a container that reorders its children
    for styling reasons, and the "next" key jumps somewhere the eye doesn't expect. A `FocusTraversalGroup`
    with an explicit policy is how a form's tab order is asserted rather than inherited from incidental
    widget nesting.
27. **The last field's action still has to reach the submit button, not just dismiss the keyboard.** Point
    16 already says the final `TextInputAction` should submit; the mechanism is calling
    `FocusScope.of(context).nextFocus()` or the form's own submit handler from that field's `onFieldSubmitted`
    — omitted, the field's action defaults to closing the keyboard, and a one-handed user on a phone has no
    way to reach a submit button that point 16 already established the keyboard was covering.
28. **`Dismissible` needs a confirmation step for anything the user cannot easily redo.** A swipe that
    deletes a row immediately, with only a snack bar's undo window after the fact, relies on the user
    noticing the snack bar before it times out; `confirmDismiss` returning a decision before the item leaves
    the list is the version of that safety net that doesn't depend on how fast someone reads.
29. **A field-level async check needs the same discard rule as point 16's search results.** A username or
    slug availability check fired on every keystroke can return "taken" for a value the user has already
    revised to something else by the time the response lands, and showing that stale verdict against the
    current text tells the user their new entry is invalid when it was never checked at all — the request
    and its answer have to be compared against what the field currently holds, not assumed to still match.
30. **Uniform manual spacing between list items and `ListView.separated`'s own separator builder are not
    interchangeable once the list is long.** A `Padding` or `SizedBox` baked into every item widget is built
    and measured for every row the lazy builder produces, including the divider; `ListView.separated`'s
    dedicated separator builder is the same lazy-build discipline as point 1 applied to the gaps between rows
    rather than only to the rows themselves.
31. **A pinned `SliverAppBar` and a floating one answer different questions about when the header
    reappears.** `pinned` keeps the collapsed bar on screen through the whole scroll, the way point 19's
    persistent header keeps a section label visible; `floating` brings the full bar back the moment the user
    scrolls up even from the middle of a long list, which is the right shape for a search bar the user wants
    back quickly and the wrong one for a section label that should only reappear at its own section.
