# dbt-cli-and-model-versioning-pitfalls §2 — Model versions and breaking changes

Sources: `skills/dbt/skills/working-with-dbt-mesh/references/model-versions.md` and `model-contracts.md` (dbt-labs/dbt-agent-skills at 7c7b5fa), read in full 2026-10-15. Version bounds are those the source states: `latest_version_pointer` on dbt Core 1.12 and later and Fusion (beta in dbt's documentation per the source), a post-hook on 1.11 and earlier.

## 2.1 When to version
1. **Version only for a breaking change to a contract:** removing a column, renaming a column, changing a data type, changing nullability.
2. **Do not version** for new columns, bug fixes, performance work, or preemptively. A removed contracted model is also flagged as breaking (dbt 1.9 and later, per the contracts file).
3. **A breaking change is a new version, not an edit of the contract in place.**

## 2.2 Mechanics
1. **Each version needs its own SQL file,** `fct_orders_v2.sql`, or a `defined_in` key naming the file.
2. **In a version's `columns`,** `include: all` inherits the parent columns, `exclude: [...]` removes some, and new entries add or override.
3. **Relation names default to `fct_orders_v{N}`.** `config.alias` pins one version to a fixed name, for example the old version at the unsuffixed name; it is not a moving pointer.
4. **Unpinned `ref('fct_orders')` resolves to `latest_version`,** `ref('fct_orders', v=2)` pins, and the cross-project form takes `v=` too. Bumping `latest_version` therefore re-points every unpinned `ref`.
5. **Selection:** `dbt run --select fct_orders` runs all versions, `fct_orders_v2` one, and `fct_orders,version:latest` the latest.
6. **Unit tests run against all versions by default;** `versions: include: [2]` targets one.

## 2.3 The migration is two deploys
1. **Introducing the new version and promoting it are two separate deploys, separated by the migration window.** The new version starts as non-latest: `latest_version` stays on the old one.
2. **The pointer does not shield consumers from a shape change.** It always tracks `latest_version`, so it protects against the suffix changing, not against the shape changing; unsuffixed consumers get the new shape the moment `latest_version` is bumped.
3. **Order of work as the source gives it:** add the new version and its SQL file with `latest_version` unchanged and a pointer in place; deploy; verify; notify consumers; bump; set a deprecation date; remove the old version after it.
4. **Verify the window is open before telling consumers:** `dbt show --inline "select <old_col> from {{ target.schema }}.<unsuffixed_relation>"`. A "column does not exist" error means the version was promoted too early and the consumer is already broken.
5. **A deprecation date goes on the old version:** `deprecation_date: 2025-06-01 00:00:00.00+00:00` is the source's form. Removing it too quickly is the listed mistake.

## 2.4 The latest version pointer
1. **A pointer is an unsuffixed relation that resolves to the latest version.** With two SQL files it yields three relations: `fct_orders_v1`, `fct_orders_v2` and `fct_orders`. It is the source's recommended default for breaking-change migrations; `config.alias` is the fallback.
2. **dbt 1.12 and later, and Fusion: set `latest_version_pointer: {enabled: true}` in the model config.** The source says it is opt-in, currently beta in dbt's documentation, created after the latest version materialises, always a view in 1.12, and that the availability should be confirmed for the exact version before relying on it in production. Project-wide it is `flags: latest_version_pointer_enabled_by_default: true`, or `+latest_version_pointer: {enabled: true}` on a directory.
3. **The pointer name defaults to the unsuffixed model name.** An `alias` under `latest_version_pointer` or an override of the `generate_latest_version_pointer_alias` macro changes it. If the latest version's own `alias` equals the pointer name, dbt raises a collision error.
4. **dbt 1.11 and earlier: no built-in pointer.** The source says dbt's documentation recommends a custom macro, `create_latest_version_view`, run as a project-wide post-hook; it is a no-op except on the latest version of a versioned model, where it drops a non-view relation at the unsuffixed name and creates or replaces a view on the current relation. The source marks the `create view` syntax as platform dependent, and the macro was not run by us.

## 2.5 Checks (own guidance)
1. A change that introduces a version does not touch `latest_version` in the same merge request.
2. The pointer mechanism matching the project's dbt version is in place before the new version is deployed.
3. The `dbt show` check against the unsuffixed relation is part of the deploy of the new version.
