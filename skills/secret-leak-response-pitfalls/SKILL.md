---
name: secret-leak-response-pitfalls
description: "Use when setting up secret scanning (a pre-commit hook, a CI scan, a baseline, an allow comment) or when a credential has been committed, logged or pasted: why a local hook is a convenience and CI the backstop, what scanners miss by default, the response order, and the traps in revoking."
---

# secret-leak-response-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for two moments the existing blocks only touch: setting up the
scanner that is meant to stop a secret reaching history, and answering the day it did. `skills/security-hardening`
§4.6 already says that a committed secret is committed forever and that rotation is the fix, and
`skills/ci-workflow-hardening` §3.5 asks for push protection and a CI backstop; this block is the detail
under both: how a scanner is bypassed or blind, and the order and the traps of the response. The principles
hold with any scanner; the worked ones are gitleaks, detect-secrets, git-secrets and Kingfisher, and their
flag names are version-bound. Choosing a secrets manager and the scanner's detection rules are out of scope.

## When
A diff adds or changes a secret-scanning hook, a CI scan job, a scanner baseline or ignore file, or an
inline allow comment. Also when a credential is found in a repository, a log, a ticket or a chat, or when a
repository is about to become public.

## Steps

**Read only the section the moment needs.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Prevention and detection: hooks, CI, history, baselines, blind spots, allow comments | a scanner is set up, changed or trusted | [`01-hooks-and-scanning.md`](./references/01-hooks-and-scanning.md) |
| 2 | Response: order, validation, revocation, rotation, cleanup, handling the evidence | a credential has leaked or a scan reports an active one | [`02-response.md`](./references/02-response.md) |

## Output / checkpoint
For a scanner setup: where it runs besides the developer's machine, what scope of history it scans, what
the baseline contains and who owns turning it into a rotation list, and which allow mechanisms are
enabled. For a leak: the credential's name (never its value), when it was exposed, what was revoked or
rotated and by whom, the evidence that the old value no longer works, what else held a copy, and the
rescan result.

## Guardrails
- Never treat a local hook as the control; CI or push protection is (§1.1).
- Never paste a leaked value into a ticket, a chat or a prompt, and never pass it on a command line (§2.5).
- Never revoke or validate a credential you are not authorised to act on, and never fall back to ambient
  credentials when revoking (§2.2, §2.8).
- Never record an unknown outcome as a success (§2.7).
- Never remove the line and call the incident closed (§2.6).
- Rotating a production credential is a human decision made with the owner of the workload; the agent
  prepares the checklist.

## Origin
Rewritten from the documentation of gitleaks (MIT), detect-secrets (Apache-2.0), git-secrets
(Apache-2.0) and Kingfisher (Apache-2.0), read 2026-10-15. The full provenance, what was removed and what
is our own guidance are in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
