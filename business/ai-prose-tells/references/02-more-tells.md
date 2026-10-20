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
    Count it per paragraph, not per document. The same holds one level up: the same closing beat after
    every paragraph or section (a punchy line, a recap) is one tell repeated, however different the words.
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
    the same. This is editorial tightening, not evidence of a machine: wordy phrases of this kind, a
    plain "is" or "has", a qualifier and a flat claim are all things the public reference on the subject
    lists as more common in human writing. Weak alone, cluster only; a lone "in order to" is never
    flagged as machine-made, and tightening it is a style edit offered, not a finding.
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
44. **Arguing with no one.** A sentence that rejects an objection or an option nobody raised: "this is not
    mainly about X", "I am not saying Y", "a tempting approach would be Z, but", "you might think". Usually
    a leftover from an earlier draft, or a rival invented so the real point can win. Test: does the text
    attribute the objection to someone, or would a reader really weigh the rejected option? If not, delete
    the defence and, if it hid a claim, state the claim. Keep an objection that is attributed and answered
    in full, and an option the reader truly faces. Several unrelated rejections in a row are a stronger sign
    than one.
45. **Hyphen in every position.** A compound modifier hyphenated after its noun as well as before it ("the
    plan is long-term", "the process is well-documented"). Test: the hyphen belongs before the noun and is
    usually dropped after; words that are always hyphenated keep it everywhere. Weak alone; only a cluster
    counts, and a house style that hyphenates throughout overrides it.

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
- **Residue strings** (below). These need no cluster: text that exists only because output was pasted
  without a look. Scan for them before the final text is returned, and clean them in the final.
  - *Unfilled placeholders*: a bracketed name, company or title ("[Your Name]", "[insert date]"), a date
    written with letter stubs, a source address written as a placeholder.
  - *Chatbot citation tokens*: markers of the form `contentReference[...]`, `turn0search0`, `oai_citation`,
    `[cite: 1]`, bracketed source ids and similar machine syntax inside prose. Tools change the shape over
    time, so recognise the idea (syntax meant for a renderer, left in the text) rather than a list.
  - *Tracking parameters on links*: a query string such as `utm_source=chatgpt.com` added to an address.
    Strip the parameter. It shows that a tool produced the link, not that it wrote the text.
  - *Invisible characters*: zero-width space or joiner, a soft hyphen, a byte-order mark, stray
    non-breaking spaces where an ordinary one belongs. Normalise to plain text.
  - *Homoglyphs*: a Cyrillic or Greek letter standing in for a Latin one inside a word.
  Legitimate cases the scan leaves alone: the non-breaking space before `:` `;` `!` `?` and inside « » in
  French (`03-french.md` §2), and the same convention in other languages that set it; a zero-width joiner
  inside emoji sequences and in scripts that need it; a soft hyphen in typeset print text; placeholders
  that a template deliberately contains. Check the language and the file kind first, then flag. A text
  that declares its provenance on purpose is a disclosure, not residue (family 41 and
  `business/ai-content-disclosure-and-provenance-pitfalls`).

## 3b. Tiers and weak-alone families

How these families weigh (the table is in `SKILL.md`): certain on one sighting are 38, 49 and the
residue strings; family 4 in `01-tells.md` joins them when the text has no reader to answer. Weak alone,
cluster only: 10, 13, 35, 36, 45, 55. A weak signal that sits on a phrase already flagged by another
family is counted once.

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
- **A caveat that is stated.** "Caveat: the two runs used different context windows" is content; only a
  sentence about where a caveat must sit, with no caveat in it, is family 46.
- **Specific when specifics follow.** "The specific error is ENOSPC" names the error.
- **Real steps.** A numbered procedure, an install, a runbook: "Step 1" there is the content (family 49).
- **Real structure.** Sections of equal length because the content has equal parts; a list of two or of
  five that really has that many; a symmetric comparison table (family 47).
- **A real analogy for a reader who needs one.** A text aimed at non-specialists may explain by comparison
  (family 52).
- **A term the project defines.** A coined label that the project's own documents define and use
  throughout is vocabulary, not family 51.
- **A conclusion the document needs.** A short summary at the head of a long reference is navigation; the
  tell is the same recap at every level (family 50).

## 5. The register test

Last step of the audit. Read the paragraph as if it were going to one of four places: a social post, a press
release, a school essay, a work memo. If it sounds like any of the first three, find the sentence that gives
it away and fix that sentence; the memo is the target for READMEs, MR descriptions and changelogs. The test
settles registers the lists above leave open, and it needs no list.

## 6. Further families, 46 to 55

Same rule as the first section: mechanism and test, no word list. Numbers 53 and 54 are unassigned and
stay free; 55 is placed where the source material put it.

**Announced care, shape and loops**

46. **Performed rigor and candor.** The writer certifies that they are being careful, fair or exact
    instead of being so, in four shapes. A spoken certificate ("it is worth being precise here", "to be
    fair", "the honest version is", "we will not undersell this"). An announced caveat written as a noun
    phrase with no verb ("one caveat that has to sit up front"): the sentence rules on where a caveat goes
    and leaves the caveat for the next one. Asserted specificity: "specific", "particular", "exact" used
    in place of the specifics ("it differs in one specific way"). And a worth-saying certificate
    ("it bears repeating", "worth noting") before or after a claim. Test: delete the announcement; if the
    content stands, the announcement was the whole move, and if nothing is left, the sentence goes. It
    differs from family 16 (a candour opener at one point), from 20 (a staged reaction) and from 36
    (padding): here the writer vouches for their own integrity. A caveat that is stated stays.
47. **Structural uniformity.** Sentences can be clean and the piece still gives itself away by its shape:
    sections of near-identical length, every list the same number of items, a recap closing every
    section. The reshuffle test: swap the second and fourth paragraphs. If nothing breaks, the piece is a
    stack of interchangeable blocks and not a line of reasoning. Fix at the cause: give each section the
    depth its content has, each list the length it really has (two is fine), and cut the closing recap.
    Distinct from 42 (templated filler per item) and from the symmetric-lists check in section 3.
48. **Treadmill.** A long section restates one idea in progressively different words; one metaphor is
    beaten across the whole document; a stack of company or era analogies stands in for an argument; the
    same paragraph appears twice. Test: what does this paragraph add that the one before did not? If the
    answer is "nothing, but louder", merge the two and keep the clearest. Distinct from 26 (one thing
    under three names) and 42 (the same sentence per item): here the idea, not the noun, is what repeats.
49. **Reasoning-chain artifacts.** The writer's working-out has leaked into the text: "let me break this
    down", "first I will look at X, then Y", "step 1", "now that we have established". The writer narrates
    their own procedure as though it were the content. Delete the scaffold and keep the conclusion in the
    author's voice. Keep numbered steps that are the content (an install, a procedure). Distinct from 5
    (announces what the document will do) and from the production-narrative blocker (how the artifact
    was made). Certain tier when the narrated procedure is the writer's own thinking, which matters most
    in agent-written MR descriptions and commit messages.

**Points, labels and teaching voice**

50. **Listicle in prose.** Points dressed as continuous prose: "The first wall is...", "The second wall
    is...", "The second takeaway is...", usually after someone asked for no lists. Its companion is the
    fractal summary: announce, say and recap at every level. Test: replace "first / second / third" with
    bullets; if nothing is lost, it is a list in costume (the mirror of family 34). The signposted
    conclusion ("in conclusion", "to sum up") belongs with 11 (generic conclusion) and 5 (announced
    plans): one marker is a habit; the same move at every level is the tell.
51. **Invented concept labels.** Coined compounds built from a domain word and an abstract problem noun
    (paradox, trap, creep, divide, vacuum, inversion) and used as if established. They name a thing and
    skip the argument. Test: is the term defined, sourced, or used by anyone but this writer? If not,
    say the mechanism in plain words. A term the project defines and uses throughout is vocabulary.
52. **Patronising analogy and invitation to imagine.** "Think of it as...", "imagine a world where...",
    "it's like a...", and the classroom register addressed to an expert ("let's break this down").
    Test: is the analogy clearer than the plain statement, and does this reader need it? An analogy for a
    non-specialist audience is a legitimate tool. Family 5 covers "let's explore"; this is the analogy and
    the imagine-opener.
55. **Heading and markup decoration.** Headings that capitalise every main word in a language whose norm
    is sentence case; unicode arrows used as connectors; a horizontal rule between every section; a
    document that opens with a top-level heading repeating its title; skipped heading levels or several
    top-level headings; a heading written for effect ("The decision, on one screen") instead of naming
    what the section holds ("How the six options compare"). Fix: sentence case where that is the
    language's norm, one title, a rule only where there is a real break, a heading that names its
    content. Weak alone, cluster only. Conventional headings (Installation, Usage, Added, Fixed) are not
    flagged (`01-tells.md` §3); in French, sentence case is the norm and title case is the English-habit
    signal (`03-french.md`, `04-other-languages.md`).
