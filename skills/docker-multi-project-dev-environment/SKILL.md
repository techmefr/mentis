---
name: docker-multi-project-dev-environment
description: Use when running more than one Laravel/Sail (or plain Docker Compose) stack on the same dev machine — a port collision, a container that answers on the wrong port, an `up` that fails or silently binds somewhere unexpected, or a zombie `docker-proxy` squatting a port a stopped stack should have released.
---

# docker-multi-project-dev-environment

Diagnoses and prevents the failures that show up once a second (or third) Laravel project's Docker
stack runs beside the first: port collisions, a leftover `docker-proxy` holding a port, and a
port-swap disguised as a database or test-suite bug. Not step-numbered in `WORKFLOW.md`: a standing
dev-environment diagnostic, not part of a feature's pipeline.

## When
- `docker compose up` (bare, via `sail up`, or a project's own wrapper) fails to bind a port, or
  starts cleanly but the app/API answers with the wrong content.
- A test suite or manual request against a known port (3306, 6379, 7700, 80, ...) hits data or
  behavior belonging to a *different* project.
- A stack was stopped (`down`, `stop`, closed terminal, killed container) and its port is still
  unavailable.
- Setting up a new project beside ones already running, so ports don't collide from the start.
- "It works with the other project's wrapper but not this one", or "works with plain `docker
  compose` but not the project's `up` wrapper".

## Steps

### 1. Diagnose: collision vs. genuine service failure
A bind failure and a wrong-service response are different symptoms with different causes. Check what
is actually listening; don't guess from the error text.

1. **A bind failure at `up` time** (`port is already allocated`, `address already in use`) means
   something on the host already holds the port. The easy case: Compose refuses to start, loudly.
2. **A silent successful bind to the wrong thing is the dangerous case.** `up` reports success, the
   port is reachable, but a *different* project's container answers: it was already bound before this
   stack tried to claim the port, or a host-level proxy routes the port elsewhere. Nothing in the
   compose output flags it; the only sign is behavior that doesn't match the project (wrong schema,
   dataset, app version).
3. **Find what actually holds the port.** On the host, `lsof -i :PORT` or `ss -ltnp | grep PORT` names
   the owning process (often `docker-proxy`, through which Docker routes a published port; see
   step 2).
4. **Find which Compose project owns the container behind it.** `docker ps --filter publish=PORT`
   lists the container; `docker inspect` on its ID shows the `com.docker.compose.project` label,
   naming the project directory Compose ran from. That traces a collision to a *specific other
   project*, not "something on 3306."
5. **A port-swap is the hardest to diagnose because it looks like an unrelated failure.** Two services
   end up with host-side ports crossed between projects (project A's database reachable at the port
   project B's test suite assumes is its own cache), so the suite reports a connection failure, a
   schema mismatch or wrong data, never "wrong port." Same lookup as steps 3-4: before touching the
   failing service's config or the test, confirm what really listens on the port it connects to. A
   suite failure right after starting a second project's stack, or one that clears when only one stack
   runs, is the signal to check ports before debugging the suite's logic.

### 2. Clean up a zombie `docker-proxy` safely
1. **Why a `docker-proxy` can survive a stack that looks stopped.** Docker publishes a container port
   through a per-mapping `docker-proxy` process (plus an iptables/nftables rule on Linux hosts); a
   mechanism, not a bug, whose lifecycle depends on the container being torn down properly. A
   container killed rather than stopped (crashed daemon, killed compose process, interrupted `down`)
   can leave its `docker-proxy` and rule behind though `docker ps` no longer lists it. *Note to
   verify locally*: whether this is general Docker Engine/Desktop behavior or has a WSL2-specific
   wrinkle (Docker Desktop's WSL2 integration, or a daemon inside a distro) is not confirmed here;
   check `docker system df` / the daemon's state after a reproduction on the machine in question.
2. **Confirm it's orphaned before killing anything.** `ps aux | grep docker-proxy`, then cross-reference
   each port against `docker ps`. A `docker-proxy` with no running container on that port is the
   orphan; one matching a container of another running project is a different stack legitimately
   using the port.
3. **Prefer restarting the Docker daemon/Docker Desktop over hand-killing** when several ports are
   affected or ownership is unclear: it releases every proxy and rule cleanly and costs a stack
   restart, not a debugging session. `kill -9` on the process alone leaves its iptables rule behind.
4. **When a full restart isn't acceptable** (other stacks must keep running), kill only the specific
   orphaned `docker-proxy` found in step 2, by PID, then re-check the port is free (`lsof -i :PORT`)
   before starting the stack that needs it. Never kill a `docker-proxy` whose container ownership
   wasn't confirmed, and never by port number alone if more than one process could match.
5. **After freeing the port, bring the stack up from a clean state** (`docker compose down` for the
   owning project, then `up`) rather than assuming the port is correctly wired: a stack that partially
   started while the port was contended can end up with a container on the wrong network alias.

### 3. A per-project port convention that scales to N stacks
1. **Sail (and bare Compose files built the same way) read every published port from an `.env`
   variable with a documented default**, not a hard-coded number: the file says
   `${FORWARD_DB_PORT:-3306}:3306`, so overriding the host port is a one-line `.env` change. Verified
   against Sail's own stub files: `APP_PORT` (app, default 80), `VITE_PORT` (default 5173),
   `FORWARD_DB_PORT` (MySQL/MariaDB/Postgres, default 3306 or 5432 depending on engine),
   `FORWARD_REDIS_PORT` (6379), `FORWARD_VALKEY_PORT` (6379), `FORWARD_MEILISEARCH_PORT` (7700),
   `FORWARD_MEMCACHED_PORT` (11211), `FORWARD_MONGODB_PORT` (27017), `FORWARD_TYPESENSE_PORT` (8108),
   `FORWARD_MAILPIT_PORT` (1025) and `FORWARD_MAILPIT_DASHBOARD_PORT` (8025), `FORWARD_RABBITMQ_PORT`
   (5672) and `FORWARD_RABBITMQ_DASHBOARD_PORT` (15672), `PUSHER_PORT` (6001) and
   `PUSHER_METRICS_PORT` (9601) for Soketi. Only the services a project installed appear in its
   compose file: check it for the exact `FORWARD_*_PORT` names in use.
2. **Give every project a fixed numeric offset and derive every port from it**, not free-looking
   numbers picked by hand per service. For example, project N gets offset `N * 100` (project 0's app
   on 8000, project 1's on 8100, ...), and within a project each service keeps a fixed sub-offset
   (`+0` app, `+06` MySQL's last two digits, `+79` Redis, ...). The exact scheme matters less than
   being a formula, not a list someone remembers.
3. **Keep a single registry of which project owns which offset**, committed in each project's
   `.env.example` (never the per-developer gitignored `.env`) with a comment naming the convention, or
   in a shared team document. It must be the one place a new project's author checks before picking an
   offset, so two projects don't converge on the same range.
4. **The registry has to cover every developer's machine, not just one.** A convention living in one
   developer's memory or one project's README reproduces the failure this skill exists to prevent
   once a second developer or third project appears.

### 4. `sail up` vs. a project's own wrapper vs. bare `docker compose up`
A wrapper's flags aren't guessable without its source, but the *category* of extra work it does is
predictable and worth checking before assuming two commands behave identically.

1. **Bare `docker compose up`** does exactly what the compose file says: builds/pulls images, creates
   the declared network and volumes, starts services in dependency order, nothing else. No migrations,
   no seeding, no waiting for a database to be ready beyond the file's own `depends_on`/healthcheck.
2. **`sail` is a thin CLI wrapper around the same compose file**: it resolves the file location,
   injects the user's UID/GID so container-created files aren't root-owned on the host, and forwards
   subcommands (`sail artisan`, `sail composer`, `sail test`, ...) via `docker compose exec`. `sail
   up` is functionally `docker compose up` on Sail's `compose.yaml`; the difference is convenience
   commands *around* the stack, not extra startup machinery inside `up`.
3. **A project's custom `up` wrapper typically adds one or more of these**, and "works with the
   wrapper but not the bare command" is almost always one of them silently not running:
   - **Config generation**: writing or templating a `.env`, per-service config or TLS certificates
     before the containers start, so a stack started without the wrapper lacks a file the containers
     assume exists.
   - **Health-gating**: blocking until a database, search engine or queue accepts connections (not just
     until its container reports "started") before migrations or the app server, which plain `up`
     doesn't do unless healthchecks are wired into `depends_on: condition: service_healthy`.
   - **First-run seeding/bootstrapping**: migrations, seeders or an initial import on first start, so a
     bare `up` on a fresh volume yields a running app on an empty, unmigrated database.
   - **Port/offset injection**: writing the §3 derived values into `.env` before starting, so skipping
     the wrapper falls back to the compose file's hard-coded defaults and collides with whatever else
     runs.
4. **Before debugging why one command fails when another works, diff what each actually runs**: read
   the wrapper script (or `sail`'s source, a plain PHP CLI Composer package) for the step-3
   categories. The compose file is usually identical; the gap is almost always in the setup a wrapper
   does before or after `up`.

## Output / checkpoint
A confirmed root cause (collision, orphaned proxy, port-swap, or a missing wrapper step) named with
the command output that showed it, not "restarted Docker and it worked," which fixes the symptom
without confirming the cause; and a stated port convention adopted for any project this diagnosis was
run against more than once.

## Guardrails
- Never kill a `docker-proxy` (or any Docker process) without confirming, via `docker ps` /
  `docker inspect`, which project's container it belongs to: killing on port number alone can take
  down an unrelated running stack.
- Never assume a bind failure and a wrong-service response share a cause: same commands diagnose them,
  but the problem (something already on the port vs. something routed to the wrong destination)
  differs.
- A "just restart Docker" fix not preceded by identifying the actual owner (§1.3-4) can paper over a
  port-swap that recurs once both projects run together again.
- Port variable names are Sail's own (`FORWARD_*_PORT`, `APP_PORT`, ...) as of the versions checked
  when this skill was written; a project on a much older or newer Sail should confirm against its own
  `compose.yaml`/`docker-compose.yml`.
- This skill assumes Docker Compose v2 (`docker compose`, not the standalone v1 `docker-compose`) and
  Sail's default service stubs; the legacy v1 binary or a heavily customized `compose.yaml` may differ
  in ways not covered here.

## Origin
No external source: no Docker/Sail multi-project environment skill exists in any catalogue this
repo mines from, and this is operational knowledge rather than a market or native block to adapt.
Assembled from documented Docker/Compose port-publishing and process-lifecycle mechanisms
(`docker-proxy`, `com.docker.compose.project` labels) and Laravel Sail's own published stub files
(`laravel/sail`, `stubs/*.stub`, branch `1.x`, read 2026-09-29) for the exact `FORWARD_*_PORT`
variable names — not mined from the org catalogue, which has no equivalent skill. The
WSL-specificity of the zombie-proxy behavior is explicitly left as an open verification note rather
than asserted either way.
