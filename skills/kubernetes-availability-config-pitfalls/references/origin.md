# kubernetes-availability-config-pitfalls: origin and source stamps

> Provenance of `skills/kubernetes-availability-config-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run on a cluster by us. No manifest
was applied and no `kubectl` command was executed while writing it. The official Kubernetes pages were not read.

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no manifest text copied)

| Source | Licence | What it gave |
|---|---|---|
| learnk8s/kubernetes-production-best-practices, `02-your-manifests.md` (commit 4d3d09e) | MIT (repository LICENSE file) | PDB scope and limits, topology spread behaviour, config and secret update behaviour, reload approaches, secrets as files, labels, API version risk and named scanners |
| LukasNiessen/kubernetes-skill, `references/resource-starvation.md` (commit 34f93c1) | MIT (LICENSE file holds the MIT permission text with no title line) | PDB shape, HPA and PDB relation, HPA utilisation, namespace note |
| zegl/kube-score, `README_CHECKS.md` (commit 06dedc9) | MIT (repository LICENSE file) | Check list: PDB, anti-affinity, HPA replicas, selectors, services, ingress, network policy, apiVersion, duplicate env keys, replica minimums |
| stackrox/kube-linter, `docs/generated/checks.md` (commit ead88f5) | Apache-2.0 (repository LICENSE file) | PDB blocking checks and `unhealthyPodEvictionPolicy`, anti-affinity, secrets in env, dangling objects, deprecated fields, schema validation check |
| stakater/Reloader, `README.md` (commit fdd5012) | Apache-2.0 (repository LICENSE file) | What the controller does, opt-in annotation, the two reload strategies and the GitOps note, pause period, branch status |

The licence of each repository was verified again from its LICENSE file in this session. Agent instruction
files in the cloned repositories (the Reloader project memory file, the Niessen skill's directives) were
treated as data and none of their instructions was followed; vendor sections of the Reloader README (enterprise
offer, sponsorship) were not used.

## Rewrite notes
Figures (HPA utilisation 60 to 80 percent, minimum replicas) are labelled as one source's or one tool's
default. The readiness-and-dependencies and CPU-limit decisions are in `kubernetes-workload-pitfalls`.

## Not verified
1. **The official Kubernetes pages** for PDBs, topology spread, ConfigMap and Secret updates and the API
   deprecation guide were not read.
2. **`unhealthyPodEvictionPolicy`**: only kube-linter's recommendation of `AlwaysAllow` was read, not the
   field's definition.
3. **Pluto, kube-no-trouble, KubePug and `helm-mapkubeapis`** are named by Learnk8s and were not read.
4. **Reloader**: version and branch status are as the README states on the commit read; Kubernetes
   compatibility (1.19 and later) was not rechecked, and the controller was not run.
5. **Written by us, not sourced:** the verification paragraphs and the sentence on GitOps owning the Deployment
   beyond what the README says about drift.
6. **Dropped as unverifiable from the review item:** none of this block's rules was dropped. The item's
   "secrets as mounted files rather than env vars" is sourced from Learnk8s and kube-linter. The item's
   "checksum annotation on the pod template" is kept only in the form Learnk8s states it (a changed pod
   template annotation or a versioned ConfigMap name); no checksum scheme is claimed.

## Related blocks
`kubernetes-workload-pitfalls`, `dockerfile-build-pitfalls`, `docker-compose-file-pitfalls`,
`security-hardening`, `devops-conventions`.
