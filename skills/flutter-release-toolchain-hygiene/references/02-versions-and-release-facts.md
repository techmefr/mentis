# flutter-release-toolchain-hygiene §2 — Versions and release facts

Sources: the Flutter website's Android and iOS deployment pages (repository text), the Android developer pages
on versioning and on manifest merging, and the Apple page on uploading builds, read 2026-10-08. The Apple and
Android pages were read through a fetch tool that summarises pages.

## 2.1 One version line
1. **The version line in `pubspec.yaml` is the source of both numbers.** Its text before the plus sign is the
   user-facing version, the part after is the build number (Flutter iOS page). On Android the Gradle file
   takes `versionCode` and `versionName` from it and says you generally need not edit them (Flutter Android
   page); on iOS they become the short version string and the bundle version.
2. **A build command can override each:** a build-name and a build-number flag (iOS page). An override is a
   second source and belongs in the release job's own record, not in a developer's shell history.
3. **A manual edit in Xcode is a third source.** The iOS page lists it as an alternative; if the project does
   that, the pubspec line stops being the only source and the rule above no longer holds.

## 2.2 Build numbers are never reused
1. **Play rejects an upload whose version code was already used** and requires each release to use a greater
   one; its largest allowed value is 2100000000 (Android versioning page).
2. **Each iOS upload needs a unique build number** (Flutter iOS page), and App Store Connect identifies a
   build by that string within the app and version (Apple upload page).
3. **So bump, never reuse.** The Apple page was not found to say what happens to the number of a failed
   upload; assume a number that reached either store's servers is spent, and bump rather than retry (our
   guidance).
4. **Split-per-architecture builds change the code:** the Flutter Android page says the framework adds a
   per-architecture offset (the architecture value times 1000) to the version code, because Play does not
   allow several APKs of one app to share a code; leave room for it.

## 2.3 The merged manifest is the real permission list
1. **The shipped Android manifest is the merge of the app's, the build variant's and every library's.** The
   Android manifest-merging page says the build merges all of them into one packaged file, and that library
   manifests have the lowest priority.
2. **Read the merged result, not the app's own file:** the manifest editor shows a merged view, and the build
   writes a merger report under the module's build outputs logs directory (same page). A plugin bump can add
   a permission the app's own manifest never mentions.
3. **The merger can add permissions implicitly** when a library targets a very old target SDK (the page's
   example), another reason to read the result.
4. **Check the permission set from the merged manifest of the release variant** whenever a plugin is added or
   upgraded (our guidance).
