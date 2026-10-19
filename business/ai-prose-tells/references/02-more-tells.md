# Further families, mechanical checks, and the register test

> Reference for `business/ai-prose-tells`. Read it at the audit step, after `01-tells.md`, when a draft
> still reads as machine-made but no family there names why. Family numbers continue from 14.

## 1. Further families

Same rule as before: judge the mechanism, not the word list. Each entry gives the test that decides
whether it is a tell or just a sentence.

**Frames that announce a point instead of making one**

15. **Authority frames.** "The real question is", "at its core", "what really matters", "fundamentally",
    "here is the thing". The frame promises an insight and then delivers the claim. Test: delete the
    frame. If the claim stands, the frame was decoration; if nothing is left, there was no claim.
16. **Candour openers.** "Honestly?", "to be frank", "let me be real", "I will be direct". They flag
    honesty at one point, which implies the rest was something else. Test: would the sentence be false
    without the opener? If not, cut it.
17. **Scaffold labels.** "The short version:", "Bottom line:", "Key takeaway:", "Plot twist:". A label in
    front of a sentence that already reads as the summary. Test: does the sentence still work with the
    label removed? Then remove it.
18. **Emphasis crutches.** "Full stop.", "Let that sink in.", "Read that again.", "That matters." and the
    hollow "X is real" ("the cost is real"). The writer asks the reader to feel weight the sentence did
    not carry. Test: put the missing fact in place of the crutch (what cost, how large).

**Voice and subject**

19. **Inanimate subject, human verb.** "The data tells us", "the architecture embraces change", "the
    release wants to simplify". Nothing here has intent; a person or a mechanism acts. Test: name who
    decided, or which code path does it. If nobody did, the sentence is mood.
20. **Performed reactions.** "That struck me", "I paused", "wait, actually", a mid-paragraph self-correction
    staged for effect, an interruption addressed to the reader. A real correction names what changed and
    why. Test: is there a before and an after the reader can check?
21. **Invented experience.** A personal error, anecdote or conversation the source does not contain. This
    is the worst one because it is a fact. Never added by a rewrite (`SKILL.md` step 4).
22. **Copula avoidance.** "serves as", "stands as", "boasts", "features", "represents" where "is" or "has"
    fits. Test: substitute the plain verb; if the meaning is unchanged, use it.
23. **Participle tails.** A clause hung on the end of a sentence with a participle: "..., ensuring
    reliability", "..., highlighting the importance of X". The tail asserts an effect without saying how.
    Test: can the participle become its own sentence with a subject and a checkable claim? If not, drop it.
24. **Vague connection.** "plays a role in", "is tied to", "is associated with", "contributes to". Say the
    relation: causes, blocks, replaces, reads from, delays by.

**Rhythm and repetition**

25. **Aphorism formulas.** A closing line built to be quoted: "Simplicity is the ultimate feature."
    "Great teams ship; good teams plan." Test: what checkable statement is inside it? Write that one.
26. **Synonym cycling.** One thing called by three names in neighbouring sentences ("the tool", "the
    platform", "the solution"). In technical writing a new word reads as a new thing. Keep one term
    (`business/ux-writing` §5.1 holds the same discipline for the interface).
27. **Trailing negations.** A negative clause tacked on for rhythm: "..., not a gimmick", "no guesswork,
    no friction, no surprises". Test: did anyone propose the thing being denied?
28. **Repeated openers.** Three sentences in a paragraph starting with the same word or the same shape.
    Count it per paragraph, not per document.
29. **Rhetorical question and answer.** A question the writer asks only to answer it: "The result? A faster
    build." Keep when the reader would plausibly ask it; cut when it only sets up the next line.
30. **Staged constructions.** "By the time X, I was Y", a sentence opening with "So," or "Look,", a colon
    or dash used to stage a reveal. One is a voice; a pattern across a document is a template.
31. **Mechanical transitions and chic words.** "Furthermore", "Moreover", "Additionally" opening
    consecutive sentences; "utilize" for "use", "commence" for "start". Transitions are fine when the
    relation they name is real (a contrast, a consequence).

**Typography and markup used as emphasis**

32. **Emphasis capitals.** A word in capitals or bold-italic for stress: "this is CRUCIAL". The reader
    hears shouting; if the point matters, the sentence order or one specific fact carries it.
33. **Scare quotes.** Quotation marks around ordinary words ("smart" routing, a "simple" fix). They
    distance the writer from a word they chose. Test: is it a quotation, a coined term, or a word
    mentioned rather than used? If none, remove the marks.
34. **Inline-header lists.** Bullets that each start with a bold label followed by a sentence that repeats
    the label: "**Performance:** Performance is improved." Test: would the list read the same as plain
    sentences? Then it is a paragraph in costume.
35. **Dash as universal joint.** The em dash used for every aside, reveal and pause. Decision for this
    framework: the default is to avoid it and to use a comma, colon, full stop or parentheses. Exception:
    when the user's own writing sample (`SKILL.md` step 1) uses dashes, match the sample. No quota, no
    counting per words; one dash in a paragraph is writing, a dash in every sentence is the pattern.
    Dashes in quotations, code, licences and legal text are never touched.

**Padding and invention**

36. **Extended filler.** "in order to", "it is important to note that", "due to the fact that", "at this
    point in time", "it should be noted". Test: delete the phrase; the sentence still parses and means
    the same.
37. **Speculative gap-filling.** The draft supplies a reason, motive, effect or timeline the source does
    not state: "which likely helped adoption", "probably because of the older API". It reads as insight
    and is invention. This is what audit question 2 in `SKILL.md` catches. Fix: state the gap ("the
    cause is not known") or remove the sentence.
38. **Knowledge-limit hedges.** "As of my last update", "specific details are limited", "I could not find
    more". A chat artefact; in a document either the fact is verified and dated or it is a stated open
    question with an owner.
39. **Fake-precision hedges.** "approximately 3 to 4 times, depending on several factors". A range and a
    cause wrapped around no measurement. Give the measured figure and its conditions, or say it was not
    measured.

## 2. Writing about the document, and production residue

40. **The document narrates itself.** Replacement history ("this section replaces the earlier draft"),
    method narration ("after reviewing several approaches"), layout captions ("the table below shows").
    A document describes its subject, not its own revisions or construction. Revision history lives in
    version control. This is common in MR descriptions and READMEs.
41. **Production commentary outside the body.** The blocker tier in `SKILL.md` also applies to captions,
    image alt text, table cells, commit messages and MR descriptions: "screenshot captured with a
    headless browser", "AI-generated illustration", "generated from the prompt above". The reader
    gets the thing, not how it was made. A real provenance statement that a licence or a policy
    requires is a disclosure, not residue; keep it, in the place the policy names.
42. **Templated filler.** The same sentence repeated per item with one noun swapped ("X provides a
    powerful way to Y" for every feature), or the same boilerplate paragraph across sibling documents.
    Test: remove the noun; if the sentences become identical, none of them carried information.
43. **Re-statement of the title.** The first sentence repeats the heading in prose. Start with the first
    thing the heading did not say.

## 3. Checks a count can settle

These need no judgement, only a look. They are findings on their own, not clusters.

- **Announced count differs from real count.** "Seven tips" followed by six; "three reasons" followed by
  four.
- **A dead column.** A table column that is identical in every row or empty in most.
- **A repeated question.** An FAQ entry whose answer begins by repeating the question's wording, or a
  heading repeated as the first sentence under it.
- **Symmetric pros and cons.** Equal numbers of items, equal lengths, every con softened by a "but".
- **Same sentence per item.** Two or more list items whose text differs only by a noun.
- **Passive concentration.** A paragraph where nearly every sentence is actorless passive (family 10).

## 4. False positives for this file

Mandatory, as in `01-tells.md` §3.

- **A frame that is the content.** "The real question for the migration is whether rollback is possible"
  names a specific question and is a sentence, not family 15.
- **A genuine correction.** "Earlier I wrote that the limit was per user; it is per tenant" is a correction
  with a before and after, not family 20.
- **Quoted or mentioned words.** Scare-quote lookalikes where the word is the subject: the string "null",
  a term of art, a quotation.
- **"Serves as" when it is the function.** "The queue serves as the buffer between the two stages" names a
  role; test by asking whether "is" loses a meaning.
- **Participle phrases that carry a fact** ("returning an empty list when the cache is cold").
- **Legal, licence and standards text**, where "furthermore", "it is important to note" and formal
  transitions are convention.
- **Parallel structure in a procedure or a spec**, where repeated openers are deliberate.
- **A symmetric comparison table** whose rows really are symmetric, because they compare the same
  attributes.
- **Dashes the author uses.** If the user's sample uses them, they stay.

## 5. The register test

Last step of the audit. Read the paragraph as if it were going to one of four places: a social post, a press
release, a school essay, a work memo. If it sounds like any of the first three, find the sentence that gives
it away and fix that sentence; the memo is the target for READMEs, MR descriptions and changelogs. The test
settles registers the lists above leave open, and it needs no list.
