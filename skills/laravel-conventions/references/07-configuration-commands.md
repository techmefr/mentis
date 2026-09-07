# laravel-conventions §7 — Configuration and commands

> Section 7 of `skills/laravel-conventions`. Read it when `config/`, `env()`, an artisan command, a seeder or a factory. The other sections and the guardrails stay in `SKILL.md`.

1. Config file names and keys follow one casing convention; every value is read **through the config layer**,
   never `env()` reached into from business code — outside config files, `env()` returns null once the config
   is cached.
2. Third-party credentials and service settings live in config with an env-backed default, never inline in
   the class that calls the API.
3. A console command declares an explicit signature and description; the class does the wiring, an
   action class does the work — a command whose `handle()` holds the logic can only be run from a terminal.
4. **A console command earns its place by being run more than once** — on a schedule, or on demand as a
   repeatable operation. A one-off **data** change (backfill a column, correct bad rows, reshape a table)
   belongs in a migration, where it is versioned, ordered against the schema it depends on, and replayed on
   every environment by the same mechanism as the rest. A one-off inspection or a single outbound action
   belongs in a REPL snippet with nothing committed. A run-once command that ships becomes dead code the
   moment it runs, and it is the file every later reader has to decide whether it is safe to run again.
5. **Run the command rather than writing it out** for the user to copy, when a runtime is available. A
   command described but never executed is an untested claim (`WORKFLOW.md`, the default-is-failure
   guarantee).
