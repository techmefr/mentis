---
name: auth-gateway-proxy-pitfalls
description: "Use when an authenticating reverse proxy or gateway (oauth2-proxy and its equivalents) sits in front of an application: which peers may supply forwarded headers, trusted-IP bypasses, path-based auth exemptions, redirect allow-lists, the flags that weaken verification, and cookie and refresh settings."
---

# auth-gateway-proxy-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the configuration of an authentication gateway: a proxy that
sends unauthenticated users to an identity provider and forwards authenticated requests, with identity
headers, to an upstream application. The code in the application is `skills/oauth-oidc-client-pitfalls`
and `skills/auth-session-conventions`; this block is about the proxy's own settings, which fail open
without any code being wrong. The worked source is the oauth2-proxy documentation, so rules name its
flags; every flag name and default is version-bound, and the principle behind each one applies to any
gateway. Cloud-specific identity-aware proxies and ingress controllers are out of scope.

## When
A diff adds or changes a gateway configuration file, its flags or environment variables, a reverse-proxy
snippet that forwards to the gateway or lets it forward upstream, a skip-authentication route, or a
redirect allow-list. Also when an app behind a gateway starts trusting an identity or client-IP header.

## Steps

**Read only the section the change touches.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Trust: forwarded headers, trusted proxies, trusted-IP bypass, identity headers | a proxy chain, a client-IP rule or a header the app trusts is added or changed | [`01-trust-and-headers.md`](./references/01-trust-and-headers.md) |
| 2 | Routes, redirects, weakening flags, cookies and refresh | an exemption, a redirect allow-list, a provider flag, the cookie secret or a refresh interval changes | [`02-routes-flags-and-cookies.md`](./references/02-routes-flags-and-cookies.md) |

## Output / checkpoint
For each gateway in the diff: the list of proxy addresses allowed to send forwarded headers, whether any
trusted-client-IP bypass exists and why, every authentication exemption with the path forms checked
against it, the redirect allow-list, the list of weakening flags and that none is set without a recorded
reason, and where the cookie secret comes from. Evidence is a request that spoofs a forwarded header from
an untrusted peer and one that reaches a protected path through an ambiguous form, both refused.

## Guardrails
- Never run a gateway with the "trust every source IP" default left in place when forwarded headers
  matter (§1.1).
- Never use a trusted-client-IP list as a list of proxies (§1.2).
- Never add an authentication exemption for a path form the gateway documents as ambiguous (§2.1).
- Never set a weakening flag to make a test pass; a provider that needs one is a recorded exception (§2.3).
- Never print the cookie secret, a client secret or a configuration dump with them into a log, a ticket
  or a prompt.
- Flag names, defaults and version gates change between releases: read the documentation of the version
  you run.

## Origin
Rewritten from the oauth2-proxy documentation (configuration overview, session storage, behaviour page and
security policy; MIT), read 2026-10-15. The full provenance, what was removed and what is our own
guidance are in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
