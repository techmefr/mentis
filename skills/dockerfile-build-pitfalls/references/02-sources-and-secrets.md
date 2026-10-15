# dockerfile-build-pitfalls §2 — What goes in: files, base images, secrets

Three things enter an image from outside: the files you copy, the base you start from and the credentials
the build needs. Each has a cheap way to go wrong that still builds green.

## 2.1 COPY, ADD and bind mounts
1. **Use `COPY` by default.** `COPY` takes files from the build context or from another stage. `ADD` also
   fetches HTTPS and Git URLs and unpacks tar archives from the context; the lint checklist of the dockle
   image linter (CIS item DI-0009) names that as the risk: unscanned remote content and unpacking
   surprises.
2. **Use `ADD` only to download a remote artifact, and pin it** with `--checksum=sha256:...`. Docker's
   documentation prefers it to `wget` plus `tar` because the cache key is precise and the checksum is
   checked.
3. **A file needed by one `RUN` only is a bind mount, not a `COPY`.** The mount exists for that instruction
   and is not stored in any layer:

```dockerfile
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install --requirement /tmp/requirements.txt
```

4. **Do this only for steps that read the file.** If the step has to write it back into the image, `COPY` it
   (Docker's agent skill states the same limit for `npm ci`, `pip install -r` and `go mod download`).
5. **`COPY --link` with `--chown` takes numeric ids.** The linked layer is independent, so a user created by
   an earlier `RUN` does not exist in it: write `--chown=1001:1001`, not a name.
6. **`WORKDIR` is absolute and replaces `RUN cd ... &&`.**

## 2.2 Base image tags and digests
1. **A tag is mutable.** `FROM alpine:3.21` resolves to whichever patch release the publisher last pushed,
   so a rebuild three months later can differ, and you have no record of what you ran.
2. **A digest (`alpine:3.21@sha256:...`) fixes it**, and also opts you out of automated security fixes
   unless something raises the bump. Docker's recommendation is to pair the pin with GitHub Dependabot
   (`package-ecosystem: "docker"`), which opens pull requests for new tags and digests, so you decide and
   keep a trail. A digest with nobody bumping it is the worst of both.
3. **Never `latest`.** The dockle checklist flags it (DKL-DI-0006) and Docker's agent skill says never to
   use it in production.
4. **Which base to pick is a decision, not a rule.** Docker's best-practices page recommends Alpine for
   small size; the distroless project and Docker's own build-strategies skill favour distroless or slim
   variants for the runtime stage; the Node image documentation (see `node-container-runtime` §1.1) states
   the default variant is the supported one. Choose with the runtime in view (a native module, a libc
   dependency, a need for a shell) and write down why.
5. **Verify an image before building on it** where the publisher signs it: the distroless project publishes
   keyless cosign signatures and gives the command to check them.

## 2.3 What the build context carries
1. **A `.dockerignore` keeps irrelevant files out of the context** (patterns like `.gitignore`): VCS
   directories, dependency directories rebuilt in the image, build output, editor files, env files.
2. **It is defence in depth, not the secret mechanism.** Keep the exclusions and still never rely on them
   as the only protection (Docker's agent skill).
3. **Files that must never be copied in**, even to a stage you discard (they stay in intermediate layers
   and the build cache): `.npmrc`, `.pypirc`, `.netrc`, `pip.conf`, Maven `settings.xml`, `.env`, cloud
   credential files, service-account JSON, registry tokens, TLS private keys, kubeconfig, SSH keys.

## 2.4 Build secrets and SSH
1. **Never carry a credential in `ARG` or `ENV`.** Both are recorded in the layers and readable with
   `docker history`.
2. **Mount a secret for the one step that needs it:**

```dockerfile
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc,required=false \
    npm ci --omit=dev
```

   Use `required=true` when the build cannot succeed without the credential so that a missing secret fails
   at once; `required=false` only when public packages alone would work. Pass the source at build time with
   `docker buildx build --secret id=npmrc,src=$HOME/.npmrc .`.
3. **Never echo or expand the secret into a command line** that ends up in a layer or in
   `--progress=plain` output; read it from its file.
4. **Private Git over SSH uses `RUN --mount=type=ssh`**, with `--ssh default` on the build command. The build
   container has no `known_hosts`, so create it inside the same `RUN`.
5. **Never `StrictHostKeyChecking=no`.** It turns host-key verification off. `ssh-keyscan` is better but
   accepts whatever key the server shows each run, and nothing is pinned between builds; for more
   assurance write the provider's published host key into `known_hosts`.
6. **`--ssh default` exposes every key in your agent** (`ssh-add -l` lists them). Use an agent that holds
   only the key this build needs, or a dedicated unencrypted deploy key passed as `--ssh default=<file>`;
   BuildKit refuses a passphrase-protected key passed that way.

## 2.5 Verify
Build from a clean checkout, then run `docker history --no-trunc` and search the output and the image
filesystem for the credential's value. Rebuild after bumping the base tag and confirm that the change came
from a pull request, not from a pull.
