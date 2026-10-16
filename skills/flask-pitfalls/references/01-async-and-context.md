# flask-pitfalls §1 — Async views, background work and the context

> Part 1 of `skills/flask-pitfalls`. Read it when a view is `async`, when work must outlive the request, or
> when a context error or a request-scoped object crossing a thread is the problem. Sourced from the Flask
> pages on async and await and on the app and request context (commit `d086db8`), read 2026-10-16. Sentences
> marked "own guidance" are ours.

## 1.1 What an async view buys
1. **Async needs the extra and a loop per request.** Routes, error handlers and the before, after and teardown
   hooks may be coroutine functions when Flask is installed with its `async` extra. Flask is a WSGI
   application: for an async view it starts an event loop in a thread, runs the view there and returns the
   result.
2. **One request still occupies one worker.** The number of requests handled at the same time does not change.
   What an async view allows is concurrent IO inside one request, for example several database queries or
   calls to an external API awaited together.
3. **Async is not faster by itself.** The documentation says it helps concurrent IO-bound work and will probably
   not improve CPU-bound work, and that ordinary synchronous views stay right for most cases. Own guidance: a
   view that awaits one call after another gains nothing from `async def`; keep it synchronous unless it
   gathers several independent calls.
4. **A mostly async code base is a different framework question.** The documentation says Flask's async
   support is less performant than an async-first framework because of how it is built, points to Quart (a
   reimplementation of the Flask API on ASGI) for many concurrent or long-running requests and websockets
   without more worker processes, and names gevent as the other route. Choosing between them is a decision
   about the project, not a Flask setting.
5. **Only asyncio is supported out of the box.** Overriding `Flask.ensure_sync` is the documented way to use a
   different library.

## 1.2 Background tasks started from a view
1. **A task spawned in an async view is cancelled when the view returns.** The loop runs until the view
   completes and then stops, and any task not yet finished is cancelled. `asyncio.create_task` in a view
   therefore does not give you background work.
2. **Hand background work to a task queue.** The documentation's advice is to have the view trigger work in a
   queue rather than spawn it. It also says tasks can run under an ASGI server with the `WsgiToAsgi` adapter
   from `asgiref`, because that adapter keeps one loop running; that is the documented exception and changes
   how the service is deployed (part 3).
3. **Verify** by starting a task that writes a marker after a short sleep, calling the view under the real
   server, and checking that the marker never appears (own guidance: this is the cheapest way to show the
   team the cancellation).

## 1.3 Extensions and async views
1. **An extension written before Flask had async support does not await your view.** The documentation says
   decorators such as a login or cache wrapper will probably not work on an async view because they neither
   await it nor are awaitable, and other calls the extension offers will probably block if called from an
   async view.
2. **Check the extension's changelog** for async support before putting one on an async view; the
   documentation says to ask the extension for support if it has none.
3. **If you write a decorator, call the view through `current_app.ensure_sync(func)`** so that both a
   synchronous and a coroutine view work.

## 1.4 Context errors and what they mean
1. **`current_app` and `g` need an app context; `request` and `session` need a request context.** A request
   pushes a request context, a CLI command pushes an app context. The proxies exist while a context is pushed
   and not after it is popped.
2. **"Working outside of application context" during setup** (an extension, a database initialisation in the
   app factory): push one yourself with `with app.app_context():` around that code, since the factory has the
   app object.
3. **The same error elsewhere means the code is in the wrong place.** The documentation says it most likely
   belongs in a view function or a CLI command, not at import time.
4. **"Working outside of request context" is mostly a test symptom.** Fix it by driving a full request with the
   test client, or by wrapping a single function in `with app.test_request_context(path, query_string=...)`.
5. **Do not import the `app` object into modules to reach the config.** The context pattern exists to avoid
   circular imports, and an app factory or a reusable blueprint has no `app` to import.

## 1.5 Proxies belong to one worker
1. **The context is unique to each thread or other worker type.** A proxy handed to another thread does not
   know the context of the thread that made it and will fail there.
2. **Pass the value, not the proxy.** Read what you need (`request.args.get(...)`, `session["id"]`) into a plain
   variable before starting the thread or the task. Own guidance: the values, not the proxy, are what a
   queue payload should carry too.
3. **When the real object is required, take it from the proxy.** A proxy has its own type and identity. Use
   `_get_current_object()` (the documentation's example sends `current_app._get_current_object()` as the sender
   of a signal) where the code compares identity or needs the true type.

## 1.6 Teardown callbacks
1. **Teardown functions run when the context is popped, even after an unhandled exception.** They may be called
   more than once in some test setups, and nothing guarantees that any other part of the dispatch ran.
2. **Write each one so that it depends on no other callback.** All teardown callbacks are called even if one
   raises. Own guidance: a teardown that closes a database session should first check that one was opened.

## 1.7 Verify
Call an `async` view under the WSGI server you deploy with and confirm it returns; start a throwaway task from
it and confirm the cancellation (part 1.2); run a function that reads `request` under
`test_request_context` and one that reads `current_app` under `app.app_context()`; and start a thread that
reads `request` without a copied value to see the error the team will meet.
