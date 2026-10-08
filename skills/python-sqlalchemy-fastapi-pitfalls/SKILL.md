---
name: python-sqlalchemy-fastapi-pitfalls
description: "Use when a Python service uses SQLAlchemy sessions or pools with async code, forks or worker processes, or a FastAPI app, or when Pydantic models define a boundary: one AsyncSession per concurrent task, expire_on_commit under asyncio, disposing an engine at shutdown and after a fork, the pool connection budget across processes and replicas, sync versus async handlers and the 40-thread limit, class dependencies, ellipsis and RootModel, middleware and context variables, and Pydantic at untrusted boundaries only (built-in constraints, subclass serialisation, forward references)."
---

# python-sqlalchemy-fastapi-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the failures that pass every single-request test and appear under
concurrency, after a fork, or at scale-out. The three sections share one premise: **a database session, a
connection pool and a thread pool are shared resources with a fixed size and an owner, and the code that
forgets who owns them works until the load or the process model changes**. The ORM rules that hold on every
stack (no cascade delete, non-loading relationships, transactions, migrations) are in `python-conventions`
§7 and the async rules in §4; this block adds what they do not say.

## When
- Opening a session in async code, or running several queries concurrently.
- A worker pool, multiprocessing, a forking server or a process manager starts more than one process.
- Sizing a connection pool, or adding replicas or workers.
- Writing a FastAPI route, a dependency, a middleware or a response type, or choosing `def` or `async def`.
- Defining a Pydantic model, especially one that is also returned.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | SQLAlchemy sessions and pools: session per task, `expire_on_commit`, engine disposal, fork, pool budget | an async session, a process fork or a pool size is involved | [`01-sqlalchemy-sessions-and-pools.md`](./references/01-sqlalchemy-sessions-and-pools.md) |
| 2 | FastAPI: handler kind and the thread limit, dependencies, router and response declarations, middleware | a route, a dependency, a middleware or a response type is written | [`02-fastapi-handlers.md`](./references/02-fastapi-handlers.md) |
| 3 | Pydantic at the boundary: where to use it, constraints, subclass serialisation, forward references | a model is defined or returned | [`03-pydantic-boundary.md`](./references/03-pydantic-boundary.md) |

## Output / checkpoint
Each rule was exercised: two concurrent tasks each ran with their own session and a shared one was shown to
fail (§1), the process was forked or the worker count raised and the connection count at the database stayed
under its limit (§1), a route with a blocking call was moved to `def` and the event loop stayed responsive
(§2), and a returned subclass was serialised and its extra field checked (§3). A diff verified only with one
request on one process is not verified.

## Guardrails
- Never pass one `AsyncSession` to several concurrently running tasks (§1.1).
- Never share an engine's pooled connections with a child process (§1.4).
- Never put a blocking call in an `async def` handler (§2.1); the rule itself is
  `python-async-no-blocking-calls`.
- Never define a Pydantic model for a class only your own code constructs (§3.1).
- Library facts are as of the SQLAlchemy, FastAPI, Starlette, AnyIO and Pydantic documentation read on the
  date in [`references/origin.md`](./references/origin.md); several rules name the version they apply from.
  Check the one the project pins. Nothing was run while writing this block.
- Adding a package is the user's step; this block names it and stops.

## Origin
Rewritten from the SQLAlchemy, FastAPI, Starlette and AnyIO documentation, the FastAPI and Pydantic
repositories' own agent skills (MIT), read 2026-10-08. This block is meant to be folded into the same-topic
ORM, web-API and FastAPI sections when PR 118 lands. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
