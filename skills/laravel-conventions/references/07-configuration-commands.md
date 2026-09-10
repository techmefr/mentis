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
22. **`config()` cascades in the order files are loaded, and a key repeated across files silently keeps the
    last one loaded**, so two packages (or a package and the app) publishing the same top-level config key
    resolve to whichever loaded last rather than merging — the fix is a package-specific top-level key
    (`services.stripe`, not a bare `stripe`), never a shared namespace two independent config sources both
    write into.
23. **`Context` carries request-scoped or job-scoped data across the async boundary a plain variable
    cannot cross** — a request id that should appear in every log line for that request and then in the
    log lines of every job that request dispatched, without threading it through every function signature
    in between. It is not a substitute for an explicit parameter where the data is actually part of the
    method's contract; it earns its place specifically for cross-cutting metadata nothing in the call chain
    otherwise needs to know about.
24. **A command's exit code is part of its contract, not a detail of how it happened to end.** Returning
    `self::FAILURE` (or a non-zero int) from `handle()` on a condition an operator or a CI pipeline needs to
    react to is what makes `&&`-chaining the command in a deploy script or a cron wrapper mean something —
    a command that always returns `0` and instead prints an error string is a failure indistinguishable
    from success to anything that only checks the exit code, which is every scheduler and every shell.
25. **`artisan schedule:list` and `schedule:test` are how a scheduled entry gets verified before waiting
    for its actual cron minute** — `schedule:test` runs a named task on demand, `schedule:list` prints the
    resolved next-run time for every entry including its timezone and overlap policy (points 11, 19).
    Reading the source to mentally evaluate a cron expression is the slower and less reliable version of
    running the command that already does it.
26. **A command meant to run unattended in CI or a cron job never blocks on an interactive prompt** —
    `confirm()` without `--no-interaction` support, or a `ConfirmableTrait` check that can't be satisfied by
    a flag, hangs a pipeline until it times out. `$this->confirmToProceed()` already respects
    `--force` and the `APP_ENV` check point 9 asks for; a custom prompt built without checking
    `$this->option('no-interaction')` reinvents that check and usually forgets the non-interactive case.
27. **Environment-specific service configuration (mail driver, queue connection, cache store) is chosen by
    which `.env` value is set, never by an `if (app()->environment('production'))` branch inside application
    code.** The branch duplicates what the config layer already exists to centralise (point 1), and it is
    the one form of environment-awareness that survives being forgotten in a diff, because nothing fails
    locally to catch it — the code path for production only runs in production.
28. **Laravel Prompts replaces `$this->ask()`/`$this->choice()` for anything richer than a single line** —
    `search()` for a list too long to display, `suggest()` for an autocomplete over known values, `spin()` to
    show progress around a call that blocks. Point 26's non-interactive requirement still applies: every
    prompt has a `required`/`validate` option and falls back to a sane default or a hard failure under
    `--no-interaction`, rather than hanging a CI pipeline waiting for a terminal that isn't there.
29. **`Config::string()`, `Config::integer()` and `Config::boolean()` read a value with the type asserted at
    the point of use, instead of `config()` returning `mixed` for the caller to trust.** A boolean read from
    `.env` is a string (`"false"` is truthy) until something casts it — point 1 already routes that value
    through `config/*.php`, but the config file itself often just returns `env('FEATURE_X')` unchanged, and
    the typed accessor is what catches the value arriving as `"0"` instead of `false` before it reaches a
    conditional.
30. **`Schedule::job(...)` dispatches straight onto the queue; `Schedule::command(...)` spawns a whole new
    PHP process to run an artisan command.** For frequent, lightweight scheduled work the difference is real
    process overhead multiplied by how often the schedule fires — a job scheduled every minute costs one
    queue push; the equivalent command costs booting the framework every minute. Reach for `command()` when
    the work must run as a specific artisan command with its own signature and exit code (point 24), and
    `job()` when the schedule is just another way to dispatch the same job the rest of the app already uses.
31. **`php artisan about` reports the effective configuration Laravel is actually running with** — cached or
    not, which drivers are active, which environment file loaded — which is the fast way to confirm point
    17's `config:cache` actually ran in this environment instead of guessing from behaviour. `--only=environment`
    or `--json` narrows it to one section for a deploy script to assert against, rather than a human reading
    the full table over SSH.
32. **A command's output goes through `$this->components->info()/error()/task()/warn()`, not raw `echo` or
    `$this->line()` styled by hand.** These helpers (from `Illuminate\Console\Concerns\InteractsWithIO`) are
    what make one command's output look like every other artisan command's output — a `task()` block that
    reports its own success or failure without the caller writing the checkmark logic, and a consistent
    look across every command in the project rather than one bespoke formatting scheme per author.
33. **`route:cache` and `event:cache` are `config:cache`'s siblings, and they carry the same trap as point
    17: a closure-based route or a route depending on a controller callable that cannot be serialised breaks
    only once the cache is built**, which in most projects is the deploy pipeline, not a local machine. A
    project that runs `optimize` (which chains `config:cache`, `route:cache`, `event:cache` and the view
    cache) as one deploy step catches all three traps together instead of discovering them one deploy at a
    time as each cache is added later.
34. **A scheduled command's output can be captured without redirecting it by hand** — `->appendOutputTo($path)`
    or `->emailOutputTo($address)` on the schedule entry is where point 11's "somewhere for a failure to
    surface" becomes a concrete destination for a task that has no other logging of its own; `->emailOutputTo()`
    only sends when there is output at all by default, so a silent success and a silent failure both need
    `->emailOutputTo($address, andSendIfSuccessful: true)` if the goal is to hear from the task on every run,
    not only when it has something to say.
35. **`vendor:publish --tag=` publishes one package's config or migration files without also overwriting
    every other file that package could publish.** Running `vendor:publish` for a package bare re-publishes
    everything it offers, including files already customised locally, unless `--force` is withheld; `--tag`
    scopes the operation to exactly the group the task needs (`config`, `migrations`, `views`), which is the
    difference between "give me this package's config file to edit" and "silently overwrite the migration I
    already modified."
36. **`env()`'s boolean and null coercion only recognises specific string forms, and a value outside that set
    reaches the caller as the literal string.** `"true"`, `"(true)"`, `"false"`, `"(false)"`, `"null"` and
    `"(null)"` are coerced; `"1"` and `"0"` are not converted to booleans by `env()` itself, they arrive as
    strings — point 29's typed `Config::boolean()` accessor exists precisely because the config file often
    just forwards `env('FEATURE_X')` unchanged, and a `.env` value written as `1` instead of `true` silently
    stays truthy-as-a-non-empty-string rather than becoming an actual boolean anywhere before that accessor
    is reached.
37. **A long-running artisan command (a queue-like worker loop, a daemon reading from an external source)
    needs to react to `SIGTERM` deliberately, the same way point 10's batching already asks it to survive an
    interruption.** `$this->trap(SIGTERM, fn () => $this->shouldExit = true);` lets the loop finish its current
    unit of work and exit cleanly instead of being killed mid-write when the process manager restarts it on
    deploy — without it, the command dies at an arbitrary point in its loop, which is the same corrupted-state
    risk point 10 already names for a crash, just triggered by a deploy instead of an outage.
38. **`php artisan config:show <key>` inspects one resolved config key without dumping the whole tree**, which
    is the fast way to confirm a value actually resolved the way point 1 and point 22's cascade rules predict
    — `config:show database.connections.mysql` shows the merged result across every file and package that
    contributed to it, rather than reading each source file and mentally merging them, and it works whether
    or not the config is currently cached.
39. **`artisan db:seed --class=` runs one seeder in isolation, without re-running the `DatabaseSeeder`'s full
    chain** — the tool for populating just the reference data a single feature needs during development,
    separate from point 12's rule that the seeder itself stays idempotent regardless of how it's invoked. It
    is also what makes point 11's "ship the seed data in the same change" checkable on its own: running the
    new feature's seeder in isolation against a fresh database proves that seeder works without needing the
    whole `DatabaseSeeder` chain to succeed first.
40. **A command's class name and its artisan signature name are two different identifiers, and
    `make:command --command=` sets the second without touching the first.** `php artisan make:command
    SyncInventory --command=inventory:sync` produces a `SyncInventory` class whose `$signature` is
    `inventory:sync` — the class name follows point 5 of `skills/laravel-conventions` §1's naming rules for
    PHP classes, while the command name follows the project's own namespacing convention for artisan commands
    (a colon-separated domain prefix); conflating the two by naming the class after the desired CLI invocation
    produces a class name that reads like a terminal command instead of a PHP type.
41. **`Command::SUCCESS`, `Command::FAILURE` and `Command::INVALID` are three distinct exit codes, not two,
    and point 24's "exit code is part of the contract" means picking the right one.** `INVALID` (exit 2) is
    for a call the command itself rejects before doing any work — a bad argument combination the signature
    alone couldn't express — while `FAILURE` (exit 1) is for the work being attempted and not succeeding; a
    deploy script or cron wrapper that only checks "zero or not" loses that distinction, but a caller that
    branches on the specific code (retry on `FAILURE`, fix the invocation on `INVALID`) needs the command to
    return the one that actually happened, not `FAILURE` for both.
42. **`$this->artisan(...)->expectsQuestion($question, $answer)` scripts an interactive prompt's answer for a
    test, which is what point 21's "invoke the command, don't extract the logic" needs for any command that
    asks something.** A command using `$this->confirm()`/`$this->choice()` still needs those prompts satisfied
    under CI's non-interactive shell (point 26) — `expectsQuestion()` supplies the scripted answer so the test
    exercises the real prompt-handling code path instead of the command being refactored to skip prompting
    just to make it testable.
43. **`config()->array('key')`, alongside `Config::string()`/`Config::integer()`/`Config::boolean()` (point
    29), asserts a config value is actually an array before the caller indexes into it.** A config key meant
    to hold a list of allowed values that instead resolves to a scalar (a `.env` override collapsing what was
    meant to stay an array in `config/*.php`) fails at the point it's read with the typed accessor, instead of
    failing later at whatever `foreach` or `in_array()` call assumed the array shape and got a scalar instead.
44. **`optimize:clear` is the single command that reverses every cache `optimize` (point 33) built — config,
    route, event and view — and running only `config:clear` after changing a route closure leaves the stale
    route cache in place.** The two commands are not symmetric in scope: `optimize` bundles all four caches
    into one deploy step precisely so nothing is forgotten, but clearing has to be told to do the same, or a
    developer chasing point 17's "the trap only fires once cached" ends up clearing the one cache they
    suspect and missing the one that's actually stale.
45. **A local `.env.testing` overrides `.env` specifically for the test runner, and a project without one is
    running its test suite against whatever `.env` happens to hold** — a queue connection, a mail driver or a
    third-party key meant for local development, silently exercised by CI unless the test environment pins
    its own values. `phpunit.xml`'s `<php>` block sets the same keys inline as a second, equally valid place
    to pin them; either way the point is that "which config the tests run under" is a decision, not whatever
    `.env` happens to contain on the machine running them.
46. **`artisan make:command --test` scaffolds the test file alongside the command class in the same step**,
    which is the mechanical nudge for point 21's "a command is tested by invoking it" — a command generated
    without it is one keystroke away from being committed with no test at all, because writing the test file
    by hand from scratch is friction a generated stub removes. The stub still needs the actual prompt and
    exit-code assertions (points 21, 41, 42) filled in; the flag only saves creating the file in the right
    place with the right base class.
