# python-patching-and-time-pitfalls §1 — monkeypatch and tmp_path

`monkeypatch` is safe in one respect: it undoes its changes. It is not safe about where the change lands. Most failed
patches are right patches applied to the wrong name, or to something pytest itself uses.

## 1.1 Patch the name the code looks up
1. **A patch must be applied before the code that uses the patched name runs.** The documentation says `setattr` has to
   be called before the function that will use the patched function is called.
2. **Patch the reference your code uses, not the original object in the standard library.** The documentation's example:
   if your module does `from os import getcwd`, patch `mymodule.getcwd`, not `os.getcwd`.
3. **Why:** the `from` import copied the name into your module, so replacing the original afterwards changes nothing
   there. When code calls `requests.get(...)` through the module at call time, patching the `get` attribute of that
   module takes effect, which is the documentation's own example. The inference about the lookup is ours, drawn from
   those two examples.
4. **Show that the patch bites.** Own guidance: remove it once and see the test reach the real function.

```python
import mymodule


def test_project_dir_uses_patched_name(monkeypatch):
    monkeypatch.setattr(mymodule, "getcwd", lambda: "/work")
    assert mymodule.project_dir() == "/work"
```

## 1.2 Do not patch builtins
1. **Patching builtins such as `open` or `compile` is not recommended: it can break pytest's own internals.**
2. **If it is unavoidable,** the documentation says that passing `--tb=native`, `--assert=plain` and `--capture=no`
   might help, with no guarantee.
3. **Prefer a seam you own.** Own guidance: wrap the builtin call in a function of your module and patch that (§1.1).

## 1.3 Standard library objects and pytest's own dependencies
1. **Patching stdlib functions, and some third-party libraries pytest uses, can break pytest itself.**
2. **For code you control, make the dependency explicit** and pass it in, instead of patching it globally; the
   documentation calls this the safer long-term pattern.
3. **When patching a stdlib object cannot be avoided, scope it with `monkeypatch.context()`** so the patch lives only
   for the block you want tested. The documentation's example patches `functools.partial` inside such a block.

## 1.4 What monkeypatch undoes, and its helpers
1. **All modifications are undone after the requesting test function or fixture finishes.**
2. **Helpers:** `setattr` and `delattr` for attributes, `setitem` and `delitem` for dictionaries, `setenv` and `delenv`
   for environment variables, `syspath_prepend` for `sys.path`, `chdir` for the working directory, `context` for scoped
   patches.
3. **For `PATH`, use `setenv("PATH", value, prepend=os.pathsep)`.**
4. **`syspath_prepend` also calls the import-cache invalidation**, as the documentation states (it names
   `importlib.invalidate_caches`), so use it rather than editing `sys.path` by hand.
5. **A module-level configuration dictionary patched with `setitem` or `delitem` is restored too,** so the change lasts
   for one test only.

## 1.5 The raising flag
1. **`raising` decides whether a missing target fails.** `setattr`, `delattr`, `delitem` and `delenv` default to raising
   `AttributeError` or `KeyError` when the target does not exist.
2. **Use `raising=False` only when absence is expected,** for example to test the path where an environment variable is
   missing and it may not be set on this machine; leave the default on everywhere else, so a typo in the target name
   fails loudly. The second half is our reasoning.

## 1.6 A guard against real network calls
1. **An autouse fixture can remove the method the HTTP library sends requests with,** so any request attempted in a
   test fails. The documentation's example deletes `requests.sessions.Session.request` for all tests from `conftest.py`.
2. **Put a mock shared by all tests in an autouse fixture in `conftest.py`;** a mock shared by some tests is an ordinary
   fixture that those tests request.
3. **The example is specific to the `requests` library.** Another client needs its own target; the principle is that
   a test that reaches the network should fail rather than succeed against the real one.

## 1.7 tmp_path and the base temporary directory
1. **`tmp_path` gives each test function a directory unique to it, as a `pathlib.Path`.** Own guidance: use it instead
   of a fixed location, so two tests never write the same file.
2. **`tmp_path_factory` is session-scoped** and creates arbitrary directories from any fixture; use it for something
   expensive that every test reads, generated once.
3. **By default pytest keeps the temporary directories of the last three runs** (configurable with the retention count
   and policy options); the incrementing number in the path is what keeps earlier results from being blindly removed.
4. **`--basetemp` is used directly as the base, with no retention, and its directory is cleared blindly before each run.**
   Give it a directory used for nothing else.
5. **Concurrent runs of the same test function need a distinct base temporary directory each,** per the documentation.
6. **Under pytest-xdist on one machine, pytest configures a base directory for the worker processes itself,** so
   everything lands under one per-run directory; you do not set it by hand for workers.
7. **`tmpdir` and `tmpdir_factory` are the legacy `py.path.local` forms;** the documentation prefers `tmp_path`, and
   `-p no:legacypath` turns uses of the legacy ones into errors.
