---
name: security-questionnaire-answer-pitfalls
description: "Use when answering a customer's security or vendor-risk questionnaire, or building the bank of answers behind it: the position-then-fact shape of an answer, the compensating control for a No or Partial, the three failures (bare No, evasion, bluff), one dated answer bank so the same question never gets two answers, tagging each answer Approved, Drafted or Unknown, keeping contract commitments out of cells, checking live configuration before claiming it, honest incident-response answers, and sign-off before submission."
---

# security-questionnaire-answer-pitfalls

The premise: **a questionnaire cell is a written statement to a counterparty, and the only dangerous answer is
the one you cannot back with evidence the next day.** A bare "No" costs a deal slowly; an invented "Yes" costs
it later, with your credibility attached. For the customer relationship around a questionnaire, read
`business/sales-support`; for the vendor side of the same exercise, `business/vendor-management`; for the
hardening itself, `security-hardening`.

This is an answer-writing discipline, not a compliance programme: nothing here makes anyone certified or
audit-ready, and nothing here is legal advice.

## When
- A questionnaire, a vendor-risk form or a security review request has arrived.
- A bank of reusable security answers is being created or cleaned up.
- A sales colleague wants to paste "the usual answer" into a new form.
- An answer depends on a claim about live configuration nobody has checked recently.

## Steps

**Read only the section the task meets.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The shape of an answer, the four positions, the three failures, the compensating control | writing or reviewing individual answers | [`01-shape-of-an-answer.md`](./references/01-shape-of-an-answer.md) |
| 2 | The answer bank, the three tags, what not to delegate, checks before claiming, incident answers, sign-off | building the bank or running one questionnaire end to end | [`02-bank-and-sign-off.md`](./references/02-bank-and-sign-off.md) |

## Output / checkpoint
Every answer has a position, a checkable fact and, for No or Partial, a compensating control; each carries a
tag (Approved, Drafted, Unknown) and its source (a library entry, or confirmed context, or an open question);
the coverage count equals the question count; contract-shaped questions are routed to whoever owns the
contracts; each claim about live configuration has a check date; the sign-off owner is named. Anything you
could not check is listed as Unknown, not answered.

## Guardrails
- Never answer Yes for something true of one system and not another, and never use Partial as a soft Yes (§1.2).
- Never bluff; a bare No and an evasive paragraph are the lesser failures (§1.3).
- Never write two different answers to the same question (§2.1).
- Never invent a control, a certification or an audit date (§2.2).
- Never let a template or a model answer a contract-shaped question (§2.3).
- Never claim MFA, encryption, retention, access or restore tests from memory (§2.4).
- Never write "I think", "we should have" or "the provider probably" as an answer (§2.4).
- Never submit before the sign-off owner is named and the open items are resolved (§2.6).
- One source here is a young repository maintained by an AI agent that sells a paid kit; its advice is generic
  and unproven, and is kept only where it matches the other source and plain risk hygiene (see
  [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten from a free answer-bank repository (CC0) used as an idea source, and a pre-sales skill's security
questionnaire workflow (MIT), read 2026-10-16. 🟡: never used by us on a real questionnaire; details in
[`references/origin.md`](./references/origin.md).
