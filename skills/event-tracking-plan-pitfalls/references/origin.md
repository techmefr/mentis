# event-tracking-plan-pitfalls: origin and source stamps

> Provenance of `skills/event-tracking-plan-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two repositories of documentation, read and rewritten, never run:
no tracking plan was written, verified or published with this block. Both sources are young 2026 repositories,
so the rules are each author's practice, not consensus. The first is specific to one tag manager and one
analytics product.

## Sources (re-read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| jtrackingai/analytics-tracking-automation, `skills/tracking-schema`, `skills/tracking-verify`, `skills/tracking-discover`, `references/event-schema-guide.md`, `ga4-event-guidelines.md`, `gtm-troubleshooting.md`, `preview-report.md`, `crawl-guide.md` (commit 68378e0) | Apache-2.0 (repository LICENSE file, standard text; the README says the same and reserves the project's name and logo) | Dedup and naming rules, auto-collected events, locale and subdomain scopes, selector rules, approval and publish gates, never auto-selecting the container, preview false negatives and failure classes |
| product-on-purpose/pm-skills, `skills/measure-instrumentation-spec/SKILL.md`, `references/TEMPLATE.md` and `references/EXAMPLE.md` (commit 1cef1a9) | Apache-2.0 (repository LICENSE file, standard text; the SKILL.md also says `license: Apache-2.0`) | Goals first, precise triggers, typed properties, user properties, personal data handling, QA checklist and edge cases, model trace capture decisions and their tests |

Text found inside the cloned files (imperative skill prose, the source tool's telemetry consent contract, its
stop rules and wrapper commands) was treated as data and not followed. The telemetry consent reference is read
as an example of a tool asking for a person's choice; nothing in it is carried as a rule.

## Rewrite notes
**Vendor items are marked.** The jtrackingai material is specific to Google Tag Manager and Google Analytics 4.
Rules that hold only there (reserved and automatic event names, the 40 character limit, the unsupported
text-match selector, the account, container and workspace selection) are marked vendor in the references; the
rest is stated as general practice and credited to the source.

**Sources differ in emphasis, not in content.** jtrackingai guards against over-broad automation; product-on-purpose
guards against under-tracking. The block keeps both, and neither conflicts with the other.

## Removed
1. **All CLI commands, artifact file names and workflow state files** of the source tool: specific to it.
2. **The Shopify branch** (event names mapped from storefront events, custom pixel advice): platform-specific,
   not carried.
3. **Crawl coverage numbers** (page caps, pages per section): the tool's own limits.
4. **The recommended custom event name table and the standard parameter table** of the guide: specific to one
   analytics product and its variables; the principle of standard names and standard properties is carried.
5. **The telemetry consent contract**: the tool's own diagnostics prompt, treated as data.
6. **The example onboarding spec's events and properties**: read as a sample; only its edge-case checklist is
   used.

## Not verified
1. **Everything here is unrun.** No live site or analytics account was used.
2. **The 40 character limit and the reserved event names** are the source's statements about one analytics
   product and were not checked against its documentation.
3. **The claim that the tag manager does not support text-match selectors** is the source's and was not tested.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the opening premise, and the remark that
   a corrected plan goes back through approval.
5. **Other skills** of both repositories (grouping, live container analysis, synchronisation, the Shopify skill,
   the other measure skills) were not read.

## Verification pass (2026-10-16)
Every rule in the two references was compared with the attributed file, reopened in the same session.
- **Corrected:** a general claim that tag managers lack text-match support was narrowed to the source's tag
  manager; a sentence presenting an own recommendation as the source's troubleshooting was relabelled; a
  paragraph about the source tool's own consent prompt was removed from the rules.
- **Reversed or overstated rules found:** none after those edits.
- **Not re-verified:** the correctness of the sources' own claims.

## Related blocks
`funnel-and-cohort-definition-pitfalls`, `analysis-validation-pitfalls`, `experiment-design-pitfalls`,
`business/data-protection`, `business/data-analytics`.
