# long-and-multistep-form-pitfalls §3 — Concurrency and accessibility

## 3.1 Two people, one record
1. **The last writer wins unless you decide otherwise.** Symptom: a colleague's change vanishes with no error.
   Check: open the same record in two sessions, edit different fields, save both. Fix: optimistic locking
   (below); pessimistic locks only where an edit session is long and conflicts are costly.
2. **Carry a version token with the record.** A version counter, an update timestamp with enough resolution,
   or a hash of the content. On HTTP the entity tag (ETag) is that token: the client sends it back in a
   conditional header (If-Match) and the server answers 412 Precondition Failed on a mismatch; 428
   Precondition Required lets the server insist the header be present (RFC 9110 and RFC 6585; facts, re-read
   before relying). Symptom of a missing token: an update that cannot tell stale from current.
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
4. **Do not use a timeout that discards input without warning**, and do give a way to extend it (an expiring
   session is a recognised accessibility problem; the WCAG criterion on timing is the reference to re-read).
5. **Keep disabled "next" buttons explained.** A disabled control that does not say why is invisible to some
   users; prefer an enabled control that reports what is missing on activation.
6. **Autocomplete and input purpose.** Fields for the person's own data should declare their purpose so the
   browser can fill them; label long forms in groups (fieldset and legend) so a screen-reader user keeps the
   context.
7. **Test the three flows by hand:** keyboard-only submit with errors, a step change with a screen reader, and a
   conflict screen. Automated checks do not cover focus order or announcements.
