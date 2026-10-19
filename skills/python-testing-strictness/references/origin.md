# python-testing-strictness: origin and source stamps

> Provenance of `skills/python-testing-strictness`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real project by us. No test was run
and nothing was installed while writing it.

This block is meant to be folded into the same-topic toolchain-and-tests section of `python-conventions`
when PR 118 lands; until then it stands alone and cross-links only sections that exist on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| pytest documentation: reference (strict options, `filterwarnings`), customize (config files and precedence), explanation of import modes, how-to on fixtures (safe teardowns) and on warnings | MIT, read 2026-10-08 | Strict option semantics and the 9.0 `strict`, rename of `xfail_strict`, `[tool.pytest]` since 9.0 and the older table since 6.0, first-match config file, `importlib` mode pros and cons, one state change per fixture, filter precedence |
| pytest-asyncio documentation: concepts, configuration, how-to guides on loop scope | Apache-2.0, read 2026-10-08 | One loop per collector, `loop_scope`, the two default settings and the planned default change, strict and auto modes, sequential execution |
| Paldom/python-skills: the testing skill | MIT (copyright 2026), read 2026-10-08 | Branch measurement, threshold band, proving the gate trips, parallel and relative-file settings, subprocess patch, combine then gate once, total counting statements plus branches |
| scientific-python/cookie: the pytest guide | BSD-3-Clause, read 2026-10-08 | The strict options and `filterwarnings` set as a recommended baseline |

## Rewrite notes
The verification lists, the advice to set both loop-scope defaults explicitly, and the "exception with an
owner and a date" rule are ours. The ratchet framing is the rule already in `python-conventions` §8.7.

## Not verified
1. **All coverage.py settings (§2):** `branch`, `fail_under`, `parallel`, `relative_files`, the subprocess
   patch and its minimum coverage version (7.10), and the exit codes come from the MIT skill; the coverage.py
   documentation itself was not read.
2. **Different-loop error text** and the exact failure symptom of §3.3.1 is general behaviour of asyncio, not
   quoted from the pytest-asyncio pages.
3. **pytest 9.0.x regression** reported in the MIT skill (strict flags in `addopts` ignored, fixed in 9.1)
   was not confirmed in the pytest changelog and is not relied on; the rule says to confirm the config is
   applied by running a scratch test.
4. **`strict_parametrization_ids`** semantics are from the reference page; its exact availability by version
   follows `strict` (9.0) and was not checked individually.
5. **Whether `--import-mode=importlib` requires the package to be installed** is our consequence of
   "does not change `sys.path`", not stated on the page read.

## Related blocks
`python-conventions` (toolchain and tests, async), `tdd`, `testing-anti-patterns`, `ci-workflow-hardening`.
