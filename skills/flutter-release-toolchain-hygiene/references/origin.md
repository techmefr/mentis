# flutter-release-toolchain-hygiene: origin and source stamps

> Provenance of `skills/flutter-release-toolchain-hygiene`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No build was made, no store upload
attempted and no CI job run while writing it. Folding targets: §1 and the accessibility part of §4 into the
performance and accessibility-testing points of `flutter-conventions` (main branch sections, any time); §2
into the release block and §3, §4 into the Dart-habits and testing sections that exist only on the
unmerged branch of PR 118. Until then this block stands alone so nothing cites a section that is not on the
main branch.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Flutter website pages: build modes, UI performance, measuring app size, Android and iOS deployment, accessibility testing (repository files) | CC-BY-3.0 text, BSD code (repository LICENSE), read 2026-10-08 | Profile mode on a device, JIT versus AOT, size of which build, the size report, version line, unique iOS build numbers, guideline matchers and scanners |
| Flutter API reference: image decode-size parameters, image cache | BSD-3, read 2026-10-08 | Decode at display size, cache bound |
| Dart site pages: pub dependencies, packages, get command, security advisories, `dart analyze`, `dart format` (repository files) | CC-BY-4.0 text, BSD-3-Clause code (repository LICENSE), read 2026-10-08 | Enforce-lockfile, advisories and their ignore list, fatal-infos, format check flag |
| Agent-plugins package-conflict, static-analysis and coverage skills (files) | BSD-3-Clause, read 2026-10-08 | Caret constraints, surgical lockfile edit, outdated columns, tighten, analyzer options, coverage script |
| build_runner package page on pub.dev | BSD-3-Clause package, read 2026-10-08 | `generate_for` scoping, watch mode |
| Android developer pages on versioning and on manifest merging | Site terms not read; facts only | Version code uniqueness and maximum, merge priority, merged view and report |
| Apple page on uploading builds in App Store Connect | Site terms not read; facts only | The build string identifies a build |

## Removed in the verification pass (no page supporting them)
"A failed upload still burns the number" (the Apple page read does not say), any claim about the iOS privacy
manifest, nutrition labels, store data-safety declarations, an in-app account-deletion requirement and
store-listing limits (Apple and Play policy pages were not read; those parts of the earlier review item were
dropped), "randomise test order" and "coverage includes files no test imports" as stated facts (the
test-ordering flag was not found in the pages read, and the coverage point is kept only as a reading of the
skill's validation step), the "`--delete-conflicting-outputs` clears every cached output and must not be
combined with a path filter" claim and the "generate before analyze" ordering as sourced rules (the
build_runner pages read do not mention the flag; the ordering is kept as our guidance), "lint include file is
coupled to the SDK", "the SDK constraint is a range while the tested tool version is recorded in a committed
file", "refuse transitive crash or analytics SDKs by policy", "wrap a single-maintainer plugin behind an
interface" (all from one skill, product-policy rather than documented), "tag the exact released commit", and
"pre-cache only what the next one or two screens show" as sourced (kept as our guidance).

## Not verified
1. **Own guidance, flagged in the text:** size recorded per release (1.2.5), server-side derivative and
   pre-cache limit (1.3), bump rather than retry (2.2.3), merged-manifest check on each plugin change (2.3.4),
   manifest and lockfile in one commit (3.1.3), leftover-import search (3.3.4), advisory reason in the commit
   message (3.4.2), watch mode and generate-then-analyze (3.5), CI never fixes (4.1.4), every gate named
   (4.1.5), await matchers and pin surface size (4.2.2, 4.2.3), coverage reading (4.3.2), exclusion
   mirroring (4.3.3).
2. **Apple behaviour on a failed upload's build number** and any iOS privacy or account policy were not read
   from Apple's pages.
3. **Page text was read partly through a fetch tool that summarises,** namely the Android, Apple and
   build_runner pages; the Flutter and Dart site pages were read from their repository files.
4. **Whether the Flutter Android page's offset for split builds is still the same** was read from the
   repository text, not tried.
5. **The `dart format` check flag combination** in the Dart format page was read; the Flutter wrapper's
   behaviour with the same flags was not.

## Related blocks
`flutter-conventions`, `ci-workflow-hardening`, `accessibility`, `ship`, `deprecation-migration`,
`flutter-agent-loop`.
