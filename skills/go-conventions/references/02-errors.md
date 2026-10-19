# go-conventions §2 — Error handling

> Section 2 of `skills/go-conventions`.

1. No returned error ignored without an explicit `_` or handling.
2. `errors.Is`/`errors.As` rather than a direct comparison (`err == SomeErr`) or a direct type assertion:
   breaks as soon as an error gets wrapped.
3. `%w` to wrap an error (preserves the chain for `errors.Is`/`As`), `%v` only if the obfuscation is a
   deliberate choice, not a default.
4. A `recover()` that swallows the error without rethrowing or logging it hides a real bug: never a silent
   `recover`.
5. **`panic` is not error handling.** A library or a service function returns an `error` for anything a
   caller could reasonably encounter; `panic` is reserved for a programmer error the caller couldn't have
   guarded against (a genuinely unreachable branch, a broken invariant at startup) or an unrecoverable
   condition, and `recover` belongs at the top of a goroutine's own boundary, not scattered to paper over
   an error path that should have returned normally.
6. **A type assertion always uses the comma-ok form** (`t, ok := i.(string)`), never the single-return form
   outside a context that has already proven the type: the single-return form panics on a mismatch, which
   is exactly the silent-crash shape this section exists to prevent elsewhere.
7. **An error is handled once**: either returned (with context added) or logged, never both. A function that
   logs and then returns the same error makes the aggregator show one failure several times.
8. Wrap with `%w` inside the program and use `%v` at a boundary you do not want callers to depend on (a
   public API, a process edge), so the chain is exposed on purpose.
9. Independent failures are combined with `errors.Join`. Error strings start lower-case and carry no trailing
   punctuation. Expected conditions are sentinel values; errors that carry data are types, inspected with
   `errors.As`.
10. A technical error never reaches the end user: translate it to a message at the edge and keep the detail in
    the structured log.
