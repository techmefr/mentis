# laravel-conventions §10 — Architecture

> Section 10 of `skills/laravel-conventions`. Read it when the change spans layers, or a new one is proposed. The other sections and the guardrails stay in `SKILL.md`.

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
   folder convention that competes with it. [`xefi/laravel-osdd`, github.com/xefi/laravel-osdd, read
   2026-08-10.]
