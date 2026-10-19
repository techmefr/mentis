# flutter-native-bridge-ffi §2 — FFI and hooks

Sources: the ffigen and native-assets skills of the Flutter agent plugins (files dated 2026), the Dart site's
hooks page, the Dart API reference pages for `isLeaf`, `asTypedList` and `NativeFinalizer`, and the Dart
C-interop overview, read 2026-10-08. The API reference page for the leaf flag was the documentation of Dart
3.13.5 when read.

## 2.1 Reaching for FFI
1. **Justify it before writing it** (our guidance): name the measured need, why pure Dart, an existing plugin
   or a channel (§1) is not enough, and who will maintain the native toolchain and ABI afterwards.
2. **For a large API surface, the Dart overview recommends generating the wrappers from the C headers with
   the ffigen package** rather than writing them by hand.

## 2.2 Bindings are generated
1. **If the native headers exist, never hand-write the lookups, native function declarations or struct
   classes.** The agent-plugins ffigen skill says hand-written bindings are error-prone and brittle and
   requires the generator.
2. **The generator is a script in the package's tool directory,** resolves its paths relative to the script,
   and the output file uses the `.g.dart` suffix; third-party headers live under a third-party directory and
   their bindings under a matching `lib/src/` directory (skill's layout rules).
3. **Restrict generation to a positive inclusion list** of the functions, structs and enums the package
   uses, so the generated surface stays small and reviewable.
4. **Run the generator and the analyzer before finishing.** A lint warning in the generated file is silenced
   in the generator's preamble, not by changing the package's rules; a real error in the generated file is
   never patched by hand and is reported to the generator's maintainers (skill).
5. **A licence header matching the native library's licence** goes in the generated file's preamble (skill).

## 2.3 Leaf calls
**Mark a native function as a leaf only if it does not call back into Dart and does not block.** The API
reference describes leaf functions as small, short-running, non-blocking, not allowed to call back into Dart
or use the VM's APIs; a blocking leaf call can stall garbage collection and thread coordination for the
whole isolate group.

## 2.4 Native memory and handles
1. **A typed-list view over native memory is a view, not a copy.** The API reference says the caller must
   ensure the memory range stays accessible while the list is used, and that an optional finalizer can be
   attached; zero-copy therefore comes with a lifetime obligation.
2. **Write down who owns each allocation before allocating it** (our guidance; the API pages read did not
   state an allocator-pairing rule, so none is asserted here).
3. **A native finalizer releases a resource after its Dart object becomes unreachable,** and the API
   reference promises every attached finalizer is called at least once before the isolate group shuts down
   normally, but says it cannot be relied on when the process crashes or is terminated. For timely release,
   release explicitly and detach the finalizer; keep the finalizer as the backstop.

## 2.5 Build and link hooks
1. **Hooks live in the package's `hook/` directory:** a build hook compiles or bundles native code as code
   assets; a link hook can tree-shake unused native code before bundling.
2. **Read the project's Dart floor first.** The Dart site says build hooks arrived in Dart 3.10 and link
   hooks with recorded-use tree-shaking in Dart 3.13. The Dart site also describes hooks as the successor to
   the older name "native assets".
3. **Compile through the toolchain package, never by calling a compiler,** and keep paths relative and
   platform-independent (the skill's constraints).
4. **A downloaded prebuilt library is checked against a stored hash** (the skill names MD5 or SHA-256 lookup
   tables; prefer SHA-256), and the hook offers an offline path such as building locally when the download is
   unavailable.
5. **Treat a native build as part of the release surface:** each platform and architecture the app ships is
   built and loaded once on a real device (our guidance; the pages read did not list the combinations).
