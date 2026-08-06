---
name: product-ownership
description: Use when deciding what gets built and in what order, or whether a request should become a story at all — priority, refusal, testable acceptance criteria, definition of ready and done. The story document itself and its estimation belong to the project-management skills; this is the decision around them.
---

# product-ownership

Business layer (`business/README.md`), product. Deliberately thin, because most of this function is
already owned elsewhere and duplicating it would be the bug `skills/maintaining-blocks` §4 exists to
catch.

**Not in scope here — use these instead:**
- **The story document** — its anatomy, its formatting, its Jira fields and labels, reviewing it,
  criticality modes → the `project-management` skills of the `xefi-claude-skills` plugin
  (`story-structure`, `story-analysis-axes`, `story-review-output`, `jira-story-creation`,
  `jira-story-formatting`, `jira-story-modification`, `jira-labels-strict`).
- **Decomposition into tasks and estimation in points** → that plugin's `breakdown` skill, which also
  holds the rule that points require repository access.
- **The technical specification** that follows → `skills/spec`.

What's left, and what this block owns: **whether the thing should exist, in what order, and how anyone
will know it's finished.**

## When
When a request arrives from a customer, a colleague or a stakeholder; when a backlog needs ordering; when
a story is about to be picked up and it isn't clear what "done" means.

## Steps

### 1. A request is not a story yet
1. **Find the problem behind the request.** A request phrased as a feature is a solution somebody already
   chose (`business/sales-support` §1.1); the problem behind it often has a cheaper answer we already
   ship.
2. **Name who has the problem and how often.** "A customer asked" and "every customer hits this weekly"
   produce different decisions, and the difference is usually knowable.
3. **What happens if we don't build it?** If the answer is "nothing much", that's the finding.
4. **Only then does it become a story** — and it gets written with the plugin's `story-structure`, not
   invented ad hoc.

### 2. Order by consequence, not by volume of asking
1. **Rank on the pair (impact, cost)**, where cost comes from an estimate grounded in the code
   (`breakdown`), not from a feeling.
2. **The loudest request is not the most valuable one.** Who asked is data about who asks, not about
   value.
3. **Bugs that lose or corrupt data, and anything with a security or privacy consequence, outrank
   features** — that ordering isn't negotiable (`skills/bug-triage` §3).
4. **Leave room for the work nobody requests**: migrations, debt, upgrades. A backlog that is 100%
   features silently borrows against the next quarter, and the interest arrives as an incident.
5. **Write down what you decided not to do, and why.** Otherwise it's re-litigated monthly, and the
   person who asked assumes it was forgotten rather than declined.

### 3. Saying no is the job
1. **A "no" with a reason keeps the relationship; a silent backlog burial doesn't.** Say which of the
   three it is: not now, not like this, or not ever.
2. **"Not now" carries what would change the answer** — a second customer with the same need, a measured
   cost, a decision that lands first.
3. **Never accept scope in a meeting on behalf of the people who'd build it**
   (`business/sales-support` §2).
4. **Scope moves, quality doesn't.** When a date is fixed, what changes is what's in it — never the tests
   or the review (`WORKFLOW.md` §3).

### 4. Acceptance criteria are a test, or they're decoration
1. **Each criterion must be checkable by someone who didn't write the code**: given this, when that, then
   this observable result. If nobody can verify it, it isn't a criterion.
2. **Criteria are the test cases.** They feed `skills/tdd` and `skills/qa-exploratory-testing` directly,
   which is what makes writing them properly worth the time rather than a formality.
3. **Include the unhappy paths** — the invalid input, the missing permission, the empty state. These are
   where the disagreement about "done" actually happens.
4. **Name what's explicitly out**, so the boundary is a decision rather than an omission discovered at
   review.

### 5. Ready and done, stated once
1. **Ready to start**: the problem is stated, criteria are testable, the unknowns are either answered or
   carved out as a spike, and the dependencies are named.
2. **Done** means merged with the pipeline's guarantees met — gate passed on cited evidence, review
   findings closed (`WORKFLOW.md` §3). Not "the developer says it works".
3. **A story that can't be made ready is split or sent back**, not started hopefully. Starting it converts
   an unanswered question into rework.
4. **Whoever accepts the work isn't the person who built it.** Same reason the gate uses a fresh-context
   judge.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the problem stated separately from the requested
solution, a rank with its reasoning, refusals written down with which kind of "no" they are, acceptance
criteria a third party can check including the unhappy paths, and an explicit ready/done bar. The story
artefact itself is produced with the `project-management` plugin skills.

## Guardrails
- **Never turn a request into a story without the problem behind it.**
- **Never commit scope or a date the people who'd build it haven't seen.**
- **Never trade the tests or the review for a date.**
- **Never leave a criterion nobody can verify** — it guarantees an argument at acceptance.
- **Never re-explain story structure, formatting or estimation here.** Those live in the plugin, they're
  versioned and org-wide, and a second copy would drift.
- Where a company has a product owner or a project manager, they decide; this block structures the
  decision, it doesn't take it.

## Origin
Written **without internal product-management expertise**, and deliberately reduced: an audit of the
installed `xefi-claude-skills` marketplace found nine `project-management` skills already covering the
story artefact, its review axes, its Jira mechanics and its decomposition-plus-estimation, with the
estimation rule that points require reading the code. Duplicating any of that would have created two
sources for one responsibility.

Public sources for what remained: standard discovery-before-solution practice, given/when/then acceptance
criteria, and definition-of-ready/definition-of-done as commonly published. What's ours: the ordering rule
that data-loss and security consequences outrank features, "leave room for the work nobody requests",
naming which of the three kinds of "no" a refusal is, criteria as the direct input to `tdd` and
`qa-exploratory-testing`, and tying "done" to the pipeline's two guarantees rather than to a developer's
say-so. Verified 2026-08-06 against the installed plugin.
