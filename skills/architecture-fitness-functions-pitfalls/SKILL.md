---
name: architecture-fitness-functions-pitfalls
description: "Use when an architecture decision (layers, module boundaries, allowed dependencies, naming, no cycles) has to be enforced by an automated check instead of a document or a review habit, or when an existing architecture check is trusted: what is worth turning into a rule, rules that select nothing and pass, a rule never seen failing, adopting a rule on a codebase with hundreds of violations, an ignore list that only grows, a rule scoped to the wrong classes or paths, and keeping the checks owned and current. Java's ArchUnit is the worked example; the method is language-independent."
---

# architecture-fitness-functions-pitfalls

An architecture decision that nothing checks decays: a layer is bypassed in a hurry, a cycle appears, a module
reaches into another's internals, and the decision record still reads as if it held. An automated check that
fails the build when the decision is broken is called a fitness function in the evolutionary-architecture
literature. The three sections share one premise: **a rule is only as good as the set of code it actually
selects and the number of exceptions it quietly tolerates**, so most pitfalls are about what the checker sees,
what it waives, and who keeps it current.

The block owns no checker and names none as required. ArchUnit (Java) is the worked example because its
documentation was read; the same questions apply to a dependency-rule tool in any language. For the PHP tools
and their pitfalls see `skills/php-architecture-test-pitfalls`. Where the layers should sit is a design
question in `skills/no-catch-all-layer` and `skills/archi`; the record of the decision is in
`skills/documentation-adr`; `skills/safe-refactor` covers moving code once a rule says it is misplaced.

## When
- A decision record says "X must not depend on Y" and nothing fails when it does.
- An architecture rule is about to be added, or one is trusted without having been seen to fail.
- A rule is introduced on a mature codebase that already violates it widely.
- An ignore list, baseline or exclusion for a rule keeps growing.
- A new module or package is added and no rule mentions it.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Which decisions deserve a rule, the kinds of check, writing one that says what it means | a rule is designed or written | [`01-choosing-and-writing-rules.md`](./references/01-choosing-and-writing-rules.md) |
| 2 | Introducing a rule on code that already breaks it: freezing, ignore lists, ratcheting down | the first run reports a pile of violations | [`02-adopting-on-grown-code.md`](./references/02-adopting-on-grown-code.md) |
| 3 | Keeping the checks honest: empty selection, the rule seen failing, scope, CI settings, ownership, metrics | a rule passes suspiciously or the suite is reviewed | [`03-keeping-rules-honest.md`](./references/03-keeping-rules-honest.md) |

## Output / checkpoint
For each rule added or changed: the decision it enforces, with a link to its record; the set of code it selects,
printed or counted and not empty; a deliberate violation introduced in a scratch change on which the rule failed;
and, where the rule was adopted on existing violations, the stored list of known violations under version control
with an owner. A rule never seen failing is not verified.

## Guardrails
- Tie each rule to a decision with a reason. Never add a rule nobody can explain; it will be waived at the first
  deadline (§1.1).
- Make the failure message say what to do. Never ship a rule whose failure reads as an opaque path list (§1.5).
- Prove each rule can fail and selects something. Never trust a green run from a rule that was never red
  (§3.1, §3.2).
- Let a list of known violations shrink only. Never add an entry to make a new change pass; fix the dependency
  or change the decision (§2.3, §2.8).
- Keep the stored violations and the ignore patterns in version control with a named owner and a reason per
  entry. Never leave a blanket pattern that waives a whole package (§2.6).
- Give the CI build a different permission from the developer's machine: it may read the stored violations but
  never create or silently refreeze them (§3.4).
- This block states the documentation read at the date in [`references/origin.md`](./references/origin.md).
  Nothing was run while writing it, and the tool's version was not matched to a project's.

## Origin
Rewritten from the user guide of the ArchUnit project (Apache-2.0), read 2026-10-20, plus own guidance flagged in
the references. Provenance, what was removed and not verified: [`references/origin.md`](./references/origin.md).
🟡: never dogfooded.
