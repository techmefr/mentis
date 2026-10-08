# android-security-hardening §2 — PendingIntent

The Android developer page on pending intents (last updated 2024-09-24), read in full as page text on 2026-10-08.

## 2.1 Mutability
1. **A mutable `PendingIntent` lets the receiving app fill in the unfilled fields of the inner intent** (the `fillIn()`
   logic); a malicious app can use that to reach components that are not exported.
2. **Make action, component and package set** to avoid the worst cases; the page's example builds the intent with
   `setClassName` (or another component-setting call) and passes it to `PendingIntent.getActivity` with `FLAG_IMMUTABLE`.
3. **If your app targets Android 6 (API 23) or later, specify mutability;** `FLAG_IMMUTABLE` prevents unfilled fields from
   being filled in by another app.
4. **On Android 11 (API 30) and later you must specify which fields are mutable,** which the page says mitigates
   accidental vulnerabilities of this type.

## 2.2 Replay
1. **A `PendingIntent` can be replayed unless `FLAG_ONE_SHOT` is set.** A malicious app that captures it can repeat an
   action meant to happen once. Combine `FLAG_ONE_SHOT` with `FLAG_IMMUTABLE` for an intent that must not fire more
   than once.
