---
name: laravel-idempotent-data-commands
description: "Use when writing or reviewing an artisan command that changes data: it is idempotent, or it refuses to run twice — key the second run on state, not on the assumption it hasn't happened yet."
---

# laravel-idempotent-data-commands

Narrow trigger extracted from `skills/laravel-conventions` §7.7–§7.9, so a data-changing console
command routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing an artisan command whose `handle()` inserts, updates, or deletes data — a
backfill, a data fix, a migration helper.

## Steps
1. **A command that changes data is idempotent, or it refuses to run twice.** Someone will run it
   again — after a timeout, after a failed deploy, or because the output scrolled past. Make the
   second run a no-op by keying on state, not on the assumption it hasn't happened yet.
2. **The command reports what it did, in counts.** "Done" is indistinguishable from a no-op — print
   the number examined, the number changed, the number skipped.
3. **A destructive command asks, and prefers a dry run.** Require explicit confirmation in
   production; where the work can be previewed, make the preview the default and the mutation the
   flag. Validate its arguments as strictly as a request payload.

## Output / checkpoint
Running the command twice on the same data produces the same end state as running it once, and its
output states counts (examined/changed/skipped) rather than a bare "done".

## Guardrails
- Idempotence here means keying on state (a natural key, a flag, a timestamp comparison), not on "it
  hasn't run before" — that assumption is exactly what a retried or re-run command breaks.
- The batching/interruption-survival rule and the scheduled-overlap-policy rule sit right beside this
  one in `skills/laravel-conventions` §7 — read it for a long-running or scheduled command.

## Origin
No external source: this is `skills/laravel-conventions` §7.7–§7.9 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
