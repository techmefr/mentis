---
name: angular-conventions
description: "Use when writing or reviewing Angular: standalone components, signals and resources, templates and control flow, injection, HTTP interceptors, routing and guards, error handling, the built-in security model, change detection and lazy loading, and unit tests."
paths: "**/*.component.ts, **/*.component.html, **/*.service.ts, **/*.routes.ts, **/app.config.ts, **/angular.json, **/*.directive.ts, **/*.pipe.ts"
---

# angular-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Angular application code. **Status:
a base to confront with real work.** No in-house Angular project stands behind it yet, the same status as
`go-conventions`: every rule below was read in the framework's own documentation and style guide
(stamped, version pinned: Angular 22, read 2026-10-02, see `references/origin.md`), none comes from our own
review feedback. Treat a rule that disagrees with a real project as a defect of this block, and fix the block.

The framework moves fast and each major reverses defaults (zoneless and `OnPush` became defaults, the
decorator inputs and `NgModule` became legacy, Signal Forms became stable). Before judging code against a rule,
read the version in `package.json`: a rule marked `v22+` does not describe a v19 project, and a v19 idiom is
not a defect there. Where a rule depends on the major, the rule says so.

## When
As soon as a component, directive, pipe, service, route table, interceptor, guard or Angular test is written or
modified, during `code` (6) or `tdd` (5).

## Steps

**Read only the sections the task touches.** One file per section under `references/`; a section read is a
section that has to be applied.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Structure, naming and files | a file is created, named or placed | [`01-structure-naming.md`](./references/01-structure-naming.md) |
| 2 | Components and templates | a component, its inputs and outputs, host bindings or a template is written | [`02-components-templates.md`](./references/02-components-templates.md) |
| 3 | Signals, resources and forms | state, derived state, async data or a form is written | [`03-signals-resources-forms.md`](./references/03-signals-resources-forms.md) |
| 4 | Injection, HTTP and routing | a service, an interceptor, a route or a guard is written | [`04-injection-http-routing.md`](./references/04-injection-http-routing.md) |
| 5 | Errors, security, performance and accessibility | an error path, a binding to a URL or HTML, a lazy boundary or a control is written | [`05-errors-security-performance.md`](./references/05-errors-security-performance.md) |
| 6 | Tests | any Angular test is written or reviewed | [`06-testing.md`](./references/06-testing.md) |

## Output / checkpoint
Code compliant with the sections the change touched, and the project's own build, lint and test commands
(`ng build`, `ng lint`, `ng test` where the project defines them) with no new finding. No dedicated checkpoint:
compliance is checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never an install: a missing dependency is named, and the person runs
`pnpm add -D <package>` (`CONVENTIONS.md`). Never build a template from a string that carries user input.
Never call `bypassSecurityTrust*` without a named reason in the review. A client-side guard is a user
experience, never the access control. When the project pins an older major than this block, say which rule
does not apply instead of rewriting working code to the newer idiom.

## Origin
Rewritten from the framework's official style guide, its machine-readable best-practice file and its
documentation, all read 2026-10-02. Provenance, licence and the refresh protocol are in
[`references/origin.md`](./references/origin.md). Read it when checking freshness, not when applying a rule.
