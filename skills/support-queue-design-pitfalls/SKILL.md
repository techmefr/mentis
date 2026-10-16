---
name: support-queue-design-pitfalls
description: "Use when a support or issue queue is being designed, rebuilt or rescued: measuring the queue before changing it, capacity arithmetic against inflow, the first-response promise, the volume-gating trigger, label axes and priority levels, cutting intake, routing security reports out of the public tracker, the per-item decision order, closing and staleness rules, what to automate, reply craft, a published scope of support, and metrics that exclude bots. Covers what changes for a paid support desk compared with open-source maintainers."
---

# support-queue-design-pitfalls

The premise: **a queue is not out of control because its labels are wrong; it is out of control because inflow
exceeds the attention available and no written rule says what happens to the difference.** This block is about
the system around the queue. For sorting one report, read `bug-triage`; for one customer whose problem has
climbed above the usual contact, `customer-escalation-pitfalls`; for many customers hit at once,
`incident-comms-pitfalls`; for writing the help article a repeated question deserves,
`troubleshooting-kb-article-pitfalls`; for the wider account process, `business/customer-success`.

Most of the source is written for open-source maintainers. A paid desk differs in two ways that matter
here: a published response target is often a contractual commitment (so shortening the promise is a contract
change, not a one-line edit), and nobody can be asked to help for free. Each section says where that bites.

## When
- The backlog is growing and someone proposes a new label scheme as the fix.
- A first-response target is about to be published, or has been missed for weeks.
- A stale bot, an auto-greeting or a triage rotation is being added or has caused damage.
- A scope-of-support list or a priority scale is being written.

## Steps

**Read only the section the task meets.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Measuring the queue, capacity arithmetic, the levers, the response target, the volume-gating trigger | the queue is out of control or a promise is being set | [`01-measure-and-capacity.md`](./references/01-measure-and-capacity.md) |
| 2 | Label axes, priority by consequence, cutting intake, security reports, scope of support | labels, forms or the priority scale are being designed | [`02-labels-and-intake.md`](./references/02-labels-and-intake.md) |
| 3 | Per-item order, closing rules, automation limits, reply craft, rejection files, metrics | the daily handling and the closing policy are being written | [`03-handling-and-closing.md`](./references/03-handling-and-closing.md) |

## Output / checkpoint
The baseline numbers and a one-line reading of them; the capacity arithmetic with the lever chosen and written
down; the response target and who it is owed to; the volume-gating trigger; the label axes with one
definition each; the intake cuts in order; the scope-of-support list; the closing policy; the metric list. What
you could not measure is listed as an estimate.

## Guardrails
- Never change the labels before measuring the queue (§1.1).
- Never publish a response target the arithmetic does not support (§1.4).
- Never decide the volume-gating trigger in the middle of a flood (§1.5).
- Never let two labels from the same axis sit on one item, or let automation apply the top priority (§2.1, §2.2).
- Never route a security report through the public tracker (§2.4).
- Never auto-close an item that is waiting on you, or run a first sweep live (§3.2).
- Never let a bot write the first human sentence, or post an agent comment without saying so (§3.3).
- Never count bot replies or self-replies as a first response (§3.5).
- The sources are one maintainer-oriented skill and a few pages of one vendor's public support documentation;
  nothing here was run by us, and the numbers each section mentions are examples, not standards (see
  [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten from samber's OSS issue triage skill (MIT) and GitHub's public documentation on ticket priority and
support scope (CC-BY-4.0, attribution in the origin file), read 2026-10-16. The skill's own numeric targets and
its second-hand case studies were not carried. 🟡: never used by us on a real queue; details in
[`references/origin.md`](./references/origin.md).
