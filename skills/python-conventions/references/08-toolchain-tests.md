# python-conventions §8 — Toolchain and tests

> Section 8 of `skills/python-conventions`. Read it when a tool version, a test double or the test base is involved. The other sections and the guardrails stay in `SKILL.md`.

1. One formatter+linter (ruff), one dependency and Python-version manager (uv), one type checker (mypy
   strict), one test runner (pytest) — **pinned**, and the same versions in CI as locally. A tool floating on
   `latest` turns an unrelated release into a red build, and the failure lands on whoever pushed next rather
   than on whoever changed something.
2. **Pin the interpreter, not only the packages.** A minor Python difference between a developer's machine
   and CI changes syntax availability, dependency resolution and occasionally behaviour, so "works for me"
   is a statement about a version nobody wrote down. The manager exists to make that one line.
3. **The lockfile is the dependency list; the manifest is the intent.** Installing from the manifest alone
   resolves differently over time, which is how a build that passed last week fails today with no diff. The
   lock is committed, and an unexplained change to it in a review is a question.
4. **One tool per job, and the boundary stated.** Two linters, or a formatter arguing with a linter,
   produces a diff that flips back and forth depending on who ran what last — and the argument gets settled
   in review instead of in configuration, every time.
5. **Configuration lives in the project file, not in each developer's editor.** A rule enforced by somebody's
   local setup is not enforced; a rule in the shared config is enforced identically for everyone including
   the pipeline, which is the only definition that matters.
6. The pytest plugin set is pinned in a dev group and configured in one block, not rediscovered per developer.
   Plugins change collection, fixtures and reporting, so a plugin present on one machine and absent on
   another means the same command runs a different suite.
7. **The checker's strictness is a ratchet, and loosening it is a project decision.** Turning a rule off, or
   relaxing a per-module override, to get a diff through is a change to everyone's contract made as a side
   effect of one change — the same shape as lowering a coverage threshold (`code-baseline` §6.16).
8. Test doubles substitute a collaborator **through its own public seam** (the facade's or the container's
   double/override), never by patching internals: a test patching a private path breaks on any refactor and
   proves nothing about the contract.
9. **Patching by string is patching a location, not a thing.** The target has to be where the name is
   *looked up*, not where it is defined, so moving an import silently makes the patch apply to nothing — the
   test then passes while exercising the real collaborator, which is the worst of both outcomes. Injecting
   the dependency (§6.6) removes the question entirely.
10. **Fake the boundary, not your own code.** A double standing in for your own client or repository
    exercises none of the mapping, retry or parsing that justified writing it; the thing to fake is the
    transport underneath — the HTTP layer, the clock, the queue (`code-baseline` §4.10).
11. A test that needs the application built goes through the project's test base, so the container, the
    config and the database context are set up the same way in every test. Hand-built setup drifts per file,
    and then a test fails for a reason that has nothing to do with what it asserts.
12. **Each test stands alone.** Shared module state (§5.2), a container left overridden (§6.13) or a row
    left in the database makes the order matter, so the suite passes in the order it was written and fails
    in the order the runner chooses — which reads as infrastructure trouble rather than as coupling.
13. **Freeze the clock and the randomness.** A test reading the real time fails at midnight, on the first of
    the month, on a leap day or in the CI timezone, and a test that fails for reasons unrelated to the code
    gets muted and then deleted.
14. **A test that has never failed has not been shown to work.** Write it red, or break the behaviour once
    and watch it — an assertion that can never fail occupies the place where the real test would have been
    and reports success for ever (`code-baseline` §8's asymmetry, arriving through the suite).
15. **Assert the refusal, not only the success.** The rejected input, the unauthorised caller, the failure
    path of §2: those are what become incidents rather than bugs, and a suite that only exercises the happy
    path proves the feature works while saying nothing about who can reach it.
16. **A slow suite gets skipped, so its speed is part of its design.** A test that reaches a real network or
    a real sleep is a tax on every future change, and taxes get evaded locally by running a subset — which
    is when the pipeline becomes the first place anyone sees a failure.
17. **Where the project has no dependency manager, points 1 to 7 have nothing to pin.** A stdlib-only
    project — no manifest, no lock, no installable tools — cannot satisfy them, and pretending otherwise
    makes this block's own checkpoint unsatisfiable on a repo that is in fact compliant. What still
    applies there: the annotations are written whether or not a checker reads them, `unittest` is the
    runner, `python -m compileall` is the only mechanical check available, and the checkpoint records
    **no type checker available** as a finding rather than as a pass. Found by dogfooding 2026-09-08.
18. **The rules above are portable to the stdlib runner, and it is worth saying because the vocabulary
    hides it.** There is no plugin set to pin, so point 6 does not apply; "the project's test base"
    (point 11) is a `TestCase` subclass the tests share; per-test isolation (point 12) is `setUp` plus
    `addCleanup`, and the second is what guarantees a cleanup still runs after a failing assertion where
    a hand-written teardown does not. Read as pytest-only, the section with the most portable content in
    this block gets skipped entirely.
19. For the doctrine of *what* to test — plan first, exhaustive rather than happy-path, the persona/permission
    matrix, the coverage floor — see `skills/tdd`; this section is only about the tooling.
20. **`pytest-asyncio`'s auto mode is a project-wide default, decided once, not a per-test marker habit.**
    Set in the config block point 5 already asks for, every `async def test_*` is collected as a coroutine
    without `@pytest.mark.asyncio` on each one — a test missing the marker under strict mode does not fail,
    it silently collects as a function that returns an unawaited coroutine and reports as passed, which is
    §4.7's never-awaited bug arriving through the suite itself rather than through application code.
21. **A faster type checker is a tool swap, not a strictness change.** Pyright/Pyrefly/ty read the same
    annotations mypy does and can replace it under point 1's one-tool rule, but the point of pinning is that
    the swap is a deliberate project decision written down once — not a personal substitution one developer
    makes locally because it is faster, which quietly means the CI job and the editor are checking the code
    two different ways.
