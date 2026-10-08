# go-tooling-testing-security §2 — Test extras

## 2.1 Check for leaked goroutines
1. **Verify at the end of the package with `goleak.VerifyTestMain(m)` inside `TestMain`,** or per test with
   `defer goleak.VerifyNone(t)`. The library's README gives both forms. Naming the dependency is the
   recommendation: the user adds it. Its README says it supports only the two most recent minor versions of Go.
2. **Use the package-level form when tests call `t.Parallel`.** The README says the library cannot tell a
   leaking goroutine from a test that has not finished running, so the per-test check gets confused.
3. **When the package check fails, find the guilty test by running them one by one;** the README shows a
   short shell loop over `go test -list` output against a compiled test binary. The package-level check runs
   once after everything, so it does not say which test leaked.
4. **A leak check complements the race detector** (§1.3): neither flags what the other finds. `go-conventions`
   §1.1 is the rule it enforces.

## 2.2 Table tests
1. **Use a table with named subtests (`t.Run`) when only inputs and outputs change.** The Uber guide's
   convention: the slice is `tests`, a case is `tt`, and fields are prefixed `give` and `want`. The case
   name is what the failing run prints, so make it distinct.
2. **Keep the loop body free of branches.** The guide says not to use a table when the subtests need
   conditional assertions or complex logic; signs of trouble are several flags such as `shouldErr` or
   `expectCall`, many `if` statements around mock expectations, and functions stored in the table. Split into
   several tables or plain test functions. A single success-versus-failure flag is acceptable when the body
   is short.
3. **Loop variable copy depends on the `go` directive.** The Uber guide tells you to scope `tt` to the
   iteration when subtests run in parallel, because otherwise most or all subtests see a wrong or changing
   value. From Go 1.22 each iteration has its own variable, and the release notes tie that to the `go`
   version in `go.mod`: with `go 1.22` or later the copy is noise, below that it is required. The guide's own
   examples predate the change, so read them with that in mind.

## 2.3 Time-dependent tests: `testing/synctest`
**Go 1.25 and later.** The package became generally available in 1.25 (in 1.24 it was experimental, behind
`GOEXPERIMENT=synctest`, and its API could change).
1. **Run the code under test in a bubble with `synctest.Test`,** which waits for every goroutine in the
   bubble to exit before returning. Inside the bubble the `time` package uses a fake clock that starts at
   midnight UTC on 2000-01-01, and time advances only when every goroutine is durably blocked, so a test of
   a timeout or a ticker needs no real waiting. Replace sleeps in such tests with it (own guidance for the
   replacement; the behaviour is the documentation's).
2. **Use `synctest.Wait` to let the bubble settle** before asserting: it blocks until every other goroutine
   in the bubble is durably blocked.
3. **Know what does not count as durably blocked:** locking a `sync.Mutex` or `RWMutex`, blocking on I/O
   and system calls can be unblocked from outside the bubble, so time does not advance past them. A test
   that does real network I/O inside a bubble will not behave like a fake-time test.
4. **Do not call `T.Run`, `T.Parallel` or `T.Deadline` inside a bubble.**
5. **Go 1.27 adds `synctest.Sleep`,** combining `time.Sleep` and `Wait`.

## 2.4 Fuzz what parses outside input
1. **Fuzz a parser or decoder with `go test -fuzz <regex>`** (one fuzz test per run). The guide says fuzzing
   reaches edge cases humans miss and is particularly valuable for finding security problems. Which
   functions to fuzz is own guidance.
2. **Seed with `f.Add` and files under `testdata/fuzz/<FuzzTestName>`.** A failing input the engine finds is
   written there and then runs under plain `go test`, so it becomes a regression test once fixed.
3. **Argument types are limited** to strings, byte slices, the integer and float types, and `bool`.
4. **Keep the target stateless:** it runs in parallel and in nondeterministic order, so state must not
   outlive a call or depend on global state. Fuzzing needs a platform with coverage instrumentation
   (AMD64 and ARM64 at the time of the guide). `-fuzztime` bounds a run; the default is indefinite, so
   a CI job must set it.
