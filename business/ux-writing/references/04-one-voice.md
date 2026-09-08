# § 4 — One product, one voice

> Section 4 of `business/ux-writing`. Read it when a string is being written in a product that already
> has strings. Point 1 is cited from `business/release-communication` §2.

1. **One form of address, applied everywhere** — every message, error, label and confirmation. Which one is a
   product decision, and in several languages it is a grammatical fork with no neutral option; mixing them
   inside one product is what reads as unfinished. The mechanism is that the choice is not confined to
   pronouns: it propagates into every verb form, so a single string written the other way is visibly
   foreign to the rest of the screen and cannot be fixed by changing one word.
2. **One word per action, across the whole product.** If deleting an item is "Delete", it is never "Remove" or
   "Clear" three screens later. Two words for one action make a user wonder whether they do the same thing,
   and they make consistent translation impossible.
3. This is also why the wording lives in one place rather than wherever it was first typed
   (`vue-nuxt-vuetify-conventions` section 6, `laravel-conventions` section 5).
4. **The choice has to be written down to be applied.** Form of address, the verb list, capitalisation
   and the terms for the product's own objects are a decision a reader cannot infer reliably from the
   existing strings — those already contain the drift. A short written reference is what makes the rule
   checkable in a review instead of a matter of whose screens you read last.
5. **The existing product is the reference, not your preference.** A new string that is better written
   than its neighbours and phrased differently makes the screen inconsistent, which costs more than the
   improvement gains. Where the house wording is genuinely wrong, changing it is its own change across
   every occurrence — not a silent divergence starting with this diff.
6. **The voice extends past the interface.** Transactional emails, notifications, exported file headers
   and the text in a generated document are all read as the same product, and they are the strings
   written furthest from any review. A confirmation email using different words from the button that
   triggered it is the most common place the voice breaks.
7. **Two words for one concept split every search.** Not only the reader's search: the codebase's, the
   translation memory's, and the support team's when they look for who else reported this. The cost is
   paid repeatedly and by people who never see the interface (§5.1, `skills/domain-modeling` §1).
8. **The same string in two places is one string.** Copying wording rather than reusing the key is what
   guarantees the two drift, and the drift is discovered by a reader noticing that one screen says
   something slightly different — at which point nobody knows which of the two was intended.
9. **Consistency is not uniformity of length.** A destructive confirmation is allowed to be longer than
   a label, and an error is allowed to be a full sentence where a button is two words. What has to be
   consistent is the vocabulary and the register, not the shape of every string — and forcing brevity
   onto a message that needs a consequence stated is how "Are you sure?" comes back (§2.2).
10. **Never let one screen's translation state differ from the rest.** A screen where half the strings
    are translated and half fall back to the source language reads as broken, and the fallback is
    silent: the missing key renders as its source text, which looks like a deliberate choice to whoever
    is not reading the file (`vue-nuxt-vuetify-conventions` §6).
11. **This block does not own tone of voice or brand vocabulary.** Where a brand reference or an org
    design catalogue's UX-writing skill exists, it is the authority and this section defers to it; what
    remains here is the requirement that whatever it decides is applied to the strings that reach a diff
    without passing through a mockup. Applying that override is silent — write what the governing rule
    requires and move on.
