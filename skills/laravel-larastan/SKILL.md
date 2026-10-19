---
name: laravel-larastan
description: "Use when configuring Larastan or reading its findings in a Laravel app: which of its rules are on by default and which to opt into, how model properties are inferred from migrations, how to type builders, factories and collections so the analyser understands them, and how to handle a baseline or an ignore without hiding a real defect."
---

# laravel-larastan

Step 7 (`gate`) of the pipeline (`WORKFLOW.md`), and the typing side of step 6. `skills/laravel-conventions` §9
says that static analysis runs and that a baseline only shrinks; this block is the detail underneath:
the rule catalogue, the settings that change what the analyser can see, and the ways to feed it types.

**Special status.** New block, 🟡: written from the Larastan repository's own documentation at its 3.x line,
never run on real work in house. Parameter names and defaults are version facts: re-read `docs/rules.md` and
`docs/custom-config-parameters.md` of the pinned version before changing a setting (`skills/source-freshness`).

## When
A `phpstan.neon` is created or edited, a Larastan error needs a decision (fix, type, ignore, baseline), or new
Eloquent code (a builder, a factory, a custom collection, an accessor) is written.

## Steps
1. **Know what it is.** An extension for PHPStan that boots the application's container to resolve types only
   knowable at runtime, so it executes some of your code at analysis time. The matrix at the 2026-10-02 reading:
   the 3.x line needs PHP 8.2+ and Laravel 11.15+ (the matrix says 11.16+ for the line); older Laravel stays on
   older majors. The operator installs it as a dev dependency and includes its extension file in the PHPStan
   config; this block installs nothing.
2. **Default rules are on for a reason; do not switch them off to make an error go away.** At the reading:
   `Model::make()` (needless double instantiation, use `new`), collection calls that could have been queries
   (`all()->count()`, a `pluck()->contains()` that is an `exists()`), `env()` outside the config directory
   (it returns null when config is cached), `$appends` entries that are not computed properties, the relation
   existence check on `has`, `whereHas`, `with`, `load`, `withCount` and the like (not optional), dispatch
   argument types against the job constructor, useless `value()` and `with()` calls, and a deferrable provider
   missing `provides()`.
3. **Opt into the rules that catch real production defects.** Disabled by default at the reading, each behind a
   named parameter: model property names in methods that take one (typos in `create([...])`), unique jobs
   that do not declare a lock lifetime or an id for a parameterised job, unique jobs dispatched through
   batches or bulk, queued jobs holding a model in a public property without the model-serialising trait,
   batched jobs missing the batch trait, batchable jobs that never check cancellation, and a job dispatched
   inside a transaction without deferring to commit (`skills/laravel-dispatch-after-commit`). Enable them one
   at a time and fix or baseline the first run, deliberately.
4. **Opt-in rules with a stated false-positive risk stay a choice.** Unused views and missing translations
   can misreport (dynamic usage, translations in a database); the Octane compatibility check is for apps that
   run on it; the implicit builder-call rule enforces `Model::query()->where()` over `Model::where()`.
   Turn them on when the team decided, not as a default.
5. **Help the analyser see the schema.** It reads model properties from migrations (and squashed schema
   dumps). Migrations in non-default places need `databaseMigrationsPath`; conditional migration code is
   assumed to evaluate true; PostgreSQL schema dumps parse poorly with the default parser, so either use a
   parser the docs name or generate migrations it can read. Casts defined through a method body are only
   inferred when `parseModelCastsMethod` is on, at a speed cost.
6. **Type the Eloquent extension points.** A custom builder (the model uses the builder trait, declares the
   builder class), a factory whose generic template is the model and which the model names, and a custom
   collection with its generic type give the analyser what it needs; the docs say custom builders analyse
   better than model scopes. An attribute accessor needs its generic return type. Where a project forbids
   scopes (`skills/laravel-no-fat-models`), the builder is the typed alternative.
7. **Choose the level and hold it.** The sample config starts at level 5 on a ten-level scale; raise it as
   the codebase allows, never lower it to pass. A raise is its own change.
8. **An ignore is a reviewed decision.** Prefer fixing, then a PHPDoc type, then a narrow ignore with the
   error identifier and a reason (`skills/code-baseline` §8 point 13). Blanket line ignores and loose regexes
   hide the next real error of the same shape. The one documented error to ignore is a higher-order message on a
   plain support collection; anything else is investigated first.
9. **A baseline freezes the past, not the future.** Generate it once for a legacy codebase; the diff must not
   add entries (`skills/laravel-verification`). A memory-limit failure is fixed with the memory option, not by
   narrowing the analysed paths.

## Output / checkpoint
Analysis passes at the project's level with no new baseline entry and no new ignore without a reason; each
enabled optional rule is named in the config with the decision that enabled it. Checked at `gate` (7).

## Guardrails
No comments in the code produced. Do not edit the baseline to hide a finding the diff introduced. A rule
turned off to make a build green is reported, not applied.

## Origin
Rewritten from the Larastan repository documentation (`larastan/larastan`, MIT, cloned 2026-10-02, 3.x line):
the README (requirements, support matrix, config skeleton, ignoring and baseline), `docs/rules.md` (rule
catalogue with defaults and parameters), `docs/custom-config-parameters.md`, `docs/features.md` (builders,
factories, collections, accessors) and `docs/errors-to-ignore.md`. Mechanisms only, rewritten in our words.
Version-sensitive: rule names, parameter names and defaults.
