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
`laravel-conventions` §4 and §8 both cited `skills/design-patterns` §7 for the transaction-boundaries
rule, and this block has never had a §7 — the rule is §4.7. Wrong since those lines were written, and
found by resolving every reference rather than by reading.

**Status.** 🟡 — the GoF catalogue and the org catalogue's triggers are solid sources, and §1, §2, §3 and
§6 are ours: written from what this repo's own review history keeps producing rather than from a source
that could be re-checked. Depth does not change that.
