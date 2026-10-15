---
name: receiving-review-pitfalls
description: "Use when you are the author of a change and review feedback arrives, before any suggestion is applied: reading all the feedback first, restating or asking about unclear items before touching any item, checking each suggestion against the code (stack, existing behaviour, why the code is as it is, the reviewer's context), looking for real usage before building a feature the reviewer calls proper, the order to apply fixes in, pushing back with evidence, correcting a wrong pushback, and replying inside the comment thread."
---

# receiving-review-pitfalls

Step 8 of the pipeline (`WORKFLOW.md`), seen from the author's side: `review` produces the findings and this block
covers what happens when they come back. The two sections share one premise: **a review comment is a claim about
your code, not an instruction, and applying it without checking is how a wrong suggestion reaches the main line**.
The shape of a good comment and the reviewer's side are in `code-review-reviewer-pitfalls`; the host-level rule
that every comment gets a fix or a stated reason is in `mr-conventions`; this block is the mechanism between the
two.

Role boundary: this block is for the **author**. A reviewer working in review-only mode never edits the code under
review; that rule is about the reviewer and does not apply here, where editing the code is the point.

## When
- Review comments, inline or general, have arrived on your change and none has been applied yet.
- A comment is unclear, looks technically wrong, or asks for more than the change needs.
- You pushed back on a point and the reviewer answered.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Reading, restating, unclear items, verifying a suggestion, the usage check | feedback has arrived and nothing is applied yet | [`01-before-implementing.md`](./references/01-before-implementing.md) |
| 2 | Order of fixes, testing each, pushing back, correcting a pushback, replying in the thread | you are about to apply, refuse or answer a comment | [`02-implementing-and-replying.md`](./references/02-implementing-and-replying.md) |

## Output / checkpoint
Every comment ends in exactly one recorded outcome: applied with its own test run (§2.2), pushed back with a
pointer to code or a test (§2.3), or answered with a question (§1.2, §1.4). No item of an unclear batch was
implemented before the unclear items were answered (§1.2). Replies sit in the comment's own thread (§2).

## Guardrails
- Never implement part of a batch while another item of it is unclear (§1.2).
- Never apply a suggestion that changes behaviour before the checks of §1.3 are done against the code.
- Never harden or complete a feature before looking for its real usage (§1.5).
- Never answer a comment with agreement you have not checked; state what changed and where (§2.4).
- Never pad a correction of your own wrong pushback (§2.4).
- This block states what one skill file describes, at the commit in [`references/origin.md`](./references/origin.md).
  Nothing was run while writing it.

## Origin
Rewritten from the `receiving-code-review` skill of the obra/superpowers repository (MIT), read 2026-10-16. The
source's agent-directive tone (forbidden phrases, a rule against any thanks, a human-partner persona) is not carried;
only the mechanisms are. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
