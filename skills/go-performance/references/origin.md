# go-performance: origin and source stamps

> Provenance of `skills/go-performance`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No benchmark or profile was run
while writing it. This block is meant to be folded into `go-conventions` when the extended version of that
block (the branch that takes it to nine sections) lands; until then it stands alone.

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
