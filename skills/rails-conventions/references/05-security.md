# § 5 — Security surface

> Section 5 of `skills/rails-conventions`. Read it when authentication, a session, a form that changes state, a
> redirect, an upload, an outgoing HTML fragment, a response header or an admin interface is written or changed.
> The query and parameter rules that are security rules too stay where they are written (§1.6, §1.8, §2.16).
> Ideas from the Rails security guide (a CC BY-SA text: mechanisms only, wording ours) and from the Rails
> configuration guide, read 2026-10-02. This is a coding checklist, not a review of an application's threat
> model (`skills/security-hardening`).

1. **Issue a new session id at login.** An attacker who can plant a known session id in a victim's browser owns
   the session once the victim signs in; calling `reset_session` after authentication invalidates the old id.
   Anything the session held that must survive (a cart, a locale) is copied into the new one on purpose.
   A hand-rolled sign-in has to do this; a maintained authentication library usually already does.
2. **Know what the cookie session holds.** The default store keeps the session in the cookie itself: it has a
   size limit, it lives on the client, which may keep or copy it past its expiry, and it cannot be invalidated
   from the server by itself. Keep only identifiers in it, store anything of lasting value on the server, and
   give sessions an expiry; a session that never expires lengthens the window for every other attack here.
3. **Protect every non-GET request against forgery, and never change state on GET.** A forged cross-site POST
   is as easy as a forged image tag. The framework adds an authenticity token to non-GET requests; keep that
   protection on. Disable it only for an action that
   deliberately serves script meant to be loaded by a script tag, and say why next to the exemption. A
   state-changing link is a form with a button.
4. **Authorize the record, not the route.** `Project.find(params[:id])` lets a user read project 42 by editing
   the URL; scope the lookup by what the user may see (`current_user.projects.find(params[:id])`) so that an
   unauthorised id is a not-found. Every parameter is user input, however hidden the field; client-side
   validation is a convenience and never a control.
5. **Throttle sign-in and password reset, and say the same thing on failure.** Use the framework's rate limiter
   on the sessions controller, give one generic message for a wrong username or password, and the same for
   the forgot-password page, which is where most applications leak which addresses exist. A CAPTCHA after
   repeated failures from one address raises the cost further; none of these stops a distributed attack.
6. **Changing a password or an email address asks for the current password**, and the change forms are protected
   against forgery (point 3): with a stolen session cookie, a change-email form is a full account takeover
   through the reset flow.
7. **Prefer a permitted list to a restricted list, everywhere.** Strip nothing, reject the malformed:
   removing `<script>` from a string leaves what removing it re-creates. For filters, list the exemptions
   (§1.5); for HTML, name the allowed tags; for file names, the allowed characters.
8. **Uploads: names from an allowlist of characters, storage outside the web root, processing off the request.**
   A user-chosen file name can climb out of the upload directory; do not try to remove the dangerous parts, keep
   only what is known good (and replace the rest). A file stored under the directory the web server serves can
   be executed by it. Image and media processing done inside the request lets a handful of uploads stall the
   application; store the file and process it in a job.
9. **Never build a command from user input.** Pass arguments to `system`, `exec` and `spawn` as separate
   arguments, so the shell never parses them; the single-string form lets `hello; rm *` run both halves.
10. **Escaping is the default; each exception is a decision** (§1.11). Add a Content-Security-Policy through the
    framework's DSL: it limits what an injected script can do when an escape is missed. The framework already
    sends `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff` and
    `Referrer-Policy: strict-origin-when-cross-origin`; tighten rather than remove them.
11. **Force HTTPS in production** (`force_ssl`, which also sends HSTS), and set `assume_ssl` when a proxy
    terminates TLS so redirects and cookies behave as if the request were secure. Keep the `hosts` allowlist in
    production configured: it is what rejects a forged `Host` header (DNS rebinding).
12. **CORS lists origins.** When the API is consumed from another origin, configure the CORS middleware with the
    exact origins, the methods and headers in use, per environment, never a wildcard with credentials.
13. **Admin and internal interfaces are the better target and get more care, not less.** An XSS or a forgery
    there acts with the administrator's rights. Limit what an admin role can do, require a separate credential or
    a second factor for it, restrict by source network where that is practical (knowing a proxy changes the
    address you see), and consider serving it from its own subdomain with its own sessions so the public site's
    cookies cannot be read from it.
14. **Update vulnerable gems conservatively:** bump the one gem (`bundle update --conservative <gem>`) and run
    the suite, instead of a blanket update; the framework itself does not raise dependency versions just to
    encourage upgrades, so the application owner has to watch the advisories.
15. **Secrets and logs.** Credentials in the encrypted credentials file, the master key out of the repository
    (§4.4); every sensitive parameter in the log filter (§4.12); the database configuration and any unencrypted
    secret file restricted per environment.
