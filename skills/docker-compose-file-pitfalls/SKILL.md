---
name: docker-compose-file-pitfalls
description: "Use when a Docker Compose file (compose.yaml, an override or a production overlay) is written, reviewed or debugged: an app starting before its database is ready (depends_on without a health condition, healthchecks with native client tools, a sidecar check for shell-less images), pinned tags, named volumes versus bind mounts, a production overlay without source mounts, secrets and defaults in variables, redeploying one service, validating the file, mounting the Docker socket (and a filtering proxy), and down -v, rm -v and volume prune deleting data. This is Docker Compose, not Jetpack Compose."
---

# docker-compose-file-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Compose file as a deliverable. The three sections share one
premise: **Compose starts what you list and removes what you tell it to, and it will not warn you about an
app that is not ready, a secret that is committed, or a volume that is about to disappear**. Host port
collisions between several projects are in `docker-multi-project-dev-environment` and are not repeated;
Dockerfile internals are in `dockerfile-build-pitfalls`.

## When
- Writing or reviewing `compose.yaml`, `compose.override.yaml` or a production overlay.
- A service crashes on first start and works on the second, or a worker runs before its API is up.
- A Compose service needs the Docker socket (a reverse proxy, a watcher, a CI agent).
- Someone proposes `docker compose down -v` or a volume prune to "start fresh".

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Startup order and health: `depends_on` conditions, database healthchecks, the sidecar for shell-less images | a service starts before its dependency is ready | [`01-startup-and-health.md`](./references/01-startup-and-health.md) |
| 2 | The file: name, pinned tags, named volumes, overrides and the production overlay, variables and secrets, redeploy, validation | a Compose file is written, split by environment or deployed | [`02-files-volumes-secrets.md`](./references/02-files-volumes-secrets.md) |
| 3 | The Docker socket and filtering proxy; commands that delete data | a container needs the socket, or a cleanup or restart is proposed | [`03-socket-and-data-loss.md`](./references/03-socket-and-data-loss.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the stack was brought up from nothing and the dependent service
waited for the healthy state (§1), `docker compose config --quiet` passed and the repository held no password
value (§2), the production overlay was rendered and mounts no source directory (§2.2), and the volumes
of the project were listed before and after any restart (§3.3). A file that only parses is not verified.

## Guardrails
- Never rely on a bare `depends_on` for readiness (§1.1).
- Never commit a secret in `compose.yaml` or a tracked `.env` (§2.3).
- Never mount the Docker socket without need, and never publish a socket proxy's port (§3.1).
- Never run `down -v`, `rm -v` or a volume prune as a side effect of debugging or "cleaning up" (§3.2).
- Never print the resolved configuration to a shared log; validate quietly (§2.4).
- This block states Docker Compose behaviour as of the repositories and documentation read on the date in
  [`references/origin.md`](./references/origin.md); the file format and Compose versions move, so check an
  option against the Compose version in use. Nothing was run while writing it.

## Origin
Rewritten from Docker's agent skill for Compose patterns and the Docker documentation pages for using Compose
in production and for environment variables (Apache-2.0 repositories), and the README of the Tecnativa Docker
socket proxy (Apache-2.0), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
