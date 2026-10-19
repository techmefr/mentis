# go-performance §1 — Measure first

## 1.1 Profile before you change
1. **Take a profile that names the cost.** The built-in profiles are CPU, heap, goroutine, thread creation,
   block and mutex; the block and mutex profiles are **off by default** and are enabled with
   `runtime.SetBlockProfileRate` and `runtime.SetMutexProfileFraction`. Profiles come from `go test`, from
   handlers in `net/http/pprof`, and are read with `go tool pprof` (diagnostics guide).
2. **Run one diagnostic tool at a time.** The guide warns that tools can interfere (precise memory
   profiling skews CPU profiles, blocking profiling affects scheduler traces) and says to use them in
   isolation.
3. **Use an execution trace for latency questions.** The collector guide says CPU profiles are poor at
   subtle, rare or latency-related costs, and that execution traces give a deep view of a short window.
   Go 1.25 added `runtime/trace.FlightRecorder`, which keeps recent trace data in an in-memory ring buffer so
   the last seconds can be written out when something significant happens.
4. **Keep profiling endpoints off the public listener** (`go-http-resilience-pitfalls` §1.4).

## 1.2 Read the collector's signature in the profile
The collector guide gives hints for a CPU profile: a large share of time in `runtime.mallocgc` (above
about 15%) suggests heavy allocation, time in `runtime.gcAssistAlloc` above about 5% suggests the program is
outpacing the collector, and `runtime.gcBgMarkWorker` time scales with collection frequency and the size and
complexity of the object graph. Treat those as the guide's rules of thumb, not limits.

## 1.3 Escape analysis
`go build -gcflags=-m=3 <package>` prints the compiler's escape decisions; editors with a language server
expose the same data as a code action ("Show compiler optimization details" in the guide's VS Code
example). Use it to find out why a value reached the heap, not to rewrite code that no profile points at.

## 1.4 Benchmarks
1. **Go 1.24 and later: write the loop as `for b.Loop() { ... }`.** The documentation says the first call
   resets the benchmark timer, so setup before the loop is not counted, and the loop keeps the variables in
   its body alive so the compiler cannot optimise the measured code away. The release notes add that the
   benchmark function runs once per `-count`, so expensive setup and cleanup also run once.
2. **Before Go 1.24, the loop is `for range b.N`** with the framework adjusting `b.N` until the measurement
   is stable; in that form, guard the result so it is not eliminated and reset the timer after setup. The
   second half is own guidance.
3. **Report allocations.** `b.ReportAllocs()` does for one benchmark what `-test.benchmem` does for a
   run, so allocation counts sit beside the timings.
4. **Keep the baseline.** Save the numbers from before the change and compare like with like: same machine,
   same toolchain, same flags. Own guidance.
