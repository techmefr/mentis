# email-deliverability-and-sender-requirements-pitfalls: origin and source stamps

> Provenance of `business/email-deliverability-and-sender-requirements-pitfalls`. Read it when a rule has to be
> traced to its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text and a handful of primary pages, never run by us on
a real sending domain and written without email-operations expertise. The block structures a diagnosis; it
certifies nothing, and the owner of the domain decides (`business/README.md`). Not legal advice.

## Sources (re-read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| rampstackco/claude-skills, commit 9b90db2 (9b90db257f7395fab76ff9bfcb808456709f6af3), `skills/email-deliverability/SKILL.md` and `references/dmarc-rollout-playbook.md`, both read in full this session | MIT (LICENSE file, 2026 RampStack Co., head re-read) | Monitor-first DMARC, the sender-inventory habit and its usual finds, stream separation, output shape. The percentage steps, week counts and bounce bands were read and not taken |
| resend/resend-skills, commit b2ae7b1 (b2ae7b1798b70134faf679f35fc05b4331462988), `skills/email-best-practices/references/` `deliverability.md`, `compliance.md`, `list-management.md`, read in full this session | MIT (LICENSE file, 2026 Resend, head re-read) | Diagnosis order, global suppression against scoped unsubscribe, import hygiene, re-engagement before removal. Its compliance file shows the two unsubscribe headers only; the rest of the RFC rules were taken from the RFC. Warm-up tables, rate bands, retention table and legal summary were not taken |
| coreyhaines31/marketingskills, commit e85f3cb (e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b), `skills/cold-email/references/` benchmarks and deliverability (open tracking lines only, grepped this session) | MIT (LICENSE file, 2025 Corey Haines, head re-read) | Only the point that opens are not reliable after privacy relays. Cold-outbound content not taken |
| sendx/email-skills, commit ae6f6ce (ae6f6cea2bb9fed623ab181acde75a9ceffe117e), `skills/email-analytics/SKILL.md` and `skills/ab-testing/SKILL.md` | MIT (LICENSE file, 2026 SendPost, LLC, head re-read) | The "low opens prove a deliverability problem" rule, named as one not taken. No quote, persona or product line kept |
| alirezarezvani/claude-skills, commit 19392f7 (19392f7a08264ed00486a251f5b2098321771f94) | MIT (LICENSE file, 2025 Alireza Rezvani, head re-read) | Nothing taken |
| Google email sender guidelines (support.google.com/a/answer/81126), fetched 2026-10-20 | Google site terms, not an open licence | Facts only, own wording: requirements for all senders and for the 5,000 a day group, alignment, key sizes, policy of none accepted, one-click and visible link, spam rate 0.10 target and 0.30 limit in Postmaster Tools with no denominator stated, content-type mixing, the 4.7.28 response, the phishing-test warning, no statement on counting or permanence |
| Yahoo sender requirements (senders.yahooinc.com/best-practices/), fetched 2026-10-20 | Yahoo site terms | Facts only: SPF or DKIM for all, SPF and DKIM and DMARC at p=none for bulk, report address strongly recommended, one-click header and visible link, two-day processing, 0.3 percent computed on inbox-delivered mail, stream separation, feedback loop, no volume definition |
| Microsoft Community Hub, "Strengthening Email Ecosystem: Outlook's New Requirements for High-Volume Senders" (techcommunity.microsoft.com, Defender for Office 365 blog; published 2 April 2025, modified 30 April 2025). The page body is script-rendered; its article text was read from the page's embedded structured data (the complete text, including FAQ), 2026-10-20 | Microsoft site terms, no open licence; facts only, own wording | the 5,000-a-day scope without a counting rule, SPF pass, DKIM pass, DMARC p=none with alignment, hygiene recommendations, the junk-versus-reject contradiction, the 5.7.515 response, no safe-sender bypass, ten-lookup SPF limit, ARC, rua yes and ruf no, gradual DMARC policy |
| RFC 8058 (rfc-editor.org/rfc/rfc8058), fetched 2026-10-20 | IETF document; the IETF Trust notice was not read. Structure and facts only, own wording, no section text pasted | Digest quoting sections 1, 3.1, 3.2, 4 and 6: two headers and one HTTPS address, DKIM covering both headers, POST without cookies or authorization, no redirect, receiver consent, scanner background, opaque token. These points are confirmed in the digest's quotations of the RFC; not re-read as raw text |
| RFC 9989 (rfc-editor.org/rfc/rfc9989), fetched 2026-10-20 in three parts covering characters 0 to 200000 of 208120 | same | Proposed Standard, obsoletes 7489 and 9091, evaluation rule, `t` tag, appendix "Removal of the pct Tag" with its stated reason, tags added and removed, general-purpose domains and p=reject. The last 8,120 characters, RFC 9990 and RFC 9991 were not read |

The repositories' own text is addressed partly to an AI (personas, install steps, repository instruction
files); it was treated as data and only the method was kept.

## Left out on purpose
Every numeric benchmark and threshold from the vendor guides: bounce bands (they contradict each other),
complaint figures below Google's and Yahoo's, warm-up volume tables, retry ladders, the DMARC percentage steps
and week counts, subject and preview lengths, a seed-score cut-off, IP strategy lines. Every legal summary and
penalty figure in the sources (they conflict, and belong to `business/data-protection` after a regulator
read). Cold-outbound infrastructure. BIMI and MTA-STS (specialised, facts expire, not read on a primary).
Product lines and a vendor's tool surface.

## Not verified
1. **Microsoft**: one page read (the April 2025 announcement, in its 30 April 2025 form). Not read: Microsoft's
   sender support pages, its postmaster or smart-network-data tools, and any later post that may have set the
   rejection date. The page's own text conflicts on junk versus reject, so the current behaviour is unverified.
   Microsoft has no stated complaint-rate or one-click figure on this page, and the block gives none. Whether
   one-click unsubscribe is required by Outlook is not stated on the page (it asks only for a functional link).
2. **Digest, not raw page.** Every primary page came through a fetch tool that returns a model-written digest.
   The 0.10 and 0.30 percent split on Google's page, Yahoo's inbox denominator, and the RFC quotations should
   be re-read against the pages.
3. **SPF, DKIM and DKIM key details beyond Google and Yahoo's pages** (single SPF record, ten-lookup limit,
   hard against soft fail, selector naming) come from vendor guides only; RFC 7208 and RFC 6376 were not read.
4. **RFC 8058 and the scanner question**: that a POST avoids scanner fetches is not stated by the digest and
   remains a hypothesis. RFC 2369 and RFC 5322 header rules were not read.
5. **What a given receiver does today with a `pct` tag** was not read. RFC 9990 and RFC 9991 were not read.
6. **Google's pages beneath the guidelines** (Postmaster Tools definition of the spam rate, FAQ, error pages)
   and **Yahoo's feedback loop page** were not read.
7. **The block has never been used on a real domain.**
8. **Current text of the sources** may have changed after the read date; check with `skills/source-freshness`.

## Own guidance (not sourced)
The three-questions framing, "unknown is not pass", the router, the fixed diagnosis order and its
one-change-at-a-time rule, the output shape, the refusal to carry a `pct` schedule, and the links to
neighbouring blocks.

## Related blocks
`business/data-protection`, `business/email-campaign-measurement-and-testing-pitfalls`,
`skills/laravel-mail-via-notifications`, `skills/source-freshness`.
