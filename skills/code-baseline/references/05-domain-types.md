# code-baseline §5 — Domain types

> Section 5 of `skills/code-baseline`. Read it when two distinct concepts share a primitive type. The other sections and the guardrails stay in `SKILL.md`.

1. **Distinct domain concepts stay distinct types**, even when structurally identical today. Two status enums
   sharing four values are two enums.
2. **Because they diverge.** Invoice statuses and order statuses look alike until one grows `refunded` and
   the other `returned`; then the shared type admits states each consumer must defensively ignore, and adding
   an order-only value re-tests and re-reviews every invoice consumer. A `Status` that means two things also
   can't be read locally — you must know which domain you're in first.
3. **The smells**: a generic name (`Status`, `Type`, `Kind`, `State`) shared across unrelated domains; one
   enum whose values are partitioned by a comment; domain-B fields added to a model named after domain A;
   **nullable columns that only apply to one subtype** (half the rows always null — that row is really two
   row-types crammed into one table); a method or foreign key that only makes sense for some rows; and a
   `match` with arms for values that "can't happen here".
4. **Two identifiers of the same primitive type are interchangeable to the compiler.** Passing an account id
   where a user id was expected typechecks, runs, and returns somebody else's data — the failure is a data
   one, discovered by a customer rather than by a build. Where that swap is plausible and the consequence is
   real, a distinct type around the identifier costs one declaration and closes it permanently.
5. **A validated value is validated once.** An email, a URL, an IBAN or a phone number carried as a bare
   string means every consumer either re-checks it or assumes someone else did, and both happen in the same
   codebase. A value object that refuses to exist in an invalid state moves the check to one constructor, and
   everything downstream is then entitled to trust it.
6. **The unit belongs in the type.** A parameter named `timeout` is seconds to whoever wrote it and
   milliseconds to whoever calls it, and the resulting bug is a factor of a thousand that looks like a
   network problem. The same applies to a distance, a weight, a percentage stored as `0.2` or `20`, and a
   date that may or may not carry a timezone.
7. **Money is an amount and a currency, and never a float.** Binary floating point cannot represent a
   decimal cent, so sums drift and comparisons fail on values the user can see; and an amount without its
   currency gets added to another one eventually. This is the case where the primitive is not merely
   ambiguous but wrong.
8. **A pair of booleans encoding one state admits the impossible combinations.** `isActive` and `isArchived`
   allow both true and both false, so every reader has to decide what those mean and they decide differently.
   One enum with named states makes the invalid combinations unrepresentable, which is the same move as
   §5.1 applied within a single concept.
9. **A nullable field that carries two meanings carries neither.** "Never set" and "explicitly none" are
   different answers with different consequences — a discount not yet decided is not a discount of zero —
   and collapsing them into `null` means the distinction is reconstructed by guesswork at each call site.
10. **The wire format is not the domain type.** Reusing the internal model as an API payload or a queue
    message couples the two, so an internal rename becomes a breaking change for every consumer and a
    consumer's request becomes a domain edit. Keep a translation at the boundary (§4) even when the two
    shapes are identical today — which, by point 2, is a statement about today.
11. **An enum crossing a boundary serialises as its values**, so those values are a published contract:
    renaming one is a migration of stored rows and in-flight messages, not a refactor. That is worth knowing
    before the name is chosen, because it is the point at which the cost is zero.
12. **The storage shape is not the domain type either.** Deriving one from the other in either direction
    means a column rename is a domain change and a domain refinement is a schema migration. They evolve for
    different reasons and at different speeds; the mapping is cheap and the coupling is not.
13. **What to share instead**: genuine commonality goes through behaviour — a shared interface, a trait, a
    value object — never a fused type.
14. **What genuinely is shared**: a real single concept reused (`Money`, `Address`, `DateRange`), and
    **cross-cutting technical types** — ids, timestamps, audit fields, pagination wrappers, soft-delete flags.
    Those aren't domain concepts; share them freely.
15. **Where to stop.** Not every string deserves a wrapper, and a codebase where it does is unreadable for a
    different reason. The test is whether a wrong value *of the same primitive type* is plausible at a real
    call site and consequential when it happens: two ids, two currencies, two units, two statuses — yes. A
    label that is only ever displayed — no.
16. **A structurally identical type is not the same type, and a language that says otherwise is not
    agreeing with you.** Where the type system compares by shape rather than by name, two records with the
    same fields are mutually assignable, so points 1 and 4 have to be bought deliberately — a distinguishing
    field, a branded alias, a wrapper. Knowing which kind of type system you are in is what decides whether
    this section's rules are enforced by the compiler or by review.
