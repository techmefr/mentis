# § 1 — Schema: naming, nullability, mutations, pagination, evolution

> Section 1 of `skills/graphql-conventions`. Read it when a type, a field, an argument, a mutation or a
> deprecation is written. Read 2026-10-02 from the GraphQL learning guides (naming and design standards, schema
> design, pagination, global object identification, governance and versioning). The guides call these
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
   nulls its nearest nullable parent. The `[Item!]!` list shape (an empty list, never null) is our choice; the guide's nullability section does not give it.
6. **Input nullability has three states** (omitted, explicitly null, a value), which matters for partial
   updates: decide how clearing an optional field is expressed and document it in the field description. Neither the three states nor this advice is on the mutations page; it is our guidance.
7. **Describe every type and every non-obvious field.** Descriptions appear in tooling and generated docs, so
   they are user-facing documentation. This is our guidance; the guides read do not discuss descriptions.
8. **Use a custom scalar when a format has clear validation rules, is shared by several fields, or helps client
   code generation** (timestamps, dates, URLs, email). Do not mint one for a string with business rules
   (a username, a product code): enforce that in the business layer. Each custom scalar must be implemented in
   every client and server.
9. **Evolve the schema without versions.** Clients ask only for the fields they need, so adding optional arguments to fields or making required
   fields optional is non-breaking; removing fields or types, changing a field's type and making a non-null field
   nullable are breaking (the guide's lists; that adding types, queries and mutations is safe, and that making an
   optional argument required or removing an enum value is breaking, are our extension). The guide discourages
   versions without forbidding them. Deprecate first, with a reason that names the replacement (a removal date is
   our addition), then remove only when tracked usage data shows it is safe. A new field is nullable unless every record can supply it.
10. **Paginate every list that can grow.** Use cursor connections: a connection type with edges, each edge
    holding a cursor and the node, and page information with the end-of-list flag and boundary cursors; the
    cursor is opaque so the backend can change how it paginates. Offset pagination has performance and security
    downsides on larger data sets, and its offsets become ambiguous when records are added between requests. The guide says fields that may return a lot of data should be paginated; that small static
    lists can stay plain is our reading.
11. **Expose a global object identifier if clients cache or refetch.** A `Node` interface with a single non-null
    `id`, globally unique so the server can refetch the object from the id alone, and a root `node` field that
    takes it.
12. **Lint the schema and diff it in CI** for naming rules and breaking changes, so the conventions above are
    checked by a tool and not by memory.
