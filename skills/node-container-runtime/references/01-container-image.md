# node-container-runtime §1 — Container image

A Node image has to do five things the default Dockerfile does not: run as an unprivileged user, receive
termination signals, keep build tools and secrets out of the final layer, stay inside its memory limit, and
start from the same command the code was tested with. Each rule below says what you see when it is missing.

## 1.1 Multi-stage build
1. **Build in one stage, run in another.** The builder stage installs dependencies with the lockfile-exact
   command (`npm ci` or the package manager's frozen-lockfile equivalent), compiles, and the final stage
   copies only the built output and the runtime dependencies. The final image then carries no compiler, no
   test tooling and, if you leave it out, no package manager.
2. **Native modules need a toolchain only in the build stage.** On Alpine-based images a module compiled with
   node-gyp needs Python, make and a C++ compiler; install them in the builder, never in the final stage.
3. **Pin the base image to a tag you choose on purpose** (the Node major and the variant), and rebuild on a
   schedule: a moving tag changes under you and a pinned one stops getting patches.

## 1.2 Run as the unprivileged user
The official Node image ships a `node` user (uid 1000). Switch to it with `USER node` in the Dockerfile or
`-u node` at run time, after installing anything that needs root, and copy files with the right owner
(`COPY --chown=node:node`). If the app needs global npm installs, point the npm prefix at a directory in the
user's home instead of running as root. A container that runs as root turns any file-write bug into a write
anywhere in the image.

## 1.3 Signals and PID 1
1. **Node was not designed to run as PID 1.** As PID 1 the process gets the kernel's special signal rules
   and no zombie reaping. Either run the container with `--init` (an init process is added for you), or
   put a small init such as tini or dumb-init in the image and make it the entrypoint.
2. **Start node directly.** Use the exec form `CMD ["node", "dist/main.js"]`. A command that goes through a
   package manager script (`npm start`) or a shell string puts a wrapper in between: the wrapper receives
   `SIGTERM`, does not forward it, and the container is killed after the grace period instead of draining.
3. **Verify it.** Start the container, send `docker stop`, and time it. A clean shutdown returns in a
   second or two; ten seconds means the signal never reached the app and the runtime killed it. The app also
   has to handle the signal (the shutdown hooks of the framework), see `nestjs-reliability` §2 for work that
   must finish or hand over.

## 1.4 Production mode
Set `NODE_ENV=production` in the final stage, before dependencies are installed there: several libraries
change behaviour on it, and the package managers skip development dependencies. What the variable should
and should not control is in §2.1 ([`02-runtime-config.md`](./02-runtime-config.md)).

## 1.5 Build secrets
`ARG` and `ENV` are unsuitable for secrets: both end up in the image and its history. Use a build secret
mount instead: `RUN --mount=type=secret,id=<name> ...` makes the secret available during that instruction
only, under `/run/secrets/<name>` by default, and it is supplied at build time with `docker build --secret`.
A private registry token for installing dependencies is the typical case. A secret needed at run time is
not a build concern: inject it when the container starts (see `security-hardening`).

## 1.6 Memory and heap
1. **Limit the container, and size V8 under it.** The container limit (`-m 300M` with a swap ceiling such as
   `--memory-swap 1G`, or the orchestrator's memory limit) is what the kernel enforces and kills at. The V8
   old-space size (`--max-old-space-size`, in MiB) is what the runtime tries to stay under. As the heap
   approaches the old-space limit V8 spends more and more time collecting.
2. **Leave headroom.** The process uses memory outside the V8 heap: buffers, native modules, the code itself,
   threads. Setting the old-space size equal to the container limit ends in the kernel's OOM kill (exit 137)
   rather than a clean out-of-memory report. The Node documentation's own example for a 2 GiB machine is
   1536 MiB, roughly three quarters.
3. **A percentage flag exists** (`--max-old-space-size-percentage`, a share of available system memory, and
   it takes precedence over the size flag). Whether it, and the default limit V8 picks, follow the
   container's cgroup limit rather than the host's was not verified; read the value the process reports
   (`v8.getHeapStatistics().heap_size_limit`) inside the container before relying on a default.
4. **Pass the flag through `NODE_OPTIONS` or the command**, not by editing code; and watch the heap over
   time (see `node-async-performance` §3) before raising it: a leak grows into any limit.

## 1.7 Verification
- `docker stop` time, and the exit code on a limit breach (143 or 0 for a handled stop, 137 for a kill).
- `docker exec <c> id -u` is not 0.
- `docker history` and the final filesystem contain no token, no `.npmrc` credential, no source of tests.
- The final image has no compiler: `docker run --rm <image> which gcc` finds nothing.
- Run the container with a memory limit at the planned value and a load that reaches it; the log shows a
  heap error or a handled shutdown, not an exit 137 with no message.

## 1.8 Nest mapping
Nothing here is Nest-specific except that the framework's shutdown hooks must be enabled for the signal to
trigger `OnApplicationShutdown`; the image only has to deliver the signal. A Nest app built with the Nest
CLI starts from `dist/main.js`; use that file in `CMD`, not `nest start`.
