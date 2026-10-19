# flutter-monetization-pitfalls: origin and source stamps

> Provenance of `skills/flutter-monetization-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from reading, never run by us. No ad SDK was integrated, no purchase made and no store
submission checked while writing it. This block is meant to be folded into the Flutter block when the extended
language blocks (the unmerged PR 118 branch) land; until then it stands alone and cites only blocks that exist on
the main branch.

## Sources (all read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Flutter-Skills (commit e073e5e): `skills/ads-and-iap-monetization/SKILL.md` | MIT (LICENSE re-read) | Parts 1 and 2 rules |
| Flutter-Skills: `ads-and-iap-monetization/references/entitlement-and-restore.md` | MIT | Part 2 detail |
| Flutter-Skills: `ads-and-iap-monetization/references/ad-unit-setup.md` and `scripts/check-release-ad-ids.sh` (header comments) | MIT | Part 3 rules |

## Removed in the verification pass (no page supporting them)
- The example Dart economy file and the policy-layer code samples: not reproduced; the rules do not need them.
- Store policy pages (the review asked to re-read them at writing time): not opened. Every store-policy claim
  here is the skill's statement and says so.
- The skill's related-skill rules on the service seam, startup, persistence and typed results: those skills were
  not read; this block cites none of their content.

## Not verified
1. **Own guidance:** none flagged; every point traces to a file above.
2. **Store review rules** (the app-completeness guideline, the first-purchase-with-a-version rule, the required
   Restore control) are the skill's and reference's statements; no Apple or Google page was opened, and these
   rules change.
3. **The ad console fields and the roughly one-month figure** are one network's console as the reference
   describes it; the current console may differ.
4. **Receipt validation, consent and tracking-prompt requirements** by region were not read; the skill treats
   them only as consequences of SDK initialisation.
5. **The release script** was read for its header comments and first checks, not run, and its sample-prefix
   check is tuned to one network.
6. **The model is the skill's choice** (free and opt-in first); a project with another monetisation model should
   keep the entitlement and ordering rules and revisit the ad-format rules.

## Related blocks
`flutter-conventions`, `flutter-native-bridge-ffi`, `flutter-release-toolchain-hygiene`.
