---
name: laravel-throw-dont-return-errors
description: "Use when a controller, action, job or command action can fail: throw the exception, never build and return the error response by hand."
---

# laravel-throw-dont-return-errors

Narrow trigger extracted from `skills/laravel-conventions` §11.1–§11.5, so "what happens when this
fails" routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing any code path that can fail — a controller action, a domain action, a job's
`handle()`, a console command — and the failure needs to become a response, a log entry or a
tracked error.

## Steps
1. **Throw. Never build and return the error response yourself.** The framework's exception
   handler is the one place that turns a failure into a status, a body and an error-tracking event
   — it only sees what is thrown. A hand-returned 500 is invisible to error tracking: the endpoint
   fails in production and the error rate stays flat, which is strictly worse than letting it crash.
2. **Reporting is not handling.** Catching an error, sending it to the tracker and then continuing
   or returning makes the operation look successful to everything upstream.
3. **Never hand-roll JSON-versus-HTML content negotiation** in the catch. Throw (or use the
   framework's abort helper) and let the handler negotiate — a hand-built branch drifts from the
   app's configured policy the moment that policy changes.
4. Where a failure always means one HTTP status, make the exception HTTP-native (extend the
   framework's own HTTP exception) rather than mapping it in a render callback.

## Output / checkpoint
Every failure path in the diff ends in a `throw`, never a `return response(...)` built inside a
`catch`. A test names the failure and asserts it goes red (`laravel-conventions` §9.14).

## Guardrails
- A `catch` earns its place by doing something — retrying, converting to a domain exception,
  committing a genuine fallback. An empty `catch`, a log-only `catch`, or one returning
  null/false/empty that the caller cannot distinguish from a real result is the same swallow in
  three costumes.
- Inside a transaction, a throw *is* the rollback — catching and continuing there commits a
  half-finished unit of work (`laravel-conventions` §11.9).
- The full argument (message audience, five ways an external call fails, identifiers-not-payloads
  in a report) lives in `skills/laravel-conventions` §11 — read it before writing a `catch`.

## Origin
No external source: this is `skills/laravel-conventions` §11.1–§11.5 extracted to its own trigger.
Written 2026-09-09, same pilot as `laravel-no-db-enums`.
