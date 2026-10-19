# python-hygiene-pitfalls: origin and source stamps

> Provenance of `skills/python-hygiene-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No code was executed and nothing was
installed while writing it.

This block is meant to be folded into the same-topic sections of `python-conventions` when PR 118 lands; it
cites only sections that exist on main.

## Attribution

Part of this block (the error-message rule in §2.2, the logging pattern rule in §2.1, the threading rule
in §3.1, the resource rule in §3.2 and the assertion litmus test in §1.1) is adapted from the Google
Python Style Guide (`pyguide`), copyright Google, licensed under the Creative Commons Attribution 3.0
Unported licence (CC-BY-3.0, the repository's licence file read 2026-10-08). The text here is rewritten, not
copied, and changes were made. The licence is at https://creativecommons.org/licenses/by/3.0/.

## Sources (all read 2026-10-08, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| Google Python Style Guide: exceptions, threading, logging, error messages, files and sockets | CC-BY-3.0, attribution above | Assert litmus test, atomicity of built-ins, queue and locks, literal log patterns, three error-message requirements with the NaN and directory examples, `__del__` unreliability and `with` |
| Ruff rule documentation: S101, the datetime-timezone group (utcnow and fromtimestamp), PLW1514, B023, B019, B039, G004, PT012 | MIT, read 2026-10-08 | `-O` stripping, naive datetime constructors, locale-dependent encoding and PEP 597, late binding example and fixes, cached method reference leak, shared ContextVar default, eager log formatting, single-statement raises body |

## Rewrite notes
The rule codes are pointers to detection only. The verification lists, the grouping of the six construct
traps and the advice to prefer queues for hand-off between threads are ours (the last restates the guide).

## Not verified
1. **Naive and aware datetime comparison raising** and the "same timestamp differs across hosts" consequence
   of `fromtimestamp` are standard-library behaviour not quoted from the pages read.
2. **`Path.read_text` taking `encoding`**, `contextlib.contextmanager` and the `match` argument of
   `pytest.raises` are standard-library and pytest API facts not re-read for this block.
3. **Version gates:** `datetime.UTC` from Python 3.11 and `encoding="locale"` from 3.10 are as stated in the
   Ruff rule text; not run.
4. **Structured logging advice** (§2.1.3) is ours; the Ruff page names the `extra` mapping, not any
   structured-logger library.
5. **Dropped for lack of a reliable source:** a general claim that a module-level cache is per process in a
   forked server (no page read states it), and the advice on async task state across an `await`.

## Related blocks
`python-conventions` (typing, exceptions, async, tests), `python-no-bare-except`,
`python-async-no-blocking-calls`, `python-testing-strictness`, `python-sqlalchemy-fastapi-pitfalls`.
