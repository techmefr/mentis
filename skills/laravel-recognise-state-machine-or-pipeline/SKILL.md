---
name: laravel-recognise-state-machine-or-pipeline
description: "Use when a request arrives as \"add a publish button\", \"the status should go back to draft\", or \"add a step that also sends a notification\": recognise the state machine or pipeline underneath before writing the first transition method."
---

# laravel-recognise-state-machine-or-pipeline

Narrow trigger extracted from `skills/laravel-conventions` §1.5, so a status-column or
multi-step-payload request routes here directly instead of only through the whole Laravel block.

## When
A feature request touches a status/state column with named transitions, or an ordered sequence of
steps over one payload that keeps growing a step per requirement (validate, dedupe, enrich, notify).
This never arrives phrased in pattern vocabulary — it arrives as "add a publish button", "the status
should go back to draft", or "it should also send a notification".

## Steps
1. **A status/state column whose values move through named transitions, with a guard or a side
   effect on the move, is a state machine.** Recognise it before writing the first transition method.
2. **An ordered sequence of steps over one payload, growing a step per requirement, is a pipeline.**
   Same recognition, before adding the next `if` to an existing method.
3. **Read `skills/design-patterns` §4 and `skills/domain-modeling`** once either shape is recognised
   — they cover the mechanics; this file only covers the recognition.
4. **A transition's guard has to be evaluated on state reread under a lock, inside the same
   transaction as the write that follows it — never on the in-memory instance a prior `find()`
   loaded.** Two concurrent requests that each load the row before either writes will both pass a
   guard checked against stale data, both perform the write, and both fire the side effect: a
   perfectly correct transition table still races if the decision is made outside the lock that
   protects the write. `ShouldDispatchAfterCommit` on the resulting event delays the dispatch past
   the transaction; it does not deduplicate it, and looks like it might.

## Output / checkpoint
Before the first transition method or the next pipeline step is written, the request has been named
as a state machine or a pipeline (or explicitly ruled out as neither) — not implemented as one more
`if` on an existing status check or method.

## Guardrails
- The whole reason to name this recognition here, rather than trusting the pattern block's own
  triggers, is that the request never arrives already labelled — by the time it looks like a pattern
  in hindsight, the ad-hoc version is already half-built.
- The rest of `skills/laravel-conventions` §1 covers where behaviour lives once the shape is known —
  thin models, concern traits, events over observers.

## Origin
No external source: this is `skills/laravel-conventions` §1.5 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
