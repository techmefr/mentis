# dotnet-testcontainers-and-time-seam-pitfalls §1 — Testcontainers

Source: the Testcontainers for .NET documentation (best practices, Resource Reaper, resource reuse, wait
strategies and xUnit.net pages; MIT, commit 84f485c, read 2026-10-16), rewritten.

## 1.1 The eight practices
1. **No static names for containers, networks or volumes.** A static name clashes with a leftover resource and
   the test fails; Docker's random names avoid it.
2. **No static host port.** Bind a random host port and read the mapped one from the container
   (`WithPortBinding(port, true)` then `GetMappedPublicPort(port)`).
3. **Never connect to `localhost` or the loopback address; use the container's `Hostname` property**, because the Docker
   daemon may not be on the test host.
4. **Container-to-container traffic uses network aliases** and the container-side port, not the host mapping.
5. **Do not mount host paths.** Copy the files the container needs before it starts with the resource-mapping
   methods, so the test does not depend on a path that exists only on one machine.
6. **For a Docker setting the library does not expose, use the create-parameter modifier**, not a second tool.
7. **Do not disable the Resource Reaper.** It removes leftover resources whether the run passed or failed. The
   documentation allows disabling it only on environments that clean up Docker resources themselves, such as
   ephemeral CI nodes.
8. **Pin the image version on every builder**, generic or module. The documentation says a `latest` tag can
   point to a new version and make tests flaky.

## 1.2 Readiness
1. **The default wait is "the container is running", which is not enough for most images.** Chain a wait
   strategy that matches what the test needs: an internal port, a file, a log message, an HTTP status.
2. **Set a timeout, retries and interval on a wait when the default is wrong**, and pass a cancellation token to
   the start so a stuck container does not hang the run.
3. **A container meant to exit (a migration, a setup script) needs the one-shot mode**; otherwise its normal exit
   is reported as a failure carrying the exit code and logs.

## 1.3 Reuse
1. **Reuse is experimental** and keeps resources between runs by hashing the builder configuration. It also
   turns the reaper off for those resources, so nothing cleans them up.
2. **The hash does not cover every builder option**, so give reusable resources a distinct label, and treat a
   hand-written hash as the caller's responsibility to keep unique.
3. **Disposing a reusable container stops it, and the next run starts it on a new random port**, which breaks
   services that need their own port in their initial configuration.
4. **Reuse is not a substitute for a shared instance.** The documentation points to the test framework's shared
   instance for speed.

## 1.4 Scope of a container in xUnit.net
1. **One container per test** (the isolated context) is the choice for destructive tests; state written by one
   test is invisible to the next.
2. **A shared fixture** (per class, or per assembly where the framework supports it) is the choice when
   starting is expensive; tests then must not depend on each other's data. The fixture reports through the
   message sink, not the per-test output helper.
3. **A private registry** needs the reaper image made available there with a tool that preserves the manifest
   list and every platform variant, or the image variable overridden; pulling, tagging and pushing by hand
   keeps only the local platform and breaks other architectures.
