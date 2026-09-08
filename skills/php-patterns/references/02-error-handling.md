# § 2 — Error handling

> Section 2 of `skills/php-patterns`. Read it when a failure is raised, caught, converted or reported at
> the language level. What belongs to a framework's error rendering is `laravel-conventions` §11.

1. A specific exception thrown (a dedicated class, not a generic `\Exception`) as soon as the caller
   has to be able to tell the error case apart to react differently. A generic exception forces the
   caller to match on the message, which is the one part of an exception nobody treats as a contract —
   so the day the wording changes, the catch that depended on it stops matching and the error escapes.
2. A `catch` that swallows the exception without rethrowing or logging it hides a real bug: never a
   silent `catch`, even as a last resort. The visible consequence is a request that returns success with
   nothing done, and the invisible one is that the log for the incident has no entry at the moment it
   happened.
3. An ambiguous `null` return (failure vs legitimate absence): prefer an exception for a real
   failure, `null`/an option only for an expected and documented absence. A caller that cannot tell the
   two apart writes the same branch for both, which is how "not found" ends up rendered as an empty
   dashboard instead of a 404.
4. **`catch (\Exception)` does not catch `\Error`.** `TypeError`, `DivisionByZeroError`,
   `ArgumentCountError` and an out-of-memory abort are `\Error`, not `\Exception` — so the block written
   to "catch everything" catches business failures and lets exactly the programmer errors through. Catch
   `\Throwable` where the intent really is everything, and catch the specific class everywhere else.
5. **Wrapping an exception without passing it as `$previous` deletes the cause.** The new exception's
   trace starts at the boundary that wrapped it, so the log shows "could not import file" and nothing
   about the type error three frames down that actually stopped it. Pass the original as the previous
   exception, and make sure whatever logs it walks the chain — a logger that prints only the top message
   throws away the half you need.
6. **`finally` runs on the way out however the block ends**, which makes it the place for releasing what
   the `try` acquired. One trap is worth stating: a `return` inside `finally` discards a pending
   exception silently — the function returns normally and the failure disappears, with no trace anywhere.
7. **Nothing secret goes in an exception message.** The message travels to the log, to the error
   tracker, often to a support ticket, and on a misconfigured environment to the reader's browser. A
   token, a password, a full row of personal data or a raw query with its bound values in the message is
   a leak into systems with a different retention policy and a different audience from the database.
8. **`@` suppresses the diagnostic, not the failure.** The call still fails, still returns `false`, and
   the next line then uses `false` as if it were data — so the symptom appears one step away from the
   cause with nothing in the log to connect them. If a failure is genuinely expected, check the return
   value; if it is not, let the error be reported.
9. **Much of the standard library signals failure by return value, and the check has to be strict.**
   `file_get_contents` and `preg_match` return `false`, `json_decode` returns `null`, `strpos` returns
   `false` — and `preg_match` returning `0` for "no match" is a different answer from `false` for "the
   pattern failed", which a truthiness check collapses into one. Compare with `===`, and prefer the flag
   or option that turns the failure into an exception where the function offers one
   (`JSON_THROW_ON_ERROR`).
10. **An exception hierarchy is what lets a caller catch by intent.** One base class per module or
    domain, with the specific classes extending it, means a caller can catch that module's failures
    without listing every class — and a new failure class added later is caught by the existing handlers
    instead of escaping to a 500. A flat set of unrelated exception classes forces every handler to be
    edited each time one is added.
11. **PHP's own error levels moved between versions, so an upgrade changes which failures are silent.**
    Division by zero became a `DivisionByZeroError` in PHP 8, an undefined array key went from notice to
    warning, and passing null to a non-nullable internal parameter is deprecated on the way to being an
    error. Code that "worked" was often relying on the silent branch, and the upgrade turns it into a
    500 in whichever path was doing it.
12. **Converting warnings into exceptions is a project-wide decision, not a local one.** An error
    handler installed for the whole process changes how every library behaves, including the ones that
    use a warning as a normal signal; installing one inside a single function and not removing it leaves
    that behaviour in place for everything that runs after. Decide once, at the entry point.
13. **A failure raised while the process is shutting down usually has nowhere to go.** An exception from
    a destructor during shutdown is fatal, and an exception thrown while another one is being handled
    replaces it in the log. So cleanup code — closing a handle, flushing a buffer, releasing a lock —
    must not be the code that can throw; do the work that can fail before the object dies.
14. **`assert()` is not validation.** It can be compiled out entirely by configuration, and on a
    production configuration it usually is — so a check written as an assertion holds in development and
    does nothing where it matters. Validate with real code that throws; use assertions only to state
    something you believe is already guaranteed.
