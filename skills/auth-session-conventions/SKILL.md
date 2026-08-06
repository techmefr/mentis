---
name: auth-session-conventions
description: Use when touching authentication, sessions, tokens or permission checks (login, refresh, logout, guards, middleware), the rules that keep an auth flow from breaking silently. Complements api-design (contracts) and the per-stack conventions blocks (idiomatic code) on the one surface where a regression is invisible until it locks users out.
---

# auth-session-conventions

Step 6 of the pipeline (`WORKFLOW.md`), on the auth surface specifically. Auth is the one place
where a regression **doesn't show up as a failing test**: the happy path keeps working, and the
breakage only appears an hour later when the first token expires. This block exists because that
already happened to us: a refresh flow broken by a change, shipped, and left broken because
nothing in the normal loop observed it.

## When
As soon as a diff touches: a login/logout route, token issuing or renewal, session storage, an
auth middleware/guard, or a permission check. Also when adding a first protected route to a
service that had none.

## Steps

### 1. Token lifecycle: the expiry path is part of the feature
1. **Test the flow after expiry, not just after login.** A login that works proves nothing about
   the refresh. Force the expiry (shorten the TTL in a dev config, or fast-forward the clock) and
   replay the journey: this is the only way to observe the renewal path.
2. **One refresh in flight at a time.** Several parallel requests hitting a 401 together must not
   each fire their own refresh: queue them behind a single renewal, then replay them. Without
   that, concurrent refreshes race and invalidate each other's token.
3. **A failed refresh logs out cleanly**, it never retries in a loop: a refresh that 401s and gets
   retried indefinitely spins forever and hides the real cause.
4. **The expiry margin is explicit**: renew shortly *before* expiry, never exactly at it, or clock
   skew between client and server produces intermittent failures no one can reproduce.

### 2. Storage and transport
1. A session/refresh token lives in an **httpOnly cookie** (`Secure`, `SameSite`), never in
   `localStorage`: anything readable by JavaScript is readable by any injected script.
2. Never a token in a URL/query string: it lands in logs, in the browser history and in the
   `Referer` header.
3. Logout **invalidates on the server side** too: clearing the client store while the token stays
   valid server-side is not a logout.

### 3. Authorisation: the check lives on the server
1. Every permission check is enforced **server-side**; the frontend check only hides UI, it never
   grants anything: hiding a button is not a permission.
2. The permission name is verified against what the backend actually exposes, never guessed from
   the feature's name: a guard wired onto a permission that doesn't exist fails open or fails
   closed depending on the framework, and both are bugs.
3. Scoped access (per tenant/agency/organisation) is applied **in the query**, not filtered after
   the fact: filtering in the response means the data was already fetched, and one forgotten branch
   leaks it.

### 4. Verification before shipping
1. Replay the journey: login → expiry → refresh → logout, plus one protected route with an
   insufficient permission (expect a clean refusal, not a crash).
2. Replay it a second time **concurrently** (two tabs on the same session) if the diff touched the
   refresh: that's where the race shows up.

## Output / checkpoint
The expiry/refresh path was observed, not assumed: evidence attached (log, network trace, or
screenshot of the renewed request succeeding). No auth diff reaches `gate` with only the login
path exercised.

## Guardrails
- Never weaken a check to make a test pass: a test that only goes green with the guard removed is
  reporting a real problem.
- Never invent a permission name to unblock yourself: ask what the backend exposes.
- Rotating or revoking credentials/secrets in a shared environment is a **human decision**, not
  something the agent does on its own initiative.
- This block covers the application-level flow. Provider configuration (SSO, identity provider,
  realms) is infra reality and stays outside this repo.

## Origin
Gap found while scouting a market per-technology agent catalogue (separate `jwt`, `oauth-oidc`,
`keycloak` and `auth0` agents, with no equivalent anywhere in our roster), crossed with a
documented internal incident: a token refresh flow broken by a change, merged, and left broken
because the normal loop never observed the post-expiry path. The per-provider agents were **not**
retained (per-library fragmentation, against our per-role doctrine); what's kept here is the
flow-level discipline that the incident showed was missing. Cookie/transport rules follow OWASP
session-management guidance.
