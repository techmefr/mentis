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
