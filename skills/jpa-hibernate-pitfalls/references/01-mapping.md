# jpa-hibernate-pitfalls §1 — Mapping

Each rule says what the mapping does silently when it is missing. Hibernate ORM 7.4 user guide unless
another source is named; the annotations are the `jakarta.persistence` ones.

## 1.1 Fetch type and association shape
1. **Map every association lazy, including `ToOne`.** The Jakarta Persistence default is eager for
   `@ManyToOne` and `@OneToOne`, a legacy of the first specification not assuming every provider could
   proxy. The Hibernate guide calls eager fetching almost always a bad choice: it cannot be turned off for a
   single query, so the association is loaded whether or not the caller needs it, and when a JPQL query
   forgets the join fetch Hibernate runs a second statement per row, which is an N+1 you did not write.
   Say `fetch = FetchType.LAZY` on every `ToOne`. Load what a use case needs in its query (§2).
2. **A parent-side `@OneToOne` is not lazy without help.** It needs bytecode enhancement, otherwise it is
   fetched even when marked lazy. Prefer a `@OneToOne` mapped with `@MapsId` so the child shares the parent's
   primary key and can be fetched by that key.
3. **Use a `Set` for a to-many association you fetch or modify.** The guide's performance chapter says that for
   unidirectional collections `Set` produces the most efficient SQL, and for an element collection a bag (an
   unordered `List`) is the least efficient. A `List` without an order column is treated as a bag.
4. **Prefer bidirectional to unidirectional one-to-many,** with the `@ManyToOne` side controlling the
   association. Treat `@ManyToMany` as rarely right: it behaves as two unidirectional associations. Map the
   link table as an entity with two `@ManyToOne`, so the link can carry its own columns and lifecycle.
5. **Keep both sides of a bidirectional association in sync in code.** Hibernate only reads the owning side.
   Put `add` and `remove` helper methods on the parent that update both ends, and make the child's
   `equals`/`hashCode` stable enough that `remove` works (§1.3).
6. **Be careful with cascade and orphan removal on shared children.** `orphanRemoval = true` deletes the child
   row when it is dropped from the parent's collection, so it is only right when the parent owns the child
   exclusively; cascading deletes also cannot be ordered parent-and-child for JDBC batching, so they can
   defeat it. Do not cascade from a `@ManyToOne` to its parent.

## 1.2 Identifiers and batching
1. **Use a sequence for the id when the database has one.** `IDENTITY` forces the row to be inserted before
   the id is known, and the guide states that the IDENTITY generators disable JDBC batching for inserts.
   Fall back to `IDENTITY` only for a database without sequences.
2. **With a sequence, keep the pooled optimizers** (the default since Hibernate 5): they cut round trips when
   several entities are written in one transaction. The `TABLE` generator performs poorly because it emulates
   a sequence with a separate transaction and row locks; avoid it.
3. **Assign ids to what you must put in a `Set` before it is saved,** or give the entity a business key
   (§1.3), because a generated id does not exist until persist or flush.

## 1.3 equals and hashCode on entities
1. **Do not implement them unless you need them.** The guide's advice is that outside one absolute case (a
   class used as an identifier, which must compare by its id values) you may want to consider not
   implementing them at all. Inside one session Hibernate already returns the same instance for the same row.
2. **You need them when entities leave the session** (detached) or sit in a `Set` before being saved.
3. **Never base them on a generated id read before it is set.** The guide shows the failure: a transient
   entity added to a `Set` has no id, gets one at commit, its hash changes while it is in the set, and
   `contains` then returns false. The contract of `Set` says the hash must not change while a member.
4. **Base them on a natural id or a business key,** or on an id assigned before the entity is added. Never on
   all fields: the fields change, the same problem as above.
5. **Do not let `toString` walk a lazy association.** It triggers loading, or throws when the session is
   closed (a practitioner rule from a JPA-patterns skill, not from the guide).

## 1.4 Enums and values
1. **Store an enum by name, not by position.** `@Enumerated(EnumType.ORDINAL)` writes the constant's
   position as an integer, so reordering or inserting a constant silently remaps every stored row. Use
   `EnumType.STRING`, or a lookup table or a stable code with a converter. The Error Prone documentation
   gives the same stability argument for any use of an ordinal outside persistence.

## 1.5 Optimistic locking
1. **Put a `@Version` field on rows that two users can edit.** The version column lets the persistence layer
   detect a conflicting update and prevent the loss of updates under a last-commit-wins strategy. Application
   code is forbidden from changing the value; to force an increment use the lock modes. Surface the
   conflict to the caller as a retry or a message; do not catch and overwrite.
2. **A bulk `update` does not touch the version column** unless you write `update versioned` (HQL), so an
   entity loaded before the bulk statement can be saved over it without a version conflict (§2).

## 1.6 Checks
- Grep for `fetch = FetchType.EAGER` and for `@ManyToOne` or `@OneToOne` with no fetch attribute.
- Load one row in two sessions and update it in both: the second commit fails on the version.
- A test that loads an entity in one session and a copy in another and puts both in a `HashSet` agrees with
  what the domain means by the same entity.
- Reorder the constants of every persisted enum in a scratch branch; no stored value changes meaning.
