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
4. One client per external system, not one per endpoint. A class talking to three APIs is a god class (§2.6).
5. **Where a client is overkill**: a one-off maintenance script hitting one endpoint once; a **webhook
   receiver** (the API is calling *us* — we're the server, there's no client); a liveness ping that only reads
   200/non-200; and pre-production exploration in a scratch file before the client's shape is known.
6. **Anything parsed from disk or the wire is wrapped in a typed object** before use — a config file, a
   manifest, a plugin descriptor, a schema. A class with named accessors, a struct, a validated model,
   immutable by default.
7. The reason is the same shape as §4.3: `data['name']` may be a string, null, absent or a typo **at every
   call site**, while an accessor is checked once; the parse call stops being scattered; a default lives on
   one accessor instead of being duplicated as `?? 'layer'` five times and diverging; a derived value (split
   a `vendor/package`, slugify, normalise case) is a method rather than a repeated expression; renaming a key
   in the file becomes a one-class change; and the IDE and the type checker stop going dark, which they do
   the moment a raw map escapes.
8. **Validation has a home**: the factory fails fast on a missing required field or a wrong type, instead of
   each consumer inventing its own "is this safe to read" check.
9. **Where wrapping is overhead**: a single read at a single call site in a short script; data the program
   intentionally treats as opaque; and very large or streamed files, where materialising one object is the
   wrong move.
