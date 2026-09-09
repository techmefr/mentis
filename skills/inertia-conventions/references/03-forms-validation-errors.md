# § 3 — Forms, validation and errors

> Section 3 of `skills/inertia-conventions`. Read it when a form is written or modified, when validation
> is added, or when a submit has to report a failure to the reader.

1. **`useForm` owns a form's state, submission and error display** — not a hand-rolled `ref`/`useState`
   plus a manual `axios.post` plus manually reading a caught error's response body. `useForm` already
   wires the request, the pending/processing flag, and the validation-errors bag together. A hand-rolled
   submit also leaves the visit out of Inertia's hands, which means no redirect handling, no error bag,
   and no cancellation of the previous in-flight request.
2. **Validation stays server-side, in a FormRequest, the same as any other Laravel controller** — a
   thrown `ValidationException` arrives back as the page's `errors` prop automatically; there's no
   separate error-shape contract to invent for Inertia. Client-side checks are there to save the reader
   a round trip, never to be the rule: the rule is the one the server will actually enforce.
3. **Real-time (as-you-type) validation feedback, where the UX genuinely needs it, uses Laravel's own
   precognition mechanism** rather than a hand-rolled debounced validation endpoint — it reuses the same
   FormRequest rules the real submission will run, so the two can't drift apart. A separate validation
   endpoint is a second copy of the rules, and the copy that gets updated is the one whose failure is
   visible; the reader is told their input is fine and then told it isn't.
4. **The errors bag is keyed by the request's field names, dot-notated for nested input.** A repeater
   sends `items.0.quantity`, so the message lands under that key and not under `quantity`. A field
   reading the wrong key displays nothing: the submit appears to do nothing at all, which is the one
   failure a reader cannot work around. Read the key the server will produce, and render an
   errors-not-shown fallback near the submit button so a mis-keyed message is still visible.
5. **A `useForm` submission is a visit, so on success the page re-renders from the server.** That is
   normally what you want — the list behind the form is now correct because it came back from the
   database, not because the client patched it. A form that must stay put across the submit needs the
   visit to preserve state and scroll (§5.4, §5.5), and a form inside a modal needs the modal's open
   state to survive the same way.
6. **Nothing stops a second submit while the first is in flight unless the button is wired to the form's
   processing flag.** Two clicks on a slow connection are two rows, two emails, two charges. Disable on
   the flag rather than on a local boolean that a failed submit forgets to reset — and where the action
   is genuinely not repeatable, make the server idempotent too, because a reload can replay it.
7. **Validation errors survive the redirect through the session, so the redirect has to go back to the
   form.** Redirecting a failed submit to a different page carries the errors to a page with no field to
   display them, and the reader sees a navigation that silently discarded what they typed. `back()` is
   the ending for a failure; the success target is the only redirect that chooses a new page.
8. **Reset the form in the success callback, not on submit.** Clearing the fields when the request leaves
   means a validation failure returns the reader to an empty form with error messages about values they
   can no longer see. Password fields are the exception worth stating: clear those on failure too, but
   keep everything else.
9. **A form carrying a file is sent as multipart, and PHP does not populate the form data for `PUT` or
   `PATCH`.** The method has to be spoofed through a `_method` field — `useForm`'s own `put`/`patch` do it
   when a file is present, a hand-built request does not, and the symptom is an empty request body with
   validation failing on every field. The same conversion is what forces a file form to be `post`.
10. **A large upload with no progress reads as a frozen page.** The visit exposes upload progress; a form
    that ignores it gives the reader nothing to distinguish a 40 MB upload from a hang, and they will
    press the button again (point 6) or navigate away. Show progress, and say what happens if they leave.
11. **The 422 becomes an errors prop only for an Inertia request.** The same controller reached by a
    non-Inertia client gets the JSON validation body instead. That is a feature — the FormRequest is the
    shared contract and both callers are validated identically — but it means a test asserting the JSON
    shape is not testing what the page receives (§6.4).
12. **A destructive action is a request with a method, never a `<Link>` with a URL.** A plain link is a
    `GET`: a browser prefetch, a crawler, a security scanner or an over-eager extension can fire it
    without a human clicking. Use the delete method on the link or a form, and put the confirmation in
    front of the request rather than in front of the navigation.
13. **A failed request that is not a 422 needs its own visible outcome.** A 500, a 403 from a policy, a
    419 from an expired session and a dropped connection all arrive as something other than the errors
    bag; a form that only renders `errors` shows nothing for any of them. Handle the error callback, and
    treat the expired-session case specifically — it is the common one, and the fix the reader needs is
    to log in again, not to correct a field.
14. **A long form deserves its state kept across an accidental navigation.** Inertia can remember a
    form's state in the history entry, so the back button returns the reader to what they had typed
    rather than to an empty form. Reach for it when losing the input would mean retyping minutes of work.
15. **`useForm`'s Precognition support is built in — the wiring point 3 asks for is the route's
    `HandlePrecognitiveRequests` middleware, not a client-side integration.** Nothing about the form's
    submit changes: the same `useForm` instance validates a field on blur/change against the live
    FormRequest and later submits for real, so point 1's single-owner-of-form-state rule holds without a
    second helper or a separate as-you-type endpoint. Point 3 stands as the reason to reach for it; this
    is that the reaching-for is one middleware line, not a package.
