---
name: react-native-expo-pitfalls
description: "Use when writing or reviewing a React Native app built with Expo: project layout and Expo Router, installing packages against the SDK, data fetching and offline states, token and key-value storage, EXPO_PUBLIC variables, development builds against Expo Go, SDK upgrades, and over-the-air updates with runtime versions and channels."
---

# react-native-expo-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the traps that are specific to Expo projects. The premise: **a React
Native app fails in the gap between the JavaScript you edit and the native binary already installed**: a package
version the SDK does not know, a variable inlined at build time, a screen decided before storage has loaded, an
update that no installed build can receive. Store submission is in `mobile-release`; Flutter is in `flutter-conventions`.

## When
- A project has an `expo` dependency, or the request names Expo, EAS or an `expo-*` package.
- A package is added, an SDK is upgraded, or a screen that loads data is written.
- A secret, a token or a persisted flag is stored.
- A change is meant to ship without a new binary.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | SDK detection, installs, routes folder, platform files, native folders | a project is opened, a package or file is added | [`01-project-and-dependencies.md`](./references/01-project-and-dependencies.md) |
| 2 | Four screen states, hydration, saves, offline, storage, public variables | a screen loads data, or anything is persisted or configured | [`02-data-storage-and-config.md`](./references/02-data-storage-and-config.md) |
| 3 | Development build or Expo Go, SDK upgrade, over-the-air updates | a native dependency changes, an upgrade or an update is planned | [`03-builds-upgrades-and-updates.md`](./references/03-builds-upgrades-and-updates.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: the SDK was read before any
version-specific advice, packages came in through the SDK-aware installer, no secret sits in a public variable,
no screen decides on unhydrated state, and every update claim names the platform and runtime version it covers.

## Guardrails
- Install packages with the SDK-aware installer, never with a bare package-manager add (§1.2). Never pin a version from memory.
- Put nothing but routes in the routes folder (§1.3).
- Never store a token in plain key-value storage, and never put a secret in a public variable (§2, storage and public variables).
- Publish to a production channel only on an explicit request that names channel, platform and runtime version (§3.4).
- Never promise that an update can add native code to an installed build (§3.3).
- Facts are given for the SDK range named in each section at the stamped commit; nothing here was run on a device (🟡).

## Origin
Rewritten from the `expo/skills` repository (MIT, commit 7ddc1f5), read 2026-10-20. Version-bound facts and own
guidance are listed in [`references/origin.md`](./references/origin.md).
