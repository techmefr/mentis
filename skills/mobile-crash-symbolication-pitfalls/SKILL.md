---
name: mobile-crash-symbolication-pitfalls
description: "Use when a native crash from an iOS or Android app has to be turned into function names and source lines: Apple .ips crash logs (two JSON parts, image base addresses and offsets, the faulting thread, the application-specific information field), Android tombstones (frame lines, library-relative offsets, build ids that logcat output often drops), matching the debug symbols to the exact binary by UUID or build id, the atos and llvm-symbolizer invocations and what each address means, NativeAOT and app-owned binaries, and when to stop instead of guessing."
---

# mobile-crash-symbolication-pitfalls

Used inside the `debug` step of the pipeline (`WORKFLOW.md`), for the moment a crash report from a device is nothing but hex
addresses. The two sections share one premise: **a symbolicated frame is only as true as the match between the
report and the symbol file**, so every rule is about reading the report the way its format means it, matching
the symbols by identifier and not by name or date, and stopping when they do not match. The source is a pair
of .NET runtime diagnostic skills; the rules here are the platform-generic ones, and the .NET specifics appear
only as the worked example. Instrumentation and crash reporting setup are in `skills/observability-instrumentation`; the cause-finding
method itself is in `skills/debug`.

## When
- A crash arrives as an Apple `.ips` file or an Android tombstone and the frames show only addresses.
- A symbolicated stack names a function that cannot be right, or most frames stay unresolved.
- Symbols are being kept, downloaded or looked up for a release build.
- A log pasted into a ticket has lost the identifiers needed to symbolicate it.

## Steps

**Read the section the task meets; most crashes need both.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Reading the report: the Apple two-part JSON, address arithmetic, which thread and which field to read first, the Android frame line, lost build ids | a crash file has just been opened, or an identifier is missing | [`01-reading-the-report.md`](./references/01-reading-the-report.md) |
| 2 | Matching symbols and stopping: UUID and build id, the tools and their arguments, owned binaries, validation, stop signals | symbols are being fetched or applied, or a result looks wrong | [`02-matching-symbols-and-stopping.md`](./references/02-matching-symbols-and-stopping.md) |

## Output / checkpoint
For each symbolicated crash: the identifier of every binary used (UUID or build id) matched the one in the
report, at least one frame resolved to a function name and its path looks like the right code base, the
faulting thread is explained before the others, and the frames that stayed unresolved are listed with their
identifiers and addresses. A trace made from symbols whose identifier was not compared is not evidence.

## Guardrails
- Never symbolicate with a symbol file whose UUID or build id was not compared with the report (part 2,
  point 1).
- Never add a library's base address to an Android tombstone offset (part 1, point 6).
- Never treat a file as Apple JSON without checking its first line, and never run the Apple steps on a
  tombstone, or the reverse (part 1, point 1).
- Never keep retrying a download that returned not found; one attempt per identifier (part 2, point 5).
- Never install a toolchain just to symbolicate; give the commands to run instead (part 2, point 7).
- Never paste a customer's crash file, which can contain device identifiers and paths, into a ticket or a
  prompt without removing them.
- This block states the source's documentation at the commit in
  [`references/origin.md`](./references/origin.md). No crash was symbolicated while writing it and the
  Microsoft symbol server URLs were not requested.

## Origin
Rewritten from two diagnostic skills and one reference page of dotnet/skills (MIT), read 2026-10-16. 🟡: never
run by us; open points are in [`references/origin.md`](./references/origin.md).
