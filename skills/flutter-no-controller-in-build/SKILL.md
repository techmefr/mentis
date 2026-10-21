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
Extracted from `skills/flutter-conventions` §1.14 (written 2026-09-09). Checked 2026-10-20 against the
`FutureBuilder` API page (the future must be obtained earlier, in `initState`, `didUpdateWidget` or
`didChangeDependencies`, never in `build` or when constructing the builder, because any `build` call may
happen every frame and a new future restarts the task) and the Flutter cookbook page on fetching data (an API
call in `build` is not recommended; storing the future in state runs it once). That sources the future half of
step 1 and the hoisting in step 2. The controller and stream halves rest on the same reasoning (a new
instance per rebuild, none disposed) and on the `AnimationController` and `State.dispose` pages for the
disposal pairing, but no page read states the rule for them in those words. Site terms not read, facts only.
🟡: never run by us.
