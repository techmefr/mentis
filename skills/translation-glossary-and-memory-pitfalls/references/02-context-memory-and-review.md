# translation-glossary-and-memory-pitfalls §2 — Context, memory and review

Own knowledge of localisation practice, "re-read before relying" for anything tool-specific. Extraction, IDs, and the
tool's blocking checks are `i18n-catalog-workflow-pitfalls` §1 to §3; the key of a message is also its identity
in the memory (`i18n-catalog-workflow-pitfalls` §2.1).

## 2.1 The brief and the context
1. **Symptom:** a one-word string such as "Back", "Post" or "Open" is translated with the wrong meaning, a string
   is too long for its button, a placeholder is moved to a position that breaks the grammar. **Cause:** the
   translator saw a string and not the place. **Fix:** every string carries a note (where it shows, what the
   variables stand for, the length limit) and, for the ambiguous ones, a screenshot or a link to the screen.
2. **A short string with two meanings is two messages.** "Post" the noun and "Post" the verb need two keys and two
   notes; one key forces one translation.
3. **Send the brief with the first batch.** It lists the product in a paragraph, the audience, the glossary, the
   style guide, the placeholder syntax, the length rules, the delivery format and who answers questions. A
   vendor who has to ask for each of these will guess instead.
4. **Give a way to ask and a way to answer.** Questions from translators go to one channel and the answers are added to the
   note on the string or to the glossary, so the next batch does not ask again.
5. **Keep the unit of translation a whole message.** Never cut a sentence across two strings or build it by
   joining fragments; the order and the inflection of the target language will not fit (the rule for building
   messages is `i18n-message-format-pitfalls`).

## 2.2 Translation memory
1. **What it is:** a store of past source and target segment pairs, offered again when a new source segment is
   identical (an exact match) or close (a fuzzy match, shown with a similarity score). It saves cost and keeps
   wording stable.
2. **A memory is an asset with an owner.** It belongs to the product, not to the vendor's tool; make sure the
   contract and the export give it back, in an exchange format (§2.4).
3. **A memory without context matches wrongly.** An exact match for a one-word segment can be right in one
   screen and wrong in another; a match that also agrees on the context (the key or the surrounding text) is
   worth more, and a tool that can store it should.
4. **Do not train the memory on unreviewed output.** An unreviewed machine draft that is saved to the memory is
   offered as a trusted match later. Save only approved segments, with a status and the author.
5. **Keep one memory per locale and per domain when voices differ.** A legal text and a button label in the same
   memory pollute each other's fuzzy matches; split it when the style differs, not before.
6. **Clean it on a schedule.** Remove segments whose source no longer exists, and segments that contradict the
   current glossary (§1.1.5), or the memory will keep re-offering the old term.

## 2.3 Source edits and fuzzy matches
1. **Symptom:** after a small source edit, the old translation is still shown in the product although it no longer
   means the same thing. **Cause:** the key stayed and the translation was kept. **Fix:** when the source text
   changes, the translation becomes "needs review", never "done"; the catalog tool or the key policy has to
   make this visible (`i18n-catalog-workflow-pitfalls` §2.1 on what changes an ID).
2. **A fuzzy match is a suggestion, not a translation.** The translator must read it against the new source; the
   similarity score is not a quality score, and a one-word change in a negation or a number can invert the
   meaning at a high score. Never auto-accept above a threshold you chose yourself; if a threshold is used,
   record it and the sample check that justified it (§2.5).
3. **Group repeated strings.** Identical source text in many places is translated once and propagated; a "repetition"
   with different meaning is the same problem as §2.1.2.
4. **Freeze before a release, and say what a late change costs.** A source edit after the translation was sent
   creates a second round; agree a freeze date and a path for urgent copy changes (one string, one reviewer) so
   the exception does not become the process.
5. **Count what changed, not what exists.** Ask the tool for new, changed and unchanged segments before sending a
   batch, so the vendor is paid and briefed for the delta.

## 2.4 Exchange formats and what they lose
1. **The common formats:** TMX moves translation memories, XLIFF moves a file to and from a translator with
   notes and states, and TBX moves termbases (re-read before relying: version differences and tool support).
   Most tools import and export all three; few preserve everything.
2. **Symptom:** after an import into another tool, placeholders are shown as plain text, notes have vanished, or
   statuses reset to "new". **Cause:** inline markup, notes and states are the parts a format carries least
   consistently. **Fix:** a round trip on a sample before a migration: export, import elsewhere, export again and
   diff the placeholders, notes, states and counts.
3. **Keep the source of truth in the repository's catalog files, and treat the tool as a working copy.** A
   migration is then a re-import of the catalog plus the memory, not a rescue of a database.
4. **Check the encoding and the line-ending policy of the exchange file**; a tool that converts quotes or
   normalises text differently from yours produces a catalog diff far larger than the change
   (`i18n-catalog-workflow-pitfalls` §1.3).

## 2.5 Review and quality sampling
1. **Delivery is not acceptance.** The vendor's own check is a start; an in-country reviewer for each locale reads
   a sample of the delivery against the glossary and the style guide before the strings ship.
2. **Review in context.** Reading a spreadsheet misses length overflows, a wrong gender and a broken sentence
   around a variable; review in the running product, in the pseudo-locale and the real one
   (`i18n-catalog-workflow-pitfalls` §3.1).
3. **Score with a small fixed list of error types**, such as accuracy, terminology, fluency, style and locale
   convention, each with a severity, so a rejection is specific and a trend is visible across batches. A
   single "bad" or "good" teaches no one (re-read before relying: published quality frameworks exist; none was
   read for this block).
4. **Sample, do not read everything, and sample the risk.** Pick strings at random plus the ones that carry
   money, legal text, safety or the first-run flow; the method is in `sampled-evaluation`.
5. **Feed findings back into the glossary and the memory the same day.** A correction that stays in the
   product but not in the memory will be undone by the next fuzzy match.
6. **A model-drafted translation follows the same path.** It gets the glossary and the guide as input, a human
   in-country review of a sample, and the same error list; the unreviewed draft is never written to the
   memory (§2.2.4).
