# code-review-reviewer-pitfalls §3 — Speed and size

Review quality depends on two things the comment text cannot fix: how long an author waits, and how much there is to
read. The numbers below are the source's examples for one large organisation; choose your own and write them down.

## 3.1 Why reviews should be fast
1. **Optimise for the speed of the team, not of the individual.** Slow reviews delay everyone else's features and fixes
   by days or weeks as changes wait for review and re-review.
2. **Authors start to protest the process.** Requesting the same substantial changes, but answering quickly each time the
   author updates, makes the complaints about strictness tend to disappear. The source says most complaints about the
   review process are resolved by making it faster.
3. **Code health suffers.** Slow reviews raise the pressure to let weaker changes through and discourage cleanups and
   refactoring.

## 3.2 How fast
1. **If you are not in the middle of a focused task, review shortly after the request arrives.**
2. **The source's example maximum is one business day to respond**, meaning first thing the next morning. Treat it as an
   example service level, not a universal rule.
3. **Following it means a typical change gets several rounds of review in a day.**
4. **Time zones:** answer while the author still has time to reply before the end of their day, or finish before they
   start the next one.

## 3.3 Do not break your own focus
1. **If you are in the middle of a focused task such as writing code, do not interrupt yourself to review.** The source
   cites research that returning to flow takes a long time, so interrupting costs the team more than a short wait does.
2. **Wait for a break point**: the end of the task, after lunch, back from a meeting.

## 3.4 Fast responses over a fast process
1. **The response time matters more than the time to finish the whole review.** Quick replies throughout ease the
   frustration of a long process.
2. **If you are too busy for a full review, send a quick reply**: say when you will get to it, suggest other reviewers
   who could answer sooner, or send some initial broad comments. Send it at a break point, not by interrupting a task.
3. **An approval must mean the change meets the standard** (§1.1), so spend enough time to be certain, while keeping
   each individual response quick.

## 3.5 Approve with comments
1. **Approve while leaving unresolved comments when at least one of these holds:** you are confident the author will
   address the remaining comments properly, the comments do not have to be addressed, or the suggestions are minor
   (sort imports, fix a nearby typo, apply a suggested fix, remove an unused dependency).
2. **Say which of the three you mean** when it is not obvious.
3. **It is especially worth considering across time zones**, where the author would otherwise wait a day for the
   approval.
4. **When you reviewed only part of a change**, say which part, and prefer this form (§1.5).

## 3.6 When the change is too large to review
1. **Ask the author to split it** into smaller changes that build on each other, rather than one huge change reviewed
   all at once. The source says this is usually possible, even if it costs the author more work.
2. **If it cannot be split and you have no time to review it quickly, at least send comments on the overall design**
   so the author can act. One goal of a reviewer is to unblock the author without sacrificing code health.
3. **Do not trade the standard for imagined speed.** The process gets faster over time as authors learn what healthy
   code requires; compromising quality for velocity does not speed anything up in the long run.

## 3.7 What a small change is
These points are written for the author; a reviewer needs them to know what to ask for.
1. **Why small:** reviewed faster and more thoroughly (large changes drown important points in detailed commentary),
   less likely to introduce bugs, less work wasted if the direction is rejected, easier to merge, easier to design well,
   less blocking on reviews, simpler to roll back.
2. **A reviewer may reject a change for size alone.** The source says this explicitly.
3. **The right size is one self-contained change:** it addresses just one thing, usually one part of a feature, includes
   its related tests, and is understandable from the change, its description, the existing code and changes already
   reviewed.
4. **The system keeps working after it lands.** It is also not so small that its implications are hard to see: a new API
   comes with a usage of it in the same change, which also prevents unused APIs.
5. **There is no hard line.** The source's example is that about one hundred lines is usually reasonable and one thousand
   usually too large, and the number of files counts too: two hundred lines in one file may be fine, spread over fifty it
   is usually too large. The reviewer's judgement decides.
6. **When in doubt, go smaller.** Authors know their code intimately; the reviewer does not, and rarely complains about
   changes that are too small.
7. **Large is acceptable** for deleting a whole file, which counts as about one line, and for the output of an automatic
   refactoring tool you trust completely, where the reviewer only confirms they want the change.
8. **Refactoring goes in its own change**, apart from a feature or fix: moving and renaming a class is separate from fixing
   a bug in it. Small cleanups such as a local variable name can ride along.
9. **Tests ride with the code they test.** Independent test work may land first: new tests for existing code, refactoring
   the test code, introducing larger test framework code.
10. **When several dependent changes land, none may break the build in between.**
11. **If a change truly cannot be made small, get the reviewers' agreement before writing it**, expect a long review, and be
    extra careful with tests.

## 3.8 Splitting, and what is not carried
1. **Ways to split:** by groups of files that need different reviewers, by layer, by vertical feature, or a grid of both,
   so that each piece is a standalone change.
2. **Decision, not carried: stacking changes on top of each other.** The source lists writing a second change on top of
   the first before the first is reviewed. This repository's practice is that each change goes to the main line on its
   own; our reasoning is that a rejected base then does not invalidate the rest. Use the other split strategies and
   sequence the changes instead.
