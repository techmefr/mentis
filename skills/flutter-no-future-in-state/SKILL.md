---
name: flutter-no-future-in-state
description: "Use when a cubit/bloc/state class holds a Future or Stream: never store the future itself, only its result — an unresolved future in state re-triggers itself on every rebuild."
---

# flutter-no-future-in-state

Narrow trigger extracted from `skills/flutter-conventions` §7.6, so a `Future`/`Stream` held in
state routes here directly instead of only through the whole Flutter block.

## When
Defining or reviewing a state class (cubit, bloc, or any state holder) whose field type is a
`Future<T>` or a `Stream<T>` rather than a resolved value.

## Steps
1. **Never put a `Future` or a stream in state; put its result.** A state holding an unresolved
   future cannot be compared, cannot be rendered without a second builder inside the first, and
   re-triggers itself on every rebuild.
2. Resolve the future/stream at the point it starts (e.g. in the state holder's own method), then
   emit the resolved value — loading, then success/error carrying data, not the awaitable itself.

## Output / checkpoint
No field or emitted state in the diff has type `Future<...>` or `Stream<...>` — every state carries
already-resolved data (or an explicit loading/error marker), never the awaitable.

## Guardrails
- This is the state-layer side effect of the same problem as an object built fresh every `build` —
  the parent block calls it out as arriving through the state layer specifically.
- The four-states discipline (`flutter-four-async-states`) is what the resolved value should be
  rendered through — this file only covers what state should *hold*.

## Origin
No external source: this is `skills/flutter-conventions` §7.6 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
