# go-container-runtime §2 — CPU and memory

Each rule names the Go version it applies to.

## 2.1 GOMAXPROCS and the CPU quota
1. **Go 1.25 and later: leave `GOMAXPROCS` unset.** On Linux the default now considers the cgroup CPU
   bandwidth limit and uses it when it is lower than the number of logical CPUs; on every OS the runtime
   re-evaluates periodically as the CPU count or the limit changes. CPU **requests** are not considered,
   only the bandwidth limit (Go 1.25 release notes). The switch follows the **language version** in the
   module's `go` directive, not the toolchain that built the binary: the runtime documentation says
   `containermaxprocs=0` and `updatemaxprocs=0` are the defaults for language version 1.24 and below, so a 1.25
   toolchain building a module that still declares 1.24 keeps the old behaviour. Raise the directive.
2. **A manual value switches that off.** Setting the `GOMAXPROCS` environment variable or calling
   `runtime.GOMAXPROCS` disables both behaviours; so do the settings `containermaxprocs=0` and
   `updatemaxprocs=0` in `GODEBUG`. A deploy template that exports the host's CPU count therefore
   reintroduces the old problem. The runtime documentation adds that `SetDefaultGOMAXPROCS` restores the
   automatic behaviour after a manual call.
3. **Go 1.24 and earlier: the default ignores the container quota.** The runtime documentation gives
   `containermaxprocs=0` as the default for language version 1.24 and below (the `go` directive again). Set `GOMAXPROCS` from the quota in the deploy manifest,
   or import the maintained shim library, whose README describes setting it from the Linux container CPU
   quota. Naming the dependency is the whole recommendation: the user adds it themselves.
4. **Why it matters, with one data point.** The shim's README reports a load balancer run at a 2-core quota:
   with `GOMAXPROCS` at the machine default of 24 it measured 22,191 requests per second and a 99.9th
   percentile of 76.19 ms, against 44,715 and 26.38 ms with the value equal to the quota; the median latency
   moved the other way (0.45 against 0.84 ms). The README shows cgroup throttling counters for the oversized
   setting and no second set of counters for the matched one. One service's measurement, not a law: measure
   yours (see Measure, below).

## 2.2 Memory limit
1. **Set `GOMEMLIMIT` when the Go program is the only user of the container's memory.** The guide's
   condition is that the environment is entirely under your control and the program alone has access to the
   reservation, such as a container memory limit.
2. **Leave 5 to 10% headroom below the container limit,** for memory sources the runtime does not know
   about (the guide's rule of thumb); the runtime documentation names what the limit leaves out: memory
   allocated by C code, mappings made through system calls, and memory the kernel holds for the process. The limit counts the Go heap and other runtime-managed memory, as
   total runtime memory minus released heap, and it is **soft**: the runtime makes reasonable effort, no
   guarantee. Syntax: a number of bytes with an optional `B`, `KiB`, `MiB`, `GiB` or `TiB` suffix
   (`runtime/debug.SetMemoryLimit`, added in Go 1.19; the environment variable sets the initial value).
3. **Do not use it to dodge an OOM kill when the program already runs near its limit.** The guide says this
   swaps an out-of-memory risk for severe slowdown, and that constant collection without progress
   (thrashing) can stall the program indefinitely, which it considers often worse than a fast OOM failure.
   The collector caps its own CPU use at roughly 50% over a window to soften this.

## 2.3 GOGC
`GOGC` trades collector CPU against heap size: doubling it roughly doubles heap overhead and halves the
collector's CPU cost, and the reverse. Change it only with a measurement (see Measure, below). From Go 1.26 the Green Tea
collector is on by default (an experiment in 1.25, switchable at build time with `GOEXPERIMENT`); the notes
expect 10 to 40% less collection overhead in programs that lean heavily on the collector, so numbers taken
on an older toolchain are stale.

## 2.4 What the limits do not do
The memory limit does not change `GOMAXPROCS`, and `GOMAXPROCS` limits threads running user-level Go code,
not threads blocked in system calls (runtime documentation).

## 2.5 Measure
Run the container under its real limits and read `GODEBUG=gctrace=1` (collection events and pause lengths)
and a CPU profile before changing anything. The guide's pointers: time in `runtime.mallocgc` above about
15% points to heavy allocation, and time in `runtime.gcAssistAlloc` above about 5% points to a program
outpacing the collector. Profiling steps are in `go-performance` §1.
