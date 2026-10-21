# flutter-monetization-pitfalls: origin and source stamps

> Provenance of `skills/flutter-monetization-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from reading, never run by us. No ad SDK was integrated, no purchase made and no store
submission checked while writing it. Overlaps with `skills/flutter-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Flutter-Skills (commit e073e5e): `skills/ads-and-iap-monetization/SKILL.md` | MIT (LICENSE re-read) | Parts 1 and 2 rules |
| Flutter-Skills: `ads-and-iap-monetization/references/entitlement-and-restore.md` | MIT | Part 2 detail |
| Flutter-Skills: `ads-and-iap-monetization/references/ad-unit-setup.md` and `scripts/check-release-ad-ids.sh` (header comments) | MIT | Part 3 rules |

## Re-read 2026-10-20 (verification pass)
Official pages opened that day, facts only, site terms not read, nothing copied. Google Play Billing
integration page (acknowledge within three days or the purchase is refunded and entitlement revoked; the window
starts once a pending purchase completes; query purchases on connect and on resume), AdMob rewarded guide for
Flutter (grant in the user-earned-reward callback; one ad object is shown once and disposed), AdMob Flutter
quick-start (app id in the manifest metadata and the property-list key, tilde format, initialisation future),
AdMob test-ads page (demo unit ids with one shared prefix, replace before publishing), Google Play ads policy
page (unexpected interstitials, launch and splash, repeated interstitials, 15-second close rule, opt-in rewarded
ads exempt) and the App Store review guidelines (3.1.1 restore mechanism, 2.5.18 interstitial labelling and
close controls, 2.1 completeness). Corrections: the rejection risk of a dead earn button is the source skill's
inference, not a guideline sentence (1.2.4); the restore requirement is for restorable purchases (2.1.1); the
unacknowledged-purchase refund window is three days on Play (2.1.5). Added: 1.3.1 policy detail, 2.1.2 query on
resume.

## Removed in the verification pass (no page supporting them)
- The example Dart economy file and the policy-layer code samples: not reproduced; the rules do not need them.
- Store policy pages (the review asked to re-read them at writing time): not opened. Every store-policy claim
  here is the skill's statement and says so.
- The skill's related-skill rules on the service seam, startup, persistence and typed results: those skills were
  not read; this block cites none of their content.

## Not verified
1. **Still unsourced after 2026-10-20 (the source skill's statements only):** the first-purchase-rides-a-version
   rule, reward amount and item being cosmetic client-side, ad pods, server-side verification, frequency capping
   and price floor settings and the one-month figure, the app-launch crash on a missing app id, unit ids not
   being secrets, banner placement and the one-model rule. No ad-console page was opened.
2. **Store review rules** that remain the skill's statements: the first-purchase-with-a-version rule. The
   Apple guideline pages were read on 2026-10-20 for restore, interstitials and completeness; the Play policy
   page for interstitials. These rules change.
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
