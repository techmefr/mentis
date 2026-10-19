# § 1 — Types and names

> Section 1 of `skills/sql-conventions`. Read it when a table or column is created or changed. A type is a
> promise about what the value means; the wrong one is silent until the data is wrong, and a type change on a
> live table is a migration (§5), not an edit.

1. **Store a point in time as a timestamp with time zone, on PostgreSQL.** That type records one moment
   (internally normalised, displayed in the session's zone) and does the right arithmetic across zones and
   across daylight-saving changes. The type without a zone stores a calendar-and-clock reading with no
   meaning of its own; keeping UTC values in it works only while every writer and reader remembers the
   convention. Use the zone-less type only for something that really is a wall-clock reading with no
   location. The time-of-day-with-zone type has no sensible use; the zone-less alternative for a date alone
   is the date type.
2. **Do not give a timestamp column a precision, least of all zero.** It rounds the fraction instead of
   truncating it, so storing the current time can store a moment up to half a second in the future. Truncate
   explicitly in the query when you want whole seconds.
3. **Money and exact decimals are exact-decimal types, with the currency beside them.** Floating-point types
   are inexact by design. The engine-specific "money" type on PostgreSQL ties its meaning to a locale
   setting, mishandles fractions of the minor unit, and stores no currency; use a numeric type with an
   explicit precision and scale, and a currency column (or a currency-per-table rule written down).
4. **Text: use the unbounded text type by default on PostgreSQL.** The manual states there is no performance
   difference between the bounded, unbounded and text types apart from the extra check on a bounded column,
   and that the padded fixed-width type is usually the slowest. A length limit chosen arbitrarily
   (a surname column of twenty characters) is a production error waiting for a long name; when a real limit
   exists, a check constraint expresses it and can express more (a minimum, an allowed character set). The
   bounded type is right when you do want the engine to refuse long values or you need standard-SQL
   portability. This rule is engine-specific: on other engines a length can matter for indexing (§7).
5. **Identity columns, not the legacy auto-increment pseudo-type, on PostgreSQL 10 and later.** The legacy
   serial types carry odd behaviour around ownership, permissions and dependencies that the identity column
   fixes. Gaps in the sequence are normal (rollbacks and crashes leave them) and are never a defect to repair.
6. **Choose identifiers for how they will be used.** A 64-bit integer identity is compact and orders by
   insertion. A UUID is right when ids are generated outside the database, merged across systems or must be
   opaque; prefer a time-ordered variant, because a random one scatters inserts across the index (on a
   clustered primary key this also fragments the table, §7.1). PostgreSQL 18 provides a time-ordered UUID
   generator; earlier versions have only the random one built in, so state the version.
7. **Name with lowercase letters, digits and underscores.** PostgreSQL folds unquoted names to lowercase, so a
   mixed-case name works only if every tool quotes it every time, and tools disagree. A readable heading in a
   report is an alias in the query, not a column name.
8. **A closed, small, stable set may be an enumerated type; a set the business evolves is a column plus a
   constraint or a lookup table.** A value list baked into the schema's type system
   changes only through a schema change, which is a migration (§5) for what is really a business decision.
   Statuses that product decisions keep changing do not belong there (`skills/laravel-no-db-enums` is the stack-level statement of the
   same rule).
9. **A semi-structured column is for what is genuinely optional or variable, and the core relations stay as
   columns.** On PostgreSQL prefer the binary JSON type to the text one: it is processed faster and indexable,
   and the text type is needed only when key order or duplicate keys must be preserved. A JSON column that
   every query reaches into by the same path wants that path promoted to a real (or generated) column and
   indexed (§3.5). A check that the value is an object (or an array) keeps a stray scalar out.
10. **Booleans are not-null booleans unless a third state is real,** and a third state gets its own name
    rather than a null that readers must interpret.

**Sources:** the PostgreSQL manual (character types, JSON types, UUID functions, CREATE TABLE) and the
PostgreSQL community "don't do this" list (timestamps, precision, money, char/varchar, serial, mixed-case
names), read 2026-10-02; vendor-published design guidance (Apache-2.0 and MIT) for the table-design defaults.
Version-bound: the time-ordered UUID generator exists from PostgreSQL 18; identity columns from 10.
