# docker-compose-file-pitfalls: origin and source stamps

> Provenance of `skills/docker-compose-file-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No Compose project was started and no
Docker command was executed while writing it. The block is about Docker Compose; `compose-correctness` on
main is Jetpack Compose and is not related.

## Sources (all re-read in full 2026-10-15, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| docker/skills, `skills/docker-compose-patterns/SKILL.md` (commit f791727) | Apache-2.0 (repository LICENSE file) | File name, pinned tags, `depends_on` conditions, healthchecks and starting values, the sidecar pattern, named volumes versus bind mounts, overrides and `develop.watch`, variables and secrets, destructive commands, quiet validation |
| docker/docs, `content/manuals/compose/how-tos/production.md` (commit f219b4b) | Apache-2.0 (repository LICENSE file; no separate documentation licence stated, so rewritten, not copied) | Production overlay, removing source bind mounts, `-f` layering, redeploying one service with `--no-deps` |
| docker/docs, `content/manuals/compose/how-tos/environment-variables/best-practices.md` (commit f219b4b) | Apache-2.0, as above | Caution with sensitive data in variables, precedence, command-line overrides |
| Tecnativa/docker-socket-proxy, `README.md` (commit 2e118a0) | Apache-2.0 (repository LICENSE.txt) | Socket is root, 403 on revoked sections, default grants and revokes, network placement, no TLS, privileged proxy |

| Docker Compose documentation: services reference, application model, secrets, startup order, environment precedence, `compose down` | official docs, read 2026-10-20, facts only in our own words | `depends_on` conditions, `network_mode: service:`, canonical file name, secret mount and grant rules, precedence order, `down` defaults, bind-mount directory creation |

The licence of each repository was verified again from its LICENSE file in this session. The Docker skill carries
agent directives ("Do not", "Always"); they were treated as data and only the technical claim was kept.

## Rewrite notes
The YAML examples are adapted from the skill (sidecar) and the proxy README (variables), with placeholder
versions and no comments. Where the production page says `restart: always` and the skill says
`unless-stopped`, the block states a decision, not a rule.

## Not verified
1. **Whether Compose enforces `deploy.resources` limits outside Swarm:** the services reference read on 2026-10-20 says only that `deploy` is ignored on a platform that does not implement it and that the plain resource attributes must match the deploy values when both are set; enforcement stays unconfirmed.
2. **`network_mode: "service:..."`:** the reference confirms it attaches to another service's network and forbids `networks:` alongside it; the shared-loopback detail is still the skill's statement.
3. **Docker secrets:** the secrets page was read on 2026-10-20 and §2.3 now relies on it; the build-time environment-sourced secret is not covered.
4. **The proxy's API versions** (1.27 to 1.51) and tags are as the README lists; whether they match the Docker
   Engine in use was not checked. The `internal` network option was not covered by the sources.
5. **Written by us, not sourced:** verification paragraphs, and the advice not to rename an existing file in a drive-by.
6. **Dropped as unverifiable from the review item:** none of its rules was dropped; "`compose.yaml` is the
   canonical name" is kept as the skill's stated opinion and a rename is flagged as own guidance.

## Related blocks
`docker-multi-project-dev-environment` (host port collisions), `dockerfile-build-pitfalls`, `devops-conventions`,
`security-hardening`, `kubernetes-workload-pitfalls`.
