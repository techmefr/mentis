---
name: flutter-monetization-pitfalls
description: "Use when adding ads, a rewarded earn loop, an interstitial, a paywall or a one-time unlock to a Flutter app: rewarded outcomes and daily caps, earn controls that never dead-end, natural-break interstitials, one derived entitlement gate, restore before ad SDK init, console unit settings, and sample ad ids in a release."
---

# flutter-monetization-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for a Flutter app that earns from ads or a purchase. The premise:
**monetisation code is where an app's promises to its user are enforced or broken, and every failure is quiet:
a paying user still gets the ad SDK started, a new account sees a permanent "no ads available" button, a release
ships the network's sample ids.** Rules here are a policy layer over a service seam the app already has;
native bridges are `flutter-native-bridge-ffi`, release tooling is `flutter-release-toolchain-hygiene`, startup
order is `flutter-startup-error-hooks`, and general conventions are `flutter-conventions`.

## When
- An ad format, a "watch to earn" control, an interstitial or a banner is added or moved.
- A purchase, a restore button, a paywall or an entitlement flag is added.
- Ad units are created in a network console, or a release build is prepared for an app that shows ads.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Ad policy: injected interfaces, rewarded outcomes, daily cap, earn control visibility, interstitial caps, banners, pricing model | an ad format or earn flow is designed or reviewed | [`01-ad-policy.md`](./references/01-ad-policy.md) |
| 2 | Entitlement: unlock, restore, one gate, restore before init, cache, commit before UI, tests | a purchase, a paywall or startup order is touched | [`02-entitlement-and-launch-order.md`](./references/02-entitlement-and-launch-order.md) |
| 3 | Ad units and the release gate: formats not to create, console fields, two identifier kinds, sample ids | units are created or a release is prepared | [`03-ad-units-and-release-gate.md`](./references/03-ad-units-and-release-gate.md) |

## Output / checkpoint
Each rewarded flow names its outcome type and grants only on the genuine reward; each interstitial names the
natural break and where the count lives; each entitlement read goes through one gate; the launch order is
written as restore first, ads second. "Ads are integrated" without saying what happens for an entitled user, an
offline owner, a failed restore and a no-fill is not verified.

## Guardrails
- Never grant a reward on a dismissed or unfilled outcome (part 1).
- Never initialise the ad SDK before the entitlement is known (part 2).
- Never show an earn control while no ad is loaded (part 1).
- Never ship a release that still carries the network's sample ids or an empty unit id (part 3).
- Never design a server-backed benefit on top of a local entitlement flag (part 2).
- No block and no agent installs an SDK or a plug-in: the blocks name it and the user installs it
  (`CONVENTIONS.md`).
- Versions: store policy and SDK behaviour change; every rule here is the source's position at the stamped
  commit. Nothing was built or run while writing this block.

## Origin
Rewritten from the ads-and-iap-monetization skill of the Flutter-Skills repository (MIT: its rules, its two
references and its release-gate script), read 2026-10-16. Meant to be folded into the Flutter block when the
extended language blocks (the unmerged PR 118) land; until then it stands alone. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
