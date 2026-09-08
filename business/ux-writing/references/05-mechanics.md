# § 5 — Mechanics that keep it consistent

> Section 5 of `business/ux-writing`. Read it when a string is added to a translation file, or when a
> message is being assembled from parts.

1. **One term per concept, everywhere.** If it's a "customer" in one screen and a "client" in the next,
   users assume they're different things. Pick one and use it in the code too
   (`skills/domain-modeling` §1). The code half is not decoration: a term that differs between the
   interface and the schema means every conversation between support and a developer needs a
   translation step, and that step is where a bug report gets attached to the wrong entity.
2. **Sentence case, no shouting, no exclamation marks** in system messages. Capitalised words read as
   emphasis the message did not intend, and an exclamation mark on a failure path reads as the product
   being pleased about it. Title case also does not survive translation — most languages do not
   capitalise that way, so the convention silently applies to one language only.
3. **Translation keys are for a translator**, so keep the source sentence readable and never build a
   sentence by concatenating fragments: word order differs between languages and the result is
   unreadable in half of them. The fragment a translator receives has no context either, so the same
   word gets one translation for a noun and a verb sense and is wrong in one of the two places it is
   used.
4. **Numbers, dates and currency are localised**, not formatted by hand. A hand-formatted date is
   ambiguous between the readers who parse it two different ways, and it is wrong rather than merely
   unfamiliar for anyone whose convention it does not match — which includes the reader deciding whether
   a deadline has passed.
5. **Text a screen reader will announce** has its own requirements — see `skills/accessibility`.
6. **A plural is not a conditional.** Choosing between two strings on a count is correct in a couple of
   languages and wrong in most: several have more than two forms, and at least one has none. Use the
   platform's plural mechanism, which is the only thing that can carry those rules — and pass the count
   through it rather than around it.
7. **A key names the string's role, not its text.** A key derived from the sentence has to be renamed
   the first time the wording changes, so it either gets renamed everywhere or stops matching what it
   holds; a key naming where and what it is for survives every rewording. This is the difference between
   a translation file that can be reviewed and one that has to be re-read.
8. **Never put markup in a translated string.** A translator handling tags will move, drop or break
   them, and a string rendered as HTML to make a link work is a rendering path that will eventually
   carry something a user typed (`skills/security-hardening`). Interpolate the component, not the
   sentence.
9. **A string interpolating a value has to say what the value is.** A placeholder with no name in the
   key or the comment reaches a translator as an unknown, and the sentence gets built around a guess —
   commonly a number where a name goes. Naming it is the cheapest fix available at authoring time.
10. **Length is part of the string's contract.** Translations run visibly longer than several common
    source languages, so a string authored to fit exactly is a string that will be truncated somewhere;
    where a hard limit genuinely exists, it belongs in the key's comment so the translator can meet it
    instead of discovering it in a screenshot.
11. **A user-visible string in the code is a string nobody will find.** Hardcoded text bypasses the
    translation file, the review that reads it and the search that finds every occurrence, and it
    surfaces as one untranslated sentence on an otherwise translated screen. This is the single most
    common way §4's consistency breaks after it was established.
12. **Never ship a placeholder.** "Lorem ipsum", "TODO", "test" and a bare "Error" all reach production
    eventually, because the string that was obviously temporary is the one nobody re-reads — and the
    reader who finds it cannot tell whether the feature behind it works.
