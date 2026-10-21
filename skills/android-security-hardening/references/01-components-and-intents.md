# android-security-hardening §1 — Components and intents

The Android developer pages "android:exported" (last updated 2024-09-24) and "Intent redirection" (last updated
2025-03-10), read in full as page text on 2026-10-08.

## 1.1 Export on purpose
1. **Declare `android:exported` explicitly on every component.** The page's meaning: with `true`, any app can reach the
   activity by its exact class name; with `false`, only components of the same app, apps with the same user ID and
   privileged system components can launch it.
2. **The default has changed over time and differs by component type and Android version** (the page's example: a provider
   on API 16 and lower is exported by default). Leaving it unset risks different behaviour on different devices. Checked 2026-10-20 on the manifest element pages: a provider is not exported by default when the app targets API 17 or higher, a service or receiver defaults to exported when it has an intent filter and to not exported without one, and an activity defaults to not exported without filters.
   For an app targeting Android 12 (API 31) or higher, an activity, service or receiver that has an intent filter and no explicit value does not install on Android 12 or later: the build tooling reports a merge error or a lint warning, and an older tool shows an install-verification failure. The behaviour-changes page says to set true for the launcher activity and false in most other cases.
3. **An accidentally exported component can lead to** denial of service, other apps changing internal behaviour,
   leaked sensitive data and code execution in your app's context (the page's list).
4. **Export only what another app must start,** and write down who. Permission-based protection of an exported
   component is not on this page, but the manifest pages for services and receivers say a caller must hold the named permission (a service call without it is not delivered), with the application-level permission as the fallback and no protection when neither is set; a provider has separate read and write permissions, and grants of temporary access are off by default (`grantUriPermissions`). The permissions page recommends the signature protection level for access limited to your own apps, says only packages signed with the same certificate may declare the same permission name, and describes a known-certificates option from Android 12 (pages read 2026-10-20). Re-read 2026-10-20 on the activity manifest page: without intent filters the value defaults to false, and an activity with filters must be set to true to be startable by other apps; the page does not state a default for the with-filters case.

5. **Filters are not a security feature.** The platform security tips page (read 2026-10-20) says to validate input in the receiver, to use an explicit intent when binding to a service (an implicit bind throws an exception since API 21), to protect a receiver with a permission on the element or by naming the permission when sending, and, for a provider, to use parameterised queries, noting that a concatenated selection argument is still injectable and that write access can leak values through crafted WHERE clauses. For caller identity in a bound interface it points to a calling-permission check, and to a signature comparison of the calling package before handing credentials over.

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
   says to use it only when strictly necessary and after weighing the security impact. A separate Android 16 feature, strict intent matching, is described on the Android 16 behaviour-changes page (read 2026-10-20) as opt-in through `intentMatchingFlags` on the application or a component: explicit intents must then match the target's intent filter and an intent with no action matches no filter; it applies only between apps, logs blocked intents under the package-manager tag, and the page says the plan is to make it the default later. Do not confuse the two.
7. **For apps that target Android 12 (API 31) or later, StrictMode can flag an unsafe launch,** when the app unparcels a
   nested intent from the extras of a delivered intent and immediately starts a component with it (`startActivity`,
   `startService` or `bindService`). The page words this as helping "in some cases".
