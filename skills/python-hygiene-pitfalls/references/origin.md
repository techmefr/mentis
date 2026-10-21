# python-hygiene-pitfalls: origin and source stamps

> Provenance of `skills/python-hygiene-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No code was executed and nothing was
installed while writing it.

Overlaps with `skills/python-conventions` (2026-10-19); cross-referenced, not merged.

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

### Second pass, read 2026-10-20 (facts only, rewritten in our own words)

| Source | Licence | What it confirmed or corrected |
|---|---|---|
| Python documentation: `datetime` (deprecation of `utcnow` and `utcfromtimestamp` since 3.12, naive `fromtimestamp`, naive and aware comparison, `datetime.UTC` added in 3.11) | Python documentation licence (PSF); facts only, no text copied | Corrected §1.2.3: ordering comparisons raise `TypeError`, equality does not raise and is always false |
| Python documentation: `open()` in the built-in functions page, `pathlib`, `using/cmdline` (`-O`, `-X warn_default_encoding`, `-X utf8`) | same | Corrected §1.3.1: the locale default applies unless UTF-8 mode is on, and the development documentation records UTF-8 as the default from 3.15; `Path.read_text` and `write_text` take `encoding`; `-O` removes assert statements |
| PEP 597 (Final, Python 3.10) | public document of the Python project; facts only | `encoding="locale"` and `EncodingWarning` from 3.10, the `LookupError` on older versions, the recommendation to use UTF-8 |
| Python documentation: `contextvars`, `functools`, logging HOWTO | same | Module-level creation of a `ContextVar`, the `get()` lookup order, `self` in the cache key and references kept, deferred formatting and the `isEnabledFor()` guard |
| pytest documentation: how-to on assertions | MIT (pytest repository licence, read 2026-10-16 for a sibling block) | `match` uses `re.search` |
| Ruff rule pages B019, B023, B039 (re-opened) | MIT | Examples and fixes as stated in the rules |

## Rewrite notes
The rule codes are pointers to detection only. The verification lists, the grouping of the six construct
traps and the advice to prefer queues for hand-off between threads are ours (the last restates the guide).

## Not verified
1. **Resolved 2026-10-20:** the naive and aware comparison (corrected, see above), `Path.read_text` taking
   `encoding`, `encoding="locale"` from 3.10 and `datetime.UTC` from 3.11 (all confirmed). Still unconfirmed on a page:
   that the same timestamp differs across hosts is the direct consequence of the documented local-time
   conversion, not a quoted sentence.
2. **`contextlib.contextmanager`** was not re-opened; `pytest.raises` `match` confirmed.
3. **Python 3.15 UTF-8 default:** re-read 2026-10-21 on the 3.15.0 documentation page (a release, no longer the development version); the first read described an unreleased
   interpreter; confirm against the release the project pins before dropping `encoding=`.
4. **Structured logging advice** (§2.1.3) is ours; the logging HOWTO page opened does not mention `extra`.
5. **Dropped for lack of a reliable source:** a general claim that a module-level cache is per process in a
   forked server (no page read states it), and the advice on async task state across an `await`.
6. **Google style guide points** (§2.2, §3.1, §3.2) were not re-opened in this pass; they keep the 2026-10-08 read.

## Related blocks
`python-conventions` (typing, exceptions, async, tests), `python-no-bare-except`,
`python-async-no-blocking-calls`, `python-testing-strictness`, `python-sqlalchemy-fastapi-pitfalls`.

Independent verification 2026-10-21: 14 checked, 13 matched, 1 corrected, 0 unverified
