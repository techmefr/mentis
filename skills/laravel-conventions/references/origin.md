# laravel-conventions — origin and source stamps

> Provenance of `skills/laravel-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

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

Section 10 point 4 (the Composer-package-per-layer structure) added 2026-08-10 from `xefi/laravel-osdd`
(github.com/xefi/laravel-osdd), read that date. Named directly rather than de-identified: it's the
company's own published open-source package, publicly readable outside the company like `test-casebook`
— rule C's generic-citation default is for internal/private facts, not for a real tool the company itself
ships publicly (`CONVENTIONS.md` rule C). Confirms the same layer-package shape as the Nuxt-side convention
referenced in `vue-nuxt-vuetify-conventions` §5.6: each domain a self-contained package with its own
tests/migrations, not a shared folder.
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

**§1.1/§1.2/§7.3 corrected 2026-08-11** against the real house doc (doc.stacktim.com, `/developer/nos-methodes`,
read that date). §1.1 previously said business logic "goes in an action/service", which quietly allowed the
exact `*Service`/`*Repository` bag-name `code-baseline` already forbids — an internal contradiction the real
doc caught: it explicitly bans `UserManager`/`UserService`/`XxxRepository` and requires one verb-plus-noun
action or query class per behaviour (`RegisterUser`, `GetActiveSessionsForUser`), with the reasoning that a
repository over an ORM already abstracting persistence is a layer maintained for no benefit. §1.2 gained the
explicit `boot()` prohibition (a lifecycle closure in `boot()` is the same hidden-effect problem as an
Observer, moved one line over) — the source's own convention page states it as a **non-negotiable** rule,
stronger than this block's existing generic phrasing. The source also names concrete required packages
(`spatie/laravel-permission`, `-activitylog`, `-medialibrary`, `-translatable`, `-sluggable`, `tymon/jwt-auth`,
Pulse, Telescope, Pint, Larastan) — left out here per rule C: those are the org's own package-list authority,
already the domain of the installed `xefi-claude-skills` `laravel` plugin, not something to duplicate
generically.
