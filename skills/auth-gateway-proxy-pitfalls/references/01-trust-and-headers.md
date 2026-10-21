# auth-gateway-proxy-pitfalls §1 — Trust and headers

> Section 1 of `skills/auth-gateway-proxy-pitfalls`. Read it when a proxy chain, a client-IP rule or a
> header the application trusts is added or changed. Flag names are oauth2-proxy's, at the commit in
> `references/origin.md`.

1. **Name the proxies that may send forwarded headers, or every peer can.** In reverse-proxy mode
   (`--reverse-proxy`), the setting `--trusted-proxy-ip` lists the direct proxy addresses or CIDR ranges
   allowed to supply `X-Forwarded-*` headers. The documentation says that when it is unset, oauth2-proxy
   currently trusts all source IPs (`0.0.0.0/0` and `::/0`) for backwards compatibility and logs a warning
   at startup, so a client that can reach the gateway directly may be able to spoof forwarded headers. List
   the direct peer and every trusted proxy hop that can appear in the forwarded chain, with narrow ranges.
2. **A trusted-IP list is an authentication bypass, not a list of proxies.** `--trusted-ip` lets matching
   clients skip authentication; the documentation says so in as many words, and tells you to configure
   `--trusted-proxy-ip` explicitly and to stop clients from reaching the gateway directly whenever the two
   are combined. A client IP is only as trustworthy as the chain that reported it (§1.1, §1.3). Prefer no
   trusted-IP rule, and where one is needed, list single addresses you control.
3. **Resolve the client address from the right end of `X-Forwarded-For`.** Per the documentation, the
   configured client-IP header is accepted only from trusted peers. For `X-Forwarded-For`, repeated header
   fields are combined in received order, then the chain is walked from right to left, skipping addresses
   covered by the trusted-proxy list; the first untrusted address is the client and entries to its left are
   ignored. In its example, where a trusted proxy appends the real client to a list whose leftmost entry is an internal address and whose next entry is `198.51.100.23`, the
   client is `198.51.100.23`, not the possibly forged leftmost entry. When every address in the chain is
   trusted the leftmost one is used. Any application or rule of yours that reads the leftmost entry
   reads the part an attacker writes.
4. **Overwrite single-value client-IP headers at the edge.** For headers such as `X-Real-IP`, the
   documentation says to configure the edge proxy to overwrite any value the client supplied. The default
   header oauth2-proxy reads is `X-Real-IP`, and the documented nginx setup overwrites it with the transport peer address and sets the user and email headers itself, never passing a client value through, so an edge that appends rather than overwrites hands the
   decision to the client. The same idea holds for any header the gateway or the app trusts for identity.
5. **Strip client-supplied identity headers before the gateway sets its own.** `--skip-auth-strip-headers`
   (default true) strips `X-Forwarded-*` style authentication headers and `Authorization` when they would
   be set by the gateway. Leave it on. The headers the gateway sets for the upstream (for example the
   forwarded user, email and groups from `--pass-user-headers`, default true) are only meaningful if a
   client cannot send the same names, which is what this setting and the edge rules enforce.
6. **The upstream must only be reachable through the gateway.** Own guidance, not a statement of the
   source: the application trusts the identity headers the gateway adds, so a network path that reaches the
   application directly lets anyone send those headers themselves. Bind the application to the gateway's
   network or a loopback address, and restrict it with network policy or a security group rather than by
   convention. The documentation's default listen address for the gateway itself is `127.0.0.1:4180`, the
   same idea one hop out.
7. **Forwarded tokens are a decision.** `--pass-access-token` (default false) sends the OAuth access token
   to the upstream and `--pass-authorization-header` (default false) sends the ID token as a bearer
   header. Own guidance: turn each on only for an upstream that calls something with it, and treat that
   upstream's logs and error pages as holding a credential.
8. **An insecure default is documented, not fixed for you.** The project's security policy says insecure
   default configuration options are not, by themselves, vulnerabilities. The trust-everything default of
   §1.1 therefore stays until you override it; do not wait for a release to change it.
