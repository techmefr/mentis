# design-contract-and-finish-gate-pitfalls §1 — The design contract

Source: the design-ui-finish-gate-reviewer agent of msitarzewski/agency-agents (MIT), read 2026-10-21.

## 1.1 The product lens comes first
1. **Symptom:** a critique that talks about pixels before it knows who uses the screen. **Fix:** write a short
   lens first: who uses this screen and what are they trying to finish, which object, status or decision must be
   understood first, what repeats daily and what is rare but costly, and which framework, component library,
   brand system and responsive constraints already exist.
2. **When the lens is unknown, label each assumption and ask.** Do not invent a redesign on a guess about the
   product.

## 1.2 Comparable evidence, a few cases
1. Collect a few screens or patterns from adjacent products, each as: the pattern, the job it serves, the lesson
   that transfers. **Symptom:** a single reference becomes a template. **Fix:** several, so the lesson is the
   overlap and not one product's styling.
2. A catalogue or gallery is research material, never a substitute for judgement and never a required service
   to finish the review.
3. A trend, a popular composition or a library default is not evidence that a layout is right.

## 1.3 Take a pattern, not a picture
1. Explain why a pattern fits this product's job, audience and constraints. Without that sentence the lesson is
   decoration copied from somewhere else.
2. Existing brand and technical constraints stay unless a named, concrete problem requires changing them.

## 1.4 The contract, one per screen
Write these lines before proposing any implementation change:
1. **User and job:** who completes what.
2. **First-read object:** the thing the eye must find first.
3. **Primary action:** one observable action.
4. **Density decision:** compact, balanced or spacious, and why.
5. **Hierarchy:** headline, key signal, controls, supporting information, in that order of weight.
6. **Interaction model:** table, canvas, editor, timeline, feed, form, or what it actually is.
7. **Responsive priority:** what stays fixed, what collapses, what moves, at the narrowest supported size.
8. **References:** pattern and lesson pairs, not copied visuals.
9. **Forbidden defaults:** the specific patterns that would make this screen generic, such as a hero where the
   work is a table, equal-weight metric cards, decorative gradients or glass, oversized rounded cards,
   animation added to feel designed, or encouraging filler copy where the product needs one decision.
10. **Finish evidence:** the screenshots, states and viewport checks that will prove the result.

## 1.5 Separate a product constraint from a taste
1. **Symptom:** a finding that is really the reviewer's preference. **Check:** can the finding be tied to the
   lens (the user's job, the first-read object, a stated constraint)? **Fix:** if not, drop it or file it as an
   optional refinement, not a blocker.

## Checks
1. The lens and the ten contract lines exist before any visual critique.
2. Evidence names a pattern and a transferable lesson, not a brand to imitate.
3. Forbidden defaults are specific to this product.
