---
name: testing-blocks
description: Use when a skill or agent in this framework has been written but never proven to change behaviour: validate it with a pressure scenario, run without the block then with it.
---

# testing-blocks

Cross-cutting, meta (`WORKFLOW.md` §2). This block exists because most of this framework was written
and never proven. `CATALOG.md` marks that honestly as 🟡, but a status isn't a test.

It's the `tdd` discipline turned on the framework itself: **a block's output is agent behaviour**, so
the test is behavioural. And it's cheaper than what we were waiting for — you don't need a real
project and a real feature to find out a block doesn't work.

## When
Before a block moves out of 🟡. Also when a block was followed in the calm case and ignored the one
time it mattered: that's not bad luck, that's a failed test nobody ran.

## Steps

### 1. RED: watch it fail without the block
1. **Write a realistic scenario** in the block's domain, with a concrete choice to make: real file
   paths, actual options A/B/C, work the agent believes is genuine rather than a quiz.
2. **Run it with the block absent.** You need to see the wrong behaviour happen.
3. **Record the exact reasoning used to justify it, verbatim.** Not "it skipped the check" but the
   sentence it told itself: "the tests are probably fine", "the user is in a hurry so I'll verify
   after". Those sentences are the specification for what the block has to counter. Paraphrasing
   them loses the thing you're building against.

### 2. Apply pressure, or you've tested nothing
A block that holds in a calm scenario tells you nothing about the moment it's needed. Combine at
least two of these:

- **time**: a deadline, a demo in ten minutes
- **authority**: someone senior already said it's fine
- **consequence**: the fix is blocking someone else
- **sunk cost**: two hours already spent down this path
- **fatigue**: the fourth attempt at the same failure
- **social**: being seen as obstructive for insisting
- **pragmatism**: "this is the exception, obviously"

Combined pressure is the realistic case. The single-stressor version is the academic one, and passing
it is not evidence.

### 3. GREEN: write against the recorded rationalisations
1. Target the sentences from step 1.3 **specifically**. A generic "don't skip verification" doesn't
   engage a reasoning chain; the counter to "the tests are probably fine" is "probably is the word
   that means you haven't looked".
2. Re-run the same scenario with the block present. Success is behavioural: the right option chosen,
   ideally with the block's reasoning cited back.

### 4. REFACTOR: close the loophole it finds next
1. An agent that can no longer take the old shortcut will find a new one. That's the expected result,
   not a failure of the block.
2. Add the specific counter, re-run. **Don't stop at the first compliance**: the first pass usually
   closes the obvious route and leaves the clever one open.
3. Stop when a round of pressure produces no new workaround.

## Output / checkpoint
For each block tested: the scenario, the pressures applied, the verbatim rationalisation from the RED
run, and the behaviour in the GREEN run. That's what promotes a block out of 🟡 in `CATALOG.md` —
and the maturity note says *tested under pressure*, which is a different and weaker claim than *used
on real work*. Both are worth having; don't let one stand in for the other.

## Guardrails
- **A block that passes only an academic test is untested.** Record the pressures applied, so the
  claim can be judged.
- **Don't skip RED.** Writing the block first means writing against imagined failures, and the real
  rationalisations are consistently more specific and more reasonable-sounding than the invented ones.
- **Don't grade your own homework in the same context.** The run that judges compliance shouldn't be
  the one that wrote the block; same reason `galadriel` exists.
- This tests whether a block **changes behaviour**, not whether its content is correct. A confidently
  wrong block can pass this and still be wrong: correctness comes from the source, from review, and
  from real use.

## Origin
Rewrite of `testing-skills-with-subagents` from a market skills repository (the companion repo of the
upstream this framework is a response to). The RED/GREEN/REFACTOR structure, the pressure taxonomy and
the "record the rationalisation verbatim" rule are theirs and are taken as-is because they're better
than what we had, which was nothing.

Found late, and the omission is worth recording: this framework's own sourcing pass had enumerated a
137-agent per-technology catalogue while never listing the contents of the project it takes its
premise from. The distinction between *tested under pressure* and *used on real work* is ours, added
so this block can't be used to quietly retire the dogfooding requirement.
