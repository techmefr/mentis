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
1. **No DB-level ENUM column.** Use a string column, with a PHP enum as the single source of truth, cast on
   the model, and validated through the framework's enum rule. Five reasons, and the first is the one that
   bites: **every value change is an `ALTER TABLE`** — adding one status to a 50-million-row table is a long
   migration that may lock it. Then: the type is inconsistent across engines (native enum here, a created type
   with its own alter semantics there); the DB constraint and the PHP list are **two sources of truth that will
   drift**; renaming a value becomes a multi-step data-plus-schema-plus-code migration; and a value set that
   depends on the tenant or that an admin can extend is simply impossible.
2. **Don't tune the column length to the longest value**, and **don't skip the cast** — without it the column
   comes back as a raw string and the enum bought nothing. A `CHECK (status IN (...))` constraint is the same
   mistake wearing a lighter costume: same migration friction, same duplication.
3. **A set that changes at runtime isn't an enum at all.** An admin-configurable category, a per-plan status
   list, a feature parameter — those belong in a table, not in code. The test is who changes it: a developer
   with a deploy (enum) or a user at runtime (table). A boolean column beats a two-value enum outright.
4. **An enum with per-case data puts the value on the enum as a method**, not in a `match` scattered across
   callers. A `match` on an enum case returning a rate, a label or a threshold is behaviour that belongs to
   the enum — otherwise the day a case is added, the compiler helps you in one file and not in the other six.
5. **No cascade delete at the database level.** The DB deletes rows behind the ORM's back, so nothing fires
   on the children. What silently stops happening: no audit entry for the deleted child, the child stays in
   the search index, its cache is never invalidated, it stays in the CRM/billing/ERP because no
   `child.deleted` listener ran, the cancellation email is never sent, and denormalised counters on siblings
   stay wrong. None of that fails loudly.
6. **Keep the foreign key, drop only the cascade.** Removing the constraint to dodge the rule is worse — you
   trade silent-wrong-behaviour for silent-orphan-rows.
7. **Cascade through a listener class**, registered explicitly — not a closure in a model hook. A class is
   testable on its own, keeps the model thin, and can be queued when the cascade is heavy. Inside it, stream
   the children (a cursor, or chunk-by-id when you need to dispatch between chunks); reading the relation as a
   property loads every child row into memory first, which is exactly the case you were worried about.
8. **Never both.** A DB cascade *and* a listener means the listener deletes children the DB has already
   removed, and the same domain must not mix the two strategies per parent/child pair.
9. **Debugging tip worth its own line: when a lifecycle listener "isn't firing", check the parent's foreign
   key for a cascade first.** That's the most common root cause, and it looks like a broken listener.
10. **Where a DB cascade is genuinely fine**: a pure pivot table with no columns and no business meaning; a
    deliberate data-destruction purge at scale, where firing per-row notifications is the thing you don't
    want; and an append-only log table whose only consumer is its parent's lifecycle.
11. **Decide all of this at the ERD/plan stage, not at code review.** A plan sentence like "delete the user
    and cascade to orders and sessions" has already chosen the mechanism, and a verbal answer to "should
    deleting a company remove its invoices?" is the same decision made without noticing.
12. **Don't factorise two concepts into one table** just because they look alike or share columns today. The
   shared table is cheap now and is the thing you can't unpick later, when one side grows a rule the other
   can't have.
13. Every model using soft deletes also carries a **pruning policy** with a retention window. Soft deletes
   without pruning is an unbounded table that silently becomes the biggest one in the database.
14. Column defaults: prefer the application-side default, visible at the call site and testable without a
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
1. **Two tiers, and no third.** A **feature test** boots the framework and asserts an observable outcome —
   a row written, a job dispatched, a notification sent, a response returned. A **unit test** covers code you
   wrote yourself with non-trivial logic and no framework coupling: a money converter, a period value object,
   a working-hours calculator. There is no "integration", "controller" or "service" folder; if something
   doesn't fit the two, the test is aimed at the wrong thing.
2. **The default is the feature test**, and the reason is economic: one factory call plus one assertion on the
   dispatched job covers the model hook, the listener registration and the payload at once — and it's written
   against the contract, so it survives the refactor. The framework's own Eloquent, router and queue are
   already tested; a test that mocks the database to prove a listener was wired proves only that you wrote a
   mock.
3. **The routing is mechanical**, which is the point — nobody should debate it: a model lifecycle side effect,
   an HTTP endpoint, a console command, a listener or job `handle()`, a notification or mail, a policy, a
   scope/accessor/mutator → **feature**. A pure custom domain piece → **unit**.
4. **Arrange / Act / Assert, with exactly one Act.** One action means one reason to fail; two Act blocks are
   two tests sharing a name. Name the method after the **behaviour**, not the method called —
   `it_marks_invoice_paid_when_payment_succeeds`, never `it_marks_paid`.
5. **Assert observable outcomes, never internal calls.** `shouldReceive('save')->once()` asserts your own
   plumbing; the row, the response, the dispatched job and the sent mail are what the user experiences.
6. **Four anti-patterns with the same root**: instantiating a controller and calling its action (it bypasses
   middleware, the form request, route binding and the response contract); unit-testing a job or listener
   against a mocked database; booting the framework to test a calculator; and reaching for a mocking library
   in a unit test — if you need to mock a collaborator, the collaborator is framework-touching and the test
   belongs one tier up.
7. **One test style across the project**, applied uniformly — but **inside an existing file, match that
   file's local style**. Half-migrating a file between styles is worse than either style.
8. **Seeders and factories: no orphans.** Every foreign key resolved through a factory relationship or an
   explicit lookup, never a hardcoded id that happens to exist locally.
9. A factory produces a valid minimal object; the test states what it needs on top. A factory that fabricates
   a fully-populated aggregate makes every test depend on data it never asked for.
10. Reference data inserted by a migration or a seeder is idempotent — it runs again on the next environment.
11. Where a static analyser is installed, detect its configured level on the first edit and **write to that
   level**, rather than introducing findings someone else has to clear. Its baseline is not a licence to add
   to the baseline.
12. Beware a factory whose model has a lifecycle listener performing an outbound call: the test needs that
   call faked, or the suite makes real network requests and fails for reasons that look like flakiness.

### 10. Architecture
1. Separate the **functional/business** layers from the **technical/shared** ones, with a predictable place
   per domain, and no technical layer importing a functional one.
2. A new dependency is a decision: check what the project already standardises on for the need (factories,
   policies, permissions, media, activity logging, translations, auth tokens, queues, multi-tenancy, static
   analysis) before adding a second library for something already solved.
3. Prefer the framework's own mechanism over a custom one; prefer configuration over a new abstraction. The
   framework already does most of the design-pattern work (`skills/design-patterns`).
4. **Where a layer-package convention (OSDD-style) is installed**, point 1's split is enforced structurally,
   not just by discipline: each functional (`users`, `billing`, ...) or technical domain is its **own
   self-contained Composer package** — `composer.json`, `src/`, its own `database/` (migrations, seeders),
   its own `tests/`, its own service provider — generated and scaffolded through the package's own commands
   rather than by hand. Where installed, it's the house override for point 1: don't hand-roll a `functional/`
   folder convention that competes with it. [a published open-source OSDD-style Laravel layer package, read
   2026-08-10 — cited generically per rule C, see `source-freshness`.]

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
Mechanisms rewritten, no copied text.

Section 10 point 4 (the Composer-package-per-layer structure) added 2026-08-10 from a published open-source
OSDD-style Laravel layer package — cited generically per rule C rather than by name, matching how section
1's split was already generic. Confirms the same layer-package shape as the Nuxt-side convention referenced
in `vue-nuxt-vuetify-conventions` §5.6: each domain a self-contained package with its own tests/migrations,
not a shared folder.
**Deepened 2026-08-06.** The first pass wrote this block from the catalogue skills' descriptions. This pass
read the **bodies**, which is where the reasons, the exclusion lists, the carve-outs and the anti-pattern
catalogues live — a description states the rule, a body states when it doesn't apply. What that added here: the full cost of a DB-level
cascade (audit, search index, cache, external sync, notifications, denormalised counters — none of which fails
loudly), the keep-the-FK-drop-the-cascade shape, cascade through a listener class streaming its children, the
never-both rule, the three cases where a DB cascade is fine, the "a listener that isn't firing is usually a
cascaded FK" diagnostic, the five reasons behind the no-DB-enum rule, the runtime-configurable-values carve-out
(that's a table, not an enum), and the test tiers with their routing table, their one-Act shape and their four
anti-patterns. Stamped 2026-08-06.

**Fills a real gap**: `php-patterns` covers the language and explicitly stopped at the framework boundary,
leaving Laravel — the stack with the largest catalogue of the set — with no block at all on the mentis side.
