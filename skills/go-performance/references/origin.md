# go-performance: origin and source stamps

> Provenance of `skills/go-performance`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No benchmark or profile was run
while writing it. Overlaps with `skills/go-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Go diagnostics guide | CC-BY-4.0 text, read 2026-10-08 | Profile kinds, block and mutex profiles off by default, tool interference, runtime statistics |
| The Go garbage collector guide | CC-BY-4.0 text, read 2026-10-08 | GOGC trade, profile hints for allocation cost, execution traces, escape analysis command, huge pages |
| Go 1.24, 1.25 and 1.26 release notes | CC-BY-4.0 text, read 2026-10-08 | `testing.B.Loop`, flight recorder, Green Tea collector, goroutine-leak profile |
| `testing`, `strings` and `sync` package documentation | BSD-3, read 2026-10-08 | `B.Loop` semantics, `ReportAllocs`, `Builder`, `Pool` |
| The Go blog article on slices | CC-BY-4.0 text, read 2026-10-08 | `make` with capacity, copy cost, retained backing array |
| The Go language specification | CC-BY-4.0 text, read 2026-10-08 | Map capacity hint does not bound size |

## Removed in the verification pass (no page supporting them)
Interface boxing, reflection in hot loops and false sharing or struct field order (the earlier review's
sources for these were idea-only: a share-alike performance book and an unread-this-pass mistakes list);
manual `b.N` guidance beyond the documented loop; "use the loop-benchmark helper where the toolchain
supports it" is kept only as the Go 1.24 rule. The share-alike performance book was not read or copied.

## Not verified
1. **Own guidance, flagged as such in the text:** keeping a baseline, same-conditions comparison,
   preallocating only a known count, the guarded-result advice for pre-1.24 benchmarks, profile before adding
   a pool, `GOGC=off` suiting only bounded programs, re-measuring after upgrades.
2. **The inference that repeated string `+` copies the growing string** is drawn from the Builder's stated
   purpose, not from a page that says it.
3. **The collector guide's percentage hints (15%, 5%)** are rules of thumb as the guide words them, and may
   change between guide revisions.
4. **No benchstat or comparison-tool page was read,** so no tool is named for comparing runs.

## Related blocks
`go-container-runtime` §2, `go-http-resilience-pitfalls` §1.4, `go-conventions`, `testing-anti-patterns`.

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

The block was already written from these pages on 2026-10-08. This pass re-opened each page and checked the exact figure, function and version behind each statement; sources are credited by page.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| Go diagnostics guide (go.dev/doc/diagnostics) | CC-BY-4.0 text and BSD code (go.dev/copyright), read 2026-10-20 | profile kinds, block and mutex off by default, tools interfere, how profiles are collected (go test, net/http/pprof), NumGoroutine for leak detection, memory profile for leaks |
| Go garbage collector guide (go.dev/doc/gc-guide) | CC-BY-4.0, read 2026-10-20 | the 15% and 5% hints, non-leaf runtime functions, GOGC doubling halving, GOGC=off, memory limit suggested uses, escape analysis flag, THP figures (up to 10% throughput, up to 50% more memory for small heaps) |
| Go blog: execution traces 2024 | CC-BY-4.0, read 2026-10-20 | a trace shows blocking a CPU profile cannot sample |
| Go release notes 1.24, 1.25, 1.26 | CC-BY-4.0, read 2026-10-20 | b.Loop run once per -count, FlightRecorder, Green Tea (10 to 40%), default in 1.26 with a nogreenteagc opt-out expected to go in 1.27, goroutineleak profile experiment |
| testing, strings, sync package pages and the benchstat page | BSD-3, read 2026-10-20 | B.Loop semantics and the KeepAlive condition, B.N style, ReportAllocs, Builder, Pool contract and example, benchstat needs ten runs |
| Go blog: slices intro; language specification | CC-BY-4.0, read 2026-10-20 | growing copies, retained backing array, map capacity hint does not bound size |

### Verified in this pass
1. 1.1 items 1 and 2, 1.2 (15% and 5% hints), 1.3 (flag, editor action), 1.4 items 1, 3 and the first half of 2, 2.1 items 1 and 2, 2.2 (Builder documentation, Grow, Reset exists, do not copy), 2.3, 2.4 items 1 to 4, 3.2 both releases, 3.3, 3.4 (figures match the guide).

### Corrected in this pass
1. 1.1 item 3 re-attributed: the claim about subtle and rare costs was not in the collector guide; it now rests on the execution traces article and the 1.25 notes.
2. 3.1 GOGC=off: the guide gives the real condition (limit with co-tenants) instead of the earlier own-guidance half.
3. Added (concrete pitfalls from the pages): non-leaf collector functions hidden in the default listing; b.Loop protection needs the exact loop form; B.N style reruns setup; benchstat needs ten runs; Pool.New should return a pointer.

### Still unverified (no page found that says it, kept as own guidance)
1. 1.1 item 4 (profiling endpoints off the public listener) cross-references another block and was not checked here.
2. 2.1 item 3 (do not preallocate a guess) is own guidance.
3. 2.2 that repeated string addition copies the growing string is an inference from the Builder documentation.
4. 2.4 item 5 (profile before adding a pool) and the pre-1.24 guarded-result advice are own guidance.
5. Re-measuring after a toolchain upgrade (3.2) is own guidance. No benchmark or profile was run.

### Tally
Points 25. Sourced 20, corrected 2, still unverified 3 (own guidance flagged in the text).
