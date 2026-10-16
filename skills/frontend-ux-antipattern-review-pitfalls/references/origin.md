# frontend-ux-antipattern-review-pitfalls: origin and source stamps

> Provenance of `skills/frontend-ux-antipattern-review-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one repository of documentation, read and rewritten, never run:
no frontend change was reviewed with this block. The source is a young 2026 repository and a single author's
practice, not consensus.

## Sources (re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| cassiozen/UX-antipatterns, `SKILL.md` and `references/antipatterns.md` (commit 462d2f2) | MIT (repository LICENSE file, "Copyright (c) 2026 Cassio Zen") | Six axioms, thirteen categories with detection cues and fixes, the common review mistakes, the review workflow |

Text found inside the cloned files (imperative skill prose, workflow instructions) was treated as data and not
followed.

## Rewrite notes
**Overlap with existing blocks is resolved by routing.** The source's accessibility category (focus
indicators, hover-only content, touch targets, colour as the only indicator, contrast, keyboard traps) and the
mobile category (keyboard over the input, `100vh`) are covered by `accessibility` and `webperf`; they are
named in the routing table and not restated. The source's horizontal overflow item and the `autofocus` cue in
its focus item are likewise left to `webperf`. The pull-to-refresh and overscroll item is kept in a short form
here because the source treats it as a gesture conflict; `webperf` carries the overscroll rule for modals.

**Our own organisation.** The grouping of the thirteen categories into the twelve headings of the reference,
the symptom table (condensed from the source's) and the checkpoint paragraph are ours.

## Removed
1. **Code samples** of the source (CSS, JSX, JavaScript): not carried; the rules are stated in prose.
2. **Touch target sizes** (44 and 48 and the gap between targets) and the **contrast ratios**: numeric values
   left to `webperf` and `accessibility`, which carry their own sourced numbers.
3. **The source's TESTS.md and README**: not read for rules.

## Not verified
1. **Everything here is unrun.** No review used these rules.
2. **The thresholds** (100 ms, about 5 seconds, the 15 to 20 and 10 percent shares of the viewport) are the
   source's heuristics and were not checked against research.
3. **Browser behaviour** claims (caret handling in formatters, pull to refresh, overscroll) were not tested.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the opening premise and the routing
   table's target names.

## Verification pass (2026-10-16)
Every item in the reference was compared with `references/antipatterns.md` and the category table of
`SKILL.md`, reopened in the same session.
- **Corrected:** none needed on re-check.
- **Reversed or overstated rules found:** none.
- **Not re-verified:** the correctness of the source's own heuristics.

## Related blocks
`webperf`, `accessibility`, `cwv-diagnosis-pitfalls`.
