# § 4 — Settings, deployment and the security surface

> Section 4 of `skills/django-conventions`. Read it when a setting is added or changed, a deployment is prepared,
> a form or an endpoint that changes state is written, a template outputs user data, or the site is put behind a
> proxy. Read 2026-10-02 from the Django deployment checklist, the security topic, the CSRF reference, the
> middleware reference and the `django-admin` reference, plus the settings layout of a public style guide.

1. **The deployment checklist is a command: `check --deploy`.** Run it against the production settings module,
   in CI and on the deployed environment; choose the failing level with `--fail-level`. It automates part of
   the checklist, not all of it: the rest (the points below) is review. `runserver` is a development server and
   is never what serves production; use a WSGI or ASGI server.
2. **`SECRET_KEY` is a large random value, kept out of the repository, read from the environment or a file, and
   never shared with another deployment.** Rotation goes through `SECRET_KEY_FALLBACKS`, and the old key is
   removed from it promptly. Database passwords are as sensitive as the key. Settings modules themselves can
   be confidential: publish a development settings file and keep the production one private.
3. **`DEBUG` is never true in production.** It leaks source excerpts, local variables, settings and library
   versions in the error page.
4. **`ALLOWED_HOSTS` is explicit,** and with `DEBUG` off the site does not run without it. A wildcard means your
   own validation of the `Host` header. Code that reads the host from `request.META` bypasses the validation;
   use `get_host()`. `X-Forwarded-Host` is trusted only when the setting that enables it is deliberately turned
   on. A front web server also rejects unknown hosts, so they never reach the logs.
5. **HTTPS everywhere on a site with sign-in, not just on the sensitive pages:** the session cookie is shared
   between HTTP and HTTPS, so a single plain request leaks it. Redirect HTTP to HTTPS (at the front server, or
   `SECURE_SSL_REDIRECT`), set `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE`, and enable HSTS
   (`SECURE_HSTS_SECONDS`, with its include-subdomains and preload companions where they apply).
   Behind a TLS-terminating proxy, `SECURE_PROXY_SSL_HEADER` must be set, and set correctly: leaving it out
   causes CSRF failures and getting it wrong is dangerous, so read that setting's warnings in full.
6. **Order middleware on purpose.** The security middleware goes near the top so that the SSL redirect
   short-circuits everything else; cache-update middleware sits before the ones that modify `Vary`
   (session, gzip, locale), and compression before any that reads or changes the body.
7. **Settings are layered, with everything in the base and nothing production-only in code.** A base module holds
   the settings; development, test and production modules import it and override a handful; anything that must
   differ in production is controlled by an environment variable, so there is no production-only code path to
   go untested. Third-party integrations (task queue, CORS, error tracking) get their own modules. Read
   environment variables once, in settings, through one helper.
8. **Media files are untrusted.** Uploaded files are never interpreted by the web server (an uploaded script is
   stored, not run), live under `MEDIA_ROOT` outside the application code, and `STATIC_ROOT` is filled by
   `collectstatic` and served by the front server.
9. **Cache and database servers accept connections from the application servers only;** caches often have weak
   authentication. Persistent connections (`CONN_MAX_AGE`) are worth enabling when connecting is a significant
   share of request time; database-backed sessions need their old rows cleared regularly.
10. **Logging and error reporting are reviewed before launch** and checked once real traffic exists. Mailing
    errors to administrators does not scale; use an error-monitoring service. Replace the default 400, 403, 404
    and 500 templates with ones of your own.
11. **Templates escape by default; each exception is a decision.** Escaping covers HTML output and the risk is in
    the gaps: an unquoted attribute (`class={{ var }}`) can still run script, so quote attribute values in the
    template; `mark_safe`, the `safe` filter, `is_safe` on custom filters and tags, and turning autoescape off
    each assert that a value is safe and need a reason beside them; the built-in escaping is designed for HTML, so
    output in any other context needs the escaping that context requires. HTML stored in the database is sanitised on input and again on
    output unless it comes from a trusted source, and user input is not one.
12. **CSRF protection stays on.** Every non-safe request (anything but GET, HEAD, OPTIONS, TRACE) must carry the
    secret in a cookie and the matching token in the form field, plus an origin check against the host and
    `CSRF_TRUSTED_ORIGINS`; the secret changes on login. `csrf_exempt` is for a view with its own proof of the
    caller (a signed webhook), never for convenience, and says why beside it. Subdomains outside your control
    can set cookies for the whole domain and defeat the protection (and enable session fixation), so do not
    give them to untrusted parties. Do not strip the `Referer` header site-wide (`no-referrer`): the strict
    referer check on HTTPS then fails every unsafe request; use `rel="noreferrer"` on outbound links instead.
13. **Queries are parameterised; raw SQL is rare.** Querysets parameterise by construction. `raw()`, `cursor.execute`,
    `extra()` and `RawSQL` take their values through `params`, with placeholders unquoted and no string
    formatting (§2.6).
14. **Clickjacking protection stays on** (the X-Frame-Options middleware), with the header value or a per-view
    exemption for the sections that must be framed. Set a referrer policy and the cross-origin opener policy
    in the security middleware settings.
15. **User input is never trusted.** Validate with forms or serializers at the boundary; a framework that
    escapes output does not validate input.
