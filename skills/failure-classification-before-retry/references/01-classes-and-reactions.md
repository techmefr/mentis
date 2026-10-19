# failure-classification-before-retry §1 — The classes and the reaction each earns

> Part 1 of `skills/failure-classification-before-retry`. Read it before writing a retry or fallback.
> Sources, all read 2026-10-19: Google SRE book, "Handling Overload"
> (https://sre.google/sre-book/handling-overload/) and "Addressing Cascading Failures"
> (https://sre.google/sre-book/addressing-cascading-failures/); RFC 6585 section 4
> (https://www.rfc-editor.org/rfc/rfc6585#section-4); an AI vendor's error reference
> (https://platform.claude.com/docs/en/api/errors). Sentences marked "own guidance" are ours.

1. **Sort the failure by scope before reacting.** The overload chapter's central distinction: when a large share
   of a dependency's capacity is overloaded, a retry cannot help and the error should bubble up; when only a
   small part is, retrying (often landing on a different instance) is the right move. The same question
   applies to every class below: whose problem is it, the request, one credential, one instance, or the whole
   dependency?
2. **Permanent errors are never retried.** The cascading-failures chapter says to separate retriable from
   non-retriable errors and not to retry permanent errors or malformed requests, because they will never
   succeed. A bad request, an authentication or permission failure and a missing resource belong here. The
   reaction is to stop and surface the error with its body, plus the fix owner (the caller for a malformed
   request, whoever holds the key for an authentication one).
3. **Rate limiting is about the caller, and it says when to come back.** RFC 6585 defines the "too many
   requests" status as the server telling a user they sent too many in a period, optionally with a header
   saying how long to wait, and it leaves how the server counts to the server. Reaction: honour the hint when
   present; otherwise back off. Own guidance: slow the whole caller, not only the failing call, since the
   limit is usually shared across calls.
4. **A limit that is not a rate may look like one.** The vendor's reference lists a tier spend cap that comes
   back under the same status as a rate limit but without a wait hint, and "keeps failing until access
   resumes". The same page lists a user-set spend limit as a plain invalid-request status. Reaction: a rate
   limit with no hint that persists is a quota or budget wall, not a burst; stop retrying and tell a person
   (see `skills/spend-guard-fail-closed`). Check the vendor's own table for each dependency, since the same
   code means different things across vendors.
5. **Billing and permission failures are account-level, not request-level.** The vendor documents a payment
   failure as its own class. Reaction: take that credential out of rotation, do not wait it out, and do not
   count it against the provider's health.
6. **"Overloaded" is its own class, distinct from "broken".** The vendor documents a temporarily overloaded
   status, observed across all users, apart from an internal error and a timeout. Reaction: back off, shed or
   defer work; the SRE chapter adds that a backend under overload should say "overloaded, do not retry" when
   many requests are already retries, so that clients stop amplifying.
7. **Server-side errors and timeouts: retry with backoff, within a budget, and watch the scope.** The vendor's
   page recommends exponential backoff for an internal error and suggests streaming for long requests that
   time out. Own guidance: a timeout with no response leaves the outcome unknown; retry it only if the call is
   safe to repeat.
8. **A concurrency or capacity refusal means "healthy but busy".** Own guidance, from a gateway's resilience
   guide (one maintainer's doc, not independently verified): when the refusal says too many parallel
   requests, the dependency is fine. Fail over or queue now, give that path a short pause, and do not climb
   the long backoff ladder or count it as an outage.
9. **A failure after success headers belongs to the stream.** The vendor says an error can arrive after a
   successful status when a streamed response is under way, and it does not follow the status-code path.
   Reaction: handle in-stream error events separately; do not assume that a good status means a good result.
10. **A slow turn is not a failed account.** Own guidance, same gateway guide: a long reasoning or generation
    step that produces nothing yet is a property of the request. Time the request out by its own budget, but
    do not mark the credential unhealthy because of it.
11. **Scope the damage by state kind.** Keep three scopes in the recorded state: dependency-wide (a breaker),
    one credential or instance (a cool-down), one request (nothing recorded). A failure that belongs to the
    request must not be written to the other two.
12. **Terminal states are not cool-downs.** Banned, revoked, expired, credit exhausted, discontinued: these
    persist until a person or a credential change clears them. Recording such a state as a timed wait makes it
    heal itself on a timer and retry a dead credential forever (own guidance, from the gateway guide).
13. **Classify by the structured field, then by the body, never by guessing text.** Use the status and the
    error type; read message text only to separate cases the type cannot (for example the concurrency refusal
    in point 8), and make that text match narrow, tested and replaceable. An unclassified failure takes the
    stop-and-report reaction.
14. **A valid empty result is a result, not a fault.** Own guidance: a normal terminal marker with no content
    can be legitimate; whether to retry is decided by proof of a normal ending (the dependency's own
    completion signal), not by the provider's name or by how much text came back.
