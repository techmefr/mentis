# agent-sandbox-egress-pitfalls §2 — Egress

## 2.1 An allowed domain is an open door for data
1. **The domain allowlist controls where a connection goes, not what it carries.** The runtime does not
   inspect traffic through its proxy, and its README warns that allowing a broad domain such as a code
   host lets a process push to any repository there.
2. **Allow the narrowest hosts that work** (own guidance), and prefer fetching dependencies from a mirror you
   operate over allowing a public registry's whole domain. Wildcard entries on a domain whose DNS you do not
   control are called out as a risk for LAN services.
3. **Review the denials and the attempts.** The runtime records violations; for audit of what was allowed, the
   README points to a custom proxy with logging as the way (its own support for that was not yet in the new
   configuration format when read).

## 2.2 Fronting, inspection and resolved addresses
1. **Domain fronting** can get around filtering by name, according to the README's warning.
2. **A content-inspecting layer is a separate control.** The README describes optional TLS termination with a
   request filter for library users, and a custom MITM proxy as the way to filter specific API calls. Say
   which one you have; the default proxy does not look at content.
3. **Resolved-address check.** Allow and deny lists match by name, and whoever controls a permitted name's DNS
   controls what it resolves to. The runtime therefore resolves an allowed hostname once, drops denied
   addresses (loopback, link-local, multicast, the host's own addresses and several cloud-metadata endpoints)
   and dials an address that passed. Private-use ranges are not denied by default; list them in
   `deniedResolvedAddresses` when names must stay out of them. The check is not applied to traffic leaving
   through a parent or MITM proxy, which owns its own address policy.

## 2.3 How traffic reaches the proxy
1. **Isolation is by environment, namespace or OS filter, per platform.** On Linux the network namespace is
   removed and traffic goes over Unix sockets to proxies on the host; on macOS the profile allows only a local
   proxy port; on Windows an OS-level filter blocks connections of the sandbox account except to the proxy
   ports. Proxy variables point tools at the proxies, and on Windows the filter is the boundary.
2. **A tool that ignores the variables fails; it does not bypass.** The README lists this as a known limit on
   Linux (programs that do not respect the variables cannot connect). Plan for tools that need special
   handling: ssh reads no proxy variable (the runtime injects a `GIT_SSH_COMMAND`), and JVM tools needed an
   injected agent.
3. **Other TCP traffic goes through a SOCKS5 proxy,** HTTP and HTTPS through an HTTP proxy.
4. **An external proxy changes what applies.** With an external HTTP proxy port named, per-command allow lists
   are not applied.
5. **Local binding is a permission.** `allowLocalBinding` defaults to false; on macOS it also lets the
   sandboxed process connect to loopback ports without going through the proxy.
