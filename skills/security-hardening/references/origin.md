# security-hardening — origin and source stamps

> Provenance of `skills/security-hardening`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Rewrite of the `security-and-hardening` idea from a market generalist dev skill catalogue, which sat
unwritten in our backlog on the assumption that `seraph` and the native `/security-review` already
covered it. They don't cover the same moment: both look at code that already exists, and neither is
consulted while the boundary is being written. Underlying references are OWASP (Top 10, ASVS) and
OWASP's cheat-sheet guidance on escaping per context. The split enforced here — auth in its own
block, audit in `seraph`, writing-time checks here — is ours, and exists so that three blocks don't
restate the same OWASP list in three places.

Coverage check against OWASP Top 10 (2026-08-10): A02 (cryptographic failures) and A07
(identification/auth failures) stay out deliberately — they're `auth-session-conventions`' boundary, not
this one, per the split above. A09 (logging/monitoring failures) stays out too — that's
`observability-instrumentation`'s boundary. §2.4 (SSRF) was added because A10 was a real gap: the
trust-boundary definition already named "an outbound call with a user-supplied target" but no step
covered it, the one item on this list this block actually owns and hadn't written yet.

**Sectioned and deepened 2026-09-08.** The five inline sections moved to one file each under
`references/` and the router became a table of triggers. No section was added: the five are the shape of
a boundary — what comes in, where it goes, who is allowed, what the diff brings with it, and what you
owe before calling it done. Every section and point number was preserved: `business/data-protection`
cites §3 by number; §2.1 cites §1.3 here for identifiers that cannot be parameterised, and the coverage
check
above cites §2.4 as the SSRF rule it added.

**What the depth adds.** The original was a correct list of writing-time rules with one clause of reason
each. What it did not have is the case where each rule is *skipped* — because none of these fail loudly:
a missing authorisation declaration returns the right data to the developer who wrote it, an
over-inclusive serialiser renders a page that looks correct, and a concatenated query works until the
value changes. The additions that were real absences rather than elaborations:

- **§1**: that the boundary is the right place because it is *enumerable* where the set of inner call
  paths is not, so a scattered check can only be verified by reading everything; that the validated
  value has to be the one used, since re-reading the raw request further down means the guard and the
  use look at two different things; reject-don't-repair, where stripping characters produces something
  that passed validation and was never legal; that binding a request onto a model accepts fields the
  interface never shows — the shape is an allow-list of *fields*, not only of values; that size, count
  and nesting depth are part of the shape; that a value from another system is still untrusted, which is
  the point that gets skipped because the boundary is invisible in the call; and that a validation
  error echoing the rejected value has moved the payload somewhere new.
- **§2**: that the "can't contain user data" cases are exactly where point 1 fails, because the value
  is internal today and becomes a request parameter in the change that adds a filter; that the rule
  extends past HTML to every parser — regex, LDAP, NoSQL filter, log format, header; that escaping on
  input gives a database correct for one destination and wrong in the export; that joining a filename
  onto a directory does not confine it, so the check is on the *resolved* path; the open redirect as an
  output; secrets in URLs being copied into history, proxies, access logs and referrers; that an
  outbound call carries whatever credentials it was given, which is the half of SSRF an IP allowlist
  does not cover; and that a fetched response is untrusted input, size included.
- **§3**: authorising before the work, since a check after the read has already spent it and any early
  return or timing difference in between is an oracle; **default-deny**, without which "every endpoint
  declares its authorisation" is aspirational because nothing detects the one that does not; a
  permission not being a role; authorising the write on the row and not the collection; every *field*
  of a response being subject to the same decision as the endpoint; caller-supplied filters, sorts and
  includes as an authorisation surface; that a queue consumer, job, webhook or websocket message is not
  reached by HTTP middleware at all, and that a webhook's authorisation is signature verification; that
  an unguessable id raises the cost of enumeration and changes nothing about entitlement; and that the
  negative test is the only proof, since a positive one passes identically with no policy at all.
- **§4**: that a file served back is a stored output, so its content type is set from the validated
  type and user content is served as a download or from another origin; that an image, archive or
  document is parsed by a large library before any of your logic — decompression bombs, archive entries
  escaping extraction, external entity resolution; that a committed secret is committed forever and
  rotation is the fix rather than deleting the line; that an environment variable is readable by the
  crash reporter, the debug page and anything printing configuration; that a secret without scope and
  expiry makes rotation an outage, so it is deferred indefinitely; that the **lock file** is the
  inventory and the manifest is the smaller half; that a dependency's install step runs with your
  credentials before any review; and that removing an unused dependency is the cheapest security work
  available.
- **§5**: the distinction the section rests on — an invalid value exercises the validation, a hostile
  one exercises what happens when the validation is wrong; that a test beats a replay because it runs
  again, at the refactor where the guard gets moved; asserting the *absence* rather than the refusal,
  since a status check passes while the body still carries the record; verifying a whitelist by its
  edges; reading what got logged while testing, which is a different exposure from the one under test;
  that a tool's pass is a floor, not a result; and that a skipped replay is a known gap to be named,
  which is what keeps the checkpoint a record rather than a claim.

Router plus sections: 1,030 → 4,144.

**Status.** The sources are unchanged and still stand; the OWASP coverage check of 2026-08-10 is the
last one and remains valid, since nothing in this pass changed which items the block owns. The depth is
ours, written from the failure modes rather than from a source that can be re-checked — which is the
form `seraph` and a reviewer both need, and is not a substitute for the platform hardening this block
explicitly leaves outside the repo.
