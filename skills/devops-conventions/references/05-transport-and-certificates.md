# § 5 — Transport security in operation

> Section 5 of `skills/devops-conventions`. Read it when a diff configures a load balancer, a reverse
> proxy, an ingress, a certificate, a redirect or a domain. The application-side half (which headers the
> code asks for, cookies, mixed content) is `skills/security-hardening` §6; this is the half that lives
> in the platform.

1. **Every public endpoint is served over TLS, and the plain-HTTP listener does one thing.** It answers
   with a permanent redirect to the same host and path on the secure scheme, and nothing else: no content,
   no API, no health page that differs from the secure one. A second listener that serves real traffic
   is a downgrade path the first listener's certificate does not protect.
2. **Redirect once, to the final address.** A chain (plain to secure, bare host to the `www` host, old
   path to new) gives an attacker as many chances to intercept as it has hops and costs the user a round
   trip per hop. Normalise scheme, host and trailing form in a single redirect, and have a test that
   follows it.
3. **Strict transport security is a promise you cannot easily take back.** Once a browser has seen the
   header, it refuses plain HTTP to that host for the declared period, and a certificate that expires or
   a subdomain that cannot serve TLS becomes an outage with no click-through. Roll it out in steps:
   enable it with a short lifetime, confirm every host it covers (including subdomains, if you declare
   them) serves TLS correctly, then lengthen it. Preloading, which hard-codes the host into browsers, is
   the last step and effectively permanent: do it only when the whole domain tree is committed to TLS
   for good. The header is only honoured when sent over a secure connection, so it belongs on the secure
   listener only. Read the current requirements of the preload list before submitting; they change.
4. **Certificates are issued and renewed by automation, and renewal is monitored.** A certificate renewed
   by a person is one that expires on the day that person is away. Use an automated issuer, alert well
   before expiry on the *observed* certificate of each public endpoint (not on the issuer's
   job having run), and test that a renewal actually reloads the process or the proxy that holds it.
5. **Prefer modern protocol versions and drop the legacy ones deliberately.** Disable the protocol
   versions and cipher suites that current guidance has retired, take the baseline from an up-to-date
   published profile instead of from memory, and re-check it on a schedule, because the right answer
   changes. Do not hand-write a cipher list when a maintained profile exists.
6. **Terminate TLS in a known place and say what is behind it.** If the proxy terminates TLS, the hop
   behind it is either on a trusted private network or encrypted again, and the application is told the
   original scheme and client address by headers it trusts only from that proxy (`skills/security-hardening`
   §7.9). Traffic between services that carry credentials or personal data is encrypted too, and
   mutual authentication between services is preferred to network location as the proof of identity.
7. **Private keys are secrets with an owner.** They are generated where they will be used, are never
   committed, never copied into an image layer or a CI log, are readable only by the process that needs
   them, and are rotated on suspicion and on schedule (`skills/security-hardening` §4.6, §4.8).
8. **Check the outside, not the config.** After a change, fetch the public endpoint from outside the
   network and look at what a client sees: the redirect, the certificate chain and expiry, the protocol
   versions offered, the strict-transport header on the secure response and its absence on the plain
   one. Config that reads correctly can still be fronted by a different listener than you think.
9. **Name the DNS and the certificate authority policy that matter.** A CAA record restricts which
   authorities may issue for the domain, a dangling record that points at a decommissioned service can be
   claimed by someone else, and a wildcard certificate widens the blast radius of one leaked key. Each is
   a deliberate choice in the infrastructure code, not an accident of what was clicked.

**Sources:** RFC 6797 (HTTP Strict Transport Security); RFC 8446 (TLS 1.3) and the current Mozilla
server-side TLS guidance for protocol and suite profiles; RFC 8555 (ACME); RFC 8659 (CAA); RFC 9110
(redirect status semantics); OWASP Transport Layer Security and HTTP Strict Transport Security cheat sheets.
