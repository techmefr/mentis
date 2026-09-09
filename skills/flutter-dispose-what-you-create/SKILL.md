---
name: flutter-dispose-what-you-create
description: "Use when writing or reviewing a widget's dispose(): never dispose a controller you didn't create — a constructor-injected controller belongs to its caller, disposing it there is a double-dispose crash."
---

# flutter-dispose-what-you-create

Narrow trigger extracted from `skills/flutter-conventions` §1.12–§1.13, so a widget's `dispose()`
method routes here directly instead of only through the whole Flutter block.

## When
Writing or reviewing a widget's `dispose()` (or a state holder's `close()`), specifically when the
widget also releases a subscription or disposes a controller.

## Steps
1. **Never dispose what you didn't create.** A controller passed in through the constructor belongs
   to the caller; a state holder owned by a provider is closed by that provider. Disposing either
   here is a double-dispose crash, surfacing in a different file than the one you're reading.
2. **Release in the reverse order of the dependency.** Cancel a subscription before disposing the
   controller it writes into — otherwise the last callback in flight arrives at a disposed object,
   and the crash names the controller instead of the listener that was still running.

## Output / checkpoint
`dispose()` only tears down what this widget's `initState`/`late final` field created; anything
received through the constructor is left untouched. Subscriptions are cancelled before the
controllers they write into are disposed.

## Guardrails
- Pairs with `flutter-no-controller-in-build` — instances hoisted correctly out of `build` still need
  a matching, correctly-ordered teardown here.
- **`dispose` runs even when `initState` didn't finish** — if setup threw halfway, teardown still
  executes against half-initialised fields, so a `late final` never assigned throws from `dispose`
  and hides the original failure (`skills/flutter-conventions` §1.15).

## Origin
No external source: this is `skills/flutter-conventions` §1.12–§1.13 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
