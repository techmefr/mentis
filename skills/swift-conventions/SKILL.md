---
name: swift-conventions
description: "Use when writing or reviewing Swift API surface: naming and fluent call sites, argument labels, parameters and defaults, mutating and non-mutating pairs, documentation of public declarations."
---

# swift-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the **design of Swift declarations and call sites**. It is
deliberately narrow: only the language project's API design guidelines were read (2026-10-02,
`references/origin.md`).

**Special status**: 🟡. Not read in this pass, so absent from the block: the concurrency model, error
handling, memory and ownership, SwiftUI, the formatter and linter documentation, and the platform vendor's
developer documentation. A review of those areas gets no rule from here; it says "no source read".

## When
As soon as a Swift declaration is added or renamed, during `code` (6) or `tdd` (5), and in `review` (8) of
any change that touches a public or module-level name.

## Steps

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Naming and fluent usage | a type, method, property or protocol is named | [`01-naming.md`](./references/01-naming.md) |
| 2 | Parameters, labels, documentation | a signature is written, a label chosen, a public declaration documented | [`02-parameters-labels-docs.md`](./references/02-parameters-labels-docs.md) |

## Output / checkpoint
Declarations whose use sites read as the guidelines require, checked by writing the call at its use site and
reading it. Checked by `review` (8).

## Guardrails
No comments in the code produced; documentation comments on the public declarations of a published module
are the product and follow §2.5. Never rename a published declaration without the deprecation path of the
project.

## Origin
Rewritten from the Swift API design guidelines, credit and pinned commit in
[`references/origin.md`](./references/origin.md).
