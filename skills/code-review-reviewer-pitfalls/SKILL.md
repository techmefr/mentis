---
name: code-review-reviewer-pitfalls
description: "Use when you are the reviewer of someone else's change, or you set up how a team reviews: the approval standard (improves overall code health, not perfection), what outranks preference, labelling every comment with a severity, commenting on the code and explaining why, review response time and the approve-with-comments option, change size and splitting, refusing a cleanup promised for later, and reviewing the tests in the change."
---

# code-review-reviewer-pitfalls

Step 8 of the pipeline (`WORKFLOW.md`), on the social side of reviewing. `review` says which axes to check and how to
triage findings before posting; this block covers what the sources describe about the human mechanics: where the
approval bar sits, how a comment tells the author what blocks, why speed and size decide whether reviews work at
all, and how to handle pushback. The four sections share one premise: **a review process fails through its
mechanics, not its rigour: an unlabelled comment is read as blocking, a slow reply breeds shortcuts, an oversized
change gets skimmed**. The author's side of the same exchange is in `receiving-review-pitfalls`. Over-engineering
is covered by `over-engineering-review`, the test rules by `testing-anti-patterns`, and the reply conventions on a
pull or merge request by `mr-conventions`; none is repeated here.

## When
- Reviewing a change, or deciding whether to approve it.
- Writing or rewording a comment that may read as harsher or more mandatory than intended.
- A review has waited for days, a change is too large to review well, or an author says they will fix it later.
- Setting the review norms for a team.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The approval standard, what outranks preference, resolving a disagreement, context and every line | deciding whether to approve or block | [`01-standard-and-principles.md`](./references/01-standard-and-principles.md) |
| 2 | Severity labels, commenting on the code, explaining why, guidance versus fixing, praise, explanations | writing review comments | [`02-writing-comments.md`](./references/02-writing-comments.md) |
| 3 | Response time, focus, approve with comments, large changes, what a small change is, splitting | a review is slow or a change is large | [`03-speed-and-size.md`](./references/03-speed-and-size.md) |
| 4 | Pushback, the cleanup promised for later, strictness complaints, reviewing the tests | the author disagrees, defers, or the change carries tests | [`04-pushback-cleanup-and-tests.md`](./references/04-pushback-cleanup-and-tests.md) |

## Output / checkpoint
Each comment carries a severity or is plainly blocking (§2.1), the decision to approve or block is tied to whether
overall code health improves and says so (§1.1), no approval was given on a change that worsens code health outside
a declared emergency (§1.2), and a deferred cleanup is either done now or recorded with an owner and a date (§4.3).
A review that only says "looks fine" gives the author no reason to trust the next one.

## Guardrails
- Never approve a change that makes the code worse, outside a declared emergency (§1.2).
- Never block on a personal style preference the project's style rules do not state (§1.3, §2.1).
- Never leave a comment unlabelled when it is optional or educational (§2.1).
- Never write the fix for the author as part of the review (§2.3); a reviewer working in review-only mode does not
  edit the code under review.
- Never approve without having understood every line you were asked to review (§1.5).
- Never let a disagreement sit without a next step (§1.4).
- This block states what the sources describe at the commits in [`references/origin.md`](./references/origin.md).
  Every number in it (days, lines) is a source's example for one organisation, not a measurement for your team.
  Nothing was run while writing it.

## Origin
Rewritten from the reviewer documents of Google's engineering practices (the standard, speed, comments, pushback
and what-to-look-for pages) and its guide on small changes, plus one MIT code review checklist for the tests angle,
read 2026-10-16. The Google material is licensed CC BY 3.0 and is adapted here with credit: this block adapts text
from Google's engineering practices documentation (https://github.com/google/eng-practices), licensed under CC BY 3.0
(https://creativecommons.org/licenses/by/3.0/); the changes are rewording, restructuring, replacing Google-internal
terms and relabelling its thresholds as examples, and no endorsement by Google is implied. 🟡: never run by us;
open points are in [`references/origin.md`](./references/origin.md).
