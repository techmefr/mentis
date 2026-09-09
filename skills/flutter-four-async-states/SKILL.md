---
name: flutter-four-async-states
description: "Use when a screen renders data from an async source: render all four states explicitly — loading, success, empty, error — never a blank screen, never stale content presented as fresh."
---

# flutter-four-async-states

Narrow trigger extracted from `skills/flutter-conventions` §4.1–§4.2, so an async view routes here
directly instead of only through the whole Flutter block.

## When
Building or reviewing a screen or widget that renders data coming from an async source — a network
call, a database query, a stream.

## Steps
1. **An async view renders all four states explicitly: loading, success, empty, error.** Never a
   blank screen, never stale content presented as fresh.
2. **The four states belong to each data source, not to the screen.** A screen with two independent
   data sources needs four states tracked per source, not one set shared between them.
3. Treat the non-success states as the normal experience of the screen, not an edge case — a mobile
   network fails constantly (a lift, a tunnel, a handover between cells), so loading/empty/error show
   up routinely over a week of real use.

## Output / checkpoint
Every screen consuming async data has an explicit branch (or widget) for each of loading, success,
empty, and error — per data source when the screen has more than one — with nothing defaulting to a
blank or stale view.

## Guardrails
- A state holding an unresolved `Future` or `Stream` instead of its result breaks this — see
  `skills/flutter-conventions` §7.6 for why the result, not the future, belongs in state.
- The full section, including how a retriable error differs from a terminal one, lives in
  `skills/flutter-conventions` §4 — read it before collapsing states for a screen that seems simple.

## Origin
No external source: this is `skills/flutter-conventions` §4.1–§4.2 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
