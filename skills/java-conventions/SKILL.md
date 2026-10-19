---
name: java-conventions
description: "Use when writing or reviewing Java: typing and immutability (records, Optional), checked versus unchecked errors, concurrency, common Spring patterns."
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
5. **A persisted enum is mapped by name, never by ordinal**: reordering the constants silently reinterprets
   every stored row. Collections on an entity are initialised, never null, and an entity changes through
   behaviour methods rather than public setters.
6. **Reads that need a collection use a fetch join, an entity graph or a projection** chosen at the call
   site; a read-only view returns a projection, not a managed entity.
7. **A transaction wraps the business unit at the service boundary.** The read-only flag is a hint, not
   write protection or authorisation. A participating call joins the outer transaction: an inner failure
   marks it rollback-only even if caught, and the outer commit then throws. A call to a transactional method
   of the same class bypasses the proxy and runs without it. A requires-new call takes a second connection
   (mind the pool) and is for records that must survive a rollback, such as an attempt log, not a success
   row for work that was rolled back. A local transaction does not make a write to another database or an
   HTTP provider atomic.
8. **Grouped settings bind to a typed, validated properties record**: registered explicitly, with units in
   durations and sizes, startup failing on a missing credential or endpoint, and no secret as a record
   component (a generated string form would print it). Test binding with an application-context runner,
   including an invalid value.

### 5. Tests
1. Three levels, readable from the file name: unit (one class, collaborators stubbed), integration (the
   container context, or a real database or cache in a container) and component (a whole module, only other
   modules stubbed).
2. **A component of the module under test is never mocked in a component test**: a mock asserts your guess
   about its behaviour and lets wiring bugs through. A store or client is tested against the real engine in a
   container, not a mocked driver, since atomicity and null handling are what a mock cannot have.
3. Method names read `method_whenCondition_shouldResult`, and the result names observable behaviour, not an
   implementation call. One test, one scenario; assertions with a fluent assertion library.
4. Test helper classes do not carry the suffix the test runner scans for, or the runner executes them.

## Output / checkpoint
Code compliant with the five sections above (section 4 only if Spring), and SpotBugs/Error Prone with no
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

**Extended, 2026-10-02** (§4.5-8, §5): rewritten from the MIT-licensed `rrezartprebreza/spring-boot-skills`
(persistence, transaction, configuration and test-pyramid skills of the Boot 3 set) and
`dmitriy-iliyov/java-agent-skills` (test-style), both read in full that day. Their test-layer percentage split,
given-when-then comments in tests and Lombok usage are left out (the first has no cited norm, the others clash
with the house no-comment rule). Sources target the Spring Boot 3 line: read the version in the build file
before applying §4 and §5 (`skills/source-freshness`). Not taken: package-level null-safety annotations
(version-dependent, not re-read), virtual threads and Maven audit (not read).
