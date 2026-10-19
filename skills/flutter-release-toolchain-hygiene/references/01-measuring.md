# flutter-release-toolchain-hygiene §1 — Measuring

Sources: the Flutter website pages on build modes, UI performance and measuring app size, and the Flutter API
reference for image decode size and the image cache, read 2026-10-08. Behaviour is that of those pages on
that date.

## 1.1 Speed: profile mode, real device
1. **Measure in profile mode on a physical device.** The UI-performance page says almost all performance
   debugging should be done that way, and that debug mode, simulators and emulators are generally not
   indicative of release behaviour.
2. **Check the slowest device your users might reasonably use,** same page.
3. **Why debug misleads:** it enables extra checks such as asserts that can be expensive, and it compiles
   Dart just in time while profile and release builds are compiled ahead of time, so JIT pauses can look like
   jank (same page). The build-modes page adds that hot reload exists only in debug mode and that the emulator
   and simulator run only debug mode; profile mode is disabled there because their behaviour is not
   representative.
4. **Profile mode keeps enough tracing for DevTools.** On web, DevTools cannot connect to a profile-mode app;
   the build-modes page points to the browser's own tools for web.

## 1.2 Size: which build to read
1. **A debug build's size is not representative,** and neither is a default release build made for upload:
   the stores reprocess the upload and split it for the downloader's hardware, filtering by screen density
   and CPU architecture (app-size page).
2. **On Android, upload the app bundle and read the download and install size in the store console's size
   view;** the console computes download size for a reference device (the page names a very high density
   screen and a 64-bit ARM architecture), so a given user's size varies.
3. **On iOS, build an archive and export with app thinning for all compatible device variants,** then read the
   thinning size report; the page says an exact figure needs a release upload to the store's build service,
   and that IPAs are commonly larger than APKs.
4. **For a breakdown by package, build with the analyze-size flag** (documented for APK, bundle, iOS, Linux,
   macOS and Windows targets since Flutter 1.22). Its output is of the unfiltered upload package, so
   duplicate architectures and densities it shows may be filtered by the stores.
5. **Record the size per release** from those reports, so a regression is a difference between two numbers of
   the same kind (our guidance).

## 1.3 Image decode size
1. **Decode an image at the size it is shown.** The API reference for the image constructors says the
   cache-width and cache-height parameters make the engine decode at that size, primarily to reduce the image
   cache's memory use, while the layout size still follows the widget's constraints. They are ignored on web.
2. **The image cache is bounded:** the API reference describes a least-recently-used cache of up to 1000 images
   and up to 100 MB. A decode at full resolution of many large images fills it fast; a smaller server-side
   derivative of the original is the better fix than a larger cache (our guidance).
3. **Pre-cache only what the next screen or two will show** (our guidance; no page read here states a limit).
