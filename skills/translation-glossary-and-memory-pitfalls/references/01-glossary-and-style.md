# translation-glossary-and-memory-pitfalls §1 — Glossary and style guide

Own knowledge of localisation practice, "re-read before relying" for anything tool-specific. The in-catalog
mechanisms (comments, terms in a message format) are in `i18n-message-format-pitfalls` §1.4 and
`i18n-catalog-workflow-pitfalls` §3.2.

## 1.1 A glossary is a record, with an owner
1. **Symptom:** "workspace" is a different word on the dashboard, in the email and in the help page; a translator
   asks which is right and gets three answers. **Cause:** the decision was made in a message and never written
   down. **Fix:** a glossary file per locale, in the repository, with one row per term.
2. **A row holds:** the source term, a one-line definition, the target term, the part of speech and gender where the
   language marks it, a usage note, forbidden alternatives, a status (proposed, approved, deprecated), an
   owner and a date. Without the definition, the same word has two meanings and one target term.
3. **Add a term when it appears twice, not when it is invented.** Start from the words that recur in the source and
   from the screens a user reads; a glossary of five hundred rows no one opens is worse than forty that are checked.
4. **One owner per locale decides.** A vendor proposes, the product owner or a named reviewer for that locale
   approves. Two reviewers deciding on the same term is how the glossary splits.
5. **A term change is a migration.** Renaming an approved term leaves every earlier translation out of date;
   deprecate the old row, record the new one, and search the memory and the catalog for the old target (§2.3).
6. **Keep the glossary in an exchange format the tools read.** A spreadsheet is fine as source; a termbase format
   (TBX) or the tool's own import is what a translator tool highlights while translating (re-read before
   relying: format support differs by tool).

## 1.2 Do-not-translate and borrowed words
1. **Symptom:** a brand name, a command, a feature name or a unit is translated in one place and left in another.
   **Cause:** no one decided. **Fix:** a status "keep" in the glossary with a reason (legal, a name users search
   for, a code identifier) and, where a language declines or inflects, the inflected form allowed next to it.
2. **Mark placeholders and code names in the message, not only in the glossary.** A tag, a variable and a
   command-line flag stay out of the translator's reach through the message format
   (`i18n-message-format-pitfalls`), and a glossary rule does not stop a tool from mangling them.
3. **A borrowed word is a decision, not a default.** In some languages the English term is the common one and the
   native one sounds stiff; in others the reverse. Ask a native reviewer for the locale and write the answer.
4. **A name that is also a word needs a gloss.** If a feature name is an ordinary word ("Boards", "Flows"), say in
   the usage note whether the word keeps its meaning in the target language.

## 1.3 Style guide per locale
1. **Decide the address form once.** Formal or informal "you" (languages that have both), the register of
   instructions (imperative or infinitive), and how the product addresses an error, a success and a warning. A
   style choice made per string produces a product that switches mood between screens.
2. **Decide the regional variant on purpose.** European and Brazilian Portuguese, Latin American and European
   Spanish, simplified and traditional Chinese, and several others differ in vocabulary and sometimes grammar; a
   single "Portuguese" or "Chinese" file is a decision to serve one and to annoy the other. One locale tag per
   variant, one native reviewer each (`locale-negotiation-and-switcher-pitfalls`).
3. **Write down the typography the locale needs:** quotation marks, the space before some punctuation, the list
   and ellipsis style, abbreviations, capitalisation of headings and of months and days. These are small and
   show everywhere; the value formats themselves come from the formatter (`locale-value-formatting-pitfalls`).
4. **Gender and inclusivity are locale decisions.** Where a language inflects for the user's gender, choose the
   approach (a neutral form, paired forms, a message format that selects on a known value) in the guide; never
   guess a user's gender from a name (`international-input-pitfalls` §4.1).
5. **Keep the guide short enough to be read before the first string.** One page of rules and a few before-and-after
   examples from the product beats a long document; examples must come from real strings, not invented ones.
6. **The style guide and the glossary are inputs to a machine-translation or model step too.** If a model drafts the
   translation, pass the glossary rows for the strings in scope and the guide's rules, and review against them
   (§2.5); an unprompted draft has neither.
