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
   `deniedResolvedAddresses` when names must stay out of them. Cloud check (AWS instance-metadata page, read 2026-10-20): the metadata service sits at a link-local IPv4 address and, on some instance types, also at an IPv6 address in a private-use range (`fd00:ec2::254`), so a deny list holding only the IPv4 address leaves the IPv6 one reachable when private-use ranges are allowed; list both. The pages also say a request from a container can get no response when the token reply hop limit is 1 (the launch default unless the image is set to IMDSv2-only, then 2) and recommend 2 for containers; that raising it also lets any process in the container reach the credentials is own reasoning, the pages read do not state it. The check is not applied to traffic leaving
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

## 2.5 When the sandbox is a pod or a VM
Facts from documentation read 2026-10-20 (Kubernetes network policy page, Firecracker design page, gVisor security page, Docker engine security and seccomp pages), restated:
1. **A pod is open for egress until a policy selects it, and a policy does nothing without a network plugin that enforces it.** Once a policy names egress for a pod, only the allowed connections and their replies pass; policies add up, so one extra policy can only widen. A default-deny egress policy also blocks name lookups, so the cluster resolver must be allowed on its own. The policy objects take pod and namespace selectors and address ranges, not domain names, so a domain allowlist needs a proxy or a plugin extension, not the standard object. Check: from inside a test pod, connect to an address the policy should refuse.
2. **A microVM monitor does not filter network traffic.** The Firecracker design page treats everything the guest sends as untrusted and says egress must be filtered on the host; its isolation is the virtualisation boundary, a minimal device set and a per-thread syscall filter on the monitor.
3. **A userspace kernel narrows the syscall surface but is not a whole defence.** The gVisor page says no application syscall goes to the host directly, and that hardware side channels, host-level attacks and resource exhaustion are outside its model: cgroups and network policy still have to be applied around it, and a sandbox does not replace a sound architecture.
4. **A plain container shares the host kernel and keeps a default syscall filter.** The Docker seccomp page says the default profile blocks a few dozen of the several hundred syscalls (mount, bpf, keyctl, perf events, io_uring among them), and that running unconfined is an explicit option; the engine security page says anyone who controls the daemon is effectively root on the host, that mounting the host root gives the container the host filesystem, and that capabilities should be dropped except those a process needs.

## 2.4 Tools that run on the vendor's side
Source, read 2026-10-20: comments and configuration in the daily digest and triage agents of
anthropics/claude-quickstarts (MIT). Sentences marked "own guidance" are ours.
1. **A search or fetch tool run by the model vendor does not go through your sandbox.** The sample's own comment:
   the toolset's web search and web fetch run on the vendor's servers, outside the sandbox, so the environment's
   domain allowlist does not cover them. Every other rule in this section constrains the sandbox's traffic and
   none constrains theirs.
2. **Text the agent reads can then send data out.** With such a tool enabled, a sentence in a chat message, a pull
   request or an error report can ask for a lookup whose address carries what the agent has read. That is the
   exfiltration path of `llm-app-prompt-injection-and-exfiltration-pitfalls`, with no sandbox in the way.
3. **A second agent product states the same boundary in its own sandbox documentation (read 2026-10-20):** its sandbox covers shell commands and their child processes only; its file tools, web fetch and search tools, tool servers and hooks run outside it under permission rules, and the sandbox domain allowlist does not limit the web fetch tool. The pattern is general: list what runs inside and what runs beside the sandbox. **Turn them off when the job does not need them.** The sample's agents that read internal sources disable both
   tools and say why in a comment. Check: list the tools the platform runs for the agent, whoever runs them, and
   ask of each "where does this connect, and who enforces the list?"
4. **If one is needed, scope it.** Own guidance: allow it only in a run that reads no untrusted text, or restrict
   the domains it may reach in the platform's own setting if one exists, and test that setting on its own, as it
   is separate from the sandbox allowlist.
5. **The same applies to remote tool servers you attach.** A remote tool server executes on someone else's host;
   what it can reach is decided there (`agent-mcp-trust-pitfalls`).
