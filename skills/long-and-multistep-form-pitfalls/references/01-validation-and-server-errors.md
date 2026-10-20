# long-and-multistep-form-pitfalls §1 — Validation and server errors

## 1.1 When to validate
1. **Format rules after leaving the field, not on every keystroke.** Symptom: an email field turns red at the
   first character. Check: type slowly in each formatted field. Fix: validate on blur for format rules, and
   re-validate on change only once the field has already shown an error, so the error clears as soon as the
   value becomes valid.
2. **Required fields at submit or step change, not on first touch.** Symptom: tabbing through a field marks it
   "required" before the person had a chance to fill it. Fix: track "touched" per field and show required errors
   only for touched fields or after a submit attempt.
3. **Cross-field rules at the moment both fields are settled.** Symptom: "end date before start date" appears
   while the end date is still empty. Fix: run the rule when both have values, attach the message to the field
   the person can change.
4. **Checks that need the server (uniqueness, existence) are asynchronous and advisory.** Symptom: a "name is
   free" answer obtained at blur is false by the time of submit. Fix: debounce, ignore out-of-order answers,
   and still accept a refusal at submit (§1.3).
5. **One rule set, not two.** Symptom: the client accepts what the server rejects, or the reverse. Fix: write
   the rules once (shared schema, or a server endpoint that validates without saving) and check a handful of
   edge values on both sides; the server stays authoritative.

## 1.2 Steps and conditional sections
1. **Validate the current step before moving on; do not block moving back.** Symptom: a person cannot return to
   fix step 1 because step 3 is invalid. Fix: gate "next", never "previous".
2. **Hidden fields are not validated and not sent.** Symptom: a rule fails on a field that a toggle hid, and the
   error has nowhere to show. Fix: when a section hides, clear or exclude its values and drop its errors; when it
   reappears, restore or re-ask.
3. **A step indicator reflects state, not position.** Show which steps are complete, invalid or untouched. A
   person who sees "step 4 of 6" cannot tell that step 2 carries an error.
4. **The final step shows a review, and submit re-validates everything.** Symptom: a value edited in step 1
   invalidates a rule in step 4 after step 4 was passed. Fix: validate the whole form on final submit and send
   the person to the first failing step.

## 1.3 Server errors
1. **Distinguish the failure classes** and show each differently: field validation (a person can fix it), rule
   violation not tied to a field (state conflict, quota), authorisation, conflict (§3.1), and unexpected failure.
   Symptom: every non-2xx becomes the same toast "Something went wrong". Fix: a small table of response shapes
   to UI treatments, reviewed with the API owner.
2. **Map errors by a stable field path, not by position or message text.** Symptom: an error for line 3 of a
   repeating group lands on line 1 after a row was deleted. Fix: the server names the field path (including row
   identifiers where rows have them), the client resolves path to input; unknown paths fall back to a form-level
   list so nothing is dropped.
3. **A machine-readable error body with a code per error, plus a human message.** The standard problem-details
   format for HTTP APIs (RFC 9457, which replaces RFC 7807; re-read before relying on member names) gives a
   type, title, detail and room for extension members such as an error list. The client switches on the code,
   never on the translated message.
4. **Errors on a step the person is not on.** Symptom: the submit seems to do nothing because the failing field
   is on step 2. Fix: on a field error, navigate to the owning step, focus the field, and say in the summary
   which step it is.
5. **Keep everything typed.** Symptom: after a 422 or a timeout the form is empty or reset to loaded values.
   Fix: never reset on a non-success response; keep the in-memory values and the draft (§2.1).
6. **Do not double submit, and make retry safe.** Disable or guard the submit while pending (the generic rule is
   in `skills/frontend-ux-antipattern-review-pitfalls`). For creates, send a client-generated idempotency token
   the server stores with the result, so a retry after a lost response returns the first outcome instead of a
   second record. (The IETF idempotency-key header is a draft at the time of writing: re-read its status.)
7. **A timeout is not a failure.** The request may have succeeded. Symptom: the person retries and creates a
   duplicate. Fix: on timeout, reload the record or query by the idempotency token before offering "retry".

## 1.4 Messages
1. **Say what to do, next to the field, in the person's words.** "Enter a date after 1 March" beats "Invalid
   value". Wording rules are in `business/ux-writing`.
2. **Keep the person's value visible with the error.** Replacing a bad value with a blank hides what was
   wrong.
3. **A summary at the top of long forms helps only if each entry links to its field.** A list that cannot be
   clicked through is noise (accessibility side in §3.3).
