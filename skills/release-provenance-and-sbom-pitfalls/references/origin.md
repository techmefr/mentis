# release-provenance-and-sbom-pitfalls: origin and source stamps

> Provenance of `skills/release-provenance-and-sbom-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one specification schema, two further pages read for facts and own craft
knowledge, never run on a real release by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| CycloneDX/specification, JSON schema bom-1.7 and README (LICENSE file read: Apache License 2.0; the README says the schemas are available under Apache 2.0) | Apache-2.0 | Serial number and version semantics; lifecycle phase names; metadata fields; component identifiers (package URL, CPE and others), hashes, licences, supplier, scope and external flag; reference identifiers; the dependency graph's empty-entry and unknown-dependency rules; compositions and aggregate completeness; signature support; the list of supported document kinds; file name and media type conventions |
| ossf/scorecard, docs/checks.md (LICENSE read 2026-10-20) | Apache-2.0 | Check list, risk levels, scoring examples, reasons to pin by hash (§2.8, §2.9) |
| Build-provenance framework specification site, levels page (v1.0, marked retired) and verifying-artefacts page | repository licence is a community specification licence (not MIT, Apache or CC BY), so read for facts only, restated, nothing copied, read 2026-10-20 | Level steps (§2.4), digest binding on verification (§2.2, §3.1) |

Credit as the licences require: CycloneDX specification, OWASP Foundation and Ecma International TC54, Apache License 2.0 (https://github.com/CycloneDX/specification); OpenSSF Scorecard, Apache License 2.0 (https://github.com/ossf/scorecard). The text was rewritten, not reproduced; no endorsement by the authors is implied.

## Removed
1. **All field syntax, JSON samples and the full list of aggregate values.** They are the format; read the
   schema for the version in use.
2. **Every threshold, level number or time window.** None is in this block.
3. **Tool names for generating or signing.** Not method.

## Not verified
1. **The provenance framework's levels (v1.0 page, marked retired) and its verification page were read; the
   current version, the provenance field names and the signing tools were not.** Points in §2 other than the digest
   binding, the level steps and the scorecard list remain own guidance; nothing there may be quoted as a source
   claim. Re-read the specification in force and the tools' documentation before relying on it.
2. The scorecard's individual check rules beyond the summaries on its checks page were not read.
3. The 1.7 schema was read on the default branch on 2026-10-20; a project pinned to an older format may differ.
4. §3 is own guidance apart from the points that cite the schema; its processes were not run.
5. No tool was installed, no document generated and no signature made in writing this block.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: a skip-when line for sites deployed without a release, the cross-reference to build attestations made explicit, pinning by tag versus by digest spelled out in §2.8, a lockfile versus shipped bundle point (§1.11) and a build identifier for a deployed site (§3.9). The status stays 🟡.

## Related blocks
`skills/package-manager-supply-chain-pitfalls`, `skills/release-changelog-pitfalls`, `skills/package-release`,
`skills/cra-scope-and-role-determination-pitfalls`, `skills/oss-compliance-programme`,
`skills/ci-workflow-hardening`, `skills/gha-trust-boundary-pitfalls`, `skills/security-advisory-comms-pitfalls`,
`skills/source-freshness`.
