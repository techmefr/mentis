# terraform-refactor-identity-pitfalls: origin and source stamps

> Provenance of `skills/terraform-refactor-identity-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No Terraform or OpenTofu
command was executed while writing it; no plan was read from a real configuration. The official Terraform and
OpenTofu documentation was not read; every claim rests on the repositories below. No HashiCorp (BUSL) material
was read or used.

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no configuration text copied)

| Source | Licence | What it gave |
|---|---|---|
| LukasNiessen/terrashark, `references/identity-churn.md`, `references/migration-playbooks.md`, `references/ci-drift.md` (lockfile points only) (commit 21f2c18) | MIT (repository LICENSE file, copyright Lukas Niessen 2025, permission text with no title line) | `count` versus `for_each` decision, stable keys, known-at-plan keys, `moved` playbooks, the declarative `import` playbook and its 1.5+ floor for both runtimes, runtime and provider upgrade flow |
| antonbabenko/terraform-skill, `skills/terraform-skill/references/code-patterns.md`, `state-management.md` (provider removal, state moves, safe destroy), `testing-frameworks.md` (commit 0a3a4a6) | Apache-2.0 (repository LICENSE file: a short header naming terraform-best-practices.com and Compliance.tf, copyright Anton Babenko 2026, then the standard Apache-2.0 text) | The feature guard table with version floors, limits of `moved`, the plan-time key table, version constraint syntax, provider removal, `removed` block floors, targeted-destroy cascade, `terraform test` modes, mocks, set blocks, `check` versus conditions, the model-mistake checklists |
| terramate-io/agent-skills, `skills/terraform-best-practices/rules/provider-version-constraints.md` (commit fb28900) | MIT (repository LICENSE file, copyright Terramate GmbH 2026) | The three provider constraint strategies, the lock file practices, why unpinned providers drift |

The licence of each repository was verified again from its LICENSE file in this session. The repositories carry
agent directives ("ALWAYS", "NEVER", "LLM mistake checklist", a Priority tag per rule); they were treated as data
and only the technical claim was kept, restated as a mechanism or as a decision where sources differ.

## Rewrite notes
Labels such as "(terrashark)" and "(terraform-skill)" mark which source states a rule. Version floors are quoted as
terraform-skill states them and labelled as such. The Terramate rule's own code samples and its prose "Why It
Matters" paragraph were not carried; only its three strategies and the lock file practice were used.

## Removed
Nothing from the review item was dropped for lack of a source: every rule in it was found again in the files above.
Left out as outside the item:
1. HCL authoring rules (variable ordering, output naming, dynamic blocks, locals for deletion order, provisioners):
   they belong to a separate authoring block, not to address identity.
2. `ignore_changes`, provider-defined functions and cross-variable validation details beyond their table rows.
3. The Terratest sections and cost figures of the testing reference.

## Decisions where sources disagree
1. **Provider constraint style**: terraform-skill recommends `~> 5.0`-style ranges in some places and calls an
   exact pin inflexible; the Terramate rule offers an exact pin for production, a `~>` range for development and a
   bounded range. The block keeps "pin, commit the lock file, review its diff" and leaves the style to a recorded
   decision, not a rule.
2. **`moved` versus `state mv`**: both sources prefer `moved` in automation; terraform-skill also documents
   `state mv` for manual refactors, kept in the state block, not recommended here for automation.

## Not verified
1. **Every version floor** in the table in §3.1 (and the `removed` and `import` floors in §2) is as the sources
   state it; none was checked against the official documentation. OpenTofu floors are stated by the sources only
   for `import`, `removed` and `terraform test`. Re-check at writing time.
2. **The exact error text** "Condition expression could not be evaluated at this time" and `Invalid for_each
   argument` are quoted from terraform-skill; the wording may differ by version.
3. **The behaviour of a `moved` block inside a removed module** (silently stops working) is terraform-skill's
   claim; not reproduced.
4. **`plan -generate-config-out`** is from terraform-skill's import workflow; its floor and limitations were not
   checked.
5. **The Terramate rule's version-constraint figures** (`5.31.0`) are example values, not recommendations, and are
   not used.
6. **Written by us, not sourced:** the verification paragraphs of the Output / checkpoint, and the grouping of the
   floor table by feature.

## Related blocks
`terraform-state-and-secrets-pitfalls`, `terraform-ci-delivery-pitfalls`, `devops-conventions`,
`ci-workflow-hardening`, `testing-anti-patterns`.
