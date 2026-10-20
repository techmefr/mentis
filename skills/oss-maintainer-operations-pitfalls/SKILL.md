---
name: oss-maintainer-operations-pitfalls
description: "Use when you run or help run a public open-source project and the work is the upkeep, not the code: an issue queue nobody triages, a contribution that does not fit, a stale thread, a request for commit access, a project that depends on one person, a contributor who has gone quiet, bot noise, or a maintainer near burnout: written expectations, scope and the polite no, triage and stale handling, roles and governance, bus factor, automation, and the signals worth watching."
---

# oss-maintainer-operations-pitfalls

The social and operational side of keeping a public project alive. The usual failures: expectations that live in the
maintainer's head so every contributor guesses, a queue that grows until a real report is lost in it, a "no" that
turns into a quarrel because the scope was never written down, a project that stops when one person does, and a
maintainer who absorbs every demand until they leave. The three sections share one premise: **an open-source
project fails through unwritten rules and unshared load, not through lack of code**. The block owns no forge, bot
or metrics tool and names none as a requirement.

It stops short of the neighbouring blocks. Receiving a vulnerability report, the embargo and the advisory are in
`skills/security-advisory-comms-pitfalls`. The licence and compliance questions are in
`skills/oss-compliance-programme`. How a reviewer comments on a change is in `skills/code-review-reviewer-pitfalls`.
Release notes and changelogs are in `skills/release-changelog-pitfalls`.

## When
- A repository is made public, or an existing one starts to receive outside contributions.
- The issue or pull request queue has grown past what the maintainers read.
- A contribution does not fit the project, or a request for access or a new role arrives.
- Only one person can release, review or administer the project.
- A maintainer is tired, or a contributor disappears mid-change.

**Skip when** the project is private or has no outside contributors. For a public personal repository with one maintainer, the checks that assume an organisation (a second administrator, a vote) are replaced by the one-person variants of §2.12; a check that needs data or settings you cannot read (issue queue size, branch protection, multi-factor status, the list of administrators) is reported as "unverifiable" with the page or query that settles it (§2.13), never guessed, and a point that does not fit is reported as "not applicable: reason".

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Written expectations, scope, the polite no, triage, stale items, response promises | the queue grows or a contribution does not fit | [`01-expectations-scope-and-triage.md`](./references/01-expectations-scope-and-triage.md) |
| 2 | Roles, commit access, governance, bus factor, company contributors, backup administrators | someone asks for access, or the project depends on one person | [`02-roles-governance-and-continuity.md`](./references/02-roles-governance-and-continuity.md) |
| 3 | Automation that earns its place, signals to watch, repository safeguards, burnout and pausing | tooling is chosen, health is reviewed, or a maintainer is overloaded | [`03-automation-signals-and-sustainability.md`](./references/03-automation-signals-and-sustainability.md) |

## Output / checkpoint
No pipeline checkpoint. For a project: a short public file set (vision or scope, how to contribute, who decides, how
to reach the security contact) that a stranger can act on without asking, a triage routine with an owner and a
cadence, at least two people able to release and to administer, and a written pause or hand-over path.

## Guardrails
- Write the scope and the process down before enforcing them. Never close a contribution for a rule that exists
  only in someone's head; point to the sentence, or write the sentence first (§1.1, §1.3).
- Give every "no" a reason, a thanks and a next step. Never close with silence or with only the word "no" (§1.5).
- Keep the decisions in public threads. Never settle something in a private message that other contributors
  will need to find (§1.4).
- Name more than one person for every critical power: release, merge, administer, security contact. Never let a
  single account hold the whole project (§2.4).
- Spread access by demonstrated responsibility, written down as a path anyone can follow. Never hand out or
  withhold it by favour (§2.2, §2.3).
- Automate the dull checks first and keep a person for the judgement. Never let a bot close a human's report
  without a written, visible rule (§3.2).
- A maintainer may pause, narrow the scope or hand over. Never present exhaustion as a virtue 
  (§3.8).
- This block restates one published guide for maintainers and sets no numeric target: choose reply windows,
  triage cadences and stale delays from your own capacity. Nothing was run while writing it.

## Origin
Rewritten from the maintainer, governance, metrics and security chapters of the Open Source Guides (GitHub, CC BY
4.0), read 2026-10-20, plus own guidance flagged in the references. Provenance, what was removed and not verified:
[`references/origin.md`](./references/origin.md). 🟡: never dogfooded.
