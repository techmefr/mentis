# go-http-resilience-pitfalls §3 — Deadlines and retries

Deadlines rest on the `context` documentation and apply to any supported Go version. In §3.3, only the
repeat-safety rule (point 1) rests on a page read (RFC 9110, section 9.2.2); the rest is **own guidance** and
stays marked, since no permissive source was found for it.

## 3.1 Every outbound call has a deadline
1. **Derive the call's context from the one you received** (`go-conventions` §3.2), with
   `context.WithTimeout` or `WithDeadline`, and call the returned `cancel` as soon as the call completes
   (`go-conventions` §1.4). The `context` documentation says failing to call it leaks the child and its
   children until the parent is cancelled, and that `go vet` checks that cancel functions are used on all
   control-flow paths.
2. **Keep `Client.Timeout` as the backstop, not as the only deadline** (§2.1): a per-call context deadline
   lets one slow dependency fail fast while others keep a longer budget.
3. **A deadline spent is a deadline spent.** Derive a retry's context from the same parent so the total
   time across attempts stays inside the caller's budget.

## 3.2 Work that must outlive its request
`context.WithoutCancel` (Go 1.21 and later) returns a context that is not cancelled when its parent is
cancelled and reports no deadline and no error. Use it only for work that is meant to finish after the
request ends, and give that work a deadline of its own; own guidance, since the function otherwise removes
every limit the parent carried.

## 3.3 Retries
1. **Retry only an operation that is safe to repeat.** A read, or a write the receiver deduplicates. Anything
   else risks doing the side effect twice. RFC 9110 lists the safe methods plus `PUT` and `DELETE` as
   idempotent, says an idempotent request may be retried automatically after a connection fails before any
   response, says a non-idempotent one (most `POST`) should not be unless the client knows it is effectively
   idempotent or can confirm the first attempt had no effect, and says a request that already failed on an
   automatic retry should not be retried again.
2. **Cap the attempts and the delay,** grow the delay between attempts, and add random jitter so many
   callers do not retry in step.
3. **Wait in a `select` on the context's `Done` channel and a timer,** not in a bare sleep, so cancellation
   ends the wait at once. A `time.After` in the loop keeps its timer until it fires on a module whose `go.mod`
   says Go below 1.23; the Go 1.23 release notes say unreferenced timers are collected from that version.
   On older modules use `time.NewTimer` and `Stop` it when the context wins.
4. **Do not retry a response that says the request itself is wrong.** A client-error status will fail the
   same way each time; retry connection failures and server-side errors.
5. **Log the final failure once with the attempt count,** and do not log each attempt at error level.
