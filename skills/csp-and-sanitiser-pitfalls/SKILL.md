---
name: csp-and-sanitiser-pitfalls
description: "Use when a web app sets a Content-Security-Policy or the other security response headers (Helmet in Express, or the same headers set by any server) or when untrusted HTML is sanitised with DOMPurify before it reaches the DOM: nonces, report-only rollout, what a header library does not validate, HSTS and upgrade-insecure-requests in development, sanitise-last, the server-side DOM, widening the allow-list, hooks, Trusted Types."
---

# csp-and-sanitiser-pitfalls

A defensive block for the two browser-side layers that sit behind output escaping: the response headers that
tell the browser what a page may load, and the sanitiser that cleans HTML you chose to render unescaped. Neither
replaces escaping at the point of output (`skills/security-hardening` §2); both exist for the day a value got
through. The two sections are independent. The examples use Express with Helmet and the browser DOMPurify API;
the ideas hold with any server and any sanitiser. Header defaults and option names are version-bound and dated in
`references/origin.md`.

## When
- Adding or changing a `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options` or
  `Referrer-Policy` header, or putting a header middleware in front of an app.
- A page renders user-supplied or third-party HTML (comments, a rich-text field, an email body, a markdown
  preview) with an "unescaped" facility.
- A sanitiser is configured, wrapped in a policy, run on the server or called from a hook.
- A CSP violation is "fixed" by loosening the policy.

## Steps

**Read only the section the change touches.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | CSP and headers: default policy, nonce, report-only, validation gap, frame-ancestors, HSTS and upgrade-insecure-requests in development | a response header policy is written, loosened or reviewed | [`01-csp-and-headers.md`](./references/01-csp-and-headers.md) |
| 2 | Sanitiser: sanitise last, `removed`, server-side DOM, profiles vs allow-list, risky toggles, Trusted Types, hooks, non-re-entrancy | untrusted HTML is rendered, or the sanitiser config or runtime changes | [`02-sanitiser.md`](./references/02-sanitiser.md) |

## Output / checkpoint
For each page type: the headers as actually sent (read them from a response, not from the config), whether the
policy is enforced or report-only, and which directive allows each external origin. For each sanitiser call
site: the configuration in force, where the output goes, whether anything touches the markup afterwards, and on
the server which DOM implementation and version supplies the window. Evidence is a response header dump and a
replay of one hostile string through the real render path in a local or preview environment, never a shared or
production one.

## Guardrails
- Never add `'unsafe-inline'` or a wildcard to `script-src` to silence a violation; fix the source of the inline
  script or give it a nonce (§1.3, §1.4).
- Never assume a header middleware validated the policy it was given (§1.6).
- Never enable HSTS preload or `includeSubDomains` before checking every host under the name serves HTTPS
  (§1.10).
- Never modify, concatenate or re-parse HTML after sanitising it (§2.1).
- Never take a security decision from `DOMPurify.removed` (§2.2).
- Never run DOMPurify server-side on a DOM implementation the project documents as unsafe, or on an old one
  (§2.3).
- Never combine `USE_PROFILES` with `ALLOWED_TAGS`, and never call `sanitize()` from inside a hook (§2.4, §2.11).
- Do not paste a real user's HTML, a real session token or a production header dump into a prompt or a fixture.

## Origin
Rewritten from the Helmet README (MIT) and the DOMPurify README (Apache-2.0, dual-licensed with MPL-2.0), read
2026-10-16. The full provenance, versions, what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
