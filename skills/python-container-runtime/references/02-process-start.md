# python-container-runtime §2 — Process start

The command at the end of the Dockerfile decides whether the orchestrator's stop signal reaches your
application, whether its shutdown code runs, and how many copies of it share the container's memory.

## 2.1 Exec form, so the signal arrives
1. **Write the command in exec form** (a JSON array), not as a shell string. The FastAPI deployment
   documentation says to always use the exec form so the app can shut down gracefully and its lifespan
   events are triggered: a shell string puts a shell in front of the server, and the stop signal goes to the
   shell, which does not hand it on. The Dockerfile reference states the mechanism for a shell-form entrypoint: it
   runs as a child of `/bin/sh -c`, so the executable is not PID 1 and does not receive the `SIGTERM` that
   `docker stop` sends; its table of command combinations shows a shell-form `CMD` run through `/bin/sh -c` the same
   way. The container is then killed after the grace period instead of draining.
2. **Do not start the service through a wrapper** (a script that does not `exec` the server, a package
   manager's run command): the same problem one level up. The Node counterpart is
   `node-container-runtime` §1, including the init-process option when the application is PID 1.
3. **After `uv sync`, put the environment's `bin` directory on `PATH` and call the server directly.** A
   command that goes through `uv run` re-syncs at start (the example's own comment says it syncs dependencies on
   startup); the example uses it for the development image only and runs the server directly in the production
   stage. Whether uv stays as a parent process, and whether it forwards signals, was not read (see origin).
4. **Verify it:** start the container, run `docker stop`, time it. Seconds is a clean shutdown; the full
   grace period means the signal never reached the app. Check that code after the lifespan `yield` ran.

## 2.2 Development server versus production server
1. **`fastapi dev` reloads on change and is for development**; `fastapi run` is the production command. The
   uv example's own comment says the production command is `run`. The FastAPI CLI page says `dev` enables
   auto-reload by default, which it calls resource-intensive and less stable, and listens on `127.0.0.1`; `run`
   disables reload and listens on `0.0.0.0`.
2. **Bind to all interfaces inside the container:** a loopback address is not reachable from outside the
   container's network namespace. `fastapi run` already defaults to `0.0.0.0` per the CLI page, while `fastapi dev`
   needs `--host 0.0.0.0`, as the uv example's development command shows; the example also passes the host
   explicitly to `run`. The port exposure and who may reach it is a deployment decision.
3. **Behind a TLS-terminating proxy, enable forwarded headers** so the server trusts the forwarded scheme and
   client address from that proxy. The container page of the FastAPI deployment documentation passes
   `--proxy-headers`. In the FastAPI CLI source (main, read 2026-10-21) that option already defaults to on for both
   `dev` and `run`, while `--forwarded-allow-ips` defaults to unset, so the address list is what you must set; the
   flag is harmless to repeat, and an older CLI release may default differently. The behind-a-proxy page says the server interprets those headers only for the addresses
   given in `--forwarded-allow-ips`, and that `"*"` trusts every address, acceptable only when nothing but the proxy
   can reach the server. Without it, generated URLs (the redirect to `http://localhost:8000/items/` instead of the
   public HTTPS address) and client-address checks see the proxy. A client can send those headers itself, so name
   the proxy address rather than trusting everyone when it is known.

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
