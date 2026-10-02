# § 1 — Schema: naming, nullability, mutations, pagination, evolution

> Section 1 of `skills/graphql-conventions`. Read it when a type, a field, an argument, a mutation or a
> deprecation is written. Read 2026-10-02 from the GraphQL learning guides (naming and design standards, schema
> design, pagination, global object identification, schema change management). The guides call these
> conventions, not rules: deviate deliberately and write down why.

1. **Model the business domain as a graph, not the database.** Relationships are edges to objects, not
   foreign-key ids a client must resolve itself, and the schema reflects domain concepts rather than tables.
2. **Name consistently.** Fields, arguments and directives in camelCase; types, enums, interfaces and unions in
   PascalCase; enum values in SCREAMING_SNAKE_CASE. Boolean fields start with `is` or `has`; list fields are
   plural nouns; query fields describe the data and carry no `get` or `fetch` prefix, since the operation type
   already says it is a read.
3. **Pick one mutation naming pattern and keep it.** Verb-first reads naturally and fits non-CRUD operations;
   noun-first groups mutations by entity and suits large CRUD-heavy schemas. Consistency matters more than the
   choice, and a linter can enforce it.
4. **Mutation inputs end in `Input`; mutation results are payload types,** not the bare entity. A payload lets
   you add validation errors or related objects later without breaking existing clients.
5. **Decide nullability on purpose.** Every field is nullable by default because a field can fail alone without
   failing the request. Use non-null only where you can guarantee a value, knowing a non-null field that fails
   nulls its nearest nullable parent. A list field is `[Item!]!` so clients get an empty list, never null.
6. **Input nullability has three states** (omitted, explicitly null, a value), which matters for partial
   updates: decide how clearing an optional field is expressed and document it in the field description.
7. **Describe every type and every non-obvious field.** Descriptions appear in tooling and generated docs, so
   they are user-facing documentation.
8. **Use a custom scalar when a format has clear validation rules, is shared by several fields, or helps client
   code generation** (timestamps, dates, URLs, email). Do not mint one for a string with business rules
   (a username, a product code): enforce that in the business layer. Each custom scalar must be implemented in
   every client and server.
9. **Evolve the schema without versions.** Clients ask only for the fields they need, so adding fields, types,
   queries and mutations, adding optional arguments with a default that matches the old behaviour, or making a
   required argument optional is non-breaking. Removing or renaming a field, type or enum value, changing a
   type, making an optional argument required and making a non-null field nullable are breaking. Deprecate
   first, with a reason that names the replacement and when removal is expected, then remove only when usage
   data shows no client calls it. A new field is nullable unless every record can supply it.
10. **Paginate every list that can grow.** Use cursor connections: a connection type with edges, each edge
    holding a cursor and the node, and page information with the end-of-list flag and boundary cursors; the
    cursor is opaque so the backend can change how it paginates. Offset pagination has performance and security
    downsides and skips or repeats items when the data changes between requests. Small, static lists (reference
    data, enum-like tables) can stay plain lists; a list that might grow without bound starts as a connection.
11. **Expose a global object identifier if clients cache or refetch.** A `Node` interface with a single non-null
    `id`, globally unique so the server can refetch the object from the id alone, and a root `node` field that
    takes it.
12. **Lint the schema and diff it in CI** for naming rules and breaking changes, so the conventions above are
    checked by a tool and not by memory.
