# testcontainers-node-pitfalls §1 — Ports, readiness and wiring

> Section 1 of `skills/testcontainers-node-pitfalls`. Read it when a test cannot reach its service, starts too
> early, or needs files or other containers. Restated from the Testcontainers for Node documentation
> (`docs/features/containers.md`, `wait-strategies.md`, `networking.md`, `quickstart/usage.md` and
> `configuration.md`, commit `fc9e1db`, MIT), read 2026-10-16. Method names and defaults are version-bound.
> Sentences marked "own guidance" are ours.

1. **Read the host and the mapped port from the started container.** The library binds a random free host port
   to each exposed container port, to avoid conflicts when tests run quickly or in parallel. Read it with the
   mapped-port call (or the first-mapped-port call for a container with one port) and build the address from
   the container's host call, as the quickstart does with a connection string. A fixed host binding exists and
   the documentation marks it not recommended. The protocol defaults to TCP; name UDP in the port.
2. **A remote daemon changes the host.** A configuration variable names the Docker host on which ports are
   exposed. Own guidance: that is why the address is built from the host call and never from `localhost`.
3. **Know what the default wait is.** The documentation says that when the image defines a health check, or one
   is configured on the container, the library waits for it; when there is none, or the image disables it, it
   waits up to 60 seconds for the mapped ports to be bound. Own guidance: a bound port is not a ready service
   for most databases and brokers, which accept the connection before they can serve it, so name the readiness
   you need.
4. **Pick the strategy that tests readiness, and set a timeout for slow images.** Set one with the container's
   wait-strategy call. The documented ones: listening ports; a log message (a string or a regular expression,
   optionally a number of occurrences); the container's health check; an HTTP request (200 by default, a status
   or a body predicate can be set, and it can stop waiting when the container exits); a command that must exit
   successfully; a one-shot container that must exit with 0; and an "all of these" combination. The startup
   timeout is configurable on a strategy; on a combination, an inner strategy keeps its own timeout, one without
   gets the combination's, and a deadline on the combination bounds all of them. Own guidance: raise the
   timeout for a heavy image, and do not add a sleep after a wait.
5. **A custom health check is declared in milliseconds.** It takes a test command, an interval, a timeout,
   retries and a start period, and the last four are inherited from the image if omitted. The shell form of the
   command needs a shell in the image; for a distroless image use the form without a shell.
6. **Do not mount a host path; copy the file in.** The documentation marks bind mounts not recommended because
   they are not portable: they do not work with Docker in Docker or with a remote Docker agent, where the path
   is on another machine. Files, directories, literal content or a tar archive can be copied into the container
   before it starts (or after), with optional permission bits, and symbolic links in the source are followed.
7. **Do not name a container, and do not set its host name.** A fixed name raises a conflict when a container
   with that name exists; the documentation points to a network and network aliases for container-to-container
   traffic, and also marks a custom host name not recommended.
8. **To let a container call a service on the host**, the library can expose a host port; containers then reach
   it at a fixed alias for the host, through a helper container that forwards the port. Own guidance: that is
   an exception to keep for a service you cannot containerise.
9. **Read the container's logs when it does not start.** A log consumer can be attached before start, and the
   log-message wait needs a log driver that can be read; one option sets the default log driver for hosts whose
   driver cannot be read. Own guidance: a wait that times out is a log to read, not a number to raise.
