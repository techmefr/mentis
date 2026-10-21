# python-testing-strictness §1 — pytest configuration

pytest's defaults are permissive so that old suites keep running. For a new or maintained suite, each
permissive default is a way for a test to stop doing its job without any output.

## 1.1 Make mistakes errors
1. **Unregistered markers: error, not ignore.** With `strict_markers` on, a marker not declared in the
   configuration raises, both on tests and in `-m` expressions. Without it a typo such as `@pytest.mark.slwo`
   is a marker nobody selects, and a `-m "not slow"` run still runs the slow test.
2. **Config warnings: error.** `strict_config` turns warnings found while parsing the pytest section into
   errors, so a misspelt key stops being a setting that never applied.
3. **`xfail` that passes: fail.** `strict_xfail` makes a test marked as expected-to-fail fail the suite when
   it succeeds, so a fixed bug does not stay marked as a known failure forever. The reference page records the
   rename from `xfail_strict` in 9.0, with the old name accepted as an alias.
4. **From pytest 9.0 a single `strict = true` enables all of these** and the other strict options, including
   `strict_parametrization_ids` (an error on non-unique parameter ids instead of the silent `0`, `1` suffixes). The documentation warns that future strict options join it automatically, so
   use it with a pinned pytest, or list the individual keys. An individually set key beats `strict`.
5. **Below pytest 9, use the command-line flags in `addopts`** (`--strict-markers`, `--strict-config`) and
   `xfail_strict`; `strict` is documented as added in 9.0. The reference page gives no "added in" note for the
   individual keys `strict_markers` and `strict_config`, so which release introduced them is unconfirmed; the flags
   are the safe form on an old pytest. Set `minversion` so an older
   pytest errors clearly instead of ignoring what it does not know.

## 1.2 Know which file is read
1. **Only one configuration file is used and files are never merged:** the first match wins, in the order
   `pytest.toml`, `.pytest.toml`, `pytest.ini`, `.pytest.ini`, `pyproject.toml`, `tox.ini`, `setup.cfg`.
   `pytest.toml` and `pytest.ini` (and their dot-prefixed forms) match even when empty, so a stray, empty one
   shadows every setting in `pyproject.toml`; `pyproject.toml` matches only with a `[tool.pytest]` or
   `[tool.pytest.ini_options]` table, `tox.ini` with a `[pytest]` section and `setup.cfg` with `[tool:pytest]`. List the candidates (`ls pytest.ini tox.ini setup.cfg .pytest.ini`) and confirm which
   file pytest reports as its config file in the run header.
2. **`pyproject.toml` has two table names with a version gate.** `[tool.pytest]`, with native TOML types, is
   supported since pytest 9.0; `[tool.pytest.ini_options]`, with INI-style string values, since 6.0. The
   older table is the portable one while the project may run an older pytest; do not write both.
3. **Check the installed pytest version before trusting a new key**, then check the header again after any
   upgrade. A setting the installed version does not know is not always loud.

## 1.3 Warnings as errors
1. **`filterwarnings = ["error"]` turns every warning into a failure,** so a deprecation fails the run on
   the day it appears instead of the day an upgrade removes the feature. By default pytest only summarises
   warnings at the end, where nobody reads them.
2. **Add named, narrow exceptions below it** (`ignore::DeprecationWarning:<module>`, or one message
   pattern), each for a reason you can state, because later filters take precedence over earlier ones (the
   documentation follows the `warnings.filterwarnings` ordering; the warnings page also notes that the message in
   the configuration option is interpreted differently from the one in the `-W` flag). A broad
   `ignore::DeprecationWarning` re-hides the thing you turned on.
3. **A third-party deprecation you cannot fix this week is an exception with an owner and a date,** not a
   reason to turn the setting off. Loosening it is a project decision (`python-conventions` §8.7).

## 1.4 Import mode and test layout
1. **The default `prepend` mode puts a directory derived from each test file at the front of `sys.path`:** the
   directory of the file itself for a standalone module, the directory above the top-level package when `__init__.py`
   files are present. It then needs
   either `__init__.py` files in the test tree or globally unique test file names, or two same-named files
   error. The documentation says it is the classic mechanism.
2. **`--import-mode=importlib` does not touch `sys.path`** and does not need unique file names, so a test
   can only import what is installed or on the configured Python path; in practice your package has to be
   installed (editable or not) for the tests to see it, which is the situation you want to test. The page does not
   state that requirement; it is our consequence of the mode leaving `sys.path` alone.
3. **Its cost is stated:** test modules cannot import each other, and shared test helpers have to live in the
   package or a plugin rather than in the tests directory. Decide at project start; moving later touches every
   test file.
4. **The default stays `prepend`** according to the documentation, so `importlib` is an explicit setting
   (`addopts` or the command line).

## 1.5 One configuration block
1. **Settings live in one block of one file** (`python-conventions` §8.5, §8.6): strictness, `testpaths`,
   markers, the asyncio mode, the filter list. A second source is how §1.2 happens.
2. **List `testpaths`** so a run from the repository root does not collect vendored or generated code.

## Verification
- A scratch test with `@pytest.mark.not_declared` fails the run; a scratch test that warns fails the run.
- The run header names the configuration file you expect, and its version satisfies `minversion`.
- A scratch `xfail` test that passes fails the suite.
