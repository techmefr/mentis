# react-native-expo-pitfalls: origin and source stamps

> Provenance of `skills/react-native-expo-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation-style skill files, never run by us on a device, simulator or EAS
build. No Expo project was created, built or updated while writing it.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: applicability gate for projects without the framework, web-view secret storage check, catch-all offline handling, device-clock caution, bundle search without a fixed path.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| expo/skills at commit 7ddc1f5 (2026-10-17): `expo-overview/SKILL.md`, `expo-project-structure/SKILL.md`, `expo-router/SKILL.md` | MIT, Copyright (c) 2025-present 650 Industries, Inc. (`LICENSE` read 2026-10-20; frontmatter `license: MIT`) | SDK detection, pinned docs, SDK-aware install, native folders, routes-only folder, platform files |
| expo/skills at 7ddc1f5: `expo-data-fetching/SKILL.md`, `references/offline-and-cancellation.md`, `expo-native-ui/references/storage.md` | MIT (same file) | Four states, hydration gate, saves, offline, cancellation, storage choice, public variables |
| expo/skills at 7ddc1f5: `expo-dev-client/SKILL.md`, `expo-upgrade/SKILL.md`, `references/new-architecture.md`, `eas-update/SKILL.md` | MIT (same file) | Development build criteria, upgrade steps, new architecture, update model, testing and debugging order |
| Expo documentation pages: New Architecture guide, EAS Update runtime versions | product documentation, facts only, rewritten, read 2026-10-20 | Default architecture by SDK, Expo Go support, native change needs a build, runtime version guarantees compatibility |
| Reanimated documentation: getting started | product documentation, facts only, rewritten, read 2026-10-20 | Worklets package required, new architecture only for the current major |
| Expo documentation: environment variables guide | product documentation, facts only, rewritten, read 2026-10-20 | Public prefix inlined at build time, literal dotted access only, no secrets, reload and rebuild behaviour |
| TanStack Query v5 documentation: queries, network mode, query retries guides | product documentation, facts only, rewritten, read 2026-10-20 | Pending versus paused fetch status, default of three retries with doubling delay |

## Removed (stated in the sources, not carried)
- Everything about SwiftUI and Compose components, animation, design tokens, Tailwind, app clips, brownfield embedding, DOM components and web-to-native migration: other subjects.
- Store submission, TestFlight and metadata (the `eas-app-stores` skill): not read; `mobile-release` is the block for it.
- All code samples, the feedback-submission commands and the telemetry instructions.
- The source's launch-without-dev-menu arguments (a harness for driving the app, not a project rule).

## Not verified
1. **SDK ranges, re-checked 2026-10-20.** New architecture: new projects from SDK 52, existing ones default-on in 53 and 54, last SDK allowing it off is 54, always on from 55 (corrected again from "all from 53"). Router imports: the source's migration page applies to SDK 56 and later (confirmed). Engine memory regression: SDK 55 with the engine enabled, all of 56, 57 before 57.0.9, per the upgrade skill at the commit (restated precisely); a point-in-time bug report. The worklets requirement is confirmed as a Reanimated 4 requirement; the SDK that bundles it was not found in the page.
2. **Key-value storage steer.** The source says never to use the async package and gives no reason; "legacy" was our word and is removed. It is the vendor's position at this commit, not a platform rule.
3. **Costs.** The plan, build-minute and Apple-account remarks are paraphrased from the files; pricing was not read.
4. **Own guidance, labelled in the text:** the retry-safety remark and the device-clock remark (§2.4), the single shared token refresh (§2.5.3: the source sketches a refresh without sharing it), every "Checks" section, and the order of the not-updating checklist beyond what the source lists.

**Re-opened and confirmed 2026-10-20** against the files at the stamped commit: SDK read first, pinned docs, SDK-aware install, committed native folders, routes-only folder, `/` route, kebab-case, API and server folders, platform files with a required default and identical props, new-projects-only layout, four screen states, status check before parsing, keep stale data on refetch, cancellation and online-manager wiring, development build criteria and costs, upgrade steps, peer and `expo-constants` rule, deprecated packages, runtime version model, production only on explicit request, two cold launches, development build test path, native change needs a new build. The Expo runtime-version page confirms what the version guarantees and the two named policies; the plan, build-minute and Apple-account remarks match the dev-client skill (no prices were read).
5. **No command, flag or configuration key was executed.**

## Related blocks
`mobile-release` (store submission, signing, version codes), `react-nextjs-conventions` (React rules shared with
web), `mobile-crash-symbolication-pitfalls`, `source-freshness`.

Independent verification 2026-10-21: 10 checked, 10 matched, 0 corrected, 0 unverified
