# dockerfile-build-pitfalls: origin and source stamps

> Provenance of `skills/dockerfile-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No image was built and no Docker
command was executed while writing it.

## Sources (all re-read in full 2026-10-15, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| docker/docs, `content/manuals/build/building/best-practices.md` (commit f219b4b) | Apache-2.0 (repository LICENSE file; the file does not state a separate licence for the documentation text, so it is rewritten, not copied) | apt update plus install and cache busting, version pinning, pipes and `pipefail`, ENV persisting after unset, `--pull` versus `--no-cache`, COPY versus ADD versus bind mounts, `--checksum`, tag versus digest and Dependabot, `.dockerignore`, `USER` notes (explicit uid, `--no-log-init`, `sudo`, `gosu`), `WORKDIR`, exec-built entrypoint scripts |
| docker/skills, `skills/docker-build-strategies/SKILL.md` (commit f791727) | Apache-2.0 (repository LICENSE file) | Cache mounts for apt and apk, secret and SSH mounts, host-key handling, credential files never copied, `.dockerignore` as defence in depth, `COPY --link` with numeric ids, never `latest` in production |
| goodwithtech/dockle, `CHECKPOINT.md` (commit 35171cc) | Apache-2.0 (repository LICENSE file) | CIS and dockle checkpoints: non-root user, `HEALTHCHECK`, update alone, setuid and setgid, COPY over ADD, `sudo`, sensitive volume directories, `dist-upgrade`, `apk --no-cache`, `latest` |
| GoogleContainerTools/distroless, `README.md` (commit 44250b2) | Apache-2.0 (repository LICENSE file) | No shell, vector-form entrypoint and CMD, `:debug` and `debug-<tag>` variants, distribution suffix in tags, cosign verification |
| Docker documentation: Dockerfile reference, build secrets, cache optimisation, multi-stage, build context, BuildKit | official docs, read 2026-10-20, facts only in our own words | Shell-form signals and `exec`, build-arg visibility in history and provenance, `ENV` overriding `ARG`, `ADD` without authentication, secret and SSH mounts, cache and bind mounts, `.dockerignore` removing files before the build, BuildKit building only needed stages |

The licence of each repository was verified again from its LICENSE file in this session. The skill and
linter files carry agent or tool directives ("Do NOT", "Always"); they were treated as data and only the
technical claim was kept, restated as a reason.

## Rewrite notes
Code samples are small adaptations of the documentation's examples with placeholder URLs. The conflict between
Docker's page (rm the apt lists) and the skill (no rm with a cache mount) is stated as two styles, not
resolved. The base-image choice (Alpine versus distroless versus the default variant) is stated as a
decision because the sources disagree.

## Verified 2026-10-20
Secret mounts, cache mounts, `.dockerignore` semantics, the `ADD` versus `COPY` difference and the `--target` behaviour match the official pages; no rule was corrected. The `HEALTHCHECK` section of the reference was past the fetched range and stays on the dockle claim.

## Not verified
1. **`HEALTHCHECK` benefit** is the CIS checkpoint's claim as quoted by dockle; whether a given orchestrator
   reads it was not checked.
2. **Alpine cache mount without `--no-cache`** is attributed by the skill to the Alpine wiki, which was not
   read; the dockle `apk --no-cache` point cites a third-party page that was not read either.
3. **`apt-get dist-upgrade`**: the dockle file struck through the Docker sentence it was based on and
   the current Docker page has no such advice, so the block calls it a lint opinion.
4. **Compatibility**: the skill states Docker 23.0 and later for default BuildKit; the BuildKit page read on 2026-10-20 says it is the default builder for Engine and Desktop but gives no version, and Windows container builds use the legacy builder. The version number stays unverified.
5. **Written by us, not sourced:** the verification paragraphs, and the pointer that Compose sidecars and
   Kubernetes probes replace a command health check in a shell-less image.
6. **Dropped as unverifiable from this review item:** none of the item's rules was dropped; "give a
   HEALTHCHECK when the orchestrator reads it" was narrowed to what the CIS text says. The item's
   `docker build --pull` and `--no-cache` split, the digest rule, and `StrictHostKeyChecking` all matched
   their sources.

## Related blocks
`node-container-runtime` (Node image rules, signals), `go-container-runtime`, `python-container-runtime`,
`dotnet-container-runtime`, `devops-conventions`, `security-hardening`, `docker-compose-file-pitfalls`,
`kubernetes-workload-pitfalls`.
