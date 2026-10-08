# python-container-runtime §1 — Image build

A Python image has to do five things the default Dockerfile does not: install from the lockfile, keep the
dependency layer cached across source edits, leave development tooling out, run as an unprivileged user, and
start from an interpreter that is where the virtual environment expects it. The commands below are uv's.

## 1.1 Dependencies before source
1. **Install the dependencies first with the project itself left out** (`uv sync --locked
   --no-install-project`), then copy the source and sync again. The uv documentation describes the first
   command as installing the dependencies but not the project, and the point is cache behaviour: the
   dependency layer is rebuilt only when the manifest or lockfile changes, not on every source edit.
2. **Bind-mount the manifest and the lockfile for the first step** rather than copying the whole tree, so
   that nothing but those two files invalidates the layer.
3. **Use a cache mount for uv's cache** and set `UV_LINK_MODE=copy`: the documentation explains the cache
   and the target are on different file systems, so the default linking cannot be used.

## 1.2 Install exactly the lockfile
1. **`--locked` makes the build fail if the lockfile is stale** instead of resolving again and changing it.
   An image built from a resolution nobody committed is not the one that was tested.
2. **A workspace with several members needs `--frozen` for the first step and `--locked` after all members
   are copied.** The documentation gives the reason: the lockfile cannot be checked as up to date without
   every member's manifest.
3. **Leave development dependencies out** with `UV_NO_DEV=1` (or the equivalent flag). Test runners and
   linters in a production image are size and attack surface with no use.
4. **Enable bytecode compilation** with `UV_COMPILE_BYTECODE=1`. The documentation says it improves startup
   at the cost of install time and image size, so it is a decision for services that start often.
5. **Set `PYTHONUNBUFFERED=1`** so standard output and error are not buffered: a process that crashes can
   otherwise die without having emitted its last log lines. The uv example sets it for this reason.

## 1.3 Build in one stage, run in another
1. **The final stage can omit uv and the source.** Sync with `--no-editable` in the builder, which installs
   the project as a normal package instead of a link back to the source tree; the documentation says this
   lets you copy only the virtual environment into the final image.
2. **The interpreter path must be identical in both stages.** The environment records the path of the
   interpreter that created it, so a final image on a different Python minor, or a different base, starts
   with "no such file". Use the same base image family and version for both, and disable managed Python
   downloads in the builder (`UV_PYTHON_DOWNLOADS=0`) when the final stage uses the system interpreter,
   as the uv example does; if a managed interpreter is used, copy it across too.
3. **Pin the base image on purpose** (the Python version and variant) and rebuild on a schedule: a moving
   tag changes under you and a pinned one stops receiving patches. See `devops-conventions` §1.

## 1.4 Keep the host out of the image
1. **Put `.venv` in `.dockerignore`.** The uv documentation says a platform-specific virtual environment has to
   be recreated inside the container and so must not be included in the build. A copied environment is
   built for the host's platform and interpreter, which is why the image may start only where it was built.
2. **Check what else the context carries:** local environment files, caches, `.git`. A `COPY . .` sends all
   of it.
3. **Never pass a secret as `ARG` or `ENV`:** both persist in the image history (`node-container-runtime`
   §1 gives the build-secret mechanism, which is not Python-specific).

## 1.5 Run as an unprivileged user
1. **Create a non-root user and switch to it** (`USER`) after the steps that need root. Copy the application
   with the right owner (`COPY --chown`). A container that runs as root turns a file-write bug into a write
   anywhere in the image.
2. **Reset the entrypoint** if the base image's is the package manager, so the command in §2 is what runs.

## Verification
- `docker run --rm <image> id` shows a non-root user; writing outside the data directory fails.
- Inside the container, the installed set matches the lockfile and contains no development tool.
- The image builds from a clean clone that has no `.venv`, and again after a source-only edit with the
  dependency layer reported as cached.
