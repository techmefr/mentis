# flutter-release-toolchain-hygiene §3 — Pub and code generation

Sources: the Dart site's pub pages (dependencies, packages, get command, security advisories, versioning), the
agent-plugins package-conflict skill (BSD-3-Clause), and the build_runner package page, read 2026-10-08.
Rules marked "skill" come from that skill file.

## 3.1 Constraints and the lockfile
1. **Use caret constraints in the manifest.** They let the resolver choose newer non-breaking versions up to
   the next major; the lockfile holds the exact resolved versions for reproducible builds (skill).
2. **Pub resolves one version of each package for the whole graph** (skill), which is why a conflict is a
   resolution problem and not something to work around in code.
3. **A manifest change and its lockfile change go in the same commit** (our guidance).

## 3.2 CI resolves what was tested
**Resolve with the enforce-lockfile option in CI and for production builds.** The pub documentation says it
fails when the lockfile does not exactly satisfy the manifest or a hosted package's content hash has changed,
and recommends it for CI and deploying to production. It guards against both an untested version and a
tampered or changed archive.

## 3.3 Conflicts and upgrades
1. **Never delete the whole lockfile to clear a conflict or a retracted version.** Remove only the entry of the
   offending package and run `pub get`; deleting all of it upgrades the whole graph at once (skill).
2. **Read the outdated report's columns before editing anything:** current (in the lock), upgradable (the
   newest version the manifest's constraints allow), resolvable (the newest that resolves with everything
   else) and latest (the newest published). Upgradable moves with an upgrade command; resolvable above
   upgradable needs a constraint change (skill).
3. **After upgrading, tighten the lower bounds** with the upgrade command's tighten option, then analyze and
   test (skill). A major bump edits the constraint by hand.
4. **After removing a dependency, search `lib/` for leftover imports** (our guidance): one that still
   resolves through another package's dependency breaks the next time that package changes.

## 3.4 Advisories
1. **Pub reports security advisories when it resolves** (the pub client prints the affected package and a link
   at `pub get`). The Dart team's advice is to read the advisory and, if it affects the app, strongly consider
   moving to a non-affected version.
2. **An ignored advisory is a decision recorded where it can be reviewed.** The manifest's
   ignored-advisories list applies to the root package only and has no reason field, so the reason goes in
   the commit message (our guidance).

## 3.5 Code generation
1. **Scope each generator to the directory that owns its annotations** with `generate_for` globs in the
   package's build configuration, so one edit does not regenerate everything (build_runner package page, which
   gives the example of restricting a builder to one folder).
2. **Use watch mode as a local convenience only;** a CI job runs a single build (our guidance).
3. **Generate, then analyze** (our guidance): stale or missing generated files produce analyzer errors that
   point at the call site, not at the stale file. Generated files are never edited by hand and their globs are
   excluded from the analyzer so machine output is not linted (the analyzer-exclude pattern is in the
   agent-plugins static-analysis skill).
