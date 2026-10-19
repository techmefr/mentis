---
name: symfony-conventions
description: "Use when writing or reviewing a Symfony application: services and configuration, thin controllers, forms and validation, firewall and voters, login protection, deployment steps and message workers."
paths: "**/src/Controller/**/*.php, **/src/Security/**/*.php, **/src/Form/**/*.php, **/config/packages/*.yaml, **/config/services*.yaml, **/config/routes*.yaml, **/templates/**/*.twig, **/.env, **/.env.*"
---

# symfony-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Symfony code, on top of
`skills/php-patterns` (the language). Every rule below holds in a repo with **nothing installed**
(`CONVENTIONS.md`, rule A). **Special status**: like `go-conventions`, no in-house production experience sits
behind this block yet, and its main source is under a share-alike licence, so the rules are the ideas
restated in the house voice, with no wording reused (`CONVENTIONS.md`, rule B). The content comes from the
Symfony documentation as read on 2026-10-02 (the framework's own best-practices article, the security,
deployment and messenger chapters); treat it as a base to confront with the first real Symfony project, not as
proven doctrine. The documentation tracks the current release at read time and its version was not recorded;
check names against the installed major.

## When
As soon as Symfony code or configuration is written or modified, during `code` (6) or `tdd` (5): a service, a
controller, a form, a security rule, a configuration file, a message handler, a deployment script.

## Steps

**Read only the sections the task touches.** One file per section under `references/`.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Structure, services, configuration, controllers, forms, templates, tests | a service, a parameter, an environment value, a controller, a form or a test is written | [`01-structure-controllers-forms.md`](./references/01-structure-controllers-forms.md) |
| 2 | Security, deployment, workers | a firewall, a voter, a login form, a release step or a message consumer is touched | [`02-security-deploy-workers.md`](./references/02-security-deploy-workers.md) |

## Output / checkpoint
Code compliant with the sections read; the project's static checks and tests green; no secret in a tracked file;
the access-control list read top to bottom with the new rule in its intended place. Checked by `gate` (7) and
`review` (8). Where the project cannot run its toolchain (no environment), the checkpoint records it rather than
reporting a pass, and nothing is installed to make it run (`CONVENTIONS.md`: a block names a dependency and
stops).

## Guardrails
No comments in the code produced. These rules govern **new** code. The structure rules are the framework
authors' preferences, not laws: a project with its own established layering keeps it, and what this block insists
on is one place per rule. Never loosen a security rule or a validation to get a diff through. For the error body
shape and idempotency, `skills/api-design`; for queues generally, `skills/background-jobs-conventions`; for
authentication and sessions, `skills/auth-session-conventions`.

## Origin
Ideas restated from the Symfony documentation (share-alike licence, so no wording reused); the full provenance
and the audit of what was left out are in [`references/origin.md`](./references/origin.md). Read it when
checking a rule's freshness, not when applying one.
