# programmatic-video-pitfalls: origin and source stamps

> Provenance of `skills/programmatic-video-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation and repository text. No video was rendered, no
renderer was run and no determinism claim was tested by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

Web pages were read through a fetch tool that returns a small model's digest, **not the verbatim page**; exact
wording and figures were not checked at the page. Repositories were cloned read-only and files read in the
session; the clones were deleted afterwards.

| Source | Licence | What it gave |
|---|---|---|
| heygen-com/hyperframes, commit 0693839b52306cbe35ee508f7b4c4b6f914a4fae: `skills/hyperframes-core/SKILL.md` (read in full), `references/determinism-rules.md` (read in full), `skills/hyperframes/SKILL.md` (router, first 150 of about 25 KB), `skills/product-launch-video/SKILL.md` (steps 0 to 6 and the start of the quick reference, 260 lines of about 36 KB), `CREDITS.md`, `CLAUDE.md`, the file tree for fonts, audio and licence files | Apache-2.0 (LICENSE re-read this session: Apache License 2.0 full text) | The frame-from-time contract and its bans; one paused timeline registered when built; static end state first; setup-time layout; the lint, snapshot, preview, render-after-approval order; a lint error that makes later checks report zero samples; the licence and credits record of what it bundles (§4.3). No file or text copied, so the NOTICE terms do not apply |
| coreyhaines31/marketingskills, commit e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b: `skills/video/SKILL.md` (read in full) | MIT (LICENSE re-read this session: "Copyright (c) 2025 Corey Haines") | The choice of approach by need, "starting with tools, not strategy", the claim that generative models handle readable text poorly and are not for specific products; its table of model prices and plans and its audience statistic were not used |
| remotion-dev/remotion `LICENSE.md` (github.com), fetched 2026-10-20 | The page is the licence of a source-available project; not an open-source licence by its own wording | Free-use groups, Company License requirement, no resale of derivatives, "will slightly change" in 5.0, no mention of open source (§4.2) |
| remotion.dev docs: `license/terms`, `the-fundamentals`, `flickering`, `random`, fetched 2026-10-20 | Vendor documentation; ideas and facts only, nothing quoted beyond a licence phrase or two in §4.2 | Headcount definition, excluded organisation types, rendering-service restriction, per-use-case licensing, kinds of Company License; frame number as the input of a component; flicker causes (parallel tabs, non-frame-driven animation, randomness, missing waits for data and fonts); seeded random versus unseeded |
| remotion.dev/docs/license (the docs page) | same | Returned only its introduction ("everything about using Remotion commercially") with no terms; nothing taken from it |
| remotion-dev/skills | **No LICENSE file** | Idea-only; nothing taken from its text and not re-read for this block |

## Removed
1. **Every price, plan, per-render fee and per-seat figure** (the framework's and the model vendors'): volatile
   vendor figures; a block points to the vendor's page.
2. **All command lines, plugin and skill install or update flows, sign-in and usage probes** of the HTML
   framework, and its audio, caption and media sourcing services: runtime dependency on one vendor (rule B).
3. **The framework's attribute names, lint rule identifiers and file layout**: tool syntax, not a method.
4. **The marketing skills repository's model comparison and avatar plan tables, the claim that models "write
   better HTML than React" and the share-watching-without-sound statistic**: unsourced or vendor marketing.
5. **The determinism claim as a promise** ("same input always gives identical output"): the vendors' claim,
   untested by us; the block gives the contract and a way to test it (§1.4).

## Not verified
1. **No render was run.** Nothing about determinism, frame rate, speed or file size was measured.
2. **The Remotion pages came as digests.** The licence conditions (§4.2) must be read again at the pages
   before anyone relies on them; the licence file and the terms page are worded differently ("employees" and
   "people"), and I did not resolve that. The Remotion docs page on the licence returned no terms; the Terms
   page's list of Company License kinds is as the digest has it. No remotion.pro page was re-read this session.
3. **The HTML framework: 150 of its router's lines, 260 of its product workflow's, its core skill and
   determinism rules in full.** The explainer, pull-request, music and slideshow workflows, the animation,
   keyframes, audio, registry and studio skills, the 48 atomic rules and the engine source were not read.
   Statements about how the framework treats a clip, a registered timeline or a lint error rest on the two
   files read in full.
4. **Licences of the shipped fonts and media were checked only as far as the licence and credits files in the
   tree state them**, and the six textures marked "origin to be confirmed" were left unresolved by their
   authors. No font or audio file was opened or hash-checked and no registry block was audited.
5. **The claim that React's frame-based approach and the HTML approach share one contract** is our reading of
   two sources, not a statement either makes about the other.
6. **Current text of the sources** may have changed after the read date (`skills/source-freshness`).

## Own guidance (not sourced)
The router; the list-what-each-frame-reads review step and the byte-for-byte check (§1.1, §1.4); the
variant-as-input idea (§1.2); the choice of still times (§3.1); the zero-items generalisation and "put the
number in the report" (§3.3); the approach table's wording (§4.1); the rule that an asset with no recorded
origin is replaced (§4.3); the guardrails.

## Related blocks
`skills/web-animation-pitfalls`, `skills/accessibility`, `skills/webperf`, `business/video-brief-and-storyboard`,
`business/licence-compliance`, `business/data-protection`, `business/ai-content-disclosure-and-provenance-pitfalls`,
`skills/source-freshness`.
