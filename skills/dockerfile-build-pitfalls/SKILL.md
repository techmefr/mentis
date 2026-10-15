---
name: dockerfile-build-pitfalls
description: "Use when a Dockerfile is written, reviewed or debugged for build traps that still produce a green build: apt update cached alone and stale installs, a failed stage hidden behind a pipe, a value that survives unset in an ENV layer, --pull versus --no-cache, COPY versus ADD versus a bind mount, base image tags and digests, credentials via ARG, ENV or copied dotfiles instead of build secrets and SSH mounts, .dockerignore limits, entrypoints in shell-less distroless images, users, setuid files, sudo and HEALTHCHECK."
---

# dockerfile-build-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Dockerfile itself, whatever the language. The three sections
share one premise: **an image build succeeds on a cached, half-failed or leaky step just as happily as on a
correct one, so each trap here is a place where "it built" proves nothing**. Node-specific image rules
(multi-stage, non-root user, PID 1 and signals, secret in ARG, heap size) are in `node-container-runtime`
§1 and are only referred to here; Go, Python and .NET have their own container blocks. Image scanning and
registry policy belong to `devops-conventions` and `security-hardening`.

## When
- Writing or reviewing a Dockerfile, or the `RUN`, `ENV`, `COPY`, `ADD`, `ENTRYPOINT` and `USER` lines of one.
- A rebuild installs an old package, a build passes though a download failed, or an image behaves
  differently after a rebuild with the same tag.
- A build needs a private registry, a private Git repository or any other credential.
- Moving a runtime stage to a distroless or other shell-less base.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Layers, cache and the shell: update plus install, pipes, ENV persistence, `--pull` and `--no-cache`, cache mounts | a build installs stale packages, hides a failure or leaks a value | [`01-layers-and-cache.md`](./references/01-layers-and-cache.md) |
| 2 | What goes in: COPY, ADD, bind mounts, tags and digests, `.dockerignore`, build secrets and SSH | a base image is chosen or bumped, a credential reaches the build, files are copied in | [`02-sources-and-secrets.md`](./references/02-sources-and-secrets.md) |
| 3 | The final stage: shell-less images, users, setuid, health | the runtime stage changes, a distroless base is adopted, a container runs as root | [`03-runtime-image.md`](./references/03-runtime-image.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the image was built twice with a changed install line and the
package index step reran (§1.1), a deliberately failing pipe stopped the build (§1.2), `docker history
--no-trunc` and the image filesystem were searched for the credential value and found none (§2.4), the final
image was started the way the orchestrator starts it and ran as the configured non-root user (§3). A
Dockerfile that was only linted is not verified.

## Guardrails
- Never put an `apt-get update` alone in its own `RUN` (§1.1).
- Never rely on `unset` in a later layer to remove an `ENV` value (§1.3).
- Never pass a credential through `ARG`, `ENV` or a copied dotfile; mount a secret for the one step (§2.4).
- Never disable SSH host-key checking to make a private clone work (§2.4).
- Never use `latest`, and never pin a digest that nothing keeps current (§2.2).
- Never write a shell-form `ENTRYPOINT` in a shell-less image, and never ship a `:debug` image (§3.1).
- This block states Docker behaviour as of the documentation and repositories read on the date in
  [`references/origin.md`](./references/origin.md); BuildKit moves, so check a flag against `docker build
  --help` on the version in use. Nothing was built or run while writing it.

## Origin
Rewritten from the Docker documentation (build best-practices page, Apache-2.0 repository), Docker's
agent skill for build strategies (Apache-2.0), the dockle image linter's checkpoint list (Apache-2.0) and
the distroless project README (Apache-2.0), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
