# § 6 — Gathering references

> Section 6 of `business/interface-design`. Read it when looking for prior art before designing a screen
> — from a story, not from taste.

1. Start from what the story actually says, and extract keywords in separate registers rather than
   searching the story's title: **the screen type or UI pattern**, **the components involved**, **the
   domain and context**, and **the intended tone/ergonomics**. A title searched whole returns products
   with the same feature name and nothing about its shape, because a title names the outcome and the
   registers name the thing you are actually looking for.
2. Search in the language the design community publishes in (English), whatever the project's language.
   Searching in the project's language returns marketing pages for local products; the pattern
   vocabulary — the words that name the container, the state, the component — exists in English, and
   without it the search cannot reach the material that discusses trade-offs.
3. Infer the tone from the domain rather than from taste — an approval workflow in a financial back
   office and a consumer onboarding flow have different correct answers. The back office is used all day
   by people who know it, so density and keyboard reach win; the onboarding flow is used once by someone
   who doesn't, so guidance and generous spacing win. Applying either one's tone to the other is the
   most expensive kind of reference mistake, because it looks deliberate.
4. References inform, they don't decide: a pattern copied from a product with different constraints
   imports those constraints. Say what was borrowed and what was rejected — that sentence is worth an
   ADR line (`skills/documentation-adr` §4) when it's a trade-off someone will revisit.
5. **The constraints a reference imports are usually the ones it does not show.** A product's screen was
   drawn for its data volumes, its permission model, its device mix and its team's tolerance for
   maintenance. A layout that works at ten rows fails at ten thousand, and one that assumes every reader
   sees every column fails the moment a role sees a subset. Neither is visible in the screenshot, which
   is why the borrowed thing has to be checked against this project's own numbers before it is drawn.
6. **A reference is prior art, not evidence.** A widely copied pattern can be widely wrong, and a
   polished screen from a large product may be the output of a constraint you do not have. So "a big
   product does it this way" is not a reason on its own — the reason is the mechanism the pattern
   exploits, stated in a sentence. If that sentence cannot be written, the pattern was chosen by
   appearance.
7. **Write down what was rejected, and why, at the same time as what was taken.** The rejection is the
   part that gets re-litigated: the next person sees the same reference, proposes the same pattern, and
   without the note the discussion starts from zero. One line naming the pattern and the constraint that
   ruled it out is what makes that discussion two sentences long.
8. **Never copy a reference's values.** Its spacing, its type sizes and its component heights belong to
   its own design system and disagree with the local scale by small amounts — the amount that reads as a
   mistake rather than a choice (§1.9). What transfers is the structure and the decision; the numbers
   come from the scale.
9. **A reference gathered after the screen is drawn is a justification, not a reference.** The order is
   part of the rule: prior art read first changes what gets drawn, and prior art read afterwards gets
   filtered for whatever agrees with the drawing. Where a screen already exists and prior art is being
   consulted, the honest use of it is as an audit against the drawing (§0.2), which is a different
   output.
