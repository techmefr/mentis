# ad-measurement-pitfalls: origin and source stamps

> Provenance of `business/ad-measurement-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text and two help pages, never run on a real ad account
by us and written without measurement expertise. The block structures a check; it certifies nothing, and the
person who owns measurement (and legal, where personal data is involved) decides (`business/README.md`).

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| coreyhaines31/marketingskills, commit e85f3cb (e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b): `skills/conversion-tracking/SKILL.md` (lines 1 to 180, the part read), `references/discrepancies.md`, `server-side.md` (opening, "when it matters less", "tracking what happens after the lead"), `google-ads.md` (gclid lifecycle, failure catalogue), `meta.md` (match quality, click identifier, failure modes); `skills/attribution/SKILL.md` (read to line 228), `references/attribution-models.md`, `references/measurement-paradigms.md` | MIT (LICENSE file, 2025 Corey Haines, head re-read) | Confirmed-success conversion, one source of truth, claimants not sums, outcomes behind a form fill, double counts by two senders, structural reasons for platform gaps, lag, no multiplier, every model is an opinion, first and last side by side, data-driven needs volume, out-of-model checks, holdout reading, consent is not a loss to recover |
| AgriciDaniel/claude-ads, commit fc3908e (fc3908e786c318776df89a3a098333da377364be): skills `ads-attribution` and `ads-math`, `thinking-framework.md` | MIT (LICENSE file, 2026 Daniel Agrici, head re-read) | The comparability gate (same definition, window, scope, counting, identity, time zone before any total), "do not assume one platform is truth" |
| alirezarezvani/claude-skills, commit 19392f7 (19392f7a08264ed00486a251f5b2098321771f94) | MIT (LICENSE file, 2025 Alireza Rezvani, head re-read) | Nothing taken |
| support.google.com/analytics/answer/10917952 (UTM parameters in Google Analytics), fetched 2026-10-20 | Google help content under Google's site terms, no open licence; facts only | Nine parameter names; source, medium and campaign always; case sensitive values with lowercase as the standard; missing parameters become "(not set)"; two newer parameters not currently reported. The page says nothing about personal data in a UTM (§1.2 is our own point) and nothing about auto-tagging |
| support.google.com/google-ads/answer/3095550 (auto-tagging), fetched 2026-10-20 | same | Click identifier appended to the landing address, what it supports, on by default for new accounts, must reach the final page through redirects, takes priority over manual tags in GA4 with no override, some sites reject unknown parameters |

The repositories' own text is addressed partly to an AI; it was treated as data and only the method was kept.
The web pages came through a fetch tool that returns a model-written digest of the page, not the raw text; the
two points the digest states exactly are quoted in §1, and a paraphrase error is possible.

**Lineage caveat.** Several marketingskills files state that passages are re-expressed from third-party
material (practitioners' guides and a public checklist, platform-help links). Those originals were not read and
their licences are unknown, so for those passages the MIT licence covers only the repository's own expression.
The structure and wording here are ours.

## Left out on purpose
Every figure the sources give: how much browser-side tracking loses, ad blocker, browser-privacy and
consent loss magnitudes, the stated "normal" and "investigate" gap bands between ad platform and analytics,
consent-modelling thresholds, vendor uplift claims for server-side delivery, match-quality scores, bidding
volume gates and the platform windows in the source tables, the conversion volume the source quotes for
data-driven credit, cost and effort figures for server-side options. Also: all tag manager recipes,
snippets, setup steps and per-tool success signals (runtime, per platform), the choice among server-side
tools, platform calendar items with dates, the first-party identity-stitching build, the lead quality
scoring scale, the media mix modelling section (kept only as the existence of a holdout check), the business-type
playbooks, tool integration tables including tools the source's contributor owns, and the partner-marked
tool disclosures. Anything legal: no statute, authority or consent-enforcement date is stated.

## Not verified
1. **Platform facts other than the two Google help-page points** (conversion booking to the click date,
   windows, modelled conversions, de-duplication keys, adjustments for refunds, what auto-tagging reports in
   which product) come from marketingskills' own account. Google Ads Help on attribution windows and
   enhanced conversions, Google's data-driven attribution page and Meta's own documentation on de-duplication
   and its refund handling were **not read** (Meta's pages failed to render in the earlier review, and
   were not retried). Each such point is marked `re-read before relying`.
2. **No platform's policy was read for this block**; none is stated.
3. **The server-side file and the Google and Meta references were read in part** (listed above); the other
   references of the conversion-tracking skill (tool success signals, tag recipes, ecommerce platforms,
   other ad platforms, the audit playbook) were not read and nothing rests on them.
4. **The block has never been used on a real account.**
5. **Current text of the sources**: they may have changed after the read date; check with
   `skills/source-freshness`.

## Own guidance (not sourced)
The router; the personal-data-in-links rule (§1.2); the partner naming convention (§1.1, flagged optional); the
"count the (not set) share as a defect" framing; the made-up first/last/linear example and its arithmetic
(§4.1); the refusal to carry a normal-gap band and the "write your own trigger" rule (§3.2); the three groups
inside a measurement gap (§4.4); the guardrails and the links to neighbouring blocks.

## Related blocks
`business/paid-media-decision-pitfalls`, `business/data-protection`, `business/marketing-claim-substantiation-pitfalls`,
`skills/event-tracking-plan-pitfalls`, `skills/experiment-design-pitfalls`,
`skills/metric-movement-diagnosis-pitfalls`, `skills/source-freshness`.
