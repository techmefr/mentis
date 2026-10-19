# laravel-conventions §12 — Production configuration

> Section 12 of `skills/laravel-conventions`. Read it when an environment file, a session, cache, queue or
> mail driver, the proxy and host configuration, a debugging tool or the deploy steps are touched. The
> framework-agnostic defence (what each header or cookie flag does, what leaks) is in
> `skills/security-hardening`; this section is the Laravel settings that put it in place, and the failure each
> one prevents. `skills/laravel-verification` runs these as a checklist. The other sections and the guardrails
> stay in `SKILL.md`.

1. **Debug mode is off, and the environment name is the real one.** With debug on, an error page shows the
   stack, the environment variables and the SQL; with the wrong environment name, every `app()->isProduction()`
   branch does the development thing. Both are asserted on the target environment after deploy, because they
   are set by a file outside the repository and nothing in the code fails when they are wrong.
2. **The application key is set, secret, and rotatable.** It signs sessions, cookies and signed URLs and
   encrypts everything encrypted; it never appears in the repository or in logs. Key rotation is planned for
   by keeping the previous key in the framework's previous-keys setting during the changeover, so a rotation
   does not log everyone out or make every encrypted column unreadable.
3. **The environment file is not served and not committed.** The web server's document root is the public
   directory and nothing above it; a `.env.example` lists every key with no value; the real file is created by
   the deploy from the secret store. A request for the environment file returning anything but 404 is an
   incident, and it is a one-line check in the deploy smoke test.
4. **TLS is enforced by the application as well as the edge.** The proxy terminates TLS, so the application
   trusts the forwarded-protocol header only from the proxies it names (the trusted-proxy setting lists
   addresses, it is not `*` unless the network guarantees only the proxy can reach the app). Without that the
   app thinks it is on HTTP and generates `http` URLs, redirect loops and insecure cookies. Force HTTPS URL
   generation in production, and send the strict-transport header from one place (the edge or a middleware,
   not both).
5. **Trusted hosts are declared.** An application that builds absolute URLs from the request's host header
   (password reset links, signed URLs) lets an attacker choose the host in the mail it sends. Restrict the
   accepted hosts to the application's own domains.
6. **The session cookie is `Secure`, `HttpOnly` and `SameSite` by configuration.** The three are settings in
   the session configuration, not defaults to trust; the lifetime is a decision (idle and absolute) and the
   driver is shared storage (database or cache) whenever more than one instance serves traffic, since the
   file driver ties a user to one server. The session id is regenerated at login and on privilege change,
   which the framework's authentication does and a hand-rolled login must do (`skills/auth-session-conventions`).
7. **Security headers have one owner.** Content type sniffing protection, frame ancestors, referrer policy,
   permissions policy and a content security policy are set either at the edge or in one middleware, with the
   policy tested against the real pages. Headers set in three places drift, and a policy that is "report
   only" forever is not a policy. The header list and values belong to `skills/security-hardening`.
8. **CORS allows named origins, methods and headers.** A wildcard origin combined with credentials is
   rejected by browsers and, when "fixed" by echoing the request origin, reflects the attack. The allowed
   origins come from configuration per environment, and the paths covered are the API's, not the whole app.
9. **Drivers are production drivers.** The queue is not `sync` (jobs would run inside the request and never
   retry), the cache is not `array` (nothing is cached across requests), the session is not `array`, and the
   mail driver in non-production environments writes to the log or a catcher so a staging deploy cannot email
   real customers. A driver chosen by environment variable is verified by name in the smoke test.
10. **Logging is bounded and carries no secrets.** The production channel writes to a destination that
    rotates (or to standard error for the platform to collect), at a level above debug; request bodies,
    tokens, passwords and personal data are not logged (`skills/observability-instrumentation`). A debug-level
    production log is both a cost and a data leak.
11. **Debugging tools are development-only, by installation and by gate.** Profilers, debug bars and the
    query inspector are dev dependencies, absent from `composer install --no-dev`, and where one must exist
    in production its dashboard sits behind an authorisation gate that names who may see it, which is
    reviewed like any permission. The default gate that allows "local" environments only is checked after the
    environment name in point 1 is verified.
12. **The runtime database user is not the migration user.** The application connects with the rights it
    needs to read and write rows; schema changes run under a separate credential during the deploy step. A
    SQL injection or a compromised container then cannot drop a table, and the privilege split is visible in
    the connection configuration.
13. **Strict model behaviour is on outside production.** Preventing lazy loading, preventing silently
    discarded attributes and preventing access to missing attributes turn a class of latent bugs into
    exceptions in tests and staging; in production they are logged, not thrown, so a missed case degrades
    instead of failing a request (§3, point 33).
14. **The deploy builds the caches and checks they build.** Configuration, route, event and view caches are
    generated on the target (§7, points 17 and 33), after dependencies are installed without development
    packages and with an optimised autoloader. A build that fails here has found a closure route, an
    `env()` call outside configuration or a missing view before traffic did; a deploy that skips the step
    runs slower and hides those.
15. **Queue workers and the scheduler are processes someone supervises.** Workers run under a supervisor
    that restarts them, are restarted by the deploy so they load the new code, and have a memory and time
    limit that recycles them. The scheduler has exactly one cron entry per environment, and a scheduled task
    that must not overlap, or must run on one server only, says so. A queue that is not consumed shows up as
    nothing at all; the smoke test enqueues a harmless job and sees it complete.
16. **Failed jobs are visible.** The failed-jobs table exists, an alert fires on its growth, and the
    retention is pruned, and each job's own `failed()` handler (§8, point 5) leaves a record a person can act
    on. A worker that fails silently produces the symptom "emails stopped last
    Tuesday".
17. **Storage and links are part of the deploy.** The public storage link exists on the target, the storage
    and cache directories are writable by the web user and nothing else, uploaded files live outside the
    public root unless they are meant to be public, and the disk driver for uploads is the shared one when the
    application runs on more than one instance.
18. **There is a health route, and it checks what the application depends on.** The framework's built-in
    liveness route answers whether the process is up; the readiness check the load balancer uses also reaches
    the database and the cache, and fails the instance when they are unreachable. A health route that always
    returns 200 keeps a broken instance in rotation.
19. **Maintenance mode has a bypass and an owner.** Taking the app down for a release uses the framework's
    maintenance mode with a secret that lets the deployer through, so the post-deploy checks run against the
    live instance before the public sees it.
20. **Rate limits are configured on the entry points, by name.** Login, password reset, registration,
    one-time-code verification and any endpoint that sends mail or SMS have a named limiter keyed by the
    identity being attacked (the account or the address) as well as by IP, with a response that tells the
    client when to retry. A global limit alone lets one client exhaust the budget of everyone behind the same
    address, and a per-IP limit alone lets a botnet try one password per address (§6).
