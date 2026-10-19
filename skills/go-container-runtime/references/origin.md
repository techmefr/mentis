# go-container-runtime: origin and source stamps

> Provenance of `skills/go-container-runtime`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No image was built and no process
was started while writing it. This block is meant to be folded into `go-conventions` when the extended
version of that block (the branch that takes it to nine sections) lands; until then it stands alone so
nothing cites a section that is not on the main branch.

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
