# flutter-notifications-background §2 — Push and background handlers

Source: the Firebase Cloud Messaging pages for Flutter (getting started, and receiving messages), read
2026-10-08. They describe Firebase's own plugin; a different push provider needs its own page read. The
fetch tool that read them summarises pages, so the quoted conditions below are paraphrased from its
extracts.

## 2.1 Platform prerequisites
1. **Apple devices: upload the APNs authentication key to Firebase before relying on FCM.** The getting-started
   page says to do this before using FCM.
2. **Method swizzling is required for the FCM Flutter plugin on Apple devices;** the page says that without
   it, key features such as registration handling do not function. Do not disable it.
3. **Android needs a device with a supported Android version and Google Play services** (or an emulator with
   Google APIs); the page's minimum was Android 7.0 when read. Re-read the number at writing time.

## 2.2 Permission
**Ask for permission through the plugin's request call, at a point where the reason is clear.** On iOS and on
Android 13 and later the user must grant it before message payloads are shown; the call asks the user when
permission has not yet been granted. The timing advice is that of `flutter-notifications-background` §1 and
the Android permission page.

## 2.3 Three delivery states, three code paths
The page separates them, and they are different entry points to the same app:
1. **Foreground:** a stream of incoming messages. A notification message that arrives while the app is in
   the foreground is not shown by default on Apple devices; on Android a high-priority channel overrides
   that, per the page.
2. **Background, opened by tapping the notification:** a stream of opened-app events.
3. **Terminated, opened by tapping:** a future that returns the initial message, to be read once at launch.
Route each into the same route table (`flutter-conventions` §5), including the terminated case, which the
launch path of `flutter-startup-error-hooks` has to be ready for.

## 2.4 The background message handler
1. **It must be a top-level function, not anonymous and not a method that needs an instance,** and from
   Flutter 3.3.0 it must carry the VM entry-point pragma or release-mode tree shaking may remove it (the
   page's wording).
2. **It runs in its own isolate outside the app's context,** so it cannot update application state or run
   anything that touches the UI; initialise Firebase inside it, because other Firebase services may be needed.
3. **Finish quickly.** Long or intensive work affects the device and the page says the OS may end the process
   after 30 seconds. Defer heavy work to the foreground reconcile of `flutter-notifications-background` §1.
4. **On iOS a user who swipes the app away from the switcher must reopen it before background messages work
   again** (the page's precondition); a feature that depends on background delivery documents that.

## 2.5 What a push payload is
A payload's route or identifiers are untrusted input, exactly as a link is (`flutter-notifications-background`
§3 and `security-hardening`): the screen they open fetches its own data and authorises it, and a message that
names a resource does not grant access to it. (Our guidance; the Firebase pages do not discuss it.)
