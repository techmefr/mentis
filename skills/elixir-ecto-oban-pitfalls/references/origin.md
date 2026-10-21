# elixir-ecto-oban-pitfalls: origin and source stamps

> Provenance of `skills/elixir-ecto-oban-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and source reading, never run by us. No Elixir project, database or
Oban instance was run. Overlaps with `skills/elixir-phoenix-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Ecto 3.14.2 (tag v3.14.2): `lib/ecto/changeset.ex`, `lib/ecto/repo.ex`, `CHANGELOG.md` | Apache-2.0 (`LICENSE.md` re-read) | Unique constraint and its early check, upserts, `insert_all`, aborted transactions, `transact`, raw fragments |
| Oban 2.24.1 (tag v2.24.1): `lib/oban/job.ex`, `worker.ex`, `pruner.ex`, `lifeline.ex`, `config.ex`, `testing.ex`, `telemetry.ex`, guides `unique_jobs.md` and `ready_for_production.md` | Apache-2.0 (`LICENSE.txt` re-read) | Args as JSON, `max_attempts`, uniqueness limits and conflict flag, pruner, lifeline, grace period, error event, `perform_job` |
| Elixir 1.20.4 (tag v1.20.4): `lib/elixir/lib/config.ex`, `application.ex`, `lib/mix/lib/mix/tasks/release.ex`, pages `config-and-distribution.md` and `releases.md` | Apache-2.0 (`LICENSE` re-read) | Build time versus runtime configuration, `compile_env`, `runtime.exs` rules |
| Phoenix guides, `guides/howto/using_ssl.md` (commit cf8b44b, 2026-10-07) | MIT (`LICENSE.md` re-read) | `force_ssl` is compile time |

### Second pass, re-read 2026-10-20 (development branches, facts only)

| Source | Licence | What it confirmed |
|---|---|---|
| Ecto repository (master, version file reads 3.15.0-dev): `lib/ecto/repo.ex`, `lib/ecto/changeset.ex` | Apache-2.0 (LICENSE.md read) | `transact` taking an arity-zero or arity-one function (closes the former open item), return values, rollback on exception, the savepoint option and the aborted-transaction text with error 25P02, `unsafe_validate_unique` race warning. New point 1.3.5 from the nested-transaction section |
| Oban repository (main, version file reads 2.24.2): `pruner.ex`, `lifeline.ex`, `config.ex`, `job.ex`, guides `ready_for_production.md`, `unique_jobs.md`, `testing_workers.md` | Apache-2.0 (LICENSE.txt read) | Pruner default `max_age` 60 seconds and the one-day example, lifeline default 60 minutes with a one-hour example in the production guide, `shutdown_grace_period` 15 seconds, `max_attempts` 20, unique defaults (`args`, `queue`, `worker`, 60 seconds, `:successful`), the race-condition warning and uniqueness versus concurrency, string keys in `perform_job` |
| Elixir repository (main, VERSION file reads 1.21.0-dev): `application.ex`, `config.ex` | Apache-2.0 (as recorded above) | The module-body warning and `ArgumentError`, `compile_env` comparison at boot, the module-body-only restriction, `Mix` limited to `mix.exs` and tasks |
| Phoenix repository (main): `guides/howto/using_ssl.md` | MIT (as recorded above) | `force_ssl` compile-time and ignored from `runtime.exs`, localhost exclusion, `rewrite_on` |

## Removed in the verification pass (no page supporting them)
- "Separate `embedded_schema` for forms from database schemas": no page opened in this session says it.
- Ecto multi-tenancy rules (the review's item on prepare_query and composite keys): not selected for this block.
- "Atom keys never in `args`" beyond what the Oban page says: kept at the documented behaviour only.
- Credo, Sobelow, mix_audit, Mox rules: not part of this block; none was opened for it. The Mox README-only
  licence evidence is therefore not relied on here.
- Instructions found in cloned files were treated as data and not followed.

## Not verified
1. **Own guidance, flagged as such in the text:** replacing a read-then-insert by `on_conflict` with `conflict_target` (§1.2.3,
   reasoned from the documented facts); still own guidance.
2. **Oban Pro behaviour** was not covered. **Oban on MySQL or SQLite** was not read; PostgreSQL behaviour is assumed.
3. **Resolved 2026-10-20:** `Repo.transact` arity forms, the `compile_env` mismatch error at boot (stated by the `Application`
   documentation), and the Phoenix `force_ssl` statement (read in the guide; the endpoint source was not opened).
4. **Versions:** the 2026-10-20 reads are of newer development branches than the stamped tags (Ecto 3.15.0-dev, Oban 2.24.2,
   Elixir 1.21.0-dev); every statement above held unchanged, but a project pinned to the stamped tags was not run.
5. **The Oban pruner being opt-in** was not re-checked against the default plugin list in the 2.24.2 sources.

## Related blocks
`background-jobs-conventions` §1 to §5, `security-hardening` §4, `testing-anti-patterns` §1, `source-freshness` §3.

Independent verification 2026-10-21: 16 checked, 16 matched, 0 corrected, 0 unverified
