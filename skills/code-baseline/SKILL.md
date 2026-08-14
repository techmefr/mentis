---
name: code-baseline
description: Use when writing or reviewing code in any language, for the rules that hold regardless of stack: comments, size and shape, errors, boundaries, domain types, the tests new code owes, customising a third party. Carries the new-code-only scope stance every rule depends on.
---

# code-baseline

Step 6 of the pipeline (`WORKFLOW.md`), and a reading angle at `review` (8). These are the rules that don't
change with the language, so each per-stack block (`laravel-conventions`, `python-conventions`,
`react-nextjs-conventions`, `vue-nuxt-vuetify-conventions`, `dotnet-conventions`, `go-conventions`,
`java-conventions`, `flutter-conventions`, `nestjs-node-conventions`, `php-patterns`,
`typescript-patterns`) can stop restating them.

**Relation to an org skill catalogue.** Where a company ships its own cross-language rule set, it is the
authority on the numbers (its file-size ceiling, its coverage floor) and overrides this block. The thresholds
below are stated as defaults with the reason attached, so a project can move one deliberately rather than by
drift.

**Applying an override is silent.** Write the code the governing rule actually requires and move on — never
report "a conflict between mentis and the house catalogue" to whoever's watching. That framing reads as
broken to a non-technical stakeholder even when the case is a normal, resolved one, and has already caused a
real project to get abandoned and restarted over nothing. Surface it as a specific, named question only when
no rule anywhere actually resolves the case — never as a general alarm.

## §0 The scope stance: read this before applying anything below
Every rule here governs **new and modified** code, and that limit is part of the rule, not a softening of it.
It is stated once, here, because all eleven depend on it:

1. **Never refactor existing code to satisfy one of these rules unprompted.** A 400-line controller, a
   12-method `*Service`, a file full of comments, a generic `throw` — they stay. A drive-by cleanup during an
   unrelated task is expensive to review, risks behaviour nobody asked to change, and is scope the requester
   didn't grant.
2. **But never *extend* the violation either.** Asked to add a behaviour whose obvious home is a god class,
   the answer is a new well-named class, not a thirteenth method. A new `throw` in a file full of generic ones
   still gets a named exception class. "Consistency with the surrounding mess" is how a codebase never
   improves.
3. **Bundled cleanup is fine, drive-by cleanup is not.** If you're editing the lines *around* a forbidden
   comment or a ticket reference, remove it in that same edit. If you're not touching those lines, leave it.
4. **Flag what you left, once, in the closing message** — the file that's now over the ceiling and where its
   seam is, the stale comment that contradicts the code, the missing coverage tooling. A finding stated is a
   decision handed to the human; a finding silently fixed is a decision taken from them.
5. **An explicit instruction overrides any rule here, without argument.** "Just put it in the service for
   now", "skip the coverage check", "throw a plain exception here, I know" — do it, and don't re-litigate.
   These are defaults for when nobody has decided, not a policy to enforce against the person asking.

## When
On every code edit, in any language. Checked at `gate` (7) and `review` (8).

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; loading all of them for a change that only renames a variable is waste, and a section
read is a section that has to be applied. If you are reviewing a whole diff, pick the rows whose
trigger the diff meets, not the whole table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Comments | a comment is about to be written | [`01-comments.md`](./references/01-comments.md) |
| 2 | Size and shape | a file or a class grows, or a name gets vague | [`02-size-shape.md`](./references/02-size-shape.md) |
| 3 | Errors | an exception is thrown or caught | [`03-errors.md`](./references/03-errors.md) |
| 4 | Boundaries | an external API, a file format or a third-party payload is consumed | [`04-boundaries.md`](./references/04-boundaries.md) |
| 5 | Domain types | two distinct concepts share a primitive type | [`05-domain-types.md`](./references/05-domain-types.md) |
| 6 | Tests owed by new code | new behaviour is added | [`06-tests-owed-new.md`](./references/06-tests-owed-new.md) |
| 7 | Customising a third party | a vendor file, template or component needs changing | [`07-customising-third-party.md`](./references/07-customising-third-party.md) |

## Output / checkpoint
No separate checkpoint: this is the floor `gate` (7) and `review` (8) check on every diff. A finding here is
not a nit — each rule exists because its violation was expensive. What it owes at review: no new comment or
ticket key, no new bag-named class, no new generic throw, no new raw external call, no new raw parsed map
escaping its reader, and the diff's own lines covered by tests that were actually run.

## Guardrails
- **§0 is not optional.** Applying any rule below it to legacy code, unprompted, is the failure mode of this
  block — it turns a discipline into an unrequested refactor.
- **Never mis-classify a file to dodge the ceiling**, and never split one purely to satisfy the count.
- **Never weaken, skip or silence a test to turn the bar green**, and never edit the project's coverage
  threshold as a side effect.
- **Never rewrite git history** to remove an attribution trailer.
- Where an org rule set is installed and its numbers differ, **its numbers win**.

## Origin
Rules mined from market catalogues, linters and internal review feedback, rewritten in the house
voice; the full provenance, the source stamps and the refresh log are in
[`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still
current, not when applying one.
