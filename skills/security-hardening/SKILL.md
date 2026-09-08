---
name: security-hardening
description: Use when writing code that crosses a trust boundary (user input reaching a query or a template, a file upload, a new endpoint, an outbound call with a user-supplied target). The writing counterpart to the seraph agent.
---

# security-hardening

Step 6 of the pipeline (`WORKFLOW.md`). The distinction that keeps this block from duplicating
others: `seraph` **audits** a repo after the fact, `auth-session-conventions` owns **auth**, and this
block is what you apply **while writing** the code, on every other trust boundary. Every rule below
holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A).

A trust boundary is any point where data you don't control meets something that acts on it: a query,
a template, a filesystem path, a shell command, an HTTP call, a deserialiser.

**Applying an override is silent.** Where an org catalogue or a platform policy governs a rule here,
write what it requires and move on — never report "a conflict between mentis and the house rules" to
whoever's watching. Surface it as a specific, named question only when no rule anywhere resolves the
case.

## When
As soon as a diff has user-controlled data reaching one of those, adds a file upload, adds an
endpoint, or brings in a new dependency. Not as a generic pass over untouched code: that's `seraph`'s
job, on demand.

## Steps

**Read only the sections the boundary actually is.** The rules live one file per section under
`references/`; §1 and §2 are the two halves of a data path, §3 is any new entry point, §4 is uploads,
secrets and dependencies, and §5 is what you owe before calling it done.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Input: validate at the edge, on a whitelist | data you don't control enters | [`01-input.md`](./references/01-input.md) |
| 2 | Output: escaping depends on the destination | a value reaches a query, template, shell, path or outbound call | [`02-output.md`](./references/02-output.md) |
| 3 | Access control on every new route | an endpoint, consumer, job or webhook is added or changed | [`03-access-control.md`](./references/03-access-control.md) |
| 4 | Files, secrets and dependencies | an upload, a secret, or a new dependency | [`04-files-secrets-deps.md`](./references/04-files-secrets-deps.md) |
| 5 | Verification | before claiming the boundary is done | [`05-verification.md`](./references/05-verification.md) |

## Output / checkpoint
For each boundary the diff introduces: where validation happens, what the whitelist is, how output is
escaped, and the authorisation applied. The hostile-value and wrong-user replays observed, with
evidence, not reasoned about (§5.3).

## Guardrails
- **Never weaken a check to make something work** (§1.5). If a guard blocks a legitimate case, the
  whitelist is wrong: widen it deliberately, don't remove it.
- **Never disable escaping to fix a display bug** (§2.12). Fix the data or sanitise it.
- **Never build a query, a command or a path by concatenation** (§2.1, §2.3, §2.7).
- **Never ship an entry point with no authorisation declaration**, and never rely on the habit rather
  than a default-deny (§3.1, §3.5).
- Never test an injection against a shared or production environment: hostile-value replays belong in
  local or preview environments (§5.8 — that boundary is `seraph`'s rule too, and it applies to writing
  code just as much as to auditing it).
- Scope: this block covers application code. Platform hardening (TLS, WAF, network policy, IdP
  configuration) is infra reality and stays outside this repo.

## Origin
A rewrite of a market generalist catalogue's `security-and-hardening` idea, against OWASP (Top 10,
ASVS) and OWASP's escaping cheat sheets. The full provenance, the split with `seraph` and
`auth-session-conventions`, the 2026-08-10 OWASP coverage check and the refresh log are in
[`references/origin.md`](./references/origin.md).
