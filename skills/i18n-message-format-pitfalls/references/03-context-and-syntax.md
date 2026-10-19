# i18n-message-format-pitfalls §3 — Context for translators and syntax hygiene

A translator reads the message and what you attached to it. A parser reads the syntax and nothing else. Both
fail quietly: a guessed meaning ships as a wrong word, and an invalid message fails only when it is rendered.

## 3.1 Context
1. **A short or ambiguous string carries a translator comment.** Say what the UI element is, where it appears,
   any length limit, and whether a word is a noun or a verb. "Back", "Post", "Save" and "Open" are the strings
   that need it most (Lingui translator-friendly guide).
2. **A comment adds information; a context splits meanings.** When the same text means two things, it gets two
   contexts so the two can be translated differently; Lingui's example is "right" as correct and "right" as a
   direction. When the text is unambiguous and you only want to add information, use a comment. This is the
   catalog-side form of `vue-nuxt-vuetify-conventions` §6.13, which says to use two keys. Adding a context to a
   message that is already translated creates a new catalog entry (Lingui), see `i18n-catalog-workflow-pitfalls` §2.
3. **Enforce it with lint, not with review.** The formatjs rule `enforce-description` requires a description
   on each message, with an optional minimum length and a mode that demands a literal; Lingui's
   `require-comment` does the same and is described as strict, best on new code. Both docs give the reason
   that the description is helpful context for translators.
4. **A per-file context directive must be closed.** Lingui's `lingui-set` applies a context and a comment to every
   later message in the file, so an unclosed one leaks into messages added later; its rule
   `require-directive-reset` requires the matching `lingui-reset`. Tool-specific.

## 3.2 Syntax
1. **Escape syntax characters with the ASCII apostrophe.** Braces written between apostrophes print literally
   (next-intl: `'{name}'`), and two consecutive apostrophes print one. The formatjs page recommends the curly
   apostrophe for text a person reads and the ASCII one only for ICU syntax. Because braces open an argument
(next-intl), a literal brace in text that was never escaped is read as one.
2. **Lint for validity.** The formatjs rule `no-invalid-icu` exists because a message can look right and still
   be invalid, for instance a plural with the comma after the argument name missing. Run it in CI so the
   failure is a red build and not a runtime error on one locale.
3. **No consecutive whitespace and no backslash line continuation in a message.** The formatjs rule
   `no-multiple-whitespaces` gives the reasons that consecutive whitespace is handled differently by locale and
   that a backslash line break inside a string produces awkward spaces.
4. **Vendor limits are a checklist you complete once.** The formatjs lint rules list, as their stated
   reasons, vendors that cannot handle `selectordinal`, `offset`, several plurals, camelCase placeholders or
   emoji. None of this was verified here. Own guidance: before enabling or ignoring any of those rules, ask the
   vendor or the translation tool, and write the answer next to the lint configuration.
