# agent-sandbox-egress-pitfalls §3 — Escalation paths

Even a tight list can contain an entry that hands back the control it limits. The README's security
limitations section names the first three.

## 3.1 Paths that lead out
1. **A container runtime socket is the host.** Allowing the Docker socket through the Unix-socket allowlist
   would effectively grant access to the host system.
2. **Writable files that something else runs.** Broad write permission on directories holding executables on
   the search path, on system configuration directories or on shell start-up files can lead to code
   execution in another security context when someone else reads them.
3. **Where the runtime is installed:** outside every allowed write path (see §1).
4. **Unix sockets in general.** They are blocked by default; on macOS an allowlist of paths applies, on Linux
   the path list is ignored (seccomp cannot filter by path) and the switch is all-or-nothing. Each allowed
   socket is a service the sandbox can reach.
5. **Settings sourced from the project.** The README says an embedder should read the macOS Apple Events
   option only from trusted user-level configuration, never from project-local files in a checked-out
   repository, which would let an attacker-authored project raise its own permissions. Own guidance: apply that
   to every permission-widening option.

## 3.2 Mandatory deny paths
1. **Some paths are always write-protected even inside an allowed path:** shell start-up files, git config files,
   `.ripgreprc`, `.mcp.json`, the IDE directories `.vscode` and `.idea`, the agent's `.claude/commands` and
   `.claude/agents`, and `.git/hooks` and `.git/config`.
2. **The protection is bounded.** On Linux it relies on a scan to a configurable depth below the working
   directory (default and range are in the README), so deeper copies are unprotected by default.
3. **Add your own sensitive paths to the deny list** (own guidance); do not rely on the built-in list for them.

## 3.3 Weaker modes
1. **`enableWeakerNestedSandbox` lets the runtime work inside Docker without privileged namespaces and,
   in the README's words, considerably weakens security;** use it only where other isolation is enforced.
2. **Combinations matter.** The README notes that `allowAllUnixSockets` together with the weaker nested mode
   leaves the user-namespace limit off, as `allowNestedUserNamespaces` does, and that the write denies
   should then be treated as not holding.
3. **Other relaxations the README labels as security trade-offs:** `enableWeakerNetworkIsolation` on macOS (a
   potential exfiltration vector through a system service) and `allowAppleEvents` (the sandbox then no longer
   isolates code execution, since launched apps run outside it).
4. **Platforms differ.** Windows support is alpha; glob support differs between macOS and Linux; a config
   tested on one platform does not prove another.
