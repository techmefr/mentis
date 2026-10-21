# agent-mcp-trust-pitfalls §2 — Proxy servers and tokens

An MCP server that fronts another service's API usually has one registered client at that service and many
callers of its own. Most of the failures below come from forgetting that those are different parties. All
facts here are from the protocol's security best-practices page, revision 2026-07-28, except where the authorisation
page of the same revision or another source is named; both pages were re-read on 2026-10-20.

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
2. **Check the audience claim on every token.** The authorisation page says servers must validate that a token was
   issued for them as the audience (resource indicators, RFC 8707), answer an invalid or expired token with 401, and
   must not accept or transit any other token; clients must send the resource parameter naming the server in both the
   authorisation and the token request. Own guidance: a test with a token minted for another audience must be
   rejected, and the proxy should use its own separate token for downstream calls.
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
   addresses such as `192.0.2.10` and `198.51.100.7` are the test values to use here: RFC 5737 sets aside three
   blocks for documentation (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24) and notes that this lowers the chance of
   clashing with real hosts; a test that must reach a blocked range needs the private ranges instead.
3. **Validate the authorisation URL before opening a browser.** The page requires only `http` and `https`
   schemes (plain http only for loopback in development), rejection of `javascript:`, `data:`, `file:` and
   similar schemes by allowlist, and no shell to open the URL (a shell can run parts of a crafted URL).
4. **Localhost redirect impersonation.** For clients that identify themselves by a metadata document at a URL, the
   page says the document proves control of a domain, not which local process listens on a localhost redirect address:
   an attacker can borrow a legitimate client's identity, bind any local port and receive the code. Its pointer is the
   authorisation specification's expectations of the authorisation server (extra warnings for localhost-only redirects
   and showing the redirect host). A server that accepts such client IDs can also apply domain trust policies:
   allowlists for protected servers, any HTTPS identity for open ones, reputation or age checks, and a prominent
   display of the client's host.
5. **Mix-up:** the page says to bind the response to the authorisation server the client recorded before
   redirecting, and notes this depends on honest servers emitting `iss`, and that PKCE alone does not stop it.
