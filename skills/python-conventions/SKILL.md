---
name: python-conventions
description: Use when writing or reviewing Python, typing (type hints, mypy/pyright), error handling, async patterns, project structure. No internal Xefi production experience on this language (unlike vue-nuxt-vuetify-conventions), sourced from the official PEPs and established tooling (ruff, mypy).
---

# python-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Python code. **Special
status**: like `go-conventions`/`dotnet-conventions`, no Xefi production experience behind this block
yet: content coming from the official PEPs and deterministic tooling (ruff, mypy), not from real review
feedback.

## When
As soon as Python code is written or modified, during `code` (6) or `tdd` (5).

## Steps

### 1. Typing: PEP 484 and beyond
1. Type hints on every public function signature (parameters + return), `mypy`/`pyright` in strict mode
   run on the diff, not only at the project's initial setup.
2. An explicit `Optional[T]`/`T | None` rather than an untyped `None` default value that leaves the real
   contract to guesswork.
3. `dataclass`/`pydantic` for a data structure with validation, rather than an untyped dict passed from
   function to function.
4. `TypedDict` to type an existing dict (external API, JSON) without converting it into a class: no
   `Dict[str, Any]` out of reflex.

### 2. Error handling
1. A specific exception raised (a dedicated class inheriting from `Exception`), never a bare
   `except Exception:` that swallows everything indiscriminately.
2. An `except` with no rethrow or log hides a real bug: never silent, even as a last resort.
3. A context manager (`with`) for every resource that has to be closed (file, connection, lock): never a
   manual close that an intermediate exception can skip.

### 3. Async
1. `asyncio.gather` for independent operations, never a serial `await` in a loop out of reflex.
2. Never mix blocking code (synchronous I/O, heavy CPU work) into an `async` function without isolating
   it (`run_in_executor`): it blocks the whole event loop, not just the caller.
3. A coroutine created but never awaited or stored is a silent bug (`RuntimeWarning: coroutine was never
   awaited`), always checked.

### 4. Structure and style
1. Immutability by default: a mutable default argument (`def f(x=[])`) is banned: it's shared across all
   calls, a classic trap.
2. `pathlib.Path` rather than string manipulation for file paths.
3. Comprehensions (list/dict/set) rather than a loop + `append` when readability gains from it, never
   nested to the point of hurting readability.

## Output / checkpoint
Code compliant with the four sections above, and `ruff check`/`mypy` (or `pyright`) with no new finding
introduced by the diff. Checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. This block hasn't been confronted with a real production Python project
at Xefi yet: if a rule here diverges from a real observed need, fix this block rather than treating it as
settled.

## Origin
Ideas taken from: PEP 484/526/604 (type hints), PEP 8 (style), ruff (default rules, replaces
flake8/isort/pyupgrade), mypy/pyright (strict typing). Mechanisms rewritten, no copied text. Market
research, no internal production feedback at this stage: same status as `go-conventions`.
