# dockerfile-build-pitfalls §3 — The final stage: shell-less images, users, health

What the last stage contains decides what an attacker or an operator can do in the running container, and
how the start command is read.

## 3.1 Images without a shell
1. **Distroless images have no shell and no package manager.** `ENTRYPOINT` must therefore be in vector
   (exec) form: `ENTRYPOINT ["myapp"]` works; `ENTRYPOINT "myapp"` does not, because the runtime would
   prefix a shell that is not there.
2. **If the entrypoint is the empty vector, write `CMD` in vector form too.** The distroless `static`,
   `base` and `cc` images have an empty entrypoint by default; the language runtime images have their own.
3. **Use the `:debug` variant to get in, never to ship.** It adds a busybox shell; start it with
   `docker run --entrypoint=sh -ti <image>`. With an existing tag such as `nonroot`, the tag is
   `debug-nonroot`.
4. **Name the distribution in the tag** (for example `-debian13`): an unqualified tag moves to the next
   Debian release later and can break the build.

## 3.2 Users and privilege
1. **Run the service as a non-root user**: a lint checkpoint (CIS DI-0001) and Docker's `USER` guidance.
   Give it an explicit UID and GID: ids assigned by `useradd` depend on what ran before, so they are not
   stable across rebuilds. The Node-specific form is in `node-container-runtime` §1.2.
2. **A very large UID can fill the disk.** Docker's documentation warns that creating a user with a huge
   UID writes a sparse `/var/log/faillog` into the layer; pass `--no-log-init` to `useradd`. The
   Debian and Ubuntu `adduser` wrapper does not take that flag.
3. **No `sudo` in an image.** Its TTY and signal handling are unpredictable; if you need to start as root
   and drop to a user, Docker points to `gosu`.
4. **Do not switch `USER` back and forth**; install as root, then switch once, before `ENTRYPOINT`.
5. **Strip setuid and setgid bits** from files you do not need them on (`chmod u-s`, `chmod g-s`): they are
   privilege-escalation material (CIS DI-0008).
6. **Do not declare a sensitive host directory as a `VOLUME`** (`/dev`, `/proc`, `/sys` are what the
   linter checks).

## 3.3 Health
1. **Give the image a `HEALTHCHECK` when whoever runs it acts on the result.** The CIS checkpoint
   (DI-0006) says the engine can use the status to replace a non-working container:

```dockerfile
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```

2. **A command-based check needs its binary in the image**, which a shell-less image rarely has. Own
   guidance, not from the sources above: for Compose a sidecar can do the check from outside
   (`docker-compose-file-pitfalls` §1.3), and for Kubernetes the probes in
   `kubernetes-workload-pitfalls` §1 are the mechanism to rely on.

## 3.4 Smaller points that tend to be copied wrongly
1. **`apt-get dist-upgrade` in an image.** The linter lists it as something to avoid, citing a Docker docs
   change; the Docker best-practices page read for this block no longer carries any advice on it, so
   treat it as a lint opinion, not a rule.
2. **Alpine package installs** are covered with the apt ones in `01-layers-and-cache.md` §1.1.
3. **Install only what the service runs.** A text editor does not belong in a database image
   (Docker's documentation); one concern per container.
4. **`EXPOSE` states the port the service listens on**; mapping it to a host port is done by whoever runs
   the container (Docker's documentation).

## 3.5 Verify
Read the configured user with `docker inspect --format '{{.Config.User}}' <image>`; in an image that has a
shell, run `id` in it as well. Run `docker stop` and check it returns quickly (signals,
`node-container-runtime` §1.3). Start a shell-less image once exactly as the orchestrator will.
