# over-engineering-review §1 — Extra tags and guards

> Section 1 of `skills/over-engineering-review`. Read it when a finding is about duplication or a function that
> does too much, before calling code unused, before reporting an audit, and before quoting a `net:` figure.
> New points are appended at the end; existing numbers never change.

## Two more tags
1. **`merge:`** near-copies that must change together: two handlers, two mappers or two validators that differ
   by a constant. A `merge:` finding names both locations, since half a finding is no finding. Distinct from
   `to-delete:` (a duplicate of something that already exists elsewhere): here neither copy is the original.
2. **`split:`** one function or class doing several unrelated jobs, so it is hard to read or to test, such as a
   Laravel controller action that validates, writes three tables and formats the response. **Split by job,
   never by line count**, and never into helpers whose only purpose is to make a function shorter: a
   function that is long but does one job gets no finding.

## `reuse:` names the path
3. **`reuse:`** the repository already has this helper: the new code should call it. The finding must name the
   path of the existing helper. "There is probably a helper for this" is a guess; `reuse: app/Support/Csv.php:12`
   is checkable. In audit mode the same applies to two helpers doing one job: keep one and name its path.
   When the duplicate is itself dead code, the finding is `to-delete:` instead; one finding, one tag.

## Before calling code unused
4. **Grep the whole tree before saying code is unused:** source, tests, fixtures, config files, and string or
   dynamic references (a class name in a config array, a route action written as a string, a component looked
   up by name). The one-caller check of `over-abstraction:` is not enough for `to-delete:`.
5. **If the grep cannot settle it, say so in the finding** and list it under what could not be checked,
   rather than assuming. Reflection and dynamic dispatch are the usual cause.

## A deliberate shortcut is a decision
6. **A shortcut whose limit is stated is not a finding,** unless the load the system is expected to meet
   already crosses that limit. "No pagination, the list never exceeds fifty rows" is a decision; the same
   sentence on a table that has ten thousand rows in production is a finding, and the number goes in it.
7. **Where the limit is written is the team's, not this block's.** Comments in code are not written here
   (`skills/code`), so the statement lives in the merge request description, the plan or a decision record; a
   limit nobody wrote down is not a stated limit. The feature's `debt.md` is the place to record it (§2).

## Audit mode honesty
8. **Say which parts you did not read.** An audit of a large repository goes deep where a mistake costs the
   most; the report ends with the folders or flows that were not opened, so "nothing found" is not read as
   "all clean".
9. **A cap on findings is allowed, and the report states how many were left out.** A top list of the worst
   findings is more useful than forty equal ones, as long as the count of those not listed is visible.
10. **"Nothing found" stays a valid result** (already in the output section); it is repeated here only
    because a cap and a "not read" list make it easy to pad. A category that is clean is called clean.

## The `net:` figure is an estimate
11. **`net: -N lines possible` is a low estimate of lines a deletion would remove, never savings achieved.**
    Nothing was deleted yet, and for code that was never written there is no baseline to subtract from.
    Do not turn it into a percentage, a cost, or a "you saved" sentence.
