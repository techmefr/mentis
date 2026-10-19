# code-review-reviewer-pitfalls §4 — Pushback, "later" and the tests

Three situations come up in nearly every review: the author disagrees, the author promises to fix it afterwards, and
the change carries tests that nobody checks because they are tests.

## 4.1 When the author pushes back
1. **First consider whether the author is right.** They are often closer to the code. Does the argument make sense, and
   does it make sense for code health? If so, say they are right and let the point drop.
2. **If they are not right, explain further.** A good explanation shows you understood their reply and adds information
   about why the change is requested.
3. **Keep advocating when the change improves code health** and the improvement justifies the extra work. The source
   says improving code health tends to happen in small steps, and that it can take a few rounds before a point sinks in.
4. **Stay polite and say that you hear them and simply do not agree.**
5. **A disagreement that stays stuck follows §1.4.**

## 4.2 Upsetting the author
1. **Reviewers often fear the author will be upset by insistence.** The source says that, when it happens, it is usually
   brief, and that with polite comments the upset is usually only in the reviewer's mind.
2. **Upset comes more from how a comment is written than from the insistence on quality** (§2.2).

## 4.3 "I will clean it up later"
1. **Experience in the source: the later cleanup usually does not happen.** The more time passes after the change, the less
   likely it becomes, not through irresponsibility but because other work crowds it out. Some authors do write the follow-up
   immediately.
2. **Usually insist on the cleanup now**, before the code is in the codebase and "done". The source calls "later" a common
   way for codebases to degenerate.
3. **A change that introduces new complexity must be cleaned up before it lands**, except in a declared emergency.
4. **If the change exposes surrounding problems that cannot be fixed now,** the author files the follow-up and assigns it to
   themselves so it is not lost. Decision for this repository: there is no tracker and comments stay out of code, so the
   follow-up is written in the change description with an owner and a date, and the source's optional TODO comment
   in the code is not carried.

## 4.4 Complaints about strictness
1. **When you move from lax to strict reviews, some authors complain loudly.** Faster reviews (§3.1) usually make the
   complaints fade.
2. **It can take months.** The source reports that authors come to see the value as they see the quality of the resulting
   code, and that the loudest protesters can become supporters.

## 4.5 Review the tests as code
1. **Ask for the tests the change needs** (unit, integration or end-to-end as appropriate), in the same change as the
   production code, except in an emergency.
2. **Check that the tests are correct, sensible and useful.** Tests do not test themselves and are rarely tested, so a human
   has to confirm they are valid.
3. **Ask four things of each test:** will it fail when the code is broken; if the code changes beneath it, will it start
   giving false positives; does each test make simple and useful assertions; are the tests separated across different
   test methods.
4. **Do not accept complexity in tests** because they are not part of the shipped program; they are code to maintain.
5. **Ask which inputs and edge cases are untested**, and whether the change is testable at all (the checklist's two
   questions on testing).
6. **The rules for what makes a test worthless** (doubles that test themselves, timing guesses) are in
   `testing-anti-patterns` §1 and §3; reviewing the test is where you apply them.
