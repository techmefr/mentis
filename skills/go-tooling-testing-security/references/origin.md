# go-tooling-testing-security: origin and source stamps

> Provenance of `skills/go-tooling-testing-security`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No scanner, test or fuzz run was
executed while writing it. Overlaps with `skills/go-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Go 1.22, 1.24, 1.25, 1.26 and 1.27 release notes | CC-BY-4.0 text, read 2026-10-08 | Per-iteration loop variable, `tool` directive, `os.Root`, `crypto/rand.Text`, vet analysers, synctest graduation, `go fix`, crypto `random` change |
| `testing/synctest`, `crypto/rand`, `crypto/subtle`, `html/template`, `os`, `testing` package documentation | BSD-3, read 2026-10-08 | Bubble and fake-time semantics, `Read` and `Text`, constant-time compare, contextual escaping, `Root` |
| The race detector article, the fuzzing guide, the vulnerability management guide | CC-BY-4.0 text, read 2026-10-08 | Overhead, runtime-only detection, seed corpus and types, govulncheck behaviour |
| The `go` command documentation | BSD-3, read 2026-10-08 | `-race` platforms, tool directives |
| The goleak README | MIT, read 2026-10-08 | `VerifyNone`, `VerifyTestMain`, parallel caveat, finding the leaking test |
| The gofumpt README | BSD-3, read 2026-10-08 | Stricter-than-gofmt, subset compatibility, skipped paths, required Go version |
| The gosec README and rule list | Apache-2.0, read 2026-10-08 | Analysis kinds, rule IDs cited |
| The Uber Go Style Guide (printf constants, test tables) | Apache-2.0, read 2026-10-08 | Const format strings, `tests`/`tt`/`give`/`want`, branch-free table loops, parallel copy |

## Removed in the verification pass (no page supporting them)
Golden files regenerated only behind a flag (no page read), a curated linter set (already in
`go-conventions` through the meta-linter) and "pin tool versions" through `tools.go` advice (replaced by the
documented `tool` directive). The share-alike security guide was not read or copied.

## Not verified
1. **Own guidance, flagged as such in the text:** adopting a stricter formatter, blocking on a vulnerability
   finding, running `go fix` on its own commit, replacing sleeps with synctest, which functions to fuzz, the
   SQL placeholder rule, hashing both sides when length is secret, suppressions needing a stated reason.
2. **`govulncheck` exit codes and installation by tool directive** are not stated in the pages read.
3. **`os.Root` limits** (hard links, mount points, platform differences) were not covered in the
   documentation read; the text says so.
4. **Fuzz target timeout and CPU architectures** were not re-checked against the current guide beyond
   the architecture note quoted.
5. **gofumpt's required Go version** is that of the README read and moves with its releases.

## Related blocks
`go-conventions`, `security-hardening`, `testing-anti-patterns`, `ci-workflow-hardening`, `devops-conventions`,
`go-container-runtime`, `go-http-resilience-pitfalls`.

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

Pages and repositories re-opened for each cited version, figure, rule identifier and flag.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| Go release notes 1.22 (earlier read), 1.24, 1.25, 1.26, 1.27 | CC-BY-4.0 text and BSD code (go.dev/copyright), read 2026-10-20 | tool directive and its -tool flag, printf non-constant check gated by language version, waitgroup and hostport analysers, synctest graduation, go fix modernizers, crypto random parameter ignored and SetGlobalRandom, stdversion by default under go test, printf %w extension, synctest.Sleep |
| Go race detector article; Go fuzzing guide; vulnerability management page; database injection page | CC-BY-4.0, read 2026-10-20 | overhead 5 to 10 times memory and 2 to 20 times time, only executed paths, supported platforms and cgo requirement; fuzz target rules, argument types, AMD64 and ARM64, fuzztime default; govulncheck guidance; placeholder rule |
| testing/synctest, crypto/rand, crypto/subtle, os package pages; govulncheck command page | BSD-3, read 2026-10-20 | bubble semantics, durable blocking list, isolation; Read never errors, Text; constant-time compare length behaviour; Root limits; exit codes and limitations |
| uber-go/goleak README and LICENSE | MIT (LICENSE file read), read 2026-10-20 | both verify forms, parallel caveat, two-latest-Go-versions support, shell loop for finding the test |
| mvdan/gofumpt README and LICENSE | BSD-3 (LICENSE file read), read 2026-10-20 | stricter subset of gofmt, skipped directories, generated files, requires Go 1.26 or later |
| securego/gosec README, RULES.md and LICENSE | Apache-2.0 (LICENSE file read), read 2026-10-20 | AST, SSA and taint analysis, G-rule identifiers cited, suppression syntax with a justification, CI invocation |
| uber-go/guide style guide and LICENSE | Apache-2.0 (LICENSE file read), read 2026-10-20 | const format strings, tests, tt, give and want, table complexity signs, parallel loop variable |

### Verified in this pass
1. 1.1, 1.2 items 2 and 3, 1.3 items 1 and 2, 1.4, 1.5 item 1, 1.6 (the modernizer facts; the commit advice is own).
2. 2.1 items 1 to 3, 2.2 items 1 and 3, 2.3 all five (plus the sleep replacement as own advice on top of the documented behaviour), 2.4 all four.
3. 3.2 all four, 3.3, 3.4 both items, 3.5.

### Corrected in this pass
1. 1.3 item 3 extended: the race detector needs cgo and a C compiler (not macOS), which conflicts with a cgo-off test job; defer and recover memory growth added.
2. 1.5 item 2: the earlier text said no page states the exit code; the command page documents it, and the structured output formats always exit successfully. Reflect and unsafe limitations added.
3. 2.2 item 2: the guide names the flag shouldError, not shouldErr.
4. 2.3: isolation and deadlock panics added.
5. 3.1: the Root limits are documented on the type page and were added; the earlier "not covered" caveat was dropped.

### Still unverified (no page found that says it, kept as own guidance)
1. 1.2 item 1 (run go vet in CI) and 2.1 item 4 (leak check complements the race detector) are own statements.
2. Adopting a stricter formatter, running go fix on its own commit, replacing sleeps with synctest, which functions to fuzz, hashing both sides when length is secret, and suppressions needing a stated reason remain own guidance.
3. Nothing was run.

### Tally
Points 36. Sourced 30, corrected 4, still unverified 2 (plus the own-guidance halves listed above).

Independent verification 2026-10-21: 21 checked, 21 matched, 0 corrected, 0 unverified (gofumpt, govulncheck exit codes, vet analysers by release, synctest semantics and Sleep in 1.27, crypto/rand, race detector figures and requirements, tool directive, goleak, fuzzing, gosec rule identifiers, go fix; os.Root limits not re-read).
