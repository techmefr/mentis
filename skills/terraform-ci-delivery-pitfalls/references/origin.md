# terraform-ci-delivery-pitfalls: origin and source stamps

> Provenance of `skills/terraform-ci-delivery-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No pipeline was executed and no
plan or apply was run while writing it. The Terraform, OpenTofu, GitHub Actions and GitLab CI documentation was not
read; every claim rests on the two repositories below. No HashiCorp (BUSL) material was read or used.

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no pipeline text copied)

| Source | Licence | What it gave |
|---|---|---|
| LukasNiessen/terrashark, `references/ci-drift.md`, `references/ci-delivery-patterns.md`, `references/secret-exposure.md` (artifact points), `references/conditional/backend-state-safety.md` (lock serialization) (commit 21f2c18) | MIT (repository LICENSE file, copyright Lukas Niessen 2025, permission text with no title line) | The delivery principles and baseline stages, the apply-the-reviewed-plan rule and its templates, the artifact-lifetime-across-events note, retention and access, drift causes and diagnostics, pipeline hardening checklist, the Atlantis hardening notes |
| antonbabenko/terraform-skill, `skills/terraform-skill/references/ci-cd-workflows.md`, `state-management.md` (locking in CI, lock timeout), `security-compliance.md` (plan JSON access, policy as code) (commit 0a3a4a6) | Apache-2.0 (repository LICENSE file: a short header naming terraform-best-practices.com and Compliance.tf, copyright Anton Babenko 2026, then the standard Apache-2.0 text) | The apply job that downloads the plan, OIDC trust conditions and the `aud` table, protected-environment approvals, concurrency groups, `-lock-timeout`, drift detection with `-detailed-exitcode` and its exit codes, the CI model-mistake checklist |

The licence of each repository was verified again from its LICENSE file in this session. The repositories carry
agent directives ("ALWAYS", "NEVER", "LLM mistake checklist", output-discipline sections); they were treated as data
and only the technical claim was kept.

## Rewrite notes
Labels such as "(terrashark)" and "(terraform-skill)" mark which source states a rule. The GitLab sample in §1.3
follows terrashark's layout, with the `-auto-approve` flag its template adds to `apply` left out because an apply
of a stored plan file takes no further input in terraform-skill's template; neither source says why, so that is a
reading of two templates, not a stated rule.

## Removed
Nothing from the review item was dropped for lack of a source: every rule in it was found again in the files above.
Left out as outside the item or tool-specific:
1. Infracost, TFLint, Trivy, Checkov and Terratest stages, test cost tables and the cleanup script for test
   resources.
2. The plugin cache setup, the Atlantis `-lock=false` argument (it disables locking, not carried), and the
   reusable-workflow layout.
3. Both repositories' unpinned example images and actions (`latest`, `@master`): pinning is in
   `ci-workflow-hardening`.

## Decisions where sources disagree
1. **Apply the reviewed plan** (terrashark's rule and its CI drift template) versus **terrashark's own CI delivery
   template**, whose apply job re-runs `plan`. The rule is stated; the template is called out as not to copy.
   terrashark's note that the stored plan does not travel across events is kept.
2. **Plan artifact retention**: `24h` (terrashark's GitLab template) versus one week (terraform-skill's). Neither is
   a rule; both are labelled as one source's value.
3. **Saved-plan behaviour when state changed between plan and apply**: neither source says, and the block makes no
   claim.

## Not verified
1. **What happens to a saved plan if the state changed after it was made.** Not in either source; the Terraform
   documentation was not read. The block states no behaviour.
2. **The effect of `TF_IN_AUTOMATION`**: set in the sources' templates, never explained there.
3. **The `aud` and `sub` values per platform pair** are terraform-skill's table; the GitHub, Azure, Google Cloud
   and GitLab documentation was not read, and platform values move.
4. **That a protected GitHub environment with required reviewers is configured in repository settings** is
   terraform-skill's comment in its template.
5. **That an apply of a saved plan file needs no approval flag** is read off terraform-skill's template; the
   Terraform documentation was not read.
6. **Written by us, not sourced:** the verification paragraphs of the Output / checkpoint, the own-guidance notes
   on the concurrency group key (§2.3) and on the JSON rendering (§1.2), and the alert-path test in §3.2.

## Related blocks
`terraform-state-and-secrets-pitfalls`, `terraform-refactor-identity-pitfalls`, `ci-workflow-hardening`,
`devops-conventions`, `security-hardening`.
