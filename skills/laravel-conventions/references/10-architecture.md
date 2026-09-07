# laravel-conventions §10 — Architecture

> Section 10 of `skills/laravel-conventions`. Read it when the change spans layers, or a new one is proposed. The other sections and the guardrails stay in `SKILL.md`.

1. Separate the **functional/business** layers from the **technical/shared** ones, with a predictable place
   per domain, and no technical layer importing a functional one.
2. A new dependency is a decision: check what the project already standardises on for the need (factories,
   policies, permissions, media, activity logging, translations, auth tokens, queues, multi-tenancy, static
   analysis) before adding a second library for something already solved.
3. **A version branch past its security-fix end of life is not a maintenance choice.** Both the framework's
   and the language's support windows are published and mechanical, so the question has a date for an
   answer rather than an opinion: a new project starts on the newest stable major and the newest minor that
   major supports, and an existing one is planned off a branch before its security window closes, not after
   an advisory forces it. Staying behind also compounds — each skipped major makes the next upgrade the
   one nobody has budget for.
4. Prefer the framework's own mechanism over a custom one; prefer configuration over a new abstraction. The
   framework already does most of the design-pattern work (`skills/design-patterns`).
5. **Where a layer-package convention (OSDD-style) is installed**, point 1's split is enforced structurally,
   not just by discipline: each functional (`users`, `billing`, ...) or technical domain is its **own
   self-contained Composer package** — `composer.json`, `src/`, its own `database/` (migrations, seeders),
   its own `tests/`, its own service provider — generated and scaffolded through the package's own commands
   rather than by hand. Where installed, it's the house override for point 1: don't hand-roll a `functional/`
   folder convention that competes with it. [`xefi/laravel-osdd`, github.com/xefi/laravel-osdd, read
   2026-08-10.]
6. **Where `laravel/boost` is present, install it with its agent skills (`--skills`), not the MCP server
   alone** — packages now ship their conventions as skills rather than as guidelines, so a guidelines-only
   install reaches nothing package-specific, including the concrete layout point 5 depends on. Run it
   interactively: a non-interactive first install silently drops every third-party skill while still
   reporting success. [`laravel/boost`, github.com/laravel/boost, read 2026-08-11.]
