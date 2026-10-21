# terraform-refactor-identity-pitfalls §3 — Versions and tests

A recent feature written for a runtime that does not have it fails at plan time, or worse, silently takes the old
behaviour. And a green `terraform test` with mocks says less than it appears to.

## 3.1 The version floor table
Floors are as terraform-skill states them for Terraform; the official documentation was not read, so re-check at
writing time. OpenTofu is named by the sources only for `import` (1.5), tests (1.6) and `removed` (1.7); for the
rest the OpenTofu floor is not stated.

| Feature | Stated floor | Mistake it guards against |
|---|---|---|
| `try()` | 0.12.20+ | falling back to `element(concat(...))` |
| `nonsensitive()` | 0.15+ | unwrapping a secret into plan artifacts (see `terraform-state-and-secrets-pitfalls` §2.2) |
| `nullable = false` | 1.1+ | omitting it, so `null` overrides a default |
| `moved` blocks | 1.1+ | omitting it in a refactor, so the change becomes destroy and create |
| `optional()` with defaults | 1.3+ | wrapper variables and loose `map(any)` contracts |
| declarative `import` blocks | 1.5+ | recommending only the CLI `import` |
| `check` blocks | 1.5+ | expecting them to block an apply (they only warn) |
| native `terraform test` | 1.6+ | treating mocked tests as integration coverage |
| mock providers, `removed` blocks | 1.7+ | asserting computed values in plan mode; deleting with no lifecycle transition |
| provider-defined functions | 1.8+ | data sources for simple transformations |
| cross-variable validation | 1.9+ | pushing every check into postconditions |
| S3 native lock file, `ephemeral` values | 1.10+ | a DynamoDB lock table on 1.10+; confusing `ephemeral` with `sensitive` |
| `write_only` arguments | 1.11+ | `sensitive = true` assumed to keep state safe |

1. **State the target runtime first, then check each feature against its floor.** Below the floor, write the
   fallback explicitly instead of silently downgrading (terraform-skill).
2. **Silently using a 1.11+ feature without checking the runtime is listed as a model mistake**, and the table is
   the guard (terraform-skill).

## 3.2 Pinning and the lock file
1. **Pin `required_version` and the provider ranges, commit `.terraform.lock.hcl`, and review its diff in the pull
   request.** Update providers deliberately with `init -upgrade`, then plan and review before committing
   (terraform-skill; terrashark; Terramate rule).
2. **The range style is a decision, not a rule here.** terraform-skill recommends `~> 5.0`-style ranges for
   providers and an exact pin for modules in production; the Terramate rule offers three strategies (an exact
   version in production, a `~>` range in development, a bounded range). `~> 5.0` allows `>= 5.0, < 6.0`, and
   `~> 5.0.1` allows patches only (terraform-skill). Pick one per repository and write it down.
3. **Ship runtime and provider upgrades separately from functional changes** where possible (terrashark;
   terraform-skill lists merging them as a model mistake).
4a. **The OpenTofu version-constraints page** says reusable modules should constrain only a minimum, root modules should
   use a `~>` bound for each provider, and `~> 1.0.4` allows `1.0.5` and `1.0.10`; its lock-file page says to
   commit `.terraform.lock.hcl`, review changes after `init -upgrade`, and commit them deliberately.
4. **An unpinned provider means two `init` runs on different days can get different versions** and behaviour
   (Terramate rule). In CI this is the usual cause of "the CI plan differs from the local plan"; see
   `terraform-ci-delivery-pitfalls` §3.1.

## 3.3 What terraform test proves
1. **A mocked-provider test validates module logic, not provider behaviour**, so it is not integration coverage
   (terraform-skill).
2. **Asserting a computed value (an ARN, a generated name, a cloud-assigned ID) in `command = plan` fails** with
   "Condition expression could not be evaluated at this time". Use `command = apply`, or assert an attribute that is
   known at plan time (terraform-skill).
3. **A set-typed nested block cannot be indexed with `[0]`**; check the real schema, then use a `for` expression
   under `command = apply` (terraform-skill).
4. **Only `validation`, `precondition` and `postcondition` gate an apply**; a `check` block is advisory and emits
   warnings (terraform-skill; the OpenTofu checks page says the same and notes that the first plan of a check with a
   scoped data source can fail because the object does not exist yet).
5. **Exercise `validation` blocks with invalid input**, not only the happy path, and run `plan -detailed-exitcode`
   after an apply to catch non-idempotent changes (terraform-skill).
6. **Gate real-cloud integration tests behind the main branch or a schedule**, not every commit (terraform-skill).
