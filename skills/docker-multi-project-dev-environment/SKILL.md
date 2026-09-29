---
name: docker-multi-project-dev-environment
description: Use when running more than one Laravel/Sail (or plain Docker Compose) stack on the same dev machine — a port collision, a container that answers on the wrong port, an `up` that fails or silently binds somewhere unexpected, or a zombie `docker-proxy` squatting a port a stopped stack should have released.
---

# docker-multi-project-dev-environment

Diagnoses and prevents the failure modes that show up once a second (or third) Laravel project's
Docker stack runs alongside the first on one machine: port collisions, a leftover `docker-proxy`
still holding a port, and a port-swap that disguises itself as a database or test-suite bug. Not
step-numbered in `WORKFLOW.md` — this is a standing dev-environment diagnostic, reached for
whenever a stack's ports misbehave, not part of a feature's pipeline.

## When
- `docker compose up` (bare, via `sail up`, or via a project's own wrapper script) fails to bind a
  port, or starts without error but the app/API answers with the wrong content.
- A test suite or a manual request against a known port (3306, 6379, 7700, 80, …) hits data or
  behavior that belongs to a *different* project.
- A stack was stopped (`down`, `stop`, closing the terminal, killing the container) and the port it
  used is still unavailable.
- Setting up a new project alongside ones that already run locally, and ports need to not collide
  from the start.
- Debugging "it works with the other project's wrapper but not this one" or "works with plain
  `docker compose` but not the project's `up` wrapper".

## Steps

### 1. Diagnose: collision vs. genuine service failure
A bind failure and a wrong-service response are different symptoms with different causes — don't
guess from the error text alone, check what is actually listening.

1. **A bind failure at `up` time** (`port is already allocated`, `address already in use`) means
   something already holds that port on the host. This is the easy case: Compose refuses to start,
   so the failure is loud and immediate.
2. **A silent successful bind to the wrong thing is the dangerous case.** `up` reports success,
   the port is reachable, but a *different* project's container is the one answering — because
   that container was already bound to the port before this stack tried to claim it, or because a
   host-level proxy is routing the port somewhere other than the compose file's own service.
   Nothing in the compose output flags this; the only sign is behavior that doesn't match the
   project being worked on (wrong schema, wrong dataset, wrong app version).
3. **Find out what actually holds the port, don't assume from the error message.** On the host:
   `lsof -i :PORT` or `ss -ltnp | grep PORT` names the owning process (often `docker-proxy` — see
   step 2 for why that process exists at all, not the container directly, since Docker routes a
   published port through it).
4. **Find out which Compose project owns the container behind that port.** `docker ps
   --filter publish=PORT` lists the container publishing it; `docker inspect` on that container's
   ID shows the `com.docker.compose.project` label, which names the project directory Compose was
   run from — this is how a port collision gets traced back to a *specific other project*, rather
   than staying "something on 3306."
5. **A port-swap is the hardest of the three to diagnose precisely because it looks like an
   unrelated failure.** Two services end up with their host-side ports crossed between projects —
   project A's database port is actually reachable at the port project B's test suite assumes
   belongs to its own cache, for instance — so the test suite reports a connection failure, a
   schema mismatch, or wrong data, never "wrong port." The fix is the same lookup as steps 3–4:
   before touching the failing service's config or the test itself, confirm what is really
   listening on the port that service connects to. A test suite failure that follows immediately
   after starting a second project's stack, or that clears up when only one stack is running, is
   the signal to check ports before debugging the suite's own logic.

### 2. Clean up a zombie `docker-proxy` safely
1. **Why a `docker-proxy` process can survive a stack that looks stopped.** Docker publishes a
   container port on the host via a per-mapping `docker-proxy` process (plus the corresponding
   iptables/nftables rule on Linux hosts); it's a mechanism, not a bug, but its lifecycle is tied to
   the container being properly torn down. A container killed rather than stopped (a crashed
   Docker daemon, a killed compose process, an interrupted `down`) can leave its `docker-proxy`
   and iptables rule behind even though `docker ps` no longer lists the container. *Note to
   verify locally*: whether this is a general Docker Engine/Desktop behavior or shows a
   WSL2-specific wrinkle (Docker Desktop's WSL2 integration, or a Docker daemon running inside a
   distro) is not confirmed here — check `docker system df` / the daemon's own state after a
   reproduction on the machine in question rather than assuming either way.
2. **Confirm it's actually orphaned before killing anything.** List `docker-proxy` processes
   (`ps aux | grep docker-proxy`) and cross-reference each port against `docker ps` — a
   `docker-proxy` with no matching running container for that port is the orphan; one that matches
   a container that's simply part of another, currently-running project is not a zombie, it's a
   different stack legitimately using that port.
3. **Prefer restarting the Docker daemon/Docker Desktop over hand-killing processes** when
   several ports are affected or the ownership is unclear — it releases every proxy and rule
   cleanly and costs a stack restart, not a debugging session. A full restart is the safe default
   precisely because a manually-killed `docker-proxy` can leave its iptables rule behind, which
   `kill -9` on the process alone does not clean up.
4. **When a full restart isn't acceptable** (other stacks must keep running), kill only the
   specific orphaned `docker-proxy` process found in step 2 by PID, then re-check the port is free
   (`lsof -i :PORT` again) before starting the stack that needs it — never kill a `docker-proxy`
   whose container ownership wasn't confirmed, and never kill by port number alone if more than one
   process could match.
5. **After freeing the port, bring the stack up again from a clean state** (`docker compose down`
   for the project that owns it, then `up`) rather than assuming the freed port is now correctly
   wired — a stack that partially started while the port was contended can be left with a
   container attached to the wrong network alias.

### 3. A per-project port convention that scales to N stacks
1. **Sail (and bare Compose files built the same way) read every published port from an `.env`
   variable with a documented default**, not a hard-coded number in `docker-compose.yml` — the
   file itself says `${FORWARD_DB_PORT:-3306}:3306`, so overriding the host port is a one-line
   `.env` change, no compose file edit. Verified against Sail's own stub files: `APP_PORT` (app,
   default 80), `VITE_PORT` (default 5173), `FORWARD_DB_PORT` (MySQL/MariaDB/Postgres, default
   3306 or 5432 depending on engine), `FORWARD_REDIS_PORT` (6379), `FORWARD_VALKEY_PORT` (6379),
   `FORWARD_MEILISEARCH_PORT` (7700), `FORWARD_MEMCACHED_PORT` (11211), `FORWARD_MONGODB_PORT`
   (27017), `FORWARD_TYPESENSE_PORT` (8108), `FORWARD_MAILPIT_PORT` (1025) and
   `FORWARD_MAILPIT_DASHBOARD_PORT` (8025), `FORWARD_RABBITMQ_PORT` (5672) and
   `FORWARD_RABBITMQ_DASHBOARD_PORT` (15672), `PUSHER_PORT` (6001) and `PUSHER_METRICS_PORT`
   (9601) for Soketi. Only the services a given project actually installed appear in its own
   compose file — check that file for the exact `FORWARD_*_PORT` names in use rather than
   assuming every project has every variable.
2. **Give every project a fixed numeric offset and derive every port from it**, instead of picking
   free-looking numbers per service per project by hand. For example: project N gets offset
   `N * 100`, so project 0's app is on 8000, project 1's on 8100, project 2's on 8200, and within a
   project each service keeps a fixed sub-offset (`+0` app, `+06` MySQL's last two digits, `+79`
   Redis, and so on) — the exact scheme matters less than that it is a formula, not a list of
   numbers someone remembers.
3. **Keep a single registry of which project owns which offset**, committed to each project's own
   `.env.example` (never the real `.env`, which is per-developer and gitignored) with a comment
   naming the convention, or in a shared team document — whichever exists, it must be the one
   place a new project's author checks before picking an offset, so two projects don't converge on
   the same range independently.
4. **The registry has to cover every developer's machine, not just one.** A convention that lives
   only in one developer's memory or one project's README reproduces the exact failure this skill
   exists to prevent, once a second developer or a third project appears.

### 4. `sail up` vs. a project's own wrapper vs. bare `docker compose up`
Framed generically — a specific wrapper script's flags aren't guessable without its source, but the
*category* of extra work it does is predictable and worth checking before assuming two commands
should behave identically.

1. **Bare `docker compose up`** does exactly what the compose file says: builds/pulls images,
   creates the declared network and volumes, starts the declared services in dependency order, and
   nothing else. It has no opinion about the application inside the containers — no migrations, no
   seeding, no waiting for a database to be ready before the app container tries to use it, beyond
   whatever `depends_on`/healthcheck the compose file itself declares.
2. **`sail` adds a thin CLI wrapper around the same compose file**: it resolves the compose file
   location, injects the user's UID/GID so files created in the container aren't root-owned on the
   host, and forwards subcommands (`sail artisan`, `sail composer`, `sail test`, …) into the
   running container via `docker compose exec`. `sail up` is functionally `docker compose up` on
   Sail's own `compose.yaml` — the difference is convenience commands *around* the stack (running
   Artisan/Composer/npm/tests inside a container without a manual `exec`), not extra startup
   machinery inside `up` itself.
3. **A project's own custom `up` wrapper typically adds one or more of these on top of either of
   the above**, and "works with the wrapper but not with the bare command" is almost always one of
   these silently not running when the bare command is used instead:
   - **Config generation** — writing or templating a `.env`, a per-service config file, or TLS
     certificates before the containers start, so a stack started without the wrapper is missing a
     file the containers assume exists.
   - **Health-gating** — blocking until a database, search engine, or queue actually accepts
     connections (not just until its container reports "started") before running migrations or
     starting the app server, which plain `docker compose up` does not do unless the compose file's
     own healthchecks are wired into `depends_on: condition: service_healthy`.
   - **First-run seeding/bootstrapping** — running migrations, seeders, or an initial data import
     the first time a stack comes up, so a bare `docker compose up` on a fresh volume produces a
     running app pointed at an empty, unmigrated database.
   - **Port/offset injection** — writing the per-project port convention's derived values (§3) into
     `.env` before starting, so skipping the wrapper and running bare Compose falls back to the
     compose file's own hard-coded defaults and collides with whatever else is running.
4. **Before debugging why one command "doesn't work" when another does, diff what each one
   actually runs** — read the wrapper script (or `sail`'s own source, since it is a plain PHP CLI
   Composer package) for the categories in step 3, rather than assuming the compose file itself is
   the difference. The compose file is usually identical between the two; the gap is almost always
   in the setup a wrapper does before or after `up`.

## Output / checkpoint
A confirmed root cause (collision, orphaned proxy, port-swap, or a missing wrapper step) named with
the command output that showed it — not "restarted Docker and it worked," which fixes the symptom
without confirming the cause, and a stated port convention adopted for any project this diagnosis
was run against more than once.

## Guardrails
- Never kill a `docker-proxy` (or any Docker process) without confirming, via `docker ps` /
  `docker inspect`, which project's container it belongs to — killing on port number alone can take
  down an unrelated running stack.
- Never assume a bind failure and a wrong-service response share a cause; they're diagnosed with
  the same commands but the underlying problem (something already on the port, vs. something
  routed to the wrong destination) differs.
- A "just restart Docker" fix that isn't preceded by identifying the actual owner (§1.3-4) risks
  papering over a port-swap that will recur identically once both projects run together again.
- Port variable names are Sail's own (`FORWARD_*_PORT`, `APP_PORT`, …) as of the versions checked
  when this skill was written; a project on a much older or newer Sail release should confirm
  against its own `compose.yaml`/`docker-compose.yml` before relying on a name listed here.
- This skill assumes Docker Compose v2 (`docker compose`, not the standalone `docker-compose`
  v1 binary) and Sail's default service stubs; a project on the legacy v1 binary or a heavily
  customized `compose.yaml` may differ in ways not covered here.

## Origin
No external source: no Docker/Sail multi-project environment skill exists in any catalogue this
repo mines from, and this is operational knowledge rather than a market or native block to adapt.
Assembled from documented Docker/Compose port-publishing and process-lifecycle mechanisms
(`docker-proxy`, `com.docker.compose.project` labels) and Laravel Sail's own published stub files
(`laravel/sail`, `stubs/*.stub`, branch `1.x`, read 2026-09-29) for the exact `FORWARD_*_PORT`
variable names — not mined from the org catalogue, which has no equivalent skill. The
WSL-specificity of the zombie-proxy behavior is explicitly left as an open verification note rather
than asserted either way.
