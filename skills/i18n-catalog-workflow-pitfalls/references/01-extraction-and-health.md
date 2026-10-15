# i18n-catalog-workflow-pitfalls §1 — Extraction and catalog health

A translation catalog is produced from code and consumed at runtime, and nothing in between complains when the
two drift apart. The checks below turn that drift into a red build.

## 1.1 Extraction is static
1. **Extraction reads the source without running it, so only literal messages are found.** Lingui's guide says
   the extractor cannot follow a variable or a function result: a message held in a constant and passed to the
   call later is not extracted, and the same call written with the literal inside is. The same holds for a key
   built with string interpolation.
2. **Match is by call shape, not by import.** Lingui's extractor recognises `i18n._` and `i18n.t` calls by
   name, including on other objects, and does not check where the function came from; the formatjs linter also
   matches calls by name, and a wrapper with another name is invisible to it until it is listed in its settings
   (`formatjs.additionalFunctionNames`). An unrelated function with a matching name is treated as a translation call.
3. **Mark the rare dynamic message explicitly.** Lingui accepts a `/** i18n */` comment in front of a literal
   or a descriptor, and `lingui-extract-ignore` to leave a call out. i18n-tasks 1.1.2 has a hint comment,
   `i18n-tasks-use`, that declares a key as used, and its README calls this the answer for keys built at runtime.
4. **A dynamic key is not recognised as used by default.** In i18n-tasks, `t "cats.#{cat}.name"` is reported
   missing or unused until the key is hinted or `search.strict` is turned off. Non-strict mode treats one
   segment per interpolation as a wildcard, so a key nested one level deeper is still reported as unused.
   Localised date calls are another case the README says cannot be inferred. Own guidance: the cheapest fix is
   a lookup table of literal keys, which extraction reads as it is.

## 1.2 A health check in CI
1. **Run a check that lists missing keys, unused keys, interpolation variables that differ between locales,
   and files that are not normalised.** That is the content of the i18n-tasks `health` command, and the
   README ships a test template for RSpec and Minitest that runs it on every CI run. Whatever tool the project
   uses, the four items are the requirement.
2. **A missing key otherwise fails at runtime, in one locale, for the user who reads it.** Own reasoning from
   `vue-nuxt-vuetify-conventions` §6.12, which makes the missing key loud in development; the CI check makes it
   fail before development is over.
3. **Treat an auto-filled key as untranslated.** i18n-tasks `add-missing` fills a missing key with the base
   value, or a humanised form of the key, by default. That entry exists so the file is complete; it is not a
   translation, and the vendor's list of untranslated strings is the one that counts.
4. **Unused keys are removed, not left.** i18n-tasks has `unused` and `remove-unused`, and `prune` drops keys
   from other locales that no longer exist in the base locale. Own reasoning: a dead key is translation cost
   already paid and a candidate for reuse by mistake.

## 1.3 Normalisation churn
1. **Normalising rewrites files, and the rewrite is not always neutral.** i18n-tasks sorts keys and, through
   its YAML emitter, may change how a multi-line string is written: its README shows two values that differ only
   by a trailing space on each line, one kept as a block and the other rewritten as a quoted string with
   escaped newlines.
2. **Run the first normalisation on its own, read the diff once, and commit it separately.** Own guidance:
   after that, the health check's "files are normalised" item keeps the diff small, and a reviewer is not
   asked to find a feature change inside a thousand reformatted lines.

## 1.4 Lint on the code side
1. **Require a description or comment on each message** (formatjs `enforce-description`; Lingui `require-comment`).
   The rule and its reason are in `i18n-message-format-pitfalls` §3.
2. **Forbid literal user-visible strings in markup.** The formatjs rule `no-literal-string-in-jsx` also checks
   attributes that a screen reader or a tooltip shows: by default `aria-label`, `aria-description`,
   `aria-details`, `aria-errormessage`, `placeholder`, `title` and the `alt` of an image. Its sibling
   `no-literal-string-in-object` checks properties such as `label` in an object that feeds a select. Both
   report string concatenation and template literals, and the first is JSX-specific; the principle for Vue is
   in `vue-nuxt-vuetify-conventions` §6.6.
3. **Check that every value is supplied** (formatjs `enforce-placeholders`, limits in `i18n-message-format-pitfalls` §2).
4. **Where a project has several message styles, pick one and forbid the other**: the formatjs rules `enforce-id`
   and `no-id` and the Lingui rules `require-implicit-id` and `require-explicit-id` exist so that the choice
   made in §2.1 is held by a tool.
