# gdpr-international-transfers-pitfalls: origin and source stamps

> Provenance of `skills/gdpr-international-transfers-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from a regulation text only, never run by us: no flow was inventoried and
no vendor was reviewed with it. This block is a working method, not legal advice, and it does not replace the DPO
or a qualified lawyer.

## Sources (all read 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Regulation (EU) 2016/679, Article 44, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 | Official text of the European Union, reused with mention of the source | The general principle, including onward transfers |
| Same, Article 45 | same | Adequacy decisions, their scope, periodic review, repeal and publication, carry-over of older decisions |
| Same, Article 46 | same | Appropriate safeguards, the ones needing no specific authorisation and the ones needing the authority, carry-over of older authorisations |
| Same, Article 47 | same | Binding corporate rules: approval, minimum conditions, content list |
| Same, Article 48 | same | Foreign judgments and decisions requiring transfer or disclosure |
| Same, Article 49 | same | Derogations for specific situations, their limits, the last-resort case, the documentation duty |

The text was read in a real browser (EUR-Lex answers an empty HTTP 202 to curl and to the fetch tool) and is the
version published in the Official Journal of 4.5.2016, not a consolidated or corrected one.

## Removed
1. **The content of any adequacy decision or list of countries.** Not read; the DPO supplies the current list.
2. **Standard clauses, their modules and annexes.** Not read; only the existence of the instrument in Article
   46(2) is stated.
3. **Any assessment of third-country law and any "supplementary measures" method.** Not in the articles read; the
   block routes the question and concludes nothing.
4. **Every figure not in the text read** (review cadences of tools, questionnaire lengths): none is given. The
   four-year review in Article 45(3) is the one period stated, from the text.
5. **Interpretation of "transfer"** for remote access or support access: the article read does not define it;
   routed to the DPO.

## Not verified
1. **Consolidated version, corrigenda and amending acts** were not checked.
2. **Recitals** were not read.
3. **Commission decisions, Board guidance, authority guidance and case law** on transfers were not read.
4. **National law**, and the name of the competent authority, were not checked.
5. **Own guidance, flagged in the text:** the inventory checklist of dull flows, the register fields, the
   sub-processor change as register event, the vendor location questions, the design-time check, the evidence
   discipline, the per-mechanism questions, the plan for a withdrawn decision, the handling of a foreign demand,
   the escalation file and the live-flow-without-mechanism rule.
6. **Source quality:** a single regulation text; no practitioner guide was used.

## Related blocks
`business/data-protection`, `business/vendor-management`, `business/regulatory-watch`,
`skills/dpa-review-pitfalls`, `skills/dsar-handling-pitfalls`, `skills/gdpr-breach-notification-and-dpia-pitfalls`,
`skills/source-freshness`.
