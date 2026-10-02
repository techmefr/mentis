---
name: kotlin-android-conventions
description: "Use when writing or reviewing Kotlin or an Android app in Kotlin: immutability and null handling, functions and errors, the layered Android app structure and tests, coroutines and Flow, static analysis."
---

# kotlin-android-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Kotlin, and of an Android app written
in Kotlin. The language rules come from the language documentation's coding conventions, null-safety and
exception pages; the app-structure rules come from the reference Android sample app maintained by the platform
vendor. Both were read on 2026-10-02 (`references/origin.md`).

**Special status**: 🟡, no in-house production Kotlin stands behind this block. Not read: the platform vendor's
own Kotlin style page, its architecture guide pages and the Compose guidance, so none of them is cited. The
coroutine and analyser sections (§4, §5) were added on 2026-10-02 from their own documentation.

## When
As soon as Kotlin code is written or modified, during `code` (6) or `tdd` (5).

## Steps

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Immutability, null handling, expressions | a variable, a collection, a nullable value, an `if` or `when`, a loop | [`01-language-idioms.md`](./references/01-language-idioms.md) |
| 2 | Functions, API shape, errors | a function signature, an extension, a factory, a thrown exception, a published library | [`02-functions-api-errors.md`](./references/02-functions-api-errors.md) |
| 3 | Android app structure and tests | a module, a layer, a ViewModel, a repository, a build flavor, a test | [`03-android-app-structure.md`](./references/03-android-app-structure.md) |
| 4 | Coroutines and Flow | a coroutine is launched, a suspending function or flow is written, state is shared, a dispatcher chosen | [`04-coroutines-flow.md`](./references/04-coroutines-flow.md) |
| 5 | Static analysis | the analyser configuration, a suppression or a baseline changes | [`05-static-analysis.md`](./references/05-static-analysis.md) |

## Output / checkpoint
Code compliant with the sections touched, formatted by the project's formatter, with its local tests run. A
check that was not run is reported "not run", never as a pass. Checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced, except public-API documentation of a published library (§2.8). Never use
`!!` to silence the compiler; never swallow an exception to get a test green. Existing code stays until
migrated deliberately.

## Origin
Rewritten from an Apache-2.0 language documentation repository and an Apache-2.0 reference app, with credit
and pinned commits in [`references/origin.md`](./references/origin.md). Read it when checking currency, not
when applying a rule.
