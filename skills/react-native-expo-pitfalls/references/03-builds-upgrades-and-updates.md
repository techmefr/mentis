# react-native-expo-pitfalls §3 — Builds, upgrades and over-the-air updates

Sources: the `expo-dev-client`, `expo-upgrade`, `eas-update` skills and the new-architecture reference of expo/skills at 7ddc1f5, read 2026-10-20.

## 3.1 Expo Go or a development build
1. **Expo Go is a playground for the native libraries it bundles; a real app moves to a development build.** A development build is required for local native modules, Apple extension targets, third-party native modules Expo Go lacks, config plugins, and testing remote push or universal links.
2. **Building locally is free; cloud builds and device distribution use the plan's allowances and an Apple developer account.** State the cost before choosing the cloud path.

## 3.2 Upgrading the SDK
1. **An upgrade is its own task:** install the target SDK, then align every dependency with the installer's fix mode, then run the project diagnostic. Do not bump versions by hand.
2. **Read the release notes for removed APIs and moved imports** (the source's checklist lists them; reading first is our advice), and update all usages of a deprecated package (the audio and video packages, the permissions package) before removing it.
3. **Run a clean prebuild only when native folders are committed** and the upgrade needs native changes; with generated native projects the step does not apply. Clear the native caches (pods, Gradle, derived data) only in that bare case.
4. **Review `expo.install.exclude` and local patches after an upgrade:** they are often workarounds the new SDK no longer needs.
5. **The new architecture is on by default for new projects since SDK 52 and for existing ones in SDK 53 and 54; SDK 54 is the last one where it can be switched off, and from SDK 55 it is always on. Expo Go supports only the new architecture** (Expo documentation, new-architecture guide, sections on new and existing projects). An old native module that does not support it is the usual migration blocker: check its repository before the upgrade, not after.
6. **The current animation library major (Reanimated 4) needs the separate worklets package installed and runs only on the new architecture; the older major is the one for the old architecture and is no longer actively maintained** (Reanimated documentation, getting started). The SDK number at which the vendor bundles the newer major (the source says 54) was not confirmed.
7. **Version-bound warning (source at the stamped commit):** the vendor's upgrade skill reports a memory regression with the worklets and animation packages on the newer JavaScript engine build, affecting SDK 55 apps that enabled it, every SDK 56 app, and SDK 57 releases before 57.0.9. It advises upgrading straight to SDK 57 at 57.0.9 or later, skipping 56 from SDK 55 or earlier, and not steering users to opt in or out of the engine. Re-read the release notes: this is a point-in-time bug report.

## 3.3 What an over-the-air update can carry
1. **An update carries JavaScript, styling and bundled assets. Native code or native configuration needs a new build** (Expo documentation, runtime versions: a new build is required whenever native code changes before publishing). Do not work around a runtime mismatch, and do not imply that publishing adds a native capability to an installed binary.
2. **The model:** a build has a platform, a runtime version and a channel fixed at build time; an update targets one platform and runtime version; a branch is an ordered stream of updates; a channel points to a branch on the server. A build gets an update only if platform and runtime version match and its channel points to the branch holding it.
3. **Changing a channel's branch mapping affects every build on that channel;** it does not change what an individual installation embeds.
4. **Changing the runtime-version policy is a separate decision:** it changes which installed builds can receive future updates.
5. **Use the vendor's configuration command rather than hand-writing the update URL, runtime version or channels,** and review its diff. Dynamic app config needs the documentation, not guesses.

## 3.4 Publishing and testing
1. **Publishing changes remote state on installed apps.** Establish project, channel, environment, platforms, runtime version and message first, publish to a preview channel to validate, and publish to production only when the person asked for that channel by name. Never infer production from the current Git branch.
2. **An exported update receives the variables of the chosen environment,** so the environment is a deliberate choice (§2, public variables).
3. **A release build normally starts the cached or embedded update and downloads a new one in the background; the new one runs on a later launch.** For manual testing, fully terminate the app, reopen, wait, and if nothing changed terminate and reopen once more: up to two cold launches. Do not shorten the startup timeout to hide this; if the product needs a prompt, use the update API to offer a non-blocking restart.
4. **A development build does not follow the release startup flow;** preview updates in it through its own extensions screen or the dashboard.

## 3.5 When an installed build does not update
1. Check the update was published to the intended project, channel or branch, platform and environment.
2. Check the installed build's platform and runtime version equal the update's.
3. Check the build actually contains the expected update URL and channel; app-config changes take effect only in a newly compiled build.
4. Check the channel's branch and that branch's active update.
5. Allow for a full termination and the download-then-apply lifecycle.
6. Never bypass a compatibility or safety check to make an update appear.

## 3.6 Checks (own guidance)
1. Every "ship it without a build" claim is backed by a diff that touches only JavaScript, styles and assets.
2. The test plan names the build type, the number of launches, and the runtime version of the installed build.
