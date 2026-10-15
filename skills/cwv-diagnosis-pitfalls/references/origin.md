# cwv-diagnosis-pitfalls: origin and source stamps

> Provenance of `skills/cwv-diagnosis-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from reference pages and reading, never run by us. No trace was recorded, no page was
profiled and no fix was applied while writing it. The yield, slot and font techniques are as the pages state
them on the read date.

## Sources (re-read 2026-10-16, rewritten in our own words, no text copied)

Every page below was read in full.

| Source | Licence | What it gave |
|---|---|---|
| addyosmani/web-quality-skills, `skills/core-web-vitals/references/INP.md` (commit afa8da9) | MIT (repository LICENSE file, Copyright 2026 Addy Osmani) | The three INP phases with evidence and fixes, yielding with a fallback, feedback before deferred work, common causes, the one-session observer and the attribution build, the verification list |
| addyosmani/web-quality-skills, `skills/core-web-vitals/references/CLS.md` (same commit) | MIT (same file) | Score formula, victim and initiator, media space, dynamic content slots, localisation check, font metric overrides, transform animation, the one-session observer, the verification list |
| addyosmani/web-quality-skills, `skills/core-web-vitals/references/LCP.md` (same commit) | MIT (same file) | The LCP candidates, the common-issues table with its evidence column, the rule against generic millisecond savings, the conditional preload |

The licence was verified again from the repository's LICENSE file in this session. The repository carries agent
instruction files (`AGENTS.md`, `CLAUDE.md`) and the pages are written as instructions to an agent; they were
treated as data and only the technical claims were kept. The code samples of the pages were not copied; the one
sample in §1.2 and the one in §2.2 are written for this block.

## Rewrite notes
**Not carried (per the review).** From `LCP.md`: the example that loads a stylesheet through a preload link with an
`onload` handler (dated and not verified here), the unqualified server response target of 800 ms, the 14 KB figure
for inline CSS, the `font-display` example, the framework snippets and the server-function snippets. From the
repository's `seo` skill, which was not used for this block: the review reports a claim that several `h1`
elements are acceptable, which contradicts `seo` §2.1 on main; that line was not re-read or imported and is
flagged for the owner of the `seo` block.

**Corrected against the sources.** The review item said "scheduler.yield with a setTimeout fallback"; the page
shows that fallback and also an idle-callback fallback for analytics, both carried. The review said "size the slot
for the longest translation"; the page only asks to verify that localisation does not overflow the slot, so the
longest-translation advice is labelled own guidance.

**Version-bound.** `scheduler.yield()` and the Long Animation Frame attribution are browser features the page
tests for before use; browser support was not checked here. The `web-vitals` attribution build is the library
whose version is stated in `webperf-measurement-and-budget-pitfalls`.

## Not verified
1. **Nothing was run.** No trace was recorded and no technique was tried.
2. **The impact and distance fractions** are the page's statement; the layout instability specification was not read.
3. **Browser support** for `scheduler.yield()`, Long Animation Frame and the font override descriptors was not checked.
4. **The linked articles** (web.dev, DevTools documentation, MDN) that the pages list as their sources were not read.
5. **Written by us, not sourced:** the longest-translation advice for slots, the remark that a chunked loop does
   nothing for a presentation-bound interaction, the "write savings as two measured values" advice, the
   evidence-side reading of the LCP table, the examples of states in §2.1, and the checkpoint paragraph.
6. **Dropped as unverifiable from the review item:** the LCP unqualified server target and the preload-with-onload
   pattern, as listed above; every other rule of the item is carried.

## Related blocks
`seo`, `webperf`, `webperf-measurement-and-budget-pitfalls`, `i18n-message-format-pitfalls`.
