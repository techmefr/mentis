---
name: java-conventions
description: Use when writing or reviewing Java, typing/immutability (records, Optional), error handling (checked vs unchecked), concurrency, common Spring patterns. No in-house production experience on this language, sourced from established market conventions (Effective Java, Spring) and tooling (SpotBugs/Error Prone).
---

# java-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Java code. **Special status**:
like `go-conventions`/`python-conventions`, no in-house production experience behind this block yet: content
coming from established conventions (Effective Java) and deterministic tooling (SpotBugs, Error Prone),
not from real review feedback.

## When
As soon as Java code is written or modified, during `code` (6) or `tdd` (5).

## Steps

### 1. Immutability and typing
1. `record` (Java 16+) for any simple immutable data (DTO, value object) rather than a class with manual
   getters/setters.
2. `final` fields by default, mutability only if genuinely necessary.
3. `Optional<T>` as a return type for a legitimate absence, never as a method parameter or a class field
   (a source of pointless complexity, the Effective Java consensus).
4. Avoid returning `null` from a public method when `Optional` or an exception expresses the real intent
   better.
5. **`equals`/`hashCode` are overridden together, never one without the other.** Overriding `equals` alone
   breaks the contract every hash-based collection (`HashMap`, `HashSet`) relies on: two objects that
   `equals()` says are the same must return the same `hashCode()`, or the object silently can't be found
   in the collection it was just put into.
6. **A class is `final` unless it was designed to be extended**, with its overridable methods documented.
   An open class nobody meant to subclass is an invitation to override a method whose invariants weren't
   written for it — favour composition (a field holding the collaborator) over inheritance when the goal
   is reusing behaviour, not modelling an "is-a" relationship.

### 2. Error handling: checked vs unchecked
1. An *unchecked* exception (`RuntimeException`) for a programming error (violated precondition),
   *checked* for a recoverable error the caller has to handle explicitly: don't turn every exception into
   an unchecked one out of convenience.
2. A `catch` that swallows the exception without rethrowing or logging it hides a real bug: never silent.
3. `try-with-resources` for every `AutoCloseable` resource (file, connection): never a manual close in a
   hand-written `finally` when `try-with-resources` covers the case.

### 3. Concurrency
1. A collection shared between threads: `java.util.concurrent` (`ConcurrentHashMap`, etc.) rather than a
   standard collection synchronised by hand case by case.
2. `synchronized` on the shortest possible block, never on a whole method out of reflex when only a
   critical section needs it.
3. `ExecutorService` with a sized pool that's explicitly shut down (`shutdown()`), never a raw `Thread`
   created on the fly with no lifecycle management.

### 4. Common Spring patterns (if applicable)
1. Constructor injection, never field injection (`@Autowired` on a field): it makes the dependencies
   explicit and testable without reflection.
2. A DTO distinct from the JPA entity exposed in the API: never the persisted entity directly at the API
   edge (coupling of the DB schema to the public contract).
3. Transactions (`@Transactional`) placed at service level, never at controller level: the controller
   shouldn't know about the transactional boundary.
4. **A JPA relationship defaults to `FetchType.LAZY`**, never `EAGER` out of convenience: `EAGER` loads
   the association on every fetch of the owning entity whether the caller needs it or not, and a
   collection mapped `LAZY` but iterated inside a loop is the classic N+1 — load it explicitly (a fetch
   join, an entity graph, or a dedicated query) at the call site that actually needs it.

## Output / checkpoint
Code compliant with the four sections above (section 4 only if Spring), and SpotBugs/Error Prone with no
new finding introduced by the diff. Checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. This block hasn't been confronted with a real production Java project
in house yet: if a rule here diverges from a real observed need, fix this block rather than treating it as
settled.

## Origin
Ideas taken from: Effective Java (Joshua Bloch, immutability, `Optional`, checked vs unchecked),
SpotBugs/Error Prone (default static rules), established Spring conventions (constructor injection, DTO
vs entity). Mechanisms rewritten, no copied text. Market research, no internal production feedback at
this stage: same status as `go-conventions`.

Re-checked directly against Effective Java's item list on 2026-08-10: the `equals`/`hashCode` contract
(§1.5) and final-by-default/composition-over-inheritance (§1.6) were real gaps, now closed — both are
judgment calls a linter doesn't reliably force (SpotBugs flags an inconsistent pair if it can see both
methods, but not a class that's extensible by omission). The builder-for-many-parameters and enum-
singleton items were left out: the first is already covered generically, cross-language, by
`design-patterns`' object-construction entry condition; the second is a niche idiom with no real case
behind it yet in any stack this roster serves. §4.4 (JPA lazy loading / N+1) closes the same gap
`python-conventions` §7.3-4 already covers for its ORM — Java/Spring had nothing on it.
