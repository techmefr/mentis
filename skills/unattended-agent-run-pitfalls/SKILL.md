---
name: unattended-agent-run-pitfalls
description: "Use when an agent runs on a schedule or a trigger with nobody watching and nobody to approve: designing its run contract (decide and record instead of asking), its per-source bookmark and ledger of reported items, how a failed source is told apart from a quiet one, re-checking live state right before it posts, posting once, a dry run when its store is read-only, the run record written even on a silent day, and what a prompt may and may not carry."
---

# unattended-agent-run-pitfalls

A block for the person who turns an agent into a recurring job: a morning digest, a triage report, a sweep that posts
to a channel. The three sections share one premise: **an unattended run has no one to ask and no one to notice, so
every question it would have asked has to be answered in advance, and every way it can fail has to leave a trace
that the next run and the reader can both read**. The budget and checkpoint side of a loop is in
`agent-run-limits-and-guardrail-pitfalls`; what a loop may remember is in `agent-memory-and-state-pitfalls`; whether
a goal is decidable is in `loop-design`; isolating what the job can reach is in `agent-sandbox-egress-pitfalls`;
a fresh session picking up half-finished work is `handoff`.

## When
- Writing the prompt or the config of an agent that a scheduler or a webhook starts.
- A recurring report is wrong, duplicated, silent when it should not be, or posted twice.
- Deciding where such a job keeps its position, what it already reported and what it did last time.
- Reviewing a job that posts to people or changes something outside its own sandbox.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The run contract: decide and record, who owns which rule, fail closed, credentials, data versus instructions | the job's prompt and permissions are written | [`01-run-contract.md`](./references/01-run-contract.md) |
| 2 | Reading sources and keeping state: one bookmark per source, overlap, ledger, unreadable against quiet, what notes may hold | the job reads something that changes over time | [`02-sources-and-state.md`](./references/02-sources-and-state.md) |
| 3 | Posting: re-verify, assert or drop, one post, ambiguous results, dry run, bookkeeping order, the run record | the job is about to write to the outside world | [`03-verify-and-post.md`](./references/03-verify-and-post.md) |

## Output / checkpoint
The job has a written contract that answers, without a human, what it does when a source fails, when it is unsure
and when its rules cannot be read (§1). Each source has its own bookmark and the reported items are in a ledger the
next run reads (§2). Before anything is posted every item was re-checked against its live source, the post is
idempotent, and a run record exists for every run, quiet or not (§3). One dry run was made and its output read by
a person before the first real post. A job that has only ever run on a good day is not verified.

## Guardrails
- Never leave a path where the run waits for an approval nobody will give; decide in advance and record the
  decision (§1).
- Never treat a source that failed to read as a source with nothing in it; report it as unreadable (§2).
- Never move a bookmark past something that was not read, or past a post that did not land (§2, §3).
- Never post an item whose live state you could not confirm just before posting; assert it or drop it (§3).
- Never put a token or a rule that changes into a prompt; prompts and messages are stored (§1).
- Never run with unreadable preferences and carry on with defaults; stop and say why (§1).
- Restates a public agent sample and craft knowledge; no run was made and no scheduler was involved while writing
  it. Provenance and open points: [`references/origin.md`](./references/origin.md).

## Origin
Rewritten from the daily digest and triage agents of Anthropic's claude-quickstarts (MIT), read 2026-10-20, with
own guidance flagged in the references; scheduler, chat-API and agent-runtime points re-checked on 2026-10-20 against the Kubernetes CronJob page (CC BY 4.0), GitHub workflow-events page (CC BY 4.0), Slack API references and one agent CLI documentation (facts only). 🟡: never run by us.
