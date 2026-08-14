---
name: regulatory-watch
description: Use when a regulation, deadline or compliance obligation is about to be stated, relied on, or written into a plan: jurisdiction, primary source, and when a verification has expired.
---

# regulatory-watch

Business layer (`business/README.md`), legal. This block exists because of one property of this domain:
**the facts move, and the wrong version of them is remembered confidently.**

The reference case, and it's recent: the EU AI Act's obligations for high-risk systems were 2 August 2026
in every summary written before mid-2026. An amendment — the "digital omnibus" on AI — deferred standalone
Annex III high-risk obligations to 2 December 2027, and was published in the Official Journal and in force
by mid-2026. Anyone repeating the first date from memory sounds precise and is wrong. The same shape
applies to the French e-invoicing reform, whose scope and dates were reworked more than once before
landing on the September 2026 / September 2027 phasing.

This block doesn't tell you what the law is. It's the discipline for handling a statement about it.

## When
Before writing a regulatory obligation into a document, a plan, an estimate or a customer answer; when a
project enters a new country or sector; when someone says a deadline out loud; periodically, as an audit.

## Steps

### 1. Name the jurisdiction and the scope first
1. **Which country, and which entity.** A group spanning several countries has several answers, and the
   one for the head office is not automatically the one that applies. Consumer versus business changes it
   again.
2. **Sector rules stack on top** of the general ones (public sector, finance, health, energy). Nothing
   about the general regime tells you whether a sector rule applies.
3. **Say the jurisdiction out loud in the answer.** An unqualified statement is read as universal, and
   that's how a French rule gets applied to a Spanish entity.

### 2. Cite a primary source, or say you have none
1. **Primary sources only**: the legislative text, the official journal, the regulator's own guidance.
2. **Law firm and vendor summaries are useful for finding out that something changed**, and are not the
   fact. Their incentive is to publish early.
3. **Content marketing is not a source.** "Guide 2026" pages selling a compliance product are how a
   wrong article number gets copied into a document that a lawyer will later have to defend.
4. **A statement with no source is flagged `[verify]`** and cannot be relied on
   (`skills/source-freshness` §1). "I believe the deadline is X" is a question for counsel, not an input
   to a plan.

### 3. Date everything, and let it expire
1. **Every regulatory statement carries the date it was verified**, and against which source.
2. **Past its window, treat it as unverified**, not as wrong: it needs re-reading before reuse.
3. **A date in the future is the most volatile fact of all.** Compliance deadlines get deferred,
   phased, narrowed and occasionally widened; treat any that hasn't passed as provisional.
4. Same mechanism as version-pinned technical facts — see `skills/source-freshness`, which this block is
   the legal instance of.

### 4. Watch, deliberately and narrowly
1. **Keep a short list of what actually applies to us**, with an owner per item. A watch covering
   everything is a watch nobody reads.
2. **On a change: what moved, does it apply to us, what does it require, by when, who decides.** Those
   five, or it's just news.
3. **Route it to whoever owns the answer** — legal, DPO, security — rather than resolving it in a
   technical channel.
4. **Note the ones that turned out not to apply**, with the reason. Otherwise the same alarm is
   re-investigated every quarter.
5. Automating the sweep is possible and tempting; **an automated summary is a lead, never a conclusion**.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the jurisdiction and scope stated, a primary
source or an explicit `[verify]`, a verification date on every claim, and for each change the five facts
of §4.2 routed to a named owner.

## Guardrails
- **Never state a regulatory deadline from memory.** This is the single most common confident error in
  the domain, and the AI Act example above is what it looks like.
- **Never generalise across countries or entities.**
- **Never present a summary as the law**, however reputable the firm publishing it.
- **Never let compliance urgency drive an engineering decision without the owner confirming it applies.**
  A deadline that turns out not to apply to us has already cost a sprint by then.
- **Non-compliance is not an engineering call to make.** If something looks non-compliant, it goes up the
  same day; deciding to accept a risk belongs to whoever can carry it.
- This block produces **structured questions and dated facts**, never an opinion on whether we comply.

## Origin
The mechanism is Anthropic's `claude-for-legal` suite rewritten: its regulatory-change monitors, its
freshness gate on bundled reference content, and its rule that citations from model knowledge alone are
flagged rather than presented as sourced. Its position that every output is a draft for attorney review
and that "the law in many of these areas is unsettled and evolving" is adopted directly. A community GRC
skill pack covering thirty frameworks was also reviewed: it tracks specific versions and dates carefully,
but has **no update mechanism at all**, which is precisely the gap §3 is aimed at — and a good
illustration that carefully-dated content still rots.

Written **without internal legal expertise**. What's ours: putting jurisdiction before everything else
(a multi-country group has no single answer), the primary-source-or-`[verify]` rule, "unverified rather
than wrong" past the window, and recording the alarms that didn't apply. The two examples are dated
facts, verified 2026-08-06, and are examples of volatility rather than statements of what applies to us.
