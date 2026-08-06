---
name: java-conventions
description: Use when writing or reviewing Java, typing/immutability (records, Optional), error handling (checked vs unchecked), concurrency, common Spring patterns. No internal Xefi production experience on this language, sourced from established market conventions (Effective Java, Spring) and tooling (SpotBugs/Error Prone).
---

# java-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Java code. **Special status**:
like `go-conventions`/`python-conventions`, no Xefi production experience behind this block yet: content
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

## Output / checkpoint
Code compliant with the four sections above (section 4 only if Spring), and SpotBugs/Error Prone with no
new finding introduced by the diff. Checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. This block hasn't been confronted with a real production Java project
at Xefi yet: if a rule here diverges from a real observed need, fix this block rather than treating it as
settled.

## Origin
Ideas taken from: Effective Java (Joshua Bloch, immutability, `Optional`, checked vs unchecked),
SpotBugs/Error Prone (default static rules), established Spring conventions (constructor injection, DTO
vs entity). Mechanisms rewritten, no copied text. Market research, no internal production feedback at
this stage: same status as `go-conventions`.
