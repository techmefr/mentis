# product-ownership — origin and source stamps

> Provenance of `business/product-ownership`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Written **without internal product-management expertise**. Sections 6 to 8 come from **an org skill catalogue
for this function (9 skills: story structure, presentation charter, story creation checklist, story
modification, label discipline, criticality modes, analysis axes, review output shape, decomposition with
estimation)** — rules extracted, de-identified and rewritten generically, with the tracker, MCP tooling,
project keys and info-panel mechanics deliberately left out (rule C). The rule that estimation requires
repository access is theirs and worth keeping verbatim in substance.

**Deepened 2026-08-06.** The first pass wrote this block from the catalogue skills' descriptions. This pass
read the **bodies**, which is where the reasons, the exclusion lists, the carve-outs and the anti-pattern
catalogues live — a description states the rule, a body states when it doesn't apply. What that added here: the
eight sections named individually, "each piece of information appears once", "describe what the user must be
able to do, never the interface", the priority order that stops escalating when the foundations are weak, the
refusal to invent a missing rule, the one-question-at-a-time conversational protocol (rather than handing over
a list), keeping a hypothesis labelled, not balancing a verdict artificially, and small-story-is-not-skipped-
sections. Stamped 2026-08-06.

Public sources for what remained: standard discovery-before-solution practice, given/when/then acceptance
criteria, and definition-of-ready/definition-of-done as commonly published. What's ours: the ordering rule
that data-loss and security consequences outrank features, "leave room for the work nobody requests",
naming which of the three kinds of "no" a refusal is, criteria as the direct input to `tdd` and
`qa-exploratory-testing`, and tying "done" to the pipeline's two guarantees rather than to a developer's
say-so. Verified 2026-08-06 against the installed plugin.

**§8.2–§8.3 and §9 added 2026-09-07.** The catalogue's tenth skill (task decomposition with a hard
confirmation gate before any tracker write) had no equivalent here: §8 covered estimation but not the phase
order, and "the tracker write is a mechanical consequence of an approved plan" is the part that stops an
agent filling a backlog nobody approved. §8.2's one-MR sizing test and §9 come from a real organisational
change rather than from the catalogue: the epic sits with one person and the stories sit with the people who
implement them, who also carry the project-management side of their own work. §9 exists because that
configuration silently removes §7's independent reader, and the honest answer is *what replaces it* — the
epic above and the fresh-context gate below — rather than pretending the separation survives. Its point 3 is
the one that matters in practice: where the implementation is delegated to agents, the story is the brief,
so §6's exclusions and edge cases stop being paperwork.

**Sectioned and deepened 2026-09-08.** The block was a single `SKILL.md` of 2,952 rules words carrying its
nine sections inline — the larger of the two blocks in `CATALOG.md`'s `project-management` row, which at
x4.7 was the worst row in the table after `csharp`. The nine sections moved to one file each under
`references/` with a router table in `SKILL.md`. Every section number and every point number was preserved:
`references/README.md` and `CATALOG.md` both cite §6–§8 as a range, and this block's own sections
cross-reference each other throughout. No section was added — the nine cover the subject — and the depth
went into the mechanism and the consequence behind each rule.

Where the depth went, and why these and not others. The four thin sections (§1 discovery, §2 ordering, §3
refusal, §4 criteria) were thin because the source catalogue does not cover them: its nine skills are all
about the story *artefact*, so everything upstream of the artefact was written from public practice and
stayed at the level of a principle. That is where the additions are:

- **§1**: a request arriving with a date being two separable facts; the person who asked usually not being
  the person with the problem, so the criteria get written for the relay; an existing workaround being the
  measurement already available; counting requests rather than remembering them, because memory
  distinguishes recent from old rather than frequent from rare; a documentation gap getting a
  documentation answer, since building a feature to explain a feature doubles the surface.
- **§2**: ranking one list rather than a series of pairs, because pairwise comparison produces a
  non-transitive order; cost not being build cost; an order that never moves being a queue and one that
  moves weekly being no order at all; bundling being how a small item waits for a big one; a weekly
  emergency being an intake problem rather than a backlog one.
- **§3**: "not like this" owing the alternative; delivering the refusal in the channel the request arrived
  in, since a tracker status is a record and not a message; a reversal saying what changed, so that asking
  repeatedly is not what gets rewarded; an unscheduled yes being a slower no; escalating rather than
  refusing a decision you do not own.
- **§4**: the four words that hide a disagreement ("correctly", "properly", "as expected",
  "user-friendly"); saying *where* the result is observable, since a database row and a line on screen are
  different claims verified by different people; a criterion needing data nobody has not being startable;
  a permission criterion having two halves, because written as one it is satisfied by code that authorises
  everybody; and acceptance happening against the criteria as written rather than against what everyone
  now remembers wanting.

§5 gained the last mile (a flag off, a migration not run, nobody told), the announcement as an output of
done, and the honest handling of a story that is done except for one thing. §6–§8 were already the deepest
and gained the mechanism behind each existing rule plus a few genuinely missing: a dependency being named
with its *state*, the story recording the decision rather than the discussion, reviewing the story against
the code where the code is available, saying what you checked and not only what you found, estimating the
whole of what done means, and a wide estimate being information that a single number throws away. §9 gained
the interval between writing and building as the replacement for the review, the criteria being written
before the implementation is chosen and not touched after, and the point that an agent fills a story's
silence with something plausible where a human developer would have asked.

Router plus sections: 2,952 → 7,616.

**Status.** Still no internal product-management expertise behind the upstream sections, and the catalogue
remains the authority on the artefact. The 🟡 that matters here is that §1–§5 are public practice plus this
repo's own experience, not a source that can be re-checked — which is stated so that a reader knows which
half of the block has a citation behind it.

**Widened against the current AI-assisted-triage trend, 2026-09-09.** Same method as the other widenings
this week — checked against how the practice is actually being done now rather than against the catalogue
— applied to the one genuinely new thing in this domain since the block was written: AI drafting stories
and scoring backlog priority is now common tooling, and the block said nothing about where it fits. Two
points added rather than a new section, because both are the existing argument meeting a faster way to
skip it: §1.13 states that a tool-drafted story is still a draft, not a finding — it answers from the
wording of the request rather than from the person who has the problem, so it cannot stand in for the
interview §1 already requires; §2.13 states that a tool's priority score is an input to the impact half of
the ranking, not the ranking itself, since publishing the score as the order lets §2's loudest-request bias
back in looking objective because a number produced it. Nothing here answers the catalogue comparison a
second time.
