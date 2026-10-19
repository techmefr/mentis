---
name: laravel-http-client
description: "Use when writing or reviewing Laravel code that calls an outside HTTP service through the framework client: timeouts, retries, error handling, pooling, shared client setup, and faking it in tests."
---

# laravel-http-client

Step 6 of the pipeline (`WORKFLOW.md`). An outbound call is a boundary the framework does not make safe by
default: no error on a 4xx or 5xx, a generous default timeout, retries that can repeat a payment. Complements
`skills/code-baseline` §4 (consume a third-party payload through a typed reader) and
`skills/laravel-conventions` §11 (failure modes).

**Special status.** New block, 🟡: written from the rule files the Laravel team ships for its tooling, never
run on real work in house. Re-read the HTTP client page of the installed version when a method below is not
there.

## When
`Http::` calls, a macro or class wrapping an outside API, a `retry`, a `pool`, or a test that must not reach
the network.

## Steps
1. **A 4xx or 5xx is a response, not an exception.** Reading `->json()` straight off the call consumes an
   error body as if it were data. When a success payload is expected, call `->throw()` before consuming it,
   or branch on `successful()`, `notFound()` and the like and `throw()` for everything unexpected. Which
   statuses are expected is a decision made at the call site, written down in the code.
2. **Set both timeouts on purpose**: `connectTimeout()` for establishing the connection, `timeout()` for the
   response. The framework's default response timeout is long enough to hold a request or a worker for half
   a minute. Choose values for the calling context (a web request tolerates less than a queued job), and
   remember retries multiply the total elapsed time.
3. **Retry only what is safe to repeat.** Transient connection failures, 429 and 5xx on an idempotent read
   (`GET`) can be retried with a delay list. A state-changing call (a charge, an order, a send) is retried
   only when the remote API supports an idempotency key, and the same key is sent on every attempt. Use the
   `retry` callback to decide which exceptions count; never retry a 4xx that will fail the same way.
4. **One place per outside service.** Shared base URL, timeouts, auth and headers live in a macro or a
   dedicated client class, not repeated at every call. Credentials come from configuration
   (`skills/laravel-conventions` §7), never inline.
5. **Independent calls run in a pool.** `Http::pool` changes elapsed time, not error handling: each response
   in the pool still needs `throw()` or an explicit status check, and a name per request (`as`) keeps the
   results addressable.
6. **Tests never reach the network.** `Http::fake([...])` with the URL patterns the code uses, plus
   `Http::preventStrayRequests()` so an unfaked call fails the test. Assert what was sent with
   `Http::assertSent`, and test the failure paths the code handles: an error status, a timeout, a failed
   connection (`Http::failedConnection()`), a sequence of responses for a retry.

## Output / checkpoint
No outside call whose success payload is read without step 1, no state-changing retry without an idempotency
key, no call without both timeouts, and the tests for the call run with stray requests prevented. Checked at
`gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. New and changed code only (`skills/code-baseline` §0). A call to a service
the project already wraps goes through that wrapper; do not add a second client for it.

## Origin
Rewritten from the `http-client` rule file of Laravel Boost (`laravel/boost`, MIT, cloned 2026-10-02):
no exception on 4xx/5xx, separate connect and response timeouts, idempotency-bound retries, pool, fakes and
`preventStrayRequests`. Mechanisms only, rewritten in our words.
