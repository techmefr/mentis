# loop-design: origin of the references

> Provenance of `skills/loop-design/references/`. Read it to trace a rule to its source, never to apply one. The
> origin of `SKILL.md` stays there.

## Section 1 (`01-multi-session-harness.md`), added 2026-10-20

**Status: 🟡.** Never run by us. No text of any repository was taken for this section.

The method (an initializer then worker sessions, a task list changed only by a pass flag, one feature per session,
a re-check of one earlier pass before new work, a progress file, a clean tree at exit, a command allowlist that
fails closed) was written from a method sheet made by a reviewer who read public sample material describing
long-running coding harnesses, plus our own craft. One sample folder whose licence statement is inconsistent
was deliberately not opened for this section; the rules are ideas and methods, which stay free, stated in our
own words and structure.

**Ours, not sourced.** The reviewed initializer output (point 2), the independent sampled pass over flags
(point 11), the test of the allowlist against substitution and chaining (point 12), the specification re-read
(point 14) and the three stop conditions (point 10).

**Not verified.** Nothing was run. The claim that the allowlist in the public sample misses command substitution
and redirections rests on the reviewer's static reading and was not tested; point 12 asks for the test rather than
asserting the gap.
