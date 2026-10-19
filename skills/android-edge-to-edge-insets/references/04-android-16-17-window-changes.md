# android-edge-to-edge-insets §4 — Android 16 and 17 window changes

The Android 16 and Android 17 behaviour-change pages on developer.android.com, read in full as page text on
2026-10-08. Thresholds are stated per target SDK as the pages state them.

## 4.1 Large screens ignore orientation and resizability locks
1. **For an app that targets Android 16 (API 36), on a display whose smallest width is 600dp or more,** orientation,
   resizability and aspect-ratio restrictions no longer apply. The app fills the display window whatever the aspect
   ratio or the user's orientation, and pillarboxing is not used. The manifest attributes `screenOrientation`,
   `resizeableActivity`, `minAspectRatio` and `maxAspectRatio`, and the calls `setRequestedOrientation()` and
   `getRequestedOrientation()`, are ignored in full-screen and multi-window modes, for every portrait and landscape
   value of `screenOrientation`.
2. **Exceptions:** games (by the `android:appCategory` flag), a user who explicitly chose the app's default behaviour in
   the device's aspect-ratio settings, and screens narrower than 600dp.
3. **Expect stretched layouts, off-screen animations and more activity re-creation,** since rotation is now allowed.
   The page says to save UI state properly so the user does not lose it, and to build an adaptive layout.
4. **Test it with the app compatibility framework** by enabling the `UNIVERSAL_RESIZABLE_BY_DEFAULT` compat flag.
5. **The temporary opt-out is the manifest property** `android.window.PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY`
   set to true on an activity or on the application; the app is then placed in compatibility mode as before.
6. **On Android 17 (API 37) the opt-out is gone:** the Android 16 page says the opt-out will not apply to an app that
   targets API 37, and the Android 17 page repeats that for apps that target Android 17 or higher.

## 4.2 The edge-to-edge opt-out
1. **`R.attr.windowOptOutEdgeToEdgeEnforcement` is deprecated and disabled for an app that targets API 36.** On an
   Android 15 device the same app still honours it, on an Android 16 device it does not; the page tells you to remove the
   attribute so the app also supports edge-to-edge on Android 15 (details in §1.1 point 3).
