# laravel-conventions §7 — Configuration and commands

> Section 7 of `skills/laravel-conventions`. Read it when `config/`, `env()`, an artisan command, a seeder or a factory. The other sections and the guardrails stay in `SKILL.md`.

1. **Config file names and keys follow one casing convention; every value is read through the config
   layer**, never `env()` reached into from business code — outside config files, `env()` returns null once
   the config is cached. Local development usually has no cached config, so the code works where it was written
   and returns null in production, on the deploy that cached it — no error, the setting just reads empty.
2. **Third-party credentials and service settings live in config with an env-backed default**, never inline
   in the class that calls the API. That makes the same class usable in a test with a fake endpoint, and
   keeps the value out of the diff.
3. **A secret never enters the repository.** `.env` is not committed and `.env.example` documents the key
   with an empty or obviously-fake value. A secret committed once is compromised even after removal: it stays in the history — rotate
   the credential, then clean up.
4. **A config file is data, not code.** No closure, no query, no service resolution inside it: the whole
   set of config files is serialised when the config is cached, and the framework source throws a
   `LogicException` ("could not be serialized ... non-serializable") for a value that cannot be, which
   surfaces in the deploy that runs `config:cache` rather than locally. [laravel/framework 12.x
   `ConfigCacheCommand.php`, read 2026-10-21.]
5. **A console command declares an explicit signature and description**; the class does the wiring, an
   action class does the work — a command whose `handle()` holds the logic can only be run from a terminal,
   so it cannot be scheduled, queued, tested or called from a controller without copying it.
6. **A console command earns its place by being run more than once** — on a schedule, or on demand as a
   repeatable operation. A one-off **data** change (backfill a column, correct bad rows, reshape a table)
   belongs in a migration, where it is versioned, ordered against the schema it depends on, and replayed on
   every environment by the same mechanism. A one-off inspection or a single outbound action belongs in a
   REPL snippet with nothing committed. A run-once command that ships is dead code once run, and every
   later reader must decide whether it is safe to run again.
7. **A command that changes data is idempotent, or it refuses to run twice.** Someone will run it again —
   after a timeout, a failed deploy, or scrolled-past output. Make the second run a no-op by keying on
   state rather than on the fact that it has not happened yet.
8. **A command reports what it did, in counts.** "Done" is indistinguishable from a no-op, so a command
   that processed zero rows because its filter was wrong looks like a success. Print the number
   examined, the number changed and the number skipped.
9. **A destructive command asks, and prefers a dry run.** Require an explicit confirmation in production,
   and where the work can be previewed, make the preview the default and the mutation the flag. Its
   arguments are validated as strictly as a request payload — only staff reaching it makes mistakes
   fewer, not smaller.
10. **A long-running command works in batches and survives interruption.** Resume from state recorded in
    the database, not from a position in a loop, because the loop's position dies with the process. Batching
    also keeps the memory flat and lets the work stop cleanly on deploy.
11. **A scheduled command declares its overlap policy and its failure visibility.** Without
    `withoutOverlapping`, a run that takes longer than its interval competes with itself; without
    somewhere for a failure to surface, a nightly task can stop working for weeks and the first signal is a
    business number that stopped moving.
12. **A seeder carries the reference data the application needs to run, and it is idempotent.** Upsert by a
    natural key rather than inserting: a seeder that duplicates its rows on the second run makes a fresh
    environment unreproducible, and reproducing an environment is the point of committing it.
13. **A factory is for tests and local development, never for production data.** It defines the valid
    minimum, with named states for the variants that matter — defaults describing the happy path push every
    test into asserting the same shape, and the interesting cases get rebuilt by hand in each test.
14. **A data backfill inside a migration is written against the schema, not against the model.** The
    model will change — a renamed attribute, a new cast, a global scope, an accessor — and the old
    migration then breaks or silently writes the wrong thing on a fresh database. Use raw queries or the
    query builder, true to the columns that existed when it was written.
15. **Run the command rather than writing it out** for the user to copy, when a runtime is available. A
    command described but never executed is an untested claim (`WORKFLOW.md`, the default-is-failure
    guarantee).
16. **`Isolatable` is point 11's overlap policy for a command started outside the scheduler, but it is opt-in per
    invocation.** The docs: marking a command `Isolatable` makes a `--isolated` option available, and only a
    run started with that option takes an atomic lock in the default cache driver (memcached, redis,
    dynamodb, database, file or array, shared by all servers) and refuses to run when another instance holds
    it; an exit status for the refused run can be passed through the option. `withoutOverlapping` guards the
    scheduled entry only, so a manual or webhook-fired start needs `--isolated` too. The lock key defaults to
    the command's name, so runs with different arguments block each other unless `isolatableId()` folds an
    argument into the key. [Laravel Artisan docs 12.x, "Isolatable Commands", read 2026-10-21.]
17. **`config:cache` freezes every config file into one array, and that is when point 1's `env()`-outside-config
    trap fires in production.** Running it locally would surface the bug at once; running it only in the
    deploy pipeline ships it unnoticed. The docs recommend `optimize` (config, events, routes and views) as
    part of the deployment, so run the cache step in a rehearsal as well. [Laravel deployment docs 12.x,
    "Optimization", read 2026-10-21.]
18. **A command's signature encodes optionality and shape, not just a name.** `{name?}` is optional, `{name=default}`
    carries a default, `{name*}` collects every remaining argument into an array, and `{--option=}` versus
    `{--option}` is a value flag versus a boolean one — a mistake fails when the command is *called*, not defined, and survives until someone hits the
    untested combination.
19. **A scheduled task's timezone is a stated setting, and daylight saving time makes it risky.** The docs let
    you set `->timezone('...')` on one entry, or `schedule_timezone` in the `app` config for every entry; they
    warn that when daylight saving changes a task may run twice or not at all, and recommend avoiding timezone
    scheduling when possible. A task meant to run "at 9am for the business" therefore states its timezone
    and avoids the hours around the change. The docs read do not say which timezone applies when none is
    set. [Laravel scheduling docs 12.x, "Timezones", read 2026-10-21.]
20. **Do not cram two scheduled steps into one command's `handle()`; give each its own entry and know how entries
    are ordered.** The docs say tasks due at the same time run one after another in the order they are
    defined, and that `runInBackground()` (for `command` and `exec` entries only) lets them run together,
    which removes that ordering. `before()` and `after()` run code around a single task, and `onSuccess()`
    and `onFailure()` react to its exit code; none of them declares a dependency between two entries.
    Own guidance: a step that must wait for another's result should not rely on definition order alone, and
    should not be backgrounded. [Laravel scheduling docs 12.x, "Running Tasks in the Background", "Task
    Hooks", read 2026-10-21.]
21. **A command is tested by invoking it, not by extracting its logic into something else to unit-test.**
    `$this->artisan('command:name', [...])->assertExitCode(0)` (or `assertSuccessful()`/`assertFailed()`) runs the
    signature, the confirmation prompt handling and `handle()` together, the only way a broken argument
    binding or a confirmation the CI runner can't answer gets caught before production — point 5 put the
    actual work in an action class so this test can stay thin.
22. **A package merges its config defaults into the application's copy one level deep.** The docs say
    `mergeConfigFrom` lets users override only the options they want in the published copy, and that it merges
    only the first level of the array: a partly defined multi-dimensional array does not get its missing
    options filled in. So a nested option a package needs must be fully defined in the application copy, and
    a package should use its own top-level key (`services.stripe`, not a bare `stripe`) rather than a
    shared namespace. [Laravel package development docs 12.x, "Default Package Configuration", read
    2026-10-21.]
23. **`Context` carries request-scoped or job-scoped data across the async boundary a plain variable
    cannot cross** — a request id that should appear in every log line for that request and then in the
    log lines of every job it dispatched, without threading it through every function signature in between.
    It is not a substitute for an explicit parameter where the data is part of the method's contract.
24. **A command's exit code is part of its contract, not a detail of how it happened to end.** Returning
    `self::FAILURE` (or a non-zero int) from `handle()` on a condition an operator or a CI pipeline needs to
    react to is what makes `&&`-chaining the command in a deploy script or a cron wrapper mean something —
    a command that always returns `0` and prints an error string is indistinguishable from success to
    anything checking the exit code, which is every scheduler and every shell.
25. **`schedule:list` and `schedule:test` check a scheduled entry before waiting for its cron minute.**
    The docs describe `schedule:list` as an overview of the tasks and the next time each runs; `schedule:test
    --name=` (in the framework source) runs one scheduled command on demand. Reading a cron expression by eye
    is slower and less reliable. [Laravel scheduling docs 12.x; framework source `ScheduleTestCommand.php`,
    read 2026-10-21.]
26. **A command meant to run unattended in CI or a cron job never depends on an interactive answer.**
    `$this->confirmToProceed()` asks only in production and is satisfied by `--force` (framework source,
    `ConfirmableTrait`), so it suits point 9's destructive command; a custom prompt needs its own
    non-interactive path (own guidance: a default or a hard failure), or it reinvents that check and forgets
    the unattended case. [laravel/framework 12.x `ConfirmableTrait.php`, read 2026-10-21.]
27. **Environment-specific service configuration (mail driver, queue connection, cache store) is chosen by
    which `.env` value is set, never by an `if (app()->environment('production'))` branch inside application
    code.** The branch duplicates the config layer (point 1), and nothing fails locally — the production path
    only runs in production.
28. **Laravel Prompts replaces `$this->ask()`/`$this->choice()` for anything richer than a single line** —
    `search()` for a list too long to display, `suggest()` for an autocomplete over known values, `spin()` to
    show progress around a blocking call. Point 26 still applies: every prompt has a `required`/`validate`
    option and falls back to a sane default or a hard failure under `--no-interaction`, rather than
    hanging a CI pipeline waiting for a terminal.
29. **`Config::string()`, `Config::integer()` and `Config::boolean()` read a value with the type asserted at
    the point of use, instead of `config()` returning `mixed` for the caller to trust.** A boolean read from
    `.env` is a string (`"false"` is truthy) until something casts it — point 1 routes the value through
    `config/*.php`, but the config file often just returns `env('FEATURE_X')` unchanged, and the typed
    accessor catches `"0"` arriving instead of `false` before it reaches a conditional.
30. **`Schedule::job(...)` dispatches straight onto the queue; `Schedule::command(...)` spawns a whole new
    PHP process to run an artisan command.** For frequent, lightweight work a job every minute costs one queue push; the equivalent command boots
    the framework every minute. Use `command()` when the work must run as a
    specific artisan command with its own signature and exit code (point 24), and `job()` when the schedule
    is just another way to dispatch a job the app already uses.
31. **`php artisan about` reports the application's environment, cache and driver state in one place** — the
    fast way to confirm point 17's `config:cache` actually ran in this environment instead of guessing from
    behaviour. `--only=environment` narrows it to one section. [Laravel configuration docs 12.x, read
    2026-10-21.]
32. **A command's output goes through `$this->components->info()/error()/task()/warn()`, not raw `echo` or
    `$this->line()` styled by hand.** These helpers (from `Illuminate\Console\Concerns\InteractsWithIO`) make
    one command's output look like every other artisan command's — a `task()` block reports its own success
    or failure without checkmark logic — instead of one bespoke format per author.
33. **`optimize` is the deploy step that builds the caches, and each of them has the same "only fires once
    cached" shape as point 17.** The framework source and docs agree that it chains `config:cache`,
    `event:cache`, `route:cache` and `view:cache`; the docs recommend running it as part of the deployment and
    `route:cache` for an application with many routes. Running it in a rehearsal catches a cache that fails to
    build before the deploy does. [Laravel deployment docs 12.x, "Optimization"; framework source
    `OptimizeCommand.php`, read 2026-10-21.]
34. **A scheduled command's output can be captured without redirecting it by hand.** The docs list
    `sendOutputTo($path)` (overwrite), `appendOutputTo($path)`, `emailOutputTo($address)` and
    `emailOutputOnFailure($address)` (only on a non-zero exit code); they exist only for `command` and `exec`
    entries, and mail needs the mail services configured. This is where point 11's "somewhere for a failure to
    surface" becomes a concrete destination for a task with no other logging. [Laravel scheduling docs 12.x,
    "Task Output", read 2026-10-21.]
35. **`vendor:publish --tag=` publishes one group of a package's files.** A package registers its publishable
    files under tags of its own naming (the package docs show separate tags for config, migrations and
    assets), so the tag scopes the publish to the group you need, and `--force` is the explicit overwrite:
    the docs use `--tag=public --force` for assets that are meant to be overwritten each time. Do not add
    `--force` to a config or migration you have already modified. [Laravel package development docs 12.x,
    "Publishing File Groups", read 2026-10-21.]
36. **`env()` converts only a few string forms, and any other value reaches the caller as the literal
    string.** In the framework source `"true"`, `"(true)"`, `"false"`, `"(false)"`, `"empty"`, `"(empty)"`,
    `"null"` and `"(null)"` are converted; `"1"` and `"0"` are not, they arrive as strings. Point 29's typed
    `Config::boolean()` exists because the config file often just forwards `env('FEATURE_X')`: a `.env` value
    written as `1` instead of `true` stays a non-empty string until that accessor is reached. [laravel/framework
    12.x `Env.php`, read 2026-10-21.]
37. **A long-running artisan command (a queue-like worker loop, a daemon reading from an external source)
    needs to react to `SIGTERM` deliberately, as point 10's batching asks it to survive an
    interruption.** `$this->trap(SIGTERM, fn () => $this->shouldExit = true);` lets the loop finish its current
    unit of work and exit cleanly instead of being killed mid-write when the process manager restarts it on
    deploy — otherwise it dies at an arbitrary point, point 10's corrupted-state risk.
38. **`php artisan config:show <file>` shows one config file's resolved values without dumping the whole tree**,
    the fast way to confirm a value resolved as point 1 and point 22 predict: `config:show database` prints
    the merged result of the file the application and its packages contributed to. [Laravel configuration
    docs 12.x, read 2026-10-21.]
39. **`artisan db:seed --class=` runs one seeder in isolation, without re-running the `DatabaseSeeder`'s full
    chain** — the tool for populating just the reference data a single feature needs during development,
    separate from point 12's rule that the seeder stays idempotent however it's invoked. It also makes
    §9 point 11's "ship the seed data in the same change" checkable: run the new seeder alone against a fresh
    database.
40. **A command's class name and its artisan signature name are two different identifiers, and
    `make:command --command=` sets the second.** `php artisan make:command SyncInventory
    --command=inventory:sync` produces a `SyncInventory` class whose signature is `inventory:sync`; without the
    option the framework derives `app:` plus the kebab-cased class name. The class name follows PHP naming,
    the command name the project's artisan namespacing convention (a colon-separated domain prefix).
    [laravel/framework 12.x `ConsoleMakeCommand.php`, read 2026-10-21.]
41. **`Command::SUCCESS`, `Command::FAILURE` and `Command::INVALID` are three distinct exit codes, not two,
    and point 24's "exit code is part of the contract" means picking the right one.** `INVALID` (exit 2) is
    for a call the command itself rejects before doing any work — a bad argument combination the signature
    alone couldn't express — while `FAILURE` (exit 1) is for the work being attempted and not succeeding; a
    caller branching on the specific code (retry on `FAILURE`, fix the invocation on `INVALID`) needs the
    command to return the one that actually happened, not `FAILURE` for both.
42. **`$this->artisan(...)->expectsQuestion($question, $answer)` scripts an interactive prompt's answer for a
    test, which is what point 21's "invoke the command, don't extract the logic" needs for any command that
    asks something.** `expectsQuestion()` supplies the scripted answer so the test exercises the real prompt-handling path
    (point 26) instead of the command being refactored to skip prompting.
43. **`config()->array('key')`, alongside `Config::string()`/`Config::integer()`/`Config::boolean()` (point
    29), asserts a config value is actually an array before the caller indexes into it.** A config key meant
    to hold a list that instead resolves to a scalar (a `.env` override collapsing what was meant to stay an
    array in `config/*.php`) fails at the point it's read, instead of later at whatever `foreach` or
    `in_array()` assumed the array shape.
44. **`optimize:clear` reverses what `optimize` built, and it also empties the default cache store.** The docs
    say it removes the cache files `optimize` generated as well as all keys in the default cache driver; the
    source runs `config:clear`, `cache:clear`, `clear-compiled`, `event:clear`, `route:clear` and
    `view:clear`. Running only `config:clear` after changing a route leaves the stale route cache in place,
    and running `optimize:clear` in production drops cached application data too. [Laravel deployment docs 12.x;
    framework source `OptimizeClearCommand.php`, read 2026-10-21.]
45. **A local `.env.testing` overrides `.env` specifically for the test runner, and a project without one is
    running its test suite against whatever `.env` happens to hold** — a queue connection, a mail driver or a
    third-party key meant for local development, silently exercised by CI unless the test environment pins
    its own values. `phpunit.xml`'s `<php>` block sets the same keys inline as a second valid place to pin
    them; either way "which config the tests run under" is a decision, not whatever `.env` contains.
46. **`artisan make:command --test` scaffolds the test file alongside the command class in the same step**
    (`--pest` and `--phpunit` pick the style), the mechanical nudge for point 21's "a command is tested by
    invoking it". The stub still needs the prompt and exit-code assertions (points 21, 41, 42) filled in.
    [laravel/framework 12.x `CreatesMatchingTest.php`, read 2026-10-21.]
47. **A factory's `definition()` maps each attribute to one Faker call; the moment an attribute needs logic
    to produce its value, that logic belongs in a Faker provider, not in the factory.** `'reference' =>
    'CMD-'.str_pad((string) random_int(1, 999999), 6, '0', STR_PAD_LEFT)` is a generator hiding inside a
    column list; `$faker->unique()->orderReference()` reads as a column-to-generator map because it is one.
    `unique()`, `nullable()` and a regex constraint only wrap a real generator call, not an inline
    string, so a factory building its own reference ends up writing its own collision-retry loop and its
    own `rand(0, 1) ? null : …`.
48. **`Faker\Provider\Base` is the extension point, registered once through `$faker->addProvider(new
    ...)` in a service provider's `boot()`, never called from inside a factory, a seeder or a test.**
    Point 2 of `skills/laravel-conventions` §1 already forbids a lifecycle closure doing this kind of
    one-time setup from anywhere but a provider; a factory registering its own provider in every
    `definition()` call re-registers it on every row, and a test registering one in `setUp()` leaks it
    into every later test in the same process, asked for or not.
49. **Every public method on a provider becomes a generator Faker exposes** — `$faker->yourMethod()` —
    so a provider's own helper methods that aren't meant to be called that way stay `private` or
    `protected`. Name the provider and its methods after the project's own domain
    (`OrderReferenceProvider::orderReference()`) rather than a generic concept, to avoid the one real
    collision risk: a provider registered twice, or two providers exposing the same method name, silently
    lets the last registration win until the wrong generator answers.
50. **Reach for a locale or a community `fakerphp/faker` extension before writing a project provider.**
    `fakerphp/faker`'s own locale packages already carry realistic company names, VAT-style business
    identifiers and addresses for most locales; a hand-rolled string that merely *looks* plausible (a
    fourteen-digit number where the real format carries a check digit) is a fixture the validation rules
    the application ships elsewhere would reject, and rots silently because nothing re-checks a factory
    value against those rules.
51. **A seeder consumes the same generators a factory does, and inline generation is not a fallback for
    either of them.** Point 12's idempotent-upsert rule and this point are independent: a seeder falling
    back to `'reference' => 'INV-'.Str::random(8)` when no provider covers the value reintroduces point 47's
    problem one call site removed — the value still needs a name, a place to live, and a way to be made
    unique that a bare string literal cannot give it.
52. **In a layer-package (OSDD-style) project, there is no `config/` at the project root** — each
   layer carries its own, including its overrides of third-party packages, loaded before providers
   register. See `skills/laravel-layer-owned-config` for the load-order trap this creates (an override
   posted from a provider's `register()` arrives after the package already read its own settings, and
   is dropped with no error) and the test that catches it.
