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
