---
name: llm-pii-and-data-handling-pitfalls
description: "Use when personal or confidential data may reach a model provider or stay behind in an LLM application: deciding what is sent in a prompt (data minimisation, redaction with reversible placeholders and their limits), what is kept (prompt and completion logs, caches, embeddings, fine-tuning sets, vendor retention and training terms), who can read it (tenant isolation, permission-aware context), how deletion requests reach every copy, and the tests that prove it. Not legal advice."
---

# llm-pii-and-data-handling-pitfalls

A defensive block for the data path of a model-backed feature. The three sections share one premise: **every
prompt is a copy of the data in a third place, and every copy has a retention, a reader and a deletion path that
someone has to own**. Telemetry backends are in `telemetry-sensitive-data-pitfalls`; transfers outside a region
and breach duties are in `gdpr-international-transfers-pitfalls` and `gdpr-breach-notification-and-dpia-pitfalls`;
the stored memory of an agent is in `agent-memory-and-state-pitfalls`; injection and exfiltration through output is
in `llm-app-prompt-injection-and-exfiltration-pitfalls`; the legal status of the AI feature is in
`ai-act-obligations-and-omnibus-status-pitfalls`. This block is method, **not legal advice**; a lawyer or the data
protection officer decides what is lawful.

## When
- A feature sends user, customer, employee or patient text, files or tool results to a hosted model.
- Prompts and completions are logged, cached, embedded, replayed in evaluations or used to tune a model.
- Choosing a provider, or checking a provider's retention and training terms.
- A person asks to see or erase their data and an LLM feature touched it.

## Steps

**Read only the section the task meets.** They are independent; §1 is the entry point for a new feature.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Before sending: minimisation, redaction and placeholders, detection limits | a prompt is assembled from data about people | [`01-before-sending.md`](./references/01-before-sending.md) |
| 2 | After sending: logs, caches, embeddings, tuning sets, vendor terms, deletion | data is kept, shared with a vendor or erased | [`02-after-sending.md`](./references/02-after-sending.md) |
| 3 | Reading and proof: tenant isolation, permission-aware context, output scanning, tests | several users share a deployment, or the design is accepted | [`03-isolation-and-proof.md`](./references/03-isolation-and-proof.md) |

## Output / checkpoint
A data-flow table lists every place a prompt or completion (or something derived from it) lands: provider, log,
cache, vector store, evaluation set, tuning set, backup. Each row has a content class, a retention, a reader and
a deletion method (§2). A redaction step, if used, has a stated list of what it misses (§1). A seeded-identifier
test shows where the planted value does and does not appear (§3).

## Guardrails
- Never send a field the task does not need; drop it or pass a placeholder (§1).
- Never call a detector's output a guarantee; list its misses, test it on your own data and keep a second control (§1).
- Never log full prompts and completions by default; log ids and sizes, and gate full capture by a short-lived,
  access-controlled switch (§2).
- Never assume a provider's retention or training terms; read them for the tier and endpoint in use and record the
  date (§2).
- Never put another user's or tenant's data in a context; filter by the caller's rights before retrieval (§3).
- Never report a deletion done before every row of the data-flow table was handled (§2).
- This block is idea-level guidance from the source in [`references/origin.md`](./references/origin.md), read on the
  date there, plus own guidance. Nothing was run. Not legal advice.

## Origin
Rewritten at idea level from the documentation of llm-guard (MIT), read 2026-10-20, plus craft knowledge marked
"own guidance". 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
