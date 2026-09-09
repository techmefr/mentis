---
name: flutter-context-after-await
description: "Use when a widget or state holder touches BuildContext after an await: guard it — mounted between the await and the use, or capture the navigator/messenger before the await, never context in a state holder."
---

# flutter-context-after-await

Narrow trigger extracted from `skills/flutter-conventions` §1 (opening rule) and §1.2, so a
`BuildContext` used after an `await` routes here directly instead of only through the whole Flutter
block.

## When
Any code that does `context.` — navigation, a snack bar, a dialog, a theme or media-query read, a
provider lookup — reached after an `await`, a `Future.wait`, a loop that awaits per item, or an
awaited navigation that returns a result.

## Steps
1. **After any `await`, the `BuildContext` is suspect.** It either throws ("this widget has been
   unmounted") or silently misfires — a snack bar on a scaffold nobody can see, a dialog on a dead
   navigator — and it's invisible in review because the code reads as straight-line.
2. **In a stateful widget: check `mounted` between the await and the context use** — a check placed
   before the await is useless, since the widget can unmount *during* it.
3. **In a stateless widget: capture what you need before the await** — the navigator or messenger
   object itself, not the context.
4. **In a state holder (cubit/bloc): don't touch context at all.** Emit, and let the widget listen.
5. **One guard per await, not one per method.** Every resumption point (each `await`, each iteration
   of an awaiting loop) is its own gap and needs its own check — including after an awaited
   navigation that returns a result.

## Output / checkpoint
Every `context.` use that follows an `await` sits behind a fresh `mounted` check (stateful widget), a
value captured before the await (stateless widget), or is absent entirely (state holder) — with one
guard per resumption point, not one per method.

## Guardrails
- Never silence the analyzer's async-context lint with an ignore comment — it flags a latent crash,
  not a false positive (`skills/flutter-conventions` §1.7).
- The full three-shapes-by-location breakdown lives in `skills/flutter-conventions` §1; the
  after-navigation-result variant is `skills/flutter-conventions` §5.12 — read it before assuming one
  shape covers every widget kind.

## Origin
No external source: this is `skills/flutter-conventions` §1's opening rule and §1.2 extracted to its
own trigger. Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
