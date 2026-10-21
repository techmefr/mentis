# terraform-state-and-secrets-pitfalls §2 — Secrets in state

A secret that reaches a resource argument usually reaches state, and from state it reaches every reader of the
backend, every plan export and every artifact. The traps are the mechanisms that look like they prevent it and do
not.

## 2.1 What keeps a value out of state, and what does not
The floors are as terraform-skill states them (Terraform; the official docs were not read, so re-check against the
runtime in use).

| Mechanism | Stated floor | Keeps the value out of state? |
|---|---|---|
| `sensitive = true` | any | **No.** It masks display; the value can still be in state (terrashark; terraform-skill) |
| `ephemeral` values, resources and data sources | Terraform 1.10+ | Yes: not persisted in state or plan. The provider or resource must support it |
| `write_only` arguments (`*_wo`) | Terraform 1.11+ (`password_wo` needs AWS provider 5.71+) | The **resource argument** stays out of state |
| A data source read, such as a Secrets Manager `secret_string` | any | **No.** It is written to state on every refresh |
| `random_password.result` | any | **No.** It lives in state |
| Provider-managed secret, such as `manage_master_user_password = true` on an RDS instance | provider | Yes: the cloud generates and holds it. The preferred RDS pattern in terraform-skill |
| A value injected from a CI environment variable outside Terraform | any | Yes, as long as nothing in the configuration reads it back |

OpenTofu's ephemerality page confirms the mechanism for that tool: ephemeral values, variables, outputs, resources and write-only attributes are not stored in state or plan, while sensitive values stay in plain text in both (read 2026-10-20). It names no version, so the floors above remain terraform-skill's for Terraform and are unknown for OpenTofu. Its state page also says to treat state as sensitive data when it holds secrets, and that remote backends may encrypt at rest.

`sensitive` and `ephemeral` are different things: `ephemeral` values are scrubbed from state, `sensitive` only
hides them in output (terraform-skill).

## 2.2 Rules
1. **Do not assume `sensitive` means "not in state".** Verify against the provider documentation before assuming
   a secret argument is excluded from state (terrashark).
2. **A write-only argument fed by a data source does not exclude the secret.** `password_wo` keeps the resource
   argument out of state, but the `aws_secretsmanager_secret_version` data source still reads `secret_string` into
   state on refresh. For real exclusion use an ephemeral resource (1.10+), a provider-managed secret, or a
   CI-injected variable (terraform-skill).
3. **`nonsensitive()` launders a secret into plans and logs.** Using it to unwrap a sensitive output so that a
   warning goes away puts the value into plan artifacts. It is safe only for a derived value that is provably not
   secret, and the value then enters the plan (terraform-skill).
4. **No secret defaults in code, and no committed `.tfvars` with credentials.** Source secrets from a managed
   secret store at runtime (terrashark; terraform-skill).
5. **Outputs do not expose full connection strings or credentials**, even when marked sensitive, and a `local-exec`
   command that prints a secret writes it to the CI log, where `sensitive` does not redact it (terraform-skill).
6. **Prefer, in this order** (terrashark): a lookup in an external secret manager, workload identity federation
   for provider authentication, then short-lived credentials from a trusted broker. Avoid long-lived static
   credentials in the repository or in runner configuration.
7. **Search for the secret after the first apply.** terraform-skill's migration ends with a search of the state
   for the password field, which must come back empty; terrashark exports the plan JSON and checks that secret
   fields are not emitted to shared artifacts or logs.

## 2.3 When a secret is already in state
1. **Masking is not remediation.** If a secret entered state, rotate it (terrashark).
2. **Rotation order** (terrashark): create a new secret version in the manager, update the application to use it,
   roll the infrastructure, revoke the old credential, then verify that no copies remain in logs or artifacts.
3. **Remove the cause** (terrashark): create the new secret path in the managed store, switch the resources to
   reference external material, rotate after the cutover, and delete the old secret-generating Terraform
   resources where possible.
4. **After rotating outside Terraform**, `apply -refresh-only` reconciles state with the new value. It does not
   rotate the secret (terraform-skill).
5. A versioned state bucket keeps earlier state versions, so the previous
   secret value remains readable there until it is revoked (S3 versioning page, read 2026-10-20: an overwrite creates a
   new version and a delete only adds a delete marker, earlier versions stay restorable). Rotation is the remedy, deletion of the current
   object is not.
6. The wider response (history, revocation traps, scanners) is in `secret-leak-response-pitfalls`.

## 2.4 A shape that keeps the password out
```hcl
variable "db_admin_username" {
  description = "Database admin user"
  type        = string
}

resource "aws_db_instance" "core" {
  identifier                  = "core-db"
  username                    = var.db_admin_username
  manage_master_user_password = true
}
```
Abridged: the other required arguments of the resource are omitted. This is the first option in terraform-skill
for RDS. The RDS documentation confirms the mechanism: the service generates the password, stores it in the secrets manager, rotates it every seven days by default, and it is not available for read replicas of a source that uses it, blue/green deployments or the custom edition (RDS password-management page, read 2026-10-20). The other mechanism it sidesteps is that the secret then appears as a service attribute, not an argument, so check the provider documentation for what the resource exports to state. The read-from-a-data-source shape in terrashark's example
avoids a hardcoded value but, as §2.1 says, still persists the secret in state.
