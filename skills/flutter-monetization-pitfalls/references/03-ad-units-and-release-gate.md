# flutter-monetization-pitfalls §3 — Ad units and the release gate

Source: the ad-unit-setup reference and the release-gate script of the ads-and-iap-monetization skill (MIT,
Flutter-Skills commit e073e5e, read 2026-10-16), rewritten. The reference uses one network's console as the worked
example and says the shape generalises; field names below are that example's.

## 3.1 Create only the formats you use
1. **Create the opt-in rewarded unit and the capped interstitial unit, named for the placement** (the benefit or
   the break), because the name is what you will read in a report months later.
2. **Do not create a rewarded interstitial unit.** It appears at a break and rewards sitting through it, the
   opposite of an opt-in earn loop, and quietly breaks the promise in part 1.
3. **Do not create an app-open unit** (a forced ad on every launch), a banner for the working surface, or a native
   unit unless the design has a real inline ad surface.

## 3.2 Console fields that reach the code
1. **Leave partner or third-party bidding unchecked unless you run third-party mediation.** The reference calls
   the setting irreversible: it locks the unit out of the network's own mediation and campaigns.
2. **Reward amount and item are cosmetic in a client-only integration**: the callback sets a flag and the app
   grants what its own economy says. The app's cap is the real ceiling.
3. **Ad pods off**: chaining several ads for one benefit earns the reviews an opt-in model exists to avoid.
4. **Server-side verification off unless you have a server**, and then only where the reward has real value to
   defend; a benefit capped on the device with nothing to spend it on has nothing to protect.
5. **Frequency capping disabled in the console**; the app caps. A console cap on an opt-in format produces
   no-fill, and no-fill hides the earn control, so the user loses the path for a reason they cannot see.
6. **Take all prices at launch (no price floor)**: a high floor fills less, and on a rewarded unit a no-fill
   removes the control. Revisit after about a month of real data (the reference's figure).

## 3.3 Two identifiers, two homes
1. **The app identifier (tilde-separated, confirmed on the AdMob Flutter quick-start page read 2026-10-20)
   goes in the platform manifest** (the iOS property list
   and the Android manifest metadata), because the SDK reads it at initialisation. A missing or empty value
   crashes the app at launch (the reference's statement; the quick-start page names the manifest metadata
   and the property-list key but does not describe the failure, so this stays unconfirmed).
2. **Unit identifiers (slash-separated) go in a Dart constant.** They are not secrets, since they are visible in any
   decompiled app and networks publish samples, so compile-time constants beat build-time defines: a release
   build cannot forget a constant. Keep debug builds on the network's test units.

## 3.4 The release gate
1. **A release check fails on an empty app identifier and an empty unit constant**, because an empty unit makes the
   earn control never appear and nobody notices until revenue is flat.
2. **It warns on the network's well-known sample publisher prefix**, fine in development, never in a release:
   sample ids serve "test ad" creatives that earn nothing and look broken to a reviewer. The AdMob test-ads page
   (read 2026-10-20) lists the demo units, all under one shared publisher prefix, including demo units for the
   rewarded interstitial and app-open formats, and says to replace them before publishing; test-labelled ads
   are safe to click and appear in no reports.
3. **Add a launch-time assertion that a release build has real, non-empty ids**, so a misconfiguration throws
   loudly instead of falling back to test creatives silently.
4. **Never reuse another app's unit ids to get going**; traffic and revenue are mis-attributed and found late.
5. **Expect no fill at first.** A new account or app may wait in review before serving, fill ramps only once the
   app is live with its listing linked, the publisher declaration file hosted and payment and tax details complete.
   Say so in the reviewer note instead of treating empty inventory as a bug.
