# dockerfile-build-pitfalls §1 — Layers, cache and the shell

Every `RUN` is a layer and every layer is cached by its instruction text, not by what the network would
return today. The traps in this section all come from that: a step is skipped because its text did not
change, a failure is swallowed by the shell, or a value is kept by a layer you thought you had cleaned.

## 1.1 The package index and the cache
1. **Update and install share one `RUN`.** A `RUN apt-get update` on its own is cached; when the install
   line below it later gains a package, Docker sees an unchanged update step, reuses it, and the install
   runs against an index from the day of the first build. The result is an old package version or a failed
   install. Writing `apt-get update && apt-get install -y --no-install-recommends ...` in one instruction
   invalidates both together. Docker's guidance calls this cache busting.
2. **Pinning a package version also busts the cache.** `package=1.3.*` changes the instruction text, so the
   update runs again, and it removes surprises from a package changing under you.
3. **Two ways to keep the index out of the image, for two styles.** In the layer style, end the same `RUN`
   with `rm -rf /var/lib/apt/lists/*`. In the cache-mount style
   (`RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked`)
   the index lives outside the layer and no cleanup is needed; `sharing=locked` is needed because apt wants
   exclusive access. The two sources read differ because they describe different styles: pick one per
   Dockerfile and do not mix a `rm` with a cache mount on the same directory.
4. **Official Debian and Ubuntu images already run `apt-get clean`**, so calling it yourself adds nothing
   (Docker's documentation).

5. **Alpine has the same two styles.** `apk add --no-cache` keeps the index out of the layer (dockle
   checkpoint DKL-DI-0004). With a cache mount on `/etc/apk/cache` (`sharing=locked`), Docker's agent skill
   says to drop `--no-cache` so the downloads land in the mount. The skill attributes that to the Alpine
   wiki, not to Docker documentation; treat it as a pattern to test.

## 1.2 Pipes in a `RUN`
1. **A pipe judges only its last command.** Docker runs `RUN` through `/bin/sh -c`, which looks at the exit
   code of the last stage of a pipe. `RUN wget -O - https://example.test | wc -l > /number` succeeds and
   produces an image even when `wget` failed.
2. **Start such a line with `set -o pipefail &&`.**
3. **Not every shell has it.** The Debian-family `dash` does not. Use the exec form to name a shell that does:

```dockerfile
RUN ["/bin/bash", "-c", "set -o pipefail && wget -O - https://example.test | wc -l > /number"]
```

## 1.3 A value set in one layer stays in that layer
1. **`ENV` writes the value into its layer.** A later `RUN unset NAME` does not remove it: the value is still
   there and can be dumped. Docker's documentation shows the leak with a build and a
   `docker run ... echo $NAME`.
2. **Set, use and unset inside one `RUN`**, chained with `&&` so that a failure stops the build:

```dockerfile
RUN export ADMIN_USER="mark" \
    && echo $ADMIN_USER > ./mark \
    && unset ADMIN_USER
```

3. **For anything secret, do not use this at all**; use a build secret (`02-sources-and-secrets.md` §2.4).
   The Node specifics of the same rule are in `node-container-runtime` §1.

## 1.4 Two flags that are not the same flag
1. **`docker build --pull`** asks the registry whether the base image tag now points to something newer and
   downloads it even if a copy is cached. It does not rerun your steps.
2. **`docker build --no-cache`** reruns every step, so package managers fetch current versions. It does not
   refresh the base image.
3. **For a clean rebuild with updated everything use both.** Rebuild on a schedule: an image is a snapshot of
   its base and libraries at build time and does not patch itself.

## 1.5 Verify
Build twice with a package added to the install line in between and check that the index step reran. Break a
piped command on purpose (a URL that returns an error) and check that the build fails. Run the finished
image with `env` and `docker history --no-trunc` and look for any value you set in an `ENV`.
