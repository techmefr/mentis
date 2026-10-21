# Origin: go-conventions

Ideas taken from: golangci-lint (meta-linter, default categories
errcheck/govet/staticcheck/gosimple/ineffassign/unused); staticcheck.dev (the SA/S/ST rules cited);
uber-go/guide (Uber Go Style Guide, copying slices/maps at boundaries, defer for resources, avoiding
catch-all `interface{}`). Mechanisms rewritten, no copied text. Market research, no internal production
feedback at this stage.

Re-checked directly against the Uber Go Style Guide's text on 2026-08-10, filtered for what a linter
doesn't already catch mechanically (the guide's own formatting/naming items stay with `gofmt`/`govet`,
same reasoning as the PSR-12 pass on `php-patterns`): no panic in library code (§2.5), the comma-ok type
assertion (§2.6), and `os.Exit`/`log.Fatal` confined to `main()` via a `run()` wrapper (§4.6) were real
gaps, now closed. The guide's pointer-vs-value-receiver and channel-sizing guidance stay out: both are
judgment calls that depend on the concrete type/use, not a rule with a mechanical trigger the way the
three added ones are.

**Dogfooded, 2026-09-10.** First real confrontation: a small worker-pool job queue (`Queue`/`Runner`
interface, goroutines draining a jobs channel, `context` for submit-cancellation and per-job cancellation,
a JSON-tagged `Job`/`Result` struct), built outside this repo, with `go build`/`go vet`/`golangci-lint
run` (default linters, clean) and `go test -race` (all green) as the checkpoint. One real gap surfaced by
writing the code, not by re-reading the guide: the "check closed under a mutex, then send on the channel"
shape used for `Submit`+`Close` is a genuine TOCTOU race (a sender can pass the check and then lose to a
concurrent `Close()`, panicking on a closed channel) that neither `go vet`, `staticcheck`, nor even
`-race` flags unless a test happens to interleave the two calls — added as §1.6. Every other rule in this
file (context-first-param, `%w` wrapping, comma-ok assertions, `defer resp.Body.Close()`, `run() error` +
single `os.Exit` in `main`) held up against the practice with no adjustment needed.


**Extended, 2026-10-02** (§1.7-11, §2.7-10, §3.4-6, §5-§9). Rewritten, not copied, from two MIT-licensed
public skill repositories read in full on that date: `samber/cc-skills-golang` (commit 8e899e2; the safety,
error-handling, context, concurrency, database, testing, project-layout, security and modernize skills) and
`spf13/go-skills` (layout and idiom arbitration only). Where the two disagree (layered package names) the
smaller structure was chosen and §8.3 says so. Left out on purpose: per-library skills (sqlx, pgx, lo, mo, do,
cobra, viper), linter configuration, profiler troubleshooting, and a table of version-specific replacements,
which goes stale: §8.5 states the mechanism (read the module's `go` directive) instead, per
`skills/source-freshness`. No numeric threshold is stated. Status stays 🟡: not yet confronted with a real
project.

**Dogfooded again, 2026-10-19.** Scenario not covered by the 2026-09-10 pass: an order-lookup HTTP service
(Go 1.24 module, stdlib only), built outside this repo with a consumer-side `Store` interface and an
in-memory implementation (RWMutex, lazily created map, defensive copies of the `Items` slice), a sentinel
`ErrNotFound` and a typed `*ValidationError` inspected with `errors.Is`/`errors.As`, `%w` wrapping, `errors.Join`
over a bounded stdlib worker pool cancelled through `context.WithCancel` (no errgroup), `net/http` handlers
mapping errors to status codes with the detail kept in `slog`, a server with the four timeouts, signal-driven
graceful shutdown via `run() error` and `context.WithoutCancel`, and table tests plus an `httptest` server
test. `go build`, `go vet`, `gofmt -l` (empty) and `go test -race` all passed. Clean, nothing found: no rule
needed adjusting. Not exercised: golangci-lint and the vulnerability checker (third-party tools, not available),
database/sql (§6), goroutine-leak checking (§1.11).

## Source pass 2026-10-20 (every point below was re-opened against the page named, own words, no text copied)

Facts only, from the official Go documentation and the standard-library package pages; the Go Wiki review-comments page is a creditable page of the same site. Section references below are page headings or documented function names.

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| Go language specification (go.dev/ref/spec) | CC-BY-4.0 text and BSD code (go.dev/copyright), read 2026-10-20 | send on or close of a closed channel panics; defer runs when the function returns; init order across files is only encouraged to follow file-name order |
| Go release notes 1.22, 1.23, 1.24, 1.25 | CC-BY-4.0 text and BSD code (go.dev/copyright), read 2026-10-20 | 1.22: range over int, per-iteration loop variable, math/rand/v2; 1.23: unreferenced timers collected; 1.24: os.Root, synctest experiment; 1.25: WaitGroup.Go, reflect.TypeAssert |
| Go blog: fixing for loops in 1.22 (loopvar article) | CC-BY-4.0 text and BSD code (go.dev/copyright), read 2026-10-20 | the per-iteration scope applies only to modules declaring go 1.22 or later |
| Go blog: working with errors in 1.13; errors and fmt package pages | CC-BY-4.0 text and BSD code (go.dev/copyright), read 2026-10-20 (pages BSD) | errors.Is and As, %w, multiple %w, Join, wrapping exposes the error to callers on purpose |
| context, sync, sync/atomic, net/http, database/sql, testing, testing/synctest, os, path/filepath, os/exec, html/template, crypto/rand, crypto/subtle, time, reflect package pages | BSD-3 (pkg.go.dev module licence), read 2026-10-20 | context rules and WithoutCancel (since 1.21), Mutex not copied, WaitGroup.Add ordering, typed atomics since 1.19, pool defaults, ErrNoRows, Rows auto-close, Root, IsLocal |
| golang.org/x/sync/errgroup page | BSD-3, read 2026-10-20 | SetLimit (negative means no limit) and TryGo |
| Go FAQ, Effective Go, Go Wiki Code Review Comments, Go Wiki table-driven tests and test comments, Go blog on package names, module layout and module reference | CC-BY-4.0 text and BSD code (go.dev/copyright), read 2026-10-20 | map concurrency note, no panic for normal errors, error strings, interfaces owned by the consumer, utils and common package names, internal, module path rules |
| Go blog: traversal-resistant file APIs; govulncheck and vulnerability pages | CC-BY-4.0 text and BSD code (go.dev/copyright), read 2026-10-20 | check-then-open is a race against a symlink swap; Root closes it; the vulnerability checker |

### Verified in this pass
1. 1.1 goroutine lifetimes: review-comments page, Goroutine Lifetimes. 1.2 sync package pages for Mutex, RWMutex, WaitGroup, Cond, Once, Pool, Map. 1.3 release notes 1.22 and the loopvar article. 1.4 context package: failing to call the cancel function leaks the child until the parent is cancelled. 1.7 errgroup SetLimit; WaitGroup.Add must precede the goroutine (documentation of Add). 1.11 race detector article (-race).
2. 2.1, 2.2, 2.3, 2.8 review-comments page (Handle Errors) and the 1.13 errors article (wrapping, Is and As, API exposure). 2.5 review-comments page (Dont Panic) and Effective Go. 2.6 the specification on type assertions. 2.9 errors.Join, review-comments page (Error Strings).
3. 3.1 and 3.5 context package: first parameter named ctx, not in a struct, never nil, use TODO. 3.3 NewRequestWithContext (since 1.13). 3.4 WithoutCancel (since 1.21). 3.6 unexported key type and request-scoped values only.
4. 4.1 net/http client: the caller must close the body. 4.2 defer runs when the function returns (specification).
5. 5.1 Go FAQ nil error. 5.2 to 5.5 specification (nil map writes, full slice expression, integer conversion, division). 5.6 Effective Go zero value, sync.Once. 5.8 reflect.TypeAssert exists and was added in Go 1.25 (release notes and reflect page): the earlier "to confirm" is closed.
6. 6.1 database/sql injection page. 6.2 the Context methods in the database/sql page. 6.3 Rows closed automatically when Next returns false, Err readable after close, Close idempotent. 6.4 ErrNoRows is returned by Scan of QueryRow, Null[T] exists. 6.6 connection pool page: open connections unlimited by default, two idle kept by default.
7. 7.1 table-driven tests page and t.Run. 7.2 t.Parallel. 7.6 testdata directory ignored by the go tool; test-comments page on printing diffs. 7.7 testing/synctest fake clock (experiment in 1.24, bubble package page).
8. 8.1 module layout page (internal) and package-names article (util, common, misc say nothing). 8.2 review-comments page, Interfaces. 8.5 release notes for the version-dependent forms. 8.6 log/slog package page (structured logging, since 1.21).
9. 9.1 os/exec does not invoke a shell; SQL placeholders. 9.2 html/template contextual escaping. 9.4 review-comments page, Crypto Rand; crypto/subtle. 9.5 net/http Server and Client timeouts. 9.6 vulnerability pages and govulncheck.

### Corrected in this pass
1. 1.5 reworded: the Go FAQ says unsafe concurrent map access can crash the program and that only some implementations report it; it is not a guaranteed, statically detectable panic.
2. 1.9 reworded: since Go 1.23 an unreferenced time.After timer is collected before it fires (time page and 1.23 notes); the old "stays alive until it fires" is the pre-1.23 behaviour.
3. 1.10 reworded: typed atomics exist since 1.19, but the sync/atomic page itself says the functions need great care and prefers channels or sync for general synchronisation.
4. 5.9 reworded: the specification only encourages build systems to present files in file-name order, so cross-file init order is not guaranteed by the language.
5. 8.4 corrected: the module reference requires lower-case ASCII only for the leading host element; hyphenated segments are not required by it.
6. 9.3 extended: the traversal article shows the clean-then-check sequence is a TOCTOU race when an attacker can alter the tree.

### Still unverified (no page found that says it, kept as own guidance)
1. 1.6 the lock-across-the-send recipe is our own analysis, dogfooded 2026-09-10; the language only says a send on a closed channel panics (specification).
2. 1.8 only the sender closes, directions, unbuffered default, buffer needing a measurement: the tour page that states the convention did not render when fetched, so none of this is sourced.
3. 2.4 silent recover; 2.7 handle an error once; 2.10 no technical error to the end user: no page read.
4. 3.2 propagating the received context rather than a fresh background one: restated from the package rule, not from a page that says it.
5. 4.3 err shadowing, 4.4 catch-all any, 4.5 copying slices and maps at boundaries (the review-comments Copying section is about struct values), 4.6 os.Exit from main only: previously read in a style guide, not re-opened in this pass.
6. 5.7 returning a copy of an internal slice or map.
7. 6.5 locking reads and serialisation retry, 6.7 batch chunks, 6.8 migrations by tool and the agent not designing schema, 6.9 business rules out of triggers: no page read.
8. 7.3 integration tests behind a build tag, 7.4 observable contract, 7.5 hand-written fakes, 7.8 file naming: no page read.
9. 8.3 not mirroring layered package names and 8.6 bounded metric label cardinality and trace spans: no page read.

### Tally
Points 71. Sourced 45, corrected 6, still unverified 20.
