---
name: elixir-phoenix-conventions
description: "Use when writing or reviewing Elixir or Phoenix code: assertive pattern matching and return types, data modelling, processes and supervision, macros, contexts, scoped access, the web-layer vulnerabilities and tests."
paths: "**/*.ex, **/*.exs, **/mix.exs, **/lib/**/*_web/**, **/config/*.exs"
---

# elixir-phoenix-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Elixir code and of a Phoenix web
layer. Every rule below holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A). **Special
status**: like `go-conventions`, no in-house production experience sits behind this block yet. The content comes
from the official Elixir anti-patterns catalogue and the Phoenix guides, read on 2026-10-02 on their main
branches (the guides describe the scope-based generators of the current Phoenix line; an older project reads
the scope points as "not yet"); treat it as a base to confront with the first real Elixir project, not as
proven doctrine.

## When
As soon as Elixir code is written or modified, during `code` (6) or `tdd` (5): a function with several
clauses, a process, a macro, a context function, a controller or LiveView, a query, a plug, a test.

## Steps

**Read only the sections the task touches.** One file per section under `references/`.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Assertive code, return types, data modelling | a function head, a `with`, an option list, a map access, a conversion from text is written | [`01-elixir-code-design.md`](./references/01-elixir-code-design.md) |
| 2 | Processes, supervision, macros, library hygiene | a process is started, a GenServer interface added, a macro or `use` written, a library published | [`02-processes-macros.md`](./references/02-processes-macros.md) |
| 3 | Phoenix: contexts, access, web vulnerabilities, tests | a context function, a controller, a plug, a query fragment, an outbound request or a test is written | [`03-phoenix.md`](./references/03-phoenix.md) |

## Output / checkpoint
Code compliant with the sections read; the project's compile (warnings as errors where the project sets it),
format check and tests green. Checked by `gate` (7) and `review` (8). Where the project cannot run its
toolchain (no environment), the checkpoint records it rather than reporting a pass, and nothing is installed to
make it run (`CONVENTIONS.md`: a block names a dependency and stops).

## Guardrails
No comments in the code produced (documentation attributes are a separate mechanism and stay where the project
uses them). These rules govern **new** code; an existing anti-pattern stays until touched. Never loosen a
check, a compile warning or a security rule to get a diff through. For the error body shape,
`skills/api-design`; for queues, `skills/background-jobs-conventions`; for authentication and sessions,
`skills/auth-session-conventions`.

## Origin
Rewritten from the Elixir documentation and the Phoenix guides; the full provenance, licences and the audit of
what was left out are in [`references/origin.md`](./references/origin.md). Read it when checking a rule's
freshness, not when applying one.
