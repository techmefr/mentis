# platform-engineering-golden-paths-pitfalls: origin and source stamps

> Provenance of `skills/platform-engineering-golden-paths-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from public documents and craft knowledge. No platform, portal or catalogue
was built or run while writing it.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| cncf/tag-app-delivery at commit cadc776: `platforms-whitepaper/latest/index.md`, `platforms-maturity-model/v1/index.md` (introduction, how to use, headings), `platform-as-a-product/` research guide (skimmed, not used); LICENSE file read | Apache-2.0 (LICENSE file) | Platform attributes and team jobs, challenges, measurement families, golden path definition, maturity model usage rules |
| backstage/backstage at commit 64ab86e: `docs/golden-path/adoption/` (getting started, leadership buy-in, proof of concept, customising, launch, plugin ownership, full catalogue), `docs/features/software-catalog/` (descriptor format, life of an entity, well-known relations, API), `docs/features/software-templates/` index; LICENSE file read | Apache-2.0 (LICENSE file) | Adoption milestones and plateau, launch advice, catalogue ingestion model and ownership semantics, orphan entries, templates |

The Backstage repository holds agent instruction folders; they were not opened and nothing in them was followed.

## Left out on purpose
- Backstage installation, plugin development, deployment, authentication, permissions, search and Kubernetes
  features, and every configuration name.
- The maturity model's per-aspect tables beyond the headings and the usage section; the white paper's capability
  list; the platform interview scripts.
- Every numeric value of the sources (none was needed).

## Not verified
1. **Behaviour of Backstage** was read from documentation, not run. Eager deletion, the orphan marker and the
   ownership relation's intended use are statements at the commit; re-read before relying.
2. **The maturity model's level descriptions** were read in part: headings and the introduction. The text of the
   levels per aspect was not fully read, so §3.3 point 4 names them only.
3. **The enforcement and leadership sections of the catalogue adoption page** were unfinished placeholders at the
   commit read; nothing was taken from them beyond that fact.
4. **Own guidance, not sourced** (marked in the text): path counts and retirement, template review and testing,
   reconciliation of the catalogue, which fields to keep, baselines, how to report metrics, and all "Checks".

## Related blocks
`helm-chart-pitfalls`, `terraform-conventions`, `devops-conventions`, `ci-workflow-hardening`,
`runbook-writing-and-maintenance-pitfalls`, `authorization-models-and-entitlements-pitfalls`,
`slo-design`, `source-freshness`.
