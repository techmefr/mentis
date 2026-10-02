# go-conventions §1 — Concurrency and goroutines: the most frequent mistake

> Section 1 of `skills/go-conventions`.

1. Every goroutine launched has an explicit stop mechanism (`context`, `WaitGroup`, or a `done` channel):
   a goroutine with no way out leaks silently on every call.
2. `sync.Mutex`/`sync.RWMutex` never copied by value (including through a struct that embeds it): the
   zero value is valid, never initialise it or pass a pointer out of reflex.
3. A closure inside a loop capturing the loop variable by reference (a classic bug in Go < 1.22, still
   present in legacy code); check the module's version before judging this point inapplicable.
4. The `cancel` returned by `context.WithCancel`/`WithTimeout` always called (often as a `defer`):
   otherwise a context leak.
5. Concurrent access to a map with no mutex or `sync.Map` panics at runtime ("concurrent map read and map
   write"), not detected statically.
6. A "check closed, then send" pattern on a channel a `Close()` method also closes is a race: a sender can
   pass the closed check, then have `Close()` run and close the channel before the send executes, panicking
   with "send on closed channel". A plain `sync.Mutex` held only around the check doesn't fix this — the
   lock must also be held across the send itself (e.g. `RLock`/`RUnlock` bracketing the `select` in the
   sender, `Lock` in `Close` before closing the channel), so the closer can't close until every in-flight
   sender has finished sending. Not caught by `go vet`, `staticcheck`, or `-race` unless a test actually
   races the two calls.
7. Bound the fan-out: a loop that starts one goroutine per item has no ceiling. Use a group with a fixed
   limit (`errgroup` with `SetLimit`) rather than a hand-rolled pool, and increment a `WaitGroup` before the
   `go` statement, never inside the goroutine.
8. Only the sending side closes a channel; a receiver that closes it turns the next send into a panic.
   Give channel parameters a direction, default to unbuffered, and treat a buffer size as a claim that needs
   a measurement behind it.
9. Every `select` that waits on work also waits on `ctx.Done()`; without it the goroutine outlives the caller
   that cancelled. A timer created by `time.After` in a hot loop allocates on each pass: reuse one timer.
10. A lock is never held across I/O or a call into code you do not own; keep critical sections to the field
    access they protect. Prefer the typed atomics for a lone counter or flag.
11. CI runs the tests with the race detector, and a package that starts goroutines checks for leaks at the end
    of its tests (a goroutine-leak checker in the test main).
