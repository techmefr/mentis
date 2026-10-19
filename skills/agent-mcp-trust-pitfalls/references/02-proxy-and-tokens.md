# agent-mcp-trust-pitfalls §2 — Proxy servers and tokens

An MCP server that fronts another service's API usually has one registered client at that service and many
callers of its own. Most of the failures below come from forgetting that those are different parties. All
facts here are from the protocol's security best-practices page, revision 2026-07-28.

## 2.1 Confused deputy and consent
1. **The attack needs four conditions together:** the proxy uses a static client ID at the third-party
   authorisation server, lets clients register dynamically, the third party sets a consent cookie after the first
   authorisation, and the proxy has no per-client consent of its own. An attacker's client then gets a code
   without the user seeing a consent screen.
2. **Per-client consent, in the proxy, before the third-party redirect.** The page requires a registry of
   approved client IDs per user checked first, stored server-side or in server-specific cookies, and a consent
   page that names the client, shows the requested third-party scopes and the registered redirect address,
   has CSRF protection and cannot be framed.
3. **Consent cookies** must use the `__Host-` prefix, `Secure`, `HttpOnly` and `SameSite=Lax`, be signed or
   session-backed, and bind to the specific client ID.
4. **Redirect address:** exact string match with the registered one, no patterns or wildcards, and a changed
   address needs a new registration.
5. **State value:** cryptographically random per request, stored server-side only after consent is approved,
   set immediately before the redirect to the third party, checked at the callback, single-use and short-lived.
   Setting the tracking cookie before consent makes the consent screen ineffective, per the page.

## 2.2 Token passthrough
1. **A server must not accept a token that was not explicitly issued for it.** The page calls passing tokens
   through to a downstream API an anti-pattern and says the authorisation specification forbids it. Its listed
   risks: circumvention of controls that depend on audience, loss of audit trail (the server cannot tell
   clients apart and the downstream logs show another identity), a stolen token usable through the server as a
   proxy for exfiltration, and trust-boundary breaks.
2. **Check the audience claim on every token** (the page cites audience validation). Own guidance: a test with
   a token minted for another audience must be rejected, and the proxy should use its own separate token for
   downstream calls.
3. **State handles are not authentication.** The protocol revision is stateless; a server that mints a handle
   such as a cart or workflow ID must verify every request, must not treat possession of the handle as
   authentication, should use unguessable expiring handles and should bind each handle server-side to the
   authenticated user taken from the verified token.

## 2.3 Scopes
1. **Start with a minimal scope and elevate on demand.** The page asks for a small initial set of low-risk
   read scopes, elevation by targeted challenges when a privileged operation is first attempted, and servers
   that accept reduced-scope tokens.
2. **Avoid the common mistakes it lists:** publishing every scope in the metadata, wildcard or omnibus scopes,
   returning the whole catalogue in every challenge, and treating the scopes claimed in a token as sufficient
   without server-side authorisation.
3. **Log elevation events** (scope requested, subset granted) with correlation IDs, as the page says. Alerting
   on them is own guidance.

## 2.4 Discovered URLs
1. **Treat every URL taken from server metadata as attacker input.** The page lists the `resource_metadata`
   URL, the authorisation server URLs and the endpoints in authorisation server metadata as fetched
   from a possibly malicious server, pointing at internal addresses, cloud metadata, local services, DNS that
   changes between check and use, or redirect chains.
2. **Mitigations it lists:** HTTPS only in production (plain http only for loopback in development), block
   private, loopback and link-local ranges, apply the same checks to each redirect hop (consider disabling
   automatic redirects), route through an egress proxy, and pin DNS results between check and use. It warns
   against hand-written IP validation because of encoding tricks (octal, hex, IPv4-mapped IPv6). Documentation
   addresses such as `192.0.2.10` and `198.51.100.7` are the test values to use here (own guidance).
3. **Validate the authorisation URL before opening a browser.** The page requires only `http` and `https`
   schemes (plain http only for loopback in development), rejection of `javascript:`, `data:`, `file:` and
   similar schemes by allowlist, and no shell to open the URL (a shell can run parts of a crafted URL).
4. **Mix-up:** the page says to bind the response to the authorisation server the client recorded before
   redirecting, and notes this depends on honest servers emitting `iss`, and that PKCE alone does not stop it.
