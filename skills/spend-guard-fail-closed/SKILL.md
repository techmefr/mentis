---
name: spend-guard-fail-closed
description: "Use when designing or reviewing a budget, quota or spend limit for agent or model usage (a per-key cap, a free-tier-only rule, a monthly ceiling, a loop that could run up a bill): where the check runs, what it does when it cannot read the numbers, what a displayed cost figure really is, and who is told."
---

# spend-guard-fail-closed

A method for limits on agent and LLM spend. An agent loop, a retry storm or a fallback to a pricier option can
spend faster than anyone reads a dashboard, so the limit has to be a gate that closes by default, not a report
read after the fact. Related: `skills/failure-classification-before-retry` (a budget wall is a failure class of
its own, §1 point 4), `skills/choose-model` (cost per task), `skills/observability-instrumentation`.

## When
- A per-key, per-team, per-agent or monthly spend limit is specified or reviewed.
- A rule says "only free options" or "never exceed X".
- Fallback or routing can send a request to a more expensive path than the one planned.
- Someone quotes a dashboard cost figure as what was or will be billed.

## Steps

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | The gate: fail-closed default, unknown is not safe, check before dispatch, per credential, reasons reported, who is told, estimates versus bills | any spend limit is designed, built or reviewed | [`01-fail-closed-budget-guard.md`](./references/01-fail-closed-budget-guard.md) |

## Output / checkpoint
No pipeline checkpoint. For each limit: where in the call path it is evaluated (before dispatch), what it does
on a missing, stale or contradictory reading, the unit it is scoped to (key, account, agent), the person
notified at each stage, and a test that removes the usage reading and sees the request refused.

## Guardrails
- Never let "could not check" mean "allowed". An unreadable budget blocks the spend or asks a person.
- Never present an estimate as a bill, or a bill as a forecast. Label which each figure is.
- Never raise a limit, add a payment method or move to a pricier option to unblock an agent without a named
  person's decision.
- Never carry another system's thresholds or free-tier facts: they change, so date and source every one.

## Origin
Vendor documentation for spend limits and billing delay (an AI vendor's error reference, a cloud provider's
budget service), read 2026-10-19; the fail-closed candidate rules come from one open-source gateway's
zero-cost-mode document. Provenance, removals and what was not verified:
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
