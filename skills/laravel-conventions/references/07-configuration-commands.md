# laravel-conventions §7 — Configuration and commands

> Section 7 of `skills/laravel-conventions`. Read it when `config/`, `env()`, an artisan command, a seeder or a factory. The other sections and the guardrails stay in `SKILL.md`.

1. **Config file names and keys follow one casing convention; every value is read through the config
   layer**, never `env()` reached into from business code — outside config files, `env()` returns null once
   the config is cached. The trap is that local development usually has no cached config, so the code works
   on the machine it was written on and returns null in production, on the deploy that cached it. There is
   no error: a feature simply behaves as though the setting were empty.
2. **Third-party credentials and service settings live in config with an env-backed default**, never inline
   in the class that calls the API. That is what makes the same class usable in a test with a fake endpoint,
   and it keeps the value out of the diff.
3. **A secret never enters the repository.** `.env` is not committed and `.env.example` documents the key
   with an empty or obviously-fake value. A secret committed once is compromised even after it is removed:
   deleting it from the working tree leaves it in the history, which is a rotation problem rather than an
   editing problem — rotate the credential, then clean up.
4. **A config file is data, not code.** No closure, no query, no service resolution inside it: the whole
   file is serialised when the config is cached, so anything not serialisable breaks the cache — or worse,
   works locally and fails at boot in production.
5. **A console command declares an explicit signature and description**; the class does the wiring, an
   action class does the work — a command whose `handle()` holds the logic can only be run from a terminal,
   so it cannot be scheduled, queued, tested or called from a controller without copying it.
6. **A console command earns its place by being run more than once** — on a schedule, or on demand as a
   repeatable operation. A one-off **data** change (backfill a column, correct bad rows, reshape a table)
   belongs in a migration, where it is versioned, ordered against the schema it depends on, and replayed on
   every environment by the same mechanism as the rest. A one-off inspection or a single outbound action
   belongs in a REPL snippet with nothing committed. A run-once command that ships becomes dead code the
   moment it runs, and it is the file every later reader has to decide whether it is safe to run again.
7. **A command that changes data is idempotent, or it refuses to run twice.** Someone will run it again —
   after a timeout, after a failed deploy, or because the output scrolled past. Make the second run a no-op
   by keying on state rather than on the fact that it has not happened yet.
8. **A command reports what it did, in counts.** "Done" is indistinguishable from a no-op, so a command
   that processed zero rows because its filter was wrong looks exactly like a success. Print the number
   examined, the number changed and the number skipped.
9. **A destructive command asks, and prefers a dry run.** Require an explicit confirmation in production,
   and where the work can be previewed, make the preview the default and the mutation the flag. Its
   arguments are validated as strictly as a request payload — a command is an input surface, and the fact
   that only staff reach it makes the mistakes fewer, not smaller.
10. **A long-running command works in batches and survives interruption.** Resume from state recorded in
    the database, not from a position in a loop, because the loop's position dies with the process. Batching
    also keeps the memory flat and lets the work stop cleanly on deploy.
11. **A scheduled command declares its overlap policy and its failure visibility.** Without
    `withoutOverlapping`, a run that takes longer than its interval starts competing with itself; without
    somewhere for a failure to surface, a nightly task can stop working for weeks and the first signal is a
    business number that stopped moving.
12. **A seeder carries the reference data the application needs to run, and it is idempotent.** Upsert by a
    natural key rather than inserting: a seeder that duplicates its rows on the second run makes a fresh
    environment unreproducible, and reproducing an environment is the entire point of committing it.
13. **A factory is for tests and local development, never for production data.** It defines the valid
    minimum, with named states for the variants that matter — a factory whose defaults already describe the
    happy path pushes every test into asserting the same shape, and the interesting cases then get built by
    hand in each test instead of being reusable.
14. **A data backfill inside a migration is written against the schema, not against the model.** The
    Eloquent model will change — a renamed attribute, a new cast, a global scope, an accessor — and the old
    migration then breaks or silently writes the wrong thing when it replays on a fresh database. Use raw
    queries or the query builder, so the migration stays true to the columns that existed when it was
    written.
15. **Run the command rather than writing it out** for the user to copy, when a runtime is available. A
    command described but never executed is an untested claim (`WORKFLOW.md`, the default-is-failure
    guarantee).
