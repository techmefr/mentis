---
name: go-http-resilience-pitfalls
description: "Use when writing or reviewing Go code that serves or calls HTTP: building an http.Server, wiring routes with the standard mux, limiting request bodies, creating or reusing an http.Client, draining response bodies, or adding deadlines and retries around an outbound call."
---

# go-http-resilience-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Go HTTP defaults that look fine in a demo and fail in
production: **the zero value of a server or client has no timeout, so every timeout is something you set**.
The context and response-body basics are already in `go-conventions` §3 and §4.1 and are not repeated;
this block adds what sits next to them. API shape and status codes belong to `api-design`; the shutdown
sequence is `go-container-runtime` §3.

## When
- Creating an `http.Server`, registering routes, or reading a request body.
- Creating an `http.Client` or calling a downstream service.
- Adding a retry, a deadline or a timeout to an outbound call.
- A service hangs on a slow client or a slow dependency, or leaks connections.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Server: timeouts, header and body limits, standard mux patterns | an `http.Server` or its routes are written or reviewed | [`01-server.md`](./references/01-server.md) |
| 2 | Client: timeouts, reuse, response body draining, address building | an `http.Client` or an outbound request is written or reviewed | [`02-client.md`](./references/02-client.md) |
| 3 | Deadlines and retries around outbound calls | a retry, backoff or deadline is added | [`03-deadlines-retries.md`](./references/03-deadlines-retries.md) |

## Output / checkpoint
Every server in the diff sets its timeouts and a body limit, no call goes through a client without a
timeout or a context deadline, and any retry loop was exercised against a failing dependency, not only a
healthy one. `go vet ./...` is clean, and `go-conventions` §3 and §4 still hold on the changed files.

## Guardrails
- Never serve with the package-level `http.ListenAndServe` or `http.Get` in code that runs in production
  (§1.1, §2.1).
- Never retry a request that is not safe to repeat (§3.2).
- Versions: each rule names its Go version. Nothing was run while writing this block.

## Origin
Rewritten from the Go `net/http` package documentation and release notes (CC-BY-4.0 text, BSD-3 code) and
the gosec rule list (Apache-2.0), read 2026-10-08. Meant to be folded into `go-conventions` when the
extended version of that block lands. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
