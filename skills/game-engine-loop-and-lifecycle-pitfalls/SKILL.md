---
name: game-engine-loop-and-lifecycle-pitfalls
description: "Use when writing or reviewing game code on a scene-tree or entity engine (Godot first, the same traps in Unity and Unreal): frame-rate-dependent movement, fixed versus variable update steps, per-frame allocation and lookups, scene and node lifecycle, signals and event leaks, resource loading hitches, and save data."
---

# game-engine-loop-and-lifecycle-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for code that an engine calls many times per second. The premise: **the
engine owns the loop and the object lifetimes, and a game works on the developer's machine at one frame rate
and breaks on every other**: movement tied to frames runs twice as fast on a fast display, a node freed in the
middle of a callback crashes the next one, an allocation per frame turns into a stutter every few seconds, a
connection nobody removed keeps a dead object alive. Language-level rules for C and C++ are in `c-conventions`
and `cpp-conventions`.

## When
- Movement, timers, animation or physics code is written or changed.
- A script creates, frees, moves or reloads scenes, nodes or entities.
- A hitch, a leak, a desync between machines or a crash on scene change is reported.
- Save files, settings or downloadable content are introduced.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Delta time, fixed and variable steps, physics callbacks, input, determinism | motion, timers or physics code is touched | [`01-time-and-update-steps.md`](./references/01-time-and-update-steps.md) |
| 2 | Per-frame cost, node and entity lifecycle, signals and events, loading, save data | objects are created, freed, loaded or saved, or a hitch is reported | [`02-lifecycle-cost-and-persistence.md`](./references/02-lifecycle-cost-and-persistence.md) |

## Output / checkpoint
For a change touching this block: every movement and timer is scaled by the step the engine passes in, physics
work runs in the physics callback, nothing allocates or searches by name inside a per-frame callback, every
freed object is freed through the engine's deferred path, and the change was run at two different frame rates
(for example capped low and uncapped), not only at the editor default.

## Guardrails
- Scale every per-frame change by the elapsed step (§1.1). Never add a constant per frame.
- Move physics bodies from the physics callback (§1.2). Never from the render callback.
- Cache references and reuse objects (§2.1). Never search by name or allocate inside a per-frame callback.
- Free through the engine's deferred call and disconnect what you connected (§2.2, §2.3). Never free an object a callback is still running on.
- Save plain data with a version field (§2.4). Never serialise live engine objects.
- Engine APIs change between major versions; re-read the documentation of the version in use (🟡, nothing here was run in an engine).

## Origin
Written from our own craft knowledge of game loops and scene-tree engines; engine behaviour is stated as general
facts in our words. No source text was taken. See [`references/origin.md`](./references/origin.md).
