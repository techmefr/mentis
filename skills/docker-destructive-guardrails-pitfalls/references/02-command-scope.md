# docker-destructive-guardrails-pitfalls §2 — What each command removes

Facts in this section come from Docker's guardrail skill and its CLI reference. Where the help text of a
local Docker 29.4.1 (read on 2026-10-16, `--help` only) agrees, it is said; flags change between releases,
so read the help of the version you run.

## 2.1 The prune family
There is no top-level `docker prune`; each resource type has its own subcommand: `container`, `image`,
`network`, `volume`, `system` and `builder` prune. `docker builder prune` is an alias of
`docker buildx prune`, which its own usage line shows.
1. **`docker system prune`** removes stopped containers, unused networks, dangling images and build cache,
   without any flag. Container-local state that was not committed to an image or a volume goes with the
   stopped containers.
2. **`-a` widens the images** from dangling only to every image not referenced by any container, running or
   stopped, including tagged images that were pulled or built on purpose.
3. **`--volumes` adds unused anonymous volumes**, never named ones. A named volume, such as database data,
   needs its own `docker volume rm` and its own confirmation. Local help for `system prune --volumes` says
   "Prune anonymous volumes".
4. **`docker system prune -a --volumes` is the widest form.** Look at what `docker system df` reports before
   it, and get explicit confirmation.
5. **`docker container prune`** removes every stopped container on the host; no flag widens it to running
   ones.
6. **`docker image prune`** removes dangling images only; with `-a` it removes any image not used by an
   existing container. Removed images must be pulled or built again, which can be slow for large images or
   on a metered connection.
7. **`docker network prune`** removes every user-defined network that is not attached to a running container
   (the skill's wording; local help says "unused networks"). The skill adds that static IP assignments and
   custom subnets of stopped Compose projects are deleted with the network.
8. **`docker builder prune`** removes build cache not tied to an existing image. With `-a` it also removes
   internal helper and frontend images and cache shared with other build outputs, forcing a cold rebuild for
   everyone who uses that cache, local or CI or a shared backend.
9. **`docker volume prune`** removes unused anonymous volumes; with `-a` it removes unused named volumes
   too. Local help says "Remove all unused volumes, not just anonymous ones".
10. **Every prune takes `-f`, which only skips the confirmation prompt.** Own check, local help text: it
    reads "Do not prompt for confirmation". A script or a command with `-f` removes the last safety, so the
    confirmation has to come from the person beforehand.

## 2.2 Removing named things
1. **`docker rm <container>`** on a stopped container is a normal, low-risk, irreversible removal; the
   container was already stopped.
2. **`docker rm -f`** also works on a running container, sends SIGKILL with no graceful shutdown, and with
   `-v` also removes the anonymous volumes attached to it.
3. **`docker kill`** sends SIGKILL, or a signal given with `-s`, with no grace period.
4. **`docker stop`** sends SIGTERM (or the signal given) and waits `-t` seconds, 10 by default per the skill,
   before SIGKILL; prefer it over `kill` unless the container does not answer SIGTERM.
5. **`docker rmi` and `docker image rm` are one command.** `--no-prune` skips removing untagged parent
   layers. The effect of `-f` on an image with several tags or used by a stopped container is not spelled out
   by the help text ("Force removal of the image"; local help agrees); the skill calls the usual
   understanding "documented by convention", not confirmed. Remove without `-f` first.
6. **`docker network rm`** removes only the networks named; no sweep.
7. **`docker volume rm`** fails on a volume that is in use, says its help: "You cannot remove a volume that
   is in use by a container". Whether `-f` forces an in-use volume or only silences a missing one is not
   settled by the help text (local help: "Force the removal of one or more volumes"); the skill leaves
   it open. Run without `-f` first and, if it fails, stop or remove the container using it, with its own
   confirmation.
8. **`docker buildx rm`** removes a builder instance, not the build cache. `--all-inactive` widens it to every
   inactive builder. `--keep-daemon` and `--keep-state` reduce what is deleted, but the registration goes
   either way.
9. **`docker context rm`** deletes the local connection configuration (endpoint, TLS references) for a
   Docker host, not the remote resources; a context set up with a one-time token or a copied TLS bundle may
   be hard to recreate. To fix an endpoint, `docker context update` avoids deleting.

## 2.3 `-f` does not mean the same thing everywhere
1. **`docker network rm -f` only suppresses the error for a network that does not exist.** It does not
   override the protection of a network in use. Local help: "Do not error if the network does not exist".
2. **`docker context rm -f` genuinely forces removal of a context that is in use**, such as the active one.
   Local help: "Force the removal of a context in use".
3. **`docker rm -f`** kills and removes a running container; **`docker image rm -f`** and **`docker volume
   rm -f`** are in the open cases of §2.2.
4. **Do not infer from one `-f` to another.** Read the help of the command, and say which meaning applies when
   asking for confirmation.

## 2.4 The scoped alternative
```
docker system df
docker container prune
docker image prune
docker builder prune
docker image prune --filter "until=168h"
docker rm <name>
docker network rm <name>
docker context update <name>
```
1. **Inspect, then prune narrowly**: `docker system df` first, then the prune of one resource type without
   `-a` or `--volumes`. Add `-a` or `--volumes` only after the user confirmed the specific resources.
2. **Target one named container, network or builder** rather than sweeping, and list candidates with
   `docker ps -a` when several look stuck.
3. **`docker container prune` is in the sample for the stopped-container case only**; it still sweeps every
   stopped container on the host, so it needs the confirmation of §1.3.
4. **The age filter is a narrowing, not a permission**: `until=168h` limits to images older than seven days
   and still needs confirmation before widening to `-a`.

## 2.5 Verify
For each command, read `docker <command> --help` for the installed version and compare the flags with this
section; where they differ, trust the help and say so.
