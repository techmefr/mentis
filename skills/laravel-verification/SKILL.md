---
name: laravel-verification
description: "Use when a Laravel change is about to be declared done, merged or deployed: the ordered verification sequence for the stack (validate, format check, static analysis, tests, dependency audit, migration review, cache build, queue and scheduler checks), each phase read as an artefact and reported pass or fail."
---

# laravel-verification

The Laravel recipe for step 7 of the pipeline (`WORKFLOW.md`): what `gate` runs on this stack, in what order,
and what counts as a pass. `gate` owns the discipline (evidence read, never a claimed pass); this block owns
the content of the phases. Every command is the project's own, run read-only against the working tree; the
block names the check, and the project's scripts say how.

## When
After the code is written and before the review, before a merge request leaves draft, and once more before a
production deploy. Also after a dependency upgrade or a refactor that moves many files.

## Steps

Run the phases in order. A failed phase stops the sequence: a later phase on top of a broken one reports noise.
Each phase ends with its output **read**, not its exit status (`skills/gate`, step 5).

1. **Environment and manifest.** The runtime versions match the ones the project declares (the manifest's
   platform setting, the container image), the manifest validates, and the lock file is in sync with it. A
   lock file out of sync means the install resolves different versions from the ones tested.
2. **Formatting, check mode.** The formatter runs in its non-modifying mode and reports differences. The
   verification never rewrites files; a fix is a separate commit by the author.
3. **Static analysis.** The analyser at the project's configured level passes with **no new baseline entry**.
   A baseline that grew in this diff is a finding: the diff hid its errors instead of fixing them
   (`skills/laravel-conventions` §9).
4. **Tests.** The project's whole suite, parallel if the project runs it so (`skills/run-generated-tests` for
   the scoped runs during development). Read the summary: skipped and incomplete tests are listed with a
   reason or the pass is not a pass. The default state of a freshly written test is failure until its output
   was observed.
5. **Coverage and mutation, only if the project uses them.** Coverage runs on the CI job that reports it,
   with the fast driver for line coverage and the slower one only where branch or path coverage is wanted.
   The report is read for the untested failure branch of the diff. No percentage is imposed here. Mutation
   testing, where the project has it, runs on the changed files only, and each surviving mutant is either a
   missing assertion or an equivalent mutant stated as such.
6. **Dependency audit.** The package manager's audit reports no known advisory for the locked set; a finding
   names the package, the version range and the fix, and an abandoned package is reported as such. The audit
   changes with time, so a pass last month says nothing about today (`skills/security-hardening` §4).
7. **Database.** Run the pretend mode of the migrations and read the SQL (`skills/laravel-conventions` §13).
   Check each new migration against the safe-migration list, that `down()` is real or honestly absent, and
   that a fresh migrate-and-seed gives a populated working application. Never run a destructive or fresh
   migrate against a database that is not local and disposable.
8. **Cache build.** Build the configuration, route, event and view caches the way the deploy will, then clear
   them. A failure here is a closure route, an environment read outside configuration or a missing view that
   production would otherwise find first (`skills/laravel-conventions` §7, points 17 and 33).
9. **Queues, scheduler and failed work.** The scheduled task list shows what the diff added, overlap rules
   included. The failed-jobs list is empty or understood. If a supervisor dashboard is in use, its status is
   running. On a non-production environment only, dispatch a no-op job on a dedicated queue and process it
   once, then confirm its side effect; this proves a worker consumes the queue, which no unit test does.
10. **Production configuration, on the target.** For a deploy, the settings in `skills/laravel-conventions`
    §12 are asserted on the live environment, not read from the repository: debug off, the environment name,
    the drivers, the cookie flags, the trusted proxies and hosts, a 404 on the environment file.
11. **Diff sweep.** Over the changed lines only: leftover debugging calls, dumps and ray-style helpers, a
    committed environment file, a secret-shaped string, a new TODO, a test marked skipped, a lowered
    threshold, a loosened analyser rule. Each is a finding with the file and line.

## Output / checkpoint
One report: each phase named, pass or fail, and for a fail the first failing item with its file and line. The
verdict is pass only when every phase ran and passed; a phase that could not run (no database, no container
runtime) is reported as **not run**, which is not a pass. Feeds the `verified` checkpoint of `skills/gate`.

## Guardrails
- Read-only. This block verifies; it does not format, fix, migrate or install anything. A missing tool is
  named and the user installs it (`CONVENTIONS.md`: no block installs).
- Never claim a phase passed on the strength of an earlier run, a summary or a green badge: the output of
  this run, read now.
- A threshold lowered, a baseline grown, a test skipped or a rule loosened to make a phase pass is a failure
  of that phase, reported as one.
- The runtime (a local container wrapper, an in-container shell, a bare host) is detected, not guessed
  (`skills/laravel-conventions` §7); when two are plausible, ask.
- Production-targeting phases (10) are asserted by a person with access or by the deploy pipeline; this block
  does not reach into production on its own.

## Origin
Idea taken from the public ECC repository's Laravel verification skill (MIT licence, read 2026-10-02): an
ordered sequence from environment checks to queue checks. Rewritten in our terms: the phases are named by
the check and not by the tool's command line; the pass criterion is the read artefact, with "not run" as a
distinct outcome; baseline growth and lowered thresholds count as failures; no coverage percentage; the
detection of the runtime is the project's own rule, not a hard-coded wrapper; mutation testing and the
failed-work check are our additions. The queue health probe (a no-op job processed once, non-production
only) is the same idea in the source, kept with its restriction. The facts about what each artisan command
does come from the framework documentation, written from knowledge of it and not re-fetched on the day.
