# react-nextjs-conventions §15 — The Server Action result contract and idempotency

> Section 15 of `skills/react-nextjs-conventions`. Read it when a Server Action is written or reviewed: what it
> returns, how it reports failure, what happens when it runs twice, and what a deployment does to a client in the
> middle of one. The security rules for an action are §7.13, §7.14 and §9; the cache calls are §14. Pinned to
> the framework's 16.x documentation (read 2026-10-02, `references/origin.md`).

1. **Two kinds of failure, two channels.** An expected failure (a field that did not validate, a business rule
   that said no, a request to another service that was refused) is a **returned value** the form can show. An
   unexpected one (a bug, an outage, a failed authorisation) is a **thrown error** that reaches the nearest error
   boundary (§7.8). The framework's own guidance is to model the first as a return and not to wrap an action in
   `try`/`catch` to turn the second into a message: a bug dressed as a form error is a bug nobody reports.
2. **One result type, shared by every action.** A discriminated union with a literal `status` member: a success
   variant carrying only the data the screen renders, an invalid variant carrying per-field messages and a
   general message, and a rejected variant carrying a message for the user. Define it once and import it, so a
   component can narrow it the same way for every action (`skills/typescript-patterns` §4). An action used with
   `useActionState` receives the previous state as its first argument, which makes that same type the state's
   type; typing the previous state as `any` (as some examples in the documentation do) removes the check this
   union exists to give (§3).
3. **A returned value is serialised to the browser, so shape it for the screen.** Return the identifier and the
   fields the UI shows, never the database row, never a field the page does not render. The same applies to
   the message of a rejected result: it is user text, not the text of an exception.
4. **Validate first, return field errors, and take a reference, not a record.** The action's argument types are
   erased at run time (§7.14), so parse the form data with a schema at the top and return the flattened field
   errors on failure. A schema checks shape only: a well-formed record can still belong to someone else. Accept
   an identifier plus the user's change, take the identity from the session, and look the row up with the owner as
   part of the filter (§7.13). A "complete this item" action that receives the whole item and trusts its id lets
   anyone mark any item.
5. **Report a result to assistive technology.** The message region that shows the result is a polite live region
   and the submit control is disabled while the action is pending, as the documentation's form examples do
   (§10). The disabled control is a courtesy, not a guarantee: rule 8.
6. **A redirect and a result are exclusive.** `redirect` works by throwing, so nothing after it runs and the caller
   never receives a return value; the invalidation and revalidation calls do not throw, so an action can call
   them and still return. Order a success path as: write, invalidate (the call that waits for fresh data is the
   one that gives read-your-own-writes, §14), then redirect. An error path returns a value and does not redirect.
   An action that does none of invalidate, refresh, cookie write or redirect re-renders nothing: its caller
   sees only the returned value.
7. **The client runs actions one at a time, and that is not a lock.** A client dispatches its actions in
   sequence, so three quick submits arrive in order; do not use `Promise.all` to parallelise actions, do the
   parallel work inside one action or in a server component. The documentation calls this an implementation
   detail that may change, and it says nothing about two tabs, two devices or a proxy that retries, which are
   different clients. Correctness may not depend on ordering.
8. **Assume every mutating action runs twice.** An action is a POST. It runs twice when a user double-submits, when
   a button is not yet disabled, when a request is retried after a dropped connection, when the user has the
   form open in two tabs, and when the interface offers a retry after the
   deployment error of rule 10. Disabling the button is a courtesy; the guarantee lives on the server (the
   database-level reasoning is in `skills/laravel-post-may-run-twice`, the same for any stack):
   - an action that **creates** carries an idempotency key made when the form is rendered, passed as a bound
     argument (it supports progressive enhancement, and the documentation contrasts it with a hidden field, whose value is not encoded) or a
     hidden field (the value is in the HTML, unencoded, so it is never a secret). The server inserts the key in
     the same transaction as the row, under a unique constraint, and on a second arrival of the key returns the
     original result instead of creating again. The key is new for each new intent, not per page load.
   - a natural unique constraint (one subscription per user and plan) does the same job when the domain has one;
     the unique-violation error is caught and turned into the existing row's result, not into a failure.
   - an action that **updates or deletes** is written to be idempotent: set an absolute value, not an increment;
     deleting a row that is already gone is a success.
   - a check-then-insert in application code loses exactly the race it was written for.
9. **Constrain what a request can cost.** Action requests are capped at 1 MB by default; raise the limit only for
   an action that takes uploads, and say which one. The framework compares the request's origin with the host
   and rejects a mismatch: behind a proxy or CDN, list the extra domains in the allowed-origins setting
   instead of disabling the check (§9.11). Variables captured by an inline action are encrypted before
   they reach the browser; with more than one server instance, set the shared encryption key to the same
   stable value everywhere, or a request served by another instance cannot decrypt them.
10. **A deployment can strand a client mid-form.** Action identifiers are regenerated by a new build (at most every
    14 days even for unchanged source), so a tab left open on the old build can submit to an identifier the
    server no longer knows and gets a "failed to find Server Action" error. Prefer rolling deployments, and
    show that error as a retry path ("reload and try again") rather than a dead end. This is why rule 8 is not
    optional: the retry will resend the intent.
11. **Test the contract, not the framework.** An action is a function: call it with form data and a fake session and
    assert each variant of the result, the ownership refusal, the second call with the same key (one row), and
    that an invalid input returns field errors without writing (§11.14).
