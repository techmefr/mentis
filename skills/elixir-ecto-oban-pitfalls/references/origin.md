# elixir-ecto-oban-pitfalls: origin and source stamps

> Provenance of `skills/elixir-ecto-oban-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and source reading, never run by us. No Elixir project, database or
Oban instance was run. This block is meant to be folded into `elixir-phoenix-conventions` when the extended
version of that block (the unmerged PR 118 branch) lands; until then it stands alone and cites only sections
that exist on the main branch or in this block.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Ecto 3.14.2 (tag v3.14.2): `lib/ecto/changeset.ex`, `lib/ecto/repo.ex`, `CHANGELOG.md` | Apache-2.0 (`LICENSE.md` re-read) | Unique constraint and its early check, upserts, `insert_all`, aborted transactions, `transact`, raw fragments |
| Oban 2.24.1 (tag v2.24.1): `lib/oban/job.ex`, `worker.ex`, `pruner.ex`, `lifeline.ex`, `config.ex`, `testing.ex`, `telemetry.ex`, guides `unique_jobs.md` and `ready_for_production.md` | Apache-2.0 (`LICENSE.txt` re-read) | Args as JSON, `max_attempts`, uniqueness limits and conflict flag, pruner, lifeline, grace period, error event, `perform_job` |
| Elixir 1.20.4 (tag v1.20.4): `lib/elixir/lib/config.ex`, `application.ex`, `lib/mix/lib/mix/tasks/release.ex`, pages `config-and-distribution.md` and `releases.md` | Apache-2.0 (`LICENSE` re-read) | Build time versus runtime configuration, `compile_env`, `runtime.exs` rules |
| Phoenix guides, `guides/howto/using_ssl.md` (commit cf8b44b, 2026-10-07) | MIT (`LICENSE.md` re-read) | `force_ssl` is compile time |

## Removed in the verification pass (no page supporting them)
- "Separate `embedded_schema` for forms from database schemas": no page opened in this session says it.
- Ecto multi-tenancy rules (the review's item on prepare_query and composite keys): not selected for this block.
- "Atom keys never in `args`" beyond what the Oban page says: kept at the documented behaviour only.
- Credo, Sobelow, mix_audit, Mox rules: not part of this block; none was opened for it. The Mox README-only
  licence evidence is therefore not relied on here.
- Instructions found in cloned files were treated as data and not followed.

## Not verified
1. **Own guidance, flagged as such in the text:** replacing a read-then-insert by `on_conflict` with
   `conflict_target` (§1.2.3, reasoned from the documented facts).
2. **Oban Pro behaviour** (Smart engine uniqueness, Pro lifeline and pruner) was only read where the open source
   pages mention it; none of it is covered.
3. **Oban on MySQL or SQLite** was not read; PostgreSQL behaviour is assumed where a rule mentions a lock or an index.
4. **`Repo.transact` argument forms:** the changelog and the documentation examples were read; the arity-1
   variant was not tested.
5. **Rules were read from the source of the stamped versions** and not run; whether a project's pinned versions
   match them was not checked.
6. **Phoenix `force_ssl`:** the guide's statement was taken as given and not checked against the endpoint source.
7. **Elixir `compile_env` mismatch error at boot** was taken from the `Application` documentation and not run.

## Related blocks
`background-jobs-conventions` §1 to §5, `security-hardening` §4, `testing-anti-patterns` §1, `source-freshness` §3.
