---
name: python-no-bare-except
description: "Use when writing or reviewing a try/except: never a bare except or except Exception that swallows everything, and never one with no rethrow and no log."
---

# python-no-bare-except

Narrow trigger extracted from `skills/python-conventions` §2.8–§2.11, so a `try`/`except` block
routes here directly instead of only through the whole Python block.

## When
Writing or reviewing any `try`/`except` — a call that can fail, a resource acquisition, a boundary
converting a library exception into a domain one.

## Steps
1. **Catch a specific class inheriting from `Exception`, never a bare `except:` or
   `except Exception:`** — a broad catch also catches your own typo and reports it as the failure
   you were expecting.
2. **Catch the narrowest scope, not the paragraph.** A `try` wrapped around a block containing the
   risky call *and* your own logic converts a null dereference or a wrong argument into the exception
   you had planned for. Wrap the call, not the surrounding logic.
3. **An `except` with no rethrow and no log hides a real bug** — never silent, even as a last resort.
   A bare swallow is indistinguishable from a forgotten branch and leaves no evidence anywhere that
   the failure happened.
4. **Preserve the cause when wrapping.** Raising a domain exception from inside an `except` without
   chaining it (`raise DomainError(...) from err`) keeps the meaning but throws away the traceback.

## Output / checkpoint
Every `except` in the diff names a specific exception class, wraps only the risky call, and either
re-raises (chained with `from`), logs with the original traceback, or does something else concrete —
never an empty or log-only swallow of a broad exception type.

## Guardrails
- Catching by type is what survives a refactor; matching on a message breaks the day somebody
  improves the wording.
- Truly exceptional conditions (a missing configuration key at boot, a broken invariant) should still
  crash rather than be converted to a result type — `skills/python-conventions` §2.7 covers that
  boundary.

## Origin
No external source: this is `skills/python-conventions` §2.8–§2.11 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
