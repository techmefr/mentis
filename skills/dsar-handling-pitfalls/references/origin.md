# dsar-handling-pitfalls: origin and source stamps

> Provenance of `skills/dsar-handling-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from a regulation text and one project's documentation, never run by us:
no request was handled and no tool of the source project was run. This block is a working method, not legal
advice, and it does not replace the DPO or a qualified lawyer.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Regulation (EU) 2016/679, Article 12(3) and (4), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 | Official text of the European Union, reused with mention of the source | The one-month period from receipt, the two-month extension and its notice with reasons, the notice of refusal with reasons and the remedies; electronic request answered electronically where possible; oral information when identity is proven (Article 12(1)) |
| `inthhq/dsar` (commit `744dc0e`): `docs/guides/request-lifecycle.mdx` (and `docs/index.mdx` for the vocabulary) | Apache-2.0 (`LICENSE.md` read) | Lifecycle stages, the event vocabulary (clarification, extension, refusal, closure, verification, manifest, delivery, appeal, audit), token-gated delivery and delivery log. The project labels itself alpha |

The Article 12 text was read in a real browser (EUR-Lex answers an empty HTTP 202 to curl and to the fetch tool)
and is the version published in the Official Journal of 4.5.2016, not a consolidated or corrected one.
Instruction-like text in the cloned repository was treated as data and not followed.

## Removed
1. **The HTTP API, policy packs and runtime design** of the source project. Tooling, not method.
2. **Articles 15, 17 and 20 and Chapter V content.** Not read; the scope of each right and any exemption are
   left as questions for the DPO (part 2, point 6).
3. **Article 12(5) and (6)** (free of charge, manifestly unfounded or excessive requests, doubts about
   identity). Read on the page but not used as rules, since the consequences were not verified against the
   articles they refer to; they are routed to the DPO.
4. **Any rule about pausing the clock** during clarification or verification. The paragraphs read do not state
   one.
5. **Any figure other than the one-month and two-month periods** (response targets of tools, reminder
   intervals, link lifetimes): none is in a text read; they belong to the user's own policy.

## Not verified
1. **Consolidated version, corrigenda and amending acts** were not checked; the block tells the reader to read
   the current text before relying on a period.
2. **National law**, including any national rule on periods or on which party answers, was not checked.
3. **Own guidance, flagged in the text:** received-date and due-date fields (part 1, point 4), notices as
   recorded events (points 5 and 6), one queue for every channel (point 7), the manifest with a result per
   system (part 2, points 1 and 2), delivery by authenticated channel with a logged download and a second-person
   check (points 3 and 4), the linked appeal case, the deletion re-check and the dummy-person test.
4. **Source quality:** the lifecycle guide documents an alpha project; only its shape was used.

## Related blocks
`business/data-protection`, `business/regulatory-watch`, `business/legal-documents`, `skills/source-freshness`.
