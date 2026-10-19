---
name: ofetch-client-pitfalls
description: "Use when code calls an API with ofetch (a fetch wrapper for Node, browsers and workers): the retry defaults (one retry, none for POST, PUT, PATCH and DELETE, and a custom count that retries everything), the timeout that is off by default, thrown errors and error.data, ignoreResponseError, response parsing and binary or streamed bodies, JSON bodies and automatic headers, interceptors, shared defaults with ofetch.create (one-level clone, nested headers), query and baseURL merging, and typed responses."
---

# ofetch-client-pitfalls

A defensive block for an HTTP client built on ofetch. The two parts share one premise: **ofetch makes the
convenient choice for you (retry once, parse JSON, throw on a bad status, add JSON headers) and each default
has a case where it is wrong**: a retry that repeats a write, a call that waits forever because no timeout
was set, a typed response that nobody checked. The source is the library's own README, which at the time of
reading is the one for its second major version in alpha, so every default below is a statement to re-check
against the version in `package.json`. Deadlines and retries around an outbound call are treated for Go in
`skills/go-http-resilience-pitfalls` and for .NET in `skills/polly-resilience-pitfalls`; the Nuxt layer on top
(composables for data fetching) was not read and is out of scope.

## When
- A client module wraps ofetch, or a call sets `retry`, `retryStatusCodes`, `timeout` or `onResponseError`.
- A POST or another write is sent through a client that retries.
- An error handler reads `error.data`, or a 4xx or 5xx must not throw.
- A response is not JSON (a file, a stream, server-sent events), or a body is a class instance.
- Several call sites share a base URL, headers or interceptors.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Bodies, headers, parsing, errors, raw and native responses, query and base URL, streaming, types | a request or a response is built or parsed | [`01-requests-responses-and-errors.md`](./references/01-requests-responses-and-errors.md) |
| 2 | Retry, timeout, interceptors, shared defaults, option augmentation, proxy and certificates | a client is configured for reliability or shared across call sites | [`02-retry-timeout-and-shared-defaults.md`](./references/02-retry-timeout-and-shared-defaults.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a call to a stub server that returns a retryable status was
counted for a GET and for a POST with the client's real options (part 2.1), a call to a server that never
answers ended at the configured timeout (part 2.2), a 404 and a 500 produced the error the handler expects
(part 1.2), and a shared instance showed the headers a nested option produced (part 2.4). A client that was only
read is not verified.

## Guardrails
- Never set `retry` to a number on a client that sends writes without an idempotency design: a custom value
  retries every method, writes included (part 2.1).
- Never ship a client without a `timeout`; it is off by default (part 2.2).
- Never treat the type parameter `ofetch<T>()` as validation of the response (part 1.7).
- Never put secrets in `onRequest` logging, and never log a whole `options` object (part 2.3).
- Never disable certificate checking outside a throwaway test, and never in a shared instance (part 2.6).
- This block states the README of the ofetch repository as of the commit read on the date in
  [`references/origin.md`](./references/origin.md); that README describes a major version in alpha, and
  nothing was run while writing the block.

## Origin
Rewritten from the README of unjs/ofetch (MIT), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
