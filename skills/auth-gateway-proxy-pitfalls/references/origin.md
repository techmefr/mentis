# auth-gateway-proxy-pitfalls: origin and source stamps

> Provenance of `skills/auth-gateway-proxy-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us against a deployed gateway. Every file below
was re-read in full on 2026-10-15 before a rule was taken from it, and the repository's LICENSE file was
read again.

## Sources (all read 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| oauth2-proxy (`oauth2-proxy/oauth2-proxy`, commit `bea3f04`), `docs/docs/configuration/overview.md` | MIT (LICENSE file) | Trusted proxies and trusted-IP warnings, the `X-Forwarded-For` walk, skip-auth path matching, the redirect allow-list footnote, the weakening flags and their defaults, header and cookie defaults, `--config-test` |
| the same repository, `docs/docs/configuration/sessions.md` | MIT | Cookie store versus Redis store, refresh and expiry recommendations |
| the same repository, `docs/docs/behaviour.md` | MIT | Authentication requirement, 401 versus redirect, invalid JWT handling |
| the same repository, `SECURITY.md` | MIT | Insecure defaults are not treated as vulnerabilities |

## Removed in the verification pass
1. **"Block direct access to the upstream"** was on the review list as a documented rule. No page read says
   it for the upstream; the nearest statement is about preventing clients from reaching the gateway
   directly. It is kept as own guidance (§1.6).
2. **Flag spellings from older oauth2-proxy releases** that the review remembered were dropped; only
   flags present in the file at the commit above are named.

## Not verified
1. **Own guidance, flagged as such in the text:** the upstream reachable only through the gateway (§1.6),
   forwarding tokens only when used (§1.7), method-qualified exemptions (§2.2), logging policy for headers
   (§2.10), and the exact-host redirect list (§2.6, the leading-dot behaviour itself is from the source).
2. **Flag names, defaults and the `0.0.0.0/0` trust fallback are version-bound** to the commit above; the
   documentation describes the fallback as "currently" in place.
3. **`docs/docs/features/endpoints.md`, the provider pages and the integration pages** (nginx, traefik,
   caddy) were not read; nothing here claims how a particular front proxy forwards or rewrites headers.
4. **The alpha configuration format** (`alpha_config.md`) was not read.

## Related blocks
`skills/oauth-oidc-client-pitfalls`, `skills/jwt-verification`, `skills/auth-session-conventions`,
`skills/security-hardening`.
