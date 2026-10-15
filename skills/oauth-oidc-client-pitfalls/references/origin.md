# oauth-oidc-client-pitfalls: origin and source stamps

> Provenance of `skills/oauth-oidc-client-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us against a real provider. Every source file
below was re-read in full on 2026-10-15 before a rule was taken from it, and the repository's LICENSE file
was read again for each.

## Sources (all read 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Copenhagen Book (`pilcrowonpaper/copenhagen`, commit `fb7eb3a`), pages `oauth.md`, `csrf.md`, `sessions.md` | MIT (LICENSE file, copyright 2024 pilcrow) | State and PKCE parameters, callback checks, the access-token-is-not-a-session rule, unverified provider emails and linking, discovery, session fixation, cookie attributes, CSRF defences, sudo mode |
| oauth2-proxy (`oauth2-proxy/oauth2-proxy`, commit `bea3f04`), `docs/docs/configuration/overview.md` | MIT (LICENSE file) | PKCE method values, the three `insecure` OIDC options and their documented defaults, cookie-name prefix advice |

## Removed in the verification pass
1. **"Validating an ID token with the provider's key is not strictly necessary for a server-side
   application using HTTPS"** (Copenhagen `oauth.md`). It contradicts `skills/jwt-verification`, which
   requires the signature, issuer and audience to be checked, and was not carried over. §2.7 points at the
   verifying block instead.
2. **The Copenhagen advice to skip PKCE when a provider does not require a client secret with it** is kept
   only as a provider-specific caveat (§1.4), not as a rule.
3. **The anti-CSRF Go samples and the session sample** were not used; only the prose. The Origin-check
   sample in `csrf.md` does not compile as written (`Header.Get()` without a key).

## Not verified
1. **Own guidance, flagged as such in the text:** the exact-string redirect URI (§1.6), minimal scopes
   (§1.7), discarding the state at the callback (§1.2), the login route mutating nothing (§1.8), fetching
   discovery documents from a configured HTTPS issuer only (§1.9), keying accounts on provider plus
   `sub` (§2.5), treating returned tokens as credentials (§2.3), the open-redirect check on a return-to
   value (§2.8) and the CORS allow-list rules (§3.7).
2. **The Copenhagen open-redirect page** referenced from `oauth.md` was not read.
3. **Option names and defaults** quoted from oauth2-proxy are those of the commit above and are version-bound.
4. **RFC 6749, RFC 7636 and OpenID Connect Core** were not read; the rules are taken from the sources above,
   which cite them. The `nonce` check (§2.7) is stated only as "check it if you sent one".

## Related blocks
`skills/jwt-verification`, `skills/auth-session-conventions`, `skills/security-hardening`,
`skills/credential-lifecycle-pitfalls`, `skills/auth-gateway-proxy-pitfalls`.
