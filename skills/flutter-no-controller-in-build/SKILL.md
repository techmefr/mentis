---
name: flutter-no-controller-in-build
description: "Use when a controller, future, or stream is instantiated inside build(): never there — hoist to initState or a late final field, or every rebuild leaks a fresh, undisposed instance."
---

# flutter-no-controller-in-build

Narrow trigger extracted from `skills/flutter-conventions` §1.14, so instantiating a controller,
future or stream in `build` routes here directly instead of only through the whole Flutter block.

## When
Writing or reviewing a widget's `build` method that constructs a controller (animation, text,
scroll), a `Future`, or a `Stream` directly inside the method body.

## Steps
1. **Never create a controller, future or stream in `build`.** A fresh instance gets created every
   rebuild, and none of the previous ones get disposed.
2. **Hoist it to `initState` or a `late final` field.** The instance is created once and lives for
   the widget's lifetime, matched by a corresponding `dispose()`.

## Output / checkpoint
No `build` method in the diff calls a constructor for a controller, future, or stream — every such
instance is created in `initState` (or as a `late final` field) and disposed in `dispose()`.

## Guardrails
- This pairs with `flutter-dispose-what-you-create` — hoisting out of `build` only fixes half the
  problem if the hoisted instance is never disposed.
- The reverse-order-of-dependency release rule and the "dispose runs even when initState didn't
  finish" trap live in `skills/flutter-conventions` §1 — read it before assuming hoisting alone is
  sufficient.

## Origin
No external source: this is `skills/flutter-conventions` §1.14 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
