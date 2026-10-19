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
