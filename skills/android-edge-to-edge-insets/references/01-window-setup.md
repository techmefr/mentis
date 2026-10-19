# android-edge-to-edge-insets §1 — Window setup

The Android developer pages "Set up edge-to-edge", "About window insets" and "About system bar protection" (all last
updated 2026-10-01) and the Android 16 behaviour-change page, read in full as page text on 2026-10-08, with one
Apache-2.0 Android agent skill for the dialog and icon-colour rules. The pages name no library version for
`enableEdgeToEdge()`.

## 1.1 Enabling edge-to-edge and what the platform enforces
1. **Call `enableEdgeToEdge()` in `onCreate()` before `setContent()`,** in every Activity. It makes the system bars
   transparent and, in three-button navigation, puts a translucent scrim behind the navigation bar by setting
   `window.isNavigationBarContrastEnforced = true`. It also makes edge-to-edge work on releases before Android 15.
2. **Android 15 enforces edge-to-edge for an app that targets SDK 35 or later.** The status bar and the gesture
   navigation bar are transparent, the three-button bar is translucent, and content that was not written for it can
   end up hidden under the bars.
3. **Do not rely on the opt-out attribute.** For an app that targets Android 16 (API 36) running on an Android 16
   device, `R.attr.windowOptOutEdgeToEdgeEnforcement` is disabled; on an Android 15 device the same app still honours
   it. Remove the attribute so the app behaves the same on both.
4. **Draw edge-to-edge and consume the insets selectively.** A single `safeDrawingPadding()` on the root of the
   whole app makes the app safe but not edge-to-edge (the Android page says so); apply insets per screen or per
   component.

## 1.2 The manifest
1. **Set `android:windowSoftInputMode="adjustResize"` on every Activity that uses the soft keyboard.** The page's
   purpose for it: the app then receives the IME insets and can pad its layout when the keyboard opens or closes.
2. **Use the manifest attribute, not the window flag `SOFT_INPUT_ADJUST_RESIZE`,** which the skill calls deprecated.

## 1.3 Bar contrast and icon colours
1. **Icon colours follow the theme automatically only with the `ComponentActivity` form of `enableEdgeToEdge()`.**
   The page says the default adapts icon colours to the system light or dark theme. If the app calls the
   `WindowCompat` form instead, set `isAppearanceLightStatusBars` and `isAppearanceLightNavigationBars` yourself to
   the inverse of the dark-theme flag (dark icons on a light theme), typically in the app theme.
2. **A bottom bar that must reach the bottom edge needs navigation-bar contrast enforcement off.** In three-button
   navigation, `Window.setNavigationBarContrastEnforced(false)` removes the translucent scrim so a bar's own colour
   extends under the buttons (the page; the skill applies it for SDK 29 and later when a `Scaffold` or navigation scaffold has
   a bottom bar). Targeting Android 15 or calling `enableEdgeToEdge()` already makes the gesture bar transparent.
3. **Protect a status bar whose icons are unreadable over content by drawing a scrim.** A composable that overlaps
   the content and draws a gradient in the inset area works; draw it after the main content so it sits on top.
4. **Navigation-bar inset size can change at runtime** with the user's navigation method and taskbar use, so read
   it from the insets and never hard-code it.

## 1.4 Full-screen dialogs
1. **A dialog that is full screen must be made edge-to-edge itself.** It is full screen when its properties set
   `usePlatformDefaultWidth = false` and the dialog content calls `fillMaxSize()`. Set `decorFitsSystemWindows = false`
   in the dialog properties for such a dialog (the skill's rule), then apply insets inside it as in §2.
