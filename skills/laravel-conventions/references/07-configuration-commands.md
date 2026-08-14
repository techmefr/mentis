# laravel-conventions §7 — Configuration and commands

> Section 7 of `skills/laravel-conventions`. Read it when `config/`, `env()`, an artisan command, a seeder or a factory. The other sections and the guardrails stay in `SKILL.md`.

1. Config file names and keys follow one casing convention; every value is read **through the config layer**,
   never `env()` reached into from business code — outside config files, `env()` returns null once the config
   is cached.
2. Third-party credentials and service settings live in config with an env-backed default, never inline in
   the class that calls the API.
3. A console command declares an explicit signature and description; the class does the wiring, an
   action class does the work — a command whose `handle()` holds the logic can only be run from a terminal.
4. **Run the command rather than writing it out** for the user to copy, when a runtime is available. A
   command described but never executed is an untested claim (`WORKFLOW.md`, the default-is-failure
   guarantee).
