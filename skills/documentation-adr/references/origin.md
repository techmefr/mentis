# documentation-adr — origin and source stamps

> Provenance of `skills/documentation-adr`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Rewrite of the `documentation-and-adrs` skill from a market generalist dev skill catalogue; the ADR
template (six fields) and the "never delete, always supersede" rule are taken as-is, rewritten to
the mentis template. Section 4 comes from a `preserving-productive-tensions` skill in a market skills
repository: the idea that some tensions are load-bearing and shouldn't be resolved is real, but as a
standalone block it had nowhere to attach, so it's reduced here to the one place it changes behaviour —
a `simplify` pass about to collapse a trade-off somebody chose.

**"When" and the Output/Guardrails corrected 2026-08-11** against the real, installed
org catalogue's cross-cutting plugin (`no-project-docs`), read directly: "An architecture decision
record is not automatically an exception. If the user wants one, write it; do not volunteer it."
This block's original phrasing ("as soon as a structural decision is taken... an ADR file created")
had the agent spontaneously committing a new doc file the moment a decision qualified — exactly the
shape of unsolicited documentation the real house policy exists to refuse. The six-field template
and the never-delete-supersede rule are unaffected: they govern what a *written* ADR looks like,
not whether one gets written without being asked.

**Sectioned and deepened 2026-09-08.** The four inline sections moved to one file each under
`references/` and the router became a table of triggers. No section was added. Every section and point
number was preserved: `skills/design-patterns` §5 cites §1.2 and §4, `business/interface-design` §6
cites §4, and this file's own sourcing table cites §4 as where the tensions skill was reduced to.

**What the depth adds.** The original was a template plus three rules, each true and each stated once.
What it did not say is why any of them is load-bearing — and this is a block whose rules are all
ignorable at no immediate cost, since a missing field, a deleted record and an unnamed trade-off all
produce a repo that works today and a reader who is wrong later. The additions that were real absences
rather than elaborations:

- **§1**: that an ADR is its own file because its subject is a *moment* — what was true and what was
  ruled out — and a record kept in a comment gets edited with the code until it describes the present,
  which is the one thing it was not for; that the test for which of the three you are writing is who
  reads it and when; that choosing wrong produces a document nobody will read rather than a filing
  error, since a decision buried in a comment is invisible to exactly the reader about to contradict
  it; that a comment states the constraint and never the intention, because a stale plan is read as a
  commitment; that a comment restating a convention is the copy that will be found and believed; that
  the commit and merge request are the durable half for anything smaller than a decision; and that a
  no-unsolicited-docs policy still needs all three kinds, so nothing goes unrecorded for want of a
  file.
- **§2**: that an indefinite status is the failure mode, because half the codebase follows the decision
  and both halves can cite the file; that the date is what makes every other field readable, since an
  undated constraint is read as current; that the alternatives field is the one dropped for time and
  the one that does the work, because the proposal that returns in six months is almost always one of
  them; that an unfillable field is a finding — no alternatives means the decision was a default; that
  the decision is dated and not the file, so a rewritten record has silently lost what it held; that a
  record titled after a technology cannot be found by someone holding the problem; that saying what the
  decision does *not* cover is what stops it being stretched to justify a shape nobody chose; and that
  it should be written for the person who will have to reverse it, in the order that reader needs.
- **§3**: that both links have to exist and the forward one is the one usually missing — a reader
  arriving at the old record from a citation acts on a reversed decision; that a reversal names *what
  changed*, which is how the next reader judges whether their case falls under the new record or the
  old situation; that a decision taken under a liftable constraint says so, converting a record that
  will look stale into one that is scheduled; that superseding and amending are different operations
  and confusing them either destroys the history or fills it with noise; that an abandoned decision
  still needs a status or it reads as binding; that moving a superseded record breaks every citation;
  and that an ADR contradicted by the code is a live defect, because after one silent drift no reader
  can rely on any record without checking.
- **§4**: the asymmetry the whole section rests on — the cost is readable in the code and the benefit
  is readable nowhere, so a reader comparing what they see against nothing concludes correctly from the
  available evidence and removes it; that the consequence has to be named concretely enough to be
  checked against somebody's own change; that saying what would *end* the tension turns a rule with no
  exit into one that can be retired deliberately; that a tension held without being named is
  indistinguishable from an accident, which is why the sentence also belongs at the duplication itself;
  and that this section is never a way to protect a decision from being questioned, the test being
  whether the sentence can be checked.

Router plus sections: 841 → 2,909.

**Status.** The sources are unchanged. The 2026-08-11 correction against the real house documentation
policy still holds and this pass did not touch it: the block still proposes rather than volunteers, and
the depth is about what a *written* record owes. The depth is ours, written from what goes wrong between
a decision and the reader who has to live with it.
