---
name: python-testing-strictness
description: "Use when a Python project's pytest or coverage configuration is written or changed, a test run passes suspiciously, or an async fixture or a multi-step fixture misbehaves: strict markers and strict config, warnings as errors, strict xfail, which config file pytest actually reads, import mode, branch coverage and a gate that is proven to fail, combining coverage across runs, pytest-asyncio event loop scope for fixtures, and fixture teardown that survives a failing setup."
---

# python-testing-strictness

Step 5 and 6 of the pipeline (`WORKFLOW.md`), for the settings that decide whether a green pytest run means
anything. The three sections share one premise: **a test setting that is wrong does not fail, it quietly
runs less than you think**: a misspelt marker that never selects, a config file that is not the one read, a
coverage threshold that cannot trip, a teardown that did not run. What to test, and the tooling basics
(pinned runner, one config block, fixture scope, parametrize ids), are in `python-conventions` §8 and
`tdd`; the doctrine on tests that prove nothing is in `testing-anti-patterns`. This block covers the settings
and fixture rules those do not state.

## When
- Creating or editing the pytest, coverage or warnings configuration, or a new project's test setup.
- A marker, a config key or a test seems to be ignored; a deprecation only showed up at an upgrade.
- Adding a coverage threshold or running tests in parallel or across several Python versions.
- Writing an async fixture shared across tests, or a fixture that creates more than one thing.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | pytest configuration: strict mode, warnings as errors, strict xfail, the config file actually read, import mode | the pytest settings are written or a setting seems ignored | [`01-pytest-config.md`](./references/01-pytest-config.md) |
| 2 | Coverage: branch measurement, the threshold, a gate that is shown to fail, parallel and multi-version runs | a coverage tool or threshold is added or changed | [`02-coverage.md`](./references/02-coverage.md) |
| 3 | Fixtures: safe teardown, one state change per fixture, event loop scope for async fixtures | a fixture creates a resource, or an async fixture is shared across tests | [`03-fixtures-and-event-loops.md`](./references/03-fixtures-and-event-loops.md) |

## Output / checkpoint
Each setting was shown to bite: a typo marker was added to a scratch test and the run failed (§1), a
warning was raised in a scratch test and the run failed (§1), the coverage gate was run once with a
threshold the code cannot meet and exited non-zero (§2), and a fixture was made to fail in its second
setup step and the first step's cleanup was observed (§3). A setting that was only written is not verified.

## Guardrails
- Never read a green run as proof when the config file in use was not confirmed (§1.2).
- Never lower a threshold or add a warning ignore to get a change through without saying it is a project
  decision (§1.3, §2.2).
- Never combine an async fixture of wider scope with tests on a narrower event loop (§3.3).
- Settings here are stated for the pytest and pytest-asyncio documentation read on the date in
  [`references/origin.md`](./references/origin.md); several are version-gated and each rule names the
  version. Check the one the project pins. Nothing was run while writing this block.
- Adding a plugin or a tool is the user's step: this block names it and stops.

## Origin
Rewritten from the pytest and pytest-asyncio documentation, one MIT agent-skill repository for pytest and
coverage setup and one BSD scientific-Python template's pytest guide (read 2026-10-08). This block is meant
to be folded into the same-topic toolchain-and-tests section when PR 118 lands. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
