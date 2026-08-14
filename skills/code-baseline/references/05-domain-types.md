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
4. **What to share instead**: genuine commonality goes through behaviour — a shared interface, a trait, a
   value object — never a fused type.
5. **What genuinely is shared**: a real single concept reused (`Money`, `Address`, `DateRange`), and
   **cross-cutting technical types** — ids, timestamps, audit fields, pagination wrappers, soft-delete flags.
   Those aren't domain concepts; share them freely.
