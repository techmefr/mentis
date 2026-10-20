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

## Removed (stated in the sources, not carried)
- Everything about SwiftUI and Compose components, animation, design tokens, Tailwind, app clips, brownfield embedding, DOM components and web-to-native migration: other subjects.
- Store submission, TestFlight and metadata (the `eas-app-stores` skill): not read; `mobile-release` is the block for it.
- All code samples, the feedback-submission commands and the telemetry instructions.
- The source's launch-without-dev-menu arguments (a harness for driving the app, not a project rule).

## Not verified
1. **SDK ranges.** Statements tied to an SDK number (new architecture from 53, worklets from 54, router imports from 56, an engine memory regression across 55 to an early 57) are the files' claims at the commit; none was checked against the SDK changelog. Re-read before relying on them.
2. **Key-value storage steer.** The vendor's preference for its SQLite-backed local storage over the older async package is its position at this commit, not a platform rule.
3. **Costs.** The plan, build-minute and Apple-account remarks are paraphrased from the files; pricing was not read.
4. **Own guidance, labelled in the text:** the retry-safety remark (§2.4), every "Checks" section, and the order of the not-updating checklist beyond what the source lists.
5. **No command, flag or configuration key was executed.**

## Related blocks
`mobile-release` (store submission, signing, version codes), `react-nextjs-conventions` (React rules shared with
web), `mobile-crash-symbolication-pitfalls`, `source-freshness`.
