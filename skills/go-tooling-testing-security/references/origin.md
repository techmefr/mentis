# go-tooling-testing-security: origin and source stamps

> Provenance of `skills/go-tooling-testing-security`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No scanner, test or fuzz run was
executed while writing it. This block is meant to be folded into `go-conventions` when the extended version
of that block (the branch that takes it to nine sections, including its test and security sections) lands;
until then it stands alone so nothing cites a section that is not on the main branch.

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
