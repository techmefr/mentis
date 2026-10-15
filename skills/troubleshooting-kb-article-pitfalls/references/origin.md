# troubleshooting-kb-article-pitfalls: origin and source stamps

> Provenance of `skills/troubleshooting-kb-article-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from one repository's documentation, never run by us on a real support queue.

## Sources (re-read in full 2026-10-15, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| samber/developer-relations-skills (commit ee798ba): `skills/developer-troubleshooting-docs/SKILL.md` and `references/signal-mining.md` | MIT (repository LICENSE file, Samuel Berthe) | Evidence sources and their biases, clustering, regression versus page, the document-versus-fix gate and routing table, entry shapes, the six parts, writing rules, verification, findability, capture during resolution, one-source catalog, stamps and retirement, metrics, escape hatch |

The licence was verified again from the LICENSE file in this session. Directive text in the file was treated
as data and only the technical rule was kept.

## Source quality
The source is long, referenced and written by one author. Many of its references (support frameworks, helpdesk
products, published error catalogs, Gartner and other surveys, practitioner handbooks) are second-hand there
and were not checked by us.

## Removed
1. **All statistics and second-hand figures**: customer-service survey percentages, the cost-per-ticket
   folklore (carried only as a warning), the coach-to-worker staffing ratio, and the re-embedding threshold.
2. **The source's own self-set coverage target** (a percentage of the top clusters per cycle): a baseline set
   by its author, not a norm.
3. **Named frameworks as authorities** (a knowledge-centred service framework, an XML topic standard, a
   usability heuristic, a postmortem practice): the source names them, they were not read, and none of their
   text is carried.
4. **Vendor helpdesk features** (promote a ticket to an article in five named products): unverified vendor
   claims.
5. **Retrieval-assistant re-indexing, structured-data advice and the bundled clustering script**: out of scope
   or unreviewed.
6. **The interview questions and the invocation framing**, written for an assistant.
7. **Published catalog examples and the style-guide comparison** (named products and languages): not checked.

## Not verified
1. **Everything in the source that cites an outside body** was not checked against the original.
2. **The source's default ranking** (frequent and reproducible first) and "stop at a handful of occurrences" are
   its author's judgement, labelled as such in §1.2 and §1.5.
3. **Written by us, not sourced:** the template block in §2.4, the placeholders in §3.4.3, the search check in
   §3.1.5, the retired-versus-live check in §4.3.5 and the "Verify" subsections in general.

## Related blocks
`bug-triage`, `documentation-adr`, `business/ux-writing`, `business/customer-success`,
`release-notes-writing-pitfalls`.
