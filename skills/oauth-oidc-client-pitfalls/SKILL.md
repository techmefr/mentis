---
name: oauth-oidc-client-pitfalls
description: "Use when code signs users in through an external identity provider (Sign in with Google or GitHub, an OIDC client, an OAuth callback route): state and PKCE per attempt, the exact callback checks, never treating an access token as a session, unverified provider emails, and the session and CSRF rules that follow a login."
---

# oauth-oidc-client-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the client side of the authorization code flow: the code that
sends the browser to a provider and handles what comes back. `skills/jwt-verification` owns the
cryptographic check of an ID token, `skills/auth-session-conventions` owns the token lifecycle and
storage, and `skills/security-hardening` owns every other trust boundary; this block owns the three places
a login integration goes wrong that none of them covers: the request that starts the flow, the callback
that finishes it, and the session and CSRF rules that decide whether the result can be hijacked. The
principles hold in any language and with any provider. Running your own authorization server is out of
scope.

## When
A diff adds or changes a login route that redirects to a provider, a callback route, an OIDC client
configuration, account linking by email, or the cookie and CSRF handling of a cookie-based session. Also
when a "Sign in with" button is added to an app that already has password accounts.

## Steps

**Read only the section the diff touches.** They follow the order of the flow.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The authorization request: state, PKCE, redirect URI, scopes | the login route is written or changed | [`01-authorization-request.md`](./references/01-authorization-request.md) |
| 2 | The callback: checks, code exchange, identity, unverified emails | the callback route or account linking is written or changed | [`02-callback-and-identity.md`](./references/02-callback-and-identity.md) |
| 3 | After login: session creation, cookies, CSRF, CORS | a session is created from the result, or a cookie session gains a form or API | [`03-session-and-csrf.md`](./references/03-session-and-csrf.md) |

## Output / checkpoint
For each provider in the diff: where the state and the code verifier are stored and when they are
discarded, the exact checks the callback makes before exchanging the code, which provider field the
account is keyed on, what happens to a user whose email is not verified, and how the session is created
and protected. Evidence is a replay of the two failure paths (a callback with no state, and one with
another browser's state), each refused.

## Guardrails
- Never skip the state check because the provider "does not require it" (§1.1, §2.1).
- Never use an access token as the user's session (§2.4).
- Never link or create an account from an email the provider did not mark as verified (§2.6).
- Never log, echo or put a code, a token or a verifier in a URL you control (`skills/auth-session-conventions`
  §2.1).
- A provider-specific behaviour (which providers require a client secret with PKCE, which expose a
  verified flag) is read from that provider's documentation, not from this block.
- Do not carry over the claim that validating an ID token signature is optional on a server: it is not,
  see `skills/jwt-verification`.

## Origin
Rewritten from the OAuth, sessions and CSRF pages of the Copenhagen Book (MIT) and the oauth2-proxy
configuration documentation (MIT), read 2026-10-15. One claim in the first source contradicts
`skills/jwt-verification` and was left out. The full provenance, what was removed and what is our own
guidance are in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
