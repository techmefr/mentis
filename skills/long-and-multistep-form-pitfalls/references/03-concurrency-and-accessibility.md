# long-and-multistep-form-pitfalls §3 — Concurrency and accessibility

## 3.1 Two people, one record
1. **The last writer wins unless you decide otherwise.** Symptom: a colleague's change vanishes with no error.
   Check: open the same record in two sessions, edit different fields, save both. Fix: optimistic locking
   (below); pessimistic locks only where an edit session is long and conflicts are costly.
2. **Carry a version token with the record.** A version counter, an update timestamp with enough resolution,
   or a hash of the content. On HTTP the entity tag (ETag) is that token: the client sends it back in a
   conditional header (If-Match) and the server answers 412 Precondition Failed when a condition in the request tested false
   (RFC 9110 section 15.5.13, read 2026-10-20; the If-Match section itself was not reached in the pages read, so the exact
   comparison rule is unverified). 428 Precondition Required lets the server insist that the request be conditional, and
   RFC 6585 §3 presents it as the guard against a lost update; the response should say how to resubmit, and servers are
   not obliged to use it, so a client cannot count on it. Symptom of a missing token: an update that cannot tell stale from
   current.
3. **Make the conditional update atomic in the data store.** Symptom: check-then-write in two statements lets
   two writers pass the check. Fix: one statement that updates where id and version match and bumps the version,
   then read the affected-row count; zero means conflict.
4. **Timestamps are weak tokens.** Second-resolution timestamps collide, and clocks differ between servers. Use
   a counter or a hash where conflicts are plausible.
5. **Send the token the person loaded, not a fresh one.** Symptom: the client re-reads the record just before
   saving and so defeats the check. Fix: the token travels with the form from first load to submit.
6. **Partial updates need the check too.** A patch of one field still races with another person's patch of the
   same field. Decide: version on the whole record, or per-field versions where fields are independent.

## 3.2 The conflict screen
1. **A refusal is a screen, not a toast.** Show the person's version beside the current server version, mark
   which fields differ, and let them keep theirs, take the server's or merge field by field. Symptom: an error
   that offers only "reload", which discards their typing.
2. **Merge automatically only when the changed field sets are disjoint**, and say so. Anything else asks.
3. **Keep the person's typed values until they decide.** The conflict response carries the current record (or
   the client fetches it), the form is not reset (§1.3.5).
4. **Deletions are conflicts too.** Editing a record that was deleted returns not-found or gone; show "this
   record was removed" with an option to recreate from the typed values.
5. **Live presence is a hint, not protection.** "Someone else is editing" banners reduce collisions but do not
   replace the version check.

## 3.3 Accessibility of errors and steps
1. **Move focus to the first invalid field on a failed submit, or to an error summary that links to the fields.**
   Symptom: screen-reader users hear nothing after pressing submit. Check: submit an invalid form with the
   keyboard only. Fix: focus management plus a live region for the count of errors.
2. **Tie each message to its field** (accessible description and an invalid state on the input), and keep the
   message text in the page, not only in a colour or an icon. The basics are in `skills/accessibility`
   reference 04.
3. **Announce step changes.** Symptom: pressing "next" swaps the content and the screen reader stays on the
   removed button. Fix: after the swap move focus to the new step heading, and update the page title or a
   progress region ("Step 3 of 5: Delivery").
4. **Do not use a timeout that discards input without warning**, and do give a way to extend it. WCAG 2.2 SC 2.2.1 (understanding
   page read 2026-10-20) wants, for each time limit the content sets, one of: the user can turn it off, adjust it over a range
   at least ten times the default, or be warned before expiry with at least 20 seconds to extend by a simple action, at
   least ten times. Exceptions: real-time events, essential limits, and limits longer than 20 hours. A session that expires
   mid-form is such a limit.
5. **Keep disabled "next" buttons explained.** A disabled control that does not say why is invisible to some
   users; prefer an enabled control that reports what is missing on activation.
6. **Autocomplete and input purpose.** Fields for the person's own data should declare their purpose so the
   browser can fill them. The HTML Standard (CC BY 4.0, read 2026-10-20) defines purpose tokens such as given-name, email, tel,
   street-address and postal-code, optional shipping or billing prefixes, a section- prefix that groups fields into one set
   (two addresses on one form), and `off` for values that must not be remembered. Label long forms in groups (fieldset and
   legend) so a screen-reader user keeps the context (this last point is own practice, unsourced).
7. **Error text is required, not optional.** WCAG 2.2 SC 3.3.1 (read 2026-10-20) asks that the item in error be identified and
   described in text, with colour or icons allowed only in addition; SC 3.3.3 separately asks for a suggestion, and one message
   can satisfy both ("Email is not valid" meets the first, adding the expected format meets both). A silent change of an
   out-of-range value also needs a text description.
8. **Page title and focus on error.** The government error-summary page (read 2026-10-20) adds an "Error: " prefix to the page title
   so a screen reader announces the failure early, in addition to moving focus to the summary (§1.4.4).
9. **Test the three flows by hand:** keyboard-only submit with errors, a step change with a screen reader, and a
   conflict screen. Automated checks do not cover focus order or announcements.
