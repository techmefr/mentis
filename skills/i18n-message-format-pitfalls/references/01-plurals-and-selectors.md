# i18n-message-format-pitfalls §1 — Plurals and selectors

A plural or a select is where one message becomes several sentences. Most defects here come from writing the
branches for the source language only and discovering the rest in production.

## 1.1 Branches are categories, not numbers
1. **A plural branch names a CLDR category, never a count.** The six categories are `zero`, `one`, `two`,
   `few`, `many` and `other`, and a language uses only some of them: English has `one` and `other`, Czech has
   `one`, `few`, `many` and `other`, Arabic has all six (Lingui plurals guide; Fluent selectors guide;
   next-intl messages page). `one` means "a number that behaves like 1", so it also covers -1 (Lingui).
2. **`other` is the only branch every language has, so it is the only one that must exist.** Lingui says so
   plainly; the formatjs ICU page adds that its parser throws when `plural`, `selectordinal` or
   `select` has no `other`; Fluent requires a default variant, marked with `*`.
3. **Do not write `=1` where you mean the singular, and do not write `one {1 item}`.** In Ukrainian, Russian
   and Serbian, the formatjs lint rule notes, `one` matches numbers that end in 1 but not in 11, such as 21
   and 151, so for 21 a branch holding a literal `1` would print "1 item". Write the count with `#`:
   `one {# item}`. Another formatjs page words the 11 case differently, and the vue-i18n documentation shows
   Russian 21 rendered with the `one` form. Own guidance: do not rely on any list of numbers written in a
   document, look the locale up in the CLDR plural table or call `Intl.PluralRules` for the numbers you care about.
4. **`#` is the count, formatted as a number.** The formatjs page says it behaves like `{count, number}`, and
   next-intl says the same. Inside a branch use `#` and do not repeat `{count}`; the formatjs lint rule
   `prefer-pound-in-plural` gives the reason that the count is then formatted correctly.
5. **An exact match such as `=0` is tried before the categories** (next-intl: "always takes precedence"), which is
   the place for a special zero such as "No followers yet" instead of "0 followers". Own guidance: it is one
   more branch for the translator, in every language, so use it only where the wording really differs.

## 1.2 Who writes which branch
1. **The developer writes the source-language branches and the translator adds the others.** Lingui's example
   is an English `one` and `other` that the Czech translator turns into `one`, `few`, `many` and `other`; no
   code changes per language.

   ```icu
   {count, plural, one {# book} other {# books}}
   ```

2. **A source language with more categories than English writes all of them.** Lingui's Czech source example
   lists four.
3. **Positional syntax is a different contract.** In vue-i18n (documentation of 12.0.0-alpha.5, version-bound)
   cases are separated by `|` and must follow the CLDR order `zero | one | two | few | many | other` up to the
   number of categories the locale has: Russian takes four, in the order one, few, many, other. When there are
   more cases than the locale has categories, or when the locale tag is not BCP 47 (`pt_BR`), the library falls
   back to the English rule. The Vue side of this is in `vue-nuxt-vuetify-conventions` §6.7.

## 1.3 Formatted numbers and ordinals
1. **When the number is shown with special formatting, select on the formatted number.** Fluent's guide says
   to give the selector the same formatting options as the display, because the formatted number picks the
   category and for some languages it differs from the category of the raw number.

   ```
   your-score =
       { NUMBER($score, minimumFractionDigits: 1) ->
           [0.0]    Zero points, try again.
          *[other]  { NUMBER($score, minimumFractionDigits: 1) } points.
       }
   ```

2. **Ordinals are a separate selector with their own categories** (`selectordinal` in ICU, `type: "ordinal"`
   in Fluent). English uses `one`, `two`, `few` and `other` for 1st, 2nd, 3rd and 4th; Chinese and Arabic use
   one form (next-intl). A cardinal plural cannot stand in for it.
3. **Some translation tools reject ordinals.** The formatjs lint rule `blocklist-elements` gives that as its
   reason, and its recommended and strict presets block `selectordinal`. That is the rule's stated reason, not
   something verified here: ask the vendor before depending on it.

## 1.4 Offset, combined selectors and grammatical variation
1. **Avoid `offset` and several plurals in one message.** Lingui documents `offset` ("you and 2 friends read
   this"), while the formatjs lint rules `no-offset` and `no-multiple-plurals` forbid it and give the reason
   that some translation vendors do not allow it. The sources disagree, so this block does not adopt
   `offset` as a default: use it only after the vendor has confirmed, and write the confirmation in the project.
2. **Count the sentences a message flattens to.** The formatjs rule `no-complex-selectors` counts the strings
   produced when every selector is expanded (a plural with two branches inside a sentence is two sentences)
   and defaults to a limit of 20, taken from a vendor's guide. A plural next to a three-way select is already
   six. When the product multiplies, split the message at a sentence boundary, never inside a sentence (§2.1).
3. **Grammatical variation goes through `select` inside the message, not through branching in code**
   (Lingui translator-friendly guide), so the whole sentence stays in one message for every variant.
   `other` is required. In next-intl a select value may contain only letters, digits and underscores, so a
   locale tag such as `en-GB` must be mapped to `en_GB` before it is passed.
4. **Grammatical forms of a term travel with the term.** Fluent's terms take parameters, so one brand name
   can hold a nominative and a locative form and the sentence asks for the case it needs; a term can also carry
   an attribute such as a gender that a message selects on. That is Fluent syntax. Own guidance for ICU
   catalogs: the caller passes the already-chosen form as a select argument, and the translator sees all
   forms in the one message.
