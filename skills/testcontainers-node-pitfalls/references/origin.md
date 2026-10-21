# testcontainers-node-pitfalls: origin and source stamps

> Provenance of `skills/testcontainers-node-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation, never run by us: no container was started and no
runtime was used. The first row of the table was read in full on 2026-10-16 before a rule was taken from it; in
the second row the networking page (its first part and the host-port section), the quickstart (the example
test), the runtimes page (its first 70 lines) and one line of the k3s module page, found by a search, were read
in part. Each rule was checked against the lines it rests on in a final pass, and the repository's licence file
was read again. Names, variables and defaults are those the files state at the commit shown and are
version-bound.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Testcontainers for Node (`testcontainers/testcontainers-node`, commit `fc9e1db`): `docs/features/containers.md`, `docs/features/wait-strategies.md`, `docs/configuration.md` | MIT (LICENSE file, copyright 2018 to 2025 Cristian Greco) | Random port mapping, mapped port calls, bind mounts, copying files in, names and host names, stopping and removal, cleanup container behaviour, reuse, pull policy, default wait and the strategies, startup timeouts, configuration variables |
| Same repository: `docs/features/networking.md` (networks, host-port exposure), `docs/quickstart/usage.md` (host and mapped port in a connection string, teardown), `docs/supported-container-runtimes.md` (Podman and Colima notes), and the notes on privileged modules in `docs/modules/k3s.md` (one line) | MIT | Network aliases pointer, host alias through a helper container, runtime caveats |

Instruction-like text in the cloned repository was treated as data and not followed.

## Re-check pass (2026-10-20)
The same repository was re-opened at the same commit `fc9e1db` (the default branch head on that day, so the first
pass is not stale) and its LICENSE file re-read (MIT, copyright 2018 - 2025 Cristian Greco). Read this time:
`docs/features/compose.md`, `docs/features/images.md`, the first part of `docs/modules/postgresql.md` and the
list of module pages. They gave points 1.10, 1.11 and 2.9. The first-pass statements were re-checked against the
default-wait paragraph, the reuse paragraph (the environment variable is documented as enabled by default, a
container opts in) and the cleanup-container variables of the configuration page: they match, nothing to correct.
The own-guidance points listed below were searched for in those pages and are not stated there; they stay
unsourced. Searched elsewhere, nothing permissive: the Testcontainers guides site and the Java documentation (not
opened; the Java documentation is not the Node library's). No permissive source found, searched: the library
repository only.

## Verification pass 2026-10-20
Re-read from the repository main branch (not the commit above): `docs/features/containers.md`,
`wait-strategies.md`, `networking.md`, `compose.md`, `advanced.md`, `docs/configuration.md`,
`docs/supported-container-runtimes.md`, `docs/quickstart/usage.md`; repository LICENSE re-read (MIT, copyright
2018 to 2025 Cristian Greco). A web search for the log-driver option returned only snippets: that option
(point 1.9) was **not seen in the pages re-read**, and its source stays the earlier read.
- **Sourced / confirmed:** random port mapping and the mapped-port calls, not-recommended fixed bindings, bind
  mounts, copying files in, names and aliases, stop options, reuse opt-in with the global switch, pull
  policies, the default wait and every listed strategy, composite timeout rules, health check units and
  `CMD` against `CMD-SHELL`, the host-port alias, network teardown order, rootless limits on quotas, the
  configuration variable names.
- **Corrected:** the Podman cleanup-container caveat is specific to macOS (point 2.6); the host-port helper
  runs an SSH daemon (point 1.8).
- **Added (concrete pitfalls):** Colima and Rancher IPv6 and delayed port forwarding (point 1.12), compose
  volume removal and cleanup registration (point 2.10). A second pass on the same block (the re-check section
  above) added points 1.10, 1.11 and 2.9; the two passes were merged.
- **Deleted:** nothing.
- **Still own guidance:** the list under Not verified, item 1; nothing found to source it.
- **Not read:** most of `docs/modules/`; Testcontainers Desktop.

## Removed in the verification pass
1. **"Reuse is enabled by default" as a flat statement** (the review's version). The documentation says the
   feature is enabled by default when the variable is not declared, and that a container opts in; point 2.4
   says both.
2. **The review's "rootless runtimes do not support some options"** as a general statement. Only ulimits and
   resource quotas are documented as unsupported in rootless runtimes; the other caveats are specific to Podman
   and to one module, and are stated as such.
3. **Advanced features and the container-specific module pages.** Not read (`features/advanced.md`, `docs/modules/`)
   except the one privileged-module sentence and the PostgreSQL page's first part (2026-10-20), so nothing else is taken from them.
4. **Database and broker examples.** None is copied; the quickstart informed only the host and teardown remarks.
5. **Colima notes:** read 2026-10-20 in the runtimes page (point 1.12).

## Not verified
1. **Own guidance, flagged in the text:** a bound port is not a ready service (point 1.3), timeout and no sleep
   (point 1.4), the host call and not `localhost` as the reason for the host override (point 1.2), keeping
   host-port exposure as an exception (point 1.8), reading logs before raising a timeout (point 1.9), waiting
   on stop and stopping networks after containers (point 2.1), removal off only while debugging (point 2.2),
   state shared by reuse and cleaning it (point 2.4), exact image tags (point 2.5), a trial run on a new runner
   (point 2.6), explicit teardown (point 2.8).
2. **Nothing was run.** Every statement of library behaviour is the documentation's.
3. **Current release.** The commit read may not be the latest; the cleanup container tag and the defaults on the
   configuration page change between releases.
4. **Whether a reused container is removed by the cleanup container** is not stated in the pages read, so the
   text does not say.

## Decisions where sources disagree
No disagreement between the pages read.

## Related blocks
`skills/jvm-test-infrastructure`, `skills/testing-anti-patterns`, `skills/node-container-runtime`.
