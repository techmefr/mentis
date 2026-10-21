# docker-destructive-guardrails-pitfalls §1 — The rule and the tiers

Docker's own guardrail skill splits container commands into two tiers because they do not all carry the
same risk. Everything else follows one flat rule.

## 1.1 The rule
1. **State exactly what will be deleted, stopped or lost, and get explicit confirmation before running the
   command.** This is the core rule of Docker's skill for every command in §2 except the one case in §1.2.
2. **Do not run a destructive command as a default troubleshooting or "just clean it up" reflex.** Disk space,
   stuck containers and stale caches almost always have a narrower, non-destructive fix (the same skill).
3. **List before you delete.** Built on the skill's examples (the prune pages of Docker's reference say what each command takes, which is why listing first matters): `docker ps -a`, `docker volume
   ls` and `docker system df` show what a command would touch, and the answer to the user names those
   resources, not the command.
4. **Order the options by risk when offering several**, as the skill's example dialogue does: stopped
   containers and dangling images first, then the wider forms, and the answer waits for the user's choice.

## 1.2 The low-friction case
Two commands, under four conditions that must **all** hold, need no blocking confirmation.
1. **The commands**: `docker rm <name>` on a container that is already stopped, and `docker rm -f <name>` on
   a container that the person or agent running the command created and started earlier in the same
   session purely for testing or debugging. The second case applies even if the container is still running,
   since that is the only reason `-f` would be needed.
2. **The conditions**: the container is already stopped, or was created by the runner this session for
   testing; there is no known unpersisted state at risk; the command targets one specific, identified
   container, not a sweep; and the runner is acting on an explicit user request in this session, not on its
   own initiative.
3. **What to do**: remove it, say what was done, and carry on. Every other case is §1.3.

## 1.3 Commands that always need confirmation
1. **`docker kill`** is always in this group. It has no stopped-container exception: it only applies to
   running containers and sends SIGKILL with no grace period.
2. **`docker container prune`** is in this group. It always sweeps every stopped container on the host,
   never just the one being cleaned up, so it can never meet the "one specific container" condition.
3. **`docker rm -f` in any case that does not meet every condition of §1.2**: a running container the runner
   did not create this session, or one it did but without an explicit request.
4. **Any unscoped sweep**, whatever the container state: `docker rm -f $(docker ps -aq)`, or "remove all
   containers" or "kill all containers".
5. **A container the runner did not create and has no context on**, and any action taken on its own
   initiative.
6. **Scope, not state, decides the group for a sweep**: a sweep of stopped containers is still a sweep.

## 1.4 `docker stop`
1. **`docker stop` removes nothing**: the container can be started again. It is outside the removal tiers.
2. **It still interrupts a running process**: SIGTERM, then SIGKILL after the timeout, which loses any
   unpersisted in-container state.
3. **On the runner's own test or debug container from this session**, stop it and say so, as in §1.2.
4. **On any other container**, say that it will stop running and that unsaved in-memory state will be lost,
   then get confirmation first.

## 1.5 Vague cleanup requests
1. **"Clean up", "clear the cache", "start fresh", "wipe everything", "nuke it", "reset" and "tear down" do
   not name a command.** Treat each as a request to choose the narrowest command that does the job, then
   confirm it.
2. **Offer the safe version first**: the resources of the project (`docker compose down`, without `-v`), one
   named container, dangling images only, or the build cache without `-a`.
3. **Volumes are the data.** A volume that is not attached to a container today is not necessarily unused;
   own reasoning from the skill's note that a named volume holding database state is deleted by
   `docker volume prune -a` as readily as a throwaway one.

## 1.6 Where this stops
1. **Compose's own commands** (`docker compose down -v`, `rm -v`, volumes of a Compose project) are in
   `docker-compose-file-pitfalls` §3.2. For a volume declared `external: true`, which Compose does not
   manage, the skill says the standalone guidance in §2 applies.
2. **Non-Docker deletions** (git, files, cloud resources) are out of scope.

## 1.7 Verify
Read the last few messages of a session that touched Docker: every removal of more than one container, any
image, network, builder, context or volume must be preceded by a message naming what would go. Re-list after
the command and compare.
