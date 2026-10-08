# python-sqlalchemy-fastapi-pitfalls: origin and source stamps

> Provenance of `skills/python-sqlalchemy-fastapi-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real service by us. No query, server
or process was started while writing it.

This block is meant to be folded into the same-topic ORM, web-API and FastAPI sections when PR 118 lands;
until then it stands alone and cites only sections of `python-conventions` that exist on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| SQLAlchemy documentation: asyncio extension, pooling (multiprocessing section), error index, the queue pool signature | MIT, read 2026-10-08 | Session not safe across tasks, one session per task, `expire_on_commit=False`, the `MissingGreenlet` error, engine disposal and event loops, `dispose(close=False)` and its 1.4.33 version, pool size and overflow defaults |
| FastAPI documentation: async, response model, deployment, events | MIT, read 2026-10-08 | `def` handlers and dependencies run in a thread pool, response validation and filtering, lifespan shutdown |
| The FastAPI repository's agent skill and its references on dependencies, responses and Pydantic | MIT, read 2026-10-08 | Plain `def` when unsure, no class dependencies, no Ellipsis, no `RootModel`, router-level declarations, one operation per function, dependency `scope` |
| Starlette documentation: thread pool and middleware pages | official docs (licence file not read), read 2026-10-08 | Sync endpoints through AnyIO, default 40 tokens shared across libraries, `BaseHTTPMiddleware` and context variables |
| AnyIO documentation: threads | MIT, read 2026-10-08 | Default worker thread limiter of 40 |
| The Pydantic repository's agent skill | MIT, read 2026-10-08 | Where to use it, constraints before validators, after-validators, coercion, subclass serialisation, discriminated unions, forward annotations, recursive aliases |

## Rewrite notes
The pool budget product (§1.5.2), the overlap symptoms of a shared session (§1.1.2) and the "fix the
blocking call, not the pool" framing are our reasoning, labelled as such in the rules.

## Not verified
1. **Defaults of 5 and 10** are from the source of the queue pool class read in the SQLAlchemy repository;
   the async engine's default pool class was not read and may differ.
2. **Interleaving symptoms of a shared session** and **the post-fork hook advice** (§1.4.3) are general
   behaviour, not quoted from the pages read.
3. **Dependency `scope`** is in the FastAPI repository's skill (current main); the release that introduced
   it was not checked.
4. **Pydantic 2.13 polymorphic serialisation** is as stated in the Pydantic skill; not run.
5. **Dropped for lack of a documentation source:** lifespan state versus `app.state` in FastAPI, an
   asyncio debug environment variable for finding blocking calls, and the claim that the response is
   validated twice.
6. **Whether the Starlette limiter also covers `run_in_threadpool` callers other than endpoints** is as
   stated on the Starlette page; not tested.

## Related blocks
`python-conventions` (ORM and migrations, async), `python-async-no-blocking-calls`, `security-hardening`,
`python-container-runtime` (worker processes), `python-testing-strictness` (async fixtures).
