# design-patterns — origin and source stamps

> Provenance of `skills/design-patterns`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

The catalogue itself is the classic Gang of Four set as published on the widely used
`refactoring.guru` reference — 5 creational, 7 structural, 10 behavioural patterns, verified 2026-08-06.
Its catalogue pages describe when each pattern applies and carry **no caution about overuse**, which is
the gap this block exists to fill: taken at face value, a catalogue is read as a menu.

§4's entry conditions come from **an org skill catalogue's per-pattern skills** (state, strategy,
null object, object construction, and — added 2026-08-11 from the same catalogue's `design-patterns` plugin,
read directly from its installed clone — value-object, pipeline, transaction-boundaries), extracted and
rewritten generically: their triggers are precise and worth owning here, while their language-specific
implementation references stay with them (rule C — nothing naming an internal library or project crossed
over). Where that catalogue is installed it remains the authority on the shape; this block keeps the
decision and the trigger, which a skill about a pattern can't cover, since it assumes you've already decided
to use it. The three added points aren't classic GoF (the catalogue audited in the 2026-08-10 pass below is
deliberately just the 22), which is exactly why they weren't already here — they're real, recurring shapes
this file had no verdict on at all, not a gap in the GoF coverage pass.

What's ours: recognise-don't-apply with the second-real-case threshold, the framework-already-does-it
subtraction pass (which is where most of the catalogue goes in our stacks), Adapter/Facade justified by
containment rather than reuse, the Repository-over-ORM verdict, and wiring the whole thing to the
existing `over-abstraction`/`yagni` tags so a named pattern gets no discount at review.

Coverage pass (2026-08-10, refactoring.guru catalogue re-checked directly for Prototype/Composite/
Bridge/Flyweight/Proxy/Chain of Responsibility/Mediator/Memento/Visitor definitions): every one of the
22 patterns now has an explicit verdict in this file — either subtracted (already the framework/language,
§2), dismissed with a reason (Flyweight), given a concrete entry condition (§4), or named as a rare escape
valve (Bridge). None was added on the strength of "it's in the catalogue"; each verdict follows the same
second-real-case/framework-subtraction test as the original seven.

**Sectioned and deepened 2026-09-08**, the last of the single-file blocks in `CATALOG.md`'s depth
programme. The five inline sections moved to one file each under `references/` with a router table in
`SKILL.md`, and a sixth was added. §4 kept its number and every point number inside it, because
`business/fintech-compliance` cites §4.5 (Value Object, money is never a float) and
`laravel-conventions` §4 and §8 cite the transaction-boundaries rule at §4.7. §2's bullet list became
numbered points, its text unchanged, so that its verdicts can be cited the way the rest of the repo's
rules are.

**§6, when a pattern stops earning its place, is the new section and the one this block was missing
most.** Everything here — and everything in the source catalogue — was about whether to *add* a pattern;
nothing said when to take one out, which is why they accumulate in a codebase that has been reviewed
carefully at every step. It states the deletion test as the version of the net-line test that applies to
code somebody already merged, and then the things nobody gets a notification about: the interface whose
second implementation was decommissioned, the state machine whose middle states a product change removed,
the pool justified by a measurement on a runtime version that has since been upgraded, the pattern grown
to fit a case that does not share its axis until every implementation ignores half its own signature, the
suite with a test per implementation and none for the dispatch where the bugs actually are, and the ADR
line that survives the structure it justified and gets the pattern reimplemented from the document.

The deepening of the five original sections followed the same method as the other blocks — mechanism plus
what the reader or the next maintainer actually sees, one point per real failure mode, every original
point kept verbatim. The additions worth citing: a class hierarchy losing the exhaustiveness check a
discriminated union gives you, so a new subclass that forgets a method silently inherits the parent's
(§2.4); the concrete loss when a Repository wraps an ORM — eager loading, query composition, and seeing
the query that ran, all re-exposed one method at a time until it is the ORM with a different spelling
(§2.9); a state machine's transitions being where concurrency bites, so the guard has to be a conditional
write rather than a read-decide-save (§4.2); a Null Object that hides a failure rather than a legitimate
absence, i.e. a no-op mailer that reports success (§4.3); same-typed neighbours being what makes a wide
constructor dangerous rather than merely ugly (§4.4); a pipeline having to answer what a failing stage
does and whether a stage may mutate what later stages read, or it is worse than the god-method it
replaced (§4.6); and a job dispatched inside a transaction being picked up before the commit, so it reads
a row that does not exist yet (§4.7). Router plus sections: 2,347 → 6,333, which takes the row from
x5.19 to x1.92.

**Two stale cross-references into this block were found and fixed in the same pass**:
`laravel-conventions` §4 and §8 both cited a seventh section of this block for the
transaction-boundaries rule, and this block has never had one — the rule is §4.7 here. Wrong since
those lines were written, and found by resolving every reference rather than by reading.

**Status.** 🟡 — the GoF catalogue and the org catalogue's triggers are solid sources, and §1, §2, §3 and
§6 are ours: written from what this repo's own review history keeps producing rather than from a source
that could be re-checked. Depth does not change that.

**Widened against the source catalogue's own stack-specific files, 2026-09-09.** The 2026-08-10 coverage
pass checked every GoF pattern name against this file's verdicts; it did not check whether the org
catalogue's per-pattern *implementation* skills (their `.md` files per stack, read directly from the
installed clone) named a failure mode this file's entry conditions say nothing about. Seven did, and each
is a mechanism, not a restatement of the pattern:

- **§4.7 (transaction boundaries)** gained the three ways a first implementation breaks silently: a
  flush is not a commit, so a same-connection test can pass on an operation that never committed; a
  nested transaction is usually a savepoint whose inner rollback the outer commit ignores; and a model's
  own lifecycle events fire *inside* the boundary, so a listener's side effect ships before the row is
  ever guaranteed to exist.
- **§4** gained seven points: an illegal state transition is an exception, never a boolean a caller can
  ignore (§4.8); the state's name stays queryable data even once its behaviour moves into classes (§4.9);
  a resolver needs three different answers for a missing key depending on where the key came from —
  ours, a request, or a legitimately optional one (§4.10); a pipeline's halt needs two distinct signals,
  because "nothing left to do" and "the run must fail" are not the same stop (§4.11); several
  constructors are named constructors, not a class called a factory (§4.12); a boolean parameter that
  changes behaviour is two methods wearing one signature (§4.13); and a value object never crosses the
  wire directly, in either direction (§4.14).
- **§1** gained the brownfield rule its twelve points had never stated: introducing a pattern and
  changing behaviour in the same diff hides which one broke the tests, and refusing the fifth branch of
  an existing `switch` on the grounds that refactoring is out of scope is its own kind of avoidable harm
  (§1.13).

Router plus sections: 6,333 → **7,369 words**, x1.92 → **x1.65**. Nothing here reproduces an installed
catalogue's stack-specific code — each point states the failure and the mechanism, and leaves the shape
to whichever house style is installed (§4's own guardrail on that division).

**Status unchanged.** Wider is not dogfooded: §1, §2, §3 and §6 remain what this repo's own review
history produced, and the new points are read from a source rather than from a real review — closer in
kind to §4's original seven than to the rest of the file.

**Widening, 2026-09-10 — pass élargie.** §1, §2, §3, §5 and §6 each gained new numbered points, appended
after the existing ones without renumbering anything already cited elsewhere in the repo. Sourcing: the
rule-of-three/smell-vs-pattern distinction (§1.14–18) and the unused-abstraction/shotgun-surgery entries
(§6.13–16) are synthesised from the public code-smell literature that follows Kent Beck's and Martin
Fowler's *Refactoring* vocabulary (code smell vs anti-pattern, dead/unused abstraction, rule of three); the
new framework subtractions (§2.13–17 — memoization, language-native decorators, DI vs domain mediator,
Chain of Responsibility as a middleware variant, queue-level circuit breaking) and the newly earned
patterns (§3.11–14 — Chain of Responsibility, Bridge, Visitor, Composite) are synthesised from the
classic Gang of Four definitions as commonly explained in public references (refactoring.guru-style
catalogues, standard GoF summaries), restated in this file's own mechanism-plus-consequence voice rather
than paraphrased from any single source. §5's naming entries (§5.11–15) are original to this repo's own
review conventions (suffix-as-promise, naming drift, test-name-for-behaviour, one-term-per-shape,
no-pattern-word-in-variable-names). Nothing here reproduces the marketplace catalogue read at
2026-08-11/09-09 — that pass is cited above for §4 only, and this pass touches every section except §4.
References-block total: 6,567 → 8,590 words.

**Status unchanged.** §1, §2, §3 and §6 are still this repo's own review history plus synthesis from
public sources, not from any installed catalogue's own text — the widening pass adds volume in the same
voice, not a new kind of source.

**Widening, 2026-09-10 — 2ème passe.** §3, §5 and §6 were the three least-enriched files after the
pass above (§1, §2 and §4 already carried more depth per point); each gained six new numbered points,
appended after the existing ones without renumbering anything already cited elsewhere in the repo. §3
gained four newly earned patterns synthesised from the classic Gang of Four definitions as commonly
explained in public references (refactoring.guru-style catalogues, standard GoF summaries) — Iterator
(§3.15), Factory Method distinguished from named constructors already covered at §4.12 (§3.16),
Specification (§3.17), Proxy at a real access boundary distinct from the memoization already covered at
§2.13 (§3.18) — plus Observer earned beyond the framework event bus already covered at §2.2 (§3.19) and a
point on two earned patterns commonly co-occurring (§3.20). §6 gained six points on failure modes this
repo's own review history keeps producing but had not yet written down: eroded institutional knowledge as
its own deletion trigger, cosmetic renames used to dodge the deletion test, test setup cost exceeding the
isolation a pattern was meant to buy, observability tooling as a hidden dependency on a pattern's own
names, public/cross-repo interfaces needing a deprecation cycle rather than a same-diff deletion, and a
stack migration carrying a stale abstraction across by default (§6.17–22). §5 gained six points on naming
hygiene not yet covered: pattern names inside error messages and user-facing strings, IDE renames that
silently invalidate an ADR, one class wearing two pattern roles, blame-history stability across cosmetic
renames, and a borrowed-glossary synonym being as misleading as no name at all (§5.16–21). Nothing here
reproduces the marketplace catalogue: every point is either restated from this file's own existing
vocabulary (§1–§2's terms cited, not copied) or synthesised from the public GoF/refactoring-literature
sources named above, in this file's own mechanism-plus-consequence voice. References-block total (six
sections, origin.md excluded): 8,590 → 9,531 words.

**Status unchanged.** §3, §5 and §6 remain this repo's own review history plus public-source synthesis,
not text read from any installed catalogue.
