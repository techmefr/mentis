# flaky-test-triage-pitfalls §1 — Classify, then reproduce

A flaky test has one of a handful of causes, and the fix for one makes another worse: a sleep added to a data
collision slows the test and leaves it flaky. Name the class first, reproduce the failure second, fix third.

## 1.1 Classes of flake
The classes below are the qa-skills `test-reliability` taxonomy (an author's classification, not a standard).

| Class | Signal | Usual cause | Fix direction |
|---|---|---|---|
| Timing | timeout errors, passes on retry, worse in CI | a race, an animation, an async step not awaited | wait for the condition, not the time (`testing-anti-patterns` §3) |
| Data dependency | fails with other tests, passes alone | shared state, missing cleanup | isolate per test, clean in a fixture |
| Order dependency | fails under sharding or full parallelism | relies on another test's side effect | make setup self-contained |
| Environment | one runner, correlates with load | resource contention, network latency | stub externals, give the runner more room |
| Time sensitivity | fails at midnight, month end, in one timezone | the real clock, a date boundary | fix the clock, compare relatively |
| Visual rendering | a screenshot diff that flickers | fonts, antialiasing, an animation frame | mask dynamic regions, compare in one environment |
| External service | correlates with a third party's status | real HTTP calls in tests | stub the external API |

1. **Currents groups the same causes into four**: UI-driven, environment-driven, data or parallelism-driven, and
   test-suite-driven (state leaks, shared fixtures, order). The groupings overlap; pick one vocabulary per project
   and write the class in the fix's message.
2. **Write the class before the fix.** Own guidance: a fix with no class in its commit message is a guess.

## 1.2 The questions that tell them apart
1. **Does it pass when run alone?** Yes: order or data dependency. If another test creates what this one needs,
   it is order; if both touch a database, a file or a cache, it is data (qa-skills).
2. **Does it fail more often in CI than locally?** Timeout errors point to timing, connection errors to the
   environment, out-of-memory or disk errors to resource contention (qa-skills).
3. **Does it fail near a specific time?** Midnight is a date boundary, month or year end a calendar calculation, a
   particular hour a timezone (qa-skills).
4. **Does it compare screenshots? Does it call external HTTP APIs?** Visual rendering and external service
   respectively; with none of the above, timing is the default classification, and the question is which async step
   is not awaited (qa-skills).
5. **Currents asks different questions first**: does it fail locally too (timing or async), only with several
   workers (data isolation), only after specific tests (state leak), or randomly (an external dependency).
   The two trees start from different questions and disagree on the first one; treat both as heuristics and let
   the reproduction in §1.3 decide.

## 1.3 Reproduce before changing anything
1. **Repeat the test**: Playwright's `--repeat-each` runs each test many times; Currents uses 20 to confirm
   instability, `--workers=1` to separate parallelism problems, and `CI=true` to run in CI-like conditions
   (Currents). qa-skills adds `--workers=4` and a trace, and says the test must fail at least once before any fix is
   trusted. In another runner, the same is a loop of N runs; the counts are examples.
2. **After the fix, run many more**: qa-skills requires 50 of 50 passes, in CI conditions too; Currents runs a new
   test 50 times before merging it and adds parallel workers to expose races. These are one source's numbers.
3. **Reproduce under CI-like conditions** when it only fails in CI: headless, the same environment variable, the CI
   container image and a limited CPU (Currents). Slower CPUs, cold browser starts, shared runners and network
   latency are the listed causes of CI-only failures (Currents).
4. **Capture evidence on the failing run**: a trace on first retry, console messages, failed requests and slow
   requests (Currents). Trace settings are in `playwright-e2e-pitfalls` §3.
5. **Own guidance:** when the test only fails in CI, change one condition at a time (workers, CPU, image) and record which
   one made it fail; the cause is the difference.

## 1.4 A replayable random seed in pytest
1. **`pytest-randomly` shuffles tests by module, then by class, then by function**, prints a base seed at the
   start of the run, and accepts it back with `--randomly-seed` to repeat a failure caused by order or random data
   (`pytest-randomly` README, version 5.0.0).
2. **`--randomly-seed=last` reuses the previous run's seed**, which works only if pytest's cache provider plugin is
   not disabled.
3. **Find a polluting test by narrowing**: because the order is by module then class, rerun the same seed against
   the failing module, then the failing class, to find the bad interaction.
4. **The plugin resets `random.seed()` before each test's setup, run and teardown** to a value derived from the base
   seed, the test id and the phase, so each test gets a different but repeatable seed. It also resets, when
   installed, factory boy, Faker, Model Bakery, NumPy's legacy random state and Polyfactory's default generator,
   and another generator can register through the `pytest_randomly.random_seeder` entry point.
5. **Consequence for fixing**: randomised data stays repeatable only because the seed is reset per test, so on a
   failure fix the seed (replay it), not the data; a test that passes only with one specific value was not
   specifying the data it needs, which is what the random values are there to expose.
6. **Turn parts off by flag, not by deleting the plugin**: `--randomly-dont-reorganize` keeps the order,
   `--randomly-dont-reset-seed` keeps the global seed; `-p no:randomly` disables it altogether. Tests that must run
   in a fixed order use the `pytest-order` plugin.
7. **The README cites research that dependent tests exist in practice** and that random order detects them.
8. **Node and other stacks:** the Node random-order and shared-data hygiene is in `prisma-ops-and-test-hygiene` §2.

## 1.5 Environment before blame
1. **When an action fails in CI, check backend health before blaming the test.** qa-skills hits a health
   endpoint: a 5xx or a timeout means an environment problem, a healthy backend means a real failure, and only the
   second is retried or fixed in the test.
2. **Its resource-contention checks use thresholds of its own**: loading a blank page over about 2 seconds, a health
   call over about 5 seconds, against baselines of about half a second and 1 second. These are the author's numbers; measure your own
   baseline.
3. **Own caveat:** the source suggests not counting contention failures toward the flake rate. Record them anyway, with
   the class "environment", so a runner that is always overloaded shows up as a runner problem.
4. **Time-sensitive tests** fix the clock and compare relative values instead of reading the real time
   (qa-skills table). No clock API page was read, so the way to fix the clock is the runner's own.
