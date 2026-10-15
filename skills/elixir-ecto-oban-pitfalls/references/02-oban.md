# elixir-ecto-oban-pitfalls §2 — Oban

Sources: Oban 2.24.1 (`lib/oban/job.ex`, `worker.ex`, `pruner.ex`, `lifeline.ex`, `testing.ex`, `telemetry.ex`,
the unique jobs and ready-for-production guides), read 2026-10-08. Behaviour that needs Oban Pro is not covered.

## 2.1 Args and attempts
1. **`args` always arrive with string keys.** They are stored as JSON, which stringifies every key, so pattern match
   on `%{"id" => id}` in `perform/1`, not on atom keys, and pass only values that serialise to JSON.
2. **Set `max_attempts` explicitly per worker.** The default is 20, so a worker that fails for a permanent reason keeps
   retrying with backoff for a long time. A `snooze` does not consume an attempt.
3. **Make jobs safe to run twice** (`background-jobs-conventions` §1). Oban's own pieces that restart work, such as
   the lifeline in §2.3, can run a job that is still executing.

## 2.2 Uniqueness
1. **Uniqueness applies at insert time only.** It prevents duplicate rows from being inserted; it does not make unique
   jobs run one at a time. Limit concurrency with the queue's `limit`, not with `unique`.
2. **It can race.** Oban's guide says uniqueness uses transactional locks and queries, not a database unique
   constraint, so it is prone to race conditions in some circumstances. Do not use it as the only protection against
   a duplicate side effect; keep the job idempotent.
3. **The defaults are a 60 second period, the `:successful` states and the fields `args`, `queue` and `worker`.**
   Set `period` and `states` deliberately, and leave `fields` alone unless you need to narrow it with `keys`,
   since the guide says other fields risk unexpected conflicts.
4. **Insert returns `{:ok, job}` on a conflict too.** Check `job.conflict?` after `Oban.insert/2`; when it is true
   and `job.id` is `nil`, no lock could be acquired. Code that assumes every `{:ok, job}` is a new job is wrong.

## 2.3 Keeping the table and the queue healthy
1. **Enable the pruner.** In 2.24.1 it is opt-in: `pruner: Oban.Pruner` or `pruner: [max_age: {1, :day}]` in the
   Oban config. Its default `max_age` is 60 seconds and the production guide suggests one day as a conservative start,
   because introspection and uniqueness rely on finished jobs staying in the table until they are pruned. Without a
   pruner the table grows indefinitely.
2. **Enable the lifeline to rescue orphans.** Jobs left `executing` after a deploy or crash stay there
   indefinitely without it. `lifeline: [rescue_after: {1, :hour}]` is the guide's example; rescuing is purely time
   based, so a job that is genuinely still running can be run a second time. A rescued job that has used all its
   attempts is discarded.
3. **Give running jobs time to finish on shutdown.** `shutdown_grace_period` defaults to 15 seconds. Raise it, or
   expect orphans; even a high value does not cover crashes or very long jobs.
4. **`Oban.Pruner` and `Oban.Lifeline` replace the old plugin modules** (`Oban.Plugins.Pruner`,
   `Oban.Plugins.Lifeline` are deprecated delegates), so use the new names in new config.

## 2.4 Errors and tests
1. **Report errors from the job exception telemetry event.** Attach a handler to `[:oban, :job, :exception]`; its
   metadata carries the job, the reason and the stacktrace. Some error trackers attach to it themselves.
2. **Test workers with `perform_job/2,3`, not by calling `perform/1`.** It checks that the worker implements the
   behaviour, that the options build a valid job and that the return value is valid, and it stringifies the args keys, so a test
   written with atom keys sees the same arguments production does.
