# code-baseline §3 — Errors

> Section 3 of `skills/code-baseline`. Read it when an exception is thrown or caught. The other sections and the guardrails stay in `SKILL.md`.

1. **Never throw a language built-in with a message string** (`Exception`, `RuntimeException`, `Error`,
   `ValueError`). Define a named class that describes the failure and throw that.
2. **The reason is catch-by-type versus catch-by-message.** `catch (UserNotFoundException)` survives a
   refactor; matching on `"user not found"` breaks the day someone improves the wording. It also gives you:
   typed context on the exception (`->userId`, `->validationErrors`, `->retryAfter`) instead of details
   stringified into a message and re-parsed; a clean mapping layer (not-found → 404, validation → 422); a log
   line that reads as a known domain outcome rather than a crash; one greppable name that finds every throw,
   catch, test and mention; and a stable assertion in tests.
3. **A hierarchy** when several failures share a category, so a caller can catch the category or the specific
   case.
4. **Four disguises that don't count.** A single mega-exception with a `code` field (enum-as-exception: it
   loses every benefit above); a catch-and-rethrow that wraps into a generic type (wrap into a *named* one);
   two throws differing only by message; and a project-wide `class AppException extends Exception` that
   everything throws — a rename, not a design.
5. **The message is for whoever debugs it; the sentence the user reads is the handler's decision.** Mixing
   the two guarantees the user-facing wording gets duplicated at the next throw site, and it cuts the other
   way too: internal detail must not reach the response (§4.1's client is where that mapping belongs). A
   corollary that costs people real incidents — **no secret, token or personal datum in a message**, because
   the message goes to the log and the error tracker, which have different retention and different readers
   than the request did.
6. **Catch narrowly, or you catch your own bugs.** A broad catch around a block that contains your logic as
   well as the risky call swallows the typo, the null dereference and the wrong-argument mistake along with
   the failure you were expecting — and it reports all of them as that failure. The scope of a `try` is part
   of its meaning: wrap the call, not the paragraph.
7. **An empty catch is a decision, and it has to look like one.** Most languages offer a way to say
   "ignore, deliberately" — a named no-op, a comment-free explicit discard, a specific narrow type. A bare
   swallow is indistinguishable from a forgotten branch, and it is the single most effective way to make a
   failure undiagnosable, because there is no evidence anywhere that it happened.
8. **Catching to log and rethrow at every layer reports one failure five times.** It also multiplies the
   stack traces so that finding the origin means reading all of them. Report where the decision is made —
   once, at the boundary that knows what to do about it — and let the failure travel untouched in between.
9. **Preserve the cause when you wrap.** A wrapping exception that drops the inner one keeps the domain
   meaning and throws away the stack, so the log says "payment failed" and nothing about the DNS error
   underneath. Every language has the mechanism; using it is the difference between a name and a diagnosis.
10. **Exceptions are for the exceptional.** A search that matches nothing, a validation that rejects input,
    a cache that misses — those are results, and expressing them as throws makes the normal path run through
    the failure machinery, where it is slower, harder to read and easily caught by someone else's broad
    catch. `python-conventions` §2 covers the failures-as-values form for the languages that prefer it.
11. **An expected failure is not a defect.** Reporting every rejected form and every stale link beside real
    exceptions raises the volume until the real ones are unfindable — the same harm as reporting nothing,
    reached from the other direction. Decide per failure class whether it is monitored or merely logged.
12. **Inside a transaction, a throw is the rollback.** Catching and continuing in there commits the
    half-finished unit of work the transaction existed to prevent. The other half of the same rule:
    irreversible side effects — a mail, a queued job, an outbound call — belong outside the transaction,
    because a rollback cannot recall an email.
13. **The failure path has cleanup obligations.** A lock, a file handle, a temporary file or a connection
    acquired before the throw is still held after it unless the language's `finally`/`defer`/scope mechanism
    releases it. This is the leak that only appears under load, because it needs failures to accumulate.
14. **Anything retried is idempotent.** A retry re-runs everything before the failure point, so a partially
    applied effect is applied again — and "it only fails rarely" is not an answer, since rare is exactly
    when nobody is watching the second run.
15. **A failure crossing a process boundary loses its type.** Over HTTP, a queue or an event bus, the class
    name does not survive, so the contract is a stable machine-readable code plus the fields the caller needs
    — never a human sentence the other side has to match on, which is point 2's mistake rebuilt across the
    network.
16. An error crossing a public boundary is part of that boundary's contract, and gets the same care as a
    return type. That includes being tested (§6.1): the failure path is asserted, or the first refactor
    quietly turns the throw into a returned error object and nothing anywhere goes red.
