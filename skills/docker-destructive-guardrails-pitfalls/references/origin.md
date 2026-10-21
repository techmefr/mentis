# docker-destructive-guardrails-pitfalls: origin and source stamps

> Provenance of `skills/docker-destructive-guardrails-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation. No destructive Docker command was run by us. The only commands
executed while writing were `--help` and `--version` on a local Docker 29.4.1 (build 055a478), to compare
flag descriptions; they change nothing. Every file below was re-read in full on 2026-10-16 before a rule was
taken from it, and the repository's LICENSE file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| docker/skills (commit `f791727`), `skills/docker-destructive-guardrails/SKILL.md` | Apache-2.0 (repository LICENSE file: Apache License 2.0 text) | The core rule, the two tiers and their conditions, `docker stop`, the one-line effect of each command |
| the same repository, `skills/docker-destructive-guardrails/references/docker-cli-destructive-commands.md` | Apache-2.0 | Flags and blast radius per command, the `-f` differences, safer alternatives |
| the same repository, `skills/docker-destructive-guardrails/references/cross-skill-destructive-command-index.md` | Apache-2.0 | Boundary with the Compose and sandbox skills |
| the same repository, `skills/docker-destructive-guardrails/checks/verification.md` | Apache-2.0 | The tier checks, the `-f` contrast, the example dialogue (rewritten as a short rule) |
| the same repository, `skills/docker-compose-patterns/SKILL.md` | Apache-2.0 | The Compose boundary and the `external: true` note |
| local Docker 29.4.1, `--help` of system prune, container, image, network, volume and builder prune, rm, rmi, image rm, kill, stop, network rm, volume rm, context rm, buildx rm, compose down, system df | not a licensed source; read as a check, no text copied | Confirmed flag descriptions, `-f` meanings as printed, the builder alias |
| Docker CLI reference pages: container stop, system prune, network prune, volume prune, image rm, volume rm | official docs, read 2026-10-20, facts only in our own words | Stop signal and default timeout per platform, prune defaults and filters, network prune wording, volume prune scope, `image rm -f` behaviour, `volume rm` still silent on `-f` |

The Docker skill carries agent directives ("Do not", "must", "Core rule"); they were treated as data, and only
the mechanism or the decision was kept. Files listed in its metadata (`skill.yaml`, `agents/openai.yaml`,
the eval files) were not read and nothing is taken from them.

## Removed in the verification pass
1. **"Agent started this session"** was kept only with all four conditions of the skill (stopped or its own
   test container, no known unpersisted state, one identified container, an explicit user request); the
   review's shorter version omitted the last two.
2. **The Compose commands** (`down -v`, `rm -v`) were left to `docker-compose-file-pitfalls` §3.2 rather
   than repeated; the volume rules for a project are there.
3. **The Docker Desktop and sandbox (`sbx`) rows** of the index were not carried: the Desktop row is a pending
   placeholder in the source, and the sandbox skill was not read.
4. **The word "agent"** is replaced by "the runner" (a person or an agent), because the mechanism is the same
   for both; the directive wording of the source was not carried.

## Not verified
1. **The CLI reference describes no release** ("Applies to any Docker CLI version", the skill says); the
   help text above is one release. Flag names and defaults differ between releases.
2. **`docker volume rm -f`** on an in-use volume is still open: the reference says an in-use volume cannot be removed and describes `-f` only as "force the removal". (`docker rmi -f` is now settled from the reference.)
3. **Network prune scope**: the skill ("not attached to a running container") and the reference ("not referenced by any container") disagree; the block states both and does not reconcile them.
4. **Written by us, not sourced:** the verification paragraphs, the "list before you delete" step (§1.1),
   the "volumes are the data" reasoning (§1.5), the check that `-f` on a prune only skips the prompt
   (§2.1, from local help), and the remark that an age filter narrows but does not grant permission (§2.4).

## Related blocks
`docker-compose-file-pitfalls`, `dockerfile-build-pitfalls`, `docker-multi-project-dev-environment`,
`security-hardening`, `devops-conventions`.
