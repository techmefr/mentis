# feature-flag-lifecycle §3 — Testing both states, removal, and flag debt

> Part 3 of `skills/feature-flag-lifecycle`. Read it when tests are written for a flag, when a flag reaches full
> rollout, or when flags are reviewed.
> Source, read 2026-10-19: Martin Fowler, "Feature Toggles (aka Feature Flags)"
> (https://martinfowler.com/articles/feature-toggles.html). Sentences marked "own guidance" are ours; the
> quiet-period idea comes from one MIT skill collection and no length is carried over.

1. **Test both states.** A flag that can be on or off in production has to be validated in both. The article
   notes that every combination of many flags is not testable, so it narrows the set: the configuration
   expected in production (including flags about to be turned on), the fallback with those new flags off, and
   now and then all flags on to catch later regressions.
2. **A test that only covers the new path proves half the change.** Own guidance: the off state is what an
   incident falls back to, so a regression there is the worse one.
3. **Tests set the flag explicitly, never by inheriting the environment.** The article suggests an in-memory
   way to reconfigure flags for tests and debugging only; it must not become a production control. Own
   guidance: a test that depends on whatever the flag source says today fails for the wrong reason later.
4. **Full rollout starts a quiet period, not a deletion.** When the flag reaches everyone, keep it for a
   period chosen by the owner (long enough to see the effects that only appear on a full weekly or monthly
   cycle, short enough that nobody forgets), watch the signals of §2, then remove. Own guidance, the length is
   deliberately not given: it depends on how fast the feature shows its problems.
5. **Removal deletes the whole branch.** Keep the new path, delete the old one and its tests, remove the flag
   definition and its record, and archive the entry with the date. Deleting only the definition leaves a
   conditional that now reads a missing flag. The deletion itself follows `skills/deprecation-migration`
   where users of the old behaviour exist (an API, a stored format).
6. **Removal is not optional for release and experiment flags.** Their value ends with the rollout or the
   test; the article's carrying-cost argument is that each remaining one costs tests, reading time and
   mistakes. An experiment that nobody calls is a flag that has already outlived its purpose: decide or end it.
7. **Operational and permission flags are reviewed, not deleted on a clock.** They are long-lived by design, so
   the question at review is whether the trigger and the owner still exist (§1 points 2 and 5).
8. **Flag debt is the list of flags past their expiry, without an owner, or at full rollout with no removal
   task.** Own guidance: audit it on a rhythm the team already has (planning, a release cut), read the
   record rather than the code alone, and treat a flag nobody can explain as a defect to fix or delete.
9. **A flag with no owner is reassigned or removed.** When the owner leaves a team, the record is handed to a
   named person the same week; a flag held by nobody is the one that survives longest.
10. **Pace creation to removal.** Teams that remove flags as fast as they add them keep the inventory flat; if
    the audit keeps growing, the cause is upstream (point 3 of §1: flags that were never needed), and a ceiling
    from §1 point 9 is the control.
