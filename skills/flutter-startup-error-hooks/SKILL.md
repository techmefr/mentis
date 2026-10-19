---
name: flutter-startup-error-hooks
description: "Use when writing or reviewing a Flutter app's main() and cold-start path: installing the framework and platform-dispatcher error hooks first, what a hook must return, what the first frame may wait for, deferring warm-up, flushing state when the app goes to the background, and the startup traps of a state library (Riverpod automatic retry, eager initialisation, experimental mutations; Bloc public surface)."
---

# flutter-startup-error-hooks

Step 6 of the pipeline (`WORKFLOW.md`), for the one function every Flutter app runs before any screen exists:
what is installed first, what is allowed to block the first frame, and what the process must save before the
OS can end it. The premise: **an error that happens before the hooks exist, or after a hook that itself
fails, is an error nobody ever sees**. Crash-reporting initialisation as a point is in `flutter-conventions`
§9; the lifecycle observer's add and remove pairing is in `flutter-conventions` §1; screens that render the
resulting failure are `flutter-four-async-states` and `flutter-conventions` §4.

## When
- Writing or editing `main`, a bootstrap function, or the widget at the root of the tree.
- A cold start shows a white screen, the wrong theme for a frame, or a "not responding" dialog.
- An async error never shows up in the crash reports, or every report names the same wrapper type.
- Using Riverpod or Bloc and a failure looks like a long spinner or a leaky public surface.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Launch order, the two error hooks and their return value, what the first frame waits for, post-frame warm-up, flushing on background | `main` or a bootstrap function is written or reviewed | [`01-launch-and-error-hooks.md`](./references/01-launch-and-error-hooks.md) |
| 2 | Riverpod automatic retry, eager initialisation, experimental mutations, Bloc and Cubit public surface | a provider fails slowly, a provider must exist before the first screen, or a state holder's public methods are written | [`02-state-library-startup.md`](./references/02-state-library-startup.md) |

## Output / checkpoint
The app was cold-started in profile or release mode on a device: the first frame showed the right theme, a
thrown error from the launch path and one from an unawaited future both reached the report, and a
background-then-resume cycle kept the last change (§1). A `main` that was only read is not verified.

## Guardrails
- Never let an error hook throw, and never return `false` from the platform-dispatcher hook for an error the
  handler has recorded (§1).
- Never await warm-up work in `main` (§1).
- Never treat the background flush as the only write: the platform can end the process with no notice (§1).
- Never build shared infrastructure on an API its own documentation calls experimental (§2).
- Versions: each rule names the documentation it comes from and the date it was read. Nothing was run while
  writing this block.

## Origin
Rewritten from the Flutter documentation on error handling, the Flutter API reference (error hook, post-frame
callback, lifecycle state), a startup skill and a bootstrap reference from two MIT-licensed agent skill
repositories, and the Riverpod and Bloc documentation sources, read 2026-10-08. The point 1.2-1.3 hook rules
are meant to extend `flutter-conventions` §9 when its owner folds them in. 🟡: never run by us; open points
are in [`references/origin.md`](./references/origin.md).
