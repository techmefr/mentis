# python-container-runtime §2 — Process start

The command at the end of the Dockerfile decides whether the orchestrator's stop signal reaches your
application, whether its shutdown code runs, and how many copies of it share the container's memory.

## 2.1 Exec form, so the signal arrives
1. **Write the command in exec form** (a JSON array), not as a shell string. The FastAPI deployment
   documentation says to always use the exec form so the app can shut down gracefully and its lifespan
   events are triggered: a shell string puts a shell in front of the server, and the stop signal goes to the
   shell, which does not hand it on. The container is then killed after the grace period instead of
   draining.
2. **Do not start the service through a wrapper** (a script that does not `exec` the server, a package
   manager's run command): the same problem one level up. The Node counterpart is
   `node-container-runtime` §1, including the init-process option when the application is PID 1.
3. **After `uv sync`, put the environment's `bin` directory on `PATH` and call the server directly.** A
   command that goes through `uv run` re-syncs at start and keeps uv as the parent process; the uv example
   uses it for the development image only.
4. **Verify it:** start the container, run `docker stop`, time it. Seconds is a clean shutdown; the full
   grace period means the signal never reached the app. Check that code after the lifespan `yield` ran.

## 2.2 Development server versus production server
1. **`fastapi dev` reloads on change and is for development**; `fastapi run` is the production command. The
   uv example's own comment says the production command is `run`. A production image with the reloader
   starts a watcher process and listens on defaults meant for a laptop.
2. **Bind to all interfaces inside the container** (`--host 0.0.0.0`): the default loopback address is not
   reachable from outside the container's network namespace. The port exposure and who may reach it is a
   deployment decision.
3. **Behind a TLS-terminating proxy, pass `--proxy-headers`** so the server trusts the forwarded scheme and
   client address from that proxy. Without it, generated URLs and client-address checks see the proxy. Only
   enable it when a proxy you control is in front: a client can send those headers itself.

## 2.3 One process per container, or workers
1. **On an orchestrator that replicates containers, run one server process per container.** The FastAPI
   documentation says replication is then the orchestrator's job, memory limits per container stay
   predictable, and workers inside a container would only multiply memory.
2. **Use `--workers` on a single host with no orchestrator,** to use several cores. It is a process manager
   with N worker processes, still one container.
3. **Each worker process is a fork or a fresh process with its own connection pool.** A pool sized for one
   process is multiplied by the worker count and the replica count (`python-sqlalchemy-fastapi-pitfalls`
   §1.5).
4. **Run migrations and one-off steps as a separate job** when there are several replicas, not in every
   container's start command; with a single container they can run right before the server starts.

## Verification
- `docker stop` time recorded, and the application's shutdown log line present.
- The start command in the image is an array; `docker inspect` shows no shell wrapper.
- With a proxy in front, a request's reported scheme and client address are the real ones.
