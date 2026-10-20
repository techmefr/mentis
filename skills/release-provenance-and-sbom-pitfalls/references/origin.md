# release-provenance-and-sbom-pitfalls: origin and source stamps

> Provenance of `skills/release-provenance-and-sbom-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one specification schema and own craft knowledge, never run on a
real release by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| CycloneDX/specification, JSON schema bom-1.7 and README (LICENSE file read: Apache License 2.0; the README says the schemas are available under Apache 2.0) | Apache-2.0 | Serial number and version semantics; lifecycle phase names; metadata fields; component identifiers (package URL, CPE and others), hashes, licences, supplier, scope and external flag; reference identifiers; the dependency graph's empty-entry and unknown-dependency rules; compositions and aggregate completeness; signature support; the list of supported document kinds; file name and media type conventions |

Credit as the licence requires: CycloneDX specification, OWASP Foundation and Ecma International TC54, Apache
License 2.0 (https://github.com/CycloneDX/specification). The text was rewritten, not reproduced; no
endorsement by the authors is implied.

## Removed
1. **All field syntax, JSON samples and the full list of aggregate values.** They are the format; read the
   schema for the version in use.
2. **Every threshold, level number or time window.** None is in this block.
3. **Tool names for generating or signing.** Not method.

## Not verified
1. **The provenance framework (SLSA), its levels and its terms, and the signing tools were not read.** The
   whole of §2 is own guidance from general knowledge; nothing in it may be quoted as a source claim. Re-read the
   specification and the tools' documentation, and check their licences, before relying on it.
2. The licence of a repository-practices scoring tool and the checks it makes were not read.
3. The 1.7 schema was read on the default branch on 2026-10-20; a project pinned to an older format may differ.
4. §3 is own guidance apart from the points that cite the schema; its processes were not run.
5. No tool was installed, no document generated and no signature made in writing this block.

## Related blocks
`skills/package-manager-supply-chain-pitfalls`, `skills/release-changelog-pitfalls`, `skills/package-release`,
`skills/cra-scope-and-role-determination-pitfalls`, `skills/oss-compliance-programme`,
`skills/ci-workflow-hardening`, `skills/gha-trust-boundary-pitfalls`, `skills/security-advisory-comms-pitfalls`,
`skills/source-freshness`.
