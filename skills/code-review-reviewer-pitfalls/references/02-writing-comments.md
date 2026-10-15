# code-review-reviewer-pitfalls §2 — Writing the comments

A comment has two jobs: say what is wrong, and say how much it matters. Authors who cannot tell a requirement from
a suggestion treat all of them as requirements, or all as noise.

## 2.1 Label the severity
1. **Say which comments block and which do not.** The source suggests labels that separate required changes from
   guidelines and suggestions, and gives three: a nit (minor, technically should be done, will not change much), an
   optional or consider (probably a good idea, not strictly required), and an FYI (not expected in this change, but
   worth thinking about for later).
2. **Why:** the labels make the intent explicit, help the author order the work, and prevent the misreading that every
   comment is mandatory.
3. **A purely educational comment is a nit.** Teaching is part of improving code health, and it is fine to leave such
   comments, but if the point is not needed to meet the standard (§1.1), mark that it is not mandatory.
4. **A style improvement the project's guide does not state is a nit as well**, never grounds to block (§1.3).
5. **Leave nitpicks and "could be better" remarks freely, but label them.** The source says to feel free to comment
   that something could be better, with a prefix when it is not very important.

## 2.2 Comment on the code, and say why
1. **Write about the code, never about the developer.** The source's example turns a question that blames ("why did
   you use threads when there is obviously no benefit") into a statement about the system: the concurrency adds
   complexity without a performance benefit that the reviewer can see, so the code is better single-threaded.
2. **You do not always have to follow this practice, but use it for anything that could be upsetting or contentious.**
3. **Explain why when it helps**: the intent, the practice you follow, or how the suggestion improves code health.
   You need not include it in every comment.
4. **Keep the tone courteous and respectful and the content clear.**

## 2.3 Point at the problem or give the fix
1. **Fixing the change is the author's job, not the reviewer's.** You are not required to design a solution or write the
   code. That also fits the house rule that a reviewer in review-only mode does not edit the code under review.
2. **Pointing out a problem and letting the author decide** often teaches more, makes review easier, and can give a
   better solution because the author is closer to the code.
3. **Sometimes direct instructions, a suggestion or even code help more.** The primary goal of review is the best change
   possible; a secondary goal is to raise the author's skill so they need less review over time. Strike the balance
   case by case.
4. **Encourage simplifying or adding a code comment over explaining the complexity to you** (the source's summary).

## 2.4 When you ask for an explanation
1. **A request for explanation should usually produce clearer code**, not a reply. Occasionally a comment in the code is
   the right result, as long as it does not merely explain code that is too complex.
2. **An explanation written only in the review tool does not help future readers of the code.** It is acceptable in a
   few cases, for example when you review an area you do not know and the author explains something that normal
   readers would already know.
3. **House rule, decision:** this repository keeps comments out of code, so the "add a comment" branch of the source is
   not carried; clearer code, a better name or a test is the result to ask for. The source's reasoning about the review
   tool is carried.

## 2.5 Say what is good
1. **When you see something good, say so, with the reason.** The source's examples: a messy algorithm that was cleaned
   up, exemplary test coverage, or something you learned from the change.
2. **Reasons for it:** people learn from reinforcement as well as correction, and review otherwise tends to focus only
   on mistakes. The source adds that it can be more valuable, for mentoring, to say what someone did right.
3. **Include the why**, as with any comment, so the good practice repeats.
