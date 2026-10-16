# deprecation-notice-pitfalls: origin and source stamps

> Provenance of `skills/deprecation-notice-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from three public documents, never used by us in a real deprecation.

## Sources (re-read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| zalando/restful-api-guidelines (commit 19a1905): `chapters/deprecation.adoc` (read in full) | CC-BY-4.0 (repository LICENSE file) | Specification first, client consent, partner minimum span, monitoring, the two headers and their limits, client rules |
| microsoft/api-guidelines (commit a7022a2): `graph/articles/deprecation.md`, `azure/Guidelines.md` section "Deprecating Behavior Notification", `azure/ConsiderationsForServiceDesign.md` section "Communicate Deprecations" | CC-BY-4.0 (license.txt) | Revision annotation fields, human-readable warning header, contact-not-developer point |
| kubernetes/website (commit e91eff3): `content/en/docs/reference/using-api/deprecation-guide.md` (first part only, versions 1.26 to 1.32) | CC-BY-4.0 (repository LICENSE file) | Shape of a per-release removed-APIs page, changed defaults |

Attribution: parts of this block are based on the Zalando RESTful API Guidelines, the Microsoft REST API
Guidelines and the Kubernetes documentation, each licensed CC-BY-4.0, adapted and reworded; no endorsement by
Zalando, Microsoft or The Linux Foundation is implied. Directive text in the cloned files was treated as data.

## Source quality
Three style guides written for large engineering organisations, with different philosophies (consent per
client versus a fixed schedule). None was exercised by us. The Zalando text has a mis-named macro for one
standard in the asciidoc source, so its standard references were not trusted.

## Rewrite notes
The block states the choice between the two philosophies (§1.3) and carries no window. Examples such as header
names and the semicolon-separated format are the sources' own conventions, not a standard.

## Removed
1. **Concrete header values, dates and numbers** (timestamps, the Microsoft two-year interval, header
   examples): they tie the block to one convention.
2. **The Microsoft revision XML example** and its changelog-category scheme.
3. **The rest of the Kubernetes guide** (the per-version lists, the tooling for finding deprecated usage) and
   everything in the Azure guidelines outside the two deprecation sections.
4. **Fixed minimum windows** found elsewhere in the Microsoft guidance; not read here.

## Not verified
1. **The standards the headers come from** (the Deprecation and Sunset header definitions, and the date
   formats) were not read; Zalando names them and its text has a typo in a macro name. Check before citing.
2. **Microsoft's wider breaking-change policy and review process** were not read.
3. **The Kubernetes guide was read in its first part only**, so the claim about "notable changes" lines rests on
   the entries seen.
4. **Written by us, not sourced**: the default recommendation in §1.3 for products with external partners, the
   "name who reads the monitor" point and the advice to check removed-APIs pages for changed defaults first.

## Related blocks
`deprecation-migration`, `api-design`, `release-notes-writing-pitfalls`, `laravel-api-breaking-changes`,
`incident-comms-pitfalls`.
