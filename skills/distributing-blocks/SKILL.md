---
name: distributing-blocks
description: Use when someone outside this repo wants to install these blocks, or an existing user needs a newer version: the install and update mechanism, and the boundary that keeps their customisations alive.
---

# distributing-blocks

Cross-cutting (`WORKFLOW.md` §2). Rule B says nobody upstream may break our workflow. The moment this
framework is installed by other people, **we are that upstream for them**. This block is how we hold
our own rule from the other side.

The mechanism is deliberately boring: git. Not a package manager, not an auto-updater.

## When
When a new team installs the blocks, when an existing user needs a newer version, or when deciding
whether something we wrote should be shared at all.

## Steps

### 1. Decide what is even shareable
Before distribution, per block:

- **Share** when it's generic, useful beyond one team, and its `Origin` is honest.
- **Keep private** when it is: specific to one project or one organisation's internals, calibrated on
  a **named person's** habits, experimental, or carrying anything sensitive.

That last case is not hypothetical: blocks have already been kept out of this repo for it. A block
built around one colleague's review behaviour is useful locally and indefensible shared. When the
*mechanism* is worth keeping, extract it generically and leave the calibration at home — that's how
the triage step in `review` survived while the agent implementing it stayed private.

### 2. Install: a clone they own
1. The consumer **clones** the repo (or forks it). They own that working copy: it's a git repo, with
   their name on the commits.
2. Blocks are copied into the target repo's `.claude/skills/` and `.claude/agents/`, or symlinked from
   the clone. Nothing is fetched at runtime — rule B applies to them too.
3. Executable pieces (`hooks/`) are wired per repo, deliberately, by a human reading what they do.

### 3. Update: they pull, we don't push
1. **Stash or commit local work first.** An update that starts on a dirty tree is how someone loses an
   afternoon.
2. **Fetch, then merge.** Fast-forward if their copy hasn't diverged, an ordinary merge if it has.
3. **Conflicts are shown to the human, with both sides explained**, and resolved by them. Never
   resolved silently in favour of upstream: a conflict means the two of us changed the same rule, and
   ours isn't automatically right for their repo.
4. **Restore the stashed work**, then confirm the block list still loads.

Their customisations are **commits**, so they survive the merge by construction. This is the whole
reason for using git rather than a copy-over installer: we don't need a folder convention separating
"our blocks" from "their overrides", because version control already models it.

### 4. Version, so pinning is possible
1. Tag releases and keep a changelog of what changed per block, so a consumer can read before merging
   rather than after.
2. A consumer must be able to **stay on an older version deliberately**. "Everyone is always on
   latest" is the property that lets an upstream break people.

## Output / checkpoint
For a new consumer: a clone they own, blocks installed, hooks wired knowingly. For an update: the
merge done, conflicts resolved by a human, local work restored, block list verified.

## Guardrails
- **Never a silent auto-update.** An update that rewrites someone's agents without them reading it is
  exactly what rule B forbids others from doing to us. Pull, not push.
- **Never resolve a conflict for them.** Surface both versions; the decision is theirs.
- **Don't share a block that has never been tested.** Distributing something never run once spends
  the credibility of the first colleagues who try it, and that's the hardest credit to win back. Use
  `testing-blocks` at minimum; real use is better.
- The decision to publish more widely (outside the company, under a licence) is **a human decision**,
  out of scope for any agent.

## Origin
Rewrite of `pulling-updates-from-skills-repository` and `sharing-skills` from a market skills
repository (the companion repo of the upstream this framework responds to). The git-based
pull-and-merge flow, the stash-first ordering and the share-vs-keep-private criteria come from there.

What's ours: framing the whole thing as rule B applied in the reverse direction, the requirement that
pinning an older version be possible, and the observation that git already provides the
ours-vs-theirs boundary, which had been flagged in the README roadmap as an unsolved design problem
needing a folder convention. It didn't.
