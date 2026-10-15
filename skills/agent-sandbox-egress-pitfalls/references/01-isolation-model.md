# agent-sandbox-egress-pitfalls §1 — The isolation model

## 1.1 Two walls, not one
1. **Both filesystem and network isolation are required.** The sandbox runtime's README says that without file
   isolation a compromised process could exfiltrate SSH keys or other sensitive files, and that without network
   isolation a process could escape the sandbox and gain unrestricted network access.
2. **Decide both at once.** A review that finds only one of the two has an incomplete sandbox, not a partial
   one (own guidance, from the README's statement above).
3. **Defaults are minimal access.** The runtime starts with no network, no writes outside a few default paths
   and unrestricted reads; the user pokes the holes needed.

## 1.2 Rule shapes
1. **Reads: deny, then allow back.** Reading is open by default; the config lists regions to deny and paths to
   re-allow inside them. `allowRead` beats `denyRead`, but a more specific deny inside the allowed region
   (such as a secrets file) stays denied.
2. **Writes: allow only.** Writing is denied everywhere until a path is allowed; an empty list means no
   writes. Here the precedence is the other way: `denyWrite` beats `allowWrite`.
3. **Network: allow only, by domain.** An empty list means no network. A denied domain is checked first and
   wins over an allowed one.
4. **The opposite precedence for reads and writes is deliberate** and a common mistake when copying a rule from
   one list to the other.
5. **Keep the allow lists short and named** (own guidance): write down why each path and domain is there, since
   the reason is what a later reviewer needs to remove it.

## 1.3 Configuration traps
1. **A broken settings file is an error, not a fallback.** The runtime refuses to start when the file exists
   but is empty, unreadable or invalid, because falling back to built-in defaults would drop the file's deny
   rules; test that your launcher does the same.
2. **A skipped glob hides nothing.** On Linux a read-deny pattern whose first path component is a wildcard is
   skipped, and the files it matches stay readable; the runtime exposes a warning list for the embedder. A
   deny for a path that does not exist when the command is wrapped hides nothing in that command.
3. **Paths are fixed when the command is wrapped.** On Linux the read-deny globs expand to what exists then, so
   a file created later is not covered.
4. **Install the runtime outside every writable path.** A copy under a writable `node_modules` can be rewritten
   by the sandboxed command, and the next run executes the result unsandboxed.
5. **Violations:** macOS has a violation log stream; on Linux bubblewrap reports none and the README suggests
   tracing denied calls with `strace`. Use that while building the lists, and widen by the exact path a
   denial names (own guidance).
