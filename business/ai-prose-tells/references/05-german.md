# ai-prose-tells §5 — German

> Reference for `business/ai-prose-tells`. Read it when the text under audit is in German.
>
> **Status: needs a native German reader before it is relied on.** The mechanisms were taken from two public
> German-language filters and restated in our own words, and the German examples are ours. The author of this
> file is not a native German speaker and nobody has reviewed it. Treat every instance below as a candidate: the
> author's own sample outranks it (`SKILL.md` step 1), and for anything beyond the certain tier and the residue
> strings (`02-more-tells.md` §3), a native reader decides before a sentence is rewritten.

The method is unchanged from `04-other-languages.md` §1: judge by mechanism, in clusters, add no fact, drop no
claim, respect native typography. This file only says where the families land in German and which tells are
German-only. Quoted phrases are examples of a mechanism, not a ban list.

## 1. The families, with German instances

1. **Mechanical connectors** (family 31). "darüber hinaus", "außerdem", "ferner", "ebenfalls" opening
   consecutive sentences. Keep a connector that names a real relation (contrast, cause, sequence); drop the
   rest and let the order of the sentences carry the link.
2. **Frames about the era** (family 5). "In der heutigen digitalen Welt", "im Zeitalter der ...",
   "in Zeiten von ...", "angesichts der rasanten Entwicklung": the sentence fits every subject, so it says
   nothing about this one. Start with the first fact.
3. **Opening on humanity** (family 5, stock framing). "Seit jeher", "seit Anbeginn der Zivilisation", "schon immer hat der
   Mensch ...": a grand claim about people to lend weight to an ordinary subject. Fine when the reference is
   specific (a date, a name, a place) and leads to the topic.
4. **Participial padding** (family 23). A chain of present participles ("ermöglichend", "gewährleistend",
   "hervorhebend") hung on a clause to sound analytical. Replace with a finite verb and a subject. In
   scientific and legal German the construction is conventional; leave it there.
5. **Copula avoidance** (family 22). "fungiert als", "stellt ... dar", "verfügt über", "zeichnet sich
   durch ... aus", "erweist sich als" where "ist" or "hat" says the same. Also raised verbs in neutral text:
   "verfasste" for "schrieb", "verstarb" for "starb". Judge by cluster; in a formal or elevated register the
   raised verb is correct. A real function ("dient als Notausgang") is information, not a tell.
6. **Nominal style hiding the actor.** "die Durchführung der Analyse", "die Nutzung von Daten", "die Umsetzung
   der Maßnahmen": a verb and its actor turned into a noun. Turn it back into a verb when the text names who
   acts. Fixed technical and legal terms stay.
7. **Analysis tail** (families 23, 24). A clause hung on a complete sentence that only restates its weight: "..., was die
   Bedeutung von X unterstreicht", "... und zeigt damit, dass ...". Test: delete the tail; if no fact is
   lost, it was padding. If the tail does carry a finding, it becomes its own sentence with its evidence.
8. **Comparative framing** (family 7). "weniger X als vielmehr Y", "eher X als Y", "mehr Werkstatt als Agentur" as a
   description. It sounds nuanced and says less than a direct statement. Ask which checkable claim sits
   behind it. A real, verifiable comparison is not the tell.
9. **Announcing split sentence** (families 5, 17). "Was mich überrascht hat, war ...", "Was dabei auffiel: ...": a cleft
   sentence that announces the point before making it, repeated before several points.
10. **Retroactive nuance and borrowed candour** (families 15, 16, 46). "Genauer gesagt ...", "fairerweise ...",
    "ehrlich gesagt ...", "die eigentliche Frage ist ..." where the next words repeat the claim more softly
    or add no precision. An opinion the writer does not hold, or an invented anecdote, is a fact the source
    lacks (`SKILL.md` step 4).
11. **Aspirational closers** (family 11). "bestens aufgestellt für die Zukunft", "die Möglichkeiten sind
    grenzenlos", "die Weichen sind gestellt". Normal in a press release or annual report, where the genre
    expects it.
12. **Chatbot openers and closers** (families 4 and 38, certain tier). A greeting or an offer at the start or end of a
    document with no reader to answer, a statement about a knowledge cut-off, a refusal ("Als Sprachmodell
    kann ich nicht ..."), a placeholder in brackets. One sighting is enough, after the check that a reader and
    a context are absent (`01-tells.md` §3).
13. **Marker vocabulary, as a cluster** (family 1). "beleuchten", "eintauchen", "nahtlos", "vielschichtig",
    "ganzheitlich", "das Zusammenspiel", "die Landschaft" (figurative), "spannend", "essenziell". One word is
    ordinary German and may be the exact word (robust statistics, dynamic routing, a milestone in a project
    plan). Three or more together in a short text is a finding, and the fix is the plain word or the named
    concrete field. These words are a functional transfer from the English marker list, not measured on German
    corpora; their discriminating power fades as the words spread into human writing.
14. **Neat list and heading shapes** (families 28, 34, 47, 55). Bold lead-ins on every bullet, repeated colon
    titles ("Thema: Warum ... und wie ..."), equal-length paragraphs, a closing sentence that adds no
    information. One colon title is ordinary; two or more built the same way in one document is the cluster.

## 2. German-only signals: translated English

German has conventions that English does not, so an English draft in disguise (`04-other-languages.md` §2)
shows through here in ways the other files cannot catch. Each is weak alone and strong as a cluster.

1. **Quotation marks.** German prose uses the low opening mark and the high closing mark pointing left, or the
   guillemet pairs (reversed in Swiss usage). A low opening mark followed by the English closing mark, or by a
   straight one, is an asymmetry that a content system does not produce by itself. Straight marks throughout a
   document, or English curly marks throughout, come from an editor or an export and prove nothing.
2. **English title case.** Capitalising adjectives, verbs and prepositions in a heading ("Der Komplette
   Leitfaden Für Modernes Marketing"). German capitalises nouns and the first word; sentence case is the norm.
3. **Decimal and date forms.** A point where German writes a comma ("3.5 Prozent"), a missing group
   separator in a long number, an English month name or date order in running text. The formatting rules
   themselves are in `skills/locale-value-formatting-pitfalls`.
4. **Genitive apostrophe.** "Peter's Projekt", "das Team's Ergebnis" borrow the English possessive. German
   writes the genitive without an apostrophe, except where one marks a dropped letter after a sibilant
   ending ("Hans' Auto").
5. **False friends.** Words used with their English sense: "eventuell" for "eventually" (German: possibly),
   "aktuell" for "actually" (German: currently), "sensibel" for "sensible" (German: sensitive). Report a false friend when the sentence only makes sense
   in English.
6. **Syntax carried over.** English word order inside a relative clause, a trailing prepositional phrase in
   the English place, a possessive spelled out where German uses the article, and collocations built word for
   word ("die Reibung fällt" for friction drops).
7. **Bullet punctuation.** A capital and a full stop on every fragment of a list of keywords. Consistency
   within a list matters more than the rule; keywords take no full stop, full sentences do.
8. **Address drift.** "du" and "Sie" mixed inside one document by the author's own voice. A quoted passage or
   a sentence-initial "Sie" meaning "she" or "they" is not drift.
9. **Too tidy, with no particles.** A friendly, informal text with no modal particles at all can feel written
   for an English reader. Do not add particles to repair it: inserting "ja", "doch" or "halt" to sound human
   is the performed voice this block warns against, and in a neutral or formal register their absence is
   correct.

## 3. What not to flag

1. **Established vocabulary.** "basiert auf", "in Bezug auf", "adressieren", "Sinn machen", "realisieren"
   for "erkennen" and common loan words (Meeting, Team, Feedback) are accepted German in many registers; one
   of them is not a finding.
2. **Regional variety.** Swiss, Austrian and German usage differ in vocabulary, register and typography
   (guillemet direction, no sharp s in Switzerland). Do not "correct" one variety towards another; match the
   audience of the text.
3. **Formal and scientific German.** Participles, nominal style, passive and long sentences are the
   convention in law, science and public administration; apply families 4 and 6 there only on request.
4. **Correct grammar, a transition word or a dash alone.** A single "darüber hinaus", one dash, or clean
   typography is how careful people write.
5. **Quotations, code, official product names, titles.** Edit the surrounding sentence only.

## 4. Positive requirement

As in `01-tells.md` §5 and `04-other-languages.md` §6: the German text leaving the filter says what it is, for
whom, and carries one checkable detail. Removing a tell leaves a hole that a fact fills, never a flourish.
