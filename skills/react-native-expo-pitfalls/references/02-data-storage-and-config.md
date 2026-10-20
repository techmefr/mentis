# react-native-expo-pitfalls §2 — Data, storage and configuration

Sources: the `expo-data-fetching` skill (with `references/offline-and-cancellation.md`) and the `expo-native-ui` storage reference of expo/skills at 7ddc1f5, read 2026-10-20.

> Framework-neutral except where a point names the Expo library: it applies to a React Native app with or without Expo and to a web-view shell. Say "not applicable: <reason>" for a point the project has no code for.

## 2.1 Four states per screen
1. **Design loading, error, empty and content for every screen that loads data.** They can overlap: a failed refresh coexists with cached content.
2. **Loading is not empty.** Empty means resolved with zero items. In TanStack Query v5 the first-fetch flag is true only while a first fetch runs; a disabled or offline-paused query has no data and is not loading, so show the prerequisite or offline state.
3. **A refetch keeps the stale content.** Render cached data when a refresh fails, with a non-blocking error and a retry; spinners are for the first fetch, a pull-to-refresh control for user-initiated reloads.
4. **An empty list is a designed state:** say why it is empty and offer the next action (create, or clear the filter).

## 2.2 Hydration
1. **When the first screen or a redirect depends on persisted state (token, onboarding flag), render nothing, or the splash, until that state has loaded.** Deciding on unhydrated state flashes the wrong screen on every cold start and misroutes a deep link that arrives early.

## 2.3 Saves
1. **While a mutation is pending, disable repeat submission. On failure keep the draft, show an inline error and allow a retry;** clear the form only after success.
2. **An optimistic update restores the previous value, or marks the edit as unsynced, on failure.**

## 2.4 Network
1. **Check the response status before reading the body.** A bare fetch resolves on a 404 or a 500; throw a typed error carrying the status and tell it apart from a network failure. A catch-all that treats every failure as offline is a defect: serve the cached fallback for a network error only, and let a 401, 403 or 5xx reach the screen as its own state. Check: grep each `catch` around a request and see whether it branches on the status.
2. **Retries use backoff and a limit.** Own guidance: retry only requests that are safe to repeat, and give a write an idempotency key first (`skills/unknown-payment-outcome-pitfalls`).
3. **Cancel on unmount.** Abort the request in the effect cleanup and ignore the abort error; the query library does it for its own requests.
4. **Offline: feed the query library's online flag from the network-status listener,** so queries pause when offline and resume on reconnect.
5. **A cached or offline evaluation that depends on the device clock can be bypassed** by moving the clock (own guidance). Where a rule (a time lock, an expiry, a schedule) is evaluated on the device from a cache, say that the server remains the authority, store the last server time with the cache and refuse to trust a device clock that is earlier than it.
6. **The source prefers the platform `fetch` over axios** for new code; treat it as the vendor's preference, not a rule.

## 2.5 Storage
1. **Tokens, passwords and device secrets go in the secure store, never in plain key-value storage or in the web-view `localStorage`.** In a web-view shell (no Expo) the equivalent is the platform keychain or keystore reached through a native plugin; any script running in the web view reads web storage. Check: grep the writes to key-value or web storage (`setItem`, `AsyncStorage`, `localStorage`) next to names like `secret`, `token`, `password`, `key`, `credential`; each hit is a finding unless the value is public. The native secure store is a plugin choice, so name the plugin the project already has before proposing one. The source's choice by use: small settings in the key-value polyfill, large or relational data in SQLite, sensitive data in the secure store.
2. **The vendor now steers away from the legacy async key-value package** towards its SQLite-backed local storage (re-read before relying on it for your SDK).
3. **Refresh a token once for concurrent callers:** share the in-flight refresh promise so ten failing requests trigger one refresh, not ten.

## 2.6 Public variables
1. **Only variables with the public prefix reach the bundle, and they are inlined at build time.** Changing one needs a rebuild or a bundler restart; it is not a runtime setting.
2. **Anything with the public prefix is readable by whoever has the app.** Never put a write-capable key or a database password there; secrets belong to server routes, in variables without the prefix.
3. **Validate presence at startup:** an API client that reads an unset variable should throw a named error, not call `undefined/users`.

## 2.7 Checks (own guidance)
1. Turn the network off on a screen that has cached data: content stays, an inline error appears, nothing blanks.
2. Kill and relaunch the app with a stored token and an incoming deep link: the first visible screen is the right one.
3. Search the built bundle for the strings of your secrets; there must be none. Use the project's own build output folder (for a web-based shell, the folder the build copies into the binary; for React Native, the exported bundle) and search it with a text search; if the build folder is unreadable or absent, say the check was not run.
