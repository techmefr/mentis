---
name: terraform-hcl-authoring-pitfalls
description: "Use when Terraform or OpenTofu HCL is written or reviewed for policies, templates, repeated blocks, lifecycle settings or deployment: jsonencode, yamlencode and policy-document data sources instead of heredocs, templatefile, dynamic blocks and the optional-block form, separate security-group rule resources versus inline rules, prevent_destroy and where it lives, create_before_destroy and unique names, ignore_changes scope, replace_triggered_by, provisioners and baked images, and image tags."
---

# terraform-hcl-authoring-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for how a configuration is written once its addresses and state are settled.
The three sections share one premise: **HCL accepts most of what you type and reports the mistake at apply time or
never, so the safe forms are the ones that make the language check your structure for you: encode instead of
concatenating, separate resources instead of nested blocks, and an image replaced instead of a host patched**.
Addresses, `count` against `for_each`, `moved` and version floors are in `terraform-refactor-identity-pitfalls`;
state, backends and secrets are in `terraform-state-and-secrets-pitfalls`; the pipeline that runs the plan is in
`terraform-ci-delivery-pitfalls`. Examples are Terraform syntax with AWS resources, because that is where the
sources were read; the mechanisms hold for OpenTofu and other providers, but provider resource names and versions
below are as the sources state them and must be re-checked.

## When
- Building a JSON, YAML or IAM policy document, or a templated script, in a configuration.
- Repeating a nested block, or writing a firewall or security-group rule set.
- Protecting a database, a key or a bucket from deletion, or planning a zero-downtime replacement.
- Telling Terraform to ignore a change made elsewhere.
- Deploying software to a host, or choosing an image reference.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Structured text and templates: encode functions, policy documents, `templatefile`, heredocs | a policy, a JSON or YAML value or a script is built | [`01-structured-text-and-templates.md`](./references/01-structured-text-and-templates.md) |
| 2 | Repeated blocks: `dynamic`, the optional-block form, security-group rules | a nested block repeats or a rule set is written | [`02-repeated-blocks-and-rules.md`](./references/02-repeated-blocks-and-rules.md) |
| 3 | Lifecycle and delivery: `prevent_destroy`, `create_before_destroy`, `ignore_changes`, provisioners, images | a resource is protected or replaced, or software is deployed | [`03-lifecycle-and-delivery.md`](./references/03-lifecycle-and-delivery.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the rendered policy or document was compared with the intended
one, `terraform plan` was run and the change set read before apply (a rule change must not show the security group
itself as replaced, §2.3), a destroy of a protected resource was tried in a scratch stack and failed with the named
error (§3.1), and a replacement was applied once in a non-production stack to see the order and any name collision
(§3.2). A configuration that only passed `validate` is not verified.

## Guardrails
- Never build JSON, YAML or an IAM policy by concatenating or interpolating into a heredoc (§1.1).
- Never mix inline security-group rules and separate rule resources on one group (§2.3).
- Never reach for `dynamic` to repeat one or two fixed blocks (§2.1).
- Never rely on `prevent_destroy` as the only protection: it lives in the file it guards (§3.1).
- Never put the state bucket's own protection in the root that uses it as its backend (§3.1).
- Never use `ignore_changes = all` on a resource Terraform is expected to manage (§3.3).
- Never deploy by `remote-exec`, and never reference an image as `:latest` (§3.4, §3.5).
- This block states behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The official Terraform and provider documentation was not read,
  and nothing was run while writing it.

## Origin
Rewritten from the Terramate agent skills Terraform best-practice rules (MIT) and the terraform-skill by Babenko
(Apache-2.0, security and code-pattern references), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
