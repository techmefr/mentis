# gdpr-breach-notification-and-dpia-pitfalls: origin and source stamps

> Provenance of `skills/gdpr-breach-notification-and-dpia-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from a regulation text only, never run by us: no breach was handled and
no assessment was produced with it. This block is a working method, not legal advice, and it does not replace the
DPO or a qualified lawyer.

## Sources (all read 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Regulation (EU) 2016/679, Article 33, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 | Official text of the European Union, reused with mention of the source | Notice to the authority without undue delay and the time limit from awareness, delay reasons, processor hand-off, minimum content, phased information, the documentation duty |
| Same, Article 34 | same | Communication to the data subject when high risk is likely, its plain-language form and content, the three conditions that remove the duty, the authority's power |
| Same, Article 35 | same | When an assessment is required (general rule and three named cases), DPO advice, authority lists, minimum content, codes of conduct, views of the people concerned, the legal-basis exception, the review |
| Same, Article 36(1) to (3) | same | Prior consultation after an assessment indicating high risk, the authority's response periods and what the controller supplies |

The text was read in a real browser (EUR-Lex answers an empty HTTP 202 to curl and to the fetch tool) and is the
version published in the Official Journal of 4.5.2016, not a consolidated or corrected one.

## Removed
1. **Interpretation of "aware", "risk", "high risk", "large scale", "disproportionate effort".** The text read
   does not define them in these articles; they are routed to the DPO.
2. **Any figure not in the text read** (alert thresholds, drill frequency, template lengths): none is given; they
   belong to the user's own policy.
3. **Guidance of the Board or of any authority** on breach examples, notification practice or the criteria for an
   assessment. Not read.
4. **Article 36(4) and (5)** (legislative proposals, Member State prior authorisation): read, not used, out of an
   engineering method's scope.

## Not verified
1. **Consolidated version, corrigenda and amending acts** were not checked; the block tells the reader to read the
   current text before relying on a period.
2. **Recitals**, which bear on how the articles are read, were not read.
3. **National law**, authority lists under Article 35(4) and (5), the name of the competent authority under
   Article 55, and any sector-specific notification duty (other regimes with their own incident rules) were not
   checked.
4. **Own guidance, flagged in the text:** the awareness timestamp field, the delay-reason field, the case-based
   processor hand-off, the open-facts list, the register entry for non-notified breaches, the drill, the
   per-population channel plan, the single case record as source of every text, the recorded trigger form, the
   written DPO request, the review triggers and the release dependency on a consultation.
5. **Source quality:** a single regulation text; no practitioner guide was used.

## Related blocks
`business/data-protection`, `skills/dpa-review-pitfalls`, `skills/dsar-handling-pitfalls`,
`skills/incident-comms-pitfalls`, `skills/blameless-incident-review-pitfalls`, `skills/source-freshness`,
`skills/gdpr-international-transfers-pitfalls`.
