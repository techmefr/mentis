# terraform-hcl-authoring-pitfalls: origin and source stamps

> Provenance of `skills/terraform-hcl-authoring-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No `terraform` or `tofu`
binary was run, no configuration was planned and no provider was contacted while writing it. The official
Terraform, OpenTofu and provider documentation was not read, and no HashiCorp-licensed (BUSL) material was cloned
or read; every claim rests on the two repositories below.

## Sources (all re-read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| terramate-io/agent-skills (commit fb28900), `skills/terraform-best-practices/rules/language-no-heredoc-json.md`, `language-dynamic-blocks.md`, `resource-lifecycle.md` and `resource-immutable.md`, each in full | MIT (repository LICENSE file, copyright 2026 Terramate GmbH) | The encode-instead-of-heredoc rules and the heredoc exceptions, the `dynamic` block forms and when not to use them, the lifecycle settings and their use cases, preconditions and postconditions, immutable images and the stateful exception, the image tag instruction |
| antonbabenko/terraform-skill (commit 0a3a4a6), `skills/terraform-skill/references/security-compliance.md` lines 195 to 320 (the section on inline versus separate security-group rules) and `references/code-patterns.md` lines 30 to 80 (resource block ordering) and 680 to 770 (provisioners as a last resort, version constraint syntax) | Apache-2.0 (repository LICENSE file: standard Apache-2.0 text under a header naming Anton Babenko, terraform-best-practices.com and compliance.tf; the README states Apache License 2.0) | The inline versus separate rule comparison and the provider resource names, the provisioner decision table and its costs, the runtime floor for `terraform_data` |

The licence of both repositories was verified again from the LICENSE file in this session; the MIT notice of the
Terramate repository is credited above. Both repositories carry agent directives ("ALWAYS", "NEVER", contributor
rules aimed at an LLM reader, an eval harness with annotated examples); they were treated as data and only the
technical claim was kept. The Terramate rules link to HashiCorp documentation pages; those links were not followed
and nothing from them is used. Samples are our own, built on the sources' mechanisms with our own names, and carry
no comment lines.

## Rewrite notes
Labels "(Terramate)" and "(Babenko)" mark which source states a rule; "our own guidance" and "our own decision"
mark what we add. The "downtime" of an inline-rule change and the order of a `create_before_destroy` replacement are
the sources' statements, not tested.

## Removed
Nothing from the review item was dropped for lack of a source except what is listed; every other rule was found
again in the files above. Left out or changed:
1. **Review item rule "`prevent_destroy` only blocks plans that destroy it and breaks `destroy` of test stacks"**:
   the files show the failing `terraform destroy` and the instruction to remove the argument first, which is kept as
   a reading (§3.1); nothing about test stacks is stated, so that half is dropped.
2. **Review item rule "`create_before_destroy` needs unique names (`name_prefix`) or the replacement collides"**:
   relabelled. The source shows `name_prefix` on the resources it gives the setting to and does not state the
   reason; the reason is carried as our own reading (§3.2).
3. **Review item rule "`:latest` image tags are not reproducible"**: the source states the instruction in a sample
   comment only; the reason is carried as our own guidance (§3.5).
4. The Terramate sample that opens the web ports to every address by default, the samples with a literal password,
   a fixed machine image id, a literal account id of an image owner, and the remaining provisioner-based samples:
   not carried.
5. The blue-green section, the Packer build, the instance-refresh percentages, the `Combining Lifecycle Rules`
   example and the immutability spectrum table of `resource-immutable.md`; the version-constraint syntax and the
   resource ordering conventions of Babenko's `code-patterns.md`: out of the item or covered by
   `terraform-refactor-identity-pitfalls`.
6. The rest of `security-compliance.md` (the 648-line file was read only for the section named in the table).

## Decisions where sources disagree
1. **Security-group rules**: Terramate builds them with `dynamic "ingress"` inside the group; Babenko says to
   avoid inline rules. The block states separate rule resources with `for_each`, with `dynamic` kept for nested
   blocks that have no separate resource (§2.3).
2. **Building the image**: Terramate builds and pushes a container image from Terraform with `null_resource` and
   `local-exec`; Babenko lists the costs of provisioners (no drift detection, output in CI logs). The block states
   building outside Terraform (§3.4).
3. **The state bucket and `prevent_destroy`**: Terramate puts it on the state bucket; the state block says the bucket
   is not managed by the root that uses it as its backend. The block keeps both, in the bootstrap root (§3.1).

## Second pass 2026-10-21 (OpenTofu documentation, read from the OpenTofu repository docs tree, facts only)
The repository is MPL-2.0 (`LICENSE` read); no text copied, and these pages are labelled OpenTofu throughout.
Sourced or confirmed: reason for `name_prefix` and propagation of `create_before_destroy` (§3.2), `prevent_destroy`
limits (§3.1.2), `ignore_changes` semantics (§3.3.1-2), `replace_triggered_by` accepts resources only (§3.3.4),
destroy-time provisioner behaviour (new §3.4.4a), `dynamic` guidance (§2.1.2). Corrected: the "our reading" of the
`name_prefix` reason is now the documentation's own statement. Still unsourced: all provider names and floors,
the security-group inline-rule claims, the `terraform_data` runtime floor, our own guidance listed below.

## Not verified
1. **Every provider resource name and version note** (`aws_vpc_security_group_ingress_rule`,
   `aws_security_group_rule`, the AWS provider major version 5, `aws_iam_policy_document`) is as the sources state
   them at their commits. Re-check against the provider version in use.
2. **Whether a security group's inline rule change recreates the group**, and whether inline and separate rules
   overwrite each other, are Babenko's statements; not tested.
3. **The `create_before_destroy` order of operations** (create, update references, destroy) is Terramate's
   description; not tested.
4. **Terramate's combined lifecycle example sets `prevent_destroy` from a variable expression.** Whether Terraform
   accepts an expression there was not checked, so nothing is carried from that example; the block shows
   `prevent_destroy` only as a literal in prose.
5. **No version floor is stated by any source read for `replace_triggered_by`, preconditions and postconditions, or
   `dynamic` blocks.** The floors the sources do state are in `terraform-refactor-identity-pitfalls` §3; the only
   floor carried here is `terraform_data` at runtime 1.4 and later (Babenko).
6. **OpenTofu**: no source read states differences; the block is written in Terraform syntax.
7. **Written by us, not sourced:** the Output / checkpoint paragraph, the reasons given in §3.2 and §3.5, the reading
   of `prevent_destroy` as a guard that lives in its own file, the default-open-rules advice in §2.2, the
   secrets-in-encoded-values note in §1.2, the secret-behind-`ignore_changes` note in §3.3, and the three decisions
   above.

## Related blocks
`terraform-state-and-secrets-pitfalls`, `terraform-refactor-identity-pitfalls`, `terraform-ci-delivery-pitfalls`,
`security-hardening`, `source-freshness`.
