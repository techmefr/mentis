# flutter-notifications-background §3 — Links and entry delivery

Sources: the Flutter deep-linking page and its two cookbook pages (Android app links, iOS universal links),
the Android page on verifying app links, read 2026-10-08 (summarised through a fetch tool). Routing the
received path into screens, guards that remember the destination and the back stack are
`flutter-conventions` §5 and are not repeated here.

## 3.1 Android app links
1. **Host the Digital Asset Links file at `/.well-known/assetlinks.json` on every host named in the intent
   filter, over HTTPS and without a redirect.** For each unique host the system fetches that file (Android
   page); the Flutter cookbook says to verify the browser can reach it and that redirects are not allowed.
2. **Mark the intent filter for automatic verification.** With it set on at least one filter, installing the
   app on Android 6.0 or later makes the system verify the hosts (Android page).
3. **The fingerprint in the file must match the signing certificate of the build under test.** For a store
   build the Flutter cookbook says to use the app signing key shown in the Play console, not the upload key;
   debug builds have their own fingerprint. One list entry per fingerprint, so a flavor with its own signing
   adds its own. A link that verifies in debug proves nothing about the store build.
4. **A failed verification leaves states such as a legacy failure or a denial, and only one app at a time can
   be associated with a domain on a device** (Android page).

## 3.2 iOS universal links
1. **Host the association file at `/.well-known/apple-app-site-association`, with no file extension, over
   HTTPS and without a redirect.** Its app identifier is the team identifier and the bundle identifier joined
   by a dot (Flutter cookbook).
2. **Add the associated-domains entitlement with an `applinks:` entry for the host** in the Runner's
   entitlements file.
3. **Apple's content delivery network may take up to 24 hours to fetch the file** after a change, so a
   failing test right after a deploy is not yet evidence (cookbook).

## 3.3 Testing
1. **The `adb` intent command only proves the app handles the link;** the cookbook states it does not test
   that the web files are hosted correctly, since it launches the app even when they are absent.
2. **A complete test follows a real link from a browser or a document,** or uses the deep-link validator in
   DevTools (the cookbooks point to it).

## 3.4 The framework's default handler and plugins
1. **From Flutter 3.27 deep linking is handled by the framework by default;** earlier versions need an
   opt-in key in the Android manifest and in the iOS property list (both cookbooks). The version number is
   the cookbooks' statement; re-read it when the project's Flutter version is below it.
2. **A plugin that handles links itself conflicts with the default handler.** The Android cookbook says the
   default handler breaks such plugins and gives an opt-out key (`flutter_deeplinking_enabled` set to false in
   the manifest, `FlutterDeepLinkingEnabled` set to false in the property list). Pick one handler.

## 3.5 A link is not authorisation
1. **Android's own page says verification is about which app handles a link, not about who the user is.**
   Opening a link to a resource proves possession of a URL, not permission to the resource; the destination
   authorises as it would for any navigation, after sign-in when the user was not yet signed in
   (`flutter-conventions` §5 point on carrying the target through a guard).
2. **Store the intent the link names, not the raw string,** while the user is unauthenticated, then
   re-validate it before acting. (Our guidance.)
3. **A destructive action never runs directly from the link callback;** the link opens the screen and the user
   confirms there. (Our guidance.)

## 3.6 Delivery order is not guaranteed to be a single event
The deep-linking page's behaviour table shows that with the older navigator an iOS app that was not running
gets an initial route and shortly afterwards a push of the link's route, while with the router the link is
parsed once into a route and a link opened while the app runs replaces the current pages. So the same link
can arrive as two events depending on which API owns navigation: make delivery idempotent (a screen reached
twice by the same link is not pushed twice, `flutter-conventions` §5 on double pushes).
