# python-conventions §5 — Structure and style

> Section 5 of `skills/python-conventions`. Read it when a module is placed, config is read, or a default is written. The other sections and the guardrails stay in `SKILL.md`.

1. Immutability by default: a mutable default argument (`def f(x=[])`) is banned — it's shared across every
   call, the classic trap. The default is evaluated once, at definition time, so the list accumulates across
   calls and the second caller sees the first caller's data. Use `None` and build inside, and note that a
   class-level mutable attribute is the same bug one scope up (§1.9).
2. **Nothing mutable at module level either.** A module body runs once per process, so a dict or list
   declared there is shared by every request, every task and every test in the session — which makes it both
   a cross-request leak (§4.12) and a source of tests that pass alone and fail together.
3. **A module body should not do work.** Opening a connection, reading an environment variable, calling an
   API or building a client at import time makes the import order load-bearing, breaks any tool that merely
   imports the module (a checker, a docs builder, a test collector), and moves failures to a place where the
   traceback names an import rather than a cause.
4. **Prefer passing a value to reaching for one.** A function that reads global state cannot be called twice
   with different inputs and cannot be tested without arranging the world; the same function taking the
   value as a parameter is both. This is the rule that makes §6's container useful rather than decorative.
5. `pathlib.Path` rather than string manipulation for file paths. Concatenating separators is where the
   Windows/POSIX difference and the double-slash bugs live, and a path built from user input needs
   resolving and checking against its intended root — string joining hides both questions.
6. Comprehensions rather than a loop + `append` where readability gains, never nested to the point of hurting
   it. The threshold in practice: one `for` and at most one `if` reads as a description of the result; two
   `for`s reads as a puzzle, and a comprehension with a side effect is a loop pretending not to be.
7. **A generator where the whole list is not needed.** Materialising a query result, a file's lines or a
   large mapping to iterate it once costs the memory of the whole thing for no benefit — and the same trap
   in reverse is a generator consumed twice, which is silently empty the second time.
8. **Mutating a collection while iterating it skips elements or raises**, depending on the type. Build a new
   collection, or iterate a copy; the version that "works" is the one that quietly processes half the input.
9. Separate **functional/business** layers from **technical/infrastructure** ones (the layered split), with a
   predictable place per component and no technical layer importing a business one. The direction is the
   point: a technical layer that reaches into a feature can no longer be reused by the next feature.
10. **The import graph is checkable, and a convention nobody checks drifts.** A layering rule in a linter
    holds on a large diff in a way that a reviewer's attention does not — and the cycle a violation creates
    is otherwise found later, as an `ImportError` at a place that names neither module.
11. **A late import to break a cycle is a note that the layering is wrong.** It works, and it moves the
    failure from import time to first call, so it is only acceptable as a deliberate, explained exception
    rather than as the standard way to make two modules coexist.
12. Every component declares its own wiring in one place (a provider/registration module) rather than
    scattering registrations across the app. Scattered, the effective graph exists only in whatever order
    the imports happen to run, which is the least readable form of configuration there is.
13. **Configuration: one file per namespace**, each exporting a module-level mapping, the filename being the
    namespace. Values are read through the config layer, never `os.environ` reached into from business code.
    Reaching directly means the variable's name, its default and its parsing are duplicated at each site and
    diverge — and it makes the code untestable without the environment.
14. **Config is validated at boot, and a missing value fails loudly.** A default silently substituted for an
    absent variable is how an application runs against the wrong database or signs with a placeholder secret
    while looking healthy; the crash at startup is a deployment problem for ten seconds, the fallback is a
    correctness problem for as long as nobody notices.
15. **A config value is typed on the way in.** Everything in the environment is a string, so a limit, a
    timeout, a port and a flag are all parsed somewhere — and `bool("false")` is `True`, which is the
    specific version of this that turns a feature on in production.
16. Reach for the project's existing support layer before the stdlib or a new dependency for something it
    already covers (password hashing, structured logging, config access, encryption, events, DI, test
    scaffolding). A second way to do a solved thing is the duplication that bites later.
17. **A dependency is code running with your privileges.** Adding a package for one helper adds its
    transitive tree, its install-time code and whoever now maintains it, so the platform is worth checking
    first — and an unexplained dependency in a diff is a question rather than a detail.
18. **`pyproject.toml` is the one place project metadata, dependencies and tool configuration are declared —
    not a `setup.py` alongside a `setup.cfg` alongside a tool's own ini file.** Three files each owning part
    of the same configuration drift the moment one is edited and the others are not, and a build backend
    reading `pyproject.toml` while a linter still reads a `.flake8` next to it is exactly the "second way to
    do a solved thing" point 16 already names — the fix is one file per project, not one file per tool.
19. **A `src/` layout catches an import that only works by accident.** With the package importable straight
    from the repository root, a test can pass by importing the working-directory copy of the module while
    the installed package — the one that will actually ship — has a different bug or is missing a file the
    editable install papered over. Nesting the package under `src/` means the test only imports the package
    that was actually installed, so packaging mistakes surface locally instead of in production.
20. **An `__init__.py` that does anything beyond re-exporting is a module body with a worse name for the
    problem in point 3.** It runs on the first import of anything in the package, so a database call, a
    plugin registry built by scanning submodules, or a side-effecting decorator placed there makes *touching
    the package at all* — including from a tool that only wants to introspect it — trigger work the caller
    never asked for.
21. **`itertools` composes a pipeline without materialising the intermediate steps, which is point 7's
    generator preference applied more than once in a row.** Chaining `filter`, then a comprehension, then
    `list()` to feed another comprehension builds and discards a full list at each stage; `itertools.chain`,
    `islice` and `groupby` (on already-sorted input — it groups consecutive runs, not the whole key space)
    compose lazily, so a pipeline over a large or unbounded source still runs in the memory of one item at a
    time.
22. **`@dataclass(slots=True)` trades a per-instance `__dict__` for a fixed set of attribute slots**, which
    is worth taking on a class instantiated many times over a request or a batch — it lowers the per-instance
    memory and rejects an attribute assigned by typo instead of silently creating it. It costs the ability to
    monkeypatch an arbitrary new attribute onto an instance later, which is rarely a loss for a data-carrying
    class and is exactly why it is the discipline this section already asks for on such a class.
23. **A `print()` in application code is a log line with no level, no destination and no structure**, and it
    is also point 3's module-level work if it runs at import time. The standard library's `logging`, or a
    structured logger built on it, gives every line a level that a handler can filter on and fields that a
    log aggregator can query on — which a string concatenated for `print` cannot offer no matter how
    carefully it is formatted.
24. **A module importing a submodule only to re-export it should say so with an explicit `as`, or a checker
    in strict mode flags the import as unused.** `from .models import User as User` is the accepted way to
    tell both the reader and the linter that the import is the public surface, not a leftover — the
    alternative of suppressing the warning wholesale hides the next genuinely unused import behind the same
    silenced rule.
