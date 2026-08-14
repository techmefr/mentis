---
name: design-patterns
description: Use when reaching for a named design pattern (Factory, Strategy, Observer, Repository) or reviewing code that has one, to check the structure earns its name.
---

# design-patterns

Steps 3 (`archi`) and 6 (`code`) of the pipeline (`WORKFLOW.md`), and a reading angle during `review`.

The classic catalogue is 22 patterns across three families. Every one of them was extracted from code
that already existed: they are **names for structures people kept rediscovering**, not a menu to order
from. Read as a menu, the catalogue reliably produces the thing `over-engineering-review` tags as
`over-abstraction` — with the difference that a named pattern is harder to delete, because it looks like
a decision.

The useful skill here is subtraction. Two thirds of the catalogue is already in the framework you're
using, and naming a structure you don't have yet is how a one-caller interface gets built.

**Relation to an org skill catalogue.** Where a company ships per-pattern implementation skills with
language-specific references, those are the authority on **how** to shape each pattern in that house style.
This block owns **whether to reach for one at all**, plus the entry conditions below — the trigger that says
a given pattern is now earned. Where such a catalogue is installed, follow its shape and this block's
threshold.

**Applying an override is silent.** Write the code the governing rule actually requires and move on — never
report "a conflict between mentis and the house catalogue" to whoever's watching. That framing reads as
broken to a non-technical stakeholder even when the case is a normal, resolved one, and has already caused a
real project to get abandoned and restarted over nothing. Surface it as a specific, named question only when
no rule anywhere actually resolves the case — never as a general alarm.

## When
When about to introduce a pattern by name; when a design discussion produces one as an answer; when
reviewing code that names one; when the same shape has appeared for the third time and needs a name.

## Steps

### 1. Recognise, don't apply
1. **A pattern earns its name after the structure exists**, not before. If the code already has three
   interchangeable behaviours behind one call site, that's a Strategy — naming it helps everyone read it.
2. **If it doesn't exist yet, you're predicting.** That's `yagni` (`over-engineering-review`), and the
   pattern name is the disguise.
3. **The threshold is the second real case**, in the code, today. Not a plausible one. Same rule as
   `when-stuck`'s three-occurrence threshold for extracting an abstraction.

### 2. Check the framework doesn't already do it
This is where most of the catalogue goes. Before writing one, look for what's already there:
- **Object construction and wiring** — the DI container resolves and configures. A hand-written factory
  usually reimplements it with less capability, and a hand-written **Singleton** replaces a managed
  lifetime with a hidden global that tests can't reset.
- **Notification / decoupling** — the framework's events, listeners and queued jobs are Observer and
  Command, already instrumented and already testable.
- **Wrapping behaviour around a call** — middleware, pipelines and interceptors are Decorator when each
  layer always runs and adds behaviour; the same stack is **Chain of Responsibility** when a layer can
  decide to short-circuit (an auth guard that stops the chain, a handler that claims the request and the
  rest never runs). Framework middleware already gives you both; naming which one you mean only matters
  in the ADR, not in new code.
- **Interchangeable behaviour** — in a typed language, a map of functions or a discriminated union does
  what a Strategy class hierarchy does, in a fraction of the lines. Reach for classes when the behaviours
  carry state. The same discriminated union with an exhaustive `switch`/`match` is also what **Visitor**
  buys in an untyped OOP language (dispatch per node type without touching the node classes) — the
  compiler's exhaustiveness check is the "you forgot a case" guarantee Visitor exists to give you.
- **Iteration, state machines, templates** — generators/iterables exist; and a state machine is better
  modelled as data (`domain-modeling` §states-not-flags) than as a class per state.
- **Cloning** — `structuredClone`, object/array spread, `Object.create`, PHP's `clone`: **Prototype** is
  the language, not a pattern to hand-roll.
- **Reactivity and composition** — Vue's `ref`/`reactive` already are a **Proxy** (JS `Proxy` under the
  hood: property access is intercepted to track dependencies); the component tree, parent and child
  addressed the same way through props/slots, already is a **Composite**. Writing either by hand on top
  of the framework duplicates what it does for free.
- **Rarely earned in a GC'd web app**: **Flyweight** (sharing state to cut memory pressure) is a
  rendering-engine/game-dev answer to a problem the garbage collector already solves at our scale; if
  you're reaching for it, measure the allocation first (`sparks`), don't assume it.

**A Repository over an ORM is the recurring local case.** It pays only when there's a genuine second
implementation or a real intention to swap the store. Otherwise it's a one-caller wrapper over an API
that was already the abstraction, and it hides the query optimiser you'll want later (`tank`).

### 3. Where they do earn their place
Not a rejection of the catalogue — the cases that hold up in our stacks:
1. **Adapter and Facade at a third-party boundary.** This is rule B in code: an external API gets one
   wrapper we own, so a breaking change upstream is one file. Even here, one caller is fine — the
   justification isn't reuse, it's containment.
2. **Strategy when the branches are real and growing**, and each has its own tests.
3. **Builder when construction genuinely has many optional parts** and the alternative is a constructor
   nobody can read.
4. **Command when work must be queued, retried or audited** — usually meaning the framework's job
   abstraction (`background-jobs-conventions`).
5. **State when the transitions are the domain** and getting them wrong is the bug you're preventing.
6. **Mediator when components must stay decoupled from each other, not just from the framework** — a
   central event bus/store two features go through instead of importing each other directly. It earns
   its place once a third participant needs to react to the same event; two callers with a direct
   reference are simpler and don't need it.
7. **Memento when the requirement is explicitly "undo" or "restore a previous state"** — a multi-step
   wizard's back button, a draft auto-saved before an edit, an optimistic UI update rolled back on a
   failed save. Without that explicit requirement, don't snapshot state "just in case".

### 4. The ones with a concrete entry condition
For these, the trigger is mechanical enough to state — which is what makes them reviewable rather than a
matter of taste. Each still passes §1's second-real-case threshold first.

1. **Strategy** — a `switch`/`match` on a `type`/`channel`/`provider`/`mode`/`kind` field with **3+ branches
   that keeps growing**, or sibling classes differing only in one method. The axis of variation must be
   **one**: two axes means you're about to build a matrix, and a map of functions keyed by the pair is
   smaller. Each strategy owns its tests. **Bridge** is the rare legitimate answer when both axes are real,
   growing independently, and each side already has several implementations (e.g. a notification
   abstraction with multiple channels *and* multiple formatters) — splitting into two hierarchies that
   compose beats a matrix of concrete classes. It's an escape valve for when the map-of-functions above
   stops being smaller, not a default.
2. **State** — one object moves through **named statuses** (`pending` → `approved` → `paid` → `refunded`) and
   its behaviour shifts at each step, with the `if`/`match` on that field repeated across **several**
   methods. The trigger is the repetition, not the existence of a status field: a status read in one place is
   a status field, not a state machine. What you're really buying is that an invalid transition becomes
   unrepresentable — if the transitions don't matter, this is over-abstraction.
3. **Null Object** — the same "is this collaborator absent?" branch repeats (`if ($logger)`, `if ($user)`,
   optional constructor arguments defaulted to null, a lookup returning null for an unknown key, a
   guest/anonymous case). Substitute an instance that does nothing, so the caller stops asking. It pays when
   the branch is **repeated**; a single null check is a null check.
4. **Object construction** — the honest answer to "this constructor has too many parameters", and the
   smallest fix wins: a **parameter object** (group the ones that travel together), a **named constructor**
   (`::fromX`, a `from_x` classmethod) when there are several distinct valid ways to build the thing, a
   **readonly class / dataclass / validated model** when it's really a value, and a **fluent builder** only
   when construction genuinely has many optional parts. Reach for the builder last: it's the most code and
   the least type safety of the four. Decide it **while the signature is being written** — reworking an
   existing wide constructor unprompted is `simplify`'s territory, not this one's.
5. **Value Object** — a domain value travels as a bare primitive: money as a float, an amount and a
   currency as two separate parameters nothing keeps together, the same email/phone/IBAN shape validated at
   2+ call sites, a start/end pair nothing keeps ordered, or raw ids from different tables passed
   interchangeably because they're all just integers. Wrap it in a small immutable value object that
   enforces its invariant **once**, in its constructor, instead of at every call site that touches it. Money
   is never a float — that one is close to a hard rule, not a judgment call.
6. **Pipeline** — one payload passes through an **ordered sequence of independent steps that keeps
   growing** (import, ETL, validation-then-enrichment, checkout) — model each step as a named stage class
   behind one interface, with an explicit ordered list, before the third step lands. The mechanical
   counter-trigger matters as much as the trigger: a **fixed** three-step sequence that will never grow is
   three named method calls in order, not a Pipeline — the abstraction has to earn its indirection against a
   growing list, or it's ceremony around three lines. Refactoring an existing god-method into one is
   `simplify`'s territory, not a drive-by here.
7. **Transaction boundaries** — a single business operation performs **two or more writes that must succeed
   or fail together** (create a parent then its children, decrement stock after creating an order,
   multi-model writes in one action). One explicit transaction wraps **all** of that operation's writes, and
   the boundary sits on the action/use-case — never on the model, never on the controller. Side effects that
   aren't the database (mail, an outbound HTTP call, a queue dispatch, a broadcast event) move **outside**
   the transaction and fire only after commit — inside it, a slow vendor call holds the lock, and a
   rolled-back transaction can't un-send an email. Not for a read-only path, a single atomic statement, or
   code that's already inside a caller's transaction.

### 5. If you use the name, use it correctly
1. **A misnamed pattern is worse than an unnamed structure.** "Factory" on something that isn't one
   sends every future reader looking for indirection that doesn't exist.
2. **Name it in the code or in the ADR, once** — not in a comment (`documentation-adr` §1.2, and no
   comments where the naming can carry it).
3. **When a pattern is deliberately not used**, and someone will wonder why, that's a line in the ADR
   (`documentation-adr` §4).

## Output / checkpoint
No separate checkpoint: this feeds `archi`, `code` and `review`. What it owes at review time — for every
named pattern in the diff, the second real case exists, the framework doesn't already provide it, and the
structure is smaller with the pattern than without. Failing any of the three, it's a
`simplify` candidate.

## Guardrails
- **Never introduce a pattern before the second real case.** "We'll need it" is the whole failure mode.
- **Never hand-roll what the container, the event bus or the middleware stack already does.**
- **Apply the net-line test** (`over-engineering-review`): if the pattern adds lines and removes none,
  it bought nothing today.
- **Never let a pattern name end a design discussion.** It's a label for an answer, not the answer.
- Don't refactor working code purely to make it match a pattern.

## Origin
The catalogue itself is the classic Gang of Four set as published on the widely used
`refactoring.guru` reference — 5 creational, 7 structural, 10 behavioural patterns, verified 2026-08-06.
Its catalogue pages describe when each pattern applies and carry **no caution about overuse**, which is
the gap this block exists to fill: taken at face value, a catalogue is read as a menu.

Section 4's entry conditions come from **an org skill catalogue's per-pattern skills** (state, strategy,
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
