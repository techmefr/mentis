# deno-bun-runtime-pitfalls §2 — Compatibility, tooling and production

Source: own craft knowledge, with the points marked "Deno docs" or "Bun docs" checked on 2026-10-20 (MIT repositories, rewritten in our words, nothing copied). Compatibility levels and tool behaviour move with each release and are to be re-read for the version in use.

## 2.1 Node compatibility
1. **Compatibility is a percentage of an API surface, not a guarantee for your dependencies.** A library passes on the runtime's compatibility page and still fails on the one built-in function or stream behaviour it uses; run the real dependency in the real flow. (Bun docs, Node compatibility page re-read 2026-10-20: compatibility is per module with three states (full, partial, not implemented); partial built-ins include the async-hook module, whose hook creation is a stub with async identifiers always zero, the cluster module, whose HTTP load balancing across workers works only on Linux, the diagnostics-channel, child-process (some IPC limits) and worker-thread modules; Deno docs, Node page: Node's own test suite passes for a large share of cases (over three quarters in the release the page describes). The vendor figures are not a guarantee for a given library.)
2. **Symptom: works in tests, fails at the first rare path in production** (a file upload stream, a child process, a worker thread, a crypto mode, a diagnostics hook). Fix: exercise those paths in an integration test on the shipping runtime before the port is called done.
3. **Test on the runtime that ships.** A suite run on Node proves nothing for Bun or Deno; run the same suite on each runtime you support and keep the matrix explicit.
4. **Frameworks with deep Node assumptions** (custom module loaders, instrumentation that patches built-ins, APM agents) are the most likely to break. List them before the port and check their documentation for the runtime.
5. **Do not rely on global object differences.** Code that detects the runtime by a global and branches is a maintenance cost; isolate the difference behind one adapter module.

## 2.2 Native code
1. **Node native addons built for Node's binary interface may not load on the other runtimes.** Check for a pure-JavaScript or WebAssembly alternative, or the runtime's own foreign-function mechanism, and see the runtime's native-addon support level in its documentation. (Deno docs, Node page: Node-API addons are supported in npm packages that use the public interface, they need a local dependency directory (a configuration option) and the native-library permission; a skipped install script can leave the binding missing. Bun's Node-API page, read 2026-10-20, says it implements the interface from scratch so most existing addons load with require or the process load function, and lists no limitations ("most" is not "all": test yours).)
2. **Prebuilt binaries are chosen by platform and runtime version.** A container on another architecture or libc fails at start; test the image on the target architecture.
3. **Foreign-function access needs the runtime's most dangerous permission or none at all** (Deno docs: native code in the process is outside what the permission layer checks). Keep it behind a narrow wrapper, validate inputs and review it like unsafe code.

## 2.3 Built-in tooling
1. **Built-in test runners, formatters, linters and bundlers are convenient and have their own semantics.** A test that depends on module mocking, snapshot format or timer behaviour of the old runner needs porting, not just a changed command.
2. **Pin the tool by pinning the runtime version;** built-in tools change with it. Record the version in the project and CI.
3. **A bundler output is an artefact to test.** Run the bundled build in a smoke test; a tree-shaken or minified bundle can differ from source behaviour, especially around dynamic imports and side-effect-only packages.
4. **Compile-to-executable features embed the runtime in a binary.** Treat the binary as an artefact with its own version and security updates; a patched runtime requires a rebuild. Deno docs (compile reference, re-read 2026-10-20): the program is embedded into a stripped runtime binary, runtime and permission flags must be given at compile time and are baked in, cross-compile targets exist, and the smaller experimental engine option comes without the main engine's security updates and with slower compute. Check which flags an executable was built with before shipping it.

## 2.4 Performance claims
1. **Published benchmarks measure small programs, not yours.** Startup time, HTTP throughput and file speed vary with workload, version and operating system. Measure your own service with your own dependencies before using speed as the reason to switch.
2. **Compare on equal terms:** same machine, same warm-up, same concurrency, same payloads, several runs. A figure without these is anecdote; write down your measurement method with the result (`load-and-capacity-testing-pitfalls`).
3. **Weigh speed against the operational cost:** a smaller ecosystem, fewer production references, and a faster release cadence mean more upgrades to track.

## 2.5 Production and CI
1. **Pin the runtime version in the container image and the pipeline** and build from the official image of that exact version; the same code on a floating tag changes behaviour at the next pull.
2. **Run as a non-root user, drop permissions, and pass the signal-handling flags the runtime needs** so a stop request reaches the process and drains requests (`node-container-runtime` §1 applies).
3. **Handle shutdown signals in code** and close servers and pools; test with a stop command rather than assuming the runtime does it.
4. **Keep an escape route.** Write code against standard web APIs and a thin adapter for runtime features so a return to Node, or a move to the other runtime, is a day of work, not a rewrite.
5. **Check the support and security update path.** Know where advisories are published for the runtime, who updates the image, and how fast; a pinned runtime that nobody updates is its own risk.

## Checks
- The real dependencies and rare paths ran on the shipping runtime (§2.1).
- Native dependencies have an equivalent for the target platform (§2.2).
- Tool versions are pinned; bundles are smoke-tested (§2.3).
- A speed claim comes from your own measurement (§2.4).
- Runtime version pinned, non-root, signals handled, update path known (§2.5).
