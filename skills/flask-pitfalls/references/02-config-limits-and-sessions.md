# flask-pitfalls §2 — Configuration, limits and sessions

> Part 2 of `skills/flask-pitfalls`. Read it when a Flask configuration is written or reviewed for a deployed
> service. Sourced from the Flask pages on configuration, security, the quickstart session section and
> debugging (commit `d086db8`), read 2026-10-16. Defaults are the ones those pages state; a version is named
> only where the page names it. Sentences marked "own guidance" are ours.

## 2.1 Debug mode
1. **Never deploy with debug on.** The configuration page says not to enable debug mode in production; the
   debugging page says the interactive debugger can run arbitrary Python code from the browser and is protected
   only by a PIN, which should not be relied on.
2. **Turn debug on with the command line flag or the `FLASK_DEBUG` environment variable, not in code.** The
   documentation recommends `flask --app <module> run --debug` and calls setting `DEBUG` in the configuration
   or in code strongly discouraged: `flask run` cannot read it early, and extensions may already have
   configured themselves from the previous value.
3. **`app.run(debug=True)` is mostly equivalent** but is the in-code form the documentation steers away from.
   Own guidance: a `__main__` block that calls it is the usual way debug reaches a deployed image; delete the
   block or keep it out of the entry point the image runs (part 3.1).
4. **With an external IDE debugger, keep debug mode and switch the built-in tools off:** `--debug --no-debugger
   --no-reload`. Without debug mode, Flask turns unhandled errors into generic 500 pages, so the external
   debugger would never see them.

## 2.2 Secret key and its rotation
1. **`SECRET_KEY` signs the session cookie** and anything else a library signs with it. It should be a long
   random `bytes` or `str`; the documentation generates one with `python -c 'import secrets;
   print(secrets.token_hex())'`. It defaults to `None`, and sessions need one.
2. **Never reveal it in a question or a commit.** The documentation says so in the configuration page and
   writes its own examples as placeholders. Own guidance: read the value from the environment or a secret
   store at start-up, and do not reuse any key shown in documentation, including the example values in the Flask pages.
3. **The default session is client-side.** The cookie holds the serialised session, signed: the user can read
   it but cannot change it without the key. Own guidance: put nothing in it you would not show to the user.
   Values that do not persist, with cookies enabled and no clear error, can be a cookie larger than the browser
   accepts; the quickstart says to check its size. Server-side sessions come from an extension.
4. **Rotate with `SECRET_KEY_FALLBACKS`** (added in Flask 3.1): a list of old keys still accepted for
   unsigning, so active sessions survive a change. The page says to remove old keys after a suitable period
   because every extra key adds checking cost, that the default implementation tries the last key in the list
   first (so oldest to newest is a sensible order), and that the built-in session supports it while extensions
   that use `SECRET_KEY` may not.

## 2.3 Request size and form limits
1. **There is no size limit by default.** `MAX_CONTENT_LENGTH` is `None`: no limit at the Flask level.
   Exceeding a set limit raises 413. With `None`, a request without a `Content-Length` header is not read at
   all unless the WSGI server says it terminates the stream, so a truly unbounded stream is still refused.
2. **Two form limits exist and have defaults.** `MAX_FORM_MEMORY_SIZE` (a non-file field in a multipart body,
   default 500,000 bytes) and `MAX_FORM_PARTS` (number of fields, default 1,000), both added in Flask 3.1 and both
   answering 413. The security page works out that together they allow a form up to 500 MB in memory at the
   defaults; lower them for forms that never need that.
3. **Set the limit per endpoint where needs differ.** Each request starts from the config value and the same
   limits can be set on the individual request object (`max_content_length`, `max_form_memory_size`,
   `max_form_parts`), so an upload endpoint can be larger than the rest of the service.
4. **These limits are one layer.** The page says to review the limits of the operating system, the container
   platform, the WSGI server, the HTTP server and the hosting platform as well: process resource limits and
   timeouts live there.
5. **Verify** by sending a body one byte over the limit to an endpoint and reading a 413, then a multipart form
   with more fields than allowed.

## 2.4 Trusted hosts
1. **By default any `Host` header is accepted.** Browsers do not let a page set it, but other clients can, and
   Flask uses it to build full URLs, for example `url_for(..., _external=True)` in an email.
2. **Set `TRUSTED_HOSTS`** (a list; an exact name, or a leading dot to match every subdomain). An invalid host
   gives a 400. Validation happens during routing, and `before_request` and `after_request` callbacks still
   run for that request.
3. **A proxy may rewrite `Host`.** Telling the application which proxy values to trust is part 3.3.
4. **Verify** with a request that carries an unlisted `Host` and expect 400.

## 2.5 The session cookie
1. **Default values matter.** `SESSION_COOKIE_HTTPONLY` is on by default; `SESSION_COOKIE_SECURE` defaults to
   off (it only makes sense when the service is served over HTTPS) and `SESSION_COOKIE_SAMESITE` defaults to
   `None`. The security page recommends `Secure`, `HttpOnly` and `SameSite` `Lax` (`Strict` blocks the cookie on
   all external requests, including following a plain link).
2. **Leave `SESSION_COOKIE_DOMAIN` unset.** Unset, the browser sends the cookie to the exact host only; the
   page says that is more restricted and more secure than setting it.
3. **Changing the cookie's name or domain after cookies exist can create a second cookie** and browsers may send
   both in an undefined order. The configuration page suggests changing `SESSION_COOKIE_NAME` too, or otherwise
   invalidating old sessions.
4. **A permanent session expires after `PERMANENT_SESSION_LIFETIME`** (default 31 days), and Flask's default
   implementation also rejects a signature older than that. The security page says lowering it can mitigate
   replay of an intercepted cookie, and shows clearing the session before storing the user id at login.
5. **Partitioned cookies** (`SESSION_COOKIE_PARTITIONED`, added in 3.1) are for a session used inside a
   third-party frame; enabling it implies `Secure`.

## 2.6 Cross-site request forgery
1. **Flask does not protect against it.** The security page explains that authentication held in a cookie is
   sent with requests triggered by other sites, that every state-changing request therefore needs a one-time
   token stored in the cookie and also sent with the form, compared on arrival, and that Flask leaves this to
   the form-validation layer, which Flask does not have.
2. **Own guidance:** pair the `SameSite` setting of part 2.5 with a token from a library or from your form
   layer; the cookie attribute alone is not what the page describes.

## 2.7 Verify
Print the effective configuration at start-up with secret values redacted, and check `DEBUG` false, a secret
set, the three size limits, the trusted hosts and the three cookie attributes against the list above; then run
the checks named in part 2.3 and part 2.4.
