# kubernetes-access-and-exposure-pitfalls: origin and source stamps

> Provenance of `skills/kubernetes-access-and-exposure-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run on a cluster by us: no manifest was applied and no
`kubectl` command was executed while writing it. Every file below was re-read in full on 2026-10-16 before a
rule was taken from it, including the whole Pod Security Standards page (581 lines), and each repository's
LICENSE file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| kubernetes/website (commit `e91eff3`), `content/en/docs/concepts/security/rbac-good-practices.md` | CC BY 4.0 (LICENSE file: Creative Commons Attribution 4.0 legal text); credit given in the block and in each file that draws on it | Least privilege, token distribution, hardening, the privilege-escalation paths, the object-creation denial of service |
| the same repository, `content/en/docs/concepts/security/secrets-good-practices.md` | CC BY 4.0 | Access to Secret objects, pods that mount a Secret, per-container mounts, base64 manifests, etcd, external stores |
| the same repository, `content/en/docs/concepts/security/pod-security-standards.md` | CC BY 4.0 | The three profiles, the Baseline and Restricted field-level controls and allowed values, OS-specific controls, FAQ |
| ahmetb/kubernetes-network-policy-recipes (commit `11f5018`), `01-deny-all-traffic-to-an-application.md` | Apache-2.0 (repository LICENSE file: Apache License 2.0 text) | Deny-all policy shape, use cases, additive policies |
| stackrox/kube-linter (commit `ead88f5`), `docs/generated/checks.md` | Apache-2.0 (repository LICENSE file) | The checks that map to the rules, their default status, the CIS items they cite |

Attribution for the CC BY 4.0 material: pages "Role Based Access Control Good Practices", "Good practices for
Kubernetes Secrets" and "Pod Security Standards", © The Kubernetes Authors, from github.com/kubernetes/website,
licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes: rephrased, condensed and
reorganised into numbered rules; the pod spec sample in §3.2 and the sample commands are our own. No
endorsement by the Kubernetes Authors is implied. Links in the pages (RBAC reference, encryption at rest,
Pod Security admission) were not followed.

## Removed in the verification pass
1. **"Turn off service account token auto-mount where the pod does not call the API"**: kept, but the page
   words it as avoiding the default auto-mounting, with the pod-level setting overriding the account's
   (§1.2).
2. **The lint checks were reduced to ones whose names and descriptions are in the check list**, with their
   default status as that file states it. The review's "default service account" check is `off` by default
   and is stated that way (§4.3).
3. **"A policy with no ingress rules drops all traffic"**: the recipe's remarks say the field is missing
   while its manifest sets an empty list; the block states both and tells the reader to test (§4.1).
4. **Not read, so not used**: the Kubernetes RBAC reference, Pod Security admission page, encryption at rest
   task, network policies concept page, and the remaining recipes of the network policy repository.
5. **Pod Security Standards field rules**: all Baseline and Restricted controls of the page are carried,
   with the page's version labels; nothing was added from memory. The FAQ points on profiles, security
   contexts and sandboxed pods are carried in short form (§3.5).

## Not verified
1. **Every version number** in §3 (v1.8, v1.19, v1.22, v1.23, v1.25, v1.26, v1.34 and the sysctl and SELinux
   additions) is as the page states it on 2026-10-16; the Kubernetes release history was not checked.
2. **How a Pod Security profile is enforced** (namespace labels, modes) was not in the page read and is not
   claimed; only the names of the admission controller and the third-party alternatives are repeated.
3. **NetworkPolicy semantics beyond the recipe** (policy types, egress, plugin support) were not read. The
   recipe's remark and example differ on the `ingress` field.
4. **kube-linter default status** is that of commit `ead88f5`; the check list changes between releases.
5. **Written by us, not sourced:** the verification paragraphs, the sample pod spec (§3.2, built from the
   page's allowed values), the remark that `runAsNonRoot: true` needs a non-root image (§3.2 and §3.5), the
   plugin-enforcement caveat (§4.2), the advice to use the linter and admission together (§4.3), and the
   `kubectl auth can-i` checks.

## Related blocks
`kubernetes-workload-pitfalls`, `kubernetes-availability-config-pitfalls`, `dockerfile-build-pitfalls`,
`docker-compose-file-pitfalls`, `security-hardening`, `credential-lifecycle-pitfalls`.
