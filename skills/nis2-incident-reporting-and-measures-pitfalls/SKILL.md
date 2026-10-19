---
name: nis2-incident-reporting-and-measures-pitfalls
description: "Use when an engineering or security/compliance owner prepares for Directive (EU) 2022/2555 (NIS2): the scope question for counsel (essential or important entity), the inventory behind the Article 21 risk-management measures, the records and owners behind the Article 23 incident reporting stages, management-body accountability under Article 20, and the national law that transposes the directive. Not legal advice."
---

# nis2-incident-reporting-and-measures-pitfalls

A method block for the engineering and security side of a directive that bites in three places at once: whether the
organisation is covered at all, a list of measures that must be evidenced, and a reporting clock that starts when the
entity becomes aware of a significant incident. The risks are practical: scope assumed by engineering, measures that
exist but cannot be shown, a clock that starts with nobody owning the filing, and the belief that the directive itself
is the rule when it is transposed into national law. The text read is Articles 2, 3, 20, 21, 23 and 41 of Directive
(EU) 2022/2555 as published in the Official Journal. **Whether the organisation is an essential or important entity,
whether an incident is significant, and what the national law of each member state says were not decided here and are
for counsel.** This block is a working method, not legal advice, and it does not replace a lawyer. Dating and sourcing
a legal statement is in `business/regulatory-watch`; a similar clock for another act is in
`skills/cra-exploited-vulnerability-clock`.

## When
- Someone asks "does NIS2 apply to us" or states a duty, a threshold or a deadline from memory.
- Security measures, an incident process or a supplier review are designed or changed in a possibly covered entity.
- An incident or a near miss occurs and someone asks whether anything must be filed.
- Management asks what it has to approve or learn.

## Steps

**Read only the part the task meets.** Part 1 before anything is planned; the others as the work needs them.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Scope as read (Articles 2, 3), the question list for counsel, and national transposition (Article 41) | a duty is about to be stated or planned, or someone asks whether the directive applies | [`01-scope-and-transposition.md`](./references/01-scope-and-transposition.md) |
| 2 | Management body (Article 20) and the Article 21 measures as an inventory with evidence | measures are inventoried, a gap list is built, or management is briefed | [`02-measures-and-management-body.md`](./references/02-measures-and-management-body.md) |
| 3 | Article 23 reporting stages as read, and the records, owners and escalation to prepare | an incident process, an on-call rota or a reporting template is built, or an incident is live | [`03-reporting-clock-records.md`](./references/03-reporting-clock-records.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). The output is a short readiness note: the scope question put to counsel and
its answer with date and name, the member states concerned and the national law found for each, the measures
inventory with the evidence location per item, the owner who declares awareness and the owner who files (each with a
deputy), where the awareness time is recorded, the channel status, and the date of the last dry run. **Not legal
advice: the note is escalated to counsel before anyone relies on it.**

## Guardrails
- This block does not replace advice from a qualified lawyer; it never states that the organisation is, or is not, an
  essential or important entity, or that an incident is or is not significant. Not legal advice, escalate to counsel.
- State a duty only after reading the article; give no period, threshold or date from memory. The text read is the
  original publication; amendments and the consolidated text were not checked.
- Never present the directive as the operative rule without checking the member-state law; the national text is what
  binds the entity, and this block did not read any.
- Never leave the filing without a named owner and a deputy (part 3, point 4).
- Do not put credentials for a reporting channel in a prompt, a ticket or a repository.
- Do not file, or tell anyone a duty exists, on the strength of this block.

## Origin
Articles 2, 3, 20, 21, 23 and 41 of Directive (EU) 2022/2555 read on EUR-Lex 2026-10-19. Provenance, what was
removed and what was not verified are in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
