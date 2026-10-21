# react-native-expo-pitfalls §1 — Project and dependencies

Sources: the `expo-overview`, `expo-project-structure`, `expo-router` and `expo-upgrade` skills of expo/skills at 7ddc1f5, read 2026-10-20.

## 1.1 Read the project first
1. **Read the `expo` version in `package.json` and the app config before giving any version-specific advice.** Defaults and APIs differ by SDK; the source treats the SDK number as the first fact to establish.
2. **Look up documentation pinned to that SDK, not the "latest" pages.** The latest pages track the newest SDK and can describe an API the project does not have yet.
3. **A bare React Native project with no `expo` dependency is not Expo work.** Do not suggest Expo-only tooling there.
4. **Committed `ios/` and `android/` folders mean native projects exist** (bare or after prebuild). With no such folders the native projects are generated at build time. Say which one the project is in before touching native setup.

## 1.2 Installing packages
1. **Add packages with the SDK-aware installer (`npx expo install <pkg>`), not a plain add.** It selects the version that matches the SDK; a version chosen by hand is the usual cause of "works in the editor, crashes on device".
2. **After removing a dependency, run the project diagnostic (`npx expo-doctor`) at once** and restore anything it reports as a missing required peer.
3. **Do not remove formerly implicit packages wholesale** (`@babel/core`, `babel-preset-expo`, `expo-constants`). Keep any package an installed dependency declares as a required peer; the router needs `expo-constants` as a direct dependency, and a transitive copy can break native autolinking outside Expo Go.
4. **Whoever installs, the operator runs it** (the no-install rule in `CONVENTIONS.md`): name the command and stop.

## 1.3 Routes and layout
1. **The routes folder holds routes only.** Every file in it becomes a route, so components, types and helpers placed there become screens. Put them in sibling folders and let a route file render the screen body.
2. **The app must always have a route for `/`,** possibly inside a group.
3. **Define stacks in layout files, and present modals and sheets through the stack's screen options** rather than building a custom modal component.
4. **File names in kebab-case, no special characters, and delete the old route file when a route moves.** A forgotten file keeps serving the old URL.
5. **Server API routes live in one folder and server-only helpers in another,** because they run in a server environment and may read variables the app bundle must never see (§2, public variables). Never import server helpers from a screen.
6. **Layout advice is for new projects only.** In an existing project follow the layout it already has; do not move files to match a template.
7. **From SDK 56 the source says application code must not import from the `@react-navigation` packages and takes the router's own entry points instead; only the module specifier changes, the runtime API does not.** It applies to SDK 56 and later; before that the old imports are the right ones.

## 1.4 Platform-specific code
1. **Small differences use the platform check; larger ones use platform files** (`.ios`, `.android`, `.native`, `.web`) imported without the extension.
2. **A default file without a platform extension is always required,** even if it is a no-op for a single-platform component, and the props of every variant must be identical.

## 1.5 Checks (own guidance)
1. Print the SDK version and say whether native folders are committed; every later recommendation is conditional on those two facts.
2. List the routes folder: every file is meant to be reachable by URL.
3. After any dependency change the diagnostic is clean and the app starts on a device or simulator, not only in the bundler.
