---
name: zig-conventions
description: "Use when writing or reviewing Zig: names of types, namespaces, functions and files, redundancy in names, layout, and doc comments that state invariants. Pinned to a development version of the language."
---

# zig-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames naming and layout of Zig code.

**Freshness stamp**: read on 2026-10-02 from the language reference shipped in the compiler's source tree at
commit `738d2be9` of 2025-11-26, whose build file declares version 0.16.0 (a development tree, not a
release). The language changes between versions; before applying this block, check the style guide of the
version the project builds with (`skills/source-freshness`). Status 🟡; only the style guide section of the
reference was read, so memory management, error handling, comptime and the build system carry no rule.

## When
As soon as Zig code is written or modified, during `code` (6).

## Steps
Read [`references/01-style.md`](./references/01-style.md) (names, layout, doc comments). It is the only
section.

## Output / checkpoint
Code formatted by the language's own formatter, which implements the layout recommendations, and names that
follow §1. Checked by `review` (8).

## Guardrails
No comments in the code produced; doc comments only where §1.8 asks, on declarations others use. Where a
convention is already established in the project or the platform (a constant copied from a system header),
follow it.

## Origin
Rewritten from the MIT-licensed compiler repository's language reference, with pinned commit in
[`references/origin.md`](./references/origin.md).
