# architecture-fitness-functions-pitfalls §2 — Adopting a rule on code that already breaks it

> Part 2 of `skills/architecture-fitness-functions-pitfalls`. Read it when the first run reports a pile of
> violations. Source, read 2026-10-20: ArchUnit user guide, "Freezing Arch Rules" and the ignore-patterns section
> of "The Lang API" (Apache-2.0). Sentences marked "own guidance" are ours and rest on no source read.

1. **Freeze the existing violations and fail only on new ones.** The guide's answer to hundreds or thousands of
   violations that cannot be fixed at once: wrap the rule so that the first run records every current
   violation in a store, and later runs report only violations not in it. When one is fixed, the store shrinks
   by itself, so the fixed violation cannot return. Symptom: a rule that never gets enabled because turning it
   on turns the build red. Fix: freeze, then ratchet.
2. **Keep the store under version control, in a path you chose.** The default store is a set of plain text
   files, meant to be committed so progress is tracked in history. Own guidance: review a change to the store
   like code; a diff that adds lines is a decision to accept a new violation and needs a reason in the review.
3. **A frozen store may only get smaller.** Own guidance: add a check, or a review rule, that rejects a change
   enlarging the store. Symptom: the store grows a little every sprint and the rule becomes decoration. Fix: the
   only legal edits are removals; an addition is a design discussion.
4. **Mind how violations are matched.** By default, the matching ignores line numbers, so a violation that
   merely moves within a class still counts as known. Own guidance: this is convenient but means a second
   violation of the same kind in the same class can hide among the known ones; for a critical rule, fix the
   class instead of freezing it.
5. **Control who may create or refresh the store.** The guide describes settings to allow creating a store at
   all, to forbid updating the stored violations, and an option that re-records the current state as
   accepted, which makes every frozen rule pass. Own guidance: leave refreezing off by default and run it
   only as a deliberate, reviewed act, such as after a format change in the tool; it is the same as deleting
   the rule for the moment.
6. **Use ignore patterns sparingly and by name.** The guide lets a classpath file hold regular expressions that
   are matched against violation messages; a violation matching a pattern is ignored, and a rule violated only
   by ignored violations passes. Lines can carry comments. Own guidance: a pattern naming one legacy class with a
   reason beside it is acceptable; a pattern matching a whole package or a verb such as "depend" waives the rule
   by accident. Review the patterns file with the same care as the store.
7. **Pair every frozen rule with a plan.** Own guidance: freezing records debt; it does not repay it. For each
   frozen rule name an owner, an intended end state (the store empties) and the slice of the work that would
   fix the largest cluster first; a rule frozen forever is an abandoned rule.
8. **Do not freeze to get a new change through.** Own guidance: a violation the current change introduces is
   fixed, or the decision is revisited in the record. Freezing happens once, at adoption, on a known snapshot.

## Checks (own guidance)
1. The store and the ignore file are committed, and each ignore pattern has a reason beside it.
2. The store's line count after the last N merges is not higher than before.
3. Each frozen rule has an owner and a date to review.
