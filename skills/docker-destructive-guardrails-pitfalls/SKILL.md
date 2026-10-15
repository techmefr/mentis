---
name: docker-destructive-guardrails-pitfalls
description: "Use when a task could lead to running a Docker command that deletes or interrupts something, even if only a cleanup is asked for (clean up, start fresh, free disk space, wipe, reset, force remove, tear down): docker system prune and its -a and --volumes forms, container, image, network, builder and volume prune, rm and rm -f, kill and stop, rmi, network rm, buildx rm, context rm and standalone volume rm. States what each command removes, the one low-friction case (a stopped container or the tester's own test container), and the scoped alternative to reach for first."
---

# docker-destructive-guardrails-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for any session that runs Docker commands on a host that holds
more than the project at hand. The two sections share one premise: **a cleanup command is chosen for the
problem in front of you and deletes everything in its scope, with nothing to say which of it mattered**. The rule is the same for a person and for an agent: say exactly what will be lost, get an explicit
yes, and prefer the narrower command. The Compose-specific commands (`down -v`, `rm -v`, a project's volumes)
are in `docker-compose-file-pitfalls` §3.2 and are not repeated here.

## When
- Someone says "clean up", "free some disk", "start fresh", "reset Docker" or "force remove" without naming a
  command.
- A stuck container, a stale network, a broken build cache or a full disk makes a prune or a force remove
  tempting.
- A debugging step proposes `docker system prune`, `docker rm -f`, `docker kill` or a volume removal as a
  side effect.
- Reviewing a script or runbook that prunes Docker resources.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The rule, the one low-friction container case, commands that always need confirmation, `docker stop`, vague cleanup requests | before running or proposing any of these commands | [`01-policy-and-tiers.md`](./references/01-policy-and-tiers.md) |
| 2 | What each command removes, the flags that widen it, `-f` flags that differ, the scoped alternative | choosing between prune and remove, or explaining the impact | [`02-command-scope.md`](./references/02-command-scope.md) |

## Output / checkpoint
The rule was exercised, not read off the file: before any such command ran, the message to the user named the
resources that would be removed (listed with `docker ps -a`, `docker volume ls`, `docker system df` or the
filter the command would apply), the user answered, and only then was the command run. After it ran, the same
listing was read again and compared. A command run first and explained afterwards is not verified.

## Guardrails
- Never run a prune, a force remove or a kill as a default fix for an unrelated problem (§1.1).
- Never treat "clean up" or "start fresh" as a request for a prune (§1.5).
- Never run `docker container prune` to remove one container; it removes every stopped container on the host
  (§1.3).
- Never add `-a` or `--volumes` to a prune before the specific resources were named and confirmed (§2.1).
- Never assume two `-f` flags behave alike; read the command's help (§2.3).
- This block states Docker CLI behaviour as of the repository read on the date in
  [`references/origin.md`](./references/origin.md); flags and defaults change between releases, so check a
  command against `docker <command> --help` for the version in use. Only help text was run while writing it.

## Origin
Rewritten from Docker's agent skill for destructive-command guardrails (Apache-2.0: the skill, its CLI
reference, its cross-skill index and its verification runbook) and the Compose patterns skill for the
Compose boundary, read 2026-10-16, with the flags re-checked against help text of one Docker release. 🟡:
destructive commands never run by us; open points are in [`references/origin.md`](./references/origin.md).
