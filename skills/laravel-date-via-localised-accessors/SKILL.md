---
name: laravel-date-via-localised-accessors
description: "Use when rendering a date as text (month name, weekday name, translated format): go through the date library's own localised accessors, never a lookup array keyed by month number or a match on it."
---

# laravel-date-via-localised-accessors

Narrow trigger extracted from `skills/laravel-conventions` §5.8, so a date-to-text rendering routes
here directly instead of only through the whole Laravel block.

## When
Writing or reviewing code that turns a date into user-facing text — a month name, a weekday name, a
translated format string.

## Steps
1. **A date rendered as text goes through the date library's own localised accessors** (Carbon's
   `translatedFormat`, or the equivalent), never a hand-rolled lookup array keyed by the month number
   or a `match` on it.
2. The hand-rolled version reinvents a catalogue the library already ships for every locale, and
   hardcodes user-facing text while doing it — a magic-strings violation riding along with the
   naming one.

## Output / checkpoint
No lookup array or `match` maps a month/weekday number to a hardcoded name anywhere in the diff —
every localised date render goes through the date library's accessor.

## Guardrails
- This is a specific instance of `laravel-no-magic-strings` (hardcoded user-facing text) arriving
  through the date-formatting door — two rules broken by one array.
- The full naming/typing/style section, including the English-everywhere rule this pairs with, lives
  in `skills/laravel-conventions` §5.

## Origin
No external source: this is `skills/laravel-conventions` §5.8 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
