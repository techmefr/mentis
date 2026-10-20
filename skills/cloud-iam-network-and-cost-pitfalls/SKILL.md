---
name: cloud-iam-network-and-cost-pitfalls
description: "Use when designing, deploying or reviewing something on a public cloud (AWS first, the same traps on GCP and Azure): which identity runs the workload and what it may do, what is reachable from the internet, outbound network paths, sizing and cost before anything is created, stateful resources inside infrastructure-as-code stacks, and what a deployment leaves behind."
---

# cloud-iam-network-and-cost-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the traps that belong to the cloud provider and not to the tool that
creates the resources. The premise: **a cloud account accepts almost any request, so the mistakes are quiet**: a
role that can do everything, a port open to the world, a managed gateway billing per gigabyte, a database replaced
because a resource was renamed, a forgotten volume billing for months. The tool that writes the resources is in
`terraform-conventions` and its siblings; cluster access is in `kubernetes-access-and-exposure-pitfalls`; functions
are in `serverless-edge-worker-pitfalls`.

## When
- A workload is deployed to a cloud account, or the request names AWS, GCP, Azure or a managed service of one.
- A role, policy, security group, bucket or network path is created or changed.
- A deployment is generated and nobody has yet said what it will cost.
- A stack, template or module is changed and could replace a stateful resource.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Identity per workload, existing-role discovery, least privilege, reachability, outbound paths | a role, policy, network rule or bucket is written or reviewed | [`01-identity-and-exposure.md`](./references/01-identity-and-exposure.md) |
| 2 | Cost estimate first, dev-sized defaults, per-use charges, stateful resources in stacks, previews, leftovers | a deployment is generated, changed or torn down | [`02-cost-and-change-safety.md`](./references/02-cost-and-change-safety.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: each workload has its own identity with a
list of the actions it needs, nothing is reachable from the internet without a stated reason, the estimated monthly
cost was shown before creation, stateful resources are protected against replacement, and the preview of the change
was read.

## Guardrails
- Give each workload its own identity limited to the actions and resources it uses (§1.1). Never attach a full-access managed policy to make an error go away.
- Look for an existing role before creating one, and stop to ask when the caller cannot create (§1.2). Never retry other identity operations hoping one is allowed.
- Open a port or a bucket to the world only with a written reason (§1.4). Never use "anywhere" as a way to test connectivity.
- Show the monthly estimate before generating or applying anything (§2.1). Never create billable resources first and price them later.
- Read the change preview before every apply and look for replacements of stateful resources (§2.4).
- Prices, limits and defaults are the provider's and change; re-read them for the region and plan in use before relying on a number (🟡, nothing here was deployed).

## Origin
Rewritten from the `awslabs/agent-plugins` repository (Apache-2.0, commit fbefb37) and the `huggingface/skills`
repository (Apache-2.0, commit c3ff942, role discovery), read 2026-10-20, plus official AWS and Google Cloud pages read for facts (NAT pricing basis, S3 Block Public Access, log retention, default compute identity). Points that come from our own experience
are labelled "own guidance" in the text. See [`references/origin.md`](./references/origin.md).
