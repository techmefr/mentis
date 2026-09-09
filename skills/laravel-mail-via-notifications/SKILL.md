---
name: laravel-mail-via-notifications
description: "Use when a user needs an email or in-app message: never hand-built Mail from a controller, always a channel-agnostic notification."
---

# laravel-mail-via-notifications

Narrow trigger extracted from `skills/laravel-conventions` §6.16 and §8.7, so "send the user a
message" routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing code that sends a user-facing email or in-app message — a controller action,
an action class, a listener reacting to an event.

## Steps
1. **User-facing email or in-app messaging is not the controller's job.** It goes through a
   notification, never a hand-built `Mail::send`/`Mail::to(...)->send(...)` call sitting in a
   controller or action.
2. **One channel-agnostic notification per event**, with the channels chosen per recipient — adding
   an in-app or push channel later becomes a configuration change, not a second copy of the message.
3. **Hand-rolled mail skips what the notification layer already handles**: queueing, locale, and the
   recipient's own channel preferences — each has to be re-implemented by hand once skipped.

## Output / checkpoint
Every user-facing message is dispatched as a notification (`$user->notify(...)` or
`Notification::send(...)`), never a direct `Mail::` call outside a notification's own `toMail()`.

## Guardrails
- A notification's own `toMail()` method is exactly where `Mail`-shaped code belongs — the rule is
  about the call site, not about never touching the mail API.
- The full argument, alongside realtime broadcasting's authorisation question, lives in
  `skills/laravel-conventions` §8 — read it before treating a "quick" hand-built mail as harmless.

## Origin
No external source: this is `skills/laravel-conventions` §6.16 and §8.7 extracted to its own trigger.
Written 2026-09-09, same pilot as `laravel-no-db-enums`.
