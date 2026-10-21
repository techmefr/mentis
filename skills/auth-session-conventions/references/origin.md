# auth-session-conventions: origin and source stamps

> Provenance of `skills/auth-session-conventions`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Never run by us.

## Original origin text
Gap found while scouting a market per-technology agent catalogue (separate `jwt`, `oauth-oidc`,
`keycloak` and `auth0` agents, with no equivalent anywhere in our roster), crossed with a
documented internal incident: a token refresh flow broken by a change, merged, and left broken
because the normal loop never observed the post-expiry path. The per-provider agents were **not**
retained (per-library fragmentation, against our per-role doctrine); what's kept here is the
flow-level discipline that the incident showed was missing. Transport rules follow OWASP
session-management guidance.

Section 4 is **not** sourced from the market: it's extracted from the two real implementations
already running on our own Nuxt frontends against a Laravel backend, read side by side. Where the
two disagreed, the stronger one became the reference and the reason is stated inline (single-flight
refresh: cross-context lock + cross-tab broadcast beats an in-memory promise). Where our own
practice is weaker than the generic rule, that gap is stated rather than smoothed over (§2.3, the
non-`httpOnly` cookie). The token-in-the-URL prohibition is written as a rule to hold precisely
because the surrounding practice on other teams goes the other way.

Re-checked directly against the OWASP Session Management Cheat Sheet on 2026-08-10: three real gaps
closed — renewal/invalidation on a privilege-level change rather than waiting for natural expiry (§1.5),
an absolute session lifetime on top of the rolling TTL (§1.6), and `Clear-Site-Data` on logout (§4.8).
The CSRF note in §2.2 was added the same pass: the cheat sheet leans on `SameSite` for CSRF defence,
which this block already set — what was missing was saying explicitly *why* the Bearer-header transport
closes the classic CSRF vector too, rather than leaving a reader to wonder if a CSRF token is also
needed. Session-ID-regeneration-at-login and idle-timeout ranges stay out: they're framed for a
server-side session store, and this reference flow is a stateless bearer token, where the equivalent
guarantee is already the expiry-margin/refresh discipline in §1.

Section 6 added 2026-10-02 from two IETF documents read that day, in full text: RFC 8252 (OAuth 2.0 for native
apps, a best current practice) and RFC 7636 (proof key for code exchange). Mechanisms restated, no wording
copied. Not read: the OAuth 2.0 security best current practice document, the device authorization grant and the
OpenID Connect specifications, so nothing is claimed here for the device flow (a command-line tool without a
browser) or for token binding. Expiry: if either RFC is obsoleted by a later one, re-read §6 first.

## Verification pass 2026-10-20
Read for facts only, restated in our words, no text copied. IETF and W3C documents and a NIST guideline; no licence file applies.

| Source | What it gave |
|---|---|
| RFC 6750 (bearer tokens), sections 2.3, 5.2, 5.3 | Tokens in a query string are discouraged because URLs are logged; TLS required; short lifetimes |
| RFC 9700 (OAuth security BCP), sections 3 and 4.2 | No access tokens in query parameters; logs and history as leak paths |
| NIST SP 800-63B-4 (pages.nist.gov), sections 2, 5.1, 5.2 | Overall and inactivity timeouts, HttpOnly, `__Host-`, SameSite, opaque identifier, erase the secret at logout |
| W3C Clear-Site-Data working draft (2017) | What each directive clears, whole registered domain, best effort |
| RFC 6265bis (first 100000 characters) | Cookie prefixes, SameSite, 400-day cap (read, no change needed) |

- Confirmed and credited: absolute lifetime (section 1.6), no token in a URL (2.1), HttpOnly as the stronger target (2.3), server-side logout (2.5), `Clear-Site-Data` (4.8, with the domain-wide caveat added).
- Not found in NIST SP 800-63B-4 section 5: a rule to change the session secret on a privilege change (point 1.5 stays unsourced).
- Still unsourced: the expiry margin (1.4), the cookie-plus-Bearer CSRF reasoning (2.2) and the localStorage claim, token-in-log paths (2.4; RFC 9700 only names logs), authorisation in the query (3.3), the reference flow and single-flight refresh (section 4, our own implementations), the verification replay (5).
- The OWASP session cheat sheet is share-alike and was not reopened.
