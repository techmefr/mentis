---
name: python-conventions
description: "Use when writing or reviewing Python: type hints and mypy strict, failures returned as values at public boundaries, async correctness, the toolchain, layered structure, the ORM rules."
---

# python-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Python code. Every rule below holds
in a repo with **nothing installed** (`CONVENTIONS.md`, rule A). Complementary to `samwise` (the diff review
agent): here we write the code, samwise re-reads it afterwards.

**Special status**: like `go-conventions`/`dotnet-conventions`, no production experience behind this block
yet — content comes from the PEPs, deterministic tooling (ruff, mypy) and an org catalogue for the stack,
not from real review feedback. That is why `samwise` reads it in a question register rather than as settled
house law.

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue for this stack, it
is the authority on **its** house style — its framework, its internal support library, its pinned tool
versions — and overrides this block wherever the two differ. This block states the same rules with the
internal names removed, so they apply to a project that has neither.

**Applying an override is silent.** Write the code the governing rule actually requires and move on — never
report "a conflict between mentis and the house catalogue" to whoever's watching. That framing reads as
broken to a non-technical stakeholder even when the case is a normal, resolved one, and has already caused a
real project to get abandoned and restarted over nothing. Surface it as a specific, named question only when
no rule anywhere actually resolves the case — never as a general alarm.

## When
As soon as Python code is written or modified, during `code` (6) or `tdd` (5).

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; loading all of them for a change that only renames a variable is waste, and a section
read is a section that has to be applied. If you are reviewing a whole diff, pick the rows whose
trigger the diff meets, not the whole table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Typing | a signature, an attribute or a generic is typed | [`01-typing.md`](./references/01-typing.md) |
| 2 | None, failures, exceptions | a failure is returned or raised, or a resource is opened | [`02-none-failures-exceptions.md`](./references/02-none-failures-exceptions.md) |
| 3 | Naming | a symbol, a domain value or a constant has to be named | [`03-naming.md`](./references/03-naming.md) |
| 4 | Async | an `async def`, a gather, or a blocking call in an async path | [`04-async.md`](./references/04-async.md) |
| 5 | Structure and style | a module is placed, config is read, or a default is written | [`05-structure-style.md`](./references/05-structure-style.md) |
| 6 | Dependency injection and lifetimes | a binding is declared or a lifetime is chosen | [`06-di-lifetimes.md`](./references/06-di-lifetimes.md) |
| 7 | ORM and migrations | a model, a relationship, a query or a migration is written | [`07-orm-migrations.md`](./references/07-orm-migrations.md) |
| 8 | Toolchain and tests | a tool version, a test double or the test base is involved | [`08-toolchain-tests.md`](./references/08-toolchain-tests.md) |

## Output / checkpoint
Code compliant with the sections above, and `ruff check`/`mypy` (or `pyright`) with no new finding introduced
by the diff. Checked by `gate` (7) and `review` (8). **Where the project has no dependency manager and the
tools cannot be installed** (rule A taken literally), the checkpoint is the stdlib's own — `unittest` green
and `python -m compileall` clean — and it records *no type checker available* as a finding rather than
reporting a pass it did not observe (§8.17).

## Guardrails
No comments in the code produced. This block has been confronted with one small stdlib project
(2026-09-08, see `references/origin.md`) and with no real production Python project: if a rule here
diverges from a real observed need, fix this block rather than treating it as settled.
These rules govern **new** code; existing untyped, sync or magic-string code stays until migrated
deliberately. Never loosen a checker rule or a coverage threshold to get a diff through — that is a project
decision, not a side effect of a change. Where an org catalogue is installed and disagrees, **it wins**.

## Origin
Rules mined from the PEPs, the deterministic toolchain and an org catalogue for this stack, rewritten in the
house voice; the full provenance, the source stamps and the refresh log are in
[`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still
current, not when applying one.
