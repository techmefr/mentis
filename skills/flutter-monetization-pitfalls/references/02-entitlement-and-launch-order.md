# flutter-monetization-pitfalls §2 — Entitlement and launch order

Source: the ads-and-iap-monetization skill and its entitlement-and-restore reference (MIT, Flutter-Skills commit
e073e5e, read 2026-10-16), rewritten.

## 2.1 The purchase
1. **One non-consumable unlock plus a visible Restore control.** Not a subscription for a one-time capability,
   and not a consumable currency sold for cash where an opt-in rewarded path already exists. The Restore button
   is required by store review for a non-consumable (the reference's statement; Apple's guideline 3.1.1, read
   2026-10-20, requires a restore mechanism for any restorable in-app purchase, without using the word
   non-consumable).
2. **Re-check the entitlement silently on every launch**, so a reinstall or a new device re-grants it without a
   support ticket. The Play Billing page (read 2026-10-20) says to query purchases once the connection is up and
   again on resume, which covers a purchase made on another device, outside the app, or completed while the app
   was not running.
3. **On the app's first release, ship the unlock in the same review submission as the app version.** The skill's
   statement is that the first purchase of each type must ride a version, and shipping the version alone gets the
   submission closed unreviewed; check the current store rules before relying on it.
4. **Persist the purchase through the single write path before the UI reacts.** One committed transaction, then
   the screen changes because the gate re-emits; never dismiss the paywall optimistically. A crash in between
   must leave a state the next launch's restore repairs, not a "paid but not entitled" ghost.
5. **Complete a pending purchase exactly once, and always.** On Google Play an unacknowledged purchase is
   refunded automatically after three days (Play Billing integration page, read 2026-10-20; the three days
   start when a pending purchase becomes purchased, so a pending one is not acknowledged), which looks to the user like the app took the money and removed
   the feature.

## 2.2 One gate
1. **One derived entitlement provider is the only gate.** Every ad call site, cap and paywall control reads it;
   nothing branches on the raw entitlement stream, because a second read is a second gate that will drift.
2. **If a feature needs to know why** (trial, purchased, cached), derive that from the same source as another
   provider, never as a parallel subscription.

## 2.3 Restore before init
1. **Restore the entitlement before the ad SDK initialises.** If the SDK already started, a paying user has had
   it started, consent resolved, a tracking prompt shown and the device identified; a later no-op does not
   undo that.
2. **Initialise ads, and preload the rewarded unit, only for a confirmed non-entitled user.**
3. **A failed restore resolves to not entitled and initialises**: never withhold ads from every free user
   because one call failed.
4. **An entitled user who launches offline also fails the restore**, so cache the last known entitlement locally
   (through the single write path), read it before the restore returns, and let the store's answer overwrite it.
5. **The cache is for offline correctness and the first frame, not authorisation.** The store account is the
   authority. Without receipt validation on a server a determined user can flip a local flag, which the
   reference accepts for a one-time unlock in a small app; never build a server-backed benefit on that flag.

## 2.4 Tests that keep it true
1. **Entitled with a fake ads service: the fake's initialisation count is zero.** That one assertion keeps
   restore-before-init true through refactors.
2. **A fake billing service whose restore throws: ads did initialise.**
3. **Entitled, offline, cache primed: the initialisation count is zero again.**
4. **A purchase: the entitlement row is committed before the gate emits true.**
