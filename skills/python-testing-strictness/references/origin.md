# python-testing-strictness: origin and source stamps

> Provenance of `skills/python-testing-strictness`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real project by us. No test was run
and nothing was installed while writing it.

Overlaps with `skills/python-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| pytest documentation: reference (strict options, `filterwarnings`), customize (config files and precedence), explanation of import modes, how-to on fixtures (safe teardowns) and on warnings | MIT, read 2026-10-08 | Strict option semantics and the 9.0 `strict`, rename of `xfail_strict`, `[tool.pytest]` since 9.0 and the older table since 6.0, first-match config file, `importlib` mode pros and cons, one state change per fixture, filter precedence |
| pytest-asyncio documentation: concepts, configuration, how-to guides on loop scope | Apache-2.0, read 2026-10-08 | One loop per collector, `loop_scope`, the two default settings and the planned default change, strict and auto modes, sequential execution |
| Paldom/python-skills: the testing skill | MIT (copyright 2026), read 2026-10-08 | Branch measurement, threshold band, proving the gate trips, parallel and relative-file settings, subprocess patch, combine then gate once, total counting statements plus branches |
| scientific-python/cookie: the pytest guide | BSD-3-Clause, read 2026-10-08 | The strict options and `filterwarnings` set as a recommended baseline |

### Second pass, read 2026-10-20 (facts only, rewritten)

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| pytest `reference/reference.rst`, `reference/customize.rst`, `reference/exit-codes.rst`, `how-to/capture-warnings.rst`, `explanation/pythonpath.rst`, `how-to/fixtures.rst` (main branch) | MIT (pytest repository licence, read 2026-10-16 for a sibling block) | `strict` and its member options (`versionadded` 9.0 on `strict` only), the `xfail_strict` rename, config file order and the matching rule per file, `[tool.pytest]` 9.0 and `[tool.pytest.ini_options]` 6.0, `prepend` and `importlib` import-mode statements, exit code 5, safe teardown text. Corrected §1.4.1 (the directory put on `sys.path` is not always the directory of the test file) and softened §1.4.2 (no page states that `importlib` needs an installed package) |
| pytest-asyncio documentation: concepts and configuration reference | Apache-2.0 (licence read 2026-10-08) | One loop per collector, sequential execution, strict and auto modes, both default settings, the planned change, valid values |
| coverage.py documentation: configuration reference and the branch page | Apache-2.0 (the project published licence; its LICENSE file was not re-read in this pass) | `branch`, `parallel`, `relative_files` (5.0), `patch` (7.10), `fail_under` exit status 2, the percentage as executions over opportunities |

The coverage.py command page returned only a redirect notice and was not read, so `coverage combine` semantics beyond the
configuration page statement stay unverified.

## Rewrite notes
The verification lists, the advice to set both loop-scope defaults explicitly, and the "exception with an
owner and a date" rule are ours. The ratchet framing is the rule already in `python-conventions` §8.7.

## Not verified
1. **Coverage settings (§2):** `branch`, `fail_under` (status 2), `parallel`, `relative_files` and the subprocess patch
   with its 7.10 minimum are now confirmed against the coverage.py configuration page; the command page was not
   read, and the per-version-leg threshold and combine-then-gate advice (coverage reference) rest on the earlier skill reading.
2. **Different-loop error text** and the exact failure symptom of §3.3.1: the pytest-asyncio concepts page does not
   say what happens when a fixture and its test sit on different loops; still general asyncio behaviour.
3. **pytest 9.0.x regression** reported in the MIT skill (strict flags in `addopts` ignored, fixed in 9.1) was not
   confirmed in the pytest changelog and is not relied on.
4. **Release that introduced the individual `strict_markers` and `strict_config` keys:** the reference page gives no
   version; §1.1.5 says so.
5. **Whether `--import-mode=importlib` requires the package to be installed:** the explanation page does not state it;
   §1.4.2 labels it as our consequence.
6. **`strict_parametrization_ids` availability** follows `strict` (9.0) by inference; the page shows no note on it.

## Related blocks
`python-conventions` (toolchain and tests, async), `tdd`, `testing-anti-patterns`, `ci-workflow-hardening`.

Independent verification 2026-10-21: 16 checked, 16 matched, 0 corrected, 0 unverified
