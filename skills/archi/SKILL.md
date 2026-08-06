---
name: archi
description: Use when the spec is locked down, before the plan, map what already exists and where the feature plugs in, to avoid duplication.
---

# archi

Step 3 of the pipeline (`WORKFLOW.md`). The step that **avoids duplicates**: agreeing on the
target architecture by looking at the real code.

## When
After `spec`, before `/PLAN`. Systematic as soon as we touch shared code or an existing domain.

## Steps
1. Run **graphify** on the worktree(s) concerned → a graph of what exists.
2. Spot the **reusable common ground** (similarity pass): helpers, components, endpoints
   already there.
3. Decide **where the feature plugs in** (reuse vs create), note the extension points.
4. Write the target architecture via **`set_arch_node`** (file / role / `planned` status).

## Output / checkpoint
`arch_done` + architecture nodes filled in (living documentation).

## Guardrails
Extracting shared code = **a coordinated refactor, a human decision**: don't refactor quietly
inside an isolated worktree. If a duplicate already exists, flag it, don't recreate it.

## Origin
Internal (graphify) + convergence of several market skill authors (architecture before build),
rewritten.
