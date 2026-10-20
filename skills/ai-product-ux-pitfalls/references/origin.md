# ai-product-ux-pitfalls: origin and source stamps

> Provenance of `skills/ai-product-ux-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Never dogfooded. Nothing was run, built or tested with users while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| W3C WCAG 2.2 Understanding pages: Status Messages (4.1.3), Error Prevention (3.3.4), Pause, Stop, Hide (2.2.2) | W3C Document License (terms read; copying allowed with attribution, no derivative texts), used for facts only | Status messages announced without focus (§2.2.4); reversible, checked or confirmed submissions (§1.1.5); pause, stop, hide for auto-updating content (§2.2.4) |

Microsoft's guidelines for human-AI interaction: the toolkit page was read, it states no licence and only links to a
terms page, so its guideline content was not used. Google's People + AI material: its licence file was not found at
the addresses tried, so it was not opened.

## Verified
1. Consequential submissions need a reverse, check or confirm path, and not every save needs one (§1.1.5).
2. Status messages (busy, progress, result counts, errors) are expected to be announced without moving focus (§2.2.4).
3. Self-updating content needs a pause, stop, hide or frequency control unless essential (§2.2.4).

## Removed
- Named guideline numbers or pattern catalogues from any third party: not opened under a licence, none cited.
- Numeric thresholds (acceptance rates, reading speeds, timeouts): none verified, none given.

## Not verified
1. **Everything not listed under Verified** is own guidance, not checked against user research or a published
   human-AI guideline: confidence display, citations, scope copy, failure-state designs, feedback loops.
2. **Time to accept** as a signal is a heuristic, not a measured rule.
3. **Whether token-by-token streamed text falls under 2.2.2** was not established; the point is phrased as a check.

## Related blocks
`ai-feature-acceptance-pitfalls`, `frontend-ux-antipattern-review-pitfalls`, `persona-ux-audit`, `accessibility`,
`llm-app-prompt-injection-and-exfiltration-pitfalls`, `ai-content-disclosure-and-provenance-pitfalls`,
`llm-cost-latency-control-pitfalls`, `prompt-versioning-and-change-gating-pitfalls`.
