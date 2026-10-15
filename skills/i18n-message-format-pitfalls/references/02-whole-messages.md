# i18n-message-format-pitfalls §2 — Whole messages, placeholders and tags

Translators work from a catalog: one message, out of order, no screen (Lingui). Whatever they cannot learn
from the message itself is a guess, and a wrong guess is found after release.

## 2.1 The sentence is the unit
1. **One sentence, one message.** "You have", then a count, then "unread messages" is three unrelated
   messages, and nothing in them can be reordered. Use one message with a plural (Lingui). This extends
   `vue-nuxt-vuetify-conventions` §6.8, which states the concatenation rule for Vue.
2. **A leading or trailing space, or a placeholder glued to a unit, marks a fragment.** The formatjs rule
   `prefer-full-sentence` fails `{count}day` and a message that ends in a space, because units and spacing
   vary by locale; its advice is a number skeleton or an `Intl` formatter for the unit.
3. **Markup belongs to the sentence too.** A sentence with an inline link is one message with a tag around the
   link text, so the translator can move the link where the language needs it (Lingui; next-intl).
4. **A message that is only `{variable}` is not a message.** There is nothing to translate; use the value
   directly (formatjs `no-useless-message`; Lingui `no-single-variables-to-translate`).

## 2.2 Placeholders
1. **Name every placeholder.** In Lingui, a plain variable becomes a named placeholder, but a property access or
   a call becomes `{0}`, which does not say whether the value is a name, a number or a date, nor whether it
   needs an article or a case. Give the value a name, either with Lingui's `ph` label or by putting it in a
   well-named variable first. The lint rule `no-expression-in-message` reports the positional cases.
2. **Renaming a variable renames the placeholder.** With generated message IDs that also changes the ID
   (Lingui), which sends the message back to translation; see `i18n-catalog-workflow-pitfalls` §2.
3. **The case of a placeholder name is a project choice, not a rule from these sources.** Lingui's examples use
   camelCase names such as `dueDate`, while the formatjs rule `no-camel-case` forbids camelCase and gives the
   reason that some translation vendors are case-sensitive. This block adopts neither; ask the vendor. In
   next-intl a name may contain only letters, digits and underscores, so a dash never works. Own guidance:
   letters, digits and underscores are valid in both stacks.
4. **Supply every value and lint it.** The formatjs rule `enforce-placeholders` reports a missing or an unused
   value, but only when the values are passed as a literal object; values held in a variable cannot be checked.

## 2.3 Tags
1. **Tags are named, not numbered.** With indexed tags the translator has to guess which index is the link
   and which is the emphasis, and reordering the elements in code silently changes the message. Lingui maps
   tag names to placeholder names in its configuration (`macro.jsxPlaceholderDefaults`, lingui 6.9.1) and ships
   `no-unnamed-tag-placeholders` to report what is still numeric; next-intl rich text uses named tags from the
   start (`<guidelines>…</guidelines>`).
2. **A tag name is unique within a message.** In Lingui two links with different props both map to `link`
   and the macro throws; give at least one an explicit name. Identical elements such as two bare line breaks
   share a name without error.
3. **Attributes stay at the call site.** next-intl cannot put an attribute inside a message; when the target of
   a link has to be translated, keep it as its own message and read it in the tag handler.
4. **ICU needs a closing tag even when there is nothing inside.** next-intl writes a line break in a message
   as `<br></br>`. Tags may nest.

## 2.4 Several strings, one widget
1. **A widget with several user-visible strings is one unit.** An input has a value, a placeholder, an
   accessible name and often a title. Fluent keeps them in one message with attributes (`.placeholder`,
   `.aria-label`, `.title`), so editors, comments and tools see them together. That is Fluent syntax. With the
   flat sentence keys of `vue-nuxt-vuetify-conventions` §6.1 and `vue-nuxt-vuetify-conventions` §6.2 there is
   no attribute construct; own guidance: give the sibling keys the same translator comment naming the widget
   (§3.1) and keep them next to each other in the catalog.
