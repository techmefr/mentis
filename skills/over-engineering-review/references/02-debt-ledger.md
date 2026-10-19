# over-engineering-review §2 — Debt ledger

> Section 2 of `skills/over-engineering-review`. Read it when a change takes a deliberate shortcut, when a
> reviewer meets a stated limit, and when the operator asks what has been deferred. New points are appended at
> the end; existing numbers never change.

A deferral is a shortcut taken on purpose, knowing it is not the final form: no pagination, one hard-coded
tenant, a polling loop where a queue belongs. It is a decision, not a finding (§1 point 6). What turns a
decision into debt nobody owns is that its limit lives in one person's head. The ledger keeps the limit and the
reason to revisit it where the team can read them.

## Where the record lives
1. **The record is `specs/<NNN>-<name>/debt.md`**, an extra artefact of the feature's spec-kit folder, beside
   `spec.md`, `plan.md` and `tasks.md` (`CONVENTIONS.md` Rule E). It is not a second place for requirements or
   tasks, and it is not a comment in the code, which this repository does not write (`skills/code`).
2. **The project wins.** If the project's own spec-kit template or constitution already has a place for
   deferrals, use that place and let the scan read it there; do not add a parallel file next to it.
3. **Every feature has its folder, so every deferral has a home.** A change small enough to skip a plan still
   gets a short `spec.md` (`skills/speckit`), and that folder is where its `debt.md` goes.

## One row per deferral
4. **The row has four cells:** where (a file, class or function name, never a line number, which moves), what
   was simplified, the ceiling, the trigger.

   | Where | Simplified | Ceiling | Trigger |
   |---|---|---|---|
   | `InvoiceExporter` | one synchronous export, no queue | about 200 invoices per run | a customer needs more than 200, or the run passes 30 seconds |

5. **The ceiling is the limit at which the shortcut stops being acceptable**, written as a number or a
   checkable condition. "For now" and "small" are not ceilings.
6. **The trigger is an event someone can observe** that says it is time to pay the debt back: a count reached, a
   second consumer, a date, a requirement landing. "Later" and "when we have time" are not triggers.
7. **A row without a trigger is kept, tagged `no-trigger`, and counted.** Those are the rows that rot: nothing
   will ever make anyone open them. Never drop the row for lacking a trigger, and never invent one to look
   complete.
8. **A deferral without a ceiling is not yet a decision.** Ask the author for the limit; do not guess it. An
   invented ceiling is the unlabelled hypothesis the whole workflow refuses.
9. **The row is written in the same change that takes the shortcut**, and removed in the change that pays it
   back; history stays in version control. Only open deferrals are counted.

## The scan
10. **The scan is report-only.** It reads every `specs/*/debt.md`, changes nothing, and prints one line per
    row: `<feature>, <where>, <simplified>. ceiling: <ceiling>. trigger: <trigger or no-trigger>.`
11. **It ends with a count:** `N entries, M with no trigger.` With no rows at all it says
    `No deferral debt recorded.` and names whether no `debt.md` exists or the files are empty.
12. **It reads `debt.md` files and never greps code.** A deferral that exists only as a comment, a commit
    message or a remembered conversation is not in the count, and the report says the scan sees recorded
    deferrals only: an empty ledger is not proof that nothing was deferred.
13. **A crossed ceiling is a finding.** When a row's ceiling is already below the load the system meets, report
    it under §1 point 6 with the number, instead of listing it as healthy debt.
