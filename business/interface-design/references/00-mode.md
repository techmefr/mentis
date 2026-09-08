# § 0 — Settle the mode first: producing, or auditing?

> Section 0 of `business/interface-design`. Read it before anything else in this block, every time — the
> same rules read differently depending on which mode you are in.

The same rules read differently depending on which you're doing, and getting this wrong wastes the whole
pass. **If it isn't explicit, ask, and don't start until it's settled.** Production is the usual need.

1. **Producing** — you apply each rule as you build: plan every mandatory state, take every value from
   the scale, choose the container from the tree. The output is the mockup. In this mode a rule is a
   constraint on what you draw, so an unresolved question is yours to resolve, and a value you cannot
   find in the scale is a question for whoever owns the scale rather than a number you pick.
2. **Auditing** — you flag, you don't redesign. The output is a list: the screen or component concerned,
   the rule broken, and what's missing. An audit that silently rewrites the designer's intent isn't an
   audit. It is a second mockup competing with the first, and the designer has no way to see which of
   your changes were rule violations and which were taste, so the usual outcome is that the whole list
   gets discarded along with the taste.
3. **The two modes fail in opposite directions, which is why the mode has to be named out loud.**
   Production done in audit register produces a mockup full of hedges and open questions that nobody can
   build from. Audit done in production register produces a redesign nobody asked for, and it destroys
   the one thing an audit is for: a list the designer can act on point by point without conceding
   anything about intent.
4. **A disagreement about intent is never a finding.** "This should be a different screen" is a product
   question and belongs to `skills/spec` and `business/product-ownership`; "this data-driven list has no
   empty state" is a finding. The test is whether the rule you are citing exists in this block or in one
   it points at. If you cannot name the rule, what you have is a preference, and stating it as a finding
   is how an audit loses its authority for every real finding in the same list.
5. **An audit finding names the element, not the screen.** "The user page is inconsistent" cannot be
   acted on; "the two chips in the header are a filter chip and a status chip at the same height, and
   the status one reads as clickable" can be, because it says what to change. The consequence of the
   vague form is a round trip that costs more than the finding was worth, and a designer who reads the
   next audit expecting the same.
6. **Say what is missing, not only what is wrong.** Most of what an audit of a mockup turns up is
   absence — the state nobody drew, the container choice nobody made explicit, the second primary that
   means the hierarchy was never decided. Absence is invisible in a screenshot, so it is the part that
   reaches step 6 unresolved and gets answered by whoever is implementing at that moment.

**Numeric thresholds are the one thing never answered from memory.** A principle is stable and always
applies; an exact number (a contrast ratio, a minimum target size) is defined by a standard and changes.
Cite it from the standard or flag the point as to be verified — never state a figure you're recalling
(`skills/source-freshness`, and `skills/accessibility` which cites its standard).

7. **A recalled threshold is worse than no threshold at all**, in both modes. In production it gets
   built, shipped and believed, and the screen carries a compliance claim nobody checked. In an audit it
   is the finding that gets the whole list dismissed, because the one number the designer looks up is the
   one you got wrong. The honest output is the point flagged as to be verified against the standard,
   which is actionable; a wrong number is not.
8. **The failure is specific to numbers, and knowing that is what makes the rule usable.** "Contrast has
   to be sufficient for body text" is a principle and holds; the ratio is a figure in a versioned
   document, and so are minimum target sizes, the reflow width and the text-spacing values. Anything of
   that shape is looked up. Everything else in this block is a decision tree or a discipline and does not
   have a number in it — which is deliberate, because a number here would be a value owned by a design
   system this block cannot see.
