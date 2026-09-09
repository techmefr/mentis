---
name: laravel-support-window-date
description: "Use when deciding a Laravel or PHP version for a new or existing project: the security-fix end-of-life date settles it, not opinion — a new project starts on the newest stable major, an existing one is planned off before its window closes."
---

# laravel-support-window-date

Narrow trigger extracted from `skills/laravel-conventions` §10.3, so a framework/language version
decision routes here directly instead of only through the whole Laravel block.

## When
Choosing which Laravel or PHP version a new project starts on, or deciding when an existing project
should upgrade off its current major/minor.

## Steps
1. **A version branch past its security-fix end of life is not a maintenance choice.** Both the
   framework's and the language's support windows are published and mechanical — the question has a
   date for an answer, not an opinion.
2. **A new project starts on the newest stable major and the newest minor that major supports.**
3. **An existing project is planned off a branch before its security window closes**, not after an
   advisory forces it.
4. **Staying behind compounds.** Each skipped major makes the next upgrade the one nobody has budget
   for.

## Output / checkpoint
The chosen version for a new project matches the current newest stable major/minor at time of
starting; an existing project's upgrade is scheduled against its actual published end-of-life date,
not against "whenever there's time".

## Guardrails
- Check the actual published support-window page for the framework and PHP version in question —
  this rule states the decision procedure, not a specific date, which changes over time.
- Neighbouring architecture decisions (dependency choice, functional/technical layering) live in
  `skills/laravel-conventions` §10 — read it for the rest of the architecture section.

## Origin
No external source: this is `skills/laravel-conventions` §10.3 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
