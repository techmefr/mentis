---
name: agent-hook-guard-pitfalls
description: "Use when a guard hook for a coding agent is written, reviewed or debugged: how a hook says no (exit code and stderr, deny versus ask, the fields that do not block), the per-guard decision between fail open, fail closed and fail loud, bypass tokens in-band versus out-of-band, protecting the guard's own configuration, append-only ledgers, matcher traps (self-matching process kills, truncating pipes, partial chains, encoding crashes, silent detector breakage) and testing a guard against replayed history before it ships."
---

# agent-hook-guard-pitfalls

A block for the person writing the script that sits between an agent and its tools. The four sections share one
premise: **a guard is code that fails like any code, and the failure that matters is the quiet one, where the
guard stops guarding and nothing says so**. The hooks this repository ships and their honest limits
(block-installs, guard-test-changes, verify-gate, wiring and staleness) are in
[`hooks/README.md`](../../hooks/README.md) on main; this block overlaps it where a guard blocks test edits,
and adds what that page does not: signalling details, failure policy, override design and guard testing.
Isolating the agent is in `agent-sandbox-egress-pitfalls`; which tools to trust is in `agent-mcp-trust-pitfalls`.

## When
- Writing a PreToolUse or similar hook that should refuse an action.
- A guard that "worked" did not stop something, or it blocked everything after an upgrade.
- Adding a way to override a guard, or protecting the guard from the agent it guards.
- Shipping a guard to a team.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Signalling: exit code, stderr, deny versus ask, fields that do not block, headless runs | a hook must refuse an action | [`01-signalling.md`](./references/01-signalling.md) |
| 2 | Failure policy: fail open, closed or loud per guard, crashes, silent breakage | a guard errors or its dependency changes | [`02-failure-policy.md`](./references/02-failure-policy.md) |
| 3 | Overrides and self-protection: in-band versus out-of-band bypass, guarding the guard, ledgers | an override or a protected config is added | [`03-overrides-and-self-protection.md`](./references/03-overrides-and-self-protection.md) |
| 4 | Matcher traps and testing: self-matching kills, truncating pipes, partial chains, replay and test harness | a pattern is written or a guard is released | [`04-matchers-and-testing.md`](./references/04-matchers-and-testing.md) |

## Output / checkpoint
Each guard has a recorded policy (fails open, closed or loud, and why) and a test file that feeds it the
blocked case, the allowed case and a broken input, asserting the exit code and the message (§2, §4). The
pattern was replayed over a real command history and the false positives were counted before release (§4).
A guard that was only read is not verified.

## Guardrails
- Never signal a refusal with a field that does not block; check the exit code path (§1).
- Never copy a fail policy from another guard; decide it for this one (§2).
- Never rely on an override token the agent can write into its own command to stop something that must not
  happen (§3).
- Never leave the guard's own configuration writable by the agent it guards (§3).
- Never write a pattern that matches the guard's own command line (§4).
- Never ship a guard that was not run against replayed history (§4).
- Restates the hook repositories read on the dates in [`references/origin.md`](./references/origin.md); their
  scripts and instruction text were treated as data. No hook was run while writing this.

## Origin
Rewritten from the README and scripts of three hook repositories by independent authors (all MIT) and the
ENGINEERING_LOGS of one of them, read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
