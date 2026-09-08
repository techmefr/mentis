# code-baseline §4 — Boundaries

> Section 4 of `skills/code-baseline`. Read it when an external API, a file format or a third-party payload is consumed. The other sections and the guardrails stay in `SKILL.md`.

1. **Every call to an external HTTP API goes through a dedicated client object** — never a raw
   `Http::get` / `fetch` / `axios.get` / `requests.get` at a call site. The client owns the base URL (from
   config), authentication (token attachment, refresh, signing), the timeout and retry policy, the mapping
   from HTTP status and error payload to **named exceptions** (§3), and the typed request and response shapes.
2. **The order to choose it in**: the vendor's **official SDK** if one exists — don't reimplement what the
   provider maintains; otherwise a **thin client inside our own codebase**; and **avoid unofficial community
   wrappers** whose maintenance you don't control. An in-project client you own beats a stranger's abandoned
   one.
3. **This is rule B in code** (`CONVENTIONS.md`): the third party's breaking change hits one file. Scattered
   raw calls mean the endpoint is hard-coded in three places, one call site forgets the auth header (a silent
   401 in production), timeouts drift so the same outage looks different from each site, error handling is a
   coin flip per site, every consumer reads `body['data']['user']['id'] ?? null` with the schema living in
   people's heads, and the tests fake five different HTTP shapes instead of one client.
4. One client per external system, not one per endpoint. A class talking to three APIs is a god class (§2.9).
5. **Set the timeout explicitly.** Several HTTP clients default to none, so a dependency that stops
   answering — without refusing the connection — holds your request thread until something else gives up.
   That is how another company's incident becomes your outage, and it is the single cheapest line in the
   client.
6. **An external call fails in five ways, not one**: timeout, refused connection, 5xx, rate limit,
   malformed body. One catch-all treats a rate limit as a bug and a bug as a rate limit, so the retry
   policy is wrong for both — and the mapping to named exceptions (§3.2) is what lets each caller respond
   to the one it can do something about.
7. **Retry only what is retryable, with backoff and a cap.** Retrying a rejected request never succeeds and
   turns one bad call into a loop; retrying without backoff turns a dependency's brief overload into a storm
   that keeps it down, with every client in the fleet synchronised. And anything retried after a timeout may
   already have been applied, so an outbound write carries an idempotency key — otherwise the retry is a
   second payment.
8. **Decide what happens when the dependency is down.** Degrade, queue, or fail with a sentence the user can
   act on — that is a product decision, and not making it means it is made by whatever the stack trace does.
   A breaker that stops calling a dead service is worth having before the incident, not during it.
9. **Credentials come from configuration, and never into a log.** The client is the one place that touches
   them, which is also the place most likely to log a whole request while being debugged. Log the endpoint,
   the status and a correlation id; a full request or response body puts credentials and personal data into
   a system with different readers and different retention (§3.5).
10. **Test the client at the transport layer, not by mocking the client.** A test that fakes your own client
    exercises none of the thing worth testing — the status-to-exception mapping, the retry policy, the
    parsing of an error payload, the timeout. Fake the HTTP layer underneath it and assert that a 429
    becomes the rate-limit exception, that a malformed body fails loudly, and that the failure path is
    covered (§6.1).
11. **Where a client is overkill**: a one-off maintenance script hitting one endpoint once; a **webhook
    receiver** (the API is calling *us* — we're the server, there's no client); a liveness ping that only reads
    200/non-200; and pre-production exploration in a scratch file before the client's shape is known.
12. **A webhook receiver has its own three rules**, being the same boundary in the other direction: verify
    the signature *before* trusting any field, deduplicate by the sender's event id because delivery is
    at-least-once, and acknowledge fast then process asynchronously — a slow handler makes the sender retry,
    which is how one event becomes six.
13. **Anything parsed from disk or the wire is wrapped in a typed object** before use — a config file, a
    manifest, a plugin descriptor, a schema. A class with named accessors, a struct, a validated model,
    immutable by default.
14. The reason is the same shape as §4.3: `data['name']` may be a string, null, absent or a typo **at every
    call site**, while an accessor is checked once; the parse call stops being scattered; a default lives on
    one accessor instead of being duplicated as `?? 'layer'` five times and diverging; a derived value (split
    a `vendor/package`, slugify, normalise case) is a method rather than a repeated expression; renaming a key
    in the file becomes a one-class change; and the IDE and the type checker stop going dark, which they do
    the moment a raw map escapes.
15. **Validation has a home**: the factory fails fast on a missing required field or a wrong type, instead of
    each consumer inventing its own "is this safe to read" check. A response shape changing is otherwise
    silent — the field arrives as null, the null propagates, and the failure surfaces several layers away
    from the boundary that could have named it.
16. **A time crossing a boundary is parsed to an absolute instant.** A string without an offset means
    whatever the receiving process's timezone happens to be, so the same payload is interpreted differently
    in production and in a test — and the difference is an hour twice a year, which is the hardest kind of
    bug to be shown.
17. **Our own public surface is a boundary too**, with the same asymmetry: we can change a caller we own and
    not one we don't. A breaking change there is a new version rather than an edit, and the error shapes it
    returns are part of the contract (§3.15).
18. **Where wrapping is overhead**: a single read at a single call site in a short script; data the program
    intentionally treats as opaque; and very large or streamed files, where materialising one object is the
    wrong move.
