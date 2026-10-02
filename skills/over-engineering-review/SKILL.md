---
name: over-engineering-review
description: "Use when re-reading a diff or a repo looking for one thing only, what can be deleted: dead code, reinvented stdlib, over-abstraction, unrequested anticipation. Measures first, forces a ranking, makes every candidate defend its right to stay. Scores and lists, never applies."
---

# over-engineering-review

Step `simplify` (9) of the pipeline (`WORKFLOW.md`), or a one-off mode on a diff before merge.
A single question asked of every line in scope: **can this disappear without breaking
anything?** No correctness judgement (that's the diff reviewer), no convention judgement (the
`*-conventions` blocks): only the hunt for what should never have been written.

## When
- Alongside the diff reviewer/`gandalf` on an MR, when a diff looks bigger than the need
  justifies.
- As a one-off audit of a whole repo (not just a diff) when over-engineering debt is suspected.
- As raw material for the native `simplify` skill, which then applies the deletions retained:
  this block fixes nothing itself, it lists and scores.

## Steps

### Diff mode (a change in progress)
Go through only the added/modified lines of the diff. For each candidate found, one finding line
with a tag:

- `to-delete:`, dead code, never called, or duplicated from an existing helper already present
  in the repo (see also [[reuse-existing-components-before-creating]]). Three shapes that are easy to
  walk past: a constructor dependency the class never reads, a condition re-tested inside itself or
  twice in one chain, and the same guard written twice in one method with nothing reassigned between.
- `stdlib:`, a function/utility reinvented when the language, the framework or an
  already-installed lib does it natively.
- `over-abstraction:`, an interface, wrapper or delegation layer with only one real caller: the
  abstraction is useless until a second use case exists.
- `yagni:`, a feature, option or parameter anticipated for a need nobody asked for today (flag,
  pre-emptive chunking, cache, unused config).
- `to-shrink:`, the same behaviour reachable with appreciably less code (dead branches, cases
  never reached, pointless indirection).

Finding format: `<tag> file:line, what, in one sentence`. No paragraph, no expanded
justification (see [[short-review-checklist-items]]), the dev fixes it or asks.

### Audit mode (whole repo): measure, rank, defend
An audit run on adjectives produces forty speculative findings. Run it in three passes, in this order.

1. **Count first, judge nothing yet.** Record a raw number for each signal that applies, and let no
   finding appear that is not traceable to one of them:
   - an abstraction (interface, abstract class, contract type) with exactly one implementer;
   - a function whose whole body is one call to another, adding no logic;
   - indirection depth: files crossed from the entry point of each main flow to the code that does real work;
   - an export nobody imports outside its own file;
   - an option, config key, flag or enum member that nothing reads;
   - two units doing the same job (formatting, money, fetch wrappers);
   - a dependency with fewer than three import sites;
   - a generic parameter, strategy or factory with a single registered member;
   - defensive noise: a catch that hides the failure behind a default value, a null check the type already
     excludes, the same validation at three layers.
2. **Rank, both ends.** Order the files by structural lines (types, wrappers, re-exports,
   boilerplate) against logic lines and report the top five and the bottom five, plus the depth of each
   main flow. A ranking that shows only the bad end ranked nothing, and the bottom five are the model to
   cite when a fix is proposed.
3. **Make each candidate defend itself.** Take the ten worst. Each gets five fields or is dropped:
   where, the measured number that flagged it, the concrete task it makes harder, **the strongest honest
   case for keeping it** (a requirement that still exists, a genuinely volatile boundary, a test suite or
   external contract that leans on it), and a verdict `REMOVE`, `SIMPLIFY` or `KEEP`. Expect roughly a
   third to end as `KEEP`: none means the defence was a formality, nearly all means the candidates were weak
   and the next ten should be taken.

The correction has to cost less than the defect it removes. When taking an abstraction out is dearer than
putting up with it, the verdict is `KEEP` and there is no finding. Style, naming and "I would have written it differently" are out of scope.

## Output / checkpoint
A list of tagged findings, ending with an overall score:
- `net: -N lines possible` if concrete deletions are found, N = a low estimate of lines that can
  be deleted without breaking anything.
- `already lean, nothing to report` if the scope holds no candidate: an audit that finds nothing
  is a valid result, not a failure of the review. Say a category is clean rather than padding it.

Audit mode adds the count table, the two-ended ranking, the `REMOVE`/`SIMPLIFY` entries, the `KEEP`
entries with their reason, and the single change that removes the most complexity for the least risk.
It also states what could not be checked (dynamic dispatch, reflection, anything only visible in production).

## Guardrails
Never fix anything yourself: this block lists, `simplify` (native skill) or the dev applies.
Don't confuse it with a correctness review: a potential bug spotted along the way is reported
separately (to the diff reviewer/gandalf), not mixed into this list. An `over-abstraction`
candidate requires checking that there really is only one caller (grep before deciding), no
deletion on an assumption. A reviewer asked to find problems feels pressure to produce them: an invented
finding is itself the fault this block hunts.

## Origin
Idea taken from a market deletion-oriented review tool (`ponytail-review`/`ponytail-audit`
skills, deletion angle only, per-category tags, net line score): mechanism and tags rewritten in
the vocabulary of the mentis blocks, no copied text.

Audit mode (count first, two-ended ranking, mandatory defence with a `KEEP` expected for about a third,
fix smaller than the problem) rewritten from the `find-overengineering` skill of
`abdian/claude-toolkit-laravel` (MIT), read 2026-10-02. The three `to-delete` shapes (unread constructor
dependency, redundant condition, doubled guard) come from the rule list of `Heyosseus/sloppy` (MIT),
same date. No text copied.
