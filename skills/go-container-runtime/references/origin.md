# go-container-runtime: origin and source stamps

> Provenance of `skills/go-container-runtime`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No image was built and no process
was started while writing it. Overlaps with `skills/go-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Go build template repository (Dockerfile, build script, Makefile) | Apache-2.0, read 2026-10-08 | CGO off, distroless static base, numeric user and `HOME`, licence directory, version required and stamped by `-X`, `-s -w` unless debugging |
| The automatic-GOMAXPROCS library README | MIT, read 2026-10-08 | Setting GOMAXPROCS from the Linux container CPU quota, one measured latency and throttling data point |
| Go 1.25 release notes | CC-BY-4.0 text, read 2026-10-08 | Container-aware GOMAXPROCS, periodic update, disabling settings, requests not considered |
| Go 1.26 release notes | CC-BY-4.0 text, read 2026-10-08 | Green Tea collector on by default |
| The Go garbage collector guide | CC-BY-4.0 text, read 2026-10-08 | Soft memory limit, what it covers, 5 to 10% headroom, thrashing, GOGC trade-off, profile hints |
| `runtime`, `runtime/debug`, `os/signal`, `net/http` package documentation, and the `net/http` server source for the `Shutdown` doc comment | BSD-3, read 2026-10-08 | GOMAXPROCS and GOMEMLIMIT syntax, `SetMemoryLimit` since 1.19, `NotifyContext`, `Shutdown`, hijacked connections |
| `go` command and `cmd/link` documentation | BSD-3, read 2026-10-08 | `-trimpath`, `-ldflags`, `-X`, `-s`, `-w`, `-buildvcs`, `go version -m` |

## Removed in the verification pass (no page supporting them)
A numeric orchestrator grace period or its name, a claim that the base image has no shell or package
manager, and the earlier review's phrase "or use a maintained shim" as a blanket rule (kept only for Go 1.24
and earlier, where the runtime documentation supports it).

## Not verified
1. **Own guidance, flagged as such in the text:** cgo needing a matching base image, only binary and
   licences in the final image, shutdown deadline shorter than the grace period, one data point being
   specific to the service measured.
2. **The consequence of `-buildvcs=auto`** in a build context without repository metadata is derived from
   the documented condition, not tested.
3. **The template's current Go version and tool versions** change; only its structure was read.
4. **Whether `GOMAXPROCS` shim libraries behave identically on cgroup v1 and v2** was not read.

## Related blocks
`node-container-runtime`, `dotnet-container-runtime` (same layer for other stacks), `go-conventions`,
`devops-conventions`, `go-http-resilience-pitfalls`, `go-performance`.

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

Pages re-opened for the exact flag, function, version and figure. The Go build template repository named in the earlier stamp was not re-opened in this pass, so what rests only on it is listed as unverified below.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| Go release notes 1.25 and 1.26; Go garbage collector guide | CC-BY-4.0 text and BSD code (go.dev/copyright), read 2026-10-20 | container-aware GOMAXPROCS, what is and is not considered, disabling settings; Green Tea 10 to 40%, default in 1.26; memory limit suggested uses, 5 to 10% headroom, thrashing, 50% CPU cap |
| runtime and runtime/debug package pages | BSD-3, read 2026-10-20 | GOMAXPROCS default, containermaxprocs and updatemaxprocs defaults for language version 1.24 and below, SetDefaultGOMAXPROCS, threads in system calls, GOMEMLIMIT syntax and what it excludes, SetMemoryLimit since 1.19, gctrace |
| go command and cmd/link pages | BSD-3, read 2026-10-20 | -trimpath, -buildvcs condition, go version -m; -s implies -w, -X string variable and its limits |
| os/signal and net/http package pages | BSD-3, read 2026-10-20 | default exit on SIGHUP, SIGINT, SIGTERM, NotifyContext and stop, buffer of one, Shutdown sequence, ErrServerClosed, hijacked connections, RegisterOnShutdown, Close |
| uber-go/automaxprocs: README and LICENSE | MIT (licence file read), read 2026-10-20 | data table (RPS, P50, P99.9 for GOMAXPROCS 1, 2, 3, 4, 8, 24) and the throttling counters |
| distroless: README and the base/static image README | Apache-2.0 (LICENSE file read), read 2026-10-20 | contents of the static image, cgo programs use the base image, nonroot tags exist |
| Kubernetes pod lifecycle page; Docker stop reference | facts only, official documentation, read 2026-10-20 | default 30 second termination term, TERM then KILL; docker stop sends SIGTERM then SIGKILL after a grace period |

### Verified in this pass
1. 1.1 item 1 (distroless static contents; cgo on the base image), 1.3 item 1 (static image has a root entry only), 1.4 items 1 and 2 (-trimpath; -s implies -w, negatable), 1.5 items 1 and 3 (-X rules; -buildvcs=auto condition; go version -m).
2. 2.1 item 2, 2.2 items 1 to 3, 2.3, 2.4, 2.5 (figures match the pages).
3. 3.1 both items, 3.2 all three, 3.3, 3.4 (now sourced).

### Corrected in this pass
1. 2.1 item 1: the automatic behaviour depends on the language version in the go directive, not only on the toolchain; added.
2. 2.1 item 3: the old default applies to language version 1.24 and below, not to a toolchain number.
3. 2.1 item 4: the README does not show throttling counters for the matched setting; the claim that matching removed the throttling was dropped and the measured figures were stated instead.
4. Added: 2.2 what the limit does not count (C allocations, mappings, kernel memory); 1.5 -X also fails when the initialiser refers to another variable.

### Still unverified (no page found that says it, kept as own guidance)
1. 1.1 item 2 (only binary and licences in the final image), 1.2 (licence collection into a licence directory), 1.3 item 2 (HOME), 1.5 item 2 (fail when the version is unset), 1.4 (the DEBUG switch): all rest on the build template read on 2026-10-08, not re-opened.
2. 3.5 (shape of main) is our own structure and a cross-reference.
3. The numeric user value 65535 comes from the template; what the nonroot tags set was not read.
4. Nothing was built or run.

### Tally
Points 28. Sourced 20, corrected 3, still unverified 5.

Independent verification 2026-10-21: 21 checked, 21 matched, 0 corrected, 0 unverified (GOMAXPROCS 1.25 and the language-version defaults, automaxprocs figures, distroless static and base, GOMEMLIMIT, SetMemoryLimit, build flags, signals, Server.Shutdown, Kubernetes 30 second term).
