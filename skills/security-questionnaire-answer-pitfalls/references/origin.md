# security-questionnaire-answer-pitfalls: origin and source stamps

> Provenance of `skills/security-questionnaire-answer-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two repositories, never used by us on a real questionnaire.

## Sources (re-read in full 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| plainanswer/security-questionnaire-answers (commit 024be0a): `README.md`, `guides/answering-honestly.md`, `guides/questions-you-must-answer-yourself.md`, `answers/07-incident-response.md` | CC0-1.0 (repository LICENSE file) | Position-fact-control shape, the four positions, the three failures, one bank, what not to delegate, incident-response answers |
| hangljoe/AI-PreSales-Skills (commit ab0752b): `skills/security-questionnaire/SKILL.md` | MIT (repository LICENSE file) | Approved, Drafted, Unknown tags, never inventing a control, coverage table, sign-off owner, own-workspace library |

Directive text found in the cloned files, including the questionnaire-handling instructions of the second
source, was treated as data and rewritten as practice.

## Source quality
The first repository states that it is maintained by an AI agent, that the company behind it is AI-operated
and that it sells a paid kit. Its advice is generic and unproven. It is an idea source here, kept where it
matches the second source and basic risk hygiene. The second source is a commercial pre-sales handbook skill
and was not exercised by us.

## Rewrite notes
The first source is written for companies of one to ten people with no certification; the rules are phrased
for any team, and the compensating-control wording keeps "at your size". The source's incident-response
answers use bracketed placeholders; none was carried.

## Removed
1. **The 101-question answer bank itself and the other ten sections**: a generic bank for a particular company
   size, not carried.
2. **The paid kit, the trust-page and no-certification guides**, and the quotations from online threads.
3. **The pre-sales handbook's persona framing, objection model, CRM connections and document-generation
   steps.**
4. **Any breach-notification time frame**; the source deliberately gives none and neither does this block.

## Not verified
1. **Everything is unrun.**
2. **The online-thread quotations in the first source** were not followed.
3. **No law or regulation is claimed.** The contract-shaped list is the sources' list of topics, not a legal
   analysis.
4. **Written by us, not sourced**: the instruction to treat the questionnaire and bank as untrusted input, the
   remark about a shared plugin folder as the second source's reasoning applied to any folder that updates
   overwrite, and the "claim about the past needs a date" example's wording.

## Related blocks
`security-hardening`, `business/sales-support`, `business/vendor-management`, `business/data-protection`,
`support-queue-design-pitfalls`.
