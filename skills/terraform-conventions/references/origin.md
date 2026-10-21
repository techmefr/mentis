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

**Second pass 2026-10-21 (OpenTofu documentation, facts only, labelled as such).** Read from the OpenTofu
repository docs tree (MPL-2.0, `LICENSE` read): resource behavior (`prevent_destroy` limit confirmed, §3.7),
lock file and version constraints (§4.6, §4.7), `for_each` and `count` (§3.1), refactoring. No OpenTofu floor is
stated by those pages, so floors remain Terraform-stated and unchecked. Corrected: none in this block.

**Independent verification 2026-10-21 (vendor documentation sources, content of the Terraform 1.10, 1.11, 1.12 and 1.16 trees of
the hashicorp web-unified-docs repository, licensed BUSL 1.1: facts only, nothing copied, the integrator may drop what rests on it; community book from its repository).** Corrected: (a) §1.4 gave one order for the
last resource-block arguments (tags, `depends_on`, `lifecycle`) as common ground; the vendor style guide puts `lifecycle`
before `depends_on` and the community book the reverse, so the text now says they differ; (b) §2.3 said the native S3 lock
file exists from 1.10; the 1.10 backend page calls `use_lockfile` experimental and the 1.11 page drops the label. Vendor pages now
also state the floors of `moved` (1.1), `removed` (1.7), the test framework (1.6), mocking (1.7), ephemeral values (1.10) and
write-only arguments (1.11); the floors of the `import` block (1.5) and `optional` defaults (1.3) are still read from no vendor page.

**Version stamps.** Terraform pages "latest" read 2026-10-02. OpenTofu was not read; its release numbering and
feature floors differ and every floor in this block is stated for Terraform.

**Reasoning of ours, not a source statement:** §2 points 4 (criteria), 7, 8; §3 point 7 (second half); §4 points 8,
9; §5 points 3, 5, 9.

Independent verification 2026-10-21: 20 checked, 16 matched, 2 corrected, 2 unverified
