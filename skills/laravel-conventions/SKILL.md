---
name: laravel-conventions
description: Use when writing or reviewing Laravel, thin models and where behaviour goes, events over observers, permissions not roles, no magic strings or DB enums, no queries in loops, relation accessors and OrFail fetches, validation and FormRequests, typing and docblocks, naming, config, seeders and factories, soft deletes with pruning, queued job ordering, translations and no markup in PHP, REST routing and CRUD shape, testing tiers, and static analysis. The framework layer above php-patterns. Self-contained, it assumes no plugin or catalogue installed.
---

# laravel-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Laravel code. Sits **above**
`skills/php-patterns` (which stays on the language: typing, error handling, OOP) and below the review agent
for the stack. Every rule holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A).

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue for this stack, it
is the authority on **its** house style — its approved package list, its architecture scaffold, its
broadcaster, its MCP tooling — and overrides this block wherever the two differ. The rules below are the
generic form, with the internal package and product names removed (rule C).

## When
As soon as a controller, model, migration, job, listener, policy, FormRequest, command, seeder or factory is
written or modified, during `code` (6) or `tdd` (5).

## Steps

### 1. Where behaviour lives
1. **Keep models thin.** A model holds `$fillable`, `$casts`, relationships, simple scopes, trivial computed
   accessors over its own attributes, and lifecycle traits. Business logic, orchestration and anything
   reaching another aggregate go in an action/service. A fat model is the class everything imports and nobody
   can change.
2. **Events + listeners, never model observers**, for reacting to lifecycle changes. An observer is invisible
   at the call site: something saves a row and unrelated code runs, with no trace in the flow being read.
   Listeners are registered explicitly.
3. Reusable cross-cutting model behaviour (historisation, auditing, snapshotting) goes in a trait the model
   **opts into**, shaped like the framework's own (`SoftDeletes`): the model declares what it tracks. A base
   class inherited by everything makes the behaviour mandatory and untestable in isolation.
4. **No markup in PHP.** A service, action, accessor, controller or job never builds HTML — no tags, no inline
   styles, no concatenated `<span>`. Markup belongs in the view layer; a backend class returns data.
5. **The application owns its domain.** When integrating an external system (payment provider, CRM, ERP), the
   app remains the central source of functional knowledge — it doesn't become a thin proxy whose rules live in
   someone else's product and whose behaviour changes without a deploy.

### 2. Authorisation
1. **Never check a role name in code** — no `hasRole('admin')`, no `@role('manager')`. Check a **permission**
   (`can()`, a policy method, a gate). A role is a bundle of permissions that changes with the business; a
   role name in code is a deploy every time it does.
2. **Permissions are access rights only**: who may create/update/delete, and which parts of the app they
   reach. A permission must never stand in for what a user *is* or for a business capability — that's a
   domain attribute, not an access right. This one is subtle and worth naming: reusing the permission system
   as a feature flag makes the access model unauditable.
3. Authorisation is declared where the entry point is (policy on the resource, check on the action), not
   assumed from the fact that the caller was already authenticated.

### 3. Data model and schema
1. **No DB-level ENUM column.** Values become a schema migration to change, differ per engine, and can't
   carry behaviour. Use a string/int column typed by a PHP enum on the model.
2. **An enum with per-case data puts the value on the enum as a method**, not in a `match` scattered across
   callers. A `match` on an enum case returning a rate, a label or a threshold is behaviour that belongs to
   the enum — otherwise the day a case is added, the compiler helps you in one file and not in the other six.
3. **No cascade delete at the database level**: the DB bypasses the ORM, so lifecycle events and listeners
   never fire on child rows. Decide the deletion policy in the application layer, where the hooks live — and
   decide it at the schema/ERD stage, not when the first orphan appears.
4. **Don't factorise two concepts into one table** just because they look alike or share columns today. The
   shared table is cheap now and is the thing you can't unpick later, when one side grows a rule the other
   can't have.
5. Every model using soft deletes also carries a **pruning policy** with a retention window. Soft deletes
   without pruning is an unbounded table that silently becomes the biggest one in the database.
6. Column defaults: prefer the application-side default, visible at the call site and testable without a
   database.

### 4. Queries
1. **No query inside a loop.** A lazy-loaded relation accessed per iteration, an aggregate per row, a
   `find()` in a `foreach` — all N+1. Eager-load or aggregate before iterating. This includes a loop inside a
   view.
2. **Read the relation accessor**, never re-fetch a related model by hand from a foreign-key attribute: the
   accessor uses the loaded relation when it's there and is the thing eager-loading can optimise.
3. **Prefer the `OrFail` fetch** (`findOrFail`, `firstOrFail`) over a fetch plus a null check that aborts
   404: one line, and the not-found path can't be forgotten.
4. Push filtering, sorting and pagination into the query, not into a collection loaded whole and filtered in
   PHP.

### 5. Naming, typing, style
1. House casing applied per artefact kind (classes, jobs, events, listeners, commands, resources, enums,
   views, routes, variables, methods, abilities) without exception.
2. **Names reveal intent**: never `$temp`, `$data`, `$result`, `$array`, `$item`, `$value`, `$x`. The generic
   name pushes the meaning into the reader's head.
3. **No magic strings or numbers with domain meaning.** A domain value (status, type, kind, mode) becomes an
   enum; a queue name, config key or event name becomes a constant or a config entry; a threshold becomes a
   named constant.
4. **Native typed properties and signatures** over docblock-only types: the runtime enforces the former.
5. A docblock is for what the type system can't express (a collection's element type, an array shape, a union
   the signature can't state). **Skip it entirely on a fully type-hinted method** — a docblock repeating the
   signature is a second copy to keep in sync.
6. **Constructor property promotion** for a constructor that only assigns its parameters to properties.
7. String building through interpolation with braced placeholders rather than concatenation splicing quoted
   fragments.
8. Blank lines **between logical steps** inside a method body, so the steps are visible; not between every
   pair of lines.
9. Guard clauses and early returns rather than nested branches; no brace-less single-line statement.
10. **All code in one language — English** — including class and method names, command signatures and
    descriptions, log messages, console output, exception messages, queue and config keys. User-facing text
    is the exception, and it goes through translation.
11. Whether new files declare strict types is a **project-wide decision applied uniformly**, and the
    framework's own scaffolding is the reference point: a codebase half strict and half not gets the downsides
    of both.

### 6. HTTP surface
1. REST routes follow one consistent URI structure across the app, declared through the framework's resource
   routing rather than hand-rolled verb by verb.
2. Standard CRUD on a model is declared through the resource/REST mechanism the project standardises on — a
   hand-rolled CRUD stack for a plain model is five endpoints of avoidable code and a sixth behaviour that
   differs.
3. **Validation in a FormRequest**, with each field's rules expressed as an **array** of entries rather than
   a pipe-delimited string: a string breaks the moment a rule contains a delimiter, and an array diffs
   cleanly.
4. A response carries a **status/type and a human-readable message**, not just an HTTP code: the frontend has
   to display something.
5. User-facing email to a user goes through a notification, not a direct mail send: the notification owns the
   channel decision and the user's preferences.

### 7. Configuration and commands
1. Config file names and keys follow one casing convention; every value is read **through the config layer**,
   never `env()` reached into from business code — outside config files, `env()` returns null once the config
   is cached.
2. Third-party credentials and service settings live in config with an env-backed default, never inline in
   the class that calls the API.
3. A console command declares an explicit signature and description; the class does the wiring, an
   action/service does the work — a command whose `handle()` holds the logic can only be run from a terminal.
4. **Run the command rather than writing it out** for the user to copy, when a runtime is available. A
   command described but never executed is an untested claim (`WORKFLOW.md`, the default-is-failure
   guarantee).

### 8. Jobs and realtime
1. **Order queued work explicitly** — chain the jobs, or make the later step verify its precondition. Never a
   fixed delay, `sleep`, or debounce window chosen so earlier work "should have settled": that's a race with
   a comment.
2. A job is idempotent where it can be: a queue retries.
3. Realtime broadcasting goes through the project's broadcaster (a Pusher-protocol-compatible server, or the
   framework's own), with channel authorisation declared alongside the channel — a public channel is a
   decision, not a default.
4. A broadcast payload is a contract with the frontend: it carries what the client needs, not the whole model
   with its hidden attributes.

### 9. Tests and static analysis
1. Two tiers, and no third: **feature tests** exercising the real HTTP/command/job entry point through the
   framework, and **unit tests** for logic with no framework dependency. A test that boots the framework to
   assert a pure function is a slow unit test; a "unit" test mocking the whole framework to check a route is
   a feature test in disguise.
2. One test style across the project (class-based with test attributes, or the project's chosen alternative),
   applied uniformly.
3. **Seeders and factories: no orphans.** Every foreign key resolved through a factory relationship or an
   explicit lookup, never a hardcoded id that happens to exist locally.
4. A factory produces a valid minimal object; the test states what it needs on top. A factory that fabricates
   a fully-populated aggregate makes every test depend on data it never asked for.
5. Reference data inserted by a migration or a seeder is idempotent — it runs again on the next environment.
6. Where a static analyser is installed, detect its configured level on the first edit and **write to that
   level**, rather than introducing findings someone else has to clear. Its baseline is not a licence to add
   to the baseline.
7. Beware a factory whose model has a lifecycle listener performing an outbound call: the test needs that
   call faked, or the suite makes real network requests and fails for reasons that look like flakiness.

### 10. Architecture
1. Separate the **functional/business** layers from the **technical/shared** ones, with a predictable place
   per domain, and no technical layer importing a functional one.
2. A new dependency is a decision: check what the project already standardises on for the need (factories,
   policies, permissions, media, activity logging, translations, auth tokens, queues, multi-tenancy, static
   analysis) before adding a second library for something already solved.
3. Prefer the framework's own mechanism over a custom one; prefer configuration over a new abstraction. The
   framework already does most of the design-pattern work (`skills/design-patterns`).

## Output / checkpoint
Code compliant with the sections above, formatter clean, and no new static-analysis finding introduced by the
diff. Checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. These rules govern **new** code; existing fat models, observers and magic
strings stay until migrated deliberately (`skills/simplify`, not this block). Never widen a permission or
skip an authorisation check to make something work — that's a security decision, and it goes to
`skills/security-hardening`. Where an org catalogue is installed and disagrees, **it wins**, and say so
explicitly rather than silently applying either one.

## Origin
Ideas taken from: **an org skill catalogue for this stack (45 skills: thin models, events over observers,
behaviour as opt-in traits, no markup in PHP, owning the domain, permissions not roles, permissions for
access only, no DB enums, enums with behaviour, no cascade delete, no superficial factorisation, soft deletes
requiring pruning, application-side defaults, no queries in loops, relation accessors, OrFail fetches,
intent-revealing naming, no magic strings, native type declarations, docblock style, constructor property
promotion, string interpolation, whitespace, control flow, code in English, REST routing, CRUD via the REST
mechanism, validation as arrays, mail via notifications, config conventions, command conventions, running
commands, deterministic job ordering, broadcasting, two-tier testing, one test style, seeder and factory
rules, static-analysis awareness, layered scaffolding, preferred packages)** — rules extracted, de-identified
and rewritten generically, with the internal package names, architecture scaffold, broadcaster and MCP
tooling deliberately left out (rule C); the framework's own documentation for the mechanisms cited.
Mechanisms rewritten, no copied text. Stamped 2026-08-06.

**Fills a real gap**: `php-patterns` covers the language and explicitly stopped at the framework boundary,
leaving Laravel — the stack with the largest catalogue of the set — with no block at all on the mentis side.
