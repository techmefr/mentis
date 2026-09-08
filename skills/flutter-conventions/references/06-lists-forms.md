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
