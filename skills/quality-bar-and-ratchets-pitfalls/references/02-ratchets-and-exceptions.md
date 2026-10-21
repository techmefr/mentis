# quality-bar-and-ratchets-pitfalls §2 — Ratchets and exceptions

Source: the constraint-driven-development skill of addyosmani/agent-skills (MIT), read 2026-10-20; the reasoning on defaults is ours.

## 2.1 Do not invent a target; measure and hold
1. **Symptom:** an 80 percent coverage rule on a codebase well under it: the build is red for ever and the team
   learns to ignore red builds. **Fix:** a ratchet. Record today's value and a direction (must not fall, must
   not grow) in a "measured, not yet enforced" table and compare every run to the recorded value, not to an
   aspiration.
2. **When a value improves, update the record; when it drops, that is the finding.** The record moves one way.
3. **Tolerance is a decision.** Unrelated changes can shift a project-wide metric slightly; either measure
   changed lines (a number the author can move) or write down the tolerance and why. A tolerance nobody wrote
   down becomes the room in which the number slides.
4. **Why a ratchet beats a rule.** A model is rewarded for green, and slow decay (structure, size, risk) never
   shows up within one task. The record is the missing penalty, kept where the build can read it.

## 2.2 Choosing a number anyway
1. A default threshold copied from an article is a guess. Name where a number came from (a standard such as a
   web performance "good" band, a regulation, the current value) and re-read that source when it is old
   (`skills/source-freshness`).
2. **Re-read before relying:** the defaults in the source repository (coverage on changed lines, mutation
   score, exception lifetime, ratchet tolerance) were not checked against any study and are not carried here.
3. Prefer a ratchet to a number when the team has no basis for one.

## 2.3 Exceptions
1. **Symptom:** a rule is too strict for a legacy folder, so someone deletes the rule. **Fix:** an exception row.
2. **Row shape:** identifier, rule, path scope, reason, owner, expiry date. Scope it to a path, not to the whole
   repository.
3. **An expiry is mandatory and short enough to be remembered.** Pick a lifetime per project; a year or more is
   a permanent waiver with a date on it.
4. **An exception has an owner and a way out.** The reason says what work removes it and where that work is
   tracked.
5. **Expired means failing.** A check reads the table and fails on a past date, or the table is decoration.
6. **Review the table on a schedule.** A row nobody discussed is a loosening (§3.1); a row nobody reopens is a
   rule that quietly stopped.

## Checks
1. Metrics without a target are recorded with a value and a direction.
2. Every threshold names its source or its measurement date.
3. Every exception row has an owner, a path scope and a future expiry, and a check reads the dates.
