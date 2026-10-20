# Other languages: the method, the translated-draft signals, Spanish

> Reference for `business/ai-prose-tells`. Read it when the text under audit is neither English nor French
> (`03-french.md` has its own file). It states a method, not a phrase list: no library exists here for
> German, Italian, Portuguese or any other language, and none is invented.

## 1. The method for any language

1. **Never apply the English lists silently.** English instances of a family ("delve", "it is worth
   noting") do not exist in another language, and their closest translations are often ordinary words
   there. Name the language you audited and the method you used.
2. **Judge by mechanism.** The families in `01-tells.md` and `02-more-tells.md` are mechanisms: a frame
   that announces a point, a closer that restates, a contrast nobody asked for, a certificate of honesty,
   a chatbot closing. Look for the mechanism in the target language's own idiom. The not-X-but-Y
   formula, for one, exists in every language and is treated the same way.
3. **Sample first, and add no fact.** The author's own writing in that language outranks any list
   (`SKILL.md` step 1), and a rewrite adds no fact, drops no claim (`SKILL.md` step 2).
4. **Say what you cannot judge.** For a language without a section here, report only the mechanisms you
   can recognise with confidence, mark the rest as unchecked, and ask for a native reader before a
   rewrite of anything beyond the clear cases (certain tier, residue strings in `02-more-tells.md` §3,
   which are language-neutral).
5. **Typography follows the language.** Quotation marks, the dash, the decimal separator, spacing before
   punctuation and heading case are conventions of the language. Native typography is never a tell; its
   absence, in a cluster, is a signal (section 2).

## 2. The translated-draft signals

A great deal of generated text in a language that is not English is an English draft in disguise: the
model arrives at the point in English patterns and emits target-language words. The marks are about the
translation, not about any single tell:

- loan translations of English idioms and of the stock vocabulary (the instances in `01-tells.md` family 1,
  carried across word for word);
- English quotation marks and English punctuation spacing where the language has its own;
- English title case in headings, and capitalised weekdays, months, nationalities or language names in a
  language that writes them in lower case;
- English word order that puts the new information first, so that every sentence opens on its subject and
  ends on something the reader already knew;
- hyphenated modifiers built the English way where the language forms compounds differently;
- pronouns and possessives spelled out in a language that drops them, because English cannot;
- a register that slides between formal and informal address inside one document.

**Weak alone, strong as a cluster.** One of these is a person's slip or a translator's choice. Several in
one document say "translated draft". The finding is that: it does not say who or what wrote it. Fix them
only when the text is yours to edit, with the language's own conventions, and offer the fix rather than
imposing it when a native speaker is available.

## 3. Code-switching is voice

A bilingual writer who moves between two languages inside one text (technical terms kept in English in a
Spanish or Portuguese README, a Spanish phrase inside English prose) is making a choice. Do not translate
it away, and do not count it as a tell. Established terms that practitioners say in English (a protocol,
a tool, a pattern name) stay in English; the tell is the opposite pair, a settled term translated into
something nobody says, and plain English left where a common word exists. Match the field, not the
dictionary. A mismatch between varieties of a language raises suspicion only when the shift is abrupt
and unexplained; a non-native writer's mixed usage is not evidence.

## 4. Spanish (to be checked by a native speaker)

> Status: the mechanisms are the same families as in `01-tells.md`, and the instances below are our own
> examples of each. A speaker of the language has not reviewed them; treat each as a candidate, not a
> rule, and prefer the writer's own sample over this section.

Where the families land in Spanish, as mechanisms with an example each:

- **Inflated connectors** (family 31). A sentence opening with a stock transition that names no real
  relation: "en este sentido", "cabe destacar que", "por otro lado" chained across a paragraph. Keep a
  connector that names a contrast or a consequence.
- **Formulaic openers** (families 5, 15). An opening about the era or the landscape instead of the
  subject: "en el mundo actual", "hoy en día", "en la era digital". Start with the first fact.
- **Promotional vocabulary** (family 1). "innovador", "de vanguardia", "imprescindible" as approval.
  Same test: a measure or a name in its place.
- **Copula avoidance** (family 22). "se erige como", "se consolida como", "constituye un" where "es"
  fits. Substitute the plain verb; if the meaning holds, use it.
- **Generic closers** (family 11). "en definitiva", "el futuro es prometedor", "un antes y un después"
  closing a text that already showed its point.
- **Signposting** (family 5). "vamos a explorar", "veamos a continuación": announce nothing, start with the
  content.
- **Academic inflation** (families 1, 36). "resulta imperativo", "cobra especial relevancia", "no cabe
  duda de que": the sentence promises weight it does not carry.
- **Chatbot openers and closers** (family 4, certain tier). A praise or an offer opening or closing a
  document ("¡excelente pregunta!", "espero que esto te sirva") in text with no reader to answer.
- **Typography** is the language's own: « » or the Spanish quotation marks, the inverted question and
  exclamation marks, lower-case weekdays and months, sentence-case headings. Their presence is correct;
  their absence in a cluster is a section 2 signal.

Not flagged: the reflexive passive ("se actualiza", "se envía") as a convention of technical and legal
Spanish, long sentences with several clauses, and regional vocabulary.

## 5. German, Italian, Portuguese and the rest

Nothing beyond sections 1 to 3. Idiom lists for these languages were not found in the sources read and are
not invented here. Until a fluent reviewer writes a section, the method applies: mechanism over word,
sample first, no added fact, no dropped claim, native typography respected, and a clear statement that
the audit stopped at what could be judged. The same holds for a multilingual product that ships six
languages: audit each in its own language, with a reader of that language for the rewrite.

## 6. Positive requirement

As in `01-tells.md` §5: each text leaving the filter, in whatever language, says what it is, for whom, and
carries one checkable detail.
