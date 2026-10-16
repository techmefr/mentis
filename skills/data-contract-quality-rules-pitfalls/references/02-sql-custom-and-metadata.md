# data-contract-quality-rules-pitfalls §2 — SQL and custom rules, metadata, scheduling

> Part 2 of `skills/data-contract-quality-rules-pitfalls`. Version-bound: ODCS v3.2.0. Read it when a rule must
> run, be routed or be referenced. Sources: the standard's data-quality page and its v3.2.0 JSON schema
> (Apache-2.0); points marked own guidance are ours.

## 2.1 SQL rules
1. **A SQL rule is one query that returns a number or a boolean**, which is then compared with the rule's
   operator.
2. **The query is written in the dialect of the contract's server.** The definitions table says no translation
   is provided, so a contract moved to another warehouse needs its SQL rules rewritten.
3. **The placeholders are spelled three ways in the standard's own files.** The SQL section substitutes
   `{object}` (the table or view) and `{property}` (the column). The operator example on the same page writes
   `{table}` and `{column}`, and the schema's example uses `${table}` and `${column}`. Use the SQL section's
   spelling and confirm what the executing engine substitutes before relying on any of them.
4. **`{property}` has a meaning only where a property exists** (own guidance, read from the placeholder's
   definition as the current column): a schema-level rule has no column to substitute.
5. **A query that returns several rows or columns is not what the rule compares** (own guidance, from "returns
   a value that can be compared"); aggregate in the query.

## 2.2 Custom rules
1. **A custom rule names an `engine` and carries an `implementation`.** The page says the implementation is
   passed as it is to the tool, in any format, and calls custom rules an intermediate step until the vendor
   accepts the standard natively.
2. **The contract does not validate what is inside.** Whether the block is correct is known only to the engine
   that runs it (own guidance, from "passed as-is"). A custom rule is therefore as strong as the engine's own
   review of it: give it an owner who can read it.
3. **The documentation and the schema disagree on the shape.** The definitions table calls the implementation
   a text, non-parsed block, one example shows it as a parsed mapping, and the v3.2.0 schema allows either a
   string or an object. Write the form the engine expects, and keep the engine and block together.
4. **The `engine` value is open and spelled inconsistently**: the page writes `greatExpectations`, the schema's
   examples write `great-expectations`. Pick one spelling per team and check what the engine expects.
5. **A custom rule is not portable.** Dropping the engine leaves a rule nobody can execute; prefer a library
   or SQL rule when one says the same thing (own guidance).

## 2.3 Rule metadata
1. **Give every rule a stable `id`.** The page calls it a unique identifier for stable, refactor-safe
   references, recommended for anything referenced. The v3.2.0 schema requires it to be unique within its
   array and to avoid `.`, `#`, `/`, `\`, `@`, `!`, `%`, `&`, `^` and whitespace.
2. **`severity` and `businessImpact` are free strings.** The schema's examples for severity are info, warning
   and error, and for business impact operational and regulatory, but nothing enforces them. If a pipeline
   routes or blocks on severity, write the allowed values and what each does in the team's own rules.
3. **`dimension` is a closed list of seven**: accuracy, completeness, conformity, consistency, coverage,
   timeliness, uniqueness. The page also lists two-letter synonyms, but the schema's list holds the full
   names only; use the full names.
4. **`method` is open**, with reconciliation as the named example. Use it to say a rule compares two sources,
   and name both in the description (own guidance).
5. **The metric field replaced `rule`.** `rule` is marked deprecated in both the page and the schema; new
   contracts use `metric`.
6. **`description`, `name`, `tags`, `authoritativeDefinitions` and `customProperties` are optional.** A rule
   with only an operator and a number is legal and unreadable; say in `description` what the failure means
   (own guidance, with `businessImpact` for the consequence).

## 2.4 Scheduling
1. **`scheduler` names the scheduling tool and `schedule` carries its configuration.** The page's example is
   `cron` with a cron expression; any tool the organisation supports may be named.
2. **Older contracts use a different field.** The page says earlier versions allowed only cron and called the
   expression `scheduleCronExpression`; check for it when moving a contract to 3.2.0.
3. **A schedule in the file is information for a tool**, not an executor (own guidance, from the page's wording
   "information for executing the rules"). Say in the pipeline which tool reads it, or the schedule is decoration.
