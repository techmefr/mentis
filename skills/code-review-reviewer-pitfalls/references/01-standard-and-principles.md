# code-review-reviewer-pitfalls §1 — The standard and its principles

A reviewer who holds out for perfect makes every change expensive, and a reviewer who approves anything lets the
code decay one small step at a time. The source's answer is one rule and a short list of principles for settling
what outranks what.

## 1.1 The bar: overall code health improves
1. **Approve once the change definitely improves the overall code health of the system, even if it is not perfect.**
   The source calls this the senior principle among its guidelines.
2. **Why both sides matter.** If nothing is ever approved, the code never improves and authors stop trying; if every
   change is approved, code health drops through many small decreases, which happens most under time pressure.
3. **There is no perfect code, only better code.** Do not ask the author to polish every small piece; weigh the need
   to move forward against the importance of each suggestion. A change that improves maintainability, readability and
   understandability as a whole should not wait days or weeks for perfection.
4. **A change the reviewer does not want in the system can still be refused** even when well designed; the standard
   is about quality, not a duty to accept features.

## 1.2 Never approve a change that worsens code health
1. **Nothing in the standard justifies a change that definitely worsens overall code health.** The source names
   an emergency as the only exception and defers to a separate page for what counts as one; that page was not read
   for this block.
2. **Code decays by small steps.** Most systems become complex through many small changes, so even small added
   complexity is worth stopping (the source's context section).

## 1.3 What outranks what
1. **Technical facts and data outrank opinions and personal preferences.**
2. **Style follows the project's style guide.** A purely stylistic point that the guide does not state is personal
   preference: follow the style already there, and accept the author's where nothing exists.
3. **Design is almost never a pure style or preference matter.** Weigh it by underlying principles. If the author shows,
   by data or sound engineering principles, that several approaches are equally valid, accept the author's; otherwise
   the standard principles of design decide.
4. **If no other rule applies, you may ask for consistency with the current codebase**, as long as that does not
   worsen code health.
5. **Never block on a preference the guide does not state.** Raise it as an optional point (§2.1).

## 1.4 Resolving a disagreement
1. **First try to reach consensus** from the standard and the project's own guidance.
2. **When that is hard, talk instead of trading comments**, by call or in person; record the result as a comment on
   the change for later readers.
3. **If that fails, escalate**: a wider team discussion, a technical lead, the maintainer of the code, or a manager.
4. **Do not let a change sit because the two of you disagree.**

## 1.5 Context and every line
1. **Look at every line you were asked to review.** You may skim data files, generated code and large data
   structures, but do not skim a human-written function and assume it is fine.
2. **If you cannot understand the code, say so and wait for clarification.** The source's reasoning: other readers
   will not understand it either, so asking helps future readers as well.
3. **If you understand it but are not qualified for a part, make sure a qualified reviewer is on the change**, in
   particular for security, concurrency, accessibility, privacy and internationalisation.
4. **When you review only part of a change**, note in a comment which parts you reviewed and prefer approving with
   comments (§3.5).
5. **Read the change in its context.** The review tool shows a few lines around each edit; sometimes you have to
   open the whole file to see that four new lines landed in a function that now needs splitting.
6. **Review the change in the context of the system.** Is it improving code health or adding complexity and
   reducing test coverage.
