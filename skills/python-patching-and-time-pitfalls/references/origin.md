# python-patching-and-time-pitfalls: origin and source stamps

> Provenance of `skills/python-patching-and-time-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation, never run by us. No test was executed, nothing was installed
and no sample was run while writing it. Open points are listed under "Not verified".

## Sources (re-read in full 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| pytest-dev/pytest, `doc/en/how-to/monkeypatch.rst` (commit c9c19f8, 2026-10-13; the sample output in the sibling page shows pytest 9.x) | MIT (repository LICENSE file, re-checked: "The MIT License (MIT)", Holger Krekel and others) | The helper list and undo rule, `raising`, where to patch, the builtin and stdlib warnings, `monkeypatch.context()`, explicit dependencies, the autouse network guard, the `PATH` and `chdir` helpers |
| pytest-dev/pytest, `doc/en/how-to/tmp_path.rst` (same commit, read in full) | MIT (as above) | `tmp_path`, `tmp_path_factory`, default retention, `--basetemp` semantics and its warning, concurrent runs, xdist handling, the legacy fixtures |
| spulec/freezegun, `README.rst` (commit 92d61b3, 2025-08-19, version 1.5.5 in `freezegun/__init__.py`; read in full) | Apache-2.0 (repository LICENSE file, re-checked: "Apache License, Version 2.0", copyright 2012 Steve Pulec) | What is frozen, monotonic clocks, the application forms, default arguments, `tick`, `auto_tick_seconds`, manual `tick` and `move_to`, `tz_offset`, `real_asyncio`, the ignore list and its defaults, `configure` |

The three code samples (§1.1, §2.2 and §2.4) are our own and were not run. No sample code was copied. The pytest and
freezegun documents contain no agent directives.

### Second pass, read 2026-10-20 (facts only)

| Source | Licence | What it confirmed |
|---|---|---|
| pytest `how-to/monkeypatch.rst` (main) and the `MonkeyPatch` entry of the reference page | MIT (pytest repository licence, read 2026-10-16) | The timing of `setattr`, the builtins warning and its three flags (hedged: "might help"), `raising` defaults and the helpers without it, `setenv` `prepend`, `syspath_prepend` invalidating the import caches (the page also names a `pkg_resources` call, not carried), the autouse network guard, `context()`, explicit dependencies |
| pytest `how-to/tmp_path.rst` (main) | MIT | Per-function uniqueness, retention of three runs, option names (no defaults given on the page), `--basetemp` cleared blindly, xdist, legacy fixtures |
| freezegun `README.rst` (master; no version shown on the page) | Apache-2.0 (repository licence, read 2026-10-16) | Frozen functions, monotonic note, default arguments, `tick` ignored with `auto_tick_seconds`, the `tz_offset` example, `real_asyncio`, the ten default ignore entries, `configure`, class decorator caveat |
| Python documentation: `unittest.mock` ("where to patch"), reference (`from` import binding), `asyncio` event loop, `time` | Python documentation licence (PSF); facts only | The lookup principle behind §1.1 (now sourced), the event loop's monotonic clock, `time.monotonic()` reference point |

## Rewrite notes
Version-bound facts carry their version: the freezegun default ignore list is that of 1.5.5, and the pytest pages are
those of the development line at the commit above. The retention count of three, the `tmp_path_retention_count` and
`tmp_path_retention_policy` option names and the `--basetemp` semantics are pytest's current documented behaviour and
may differ in older releases.

**Own guidance, not from a source (still):** the "show the patch bites" check (§1.1.4), the wrapper-seam advice for
builtins (§1.2.3), the reason to keep `raising` on by default (§1.5.2), the preference for manual ticking (§2.2.3), the
date-boundary test (§2.3.4, built on the README's own offset example) and the ignore-list confirmation step (§2.5.5).
**Sourced on 2026-10-20 and no longer marked:** the lookup rule behind the `from` import (§1.1.3), and the asyncio
consequence wording (§2.4.1) apart from its last clause.

## Removed or corrected from the review item
1. **Corrected:** the item said to give `--basetemp` a unique value per concurrent run under xdist. The page says
   pytest-xdist on one machine configures a base directory for its workers itself; the unique value is needed for
   concurrent runs of the same test, such as two separate invocations (§1.7.5, §1.7.6).
2. **Added from the source, missing in the item:** `time.monotonic()` and `time.perf_counter()` are also frozen (§2.1.2),
   and the default arguments trap (§2.1.4).
3. **Not carried:** the monkeypatch examples for dictionaries and connection strings, the `requests.get` mock-response
   class, and the freezegun function and generator inputs, since they illustrate API shape rather than a failure mode.
4. **Cross-links not made:** the fixtures rule in `python-testing-strictness` §3 is linked, nothing else; no section that
   exists only on another branch is cited.

## Not verified
0. **Resolved 2026-10-20:** that the event loop uses a monotonic clock is the asyncio page's statement; it does not
   say the clock is `time.monotonic()`, which is CPython behaviour read nowhere here.
1. **The `pkg_resources` part of `syspath_prepend`** was left out because it is a packaging detail that may have changed;
   only the import-cache note is carried.
2. **Behaviour under pytest-xdist** beyond the sentence in the tmp_path page was not checked.
3. **freezegun with pytest-asyncio** or other async plugins: the `real_asyncio` example is the README's, no plugin was
   examined.
4. **Other freezegun options** (`as_arg`, `as_kwarg`, function and generator inputs, nice input formats) were read but not
   carried.

## Related blocks
`python-testing-strictness`, `testing-anti-patterns`, `flaky-test-triage-pitfalls`.
