# nestjs-node-conventions §6 — Configuration, lifecycle, scopes and shutdown

> Section 6 of `skills/nestjs-node-conventions`. Read it when configuration is read, a provider needs set-up or
> tear-down, a provider's lifetime is chosen, or the process must start and stop cleanly. The other sections and
> the guardrails stay in `SKILL.md`. Pinned to NestJS 12 (documentation read 2026-10-02).

## Configuration
1. **Read configuration through an injected service, not `process.env`.** Import the configuration module once
   (global if most modules need it), and inject its service. Scattered `process.env` reads cannot be mocked,
   typed or validated, and are slower than the service's cached read (enable the cache option).
2. **Validate the environment at startup and stop on failure.** Give the configuration module a validation
   schema (or validate in the factory); use the throwing getter for values the app cannot run without, so a
   missing value stops the process at boot and not on the first request that needs it. The schema option
   covers environment variables only, **not** custom configuration files: validate those inside their
   factory.
3. **Group configuration in namespaces** (a registered factory per concern: database, mail, auth), inject the
   typed namespace where used, and convert a namespace to a provider definition to configure another module.
   One flat bag of keys read by string name invites typos.
4. **Environment files are not secrets stores.** The file is merged with the process environment; the file
   stays out of version control and the real secrets come from the platform. To read only
   validated and declared values, tell the service to ignore the raw `process.env`.

## Initialization
5. **Hooks, not constructors, for asynchronous set-up.** A constructor cannot await. `onModuleInit()` runs once
   the module's dependencies are resolved; `onApplicationBootstrap()` once every module is initialised and
   before the server listens. Both can return a promise, and Nest awaits it, so a connection opened there delays
   readiness until it is up. Hooks run module by module, deepest imports (and global modules) first, the root
   last; shutdown hooks run in the reverse order. Do not rely on a sibling module's hook having run.
6. **Hooks do not run for request-scoped classes**; their lifetime is not tied to the application's.

## Scopes
7. **Keep providers singletons.** In Nest almost everything is shared across requests (the connection pool,
   services with state), which is the intended model: instances are created once at startup and cached.
8. **A request-scoped provider makes every consumer request-scoped**, up the injection chain, up to and
   including the controller, and cannot be undone. It costs an instance per request (the framework states
   latency should not rise by more than about 5% in a well-designed application). Transient scope gives each
   consumer its own instance but does not bubble up.
9. **To read a per-request value (user, tenant, locale), use an async-local-storage store** rather than a
   request-scoped provider: every provider stays a singleton, and it also works in queue jobs and message
   handlers. Gateways, passport strategies and cron controllers must not be request-scoped.
10. **Per-test resolution of scoped providers** uses `resolve()`, not `get()`; two calls return two instances.

## Shutdown
11. **Enable shutdown hooks in the entry point** (`enableShutdownHooks()`), or the destroy and shutdown hooks
    do not run on `SIGTERM`; they always run on an explicit `app.close()`. The sequence is `onModuleDestroy()`
    for every module, then `beforeApplicationShutdown()`, then connections close, then `onApplicationShutdown()`;
    each awaits a returned promise. Put "stop accepting work and drain" in the first, "close resources" in the
    last.
12. **Release what you open in the destroy hooks**: database pools, queue consumers, timers, subscriptions. A
    leaked handle is why a process does not exit.
13. **A process that will not exit** usually has an open handle or a long-lived keep-alive connection. The
    HTTP adapter waits for in-flight responses; the force-close-connections option (Express adapter; Fastify
    has its own server option) ends the wait, mostly useful in watch mode. Reach for it after checking for
    unreleased handles, not instead.
14. **Shutdown hooks add listeners.** With several application instances in one test process, Node warns about
    too many listeners; enable them in the real entry point, not in tests.
15. **Windows does not deliver `SIGTERM`**; only `SIGINT` (and to a degree `SIGBREAK`, `SIGHUP`). Test shutdown
    on the target platform.

## Standalone applications
16. **Scripts and jobs reuse the container without a server**: create a standalone application context, take
    the provider by type, run, then close it (which runs the destroy hooks). Do not instantiate services by
    hand in a script.

## Mechanical checks

```
grep -rnE "process\.env\." src --include=*.ts
grep -rnE "enableShutdownHooks|app\.close\(" src
grep -rnE "Scope\.(REQUEST|TRANSIENT)|scope: *Scope" src
grep -rnE "onModuleInit|onApplicationBootstrap|onModuleDestroy|onApplicationShutdown" src
grep -rnE "setInterval|setTimeout|createServer|new Pool|connect\(" src
grep -rnE "validationSchema|validate:|getOrThrow" src
```

- `process.env` outside the configuration factory and the entry point is a finding (rule 1).
- A `setInterval`, a pool or a subscription with no matching destroy hook is a leak (rule 12).
- A request-scoped provider is listed with its reason and checked against rule 9.
