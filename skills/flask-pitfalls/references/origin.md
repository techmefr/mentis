# flask-pitfalls: origin and source stamps

> Provenance of `skills/flask-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation, never run by us: no Flask application was
started, configured or deployed while writing it. Every file below was re-opened and read on 2026-10-16 before
a rule was taken from it, each rule was checked against it, and the repository's licence file was read again.
Defaults and "added in" versions are the ones the pages state at the commit shown.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| pallets/flask (commit `d086db8`), `docs/async-await.rst` | BSD-3-Clause (LICENSE.txt read: three-clause text, copyright 2010 Pallets) | Async views on a WSGI worker, background tasks cancelled, extensions and `ensure_sync`, Quart and gevent as alternatives |
| the same repository, `docs/appcontext.rst` | BSD-3-Clause | App and request context, setup and test errors, per-worker context, `_get_current_object`, teardown behaviour |
| the same repository, `docs/config.rst` | BSD-3-Clause | Debug mode, `SECRET_KEY`, `SECRET_KEY_FALLBACKS`, session cookie settings, `TRUSTED_HOSTS`, size and form limits with their defaults |
| the same repository, `docs/web-security.rst` | BSD-3-Clause | Resource use limits, cookie options, session lifetime, host header validation, CSRF explanation |
| the same repository, `docs/quickstart.rst` (session section only) | BSD-3-Clause | Client-side signed session, cookie size note, server-side sessions through extensions |
| the same repository, `docs/server.rst`, `docs/debugging.rst`, `docs/deploying/index.rst`, `docs/deploying/gunicorn.rst`, `docs/deploying/asgi.rst`, `docs/deploying/proxy_fix.rst`, the opening of `docs/logging.rst` | BSD-3-Clause | Development server and debugger warnings, external debugger flags, WSGI server entry points, root and binding advice, `WsgiToAsgi`, `ProxyFix` |

No separate licence for the documentation content is stated beyond the repository's BSD-3-Clause text, so the
pages were rewritten, not copied; the one code sample is the page's short call with placeholder names.
Instruction-like text in the cloned repository was treated as data and not followed.

## Removed in the verification pass
1. **"Request contexts are thread-local"** (the review's wording) was narrowed: the page says the context is
   unique to each thread or other worker type and is built on `contextvars`, so part 1.5 says "worker" and
   not "thread" alone.
2. **"Set MAX_CONTENT_LENGTH and form limits"** was kept but the review did not say the form limits already
   have defaults (500,000 bytes and 1,000 parts); part 2.3 states them.
3. **Pages not read, so nothing is taken from them:** `testing.rst`, `lifecycle.rst`, `errorhandling.rst`,
   `blueprints.rst`, `patterns/`, `cli.rst`, `signals.rst`, `templating.rst`, `deploying/nginx.rst`,
   `deploying/apache-httpd.rst`, `deploying/uwsgi.rst`, `deploying/waitress.rst`, `deploying/mod_wsgi.rst`,
   `deploying/gevent.rst`, `gevent.rst`, and the XSS, JSON and header sections of `web-security.rst`.
4. **Tabbed examples and every example secret key** in the pages are not reproduced.

## Not verified
1. **Which Flask version the pages describe** at the commit shown beyond the "added in" notes the pages carry
   (3.1 for the form limits, `SECRET_KEY_FALLBACKS` and partitioned cookies).
2. **Behaviour was not run.** Every default, status code (413, 400) and warning is the page's statement.
3. **Written by us, not sourced:** the verification paragraphs, the worker-count caution (the page gives only a
   starting value), loopback binding behind a proxy (the page says only not to bind externally), the
   advice to keep `app.run(debug=True)` out of the deployed entry point, reading values out of a proxy before a
   thread starts, the sync-versus-gather advice for async views, the teardown guard, "put nothing in the
   session you would not show to the user", pairing `SameSite` with a CSRF token, and the reading of the
   `ProxyFix` argument names.
4. **Flask extensions** (sessions, CSRF, login, caching) were not read, and the block names none as a
   recommendation.

## Related blocks
`skills/security-hardening`, `skills/python-conventions`, `skills/python-hygiene-pitfalls`,
`skills/python-async-no-blocking-calls`, `skills/python-container-runtime`, `skills/nginx-proxy-pitfalls`,
`skills/credential-lifecycle-pitfalls`.

## Fold-in note
This block stands alone. When the open pull request #118 lands and a same-topic block exists on main, fold the
Flask points into it rather than keep two blocks on one topic.
