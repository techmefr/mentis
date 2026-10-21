# ai-product-ux-pitfalls: origin and source stamps

> Provenance of `skills/ai-product-ux-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Never dogfooded. Nothing was run, built or tested with users while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| W3C WCAG 2.2 Understanding pages: Status Messages (4.1.3), Error Prevention (3.3.4), Pause, Stop, Hide (2.2.2), Error Identification (3.3.1), Timing Adjustable (2.2.1); levels re-read: 4.1.3 and 3.3.4 AA, 2.2.2, 3.3.1 and 2.2.1 A | W3C Document License (terms read; copying allowed with attribution, no derivative texts), used for facts only | Status messages announced without focus (§2.2.4); reversible, checked or confirmed submissions (§1.1.5); pause, stop, hide for auto-updating content (§2.2.4) |
| Anthropic: citations, streaming messages and handle-streaming-refusals pages; OpenAI: streaming-responses and file-search guides | Product documentation, facts only, read 2026-10-20 | Citation pointers validity, scanned PDFs not citable, 400 with structured outputs (§1.1.3); refusal stop reason with possibly empty category and reset advice (§1.1.4, §2.3.3); error events after output has begun, partial output moderation (§2.2.1) |

Microsoft's guidelines for human-AI interaction: the toolkit page was read, it states no licence and only links to a
terms page, so its guideline content was not used. Google's People + AI material: its licence file was not found at
the addresses tried, so it was not opened.

## Verified
1. Consequential submissions need a reverse, check or confirm path, and not every save needs one (§1.1.5).
2. Status messages (busy, progress, result counts, errors) are expected to be announced without moving focus (§2.2.4).
3. Self-updating content needs a pause, stop, hide or frequency control unless essential (§2.2.4).

4. Re-read 2026-10-20 on the pages: the levels (AA for 3.3.4 and 4.1.3, A for 2.2.2), the three alternatives of 3.3.4, the "essential" exception of 2.2.2, the sentence that excludes a list of search results from status messages.
5. Newly sourced: structured citation limits (§1.1.3), refusal as a stop reason (§1.1.4, §2.3.3), late errors and moderation of partial output (§2.2.1), time limits (§2.2.3), input error text (§2.3.3).
6. **Adjusted:** the earlier line that streamed content "does not" count as a status message is now marked as our reading of the page's search-results example.

## Removed
- Named guideline numbers or pattern catalogues from any third party: not opened under a licence, none cited.
- Numeric thresholds (acceptance rates, reading speeds, timeouts): none verified, none given.

## Not verified
1. **Still own guidance, not sourced:** basis over a score and calibrated numbers (§1.1.2), fluent text read as true
   (§1.1.1), scope copy and empty states (§1.2), the control points of §2.1, designed failure states other than refused
   (§2.3), feedback loops (§2.4), the usage-signal points of §3.2. Searched: W3C pages, Anthropic and OpenAI
   documentation; no permissive human-AI design guideline was found (the two named above are unusable).
2. **Time to accept** as a signal is a heuristic, not a measured rule.
3. **Whether token-by-token streamed text falls under 2.2.2** was not established; the point is phrased as a check.

## Related blocks
`ai-feature-acceptance-pitfalls`, `frontend-ux-antipattern-review-pitfalls`, `persona-ux-audit`, `accessibility`,
`llm-app-prompt-injection-and-exfiltration-pitfalls`, `ai-content-disclosure-and-provenance-pitfalls`,
`llm-cost-latency-control-pitfalls`, `prompt-versioning-and-change-gating-pitfalls`.

Independent verification 2026-10-21: 13 checked, 13 matched, 0 corrected, 0 unverified
