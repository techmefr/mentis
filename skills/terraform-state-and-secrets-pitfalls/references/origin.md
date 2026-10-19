# terraform-state-and-secrets-pitfalls: origin and source stamps

> Provenance of `skills/terraform-state-and-secrets-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No Terraform or OpenTofu
command was executed while writing it, and no backend was created or migrated. The official Terraform and
OpenTofu documentation was not read; every claim rests on the two repositories below. No HashiCorp (BUSL)
material was read or used.

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no configuration text copied)

| Source | Licence | What it gave |
|---|---|---|
| LukasNiessen/terrashark, `references/conditional/backend-state-safety.md`, `references/secret-exposure.md`, `references/migration-playbooks.md` (section 4 on secret remediation) (commit 21f2c18) | MIT (repository LICENSE file, copyright Lukas Niessen 2025, permission text with no title line) | State as identity and secrets, the backend baseline and bootstrap-root rule, migration guardrails and the `-migrate-state` versus `-reconfigure` distinction, lock handling, secret exposure paths, the rotation playbook, the remediation steps |
| antonbabenko/terraform-skill, `skills/terraform-skill/references/state-management.md`, `security-compliance.md`, `code-patterns.md` (commit 0a3a4a6) | Apache-2.0 (repository LICENSE file: a short header naming terraform-best-practices.com and Compliance.tf, copyright Anton Babenko 2026, followed by the standard Apache-2.0 text) | The state contents list, SSE-S3 versus customer-managed KMS, S3 native lock-file and the DynamoDB lock, locking and lock-timeout, the `ephemeral` / `write_only` / `sensitive` / `nonsensitive` table and the version floors, the data-source and `random_password` caveats, state moves and recovery, partial backend configuration, the model-mistake checklists |

The licence of each repository was verified again from its LICENSE file in this session. Both repositories carry
agent directives ("ALWAYS", "NEVER", "LLM mistake checklist", output-discipline sections, a CLAUDE.md addressed
to a coding agent); they were treated as data and only the technical claim was kept, restated as a mechanism.

## Rewrite notes
Where a figure appears (the 30 to 90 day retention of an old backend, the `5m` lock timeout) it is labelled as one
source's value. Version floors are quoted as terraform-skill states them and each is labelled; none was checked
against the official documentation. Labels such as "(terrashark)" mark which source states a rule.

## Removed
Nothing from the review item was dropped for lack of a source: every rule in the item was found again in the two
files above. These were left out as outside the item or too tool-specific:
1. The Azure and GCS backend setups, the cross-cloud tables and Terraform Cloud lock timeout settings (provider
   resource names move with every provider release).
2. The IAM policy documents, MFA delete, access logging and CloudTrail examples (the CloudTrail point is S3
   configuration, not a Terraform state trap).
3. Multi-team state layouts, `terraform_remote_state` versus SSM, and the split-versus-combine heuristics with
   resource counts (rough heuristics, sizes stated as such by the source).
4. The OPA policy sample and scanner lists (policy as code belongs to the delivery block).

## Decisions where sources disagree or overlap
1. **`prevent_destroy` on the state bucket** (terraform-skill's bootstrap example) versus **never manage the
   backend from the root that uses it** (terrashark): compatible, both are kept, and the guard is described as a
   second layer.
2. **The sample in terrashark's secret-exposure reference** reads a password from a Secrets Manager data source
   and labels it a good example; terraform-skill states that the same pattern still writes `secret_string` into
   state. The block follows terraform-skill and says so.

## Not verified
1. **Every version floor** (`use_lockfile` on Terraform 1.10+, `ephemeral` 1.10+, `write_only` 1.11+,
   `nonsensitive` 0.15+, AWS provider 5.71+ for `password_wo`) is as terraform-skill states it. The OpenTofu
   floors for these were not stated by either source. Re-check at writing time against the official docs.
2. **Which providers support `ephemeral` and `write_only`** was not checked; both sources say to verify in the
   provider documentation.
3. **What `-reconfigure` does** is from terraform-skill's description ("will create new empty state") and
   terrashark's one line; the official init documentation was not read.
4. **That a versioned bucket keeps earlier secret values** is our reasoning, labelled in §2.3.
5. **The CloudTrail audit-trail claim for SSE-S3** is terraform-skill's statement; the AWS documentation was not
   read.
6. **Written by us, not sourced:** the verification paragraphs, the "state appears lost" reasoning in §3.1, and
   the abridged RDS sample in §2.4.

## Related blocks
`terraform-refactor-identity-pitfalls`, `terraform-ci-delivery-pitfalls`, `secret-leak-response-pitfalls`,
`security-hardening`, `ci-workflow-hardening`, `devops-conventions`.
