# python-container-runtime: origin and source stamps

> Provenance of `skills/python-container-runtime`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real service by us. No image was built
and no process was started while writing it.

This block is meant to be folded into the same-topic container or deployment block when PR 118 lands. It
cross-links only blocks that exist on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The uv Docker integration guide (uv documentation) | MIT or Apache-2.0, read 2026-10-08 | `--no-install-project` layering, cache mount link mode, bytecode flag and trade-off, `--no-editable` for copying only the environment, `.venv` in `.dockerignore`, `--frozen` then `--locked` for workspaces, `UV_NO_DEV` |
| The uv Docker example repository: single-stage and multi-stage Dockerfiles, README | MIT or Apache-2.0 (both licence files read), read 2026-10-08 | Non-root user, `PYTHONUNBUFFERED` and its reason, matching interpreter path between stages, disabled Python downloads in the builder, production versus development command |
| FastAPI deployment documentation: Docker and server workers | MIT, read 2026-10-08 | Exec form for graceful shutdown and lifespan events, one process per container on an orchestrator, `--workers` for a single host, `--proxy-headers` behind a TLS proxy |

## Rewrite notes
The base-image pinning rule restates the same advice in `node-container-runtime`; the verification lists and
the rule against `uv run` as the production command are our synthesis from the example's own comments.

## Not verified
1. **`--no-editable` end to end:** the guide was read, but the multi-stage example in the repository copies
   the whole application directory and does not use the flag; the combination was not built.
2. **Shell form not forwarding the signal:** the FastAPI page states the consequence (no graceful shutdown);
   the mechanism of the shell receiving the signal is general container knowledge, not from the pages read.
3. **Loopback binding inside a container** and the "client can send forwarded headers itself" caution are
   general knowledge, not from the pages read.
4. **Whether the uv server wrapper commands forward signals** when started through `uv run` was not tested.
5. **Python minor-version path mismatch** is as stated in the example's comment; the exact error text differs.

## Related blocks
`node-container-runtime` (the Node counterpart), `devops-conventions`, `security-hardening`,
`ci-workflow-hardening`, `python-sqlalchemy-fastapi-pitfalls`.
