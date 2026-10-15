# docker-compose-file-pitfalls §1 — Startup order and health

A Compose file says which containers exist and which ones start first. It does not know when a service is
ready unless you tell it how to ask. Most "it worked on my machine" Compose failures are an application that
started before its database accepted connections.

## 1.1 `depends_on` orders starts, not readiness
1. **A bare `depends_on` only guarantees that the dependency's container was started.** It says nothing about
   the process inside having finished initialising (Docker's Compose patterns skill).
2. **Wait for health.** Use the long form with `condition: service_healthy`:

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:17.2
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 3
      start_period: 10s
```

3. **Every service named with a health condition needs a `healthcheck`.** Without one the condition has
   nothing to evaluate.
4. **Pin the image tag in the same breath** (§2.1): the example's tag stands for a version you choose.

## 1.2 Health checks for databases
1. **Give every database service a healthcheck** (Postgres, MySQL, Redis, MongoDB).
2. **Use the service's own client tool when it ships one**: `pg_isready`, `redis-cli ping`, `mysqladmin ping`.
   It needs no extra package and asks the thing you care about.
3. **Starting values from Docker's skill** are `interval: 5s`, `timeout: 3s`, `retries: 3`,
   `start_period: 10s`. They are a starting point: raise `start_period` for a service that really takes
   longer to initialise, so that early failures are not counted against it.

## 1.3 A shell-less image cannot check itself
Distroless, scratch-based and hardened images contain no shell, `curl` or `wget`. Docker's skill advises not
baking tools in (it defeats the purpose of the image) and running the check from a **sidecar** that shares
the application's network namespace:

```yaml
services:
  api:
    build:
      context: .
      target: runtime
    ports:
      - "8080:8080"

  api-health:
    image: curlimages/curl:8.22.0
    network_mode: "service:api"
    entrypoint: ["sleep", "infinity"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 45s
    deploy:
      resources:
        limits:
          memory: 32M

  worker:
    depends_on:
      api-health:
        condition: service_healthy
```

1. **The sidecar must stay alive** (`sleep infinity`) so that Compose can run its healthcheck inside it.
2. **`network_mode: "service:api"` makes `localhost` in the sidecar the application's loopback**; the check
   hits the real listener without any extra network.
3. **Dependents wait on the sidecar, not on `api`**, since `api` itself has no healthcheck to wait for.
4. **Cap the sidecar's memory.** The skill's example uses 32M for curl and calls that sufficient. Whether
   your Compose version enforces a `deploy` limit outside Swarm was not checked here; confirm with
   `docker stats`.
5. **Instruction-level health** for the image itself is in `dockerfile-build-pitfalls` §3.3.

## 1.4 Verify
Bring the stack up from nothing (`docker compose down`, then `up`) and watch `docker compose ps`: the
dependent service must stay in `created` until the dependency reports healthy. Break the database command
and confirm the dependent never starts.
