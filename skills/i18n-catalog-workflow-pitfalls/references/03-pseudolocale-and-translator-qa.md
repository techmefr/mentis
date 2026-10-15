# i18n-catalog-workflow-pitfalls §3 — Pseudo-locale and translator-side quality

Two checks sit on either side of translation: a fake locale that shows what the interface will do with text it
has never seen, and the vendor tool's own rules that decide what a translator can save.

## 3.1 Pseudo-localisation
1. **Generate a pseudo-locale before any translation exists.** Lingui's guide describes it as a way to see how
   the interface will look after translation and to catch source strings that should change before translation
   starts. It also exposes hard-coded strings and badly concatenated ones, because those are the strings that
   stay in plain source text while everything else is transformed.
2. **Give it width and a visible marker.** The Lingui configuration offers `prepend` and `append` strings,
   `extend` to widen each message by a percentage (its own example is 0.3 or 0.4), `extendCharacter`, and
   `override` to replace every non-token character, which makes an untranslated string easy to spot. Tags, ICU
   syntax and variables are kept intact by the tool, so the pseudo-message still renders.
3. **Add a right-to-left pseudo-locale when the product may need one.** `rightToLeft: true` inserts Unicode
   right-to-left override marks, and the configuration takes an array so one left-to-right and one
   right-to-left pseudo-locale can be generated together. The layout work itself is not covered by any block yet.
4. **A browser setting accepts only valid BCP 47 tags.** To open the application in a pseudo-locale named
   freely, an extension that sets the language header is needed (Lingui's guide notes Firefox's extension
   accepts any string). Without one, pick a valid locale your application does not use; its example is `zu-ZA`.
5. **Keep it out of the shipped locale list.** Own guidance, not from the sources: the pseudo-locale is a test
   fixture, so it should not appear in the language switcher or in `hreflang` output of a production build.
   Lingui's configuration says the pseudo-locale must be in the project's `locales` list to be generated, which
   is why this needs a deliberate exclusion.

## 3.2 What the translator's tool blocks
1. **Quality checks have two levels.** In Mozilla's Pontoon documentation, errors cover issues that would make
   the string be removed from products and cannot be bypassed: the submit button disappears until the error is
   fixed. Its examples are exceeding the maximum string length and incorrect syntax. Warnings can be bypassed:
   missing punctuation, a different number of sentences, capitalisation. Failures are stored, and strings with
   issues can be filtered.
2. **Some checks produce false positives and can be switched off by the translator.** Pontoon says so for a
   class of checks that come from a library it uses. Own guidance: when a vendor tool is chosen, ask which
   checks it has, which are blocking, and which a translator may disable.
3. **Set a maximum length for a string that lives in constrained UI, and say so in the comment.** Pontoon
   treats an exceeded maximum as a blocking error, which is the only way the limit holds. How a limit is declared in
   a given tool was not read, so the declaration step is own guidance; Lingui's guide already lists length limits as
   something a translator comment should carry (`i18n-message-format-pitfalls` §3).
4. **Keep a glossary for brand and product words.** Pontoon's terminology is a list of terms with definitions
   that are highlighted in a source string and shown with their translations; it can be exported in TBX, a
   standard exchange format. Fluent's terms (`i18n-message-format-pitfalls` §1.4) are the in-catalog form of
   the same idea. Whether a word is translated is a decision the glossary records, not each translator.
