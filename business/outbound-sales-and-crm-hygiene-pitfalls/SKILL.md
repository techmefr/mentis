---
name: outbound-sales-and-crm-hygiene-pitfalls
description: "Use when an outbound sequence is designed or launched, or pipeline data in a CRM is cleaned or reported: stage names nobody defined, a deal that moves forward with no exit evidence, duplicate contacts and accounts merged by the wrong rule, a stale record counted as pipeline, a prospect who replied on one channel and still gets the next touch, an opt-out that lives in one tool only. Stage definitions with entry and exit evidence, dedupe and merge rules, stale-record handling, shared sequence state, reply classification, suppression keyed on every channel. Consent and opt-out as method only, not legal advice."
---

# outbound-sales-and-crm-hygiene-pitfalls

Business layer (`business/README.md`), sales. Outbound goes wrong in two quiet places: the CRM, where a stage means a
different thing to each rep, and the sequence, where nobody owns the shared record of who has already answered or
asked to stop. This block is the check for both. Support-side and in-meeting work is `business/sales-support`;
what happens after the sale is `business/customer-success`; deliverability, authentication and the one-click
unsubscribe mechanics are `business/email-deliverability-and-sender-requirements-pitfalls`; automated flows to
people who already signed up are `business/lifecycle-email-program-design-pitfalls`; defining pipeline and revenue
metrics is `skills/saas-metric-definition-pitfalls`; whether a claim in a message is true is
`business/marketing-claim-substantiation-pitfalls`.

It states method only. It carries no reply-rate benchmark, no cadence length, no response-time target and no
discount or score threshold: the sources gave such figures without a derivation. Consent and opt-out are method,
not legal advice (§4); the person who owns legal decides what a message needs.

## When
- A cold or warm outbound sequence is being written, loaded into a tool or changed.
- Pipeline stages, required fields or routing rules are being defined or audited.
- A CRM export is cleaned, deduplicated, merged or used for a pipeline report.
- A reply, a bounce or an opt-out arrives and the sequence state has to be updated.

## Steps

**Read only the section the task meets.** §1 and §2 for CRM data; §3 for any sequence; §4 before a list is loaded.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Stage definitions: entry and exit evidence, one owner, no skipping, the close-date push, loss reasons | stages are defined, or a pipeline figure is questioned | [`01-stage-definitions.md`](./references/01-stage-definitions.md) |
| 2 | Duplicates, merge rules, survivorship, stale records, the audit that can be repeated | records are merged, imported or counted | [`02-duplicates-and-stale-records.md`](./references/02-duplicates-and-stale-records.md) |
| 3 | Sequence state: one shared record, a reply stops every channel, reply classes, what a person approves | a sequence is built, loaded or paused | [`03-sequence-state-and-replies.md`](./references/03-sequence-state-and-replies.md) |
| 4 | Consent and opt-out as method: source lineage, one suppression list, scope, what to ask legal | a list is bought, scraped, imported or contacted | [`04-consent-and-opt-out-method.md`](./references/04-consent-and-opt-out-method.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a stage table (entry evidence, exit evidence, owner), a
merge rule written before the first merge with the list of records it touched, a sequence-state record that every
tool reads before a touch, and a suppression list with its scope. Legal and consent readings go to the person who
owns legal; stage, scoring and discount decisions go to the sales owner.

## Guardrails
- Define each stage by evidence a second person could check, and name one owner. Never let a stage mean "the rep
  felt good about it" (§1).
- Write the merge rule and the field-survivorship rule before merging, and keep the list of what was merged. Never
  merge on a guess from a name alone or lose the losing record's history (§2).
- Count only records with a recent, real touch as pipeline, and say which are stale. Never report a pipeline total
  that includes records nobody has worked (§2).
- Read the shared sequence state before every touch, and stop all channels when anyone replies. Never run email,
  social and calls from separate lists with no common record (§3).
- Classify every reply and let a person send anything beyond a mechanical stop. Never let automation argue with
  an objection or answer a question it was not given the facts for (§3).
- Keep one suppression list keyed on every channel identifier, applied before every load. Never treat an
  opt-out in one tool as an opt-out in that tool only (§4).
- Record where each contact came from. Never contact a person whose source you cannot state (§4).
- Send the legal question to legal. Never state what a message needs in a country from memory (§4).
- This block is a method written from two young public repositories, never run by us on a real pipeline or
  sequence. Source status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the revenue-operations and cold-outreach notes of an MIT marketing skills repository,
read 2026-10-20, with the one other MIT repository checked for overlap. 🟡: never run by us. Details in
[`references/origin.md`](./references/origin.md).
