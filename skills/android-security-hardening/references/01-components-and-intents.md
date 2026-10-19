# android-security-hardening §1 — Components and intents

The Android developer pages "android:exported" (last updated 2024-09-24) and "Intent redirection" (last updated
2025-03-10), read in full as page text on 2026-10-08.

## 1.1 Export on purpose
1. **Declare `android:exported` explicitly on every component.** The page's meaning: with `true`, any app can reach the
   activity by its exact class name; with `false`, only components of the same app, apps with the same user ID and
   privileged system components can launch it.
2. **The default has changed over time and differs by component type and Android version** (the page's example: a provider
   on API 16 and lower is exported by default). Leaving it unset risks different behaviour on different devices.
3. **An accidentally exported component can lead to** denial of service, other apps changing internal behaviour,
   leaked sensitive data and code execution in your app's context (the page's list).
4. **Export only what another app must start,** and write down who. Permission-based protection of an exported
   component is not on this page; see Not verified in the origin file.

## 1.2 Intent redirection
1. **A redirection occurs when an attacker controls all or part of the intent your app uses to start a component.** The
   intent usually arrives serialised in an extras field, or marshalled to a string and parsed; partial control of parameters
   leads to the same result. The impact can be running internal features or reaching private components such as unexported
   providers.
2. **Do not expose features that redirect nested intents.** Where unavoidable, sanitise the bundled intent: check or
   clear the read, write, persistable and prefix URI-permission grant flags, and check where the intent resolves. The
   page names `IntentSanitizer` for this.
3. **Resolve the target and compare package and class with the single expected pair** before starting the intent (the
   page's example uses `resolveActivity`), or build an `IntentSanitizer` with an allow-list of component, data and type
   and call `sanitizeByThrowing`.
4. **Using `PendingIntent` objects is also a mitigation,** per the page: it keeps your component from being exported and
   makes the target action immutable.
5. **Two mistakes the page names:** checking that `getCallingActivity()` is non-null (a malicious app can supply null) and
   assuming `checkCallingPermission()` works in every context, or that it throws when it actually returns an integer.
6. **Android 16 adds default protection against redirection exploits;** the page says most apps that use intents normally
   see no compatibility problem. An opt-out exists, `removeLaunchSecurityProtection()` on the nested `Intent`; the page
   says to use it only when strictly necessary and after weighing the security impact.
7. **For apps that target Android 12 (API 31) or later, StrictMode can flag an unsafe launch,** when the app unparcels a
   nested intent from the extras of a delivered intent and immediately starts a component with it (`startActivity`,
   `startService` or `bindService`). The page words this as helping "in some cases".
