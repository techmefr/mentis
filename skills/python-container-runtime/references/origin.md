# python-container-runtime: origin and source stamps

> Provenance of `skills/python-container-runtime`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real service by us. No image was built
and no process was started while writing it.

Overlaps with `skills/dockerfile-build-pitfalls` (2026-10-19); cross-referenced, not merged. It
cross-links only blocks that exist on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The uv Docker integration guide (uv documentation) | MIT or Apache-2.0, read 2026-10-08 | `--no-install-project` layering, cache mount link mode, bytecode flag and trade-off, `--no-editable` for copying only the environment, `.venv` in `.dockerignore`, `--frozen` then `--locked` for workspaces, `UV_NO_DEV` |
| The uv Docker example repository: single-stage and multi-stage Dockerfiles, README | MIT or Apache-2.0 (both licence files read), read 2026-10-08 | Non-root user, `PYTHONUNBUFFERED` and its reason, matching interpreter path between stages, disabled Python downloads in the builder, production versus development command |
| FastAPI deployment documentation: Docker and server workers | MIT, read 2026-10-08 | Exec form for graceful shutdown and lifespan events, one process per container on an orchestrator, `--workers` for a single host, `--proxy-headers` behind a TLS proxy |

### Second pass, read 2026-10-20 (facts only, rewritten)

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| uv documentation, Docker integration guide (source page in the uv repository, main) | MIT or Apache-2.0 (as recorded above) | The guide mounts only `uv.lock` with `--frozen` for the first sync (block now states both variants); `--no-install-workspace` for workspaces; the cache mount and `UV_LINK_MODE=copy`, bytecode trade-off, `--no-editable`, `.venv` in `.dockerignore`, `--frozen` then `--locked` reason |
| uv Docker example repository: `Dockerfile`, `multistage.Dockerfile`, `standalone.Dockerfile`, README (main) | MIT or Apache-2.0 (both licence files present, MIT file header read) | Both bind mounts with `--locked`, non-root user, `PYTHONUNBUFFERED` comment, `uv run fastapi dev` for development only, `fastapi run` in the production stage, matching interpreter path comment, `UV_PYTHON_DOWNLOADS=0`; the multistage example syncs without `--no-editable` (confirms the earlier note) |
| FastAPI documentation, source pages in the FastAPI repository (master, version file reads 0.156.8): deployment (Docker, server workers), the behind-a-proxy page, the FastAPI CLI page | MIT (repository LICENSE, MIT licence, copyright Sebastian Ramirez) | Exec-form warning, `--proxy-headers` in the container page, `--forwarded-allow-ips` in the proxy page, `dev` listens on `127.0.0.1` with reload and `run` on `0.0.0.0` without, one process per container on a cluster, `--workers` on a single host. Corrected §2.2.2 and §2.2.3 |
| Docker documentation, Dockerfile reference (rendered page) | Apache-2.0 (documentation repository LICENSE read) | A shell-form entrypoint runs under `/bin/sh -c`, is not PID 1 and does not receive `SIGTERM` from `docker stop`; the command table shows a shell-form `CMD` run through `/bin/sh -c` |

## Rewrite notes
The base-image pinning rule restates the same advice in `node-container-runtime`; the verification lists and
the rule against `uv run` as the production command are our synthesis from the example's own comments.

## Not verified
1. **`--no-editable` end to end:** the guide and the example were read; the multi-stage example does not use the flag and
   the combination was not built.
2. **Resolved 2026-10-20:** the shell-form signal mechanism is stated by the Dockerfile reference (ENTRYPOINT text,
   and the CMD command table); the FastAPI page states the consequence. Still unverified: any claim about a
   specific shell, such as one that does forward signals.
3. **Loopback binding inside a container:** the reachability statement is general networking; the CLI defaults
   (`dev` on `127.0.0.1`, `run` on `0.0.0.0`) are read. The forwarded-header caution is now backed by the proxy page.
4. **Whether `uv run` stays as a parent process or forwards signals** was not read or tested; the example comment says
   only that it syncs at start.
5. **Python minor-version path mismatch** is as stated in the example comment; the exact error text differs.
6. **Per-worker connection pools** (§2.3.3) are general behaviour; the server-workers page says nothing on pools.
7. **FastAPI pages are the master branch** (0.156.8 in the version file) and may not match the release a project pins.

Corrected 2026-10-21: §2.2.3 said forwarded headers have to be enabled with `--proxy-headers`; the `fastapi-cli`
source on main defaults it to on, so only `--forwarded-allow-ips` is a real choice (the docs pages still show the flag).
The `dev` and `run` host and reload defaults (127.0.0.1 with reload; 0.0.0.0 without) were confirmed in that source.

## Related blocks
`node-container-runtime` (the Node counterpart), `devops-conventions`, `security-hardening`,
`ci-workflow-hardening`, `python-sqlalchemy-fastapi-pitfalls`.

Independent verification 2026-10-21: 15 checked, 14 matched, 1 corrected, 0 unverified
