---
name: agent-memory-and-state-pitfalls
description: "Use when an agent or assistant keeps anything between sessions (saved facts, preferences, summaries, notes files, a vector store of past conversations, a task state file) and it is designed, reviewed or misbehaves: what may be written and by whom (write gating, provenance, memory poisoning through retrieved or tool content), scoping per user, tenant and project, expiry and contradiction handling, forgetting on request, and the tests that plant a false memory, cross a user boundary and age an entry."
---

# agent-memory-and-state-pitfalls

A defensive block for stored agent memory, the part that outlives the context window. The three sections share one
premise: **a memory is a write that a later run will trust as if the user had just said it, so every write needs a
gate, an owner and an end date**. Degradation inside one long context (lost in the middle, poisoning, clash) and the
write, select, compress and isolate mitigations are in `agent-context-hygiene-pitfalls`; untrusted text reaching a
model is in `llm-app-prompt-injection-and-exfiltration-pitfalls`; personal data in what is stored is in
`llm-pii-and-data-handling-pitfalls`; running limits are in `agent-run-limits-and-guardrail-pitfalls`.

## When
- An agent remembers facts, preferences, decisions or summaries across sessions, or reads a notes or state file at start.
- A store of past conversations is searched to answer new ones.
- An agent behaves strangely "for no reason" and a stored entry may be the cause.
- Two users, tenants or projects share one agent deployment.

## Steps

**Read only the section the task meets.** They are independent; §1 is the entry point for a new memory feature.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | What is written: write gating, provenance, poisoning, what never to store | a memory write path is designed or reviewed | [`01-writes-and-poisoning.md`](./references/01-writes-and-poisoning.md) |
| 2 | Scope, expiry, contradiction, forgetting, size | memory is read back, shared or growing | [`02-scope-expiry-and-forgetting.md`](./references/02-scope-expiry-and-forgetting.md) |
| 3 | Tests: planted memory, boundary crossing, ageing, reset | a memory feature is accepted or a suspicious behaviour is traced | [`03-tests-and-diagnosis.md`](./references/03-tests-and-diagnosis.md) |

## Output / checkpoint
For each kind of memory there is a one-line record: who or what may write it, which sources are barred from
writing it, its scope key (user, tenant, project), its expiry rule and how it is deleted (§1, §2). A planted false
memory, a cross-user read attempt and an aged entry were run against the real store and the observed result is
written down (§3). Diagnosing odd behaviour starts by listing what the run loaded from memory (§3).

## Guardrails
- Never let text from a web page, document, mail or tool result write a memory on its own; require the user's
  statement or an explicit confirmation, and store which one it was (§1).
- Never store a secret, a credential or a raw personal identifier as a memory; store a reference or nothing (§1).
- Never read memory without the scope key in the query; filter by user and tenant before ranking (§2).
- Never keep an entry with no expiry or no owner; give each a review date and the writer's identity (§2).
- Never answer from a stored fact that contradicts the user's current message; the current message wins and the
  old entry is marked superseded (§2).
- Never claim a memory was forgotten before the entry, its embeddings, its summaries and its copies were removed (§2).
- This block is craft guidance written from experience, with no source text read. Nothing was run while writing
  it. See [`references/origin.md`](./references/origin.md).

## Origin
Own craft guidance, no external text taken or read. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
