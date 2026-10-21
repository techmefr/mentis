---
name: laravel-http-client
description: "Use when writing or reviewing Laravel code that calls an outside HTTP service through the framework client: timeouts, retries, error handling, pooling, shared client setup, and faking it in tests."
---

# laravel-http-client

Step 6 of the pipeline (`WORKFLOW.md`). An outbound call is a boundary the framework does not make safe by
default: no error on a 4xx or 5xx, a generous default timeout, retries that can repeat a payment. Complements
`skills/code-baseline` §4 (consume a third-party payload through a typed reader) and
`skills/laravel-conventions` §11 (failure modes).

**Special status.** New block, 🟡: never run on real work in house. Checked on 2026-10-20 against the
framework's HTTP client documentation (12.x) and the Laravel Boost rule file; re-read the page of the installed
version when a method below is not there.

## When
`Http::` calls, a macro or class wrapping an outside API, a `retry`, a `pool`, or a test that must not reach
the network.

## Steps
1. **A 4xx or 5xx is a response, not an exception.** Reading `->json()` straight off the call consumes an
   error body as if it were data. When a success payload is expected, call `->throw()` before consuming it,
   or branch on `successful()`, `notFound()` and the like and `throw()` for everything unexpected. Which
   statuses are expected is a decision made at the call site, written down in the code.
2. **Set both timeouts on purpose**: `connectTimeout()` for establishing the connection, `timeout()` for the
   response. The documented defaults are 30 seconds for the response and 10 seconds for the connection, long
   enough to hold a request or a worker for half a minute (docs, Timeout). Choose values for the calling context (a web request tolerates less than a queued job), and
   remember retries multiply the total elapsed time.
3. **Retry only what is safe to repeat.** Transient connection failures, 429 and 5xx on an idempotent read
   (`GET`) can be retried with a delay list. A state-changing call (a charge, an order, a send) is retried
   only when the remote API supports an idempotency key, and the same key is sent on every attempt. Use the
   `retry` callback (third argument) to decide which exceptions count; never retry a 4xx that will fail the same
   way (own guidance). When every attempt fails, `retry` throws a `RequestException` unless `throw: false` is
   passed, and a connection failure still throws a `ConnectionException` in that case (docs, Retries).
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
Rewritten from the `http-client` rule file of Laravel Boost (`laravel/boost`, MIT, LICENSE read 2026-10-20) and
checked the same day against the framework's HTTP client documentation, 12.x (read for facts only, our words):
Error Handling (no exception on 4xx/5xx, `throw`), Timeout (30 s and 10 s defaults), Retries, Request Pooling
(`as`, `concurrency`), Macros, Faking Responses (`failedConnection`, sequences), Inspecting Requests,
Preventing Stray Requests. Not found in either source, so own guidance: the idempotency-key condition on
state-changing retries is stated by the rule file but is not a documented framework feature; "never retry a 4xx".
Mechanisms only, rewritten in our words.
