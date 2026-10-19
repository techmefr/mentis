---
name: reuse-before-write
description: "Use when about to write new code in an existing codebase (a feature, a component, a helper, a bug fix, a dependency choice), before the first line: read what the change touches, list everything it must reach, then climb a fixed ladder (does it need to exist, is it already here, does the language or platform do it, does an installed dependency do it, one readable line, the minimum) and keep the guards that stop the shortcut from cutting what must stay."
---

# reuse-before-write

The author-side half of the deletion hunt, at step `code` (6) of the pipeline (`WORKFLOW.md`). Where
`over-engineering-review` lists what should not have been written, this block makes the author stop before
writing it. `code` step 0 carries the ladder in one paragraph; this is the long form, with the guards that
make the ladder safe to follow.

The principle in one line: **be economical about the solution, never about the change.** The ladder shortens
what you write. It never shortens what you read, what you finish, or what you keep.

## When
- Before writing any new unit in a codebase that already has code: a feature, a component, a helper, a fix.
- Before adding a dependency, or before hand-building something a platform feature might give for free.
- When a request is vague ("build me an export") and the scope is yours to choose.

Not for a change that is already written (that is `over-engineering-review`, after the fact) and not for a
greenfield file nothing else touches, where only the last rung of the ladder applies.

## Steps

Read the rows whose trigger the task meets, in order: a section read is a section applied.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Read first, list the reach | always, before the ladder | [`01-read-and-reach.md`](./references/01-read-and-reach.md) |
| 2 | The ladder, six rungs | after §1, to choose what to write | [`02-the-ladder.md`](./references/02-the-ladder.md) |
| 3 | The guards, never-cut list, bug fixes, tests, closing note | the ladder produced a shorter answer, or the change is a fix, moves code or has logic | [`03-guards-and-closing.md`](./references/03-guards-and-closing.md) |

## Output / checkpoint
The change itself, plus a closing note of one or two lines: what was skipped on purpose and what was not
checked, with any risk the reviewer must know (§3). This block writes no checkpoint of its own; it runs inside
`code`, and `build_done` stays `code`'s.

## Guardrails
- **The ladder runs after §1, never instead of it.** A short answer chosen before the callers were read is a
  guess that happens to be short.
- **The project's policies outrank rung 4.** A dependency policy (cooldown on new versions, preferred or
  forbidden packages) decides before "it is already installed" does.
- **No reviewing of other people's code here.** Spotting a defect on the way is reported, not fixed in this
  change (`skills/code-baseline` §0).
- A convention block for the stack (`WORKFLOW.md` §2, step 6) overrides a rung when it says how this stack
  does the thing; the ladder says where to look first, not how the stack writes it.

Cross-links: after the fact, `over-engineering-review`; whether it was reused or created is decided at the
design step by `archi`; the comment rule is `code`'s ("no comments in the code").

## Origin
Rewritten from the `ponytail` skill (MIT) of a public repository, read 2026-10-19; sources, what was dropped
and what was not verified are in [`origin.md`](./references/origin.md). Status 🟡: written, never dogfooded.
