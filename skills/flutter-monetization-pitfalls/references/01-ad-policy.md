# flutter-monetization-pitfalls §1 — Ad policy

Source: the ads-and-iap-monetization skill of the Flutter-Skills repository (MIT, commit e073e5e, read
2026-10-16), rewritten. The skill encodes one model, free and opt-in first with a single purchase that removes
the exchange, and says it is not the only viable one; the rules below keep any ad-funded app reviewable.

## 1.1 Seam and model
1. **Every ad and store call crosses an injected interface**, with the concrete SDK wired once at the composition
   root and faked in tests. No SDK type appears in feature code.
2. **Pick one model: paid upfront or ad-supported, never both.** Charging for the app and then selling the
   buyer's attention is the pattern users punish in reviews.

## 1.2 Rewarded views
1. **A rewarded view is opt-in and grants exactly one concrete benefit**: it fires only from an explicit
   "watch to earn" tap, never automatically, and gives one unit (a credit, an extra attempt, a partial reveal),
   never the whole outcome the user is working toward. An automatic rewarded ad is an interstitial in disguise.
   The AdMob rewarded guide (read 2026-10-20) puts the grant in the user-earned-reward callback, not at show
   or dismiss time, and the Play ads policy page exempts rewarded ads the user explicitly opts into from its
   rules on unexpected interstitials.
2. **Model the result as a sealed type with three outcomes**: rewarded, dismissed (closed early) and no fill.
   Switch exhaustively; only the first grants, and the other two leave state untouched. A boolean collapses "no
   ad existed" into "the user declined", which need different screens.
3. **Cap earning per calendar day in the policy layer, against an injected clock**, never against the system
   time. An uncapped earn loop bypasses whatever the benefit was rationing, and a cap kept only in the network
   console produces no-fill (part 3).
4. **Never show an earn control that can dead-end.** A new ad account has almost no fill, so an always-visible
   button answers "no ads available" every time, which reads as broken. (The earlier text tied this to a store
   rejection under the app-completeness guideline; Apple's guideline 2.1, read 2026-10-20, rejects incomplete
   or crashing apps and requires purchases to be working and reviewable, but says nothing about dead ad
   buttons, so the rejection risk is the source skill's inference.) Preload, expose availability as a stream, show the control only while an ad is
   loaded or a redemption is in flight, and keep whatever the user needs reachable without watching anything.

## 1.3 Interstitials and banners
1. **An interstitial fires only at a natural break**: a completion or transition the user already expected,
   never mid-task, never in onboarding, never in the first session. The Play ads policy page (read
   2026-10-20) lists as violations a full-screen interstitial that appears unexpectedly while the user is doing
   something else, one before the splash screen at launch, one shown after consecutive taps or swipes, and one
   at the start of a level; an interstitial must be closeable within 15 seconds unless it is opt-in or does not
   interrupt an action. AdMob's interstitial guide recommends natural transition points. Apple's guideline
   2.5.18 (read 2026-10-20) adds that an interstitial must be clearly labelled, not trick the user into
   tapping, and carry a large visible close or skip control.
2. **The cap has two halves and both must pass**: at most one per N completions and at least M seconds since the
   last one. Put the counting and the clock inside the service's show method and return whether it showed, so no
   caller counts; a cap enforced at three call sites is three caps that will disagree.
3. **No banner on the primary work surface.** It reflows layout, invites mis-taps and earns the least of any
   format. A menu or home surface is the only defensible place and it is optional.

## 1.4 Anti-patterns the skill lists
Auto-playing a rewarded ad; granting on dismissed or no fill; a boolean result; an uncapped loop or a cap in the
console; an always-visible earn button on a new account; a grant that completes the user's task; interstitials
mid-task or at first launch; a caller that counts completions or reads a clock; a banner on the working surface;
paid upfront plus ads.

## 1.5 What to test
Against fakes: watch then granted; cap reached then refused; no fill then the control is hidden; a purchase then
ads are gone and caps are lifted.
