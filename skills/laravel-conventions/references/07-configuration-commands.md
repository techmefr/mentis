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
16. **`Isolatable` is point 11's overlap policy for a command triggered outside the scheduler** — a manual
    rerun, a webhook-fired command, two deploys landing close together. `withoutOverlapping` only guards
    the scheduled entry; a command that can also start some other way is unprotected unless it carries the
    lock itself. The lock key defaults to the command's name, so two runs of the same command with
    different arguments block each other unless `isolatableId()` folds the argument into the key — the
    trap is a command isolated by name alone silently serialising work that was actually safe to run in
    parallel per tenant or per record.
17. **`config:cache` freezes every config file into one array, and that is when point 1's `env()`-outside-config
    trap actually fires in production.** Running it in local development would surface the bug immediately;
    skipping it locally and running it only in the deploy pipeline is exactly how the bug ships unnoticed — the
    fix is to run `config:cache` (and `config:clear` before it, so stale keys don't survive a removed file) as a
    standard deploy step, not as an optional performance tweak reached for later.
18. **A command's signature encodes optionality and shape, not just a name.** `{name?}` is optional, `{name=default}`
    carries a default, `{name*}` collects every remaining argument into an array, and `{--option=}` versus
    `{--option}` is a value flag versus a boolean one — getting this wrong reads as a bug in argument parsing
    that is actually a bug in the signature string, and it fails at the point the command is *called*, not at
    the point it's defined, so it survives until someone hits the untested combination.
19. **A scheduled task's timezone follows the server unless the schedule states one.** `->timezone('...')` on the
    entry itself is the only way a task meant to run "at 9am for the business" survives a server in UTC or a DST
    change — the default silently drifts twice a year in a region that observes it, and nothing in the schedule
    definition says so unless it's stated per entry.
20. **Chain scheduled tasks with `->after()`/`->before()` rather than cramming both into one command's `handle()`.**
    A report that must run after an import finishes is two schedule entries with a declared dependency, not one
    command calling the other directly — the chain stays visible in `schedule:list`, and either step can still be
    run alone for a manual backfill.
21. **A command is tested by invoking it, not by extracting its logic into something else to unit-test.**
    `$this->artisan('command:name', [...])->assertExitCode(0)` (or `assertSuccessful()`/`assertFailed()`) runs the
    signature, the confirmation prompt handling and `handle()` together, which is the only way a broken argument
    binding or a confirmation the CI runner can't answer gets caught before it does in production — point 5
    already put the actual work in an action class precisely so this test can stay thin.
