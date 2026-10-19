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
