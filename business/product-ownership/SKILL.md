---
name: product-ownership
description: Use when deciding what gets built and in what order, or whether a request should become a story at all — priority, refusal, testable acceptance criteria, definition of ready and done — and when writing, reviewing or decomposing the story itself, its sections, its criticality, its review axes and its estimation. The technical specification that follows is skills/spec.
---

# product-ownership

Business layer (`business/README.md`), product.

**Relation to an org skill catalogue.** Where a company ships its own project-management skills, they are the
authority on **its** artefacts — its tracker fields, its info-panel presentation charter, its label
taxonomy, its MCP tooling — and override this block on all of that. What's below is the generic form: the
decisions, the story anatomy and the review axes, with no tracker or project named (rule C). The technical
specification that follows a ready story is `skills/spec`; decomposition and estimation are §6 here.

This block owns: **whether the thing should exist, in what order, how it's written down, how it's reviewed,
and how anyone will know it's finished.**

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

### 6. The story document
1. **A complete story has a fixed set of sections**, the same in every project so a reader knows where to
   look: a title that names the business objective with a verb; the context/problem; the user need stated
   from the user's side; the functional rules; the acceptance criteria; what's explicitly out of scope; the
   dependencies and open questions; and the technical or design references.
2. **One presentation charter, applied uniformly.** Which mechanism renders it — panels, headings, a
   template — is the tracker's business, but every story looking the same is what makes a backlog scannable.
3. **Labels are a taxonomy, not free text.** Never create a new label without explicit confirmation, and
   check for an existing one with near-identical spelling first: two labels for one concept splits every
   filter built on it, silently.
4. **Before modifying someone else's story, check the assignee.** If it isn't the person asking, confirm
   explicitly — a rewritten story is someone else's work overwritten.
5. **Never rewrite a description wholesale to "improve" it**: embedded media (screenshots, recordings) is
   lost with the old body, and it's often the only reproduction evidence. Add a comment instead.
6. **One ticket per problem.** Two bugs in one ticket means one of them gets closed without being fixed.

### 7. Reviewing a story
1. **Set the criticality first**, because it decides how deep the review goes: low (UI comfort), medium
   (standard business workflow), high (security, permissions, synchronisation, billing, anything with a data
   or money consequence). Reviewing everything at maximum depth means nothing gets reviewed at all.
2. **Read along fixed axes** rather than freehand, so two reviewers find the same gaps: the business
   objective, the actors and their permissions, the functional rules and their edge cases, the calculation
   rules, the data model impact, the states and transitions, the errors and refused cases, the empty states,
   the volume and performance implications, the external dependencies, the security and personal-data
   consequences, the migration or backfill of existing data, and the testability of each criterion.
3. **The output is structured and the same every time**: what's missing, what's ambiguous, what's
   contradictory, what's out of scope, the questions that block a start, and — where it helps — a rewritten
   version. A verdict with no rewrite forces the writer to guess what would satisfy it.
4. Separate a **blocking** gap (can't start) from an **improvement** (can start). Not doing so makes every
   review read as a refusal.

### 8. Decomposition and estimation
1. Decompose into tasks that each end in something verifiable, not into phases.
2. A task nobody can finish inside a normal working slice is still two tasks.
3. **Estimating without reading the code is a guess with a number on it.** Where the repository isn't
   accessible, say the estimate is unavailable rather than producing a figure that will be held against the
   team.
4. State the unit and keep it stable across the backlog; a re-scaled unit invalidates every past comparison.
5. A bug in work you are currently delivering isn't estimated separately — it's part of that work. A
   pre-existing or third-party bug is estimated like anything else.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the problem stated separately from the requested
solution, a rank with its reasoning, refusals written down with which kind of "no" they are, acceptance
criteria a third party can check including the unhappy paths, an explicit ready/done bar, a story written to
the fixed section set, and — when reviewing — a criticality level, the axes actually read, and blocking gaps
separated from improvements.

## Guardrails
- **Never turn a request into a story without the problem behind it.**
- **Never commit scope or a date the people who'd build it haven't seen.**
- **Never trade the tests or the review for a date.**
- **Never leave a criterion nobody can verify** — it guarantees an argument at acceptance.
- **Never create a label, rewrite a description, or transition someone else's story without confirmation.**
- **Never produce an estimate without having read the code.**
- Where an org catalogue defines the tracker fields, the presentation charter or the label taxonomy, **it
  wins** — this block's §6–§8 are the generic form, not a competing charter.
- Where a company has a product owner or a project manager, they decide; this block structures the
  decision, it doesn't take it.

## Origin
Written **without internal product-management expertise**. Sections 6 to 8 come from **an org skill catalogue
for this function (9 skills: story structure, presentation charter, story creation checklist, story
modification, label discipline, criticality modes, analysis axes, review output shape, decomposition with
estimation)** — rules extracted, de-identified and rewritten generically, with the tracker, MCP tooling,
project keys and info-panel mechanics deliberately left out (rule C). The rule that estimation requires
repository access is theirs and worth keeping verbatim in substance.

Public sources for what remained: standard discovery-before-solution practice, given/when/then acceptance
criteria, and definition-of-ready/definition-of-done as commonly published. What's ours: the ordering rule
that data-loss and security consequences outrank features, "leave room for the work nobody requests",
naming which of the three kinds of "no" a refusal is, criteria as the direct input to `tdd` and
`qa-exploratory-testing`, and tying "done" to the pipeline's two guarantees rather than to a developer's
say-so. Verified 2026-08-06 against the installed plugin.
