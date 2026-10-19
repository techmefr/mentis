# terraform-conventions: origin and source stamps

> Provenance of `skills/terraform-conventions`. Read it when tracing a rule to its source or checking freshness
> (`skills/source-freshness`), never to apply a rule.

Written 2026-10-02 from sources read that day. Status: **new block, base to confront with a real
configuration**, no in-house production experience (🟡 in `CATALOG.md`).

| Source | Licence | Treatment |
|---|---|---|
| The vendor's Terraform language documentation (style guide, state and backends, sensitive data, module creation, version constraints, dependency lock file, tests, refactoring, import, removed, check, lifecycle, `depends_on`, `for_each`, count, provisioners, plan command, S3 backend) | not verified for reuse | **Idea only.** Facts and version floors checked against it; every sentence is ours |
| The community `terraform-skill` repository (workflow by failure mode, response contract, version-floor table, state-management and pipeline practice), last pushed 2026-07-03 | Apache-2.0 (LICENSE read) | Rewrite with credit: the failure-mode-first routing, count-versus-key identity reasoning, the destroy cascade through locals, drift alert without auto-apply, the identity-federation subject pinning, scanner-as-gate |
| The community `terraform-best-practices` book | Apache-2.0 (LICENSE read) | Rewrite with credit: naming (no type in the name, the single-resource name), argument order, the resource/infrastructure/composition vocabulary, blast radius |

**Checked against the vendor.** A secondary-guide claim was kept only where the vendor pages confirm it, or is
marked as coming from the guide alone (the floors of import, removed, the native lock file and optional-with-
defaults). One rule the secondary sources state flatly was qualified by the vendor: the destroy guard
(`prevent_destroy`) does not protect against deleting the resource block (§3.7).

**Not taken.** Ansible and Packer (not read: no block written, see the notes), cloud-specific resource advice
(a network, a storage service: infra reality and cloud documentation), the language-server and code-intelligence
workflow of the secondary guide (tooling, harness-bound), compliance-framework mappings (a different subject),
the numeric thresholds for splitting state (not a standard).

**Version stamps.** Terraform pages "latest" read 2026-10-02. OpenTofu was not read; its release numbering and
feature floors differ and every floor in this block is stated for Terraform.

**Reasoning of ours, not a source statement:** §2 points 4 (criteria), 7, 8; §3 point 7 (second half); §4 points 8,
9; §5 points 3, 5, 9.
