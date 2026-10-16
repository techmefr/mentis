# vendor-claims-and-scoring-pitfalls §2 — Claims and evidence

> Section 2 of `skills/vendor-claims-and-scoring-pitfalls`. Read it when a vendor claim is being checked.
> Sourced from the evidence model of salespeak-ai/buyer-eval-skill (commit `ebb0e06`,
> `references/evidence-model.md`), read 2026-10-16. The source has telemetry and a vendor-hosted service
> elsewhere in the repository; only its evidence method is used. Sentences marked "own guidance" are ours.

## Pick the claims worth checking
1. **A claim is specific and checkable and bears on a buyer criterion.** "Native two-way sync with a named
   product" is a claim; a slogan or an adjective with nothing to check is not. Questions the vendor makes no
   statement about go in a list of things to get answered before signing, not in the claims table.

## Type every source by who controls it
2. **Five types:** a vendor claim (made to persuade: product and marketing pages, case studies, press
   releases, marketplace listings the vendor wrote); vendor documentation (first-party material that commits
   the vendor to specifics: technical docs, security pages naming certifications, public prices, published
   terms); independent evidence (not controlled by the vendor or its competitors: reviews read on the review
   site, analyst work, reputable press, registries); competitor content; and buyer-supplied evidence
   (proposals, trial results, questionnaires).
3. **Type by relationship to the claim.** A vendor's own "us versus them" page is a vendor claim about itself
   and competitor content about the rival.
4. **A vendor's own assistant is a vendor claim.** Its answer verifies nothing; if it cites documentation,
   fetch that and classify it on its merits.
5. **Competitor content is a lead, never proof.** It becomes a question to check elsewhere or to put to the
   vendor, and is never counted as independent.

## What each type can verify
6. **Vendor documentation verifies narrow, self-describing facts:** that an endpoint exists, that the vendor
   states it holds a certification. It cannot verify outcomes such as time to value, savings or ease of use;
   those need independent or buyer evidence.
7. **Corroboration must be independent.** Several sources repeating one upstream count as one. A review site
   that restates the vendor's own terms does not corroborate them.
8. **A negative claim** ("no setup fee", "no guarantee required") is verified only by a source that commits
   the vendor, such as contract text or a fee schedule. A marketing or FAQ line alone is at most vendor
   documentation, and the report says the contract was not read.
9. **Buyer evidence is strong but specific.** A proposal verifies what that vendor offered this buyer; it
   contradicts a general claim only where the buyer's situation is the one the claim covers.
10. **Self-reported company figures are labelled** as reported by the named source and unaudited.

## Read the page, ask neutral questions
11. **Read the source, not a snippet.** Search snippets and generated summaries are leads. If a page is
    blocked, record it as not accessible; a tool limit is a gap, not a finding.
12. **Ask a fetch tool for verbatim quotes, never a yes or no.** A summarising tool can echo your question as
    if the page said it. Ask it to quote what the page says on a topic; treat anything asserted without quoted
    text as not found, and base a deciding fact on quoted words.

## Statuses
13. **Verified** (enough supporting evidence of the right type; a vendor claim alone never qualifies),
    **qualified** (true in the main case with a material limit, such as a plan tier or add-on),
    **contradicted** (credible evidence conflicts with the claim; name the source), **unverified** (not enough
    corroboration found, not a negative finding) and **unknown** (part checks out, the part that matters cannot
    be assessed). Own guidance: write the evidence basis next to the status so a reader never mistakes vendor
    documentation for independent confirmation.

## Before you finish
14. **Challenge your own conclusion.** The source's pass asks, in substance: what would make the apparent
    winner wrong, which weakly supported claim carries the conclusion, whether polished vendor content is
    being rewarded over plain independent evidence, whether contrary customer experience was sought for every
    vendor and not only the loser, whether hidden constraints exist (tiers, add-ons, services, minimums,
    migration, hosting), and whether any vendor got a stricter or looser standard. Report only what changed a
    finding.
15. **List the open questions** the buyer must have answered before signing.
