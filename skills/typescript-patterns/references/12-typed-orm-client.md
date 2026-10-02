# typescript-patterns §12 — A typed database client (Prisma)

> Section 12 of `skills/typescript-patterns`. Read it when code calls a generated, schema-derived database
> client: a query result is typed, a filter is built from a variable, an error from the client is caught, JSON
> is read from a column, or the client's version is chosen. The other sections and the guardrails stay in
> `SKILL.md`. Pinned to **Prisma ORM 7** (documentation read 2026-10-02, `references/origin.md`); the
> schema, migration and transaction rules for a Nest service stay in `skills/nestjs-node-conventions` §4.

1. **Know which major the project is on, and that the registry's tags disagree.** On 2026-10-02 the library
   package's `latest` tag was 7.10 while the command-line tool's `latest` tag pointed at an 8.0 release candidate,
   and the 8 line's own page says general availability is expected in October 2026. Version 8 is two packages
   (the tool, and one library per database) with their own version numbers, renames the schema file to a
   contract and generating the client to emit, and does not yet offer client extensions, filtering inside JSON
   columns, atomic increments, most nested writes, transaction isolation levels or the code-based error
   classes of rule 6. Version 7 is supported 18 months after 8 reaches general availability; version 6 gets
   security patches only, until 2026-11-19. Install the major deliberately and read the matching page tree.
2. **Derive result types from the query, never retype them.** Declare the query arguments once as a constant
   that `satisfies` the model's generated default-arguments type, then take the result type from the generated
   payload helper applied to that constant; the type then follows both the schema and the query. For a function's
   result, `Awaited` of its `ReturnType` does the same. A hand-written "user with posts" interface drifts the
   first time the schema changes, and the compiler no longer tells you.
3. **Fetch what you need: by default you get every scalar field and no relations.** `select` narrows to named
   fields (and nests into relations); `include` adds relations to the full scalar set; `omit` removes fields from
   the default set, per query or once on the client for the whole model (a password hash is the standard case).
   A response type that must not carry a field is made by the query, not by deleting the field afterwards.
4. **`undefined` means "do nothing", `null` is a value.** A filter whose value is `undefined` is dropped from the
   query: `deleteMany({ where: { id: maybeId } })` with an undefined id deletes every row, and an update with an
   undefined field leaves it unchanged. The docs' own remedy is the strict-undefined-checks preview option, under
   which an explicit `undefined` throws and a `skip` symbol states "leave this out" on purpose; pair it with the
   exact-optional-property-types compiler option (§6.2) so the compiler objects first. Without the preview option,
   a bulk write or delete never takes its filter straight from an optional input: check it is defined, or
   fail, before building the query.
5. **Use the checked input form unless you need the other.** Each create or update accepts a "safe" input that
   sets a relation through its relation field (connect, create, or connect-or-create) or an "unchecked" input that
   sets the foreign-key scalar directly; one call uses one form, not a mix. The relation form gives a more
   descriptive error when the target is missing.
6. **Narrow a client error before reading its code.** The client throws five classes: a known-request error with
   a code, an unknown-request error, an engine-panic error (restart the client or the process), an
   initialisation error (startup or connection) and a validation error (a query shape the client rejects). Check
   the class with `instanceof` against the one exported from the generated namespace, then branch on the
   code (unique violation P2002, foreign-key violation P2003, record required but not found P2025, write
   conflict or deadlock to retry P2034), and rethrow everything not handled (§4). A catch that reads a code off
   an unnarrowed value is the pattern §4 forbids.
7. **One client per process.** Creating a client per call or per request opens a new connection pool each time
   and can exhaust the database's connections, especially serverless or under hot reload; export one instance
   from one module (with the usual single-instance guard in development). The client connects on the first
   query; connect explicitly only to move the cost to start-up; do not disconnect after each request. Disconnect
   in a short-lived script, or one embedded in a long-running process that would otherwise hold the pool.
8. **The loop is the N+1.** A query per row, or per parent, is the slow path: fetch the relation in the parent
   query with `include` or a nested `select`, or let the client batch single-record lookups made in the same
   tick through its fluent relation API. Large writes go through the bulk methods (create-many, update-many,
   delete-many and their return-the-rows forms) in batches, not through one call per row. The join-based relation
   load strategy exists for PostgreSQL but is a preview option in 7; do not rely on it without enabling and
   testing it.
9. **A JSON column is untrusted input at the type level.** Its type is the union of all JSON values. The docs
   narrow with `typeof` and `Array.isArray` and then assert to the client's JSON array or object type; do not stop
   there, because an assertion proves nothing about the shape inside. Parse the value with a schema validator at
   the repository boundary (§7) and hand the rest of the program a real type. Use a JSON column for data with no
   consistent structure; use related models for data you query by field.
10. **Keep the client behind a boundary.** Repositories, a data module or a query layer return domain types or the
    derived payload types of rule 2, not raw client calls scattered through handlers; this is where errors from
    rule 6 become the application's own, and where the client's major can change without touching callers.
