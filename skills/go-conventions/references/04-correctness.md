# go-conventions §4 — Other correctness

> Section 4 of `skills/go-conventions`.

1. An HTTP response's `resp.Body` always closed (`defer resp.Body.Close()`), otherwise a connection leak.
2. `defer` inside a loop accumulates until the end of the function, not of the iteration: resource
   exhaustion (files, locks) on a long loop.
3. An `err` variable redeclared with `:=` shadowing a parent scope's error; check that no error from the
   outer scope is silently lost.
4. `interface{}`/`any` as a catch-all to avoid typing properly: prefer generics or a concrete type.
5. Slices/maps received or returned at API boundaries = a reference to the caller's data, mutable without
   their knowledge: copy if isolation is necessary.
6. **`os.Exit`/`log.Fatal` only ever called from `main()`, and at most once there.** Anywhere else they
   skip every deferred cleanup on the way out (no closed files, no released locks, no flushed logs) —
   every other function returns its error and lets the caller decide. Wrap `main()`'s own logic in a
   `run() error` so the exit call is the last line, not scattered through the business logic.
