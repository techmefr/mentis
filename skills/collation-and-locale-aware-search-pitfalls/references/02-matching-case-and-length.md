# collation-and-locale-aware-search-pitfalls §2 — Matching, case and length

Collation facts are from UTS #35 part 5 (facts only). Read 2026-10-20 for facts only, restated in our words: the
Unicode special-casing data file (Turkish and Azerbaijani i, sharp s, final sigma), the normalisation report UAX #15,
and the PostgreSQL collation page (nondeterministic collations). Segmentation rules and the Intl API options are
our own knowledge, "re-read before relying" throughout (the ECMAScript specification page was tried; the part read
held only the constructor and the table of contents).

## 2.1 Case: folding, mapping and language
1. **Symptom:** a search for "Istanbul" typed in a Turkish locale misses, or a Turkish user's "i" becomes a
   dotted capital that no one expects, or the reverse. **Cause:** in Turkish and Azerbaijani the letter i has a
   dotted and a dotless pair, so the default lower-casing of an uppercase I is wrong for them (confirmed in the Unicode special-casing data: under the Turkish and Azerbaijani language conditions the uppercase I lower-cases to the dotless i unless a dot above follows, the lowercase i upper-cases to the dotted capital, and a combining dot above after I is removed; these rules are conditional on language). **Fix:** pass the
   language to the display conversion (the `toLocaleLowerCase` and `toLocaleUpperCase` forms), and never run the
   default one on text a user in those locales reads.
2. **A case change can change the length.** Upper-casing the German sharp s gives two letters (confirmed: the data's unconditional mapping is to two S letters, and the pair-stability policy prevents changing it to the capital sharp s), and some other
   characters expand or have no one-to-one pair. **Symptom:** a field that is limited in length overflows after
   upper-casing, or a character index taken before the change points elsewhere afterwards. **Fix:** never
   assume a case conversion keeps length or position; recompute.
3. **Case-insensitive matching is not "lower-case both sides".** Lower-casing is a display operation; matching
   needs case folding or a collator at secondary strength or lower, which treats the pairs the language treats
   as the same letter (confirmed: the Greek capital sigma lower-cases to the final form only under a context condition on the surrounding letters, not by language).
4. **Title case is language-dependent.** "Capitalise each word" breaks names with particles and apostrophes and
   languages that do not capitalise nouns the same way; do not title-case user data, and keep a display rule
   for headings only.
5. **Do not hand-roll an ASCII fold.** A table for the letters of one language misses all the others; use the
   platform's folding or the collator.

## 2.2 Accent- and case-insensitive search
1. **Symptom:** a search for "resume" does not find "résumé", or the reverse. **Cause:** a byte-for-byte
   comparison. **Fix:** compare with the collator at a lower strength: primary ignores accents and case,
   secondary ignores case only (the spec's common combinations). The Intl option for this is the sensitivity
   of the collator, with "base" as the primary level (re-read before relying).
2. **Deleting combining marks after decomposing is a shortcut with a failure rate.** It works for languages where
   the accent is decoration and breaks where the accented letter is a letter of its own (it merges two distinct
   letters in some alphabets). **Fix:** use the collation of the user's language at primary strength, which
   knows which marks matter; do not derive "accent-free" copies of user text for matching.
3. **CLDR has a collation type for searching.** The root data defines a "search" type, a locale may tailor it, and
   a request for a longer name that starts with "search" falls back to it, then to the root one; matching
   should ask for that type, not for the sorting one, since the best order for display is not always the best
   rule for equality.
4. **A match must not stop inside a user-perceived character.** The collation specification defines match
   boundaries (none, whole character, whole word) and styles (minimal, medial, maximal). Without a
   boundary rule, a search for "e" can match the base of a decomposed "é" and highlight half a letter. Use a
   search function that respects boundaries, or check that the match ends on a cluster edge.
5. **Collation-based matching is not a substring index.** A collator compares whole strings; for substring search
   over a large corpus, the engine's analyser and folding are the lever (`search-engine-index-settings-pitfalls`
   and `elasticsearch-mapping-and-reindex-pitfalls` own that), with the same strength decision stated.
6. **Tokenising by spaces fails for scripts that do not use them.** Chinese, Japanese and Thai need a word
   segmenter (the `Intl.Segmenter` with word granularity, or the engine's analyser for the language); do not
   split on whitespace and call the result words.

## 2.3 Normalisation and uniqueness
1. **Symptom:** two usernames or filenames that look the same are accepted, or a copied value does not match its
   source. **Cause:** a letter can be one code point or a base plus a combining mark; both display the same.
   **Fix:** choose one normalisation form at the input boundary (the composed form is the usual storage choice)
   and normalise before comparing or storing an identifier. Confirmed (normalisation report): the four forms are canonical decomposition, the same with canonical composition, and the compatibility versions of both; two strings put in the same form can be compared byte for byte; most text is already in the composed form and checking is much faster than normalising; the web standards body recommends the composed form for web content. The compatibility forms erase distinctions (superscripts, ligatures, long s) and the report says they must not be applied blindly to arbitrary text, so do not use one to normalise what a person reads or what must round-trip.
2. **Collation normalises internally; equality does not.** The algorithm decomposes before it compares (with an
   option to skip it when the input is known to be safe), so a sort looks right while a plain equality test of
   the same strings fails. Do not use a sort's behaviour as proof that a lookup works.
3. **A case- or accent-insensitive collation on a unique column makes a different set of values collide.** It
   may reject "resume" next to "résumé". **Decide per column:** an identifier uses a binary or a fixed
   normalisation-and-fold rule written in code; a person's name is not unique at all. Read the engine's own
   behaviour in `mysql-pitfalls` §1.3 and `laravel-mysql-to-postgres-pitfalls` rather than assuming.
4. **Look-alike characters from different scripts are a security question, not a collation one.** A collator
   will not make a Cyrillic letter equal to a Latin one; a policy for confusable identifiers is a separate check
   (re-read before relying; not covered by this block).
5. **A database's case-insensitive equality has a price and limits.** Confirmed on one engine (PostgreSQL docs):
   a nondeterministic collation treats different byte sequences as equal (the manual's example is a case-insensitive
   one built from the root locale at secondary strength), standard and predefined collations are deterministic,
   a user-defined one is deterministic unless declared otherwise, a B-tree index cannot use deduplication with a
   nondeterministic collation, some pattern-matching operations are unavailable, there is a performance cost, and
   the manual's tip is to consider the normalisation functions instead. Symptom: a `LIKE` search on a column made
   case-insensitive this way errors or is slow, and an index is larger than expected. Check: read the engine's list of
   unsupported operations for your version before choosing it for a column that is searched by prefix. Fix: use it
   only where equality must be insensitive, and keep pattern search on a normalised, folded copy.

## 2.4 Length and truncation
1. **Symptom:** a counter says 140 and the user typed fewer visible characters, a cut leaves a broken glyph or a
   replacement mark, a flag or a family emoji is cut in half. **Cause:** the length counts code units or code
   points, while a user sees clusters (a letter with its marks, a sequence joined into one emoji).
   **Fix:** count and cut by user-perceived character with the segmenter (the grapheme granularity of
   `Intl.Segmenter`, or the ICU break iterator).
2. **Name the unit of every limit.** A UI limit counts clusters, a storage limit counts bytes or characters
   depending on the engine's column type, and an API limit often counts code points. Write the unit beside the
   number in code and in the error text; a column in characters can still overflow a bytes limit on the wire.
3. **A cut needs an ellipsis rule and a boundary rule.** Cut at a cluster edge, and where the text is words, at a
   word edge from the word segmenter, never at a fixed code-unit offset.
4. **Case conversion happens before the length check, not after** (§2.1.2).
5. **Right-to-left and mixed text can be cut where the visible order is not the logical one.** The logical
   order decides a cut; see `rtl-and-bidi-layout-pitfalls` §2 for isolating the result.
