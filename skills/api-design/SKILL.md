---
name: api-design
description: "Use when designing a new API or interface (REST, tRPC, GraphQL) before implementing it: contract-first, Hyrum's law, extension rather than breakage."
---

# api-design

Step 3 of the pipeline (`WORKFLOW.md`, between `archi` and `plan`), when the task is designing an
interface consumed by others (frontend, third-party service, another team): not for an internal
function with no public contract. Every rule below holds in a repo with **nothing installed**
(`CONVENTIONS.md`, rule A).

**Applying an override is silent.** Where an org catalogue or a house API convention governs a rule
here, write what it requires and move on — never report "a conflict between mentis and the house rules"
to whoever's watching. Surface it as a specific, named question only when no rule anywhere resolves the
case.

## When
Before implementing a new endpoint/route/procedure: never after the fact by "documenting what
already exists" (by then it's too late to steer the design).

## Steps

**Read only the section the task actually needs.** The rules live one file per section under
`references/`; §1 is a new contract, §2 is what the contract exposes, §3 is any change to one that
already ships.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Contract-first | designing a new endpoint, route or procedure | [`01-contract-first.md`](./references/01-contract-first.md) |
| 2 | Hyrum's law: whatever is observable will be depended on | deciding what an interface exposes | [`02-hyrums-law.md`](./references/02-hyrums-law.md) |
| 3 | Extension rather than breakage | an existing contract has to change | [`03-extension.md`](./references/03-extension.md) |

## Output / checkpoint
Final verification checklist cleared before shipping the contract: pagination consistent with the
rest of the API, backwards compatibility verified against the previous contract rather than from
memory (§3.9), error format compliant with the system-wide standard, no internal field exposed without
reason.

## Guardrails
No over-engineering of the contract for a hypothetical need nobody asked for (§1.11): the contract
covers the real need, extensible later if required, not pre-generalised. An incompatible change never
slips quietly into a "minor" evolution: a rename (§3.6 here) and a change of a field's *meaning*
(§3.8 here) are both incompatible even though neither looks it, and both go explicitly through
`deprecation-migration` (its §3.2). **Never expose an internal field because it's handy** (§2.2) — it is
permanent from the first integration.

## Origin
A rewrite of a market generalist catalogue's `api-and-interface-design` skill. The full provenance and
the refresh log are in [`references/origin.md`](./references/origin.md).
