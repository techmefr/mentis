# flask-pitfalls §3 — Running in production

> Part 3 of `skills/flask-pitfalls`. Read it when the service is started, deployed or placed behind a proxy.
> Sourced from the Flask pages on the development server, debugging, deploying (index, Gunicorn, ASGI and
> proxy fix) and logging (commit `d086db8`), read 2026-10-16. Sentences marked "own guidance" are ours.

## 3.1 The development server and the debugger
1. **"Production" means "not development".** The deployment page says this applies whether the service is
   public to millions of users or private to one person, and that the development server is meant only for
   local work and is not designed to be efficient, stable or secure.
2. **Run a WSGI server instead** and, usually, an HTTP server in front of it. The documentation lists Gunicorn,
   Waitress, mod_wsgi, uWSGI and gevent as options and says to evaluate them against the project's needs.
3. **Point the WSGI server at the application the way the page shows.** Gunicorn takes `module:variable`; for
   an app factory it takes a call in quotes, `'module:create_app()'`, which is the same as importing the
   factory and calling it.
4. **The interactive debugger is for development only.** It runs arbitrary code from the browser and is PIN
   protected only; see part 2.1. In production the documentation points to an error-logging tool such as
   Sentry, or to logging and notifications, and says an external debugger may be enabled only temporarily.
5. **Own guidance, verify:** start the image the way production starts it, trigger an unhandled exception and
   confirm the response is a plain error page with no traceback and no debugger console.

## 3.2 Worker settings
1. **Gunicorn starts one worker by default**, which the page says is probably not what you want for the
   default worker type; `-w` sets the number of processes and the page gives `CPU * 2` only as a starting
   value. Own guidance: measure; the page makes no claim beyond a starting value.
2. **Do not run the WSGI server as root.** The application code would run as root. The cost is that it cannot
   bind port 80 or 443, which is the page's reason for a reverse proxy such as nginx or Apache in front.
3. **With a reverse proxy, do not bind the WSGI server to all interfaces.** The page says doing so lets
   clients bypass the proxy. Own guidance: bind to the loopback address or a private network the proxy
   reaches.
4. **Logs.** Flask uses the standard `logging` module; configure it as early as possible, ideally before the
   application object is created, because touching `app.logger` first adds a default handler. Gunicorn shows
   no per-request line by default; `--access-logfile=-` sends the access log to standard output.
5. **The gevent worker is for many long-lived connections** and is not Python's `async` and `await`; the
   default sync worker is the page's recommendation for most uses. Under ASGI, see part 1.2.

## 3.3 Behind a reverse proxy
1. **The application sees the proxy, not the client.** From Flask's point of view requests come from the HTTP
   server to a local address. The proxy has to send `X-Forwarded-` headers and Flask has to be told to use
   them.
2. **Wrap the WSGI app in Werkzeug's `ProxyFix`:**

```python
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
```

3. **Set each count to the number of proxies that set that header.** Incoming headers can be forged, so the
   middleware must be told how many proxies in the chain to trust, and not all proxies set all headers. The
   page says a wrong configuration can be a security issue.
4. **Only add it when there is a proxy.** Most hosting platforms are one, the page says, and need it.
5. **The four settings are named for the forwarded address, protocol, host and prefix** (own reading of the
   argument names; the page does not spell them out). The page says `Host` is validated against
   `TRUSTED_HOSTS` and may be changed by proxies (part 2.4). Own guidance: test with a request
   that passes through the real proxy and print the client address, scheme and host in a temporary route; a
   direct request to the application must not be able to supply those headers, which is one more reason for
   part 3.2 item 3.

## 3.4 Verify
Run the production start command locally, send one request through a proxy container and one straight to
the WSGI port, and compare the address, scheme and host the application reports; check that a missing page
and an exception both answer without a traceback.
