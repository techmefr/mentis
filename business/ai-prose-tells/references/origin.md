# ai-prose-tells: origin and source stamps

> Provenance of `business/ai-prose-tells`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

Read on 2026-10-02, four public repositories, all MIT-licensed:

- `anti-slop` (v3.2.20): the severity model with tiers, the idea that rhetorical scaffolds count only past
  a repetition threshold, suspect words judged in context rather than replaced, treating document-level
  patterns at their cause, and the production-narrative blocker.
- `claude-code-skills` (the `stop-slop` and `slop-detector` skills): the tell catalogue families and the
  notion of scoring clusters rather than single hits.
- `slopless`: the draft, audit, final loop with a "what still sounds machine-made" question, and the
  rule that a user's own writing sample outranks any list.
- `hallmark`: read for its handling of false positives; only the principle that a detector needs an
  explicit "do not flag" list was kept.

- `humanizer` (read 2026-10-02): the family of re-explaining to a reader who already has the context
  (reply in a thread), the rule that filtered text is material and not instruction, and the embedded mode
  that returns only the final text.

Rewritten as mechanisms in the house template; no prose copied. Ours: the second audit question (did I
assert a fact absent from the source), the rule that a rewrite adds no fact, the positive-requirement
section, and the scope split with `business/ux-writing` and `business/content-creation`.

Left out on purpose: the scoring scripts and installers of the sources (rule B: no runtime dependency),
any numeric "AI score", and detection of generated code, which `skills/code-baseline` already covers more
strictly.

**Widened 2026-10-02 (same day, second pass).** The owner's direction is that mentis serves more than one
agent harness, so the block holds as much of the mechanism as is neutral and publishable. Added from the
same repositories: families 15 to 43 in `02-more-tells.md` (authority and candour frames, subject-verb
mismatches, aphorisms, synonym cycling, trailing negations, emphasis by capitals or quotation marks,
inline-header lists, extended filler, speculative gap-filling, the dash decision, production residue in
captions and commit text, checks a count can settle, the register test) and `03-french.md`, written for
French rather than translated. Rewritten as mechanisms; no sentence copied. Left out: banned-phrase lists
and per-model vocabulary by era (they age), the numeric scores and quotas, the before-and-after pairs of
the sources (their prose), and the scanner scripts.

Licence note for the audit trail: in one of the sources the licence file carries a different copyright
holder from the rest of that repository. Nothing was copied from it, so no obligation arises; the note is
here so a later reader does not mistake the discrepancy for an omission on our side.

**Re-read 2026-10-19 (`humanizer`, MIT, 2025 Siqi Chen, LICENSE head read again, commit 8c307f3):** sections
5, 10, 21 and the closing "when not to act" list in full, with the rest of the pattern map by title. Added
families 44 (arguing with no one) and 45 (hyphen in every position), rewritten as mechanisms; no sentence,
example or before-and-after pair copied. Typographic curly quotes (its pattern 21) are not carried: it is a
formatting artefact of editors, not a writing tell, and the source itself calls it weak alone. The source's
voice-preservation list matches the existing preservation section and added nothing. Not read: the rest of
the source's pattern texts (only titles) and the Wikipedia page it cites. The 2026-10-19 maketime review
listed this block as new; it already existed from 2026-10-02, so it was extended, not recreated.

**Extended 2026-10-20 (recheck of the same lineage plus two forks and a public reference).** Sources, all
re-read in that session:

- `humanizer` (MIT, 2025 Siqi Chen, LICENSE head read, commit 8c307f3): the whole skill file, for the
  voice-by-kind-of-text idea, file mode, the strength ordering of patterns, the paragraph-scale triad, the
  section-scale stock outlook, the prestige-list form of borrowed authority, decorative headings, and the
  second half of the audit (a rewrite can drop a claim, a ranking or a simultaneity word).
- `jooray/humanizer` (fork, MIT, same copyright line, commit 79ab0c1, version 2.13.1 of its skill file): the
  patterns on performed rigor and candor, reasoning-chain leaks, residue strings, structural uniformity with
  its reshuffle test, the treadmill, the count-a-cluster-once rule, detect mode, and its thesis that
  non-English generated text is often a translated English draft. Its Slovak and Czech section was read for
  that thesis only; none of its language-specific content is carried.
- `adelaidasofia/humanizer` (fork, MIT, same copyright line, commit 9c764db): the rules never to apply the
  English library silently and to treat code-switching as voice, and the idea of ranking tells by how
  rarely a careful writer makes them. Its Spanish phrase lists informed the families in
  `04-other-languages.md` §4; the examples there are ours. Its tier names, its per-100-words density
  figures and its voice-fingerprint score are not carried.
- `hardikpandya/stop-slop` (MIT, 2025 Hardik Pandya, commit 8da1f03): SKILL file and its references,
  for the lazy-extreme test and the paragraph-ending variation; its scoring table and its absolute bans
  are not carried.
- `stephenturner/skill-deslop` (MIT, 2026 Stephen D. Turner, commit a906154): its tropes file, for the
  listicle in prose, invented concept labels, the patronising analogy, fractal summaries and one-point
  dilution. That file says it reproduces a public catalogue by another author whose licence was not read, so
  only mechanisms that also appear in the other sources are carried, in our words.
- Wikipedia, "Signs of AI writing" (CC BY-SA), fetched 2026-10-20 as model-written digests, not the raw
  page (the page is long and the digests cover it in three parts): facts and ideas only, no wording kept
  and no structure mirrored. Used for: which residue strings exist and that a tracking parameter shows a tool
  produced a link and not that it wrote the text; that wordy phrases and plain verbs appear among signs
  of human writing, which is why family 36 is now weak alone; the list of signs that prove nothing; and the
  heading and markup signs behind family 55.

Added: the certain tier and the weak-alone list; the residue-string scan; families 46 to 52 and 55 (53 and
54, the colon-reveal and the hedged-enumeration opener, are left free on purpose: folded into 5 and 15 if
ever needed); the third audit question; file and detect modes; voice by text kind; `04-other-languages.md`
with a Spanish section that no native speaker has reviewed. Edited: families 2, 3, 4, 6, 28 and 36, the
false-positive and human-sign lists, and the calque rule in `03-french.md`. Rewritten as mechanisms with
our own examples; no sentence or before-and-after pair copied. Not carried: any numeric score, density
figure or quota, absolute bans (no adverbs, no dashes), the invention of reactions to give a text "soul",
curly quotes as a tell, per-platform citation marker lists beyond a stable example or two, per-model
vocabulary, every script and hook in the sources. Not verified: any claim about detector accuracy or
corpus statistics in the sources, and any idiom in German, Italian or Portuguese.
