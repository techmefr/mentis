# testcontainers-node-pitfalls §2 — Lifecycle, reuse and runtimes

> Section 2 of `skills/testcontainers-node-pitfalls`. Read it when containers leak, tests share state, or CI
> behaves differently from a laptop. Restated from the Testcontainers for Node documentation
> (`docs/features/containers.md`, `configuration.md`, `supported-container-runtimes.md`, `quickstart/usage.md`
> and `features/networking.md`, commit `fc9e1db`, MIT), read 2026-10-16. Variable names, image tags and
> defaults are version-bound. Sentences marked "own guidance" are ours.

1. **Stopping returns immediately by default.** The documentation says the library issues the stop command and
   does not wait for the container to stop, to save time; pass a timeout to wait. Own guidance: wait when the
   next step needs the resource released, such as a volume, a network or a name, and stop a network after the
   containers in it (the documentation's example stops the container, then the network).
2. **Containers are removed when stopped, and so are their volumes.** Both can be turned off, for the container
   (the auto-remove setting, or a stop option) and for volumes (a stop option). A stopped container that was
   not removed can still be read: its files can be fetched as a tar stream, for example a log file, after the
   failure. Own guidance: turn removal off only while debugging a failure, not in the committed configuration.
3. **The cleanup container is the safety net; do not remove the net and the cleanup together.** The library
   starts a resource reaper (Ryuk) that removes what a run left behind when the process exits unexpectedly. The
   documentation warns that disabling it (an environment variable) and disabling automatic removal together
   leaves containers behind after you are done. It can also be turned off for one container, which only affects
   that automatic cleanup; an explicit stop still stops and removes it.
4. **Reuse shares one container across tests, and what is inside it too.** With reuse requested on a container,
   the library does not start a new one if a managed container with the same configuration is already running,
   and it can also reuse one that is stopped but not removed. A global variable turns the feature on or off and,
   per the page, it is enabled when the variable is not declared; a container still has to ask for reuse. Own
   guidance: rows, keys and queues one test wrote are visible to the next, and to the next run if the container
   outlives it, so either clean the state between tests or do not request reuse on CI.
5. **Pull policy decides what happens to an image that is not there.** By default an image missing locally is
   pulled. Options: always pull, never pull (startup fails if the image is missing, and the policy only covers
   the image you named, so the cleanup container may still be pulled), or a custom policy that can forbid
   pulling. A platform can be requested for an image. A default registry prefix can be set by a variable.
   Own guidance: name an exact image tag, as the documentation's version example does, so CI and laptops run the
   same version.
6. **Some options need a runtime that allows them.** The documentation says ulimits and resource quotas are not
   supported in rootless runtimes, that bind mounts fail with Docker in Docker or a remote agent (point 1.6),
   that host networking only works on Linux, that one module needs a privileged container and so does not
   work in rootless or Docker-in-Docker environments, and, for Podman, that the cleanup container does not
   work when running rootless and has a privileged setting when rootful. Own guidance: before moving a suite to
   a new runner type, run it once there with the debug logging of point 2.7.
7. **Turn on the library's logs and the container's logs when a start fails.** A debug variable enables all
   library loggers or one at a time (containers, pulls, execs, builds, compose), and a log consumer can be
   attached to the container before it starts, which the documentation recommends for a container that fails to
   start.
8. **Do not leave a client open.** The quickstart disconnects the client and stops the container in its teardown
   hook. Own guidance: a test file that starts a container in a setup hook must have the matching stop in a
   teardown hook, even when the suite is also covered by point 2.3, because the safety net only fires at
   process exit.
