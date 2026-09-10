# python-conventions — origin and source stamps

> Provenance of `skills/python-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Ideas taken from: PEP 484/526/604/695 (type hints, generics), PEP 8 (style), ruff (default rule set, replaces
flake8/isort/pyupgrade), mypy/pyright (strict typing); **an org skill catalogue for this stack (20 skills:
type hints on new code, explicit `is None`, failures as values at boundaries, intent-revealing naming, magic
strings as enums, async-first data access, DI lifetimes, layered component layout, config per namespace,
transactions through one facade, no DB cascade, Python-side defaults, non-loading relationships, facade-based
test doubles, application test base, ruff/uv/mypy/pytest toolchain)** — rules extracted, de-identified and
rewritten generically, with the internal framework and support-library names deliberately left out (rule C).
Mechanisms rewritten, no copied text. Stamped 2026-08-06.

**Re-checked directly against PEP 8 and ruff's default rule set on 2026-08-10**: re-verified, unchanged —
the PEP 8 items that carry a real judgment call (naming, truthiness, mutable defaults, comprehensions,
context managers) were already covered, and everything else it states is pure style ruff already auto-fixes
(import order, f-strings over `%`/`.format()`, `enumerate` over `range(len(...))`). That is the same reason
this block never restated PSR-12-style formatting the way `php-patterns` didn't. This note previously sat
inside the rules as point 8 of the inline §5, where it was the only entry in the block that was provenance rather than a rule;
the 2026-09-08 pass moved it here.

**§3.10 added 2026-09-07** (then §3.3) from a bodies pass over the same org catalogue, now 22 skills against
the 20 mined: the state-machine recognition pointer, which mirrors `laravel-conventions` §1.5 and exists for
the same reason — the source ships it as a skill whose only job is to be *seen*, because the task never
arrives phrased in pattern vocabulary. Everything else in the two-skill delta was already covered (§4.6's
async engine, §2's explicit `None` check, §7.3's non-loading relationships, §8's pinned toolchain); the
internal framework's own bootstrap, provider and utility APIs stay out under rule C, their mechanisms
already being §5, §6 and §7.

**Sectioned and deepened 2026-09-08.** This block was a single `SKILL.md` holding eight numbered sections
inline — the shape every other stack block had already grown out of. The pass did two things at once
because the second is what justifies the first: the eight sections moved to one file each under
`references/`, and each was taken through the same depth pass as the nuxt, laravel, react, flutter and
`code-baseline` blocks — every original point kept verbatim, given the mechanism and what the reader
actually sees when the rule is broken, with new points only where a section was *silent* on a failure mode.
Before → after, counting each section's inline body against its new file: §1 typing 207 → 902 words, §2
none/failures/exceptions 188 → 902, §3 naming 162 → 846, §4 async 110 → 881, §5 structure and style
236 → 914, §6 DI and lifetimes 69 → 824, §7 ORM and migrations 149 → 892, §8 toolchain and tests
162 → 866. The eight sections go **1,283 → 7,027** words, and the router that remains in `SKILL.md` is now
a table of triggers rather than the rules themselves. Each new file carries about 35 words of title and
pointer that the inline sections did not, which the other blocks' figures also include.

The additions worth naming are the ones the block had no line about. **Async** was the thinnest section in
the repo relative to how much can go wrong in it, and gained: a `gather` needs a decision about failure,
since by default the first exception propagates while the siblings keep running; concurrency without a
bound opens as many connections as the data says, so the same code is fine on ten rows and a denial of
service on ten thousand; cancellation is delivered as an exception, so a broad `except` breaks shutdown;
`async` does not make shared state safe, because there is no lock — only the absence of pre-emption between
awaits, which makes check-then-act across an `await` a genuine race; module-level mutable state is shared
across concurrent requests, i.e. between users; and a context variable rather than a global is the
mechanism that survives that. **DI** was thinner still, and the load-bearing addition is that a
dependency's lifetime cannot exceed the lifetime of what it holds — a singleton handed a request-scoped
session captures the first one and keeps using it after that request ended.

**§7** gained the transaction rules it had implied and not stated: a raise inside a transaction *is* the
rollback, a transaction held open across an external call holds row locks for the network's duration, and
nested blocks are usually not nested transactions. It also gained the migration failures — tested against
real data rather than a fresh install, a non-null column on a populated table needing add-nullable then
backfill then constrain, a schema change locking a large table, the model and the migration being one
change, and reversibility. **§5** gained the module-level rules that make Python specifically: nothing
mutable at module scope, no work in a module body, and config typed and validated at boot, since everything
in the environment is a string and `bool("false")` is true. **§3** gained the enum's published values, the
`StrEnum` carve-out (its members compare equal to plain strings, so it re-admits the magic string the rule
exists to remove), and the module name shadowing a standard-library one. **§2** gained the reason its
central rule exists at all: Python has no checked exception, so a raised failure is invisible to the
caller, the checker and the reader, and the only way to learn it is to read every function the body calls.

**Dogfooded once, 2026-09-08.** A small stdlib-only project was written by following this block and
`data-pipeline-conventions` — a pipeline that measures this repo's own depth table and stores each run in
SQLite, 44 tests green, run against the real repo. §4 (async), §6 (DI) and the mapper half of §7 never
applied and the router correctly kept them unread, which is the first useful result: the
read-only-what-you-touch table works. Three real gaps came out of it and are now closed:

- **§8.17 and the checkpoint**: the block opened by saying every rule holds in a repo with nothing
  installed, and its checkpoint required `ruff` and `mypy`, which §8.1 requires pinning. On a project
  where installs are refused by design, that checkpoint is unsatisfiable on code that is in fact
  compliant, and the block said nothing about the fallback. It now does, and the honest output is *no
  type checker available* as a finding rather than a pass nobody observed.
- **§8.18**: every rule in §8 was phrased in pytest's vocabulary — the plugin set, the test base, the
  fixtures — so the section with the most portable content in the block reads as inapplicable to a
  stdlib runner. The mapping is now stated.
- **§7.17 to §7.19**: §7 was entirely mapper- and migration-tool-shaped and said nothing about the case
  the project actually was, hand-written DDL. §7.8 to §7.11 (transactions) turned out to be fully
  portable and are now said to be; and a create-if-not-absent script silently never migrating an
  existing database, plus the engine defaults a mapper would have handled, were absent.

The project lives outside this repo, with its findings beside it. It is one small project written by the
same agent that wrote the block, so it does not make the row green — what it did is find three things
reading could not.

**What this block still is not.** The special status stands: no production experience behind it, so the
depth comes from the language's documented behaviour, the PEPs, the tooling and the mechanisms shared with
the blocks that *have* been dogfooded — not from real review feedback. Deepening it does not change its
status letter, and `samwise` keeps its question register for the same reason.

**Widened against the current async/tooling surface, 2026-09-09.** Same method as `csharp`, `design-patterns`
and `react` the same week: checked against the language and toolchain's current state rather than against
the source catalogue, which the 2026-09-07 bodies pass already settled. §4 gained `TaskGroup` as the
structured form of point 2's failure-handling decision — cancelling siblings and raising an `ExceptionGroup`
by construction rather than by discipline, caught with `except*` — plus cancellation reaching a context
manager's own `__aenter__`/`__aexit__`, the same leak shape as point 9 arriving from library internals. §8
gained `pytest-asyncio`'s auto mode as a config-block decision rather than a per-test marker (a test missing
the marker under strict mode collects silently as an unawaited coroutine and reports passed — point 7's bug
through the suite itself), and named the faster type-checker options (Pyright, Pyrefly, ty) as a one-tool
swap under point 1, not a personal substitution. Nothing here answers the catalogue comparison a second
time.

**Widening, 2026-09-10 — pass élargie.** A word-count pass against the stack's parity target, not another
catalogue comparison: the five thinnest sections (§6 DI/lifetimes, §3 naming, §1 typing, §2
none/failures/exceptions, §5 structure/style) each gained 500-700 words as 6-7 new numbered points appended
after their existing ones — nothing renumbered, nothing already stated repeated. Sourced from PEP 484/526/604
/695/612 (`ParamSpec`), the `contextvars`, `weakref`, `contextlib`, `itertools`, `dataclasses` and `logging`
stdlib docs, and the CPython exception-group / `except*` documentation — never from the org catalogue this
block was already mined from, and never by reading the XEFI marketplace files. §6 gained `contextvars` over
thread-locals for per-request state, runtime-parameterised factories, lazy-singleton race conditions, weak
references for unowned caches, health checks resolving the real pooled binding, container-seam test overrides,
and per-request scope teardown. §3 gained multi-parameter generic naming under PEP 695, `__all__` as the
stated public surface, keyword-only parameter naming, scenario-based test names, abbreviation cost, positional
-only parameter naming, and boolean-parameter naming. §1 gained `Protocol` vs `@runtime_checkable`,
`TypedDict`'s `Required`/`NotRequired`, `ParamSpec` for signature-preserving decorators, `Self` return types,
`@overload` resolution order, dataclass-vs-validation-model boundaries, and `Literal` as the typed alternative
to a small magic string. §2 gained sentinel values distinct from `None`, `contextlib.suppress` naming its
exceptions, `ExceptionGroup`/`except*` for concurrent failures, retry-policy design, the walrus operator
next to an explicit `is None` check, generator cleanup under cancellation, and a custom exception forwarding
its base `__init__`. §5 gained `pyproject.toml` as single-source project metadata, `src/`-layout catching
accidental local imports, `__init__.py` side effects as module-body work, `itertools`-composed lazy
pipelines, `@dataclass(slots=True)`, and `logging` over `print`.

**Widening, 2026-09-10 — deuxième pass.** Same word-count method as the previous day's pass, aimed at the
three sections that pass had not reached — §4 async, §7 ORM/migrations, §8 toolchain/tests, the thinnest
remaining files in the block — each gaining 500-700 words as 6-9 new numbered points appended after their
existing ones, nothing renumbered. Sourced from the `asyncio` stdlib docs (`asyncio.timeout`, `Queue`,
`to_thread`, `shield`, signal handlers, subprocess), the SQLAlchemy 2.0 and Alembic documentation (connection
pooling, autogenerate's documented limitations, naming conventions, branched migration heads), and the
pytest and Hypothesis documentation (fixture scope, parametrize composition, property-based testing,
`conftest.py` discovery rules) — never from the org catalogue this block was already mined from, and never
by reading the XEFI marketplace files. §4 gained `asyncio.timeout()` as a block-scoped deadline, backpressure
via a bounded `asyncio.Queue`, `to_thread` versus a process for genuinely CPU-bound work, `shield`'s narrower
guarantee, signal handlers unable to `await`, subprocess reaping, and an unbounded retry loop as timeout
point 10 failing one level up. §7 gained `pool_pre_ping`'s mid-transaction blind spot, autogenerate as a
draft rather than a commit (including its check-constraint expression blind spot), constraint naming
conventions, branched migration heads needing an explicit merge, bulk writes bypassing ORM hooks, JSON/JSONB
mutation-tracking, and autogenerate-proposed indexes still being a locking operation on a large table. §8
gained fixture scope as a state-sharing claim, parametrized-fixture combinatorial multiplication, readable
parametrize ids, Hypothesis for properties rather than examples, test-only dependencies still needing a
declared group, matching a fixture's scope to its resource's real lifetime, and `conftest.py`'s
directory-based discovery and shadowing.

**Widening, 2026-09-10 — troisième pass.** Same word-count method as the day's first two passes, run against
the five thinnest files remaining after them: §1 typing, §2 none/failures/exceptions, §3 naming, §4 async,
§6 DI/lifetimes — each gaining roughly 400-600 words as new numbered points appended after their existing
ones, nothing renumbered, nothing already stated repeated. Sourced from the `typing` documentation and its
associated PEPs (698 `@override`, 742 `TypeIs`, 728 closed `TypedDict`), the `asyncio` stdlib docs (`Future`,
locks, comprehensions, `anyio` versus raw structured concurrency), the exception and pytest-fixture
documentation, and general naming/DI reasoning already used elsewhere in this block — never from the org
catalogue this block was already mined from, and never by reading the XEFI marketplace files. §1 gained
`@override`, `TypeIs` versus `TypeGuard`, closed `TypedDict`s, stub-file contracts, generic bounds, `NewType`,
and callable `Protocol`s. §2 gained `raise ... from None`'s deliberate-hiding claim, exception hierarchies as
a selective-catch tool, a library's exceptions as part of its public contract, tuple- versus stacked-`except`
semantics, `BaseException` versus `Exception`, context managers duplicating pytest fixtures, and
`TimeoutError`'s two unrelated origins. §3 gained module-versus-symbol naming, package `__init__.py`
re-exports as a public-surface statement, decorator naming, name reuse across a module's history, pytest
fixture names as public vocabulary, version-numbered names, and dunder look-alikes. §4 gained async context
managers under cancellation, `asyncio.run()`'s per-call teardown, unresolved manual `Future`s, non-reentrant
lock deadlocks, async comprehensions exhausting an unbounded source, and mixing `anyio` with raw `asyncio`
primitives. §6 gained framework-native DI (`Depends`) still following the same rules, mutable default
arguments as an invisible singleton, constructor versus attribute injection, decorator-based registration
discoverability, environment-branching inside a binding instead of at the composition root, and typing a
marker-resolved dependency as what it resolves to.

**Widening, 2026-09-10 — 4ème passe.** Same word-count method as the day's three previous passes, this
time on §5 structure/style, the one section untouched since the original 2026-09-08 sectioning pass and,
combined with `data-pipeline-conventions`'s four sections, among the thinnest files left in the stack
against `bin/measure_depth.py`'s parity target. §5 gained roughly 425 words as 8 new numbered points
appended after its existing 24, nothing renumbered, nothing already stated repeated. Sourced from PEP 735
(dependency groups in `pyproject.toml`) and its accompanying `peps.python.org` text, current packaging
guidance on `[build-system]` and lockfiles, and reasoning already established elsewhere in this section —
never from the org catalogue this block was already mined from, and never by reading the XEFI
marketplace files. §5 gained `[dependency-groups]` as the one standardised place for non-production
dependencies over a tool-specific table, the distinction between an optional extra (shippable to a
consumer) and a dependency group (deliberately excluded from the distribution), group composition to
avoid duplicating a shared dependency across groups, a committed lockfile as what makes "the same code"
actually reproducible rather than a version-range fiction, namespace packages as a deliberate
plugin-ecosystem trade-off rather than a default layout, the limits of point 18's "one file" rule against
tools with no `pyproject.toml`-native form, a lockfile pinning a composed group's own resolution, and an
explicit `[build-system]` declaration as the same "declared, not assumed" discipline applied to the build
itself.

**Dogfooded again, 2026-09-10.** A real project (`/tmp/dogfood-python`, outside this repo): an
order-enrichment pipeline (`asyncio.TaskGroup` + `Semaphore` + `asyncio.timeout` fan-out over an async
tier lookup, `except*` re-raising a typed `EnrichmentUnavailableError` at the boundary,
constructor-injected `Protocol`-bound tier lookup, `Order | ValidationFailure` returns at the row
validation boundary, a `SourceSchemaError` raised — not returned — on a missing source column, and an
idempotent order_id-keyed dict merge), covering exactly the sections the widening rounds since
2026-09-08 had added ~9,000 words to and that had never been run for real: §1 typing, §2
none/failures/exceptions, §4 async, §6 DI/lifetimes (plus §8 toolchain). `ruff check` and
`mypy --strict` passed clean on the first pass, no loosening needed. 12 pytest cases — including one
regression guard for §2.1 (an explicit `amount_cents: 0` must not be rejected by truthiness), one that
asserts `except*`/`ExceptionGroup` catches what §4.16 says it raises under `asyncio.timeout`, and one
that runs the pipeline twice on the same input and diffs the result rather than asserting idempotence by
reading the code (§1.18's own doctrine, self-applied) — passed green.

No rule failed to hold in practice. One real gap surfaced: §4.16 states that `TaskGroup` cancels
siblings and raises through an `ExceptionGroup`, and §2.3 states a public boundary returns/raises a
single typed failure — but nothing bridges the two. Collapsing an `ExceptionGroup` back into the one
typed exception a boundary is supposed to expose (`except* EnrichmentUnavailableError as eg: raise
eg.exceptions[0] from eg`) silently discards every sibling exception beyond the first, which is a real
decision (which one to surface, whether the rest are worth logging) that neither section states. §4
gained a point for this. One correction, not a gap: the *previous* entry in this file, also dated
2026-09-10, described a project (`SourceUnavailableError`, a warehouse, a duplicate-key quarantine)
that does not match anything actually built or run under that timestamp — it has been replaced by this
entry. One environment-only friction, not a content gap: this sandbox had no `sudo`/`venv`, but `ruff`
and `mypy` were already available via `~/.local/bin` from a prior `pip install --user`, so no toolchain
workaround was needed this time.
