---
name: maintaining-blocks
description: "Use when auditing this framework's own corpus, after renaming or removing a block or agent, before a release others will pull, or periodically: dangling references, stale claims, drift."
---

# maintaining-blocks

Cross-cutting (`WORKFLOW.md` §2), applied to this repo rather than to a product. A corpus of blocks
rots in a specific way: nothing errors. A skill can point at a file that doesn't exist and still read
perfectly, and the only symptom is an agent following a reference into nothing mid-task.

Every check below exists because it already failed here once.

## When
After renaming, removing or splitting a block or an agent; before tagging a version other people will
pull (`distributing-blocks` §4); otherwise periodically, when nothing else is pressing.

## Steps

### 1. Resolve every cross-reference
1. Collect the references: block paths under `skills/` and `business/`, agent names, `WORKFLOW.md`
   sections, `hooks/` scripts.
   Watch out for one false positive: `Origin` sections quote **paths inside other people's repos**,
   which look exactly like ours. Those must not resolve locally, and must not be "fixed".
2. **Check each target exists.** A block cited by thirty others and never written reads as authoritative
   precisely because so many things point at it.
3. **Check section numbers still exist**, not just files — sections get renumbered when a block grows.
   This one is mechanical, so it should be a script rather than a reading: `bin/check_citations.py` here,
   stdlib only, in the pre-push suite since 2026-09-09.
4. A reference to something intentionally absent (kept private, not written yet) must **say so at the
   reference**, not just in a catalogue.
5. **Write a citation so that it can be attributed on its own.** A `§N.M` carries no block name, so a
   reader — and any check — takes the nearest block named before it on the line: a bare number after
   another block has been mentioned reads as *that* block's section, whether or not it was meant that
   way. Name the block immediately before the citation, or mark the citation local by writing *here*
   after it, and be most careful in an `Origin` section listing who cites what — the natural phrasing
   there, a backquoted block name followed by a number, states the reverse of what it means. Measured on
   this repo on 2026-09-09: of 1,260 citations, ten did not resolve, and eight of those were this shape
   rather than a genuinely missing section — which is also why point 3 had never actually been run. A
   second implementation of the same check, stricter about attribution, found four more of this shape and
   nothing else.

### 2. After a rename, check what else the name meant
1. Rename by tracked file (`git mv`, then a substitution over `git ls-files`), never a blind
   recursive replace.
2. **Then read the diff.** A blind rename rewrites the name everywhere it appears, including where it
   referred to somebody else's work — a market catalogue entry, an `Origin` line, a quoted example. That
   corrupts the sourcing record silently, and sourcing is the only thing making rule B checkable.
3. Resync wherever blocks are installed (`~/.claude/`), and **move superseded copies aside rather than
   deleting them**, so a stale local copy can't shadow the current one and can still be inspected.

### 3. Keep the maturity claims true
1. Statuses (`CATALOG.md`) are a claim about reality: ✅ rewritten, 🟢 used in real production work, 🟡
   written but never run, 🔜 to wire, 🔎 to mine, ✕ ruled out.
2. **A block that has never been executed is 🟡, however carefully it was written.** Promoting it because
   it reads well is the same error as `passes: true` with no test output.
3. **Removing a block means removing its row and its references**, not leaving a row that claims a status
   for a file nobody can open.
4. **A ✕ keeps its reason.** Without it, the same idea gets re-sourced and re-litigated in six months.

### 4. Deduplication and retirement
1. Search the corpus for the same rule stated in two blocks. Overlap is normal at the edges; the same
   *responsibility* in two places means one of them is wrong and nobody knows which.
2. When two blocks converge, **merge into one and delete the other** — don't leave a stub pointing
   sideways.
3. **Retire a block that has been available and unused.** A corpus nobody can hold in their head gets
   ignored wholesale, which costs more than the missing block did.
4. Every merge or retirement is recorded in `Origin` or the catalogue, so the idea can be found again.

## Output / checkpoint
Every reference resolves; no rename has touched text about somebody else's work; statuses match what
has actually been run; no two blocks own the same responsibility. Anything failing is either fixed in
the same pass or written down as a known gap — not left implied.

## Guardrails
- **Never fix a dangling reference by deleting the reference** when the referenced thing should exist.
  The missing block is the finding; the pointer was right.
- **Never upgrade a maturity status to make the catalogue look finished.**
- Don't rewrite `Origin` sections to be tidier. They're the audit trail for rule B, and an
  approximation there is indistinguishable from taking credit.
- This block audits the corpus; it does not rewrite the blocks' content. A rule that looks wrong goes
  to a human.

## Origin
The idea of treating a skills corpus as something needing deliberate upkeep comes from a
`gardening-skills-wiki` skill in a market skills repository (the companion repo of the upstream this
framework responds to); what it prescribes — pruning, deduplicating, keeping an index true — is generic
and rewritten here.

What's ours is every specific check, because each is a bug this repo actually had: a `WORKFLOW.md`
cited by 32 blocks that had never existed, a `review` step routing to an agent with no file in the repo,
a catalogue claiming ✅ for agents that had been removed, and a nine-agent rename whose substitution
also rewrote two market-catalogue entries about other people's agents.
