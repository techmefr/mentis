---
name: python-patching-and-time-pitfalls
description: "Use when a Python test patches a function, an attribute, an environment variable, the working directory or the path with pytest's monkeypatch, needs a temporary directory (tmp_path, basetemp), or freezes the clock with freezegun: patching the name the code looks up rather than the original, never patching builtins, scoping stdlib patches, what monkeypatch undoes, the raising flag, a guard against real network calls, tmp_path retention and basetemp, what freezegun freezes, ticking, timezone offset, asyncio sleep, default arguments and the ignore list."
---

# python-patching-and-time-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for the two kinds of test double Python projects reach for first: patching
what the code looks up, and controlling the clock. The two sections share one premise: **a patch only works at the
place the code reads from and at the time it is read, and a frozen clock changes every reader of time, including the
ones you did not mean to freeze**. Pytest configuration, coverage and fixture teardown are in
`python-testing-strictness` §3 and are not repeated; the doctrine on doubles that test themselves is in
`testing-anti-patterns` §1.

## When
- Writing a test that replaces a function, a class attribute, a dictionary entry or an environment variable.
- A patch has no effect, or a patched stdlib object breaks pytest itself.
- A test needs a temporary file or directory, or runs concurrently with other runs.
- A test depends on the current date or time, on elapsed time, or on `asyncio.sleep`.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | `monkeypatch`: where to patch, builtins, scoping, undo, env and path helpers, the network guard; `tmp_path` and `--basetemp` | a test patches or needs a temporary directory | [`01-monkeypatch-and-tmp-path.md`](./references/01-monkeypatch-and-tmp-path.md) |
| 2 | freezegun: what is frozen, ticking, offset, asyncio, default arguments, the ignore list | a test controls or depends on the clock | [`02-freezing-time.md`](./references/02-freezing-time.md) |

## Output / checkpoint
Each patch was shown to bite: with the patch removed, the test reached the real function or the real value (§1.1);
the patched target is the name the module under test imports (§1.1); no builtin was patched (§1.2); a frozen-time
test that waits was run once and finished (§2.2, §2.4). A patch that was only written and never shown to take
effect is not verified.

## Guardrails
- Never patch the original object when the code under test imported the name; patch the name it uses (§1.1).
- Never patch a builtin such as `open` or `compile` (§1.2).
- Never leave a patch of a stdlib object unscoped when it cannot be avoided (§1.3).
- Never point `--basetemp` at a directory that holds anything you want to keep (§1.7).
- Never freeze time around code that waits on elapsed time without choosing how time advances (§2.2).
- Never freeze time around an asyncio test without deciding on the event loop's clock (§2.4).
- This block states what the pytest and freezegun documentation describe at the commits in
  [`references/origin.md`](./references/origin.md). Version-bound facts name their version. Nothing was run while
  writing it.

## Origin
Rewritten from the pytest how-to pages on monkeypatching and temporary directories (MIT) and the freezegun README
(Apache-2.0), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
