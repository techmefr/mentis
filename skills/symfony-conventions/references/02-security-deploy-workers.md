# § 2 — Security, deployment, workers

> Section 2 of `skills/symfony-conventions`. Read it when a firewall, a voter, a login form, a release step or a
> message consumer is touched. Ideas restated 2026-10-02 from the Symfony best-practices article and the
> security, deployment and messenger chapters (no wording reused: the source is share-alike).

1. **One firewall unless there are two really different authentication systems** (a form login for the site and
   a token for the API are the legitimate pair). More firewalls multiply the places a request can slip through.
2. **Use the automatic password hasher setting,** which picks the strongest algorithm the PHP installation
   supports, so a later algorithm change needs no code edit (`skills/auth-session-conventions` for policy).
3. **Access control rules are matched top to bottom; the first match wins.** Read the whole list when adding a
   rule and put narrow paths before broad ones.
4. **Move non-trivial authorization into voters,** not into long expressions inside an attribute. A voter is a
   class that can be unit-tested and reused by controllers, templates and services alike.
5. **Role hierarchy is applied by the authorization checker, not by reading the roles array yourself.** Code
   that tests `getRoles()` by hand bypasses the hierarchy and drifts from the configured rules.
6. **Protect the login form against CSRF** (enable it on the form login and render the token in the form),
   and **throttle login attempts** with the login-throttling setting.
7. **Disable CSRF protection only where the caller proves itself another way** (a signed webhook, a token in a
   header with no cookie), and say why beside the line.
8. **Deploy in a fixed order, scripted:** install dependencies without dev packages and with an optimised
   autoloader, set the production environment before any step that runs framework scripts, load environment
   values (real environment variables or a generated, optimised dotenv file; neither is better, pick what the
   host makes natural), run migrations, clear and warm the cache with debug off, then restart the workers.
   Staging, tests, a way to roll back and CI are advised in the deployment chapter, not optional extras.
9. **Never run with debug on, or with the development environment, in production.** The debug flag and the
   environment are set outside the code, per host.
10. **Message workers are supervised, bounded and restarted on deploy.** Run the consumer under a process manager
    (it exits by design and must come back); bound each worker by time and memory so a leak ends in a clean
    restart; restart all workers on every release so they load the new code (on an orchestrator, a rolling
    restart of the worker deployment). Give each message type that needs its own retry window or failure
    handling its own transport rather than mixing them. For the contract of a job (idempotency, retries,
    poison messages), `skills/background-jobs-conventions`.
